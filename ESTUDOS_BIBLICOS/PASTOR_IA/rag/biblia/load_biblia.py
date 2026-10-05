"""
load_biblia.py -- Carrega a Biblia do repositorio BibleMarkdown para o ChromaDB

Fonte: https://github.com/ameisehaufen/BibleMarkdown
Traducao: ACF 2007 (Almeida Corrigida Fiel) -- unica disponivel no repo

Estrutura do repositório:
  BibleMarkdown/
  ├── Genesis/         ← uma pasta por livro (nome em português)
  │   ├── 01.md          ← um arquivo por capítulo
  │   ├── 02.md
  │   └── ...
  ├── João/
  │   ├── 01.md          ← cada linha = 1 versículo com marcador numérico
  │   └── ...
  └── Apocalipse/

Uso:
    python load_biblia.py --source ./sources/BibleMarkdown --dry-run
    python load_biblia.py --source ./sources/BibleMarkdown
    python load_biblia.py --source ./sources/BibleMarkdown --benchmark
"""

import sys
import io
# Forca UTF-8 no stdout para evitar erros de encoding no Windows (cp1252)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import os
import re
import argparse
import json
import unicodedata
from pathlib import Path
from typing import Generator

import chromadb
from chromadb.utils import embedding_functions
from tqdm import tqdm
from rich.console import Console
from rich.table import Table

console = Console()

# ── Configurações ──────────────────────────────────────────────────────────────

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8001"))  # porta ajustada (8001)
COLLECTION_NAME = "biblia_pt_br"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
BATCH_SIZE = 200  # Versículos por batch (CPU-safe)
TRADUCAO = "ACF"  # Única tradução disponível no BibleMarkdown

# Mapa: prefixo da pasta -> nome canonico do livro
# Nomes verificados contra o repositorio real em 2026-07-15
PREFIXO_LIVRO = {
    "01A-Gn":  "Genesis",          "02A-Ex":  "Exodo",
    "03A-Lv":  "Levitico",         "04A-Nm":  "Numeros",
    "05A-Dt":  "Deuteronomio",     "06A-Js":  "Josue",
    "07A-Jz":  "Juizes",           "08A-Rt":  "Rute",
    "09A-1Sm": "1Samuel",          "10A-2Sm": "2Samuel",
    "11A-1Rs": "1Reis",            "12A-2Rs": "2Reis",
    "13A-1Cr": "1Cronicas",        "14A-2Cr": "2Cronicas",
    "15A-Es":  "Esdras",           "16A-Ne":  "Neemias",
    "17A-Et":  "Ester",            "18A-Jo":  "Jo",
    "19A-Sl":  "Salmos",           "20A-Pv":  "Proverbios",
    "21A-Ec":  "Eclesiastes",      "22A-Ct":  "Cantares",
    "23A-Is":  "Isaias",           "24A-Jr":  "Jeremias",
    "25A-Lm":  "Lamentacoes",      "26A-Ez":  "Ezequiel",
    "27A-Dn":  "Daniel",           "28A-Os":  "Oseias",
    "29A-Jl":  "Joel",             "30A-Am":  "Amos",
    "31A-Ob":  "Abdias",           "32A-Jn":  "Jonas",      # 31A-Ob (nao Ab)
    "33A-Mq":  "Miqueias",         "34A-Na":  "Naum",
    "35A-Hc":  "Habacuque",        "36A-Sf":  "Sofonias",
    "37A-Ag":  "Ageu",             "38A-Zc":  "Zacarias",
    "39A-Ml":  "Malaquias",
    "40N-Mt":  "Mateus",           "41N-Mc":  "Marcos",
    "42N-Lc":  "Lucas",            "43N-Joa": "Joao",       # 43N-Joa (nao Jo)
    "44N-At":  "Atos",             "45N-Rm":  "Romanos",
    "46N-1Co": "1Corintios",       "47N-2Co": "2Corintios",
    "48N-Gl":  "Galatas",          "49N-Ef":  "Efesios",
    "50N-Fp":  "Filipenses",       "51N-Cl":  "Colossenses",
    "52N-1Ts": "1Tessalonicenses", "53N-2Ts": "2Tessalonicenses",
    "54N-1Tm": "1Timoteo",         "55N-2Tm": "2Timoteo",
    "56N-Tt":  "Tito",             "57N-Fm":  "Filemon",
    "58N-Hb":  "Hebreus",          "59N-Tg":  "Tiago",
    "60N-1Pe": "1Pedro",           "61N-2Pe": "2Pedro",
    "62N-1Jo": "1Joao",            "63N-2Jo": "2Joao",
    "64N-3Jo": "3Joao",            "65N-Jd":  "Judas",
    "66N-Ap":  "Apocalipse",
}


