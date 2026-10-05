# {NOME DO ESTUDO} — Configuração para Claude Code

> **Estudo teológico baseado no template TEMPLATE_ESTUDO**

---

## ⚠️ AVISO CRÍTICO — TEMPLATE IMUTÁVEL

**TEMPLATE_ESTUDO É A BASE IMUTÁVEL DE TODOS OS PROJETOS**

Este projeto foi criado copiando o TEMPLATE_ESTUDO. O TEMPLATE original em `f:/ESTUDOS_BIBLICOS/TEMPLATE_ESTUDO/` **NÃO DEVE** ser alterado.

### Suas Responsabilidades

1. **Trabalhe neste projeto** — Este é o projeto ativo, edite aqui livremente
2. **Consulte o TEMPLATE** — Use o TEMPLATE como referência para formatos e estruturas
3. **Não altere o TEMPLATE** — NUNCA modifique arquivos em `TEMPLATE_ESTUDO/`

### Quando Criar Novo Estudo

Se o ARQUITETO (Eduardo) pedir para criar um novo estudo:

1. **Peça** o nome da pasta do novo estudo
2. **Copie** todo o TEMPLATE para a nova pasta
3. **Personalize** apenas na nova pasta
4. **Use** este projeto como exemplo

### Verificação de Segurança

Antes de qualquer operação de escrita:

- [ ] Sei qual projeto estou editando?
- [ ] Não estou alterando o TEMPLATE_ESTUDO?
- [ ] Estou operando na pasta correta?

---

## Instruções para o Agente Claude

### 1. Identidade e Linguagem

- **Trate o usuário pelo nome**: Eduardo
- **Idioma**: Sempre responda em **português brasileiro** (pt-BR)
- **Acentuação**: Use acentuação 100% correta em todos os textos
- **Tom**: Respeitoso, acadêmico, mas acessível

### 2. Estrutura do Projeto

Este projeto segue a estrutura padrão do TEMPLATE_ESTUDO:

```
{NOME_DO_PROJETO}/
├── estudo/              ← Conteúdo principal (capítulos)
├── decks/               ← Slides animados do Mira
├── estudo_dirigido/     ← Planos de estudo dirigido
├── docs/                ← Documentação e referências
├── mira-templates/      ← Templates do Mira
└── plano-template-estudo/ ← Templates de planejamento
```

### 3. Regras para Edição de Conteúdo

#### 3.1. Edição de Capítulos

Quando trabalhar com arquivos em `estudo/capitulo_XX/`:

- **NUNCA edite** arquivos `*_EN.md` (originais em inglês)
- **NUNCA edite** arquivos `*_PT.md` (traduções preservadas)
- **SEMPRE edite** apenas arquivos `*_PT_v1.md` (versões corrigidas)

#### 3.2. Formatação de Capítulos (_PT_v1.md)

Siga este padrão:

```markdown
# Título do Capítulo em Português

> **Capítulo N** — Título Original em Inglês

## Perguntas centrais

- q1. Pergunta 1?
- q2. Pergunta 2?
- q3. Pergunta 3?

## I. Explicação e Base Bíblica

### A. Primeira seção principal

#### 1. Subseção

Conteúdo...

> **Definição**: Termo teológico em blockquote

## Notas

[^1]: Nota de rodapé
```

#### 3.3. Convenções Bíblicas

Use abreviações em português:

- Gn = Gênesis
- Êx = Êxodo
- Lv = Levítico
- Nm = Números
- Dt = Deuteronômio
- Sl = Salmos
- Pv = Provérbios
- Is = Isaías
- Mt = Mateus
- Mc = Marcos
- Lc = Lucas
- Jo = João
- At = Atos
- Rm = Romanos
- 1Co = 1 Coríntios
- 2Co = 2 Coríntios
- Ef = Efésios
- Fp = Filipenses
- Cl = Colossenses
- 1Ts = 1 Tessalonicenses
- 1Tm = 1 Timóteo
- 2Tm = 2 Timóteo
- Hb = Hebreus
- Tg = Tiago
- 1Pe = 1 Pedro
- 2Pe = 2 Pedro
- 1Jo = 1 João
- 2Jo = 2 João
- 3Jo = 3 João
- Ap = Apocalipse

### 4. Integração com Mira

