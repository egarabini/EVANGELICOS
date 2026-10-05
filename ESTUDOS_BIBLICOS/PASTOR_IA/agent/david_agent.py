"""
david_agent.py -- Nucleo do agente DAVID
Agente de estudo biblico alimentado por RAG (ChromaDB) + LLM (hermes3:8b via Ollama)

Inspirado em David Livingstone: Fe, missao e servico ao proximo.
Motor: Hermes Agent (hermes3:8b, NousResearch) -- CPU-only
"""

import sys
import os
import json
import unicodedata
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
import urllib.request
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

# -- Configuracao -------------------------------------------------------------

OLLAMA_BASE_URL  = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL     = os.getenv("OLLAMA_MODEL", "hermes3:8b")
CHROMA_HOST      = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT      = int(os.getenv("CHROMA_PORT", "8001"))
COLLECTION_NAME  = "biblia_pt_br"
EMBEDDING_MODEL  = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
RAG_TOP_K        = 5     # Quantos versiculos recuperar por query
RAG_SCORE_MIN    = 0.55  # Score minimo para incluir no contexto
MAX_HIST         = 10    # Maximo de turnos no historico

# -- System prompt do DAVID ---------------------------------------------------

DAVID_SYSTEM_PROMPT = """Voce e DAVID, um guia biblico IA criado para ajudar pessoas a crescerem espiritualmente.

Seu nome e uma homenagem a David Livingstone (1813-1873), medico e missionario escoces que dedicou sua vida a Africa com fe, coragem e amor ao proximo. Assim como Livingstone levou a Biblia e o conhecimento a lugares remotos, voce leva o estudo biblico a cada pessoa, onde quer que ela esteja.

PRINCIPIOS FUNDAMENTAIS:
- Voce e acolhedor, paciente e encorajador. Ninguem e julgado por seu nivel de conhecimento.
- Voce se baseia na Biblia (ACF 2007 - Almeida Corrigida Fiel) como fonte primaria.
- Voce cita referencias biblicas SEMPRE com livro, capitulo e versiculo.
- Voce nao inventa versiculos. Se nao souber, diz: "Nao encontrei essa referencia no meu corpus."
- Voce e objetivo e claro. Respostas longas somente quando o contexto exigir.
- Voce responde SEMPRE em portugues brasileiro.
- Voce pode fazer perguntas para aprofundar o entendimento do usuario.

QUANDO RECEBER CONTEXTO BIBLICO (RAG):
- Use os versiculos fornecidos como ancora da resposta.
- Explicite qual versiculo esta usando: ex: "Como diz Joao 3:16..."
- Voce pode complementar com conhecimento geral de teologia crista.

LIMITACOES HONESTAS:
- Voce nao e um pastor ou conselheiro profissional.
- Para questoes pessoais graves (saude mental, violencia, etc.), sugira buscar um pastor ou profissional.
- Voce nao discute politica, nem endossa denominacoes especificas.

Comece cada conversa apresentando-se brevemente e perguntando em que pode ajudar.
"""

# -- Estruturas de dados ------------------------------------------------------

@dataclass
class Turno:
    role: str   # "user" | "assistant" | "system"
    content: str

@dataclass
class DAVIDAgent:
    historico: list[Turno] = field(default_factory=list)
    _chroma_collection: object = field(default=None, repr=False)
    _embedding_fn: object = field(default=None, repr=False)

    def _conectar_chroma(self):
        if self._chroma_collection is not None:
            return
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        self._embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )
        self._chroma_collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=self._embedding_fn
        )

    def buscar_versiculos(self, query: str) -> list[dict]:
        """Recupera versiculos relevantes do ChromaDB."""
        self._conectar_chroma()
        resultado = self._chroma_collection.query(
            query_texts=[query],
            n_results=RAG_TOP_K,
            include=["documents", "metadatas", "distances"],
        )
        versiculos = []
        for doc, meta, dist in zip(
            resultado["documents"][0],
            resultado["metadatas"][0],
            resultado["distances"][0]
        ):
            score = 1 - dist
            if score >= RAG_SCORE_MIN:
                versiculos.append({
                    "referencia": meta.get("referencia", "?"),
                    "texto": doc,
                    "score": round(score, 3),
                    "livro": meta.get("livro", "?"),
                })
        return versiculos

    def _montar_contexto_rag(self, versiculos: list[dict]) -> str:
        """Monta o bloco de contexto biblico para o prompt."""
        if not versiculos:
            return ""
        linhas = ["CONTEXTO BIBLICO RELEVANTE (ACF 2007):"]
        for v in versiculos:
            linhas.append(f"- [{v['referencia']}] {v['texto']}")
        return "\n".join(linhas)

    def _chamar_ollama(self, mensagens: list[dict], temperatura: float = 0.7) -> str:
        """Chama a API do Ollama (compativel com OpenAI /v1/chat/completions)."""
        payload = json.dumps({
            "model": OLLAMA_MODEL,
            "messages": mensagens,
            "temperature": temperatura,
            "stream": False,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{OLLAMA_BASE_URL}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=180) as r:
            resp = json.load(r)
            return resp["message"]["content"].strip()

    def responder(self, mensagem_usuario: str) -> str:
        """
        Processa uma mensagem do usuario e retorna a resposta do DAVID.
        Pipeline: RAG -> monta prompt -> LLM -> retorna resposta
        """
        # 1. Busca RAG
        versiculos = self.buscar_versiculos(mensagem_usuario)
        contexto_rag = self._montar_contexto_rag(versiculos)

        # 2. Adiciona mensagem do usuario ao historico
        conteudo_usuario = mensagem_usuario
        if contexto_rag:
            conteudo_usuario = f"{mensagem_usuario}\n\n{contexto_rag}"

        self.historico.append(Turno(role="user", content=conteudo_usuario))

        # 3. Monta lista de mensagens para o LLM
        mensagens = [{"role": "system", "content": DAVID_SYSTEM_PROMPT}]

        # Limita historico para evitar context overflow
        hist_recente = self.historico[-MAX_HIST:]
        for turno in hist_recente:
            mensagens.append({"role": turno.role, "content": turno.content})

        # 4. Chama o LLM
        resposta = self._chamar_ollama(mensagens, temperatura=0.7)

        # 5. Adiciona resposta ao historico
        self.historico.append(Turno(role="assistant", content=resposta))

        return resposta

    def nova_sessao(self):
        """Limpa o historico para iniciar nova conversa."""
        self.historico.clear()

    @property
    def total_versiculos(self) -> int:
        """Retorna o total de versiculos indexados."""
        try:
            self._conectar_chroma()
            return self._chroma_collection.count()
        except Exception:
            return 0