# Ordem canônica dos livros (para metadados de ordenação)
LIVROS_ORDEM = {
    "Génesis": 1, "Gênesis": 1, "Exodo": 2, "Êxodo": 2, "Levitico": 3,
    "Levítico": 3, "Numeros": 4, "Números": 4, "Deuteronomio": 5,
    "Deuteronômio": 5, "Josue": 6, "Josué": 6, "Juizes": 7, "Juízes": 7,
    "Rute": 8, "1Samuel": 9, "2Samuel": 10, "1Reis": 11, "2Reis": 12,
    "1Cronicas": 13, "1Crônicas": 13, "2Cronicas": 14, "2Crônicas": 14,
    "Esdras": 15, "Neemias": 16, "Ester": 17, "Jo": 18, "Jó": 18,
    "Salmos": 19, "Proverbios": 20, "Provérbios": 20, "Eclesiastes": 21,
    "Cantares": 22, "Isaias": 23, "Isaías": 23, "Jeremias": 24,
    "Lamentacoes": 25, "Lamentações": 25, "Ezequiel": 26, "Daniel": 27,
    "Oseias": 28, "Oséias": 28, "Joel": 29, "Amos": 30, "Amós": 30,
    "Abdias": 31, "Obadias": 31, "Jonas": 32, "Miqueias": 33, "Miquéias": 33,
    "Naum": 34, "Habacuque": 35, "Sofonias": 36, "Sofonias": 36,
    "Ageu": 37, "Zacarias": 38, "Malaquias": 39,
    "Mateus": 40, "Marcos": 41, "Lucas": 42, "Joao": 43, "João": 43,
    "Atos": 44, "Romanos": 45, "1Corintios": 46, "1Coríntios": 46,
    "2Corintios": 47, "2Coríntios": 47, "Galatas": 48, "Gálatas": 48,
    "Efesios": 49, "Efésios": 49, "Filipenses": 50, "Colossenses": 51,
    "1Tessalonicenses": 52, "2Tessalonicenses": 53, "1Timoteo": 54,
    "1Timóteo": 54, "2Timoteo": 55, "2Timóteo": 55, "Tito": 56,
    "Filemon": 57, "Filemom": 57, "Hebreus": 58, "Tiago": 59,
    "1Pedro": 60, "2Pedro": 61, "1Joao": 62, "1João": 62,
    "2Joao": 63, "2João": 63, "3Joao": 64, "3João": 64,
    "Judas": 65, "Apocalipse": 66,
}


# ── Parser de Markdown da Bíblia ───────────────────────────────────────────────

