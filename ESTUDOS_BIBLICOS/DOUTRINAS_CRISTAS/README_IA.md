# README_IA — Instruções para IAs

> **Guia para agentes de IA sobre como usar o TEMPLATE_ESTUDO**

---

## ⚠️ REGRA FUNDAMENTAL

**TEMPLATE_ESTUDO É IMUTÁVEL**

NUNCA altere arquivos dentro de `TEMPLATE_ESTUDO/`. Este é a BASE de todos os projetos e deve ser preservado intacto.

---

## Quando Criar um Novo Estudo

### 1. Identificar a Solicitação

Quando o ARQUITETO (Eduardo) pedir para "criar um novo estudo" ou "iniciar um projeto de estudo":

✅ **FAZER**:
- Pedir o nome da pasta do novo estudo
- Pedir o nome do autor/obra (se não informado)

❌ **NÃO FAZER**:
- Não começar a criar arquivos sem saber a pasta
- Não alterar o TEMPLATE
- Não assumir nomes ou caminhos

### 2. Confirmar a Estrutura

Antes de copiar, confirme:

```
NOVO ESTUDO: {NOME DO ESTUDO}
PASTA: {CAMINHO COMPLETO}
AUTOR: {NOME DO AUTOR}
OBRA: {NOME DA OBRA}

Você confirma? (s/n)
```

### 3. Copiar o TEMPLATE

Use o comando de cópia apropriado:

```bash
# Copiar todo o TEMPLATE para a nova pasta
cp -r "f:/ESTUDOS_BIBLICOS/TEMPLATE_ESTUDO/"* "f:/ESTUDOS_BIBLICOS/{NOVA_PASTA}/"
```

### 4. Personalizar o Novo Projeto

Depois de copiar, personalize na NOVA pasta:

1. **README.md principal** — Atualizar com informações do novo estudo
2. **resumo_bibliografico/** — Preencher com dados do autor e obra
3. **CLAUDE.md e AGENTS.md** — Atualizar com contexto específico
4. **mira.config.json** — Atualizar nome do projeto

---

## Durante o Trabalho no Projeto

### Consultar o TEMPLATE

Quando precisar de referência:

✅ **CONSULTE** o TEMPLATE para ver:
- Estrutura de pastas
- Formatos de arquivos
- Convenções de nomenclatura
- Templates de documentos

❌ **NÃO ALTERE** o TEMPLATE:
- Não modifique arquivos no TEMPLATE
- Não adicione novos arquivos no TEMPLATE
- Não crie estruturas no TEMPLATE

### Trabalhar no Projeto

Todas as edições devem ser na pasta do NOVO estudo:

```
TEMPLATE_ESTUDO/     ← NÃO TOCAR (referência apenas)
    ├── estudo/
    ├── decks/
    └── ...

NOVO_ESTUDO/         ← TRABALHAR AQUI
    ├── estudo/
    ├── decks/
    └── ...
```

---

## Situações Comuns

### Situação 1: Criar Novo Capítulo

1. **Verifique** em qual projeto está trabalhando
2. **Se for TEMPLATE**: Recuse e peça para criar projeto primeiro
3. **Se for projeto**: Use os templates do `plano-template-estudo/`

### Situação 2: Gerar Slides

1. **Verifique** se está na pasta do projeto correto
2. **Use** os templates de `mira-templates/` como referência
3. **Crie** os arquivos na pasta `decks/` do projeto

### Situação 3: Adicionar Documentação

1. **Consulte** `docs/README.md` do TEMPLATE para ver estrutura
2. **Crie** arquivos na pasta `docs/` do projeto
3. **Siga** as convenções estabelecidas

---

## Verificação de Segurança

Antes de qualquer operação de escrita, pergunte:

### Checklist Pré-escrita

- [ ] Estou operando na pasta do NOVO estudo, não no TEMPLATE?
- [ ] O arquivo que vou criar/alterar está no projeto correto?
- [ ] Não vou alterar nenhum arquivo em TEMPLATE_ESTUDO/?
- [ ] Sei qual é a pasta raiz do projeto?

Se qualquer resposta for **NÃO**, **PARE** e peça clarificação.

---

## Estrutura do TEMPLATE (Referência)

```
TEMPLATE_ESTUDO/
├── README.md                ← Documentação geral
├── CLAUDE.md                ← Configuração Claude
├── AGENTS.md                ← Configuração outros agentes
├── CONVENTIONS.md           ← Convenções do projeto
├── .cursorrules             ← Regras Cursor
├── mira.config.json         ← Config Mira
│
├── docs/                    ← Documentação
├── estudo/                  ← Conteúdo principal
├── decks/                   ← Slides Mira
├── estudo_dirigido/         ← Planos de estudo
│   ├── resumo_bibliografico/ ← Dados autor/obra
│   └── capitulo_XX/          ← Por capítulo
│       ├── plano-de-estudo.md
│       ├── leitura-base.md
│       ├── visual-html.md
│       └── videos-apoio.md
├── mira-templates/          ← Templates Mira
└── plano-template-estudo/   ← Templates de planejamento
```

---

## Convenções Importantes

### Nomenclatura de Pastas

- `capitulo_XX/` — Sempre dois dígitos (01, 02, etc.)
- `xx-nome-do-capitulo/` — Kebab-case para decks

### Nomenclatura de Arquivos

- `XX_Titulo_EN.md` — Original em inglês
- `XX_Titulo_PT.md` — Tradução preservada
- `XX_Titulo_PT_v1.md` — Versão corrigida

### Regras de Edição

- **NUNCA** edite `_EN.md` ou `_PT.md`
- **SEMPRE** edite `_PT_v1.md`

---

## Exemplo de Fluxo Correto

### Usuário: "Vamos criar um estudo sobre Teologia da Adoração"

### IA (Resposta Correta):

```
Entendido! Vou criar um novo estudo baseado no TEMPLATE_ESTUDO.

Para isso, preciso de algumas informações:

1. Qual o nome da pasta do novo estudo?
   (Sugestão: Teologia_Adoração)

2. Qual o autor/obra principal?
   (Ex: "Teologia da Adoração" — John Frame)

3. Onde devo criar a pasta?
   (Sugestão: f:/ESTUDOS_BIBLICOS/Teologia_Adorado)

Confirme essas informações e prosseguirei.
```

### IA (Resposta Incorreta — NÃO FAZER ISSO):

```
Ok, vou começar criando os arquivos...
[IA começa a criar arquivos sem confirmar pasta]
```

---

## Resumo

### O QUE FAZER

✅ Consultar o TEMPLATE como referência
✅ Copiar o TEMPLATE para criar novos projetos
✅ Trabalhar nas pastas dos novos projetos
✅ Seguir as convenções estabelecidas

### O QUE NÃO FAZER

❌ Alterar arquivos no TEMPLATE_ESTUDO
❌ Criar arquivos dentro do TEMPLATE
❌ Trabalhar no TEMPLATE em vez de no projeto
❌ Assumir caminhos sem confirmar

---

> *"A disciplina é a alma de um projeto. Preservar a base é essencial para o crescimento."*

---

**Lembre-se**: O TEMPLATE é imutável. Preserve-o para garantir consistência em todos os projetos futuros.

---

**Versão**: 1.0
**Data**: 17 de Junho de 2026
**Para**: Todas as IAs que trabalham com TEMPLATE_ESTUDO
