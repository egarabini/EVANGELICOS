# Teologia Sistemática — Configuração para Claude Code

> **Estudo teológico baseado no livro "Teologia Sistemática" de Wayne Grudem**

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
TEOLOGIA_SISTEMATICA/
├── docs/              ← Documentação e referências
├── estudo/            ← Conteúdo principal (capítulos)
├── decks/             ← Slides animados do Mira
├── estudo_dirigido/   ← Planos de estudo dirigido
├── mira-templates/    ← Templates do Mira
└── plano-template-estudo/ ← Templates de planejamento
```

### 3. Regras para Edição de Conteúdo

#### 3.1. Edição de Capítulos

Quando trabalhar com arquivos em `docs/base/`:

- **NUNCA edite** arquivos originais sem confirmação
- **SEMPRE preserve** a estrutura de partes e capítulos
- **Use** a nomenclatura padrão para novos arquivos

#### 3.2. Convenções Bíblicas

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

#### 6.1. Capítulos

- Mantenha a estrutura organizada por Partes (I-VII)
- Cada Parte contém os capítulos correspondentes
- Use prefixo `Cap_` para os arquivos (ex: `Cap_01_A_Trindade.md`)

#### 6.2. Decks

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
- [ ] Preservou estrutura de partes e capítulos
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

Teologia Sistemática — Wayne Grudem

### Autor/Referência Principal

Wayne Grudem — Teólogo reformado, professor e autor

### Descrição

Estudo completo da Teologia Sistemática de Wayne Grudem, cobrindo as principais doutrinas da fé cristã em 7 partes:
- Parte I: A Doutrina da Palavra de Deus
- Parte II: A Doutrina de Deus
- Parte III: A Doutrina do Homem
- Parte IV: A Doutrina de Cristo
- Parte V: A Doutrina da Aplicação da Redenção
- Parte VI: A Doutrina da Igreja
- Parte VII: A Doutrina do Futuro

### Objetivos

1. Proporcionar um estudo sistemático das doutrinas cristãs
2. Criar materiais visuais (slides) para cada capítulo
3. Desenvolver planos de estudo dirigido para aprendizado profundo
4. Documentar referências e recursos adicionais

---

> *"Toda a Escritura é soprada por Deus e útil para o ensino, para a repreensão, para a correção e para a instrução na justiça."* — 2 Timóteo 3.16

---

**Projeto criado em:** 17 de Junho de 2026
**Baseado em:** TEMPLATE_ESTUDO v1.0