def parse_biblia_markdown(source_dir: Path, traducao: str = "ACF") -> Generator[dict, None, None]:
    """
    Parseia a Biblia do BibleMarkdown -- estrutura real:
      source_dir/versoes_online/acf2007-MHenry/
        01A-Gn/01.md  (capitulo 1)
        01A-Gn/02.md  (capitulo 2)
        ...

    Formato de cada .md:
      # Genesis Cap 01          <- cabecalho (ignorado)
      **1** \tTexto do versiculo  <- versiculo (capturado)
      > **Cmt MHenry**: ...      <- comentario (ignorado)
      ![](imagem.jpg)            <- imagem (ignorada)

    ATENCAO: arquivos em cp1252 (Windows) -- ler com encoding correto.
    """
    # Aponta para o diretorio correto dentro da estrutura do repo
    biblia_dir = source_dir / "versoes_online" / "acf2007-MHenry"
    if not biblia_dir.exists():
        # Tenta usar source_dir diretamente se ja apontar para acf2007-MHenry
        biblia_dir = source_dir

    pastas_livro = sorted(
        [p for p in biblia_dir.iterdir()
         if p.is_dir() and p.name in PREFIXO_LIVRO]
    )

    if not pastas_livro:
        console.print(f"[red]ERRO: Nenhuma pasta de livro encontrada em {biblia_dir}[/red]")
        console.print(f"[yellow]Pastas encontradas: {[p.name for p in biblia_dir.iterdir() if p.is_dir()]}[/yellow]")
        return

    console.print(f"[green]OK: {len(pastas_livro)} livros encontrados[/green]")

    # Padrao de versiculo: **N** \tTexto  ou  **N**   Texto
    VERS_PATTERN = re.compile(r"^\*\*(\d+)\*\*\s+(.+)")

    for pasta_livro in pastas_livro:
        livro_nome = PREFIXO_LIVRO[pasta_livro.name]
        livro_ordem = LIVROS_ORDEM.get(livro_nome, 99)

        # Arquivos de capitulo: 01.md, 02.md, ... (00.md = intro, ignorar)
        arquivos_cap = sorted(
            [f for f in pasta_livro.glob("*.md")
             if f.stem.isdigit() and int(f.stem) >= 1]
        )

        for arquivo_cap in arquivos_cap:
            capitulo_num = int(arquivo_cap.stem)

            # Tenta varios encodings -- arquivos originais podem ser cp1252 ou utf-8
            conteudo = None
            for enc in ("utf-8", "cp1252", "latin-1"):
                try:
                    conteudo = arquivo_cap.read_text(encoding=enc, errors="strict")
                    break
                except (UnicodeDecodeError, UnicodeError):
                    continue
            if conteudo is None:
                conteudo = arquivo_cap.read_text(encoding="utf-8", errors="replace")

            for linha in conteudo.splitlines():
                linha = linha.strip()

                # Ignora linhas vazias, cabecalhos, comentarios, imagens e links
                if not linha:
                    continue
                if linha.startswith("#") or linha.startswith(">") or linha.startswith("!"):
                    continue

                m = VERS_PATTERN.match(linha)
                if not m:
                    continue

                num_vers = int(m.group(1))
                texto = m.group(2).strip()

                # Remove markdown residual: links [texto](url), negrito **x**, italico *x*
                texto = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", texto)  # links
                texto = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", texto)  # bold/italic
                texto = re.sub(r"\t", " ", texto)                        # tabs
                texto = texto.strip()

                if len(texto) < 5:
                    continue

                referencia = f"{livro_nome} {capitulo_num}:{num_vers}"
                uid = f"{traducao}_{livro_nome}_{capitulo_num}_{num_vers}"

                yield {
                    "id": uid,
                    "documento": texto,
                    "livro": livro_nome,
                    "capitulo": capitulo_num,
                    "versiculo": num_vers,
                    "traducao": traducao,
                    "referencia": referencia,
                    "livro_ordem": livro_ordem,
                }




# ── Carga no ChromaDB ──────────────────────────────────────────────────────────

def carregar_no_chromadb(
    versiculos: list[dict],
    collection,
    dry_run: bool = False
) -> int:
    """Insere versículos no ChromaDB em batches."""
    total = len(versiculos)
    inseridos = 0

    for i in tqdm(range(0, total, BATCH_SIZE), desc="Indexando versículos"):
        batch = versiculos[i : i + BATCH_SIZE]

        ids = [v["id"] for v in batch]
        documentos = [v["documento"] for v in batch]
        metadados = [
            {
                "livro": v["livro"],
                "capitulo": v["capitulo"],
                "versiculo": v["versiculo"],
                "traducao": v["traducao"],
                "referencia": v["referencia"],
                "livro_ordem": v["livro_ordem"],
            }
            for v in batch
        ]

        if not dry_run:
            collection.upsert(
                ids=ids,
                documents=documentos,
                metadatas=metadados,
            )

        inseridos += len(batch)

    return inseridos


# ── Benchmark de qualidade ─────────────────────────────────────────────────────

