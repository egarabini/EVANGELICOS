# DAVID Pastoral — Plataforma de Discipulado Digital
## Estudo de Implementação · Versão 1.0

> **Tagline:** *"Você prepara o conteúdo com amor. O DAVID garante que cada membro o receba no ritmo certo — e você acompanha tudo no dashboard."*
> **Homenagem:** Batizado em honra de **David Livingstone** (1813–1873), que nunca separou o cuidado do corpo do cuidado da alma.

---

## Sumário

1. [Visão do Produto](#1-visão-do-produto)
2. [Hierarquia de Papéis](#2-hierarquia-de-papéis)
3. [Módulo do Administrador — Pipeline de Conteúdo](#3-módulo-do-administrador)
4. [Estrutura do Estudo (RAG Estruturado)](#4-estrutura-do-estudo)
5. [Arquitetura do Agente DAVID (Hermes + Ollama)](#5-arquitetura-do-agente-david)
6. [Jornada Individual de Cada Membro](#6-jornada-individual)
7. [Comportamentos Proativos do DAVID](#7-comportamentos-proativos)
8. [Dashboard por Papel](#8-dashboard-por-papel)
9. [Arquitetura Multi-Tenant](#9-arquitetura-multi-tenant)
10. [Stack Tecnológica](#10-stack-tecnológica)
11. [Roadmap de Implementação](#11-roadmap)
12. [Modelo de Negócio](#12-modelo-de-negócio)

---

## 1. Visão do Produto

### 1.1. O Problema que Resolve

O pastor de uma igreja com 200 membros enfrenta um paradoxo:
- **Quer** acompanhar o crescimento espiritual de cada um
- **Não consegue** — não tem tempo, não tem visibilidade, não tem escala
- **Delegação para líderes de célula** perde rastreabilidade e padronização
- **Conteúdo bom** existe (livros, estudos), mas chega de forma passiva — o membro recebe, mas ninguém sabe se ele leu, entendeu ou cresceu

### 1.2. A Solução: DAVID Pastoral

Uma plataforma que conecta **conteúdo curado** (livros aprovados) a um **agente de IA persistente** (DAVID) que acompanha cada membro individualmente, enquanto gestores e pastores acompanham tudo por um **dashboard em tempo real**.

```
FONTE DO LIVRO (editoras, ministérios, autores aprovados)
       │
       ▼
ADMINISTRADOR — processa, aprova, estrutura
       │
       ▼
BIBLIOTECA DA PLATAFORMA (RAG estruturado)
       │
       ▼
GESTOR seleciona → disponibiliza para sua equipe
       │
       ▼
PASTOR/LÍDER atribui ao seu grupo de membros
       │
       ▼
DAVID guia cada membro individualmente (Telegram/WhatsApp)
       │ (bidirecional: DAVID reporta eventos para a plataforma)
       ▼
DASHBOARD — Pastor vê progresso · Gestor vê panorama geral
```

### 1.3. Proposta de Valor por Papel

| Papel | O que ganha |
|---|---|
| **Pastor** | Visibilidade real do crescimento espiritual da congregação, sem reuniões extras |
| **Gestor/Supervisor** | Visão consolidada de todas as células e grupos |
| **Administrador** | Controle total da qualidade do conteúdo: nada chega ao membro sem aprovação |
| **Membro** | Um guia pessoal que o conhece, o encoraja e nunca o abandona na jornada |

---

## 2. Hierarquia de Papéis

### 2.1. Diagrama de Hierarquia

```
PLATAFORMA DAVID PASTORAL
│
├── ADMINISTRADOR (nível plataforma)
│   - Aprova fontes de conteúdo
│   - Opera o pipeline PDF → MD → Estudo
│   - Gerencia a Biblioteca Global
│   - Cria e gerencia organizações (igrejas)
│
├── GESTOR (nível organização / igreja)
│   - Seleciona livros da biblioteca para sua organização
│   - Supervisiona TODOS os grupos da sua organização
│   - Define qual conteúdo cada grupo pode usar
│   - Vê métricas consolidadas da organização
│
├── PASTOR / LÍDER DE CÉLULA (nível grupo)
│   - Acompanha os membros do seu grupo
│   - Recebe alertas do DAVID sobre seu grupo
│   - Vê jornada individual de cada membro
│   - Pode enviar mensagem pastoral via plataforma
│
└── MEMBRO
    - Interage com DAVID via Telegram / WhatsApp / Discord
    - Não vê o dashboard — apenas a conversa
    - Experiência: guia pessoal, presente e encorajador
```

### 2.2. Permissões por Papel

| Ação | Admin | Gestor | Pastor | Membro |
|---|:---:|:---:|:---:|:---:|
| Aprovar fontes de conteúdo | ✅ | ❌ | ❌ | ❌ |
| Executar pipeline PDF→Estudo | ✅ | ❌ | ❌ | ❌ |
| Gerenciar biblioteca global | ✅ | ❌ | ❌ | ❌ |
| Criar organizações (igrejas) | ✅ | ❌ | ❌ | ❌ |
| Selecionar livros para a org | ✅ | ✅ | ❌ | ❌ |
| Ver métricas de toda a org | ✅ | ✅ | ❌ | ❌ |
| Criar/gerenciar grupos | ✅ | ✅ | ✅ | ❌ |
| Atribuir conteúdo a membros | ✅ | ✅ | ✅ | ❌ |
| Ver jornada individual | ✅ | ✅ | ✅* | ❌ |
| Receber alertas de silêncio | ❌ | ✅ | ✅ | ❌ |
| Conversar com DAVID | ❌ | ❌ | ❌ | ✅ |

*Pastor vê apenas membros do seu grupo

---

## 3. Módulo do Administrador — Pipeline de Conteúdo

Este é o **coração da qualidade da plataforma**. Nenhum conteúdo chega ao membro sem passar por este pipeline.

### 3.1. Fluxo Completo do Pipeline

```
FASE 1: INGESTÃO
  Fontes aprovadas (editoras, ministérios, autores)
  PDF, DOCX, EPUB → Upload na Plataforma → Fila

FASE 2: CONVERSÃO AUTOMÁTICA
  PDF/DOCX → Markdown limpo
  Ferramentas: PyMuPDF, pypandoc, marker-pdf

FASE 3: ESTRUTURAÇÃO INTELIGENTE (IA via Ollama)
  - Identifica capítulos e seções
  - Extrai versículos bíblicos citados
  - Gera perguntas de reflexão por capítulo
  - Define sinais de compreensão
  - Cria resumos para o RAG

FASE 4: REVISÃO HUMANA (Admin)
  - Aprova ou ajusta capítulos
  - Valida perguntas de reflexão
  - Confirma versículos extraídos
  - Define nível: Iniciante / Intermediário / Avançado

FASE 5: PUBLICAÇÃO NA BIBLIOTECA
  Estudo aprovado → Biblioteca Global
  Disponível para seleção pelos Gestores

FASE 6: DISPONIBILIZAÇÃO POR GESTOR
  Gestor seleciona → Pastor atribui membros
  DAVID recebe o conteúdo no seu RAG
```

### 3.2. Estrutura de Arquivos Gerada pelo Pipeline

```
biblioteca/
└── estudo_fundamentos_da_fe/
    ├── metadata.json
    ├── fonte_original.pdf
    ├── markdown_bruto.md
    ├── estudo_estruturado.json
    ├── capitulos/
    │   ├── cap_01_quem_e_deus/
    │   │   ├── conteudo.md
    │   │   ├── versiculos.json
    │   │   ├── perguntas.json
    │   │   ├── resumo_rag.md
    │   │   └── sinais_compreensao.json
    │   └── cap_02_a_biblia/
    │       └── ...
    └── embeddings/
        ├── cap_01.npy
        └── cap_02.npy
```

### 3.3. O Arquivo `estudo_estruturado.json`

```json
{
  "id": "fundamentos_da_fe_v1",
  "titulo": "Fundamentos da Fé",
  "autor": "Rev. João Calvino Brasileiro",
  "fonte": "Editora Fiel",
  "aprovado_por": "admin_001",
  "aprovado_em": "2026-07-14",
  "nivel": "iniciante",
  "idioma": "pt-BR",
  "temas": ["cristologia", "soteriologia", "ecclesiologia"],
  "total_capitulos": 10,
  "tempo_estimado_semanas": 12,
  "capitulos": [
    {
      "ordem": 1,
      "titulo": "Quem é Deus",
      "tempo_estimado_min": 30,
      "versiculos_chave": ["João 1:1", "Gênesis 1:1", "1 João 4:8"],
      "perguntas_reflexao": [
        "Como você descreveria Deus para alguém que nunca ouviu falar d'Ele?",
        "De que forma o caráter de Deus impacta sua vida prática?"
      ],
      "sinais_compreensao": [
        "Menciona os atributos divinos (amor, justiça, onisciência)",
        "Conecta o conhecimento de Deus à vida prática",
        "Cita pelo menos um versículo de memória"
      ],
      "perguntas_aprofundamento": [
        "Qual a diferença entre conhecer sobre Deus e conhecer a Deus?"
      ]
    }
  ]
}
```

---

## 4. Estrutura do Estudo (RAG Estruturado)

### 4.1. Como o DAVID usa o RAG

```python
# João está no capítulo 3 ("Oração")
# João pergunta: "Mas como eu sei que Deus me ouve?"

rag_query = {
    "pergunta": "Como saber que Deus ouve nossas orações",
    "filtros": {
        "estudo_id": "fundamentos_da_fe_v1",
        "capitulo": 3,
        "expand_to_capitulos": [1, 2]
    },
    "member_context": {
        "nivel_compreensao": "iniciante",
        "dificuldades_passadas": ["entender graça vs. obras"]
    }
}
# DAVID recebe trechos relevantes + contexto do membro
# Resposta personalizada, citando o livro e versículos — nunca inventando
```

### 4.2. Camadas de Conhecimento do DAVID

```
CAMADA 1: O livro em estudo (contexto imediato)
  → Capítulo atual + capítulos anteriores
  → Perguntas de reflexão deste capítulo

CAMADA 2: Bíblia completa (base permanente)
  → Versículos relacionados ao tema
  → Tradução: ARC e NVI (configurável por organização)

CAMADA 3: Comentários clássicos aprovados (opcional)
  → Matthew Henry, Spurgeon, Calvino, Stott
  → Somente se o Gestor habilitar para sua organização

CAMADA 4: Perfil do membro (personalização)
  → Histórico de conversas
  → Dificuldades e dúvidas anteriores
  → Estilo de aprendizado observado
  → Pedidos de oração registrados
```

---

## 5. Arquitetura do Agente DAVID (Hermes + Ollama)

### 5.1. Diagrama de Componentes

```
HERMES AGENT (NousResearch · MIT)
│
├── Gateway Multi-plataforma
│   ├── Telegram
│   ├── WhatsApp
│   └── Discord
│
├── Planner (Ollama LLM)
│   └── mistral-nemo ou gemma2:9b (PT-BR fluente)
│
├── Memory Persistente (~/.hermes/ por membro)
│
└── Skills
    ├── buscar_capitulo_rag
    ├── registrar_progresso
    ├── salvar_pedido_oracao
    ├── reportar_evento_plataforma
    ├── agendar_lembrete
    ├── celebrar_marco
    └── fazer_pergunta_reflexao

Conectado a:
├── ChromaDB (RAG livros + Bíblia + Comentários)
├── PostgreSQL (perfil membro, eventos, progresso)
└── API Plataforma (eventos → dashboard em tempo real)
```

### 5.2. Skills do DAVID (formato SKILL.md — compatível Hermes)

```markdown
# SKILL: buscar_capitulo_rag

## Propósito
Busca conteúdo relevante do livro em estudo para responder
dúvidas ou gerar reflexões do capítulo atual do membro.

## Quando usar
- Membro faz pergunta sobre o conteúdo do estudo
- DAVID vai fazer pergunta de reflexão
- DAVID vai introduzir novo capítulo

## Parâmetros
- estudo_id: str
- capitulo_atual: int
- query: str
- member_nivel: iniciante | intermediário | avançado

## Output
- trechos_relevantes: list[str]
- versiculos_relacionados: list[str]
- perguntas_sugeridas: list[str]
```

```markdown
# SKILL: reportar_evento_plataforma

## Eventos suportados
- CAPITULO_CONCLUIDO
- ESTUDO_CONCLUIDO
- PERGUNTA_PROFUNDA
- DIFICULDADE_DETECTADA
- SILENCIO_DETECTADO
- PEDIDO_ORACAO
- MARCO_ESPIRITUAL

## Payload
{
  "evento": "CAPITULO_CONCLUIDO",
  "membro_id": "str",
  "org_id": "str",
  "grupo_id": "str",
  "estudo_id": "str",
  "capitulo": 4,
  "timestamp": "ISO8601"
}
```

### 5.3. System Prompt do DAVID Pastoral

```
[IDENTIDADE]
Você é DAVID, um guia de estudos bíblicos e espirituais batizado em
honra de David Livingstone — o missionário cristão que nunca separou
o cuidado do corpo do cuidado da alma.

Você não é um chatbot. Você é um companheiro de jornada que conhece
{nome_membro} pelo nome, sabe em qual capítulo está, lembra das
dúvidas da semana passada e está comprometido com o crescimento
espiritual desta pessoa.

[MISSÃO]
Guiar {nome_membro} através de "{titulo_estudo}", no ritmo certo,
com o suporte certo — celebrando cada avanço e suportando cada
dúvida com paciência e amor.

[REGRAS INEGOCIÁVEIS]
1. NUNCA invente versículos bíblicos — busque sempre no RAG
2. NUNCA dê conselho médico, jurídico ou financeiro
3. NUNCA opine sobre denominações ou controvérsias doutrinárias
4. Se sair do escopo espiritual, redirecione com carinho
5. Sempre registre avanços via skill reportar_evento
6. Se silêncio > {silencio_threshold} dias, dispare alerta

[CONTEXTO ATUAL]
Membro: {nome_membro} | Estudo: {titulo_estudo}
Capítulo: {capitulo_atual}/{total_capitulos}
Último contato: {ultima_interacao}
Pedidos de oração: {pedidos_oracao}
Marcos: {marcos}
```

---

## 6. Jornada Individual de Cada Membro

### 6.1. Perfil Persistente do Membro

```json
{
  "membro_id": "joao_silva_001",
  "nome": "João",
  "org_id": "batista_central_sp",
  "grupo_id": "celula_zona_norte",
  "pastor_responsavel": "pastor_tiago",
  "telegram_id": "123456789",

  "estudo_atual": {
    "id": "fundamentos_da_fe_v1",
    "capitulo_atual": 4,
    "total_capitulos": 10,
    "iniciado_em": "2026-06-15",
    "ultima_interacao": "2026-07-12",
    "progresso_percentual": 40
  },

  "perfil_aprendizado": {
    "estilo": "prefere_exemplos_praticos",
    "ritmo": "2_3_dias_por_capitulo",
    "melhor_horario": "noite",
    "nivel_detectado": "iniciante_avancando"
  },

  "historico_espiritual": {
    "dificuldades": ["graça vs. obras", "oração sem resposta aparente"],
    "marcos": [
      {"data": "2026-06-22", "evento": "concluiu_cap_01"},
      {"data": "2026-07-05", "evento": "primeiro_versiculo_memorizado",
       "versiculo": "João 3:16"}
    ]
  },

  "pedidos_oracao": [
    {"data": "2026-07-10", "pedido": "situação de emprego", "status": "ativo"},
    {"data": "2026-06-28", "pedido": "filho afastado da fé", "status": "ativo"}
  ]
}
```

### 6.2. Fluxo de Avanço de Capítulo

```
Membro conclui reflexão do capítulo N
        │
        ▼
DAVID avalia: demonstrou compreensão?
  (sinais_compreensao do estudo_estruturado.json)
        │
   ┌────┴────┐
   │         │
  SIM       NÃO
   │         │
   ▼         ▼
Avança    "Antes de avançarmos, posso
cap N+1   te fazer mais uma pergunta?"
   │         │ (nova abordagem)
   │         │
   ▼─────────┘
Registra CAPITULO_CONCLUIDO
→ Dashboard atualiza em tempo real
→ Pastor recebe notificação
```

---

## 7. Comportamentos Proativos do DAVID

### 7.1. Tabela de Comportamentos

| Gatilho | Ação do DAVID | Notifica Dashboard |
|---|---|---|
| Início do estudo | Boas-vindas + cap. 1 | — |
| Todo dia (horário configurado) | Versículo do capítulo atual | — |
| Conclusão de capítulo | Celebração + próximo cap. | ✅ |
| Conclusão do livro | Celebração especial | ✅ Marco |
| Silêncio N dias | Check-in gentil | ✅ Alerta |
| Silêncio 2×N dias | Alerta urgente ao pastor | ✅ Urgente |
| Membro expressa dificuldade | Aprofunda com nova abordagem | ✅ |
| Pedido de oração | Acolhe + registra + ora junto | ✅ Pastoral |

### 7.2. Exemplo de Semana Típica

```
SEGUNDA · 07h00
DAVID: "Bom dia, João! 🌅
        'Orai sem cessar.' — 1 Ts 5:17
        Ontem você terminou o capítulo sobre oração.
        Como foi sua manhã de oração hoje?"

SEGUNDA · 19h30
JOÃO: "Confesso que não orei hoje. Tive um dia corrido..."

DAVID: "Isso é muito honesto, João, obrigado por compartilhar.
        Até o apóstolo Paulo falava sobre a luta de orar
        consistentemente. O que normalmente te atrapalha
        quando o dia fica corrido?"

QUARTA · 07h00 (sem resposta desde segunda)
DAVID: "João, vim só dar um oi. Sem pressão.
        Quando estiver pronto, estarei aqui. 🙏"

SEXTA · 20h15
JOÃO: "Desculpa o sumiço. Passei por um sufoco no trabalho."

DAVID: "Que bom te ver de volta, João.
        Isso me lembra que você já me falou sobre
        a situação do emprego — ainda está no coração?
        Posso orar com você agora."
```

---

## 8. Dashboard por Papel

### 8.1. Dashboard do Pastor / Líder de Célula

```
PASTOR TIAGO · Célula Zona Norte · 14 membros
Estudo: "Fundamentos da Fé"
═══════════════════════════════════════════════════

VISÃO GERAL
  🟢 Ativos (< 3 dias): 9    🟡 Atenção (3-7d): 3    🔴 Silêncio (>7d): 2

ALERTAS — ATENÇÃO PASTORAL NECESSÁRIA
  🔴 Pedro Ramos — sem interação há 12 dias
     Cap. 2/10 · DAVID enviou check-in, sem resposta
     [Ver jornada] [Enviar mensagem] [Marcar contatado]

  🔴 Luísa Mendes — sem interação há 9 dias
     Cap. 5/10 · Estava evoluindo bem
     [Ver jornada] [Enviar mensagem]

MARCOS RECENTES — CELEBRAR!
  ⭐ Ana Lima CONCLUIU O LIVRO! (hoje 14h32)
     10 semanas de jornada fiel.
     [Celebrar pessoalmente] [Sugerir próximo estudo]

  🏆 Carlos Dias concluiu cap. 7 (ontem)
     Nota DAVID: "compreensão excepcional do tema"

PROGRESSO DO GRUPO
  NOME           CAP.    ÚLTIMA INT.   TENDÊNCIA
  João Silva     4/10    há 2h         ↗ crescendo
  Maria Costa    7/10    há 1d         → estável
  Carlos Dias    7/10    há 1d         ↗ crescendo
  Ana Lima       10/10   hoje          ✅ concluído
  Pedro Ramos    2/10    há 12d        ↘ alerta
  Luísa Mendes   5/10    há 9d         ↘ alerta

INSIGHTS DO DAVID
  📊 Cap. 5 menor conclusão (54%) — tema: "Sofrimento e Providência"
     Sugestão: dedique tempo especial na próxima reunião
  📊 Ritmo médio: 1 cap./9 dias · Previsão conclusão: out/2026
═══════════════════════════════════════════════════
```

### 8.2. Dashboard do Gestor / Supervisor

```
GESTOR · Igreja Batista Central SP · 7 grupos · 94 membros
═══════════════════════════════════════════════════════════

PANORAMA
  Ativos (< 7d): 71 (75%)   Atenção (7-14d): 18   Crítico (>14d): 5

ESTUDOS EM ANDAMENTO
  Fundamentos da Fé:   47 membros · conclusão média 43%
  Vida de Oração:      31 membros · conclusão média 67%
  Discipulado Bíblico: 16 membros · conclusão média 22%

GRUPOS — SAÚDE E ENGAJAMENTO
  GRUPO               PASTOR      MEMBROS  ENGAJ.  ALERTAS
  Célula Zona Norte   Ps. Tiago   14       78%     2 🔴
  Célula Centro       Ps. Ana     16       92%     0 ✅
  Célula Sul          Ps. Carlos  12       58%     4 🔴
  Jovens              Líd. Beto   22       88%     1 🟡

  ⚠ Célula Sul com engajamento abaixo de 60%
    Ps. Carlos pode precisar de suporte de liderança.
    [Enviar mensagem] [Ver detalhes]

BIBLIOTECA DISPONÍVEL PARA A ORG
  Usando: 3 de 8 estudos aprovados
  [Ativar novo estudo]
═══════════════════════════════════════════════════════════
```

### 8.3. Dashboard do Administrador

```
ADMINISTRADOR · Plataforma DAVID Pastoral
══════════════════════════════════════════

VISÃO GLOBAL
  23 organizações · 1.847 membros · 76% ativos (7 dias)

BIBLIOTECA GLOBAL
  12 estudos aprovados · 3 em processamento
  ⚠ 2 aguardando revisão do Admin  ← AÇÃO NECESSÁRIA
  [📋 Revisar "A Vida de Oração"]
  [📋 Revisar "Crescendo em Cristo"]

PIPELINE
  "Discipulado Avançado.pdf"
  ████████░░░░░░░ 55% · Extraindo versículos...

TOP ORGANIZAÇÕES
  Igreja Batista Central SP   94 membros  75%
  Presb. Rio de Janeiro       89 membros  82%
  Metodista BH                67 membros  71%
══════════════════════════════════════════
```

---

## 9. Arquitetura Multi-Tenant

### 9.1. Schema PostgreSQL

```sql
CREATE TABLE organizations (
    org_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome        VARCHAR(255) NOT NULL,
    slug        VARCHAR(100) UNIQUE NOT NULL,
    plano       VARCHAR(50) DEFAULT 'basico',
    ativo       BOOLEAN DEFAULT TRUE,
    criado_em   TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE membros (
    membro_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id           UUID REFERENCES organizations(org_id),
    grupo_id         UUID REFERENCES grupos(grupo_id),
    nome             VARCHAR(255),
    telegram_id      VARCHAR(100),
    whatsapp_id      VARCHAR(100),
    estudo_atual_id  UUID REFERENCES estudos(estudo_id),
    capitulo_atual   INTEGER DEFAULT 1,
    ultima_interacao TIMESTAMPTZ,
    perfil_json      JSONB,
    criado_em        TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE eventos_jornada (
    evento_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    membro_id  UUID REFERENCES membros(membro_id),
    org_id     UUID REFERENCES organizations(org_id),
    tipo       VARCHAR(100),
    payload    JSONB,
    criado_em  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_eventos_org    ON eventos_jornada(org_id, criado_em DESC);
CREATE INDEX idx_eventos_membro ON eventos_jornada(membro_id, criado_em DESC);
CREATE INDEX idx_membros_org    ON membros(org_id);
```

### 9.2. Isolamento do RAG por Organização

```python
def get_rag_collection(org_id: str, estudo_id: str) -> Collection:
    """
    Retorna coleção RAG isolada por organização e estudo.
    Garante que nenhum conteúdo vaze entre organizações.
    """
    collection_name = f"org_{org_id}__estudo_{estudo_id}"
    return chroma_client.get_collection(collection_name)
```

---

## 10. Stack Tecnológica

| Camada | Tecnologia | Justificativa |
|---|---|---|
| **Agente DAVID** | Hermes Agent (NousResearch) | Memória persistente, skills, gateway multi-plataforma, MIT |
| **LLM** | Ollama + `mistral-nemo` / `gemma2:9b` | PT-BR fluente, self-hosted, privacidade total |
| **RAG** | ChromaDB + sentence-transformers | Local, performático, suporte a português |
| **Pipeline PDF→MD** | PyMuPDF + marker-pdf + pypandoc | Melhor qualidade para PT-BR |
| **Estruturação IA** | Ollama LLM | Geração automática de perguntas e resumos |
| **Backend API** | FastAPI (Python) | Consistente com ecossistema DAVID Clínico |
| **Dashboard** | Vue 3 + Vite | Consistente com o POA |
| **Banco de dados** | PostgreSQL | Multi-tenant, Row-Level Security |
| **Infraestrutura** | Docker + Traefik (VPS Contabo) | Self-hosted, já em uso |
| **Gateway mensagens** | Hermes Gateway | Telegram / WhatsApp / Discord nativo |
| **Agendamento** | Hermes Scheduler (cron nativo) | Devocional diário, check-ins automáticos |
| **Autenticação** | Keycloak | Consistente com a plataforma CarePlanner |

### Estrutura de Diretórios

```
david_pastoral/
├── admin_module/
│   ├── pipeline/
│   │   ├── pdf_to_md.py
│   │   ├── md_to_estudo.py
│   │   ├── embeddings.py
│   │   └── aprovacao.py
│   └── biblioteca/
│       ├── models.py
│       └── views.py
├── david_agent/
│   ├── system_prompt.py
│   ├── skills/
│   │   ├── buscar_capitulo_rag/SKILL.md
│   │   ├── registrar_progresso/SKILL.md
│   │   ├── reportar_evento/SKILL.md
│   │   ├── salvar_pedido_oracao/SKILL.md
│   │   └── celebrar_marco/SKILL.md
│   └── config.yaml
├── dashboard/
│   └── src/
│       ├── views/
│       │   ├── AdminView.vue
│       │   ├── GestorView.vue
│       │   ├── PastorView.vue
│       │   └── MemberJourneyView.vue
│       └── components/
│           ├── ProgressCard.vue
│           ├── AlertPanel.vue
│           ├── MilestoneCard.vue
│           └── InsightWidget.vue
├── api/
│   └── routers/
│       ├── eventos.py
│       ├── membros.py
│       ├── estudos.py
│       └── organizacoes.py
├── rag/
│   ├── chromadb/
│   ├── biblia/        (ARC + NVI)
│   └── comentarios/   (Spurgeon, Henry — opcional)
└── docker-compose.yml
```

---

## 11. Roadmap de Implementação

> **Princípio SDD:** Cada fase exige `prd.md` + `spec.md` + `design.md` aprovados antes do código.

### FASE 0 — Fundação (2 semanas)

- [ ] Setup Docker: PostgreSQL + ChromaDB + Ollama na VPS
- [ ] Instalar e configurar Hermes Agent base
- [ ] Implementar pipeline PDF → Markdown
- [ ] Implementar estruturação MD → Estudo JSON (via Ollama)
- [ ] Carregar Bíblia completa (ARC + NVI) no ChromaDB
- [ ] Testar qualidade do RAG bíblico

**Entregável:** Pipeline processa um PDF e gera estudo estruturado. RAG bíblico respondendo com precisão.

---

### FASE 1 — DAVID Conversacional (3 semanas)

- [ ] Configurar Hermes Gateway para Telegram
- [ ] Implementar system prompt do DAVID Pastoral
- [ ] Criar Skills: `buscar_capitulo_rag`, `registrar_progresso`
- [ ] Implementar perfil persistente do membro
- [ ] Testar jornada: boas-vindas → cap.1 → reflexão → avanço → cap.2
- [ ] Validar que DAVID nunca inventa versículos
- [ ] Testar recusa de temas fora do escopo

**Entregável:** DAVID guia um membro real pelo primeiro capítulo.

---

### FASE 2 — Dashboard Base (3 semanas)

- [ ] Implementar API de eventos (FastAPI)
- [ ] Criar Skill `reportar_evento_plataforma`
- [ ] Implementar schema PostgreSQL multi-tenant
- [ ] Construir Dashboard do Pastor (Vue 3)
- [ ] Alertas de silêncio em tempo real (WebSocket)

**Entregável:** Pastor vê em tempo real quando membro avança, trava ou para.

---

### FASE 3 — Módulo Admin e Biblioteca (2 semanas)

- [ ] Interface de upload de PDF
- [ ] Workflow de revisão e aprovação
- [ ] Biblioteca Global com metadados e filtros
- [ ] Disponibilização de estudos por organização (Gestor)

**Entregável:** Admin processa um livro do zero até disponível para igrejas.

---

### FASE 4 — Comportamentos Proativos (2 semanas)

- [ ] Hermes Scheduler (cron diário)
- [ ] Devocional matinal automático por membro
- [ ] Detecção e alerta de silêncio
- [ ] Celebração automática de marcos
- [ ] Skill `salvar_pedido_oracao`
- [ ] Dashboard do Gestor com visão panorâmica

**Entregável:** DAVID age sem ser acionado. Pastor recebe alertas.

---

### FASE 5 — Multi-tenant e Multi-plataforma (3 semanas)

- [ ] Wizard de onboarding de nova organização
- [ ] Integração WhatsApp Business API
- [ ] Integração Discord
- [ ] Testes de carga com N organizações simultâneas
- [ ] Dashboard do Administrador (visão global)

**Entregável:** Múltiplas igrejas rodando. DAVID em Telegram + WhatsApp.

---

### FASE 6 — Hardening e Produção

- [ ] LGPD: política de dados e consentimento do membro
- [ ] Backup e recuperação dos perfis
- [ ] Monitoramento de latência e engajamento
- [ ] Guardrails: DAVID nunca extrapola o escopo
- [ ] Guia de suporte para pastores

---

## 12. Modelo de Negócio

### Proposta de Planos

| Plano | Membros | Estudos | Suporte |
|---|---|---|---|
| **Semente** | até 30 | 2 ativos | Documentação (gratuito) |
| **Crescimento** | até 150 | 5 ativos | Chat |
| **Congregação** | até 500 | ilimitados | Prioritário |
| **Rede** | ilimitados | ilimitados | Dedicado |

### O Diferencial Inegociável

Nenhuma plataforma de discipulado hoje combina:

- IA com **memória individual persistente** por membro
- **Pipeline de conteúdo** próprio (PDF → Estudo estruturado)
- **Dashboard pastoral em tempo real**
- Entrega via **Telegram / WhatsApp** (onde as pessoas já estão)
- **Self-hosted** — privacidade, LGPD-friendly, sem nuvem americana
- Custo de infraestrutura mínimo (Ollama local — sem API por mensagem)

---

## Apêndice — A frase que resume o produto

> *Livingstone andava dias a pé para encontrar uma família e acompanhar sua jornada.*
> *O DAVID chega no Telegram de cada membro às 7h da manhã,*
> *com exatamente o que essa pessoa precisa ouvir naquele dia —*
> *enquanto o pastor acompanha tudo no dashboard.*
>
> **Discipulado em escala. Com alma.**

---

*Este documento segue a metodologia Spec-Driven Development (SDD).*
*Nenhuma linha de código deve ser escrita sem `prd.md` + `spec.md` + `design.md` aprovados para cada fase.*