Este projeto usa o Mira para criar slides animados:

#### 4.1. Quando Usar Skills do Mira

Use as skills do Mira quando:

- `/mira-new` — Criar um novo deck
- `/mira-extract` — Extrair contexto de um capítulo
- `/mira-planner` — Planejar a estrutura dos slides
- `/mira-copywriter` — Refinar textos dos slides
- `/mira-builder` — Construir slides HTML
- `/mira-animator` — Adicionar animações D3.js
- `/mira-validator` — Validar slides gerados

#### 4.2. Pipeline Padrão

Para criar slides de um capítulo:

1. `/mira-extract` → Extrair conteúdo do capítulo
2. `/mira-planner` → Planejar estrutura dos slides
3. `/mira-copywriter` → Refinar textos
4. `/mira-builder` + `/mira-animator` → Criar slides animados
5. `/mira-validator` → Validar resultado

#### 4.3. Regras de Animação

- **TODA animação** deve entrar com coreografia e DEPOIS continuar em loop interno
- Animação estática é PROIBIDA
- Use SEMPRE as CSS variables do tema (`var(--mira-primary)`, etc.)
- O tema padrão é `mira-dark`

### 5. Criação de Planos de Estudo Dirigido

Para criar planos em `estudo_dirigido/`:

#### 5.1. Estrutura de 6 Etapas

Cada plano deve seguir:

1. **Aquecimento** — 3 perguntas-gatilho antes de ler
2. **Leitura guiada** — Leituras focadas
3. **Conceitos-chave** — Definições a memorizar
4. **Teste de entendimento** — Questões objetivas e dissertativas
5. **Reflexão pessoal** — Espaço para aplicação
6. **Consolidação** — Síntese e farol final

#### 5.2. Elementos Obrigatórios

- Caixas de seleção `- [ ]` para marcar progresso
- Espaços `> _Resposta:_` para o estudante escrever
- Rubrica de autoavaliação (0–5)
- Farol final: 🟢 dominado · 🟡 revisar · 🔴 reler
- Link para próximo capítulo

### 6. Regras de Nomenclatura

#### 6.1. Pastas de Capítulos

- `capitulo_XX/` — XX = número com zero à esquerda (01, 02, etc.)

#### 6.2. Arquivos de Capítulos

- `XX_Titulo_EN.md` — Original em inglês
- `XX_Titulo_PT.md` — Tradução preservada
- `XX_Titulo_PT_v1.md` — Versão corrigida

#### 6.3. Decks

- `xx-nome-do-capitulo/` — kebab-case, número com zero
- `index.html` — Apresentação final
- `briefing.md` — Briefing inicial
- `plano-refinado.md` — Plano de slides

### 7. Documentação em docs/

Ao adicionar documentação:

- **docs/diversos/** — Documentos gerais sobre o projeto
- **docs/referencias/** — Referências bibliográficas
- **docs/videos/** — Links e metadados de vídeos
- **docs/imagens/** — Figuras e diagramas
- **docs/audios/** — Áudios de apoio

### 8. Checklist de Qualidade

Antes de considerar uma tarefa concluída:

- [ ] Acentuação 100% correta
- [ ] Seguiu convenções de nomenclatura
- [ ] Não editou arquivos _EN.md ou _PT.md
- [ ] Usou formato correto para _PT_v1.md
- [ ] Animações têm loop interno (se aplicável)
- [ ] Plano de estudo tem 6 etapas completas
- [ ] Documentação está em docs/

### 9. Prioridade de Atividades

1. **Não perca dados** — Preserve arquivos originais
2. **Mantenha consistência** — Siga convenções estabelecidas
3. **Qualidade sobre quantidade** — Melhor fazer certo que rápido
4. **Comunique claramente** — Explique o que está fazendo

---

## Contexto do Estudo

### Título do Estudo

{NOME_DO_ESTUDO}

### Autor/Referência Principal

{AUTOR_OBRA}

### Descrição

{DESCRICAO_DO_ESTUDO}

### Objetivos

{OBJETIVOS_DO_ESTUDO}

---

> *"Toda a Escritura é soprada por Deus e útil para o ensino, para a repreensão, para a correção e para a instrução na justiça."* — 2 Timóteo 3.16

---

**Este arquivo deve ser personalizado para cada estudo específico.**