def testar_rag(collection) -> None:
    """Testa qualidade básica do RAG após indexação."""
    console.print("\n[bold yellow]BENCHMARK: Qualidade do RAG biblico[/bold yellow]\n")

    testes = [
        {
            "query": "Porque Deus amou o mundo de tal maneira",
            "esperado": "João 3:16",
        },
        {
            "query": "amarás o Senhor teu Deus de todo o teu coração",
            "esperado": "Mateus 22:37",
        },
        {
            "query": "No princípio Deus criou os céus e a terra",
            "esperado": "Gênesis 1:1",
        },
        {
            "query": "Orai sem cessar",
            "esperado": "1 Tessalonicenses 5:17",
        },
        {
            "query": "futebol campeonato brasileiro",
            "esperado": "SEM RESULTADO RELEVANTE",
        },
    ]

    tabela = Table(title="Resultados do Benchmark")
    tabela.add_column("Query", style="cyan", no_wrap=False)
    tabela.add_column("Esperado", style="yellow")
    tabela.add_column("Encontrado", style="green")
    tabela.add_column("Score", style="magenta")
    tabela.add_column("Status", style="bold")

    for teste in testes:
        resultado = collection.query(
            query_texts=[teste["query"]],
            n_results=1,
            include=["documents", "metadatas", "distances"],
        )

        if resultado["ids"][0]:
            meta = resultado["metadatas"][0][0]
            referencia = meta.get("referencia", "?")
            score = 1 - resultado["distances"][0][0]  # distância → similaridade

            if teste["esperado"] == "SEM RESULTADO RELEVANTE":
                status = "OK" if score < 0.5 else "SCORE ALTO"
            else:
                # Normaliza acentos para comparacao robusta
                def norm(s):
                    s = unicodedata.normalize('NFD', s)
                    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
                    return s.replace(' ', '').upper()
                acertou = norm(teste["esperado"]) in norm(referencia) or norm(referencia) in norm(teste["esperado"])
                status = "OK" if acertou else "MISS"

            tabela.add_row(
                teste["query"][:50],
                teste["esperado"],
                referencia,
                f"{score:.3f}",
                status,
            )
        else:
            tabela.add_row(
                teste["query"][:50],
                teste["esperado"],
                "Sem resultado",
                "—",
                "⚠️",
            )

    console.print(tabela)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Carrega a Bíblia do BibleMarkdown para o ChromaDB"
    )
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Diretório raiz do repositório BibleMarkdown clonado",
    )
    parser.add_argument(
        "--traducao",
        type=str,
        default="ARC",
        help="Sigla da tradução (ex: ARC, NVI, NVT)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parseia mas não insere no ChromaDB",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Executa benchmark de qualidade após indexação",
    )
    args = parser.parse_args()

    console.print(f"\n[bold green]DAVID Pastoral -- Carga do Corpus Biblico[/bold green]")
    console.print(f"Fonte: {args.source}")
    console.print(f"Traducao: {args.traducao}")
    console.print(f"Dry-run: {args.dry_run}\n")

    # 1. Parseia todos os versiculos
    console.print("[cyan]Parseando arquivos Markdown...[/cyan]")
    versiculos = list(parse_biblia_markdown(args.source, args.traducao))
    console.print(f"[green]OK: {len(versiculos):,} versiculos extraidos[/green]")

    if not versiculos:
        console.print("[red]ERRO: Nenhum versiculo extraido. Verifique a estrutura dos .md[/red]")
        return

    # 2. Conecta ao ChromaDB
    if not args.dry_run:
        console.print(f"\n[cyan]Conectando ao ChromaDB em {CHROMA_HOST}:{CHROMA_PORT}...[/cyan]")
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

        ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )

        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=ef,
            metadata={"hnsw:space": "cosine"},
        )
        console.print(f"[green]OK: Colecao '{COLLECTION_NAME}' pronta[/green]")

        # 3. Carrega no ChromaDB
        console.print(f"\n[cyan]Indexando {len(versiculos):,} versiculos (batch={BATCH_SIZE})...[/cyan]")
        console.print("[yellow]CPU-only: pode levar 10-30 minutos. Aguarde.[/yellow]\n")

        inseridos = carregar_no_chromadb(versiculos, collection, dry_run=False)
        console.print(f"\n[bold green]SUCESSO: {inseridos:,} versiculos indexados![/bold green]")

        # 4. Benchmark opcional
        if args.benchmark:
            testar_rag(collection)
    else:
        console.print(f"\n[yellow]DRY-RUN: {len(versiculos):,} versiculos seriam indexados[/yellow]")
        console.print("Primeiros 5 versiculos extraidos:")
        for v in versiculos[:5]:
            console.print(f"  [{v['referencia']}] {v['documento'][:80]}...")


if __name__ == "__main__":
    main()
