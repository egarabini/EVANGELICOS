# README_IA — Instruções para IAs

> **Arquitetura Centralizada — TEMPLATE_ESTUDO como Fonte de Verdade**

---

## 🏗️ ARQUITETURA DO SISTEMA

```
┌─────────────────────────────────────────────────────────────┐
│  TEMPLATE_ESTUDO (Fonte de VERDADE)                         │
│  📍 f:/ESTUDOS_BIBLICOS/TEMPLATE_ESTUDO/                    │
│                                                              │
│  - Templates de capítulos                                    │
│  - Templates de slides                                       │
│  - Templates de planos de estudo                             │
│  - Convenções e formatação                                   │
│  - Todas as regras e padrões                                │
│                                                              │
│  ⚠️ IMUTÁVEL — Só o ARQUITETO (Eduardo) altera             │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Todas as IAs LEEM daqui
                              │ (como referência externa)
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  DOUTRINAS_CRISTAS (ou qualquer estudo)                      │
│  📍 f:/ESTUDOS_BIBLICOS/{NOME_DO_ESTUDO}/                    │
│                                                              │
│  - Conteúdo dos estudos (capítulos)                          │
│  - Decks de slides gerados                                   │
│  - Planos de estudo preenchidos                              │
│  - Documentação específica                                   │
│                                                              │
│  ✅ LIMPO — Sem templates replicados                         │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚠️ REGRA FUNDAMENTAL

### TEMPLATE_ESTUDO = Fonte de Verdade (READ-ONLY para IAs)

**O TEMPLATE_ESTUDO é consultado, nunca copiado.**

### Para IAs:

✅ **FAZER**:
- **LER** templates do TEMPLATE_ESTUDO quando necessário
- **CONSULTAR** convenções e padrões do TEMPLATE_ESTUDO
- **CRIAR** arquivos nos projetos usando os templates como referência
- **RESPEITAR** a estrutura definida no TEMPLATE_ESTUDO

❌ **NÃO FAZER**:
- **NÃO copiar** templates do TEMPLATE para os projetos
- **NÃO duplicar** arquivos do TEMPLATE nos projetos
- **NÃO alterar** nada no TEMPLATE_ESTUDO
- **NÃO criar** versões locais de templates

---

## COMO FUNCIONA NA PRÁTICA

### Cenário 1: Criar Novo Capítulo

**IA deve:**

1. **LER** o template em `TEMPLATE_ESTUDO/plano-template-estudo/template_capitulo.md`
2. **CRIAR** o arquivo no projeto com base no template lido
3. **PERSONALIZAR** com o conteúdo do capítulo

```bash
# ✅ CORRETO
# IA lê o template e cria arquivo novo
TEMPLATE: template_capitulo.md (lido apenas)
PROJETO: capitulo_01/01_Titulo_PT_v1.md (criado)

# ❌ INCORRETO (não fazer)
# Copiar template para o projeto
```

### Cenário 2: Criar Plano de Estudo

**IA deve:**

1. **LER** o template em `TEMPLATE_ESTUDO/estudo_dirigido/_template_plano-de-estudo.md`
2. **CRIAR** o arquivo no projeto com base no template
3. **PREENCHER** com informações específicas do capítulo

### Cenário 3: Criar Deck do Mira

**IA deve:**

1. **CONSULTAR** templates em `TEMPLATE_ESTUDO/mira-templates/`
2. **SEGUIR** padrões definidos no TEMPLATE
3. **CRIAR** deck na pasta do projeto

---

## CAMINHO DO TEMPLATE

### Localização do TEMPLATE

```
f:/ESTUDOS_BIBLICOS/TEMPLATE_ESTUDO/
```

### Templates Principais

| Template | Caminho no TEMPLATE |
|----------|---------------------|
| Capítulo | `plano-template-estudo/template_capitulo.md` |
| Slide | `plano-template-estudo/template_slide.md` |
| Reflexão | `plano-template-estudo/template_reflexao.md` |
| Plano de estudo | `estudo_dirigido/_template_plano-de-estudo.md` |
| Leitura base | `estudo_dirigido/capitulo_template/leitura-base.md` |
| Visual HTML | `estudo_dirigido/capitulo_template/visual-html.md` |
| Vídeos | `estudo_dirigido/capitulo_template/videos-apoio.md` |
| Sobre autor | `estudo_dirigido/resumo_bibliografico/sobre_autor.md` |
| Sobre obra | `estudo_dirigido/resumo_bibliografico/sobre_obra.md` |

---

## QUANDO CRIAR NOVO ESTUDO

### Passo 1: Identificar Solicitação

Quando o ARQUITETO pedir para criar um novo estudo:

1. **Peça** o nome da pasta do novo estudo
2. **Peça** o autor/obra principal
3. **Confirme** o local

### Passo 2: Criar Estrutura Mínima

```bash
# Criar apenas pastas, sem copiar templates
mkdir "f:/ESTUDOS_BIBLICOS/{NOVO_ESTUDO}/estudo"
mkdir "f:/ESTUDOS_BIBLICOS/{NOVO_ESTUDO}/decks"
mkdir "f:/ESTUDOS_BIBLICOS/{NOVO_ESTUDO}/estudo_dirigido"
mkdir "f:/ESTUDOS_BIBLICOS/{NOVO_ESTUDO}/docs"
```

### Passo 3: Criar README.md Personalizado

Crie um README.md no projeto com informações específicas, consultando o TEMPLATE quando necessário.

### Passo 4: Criar resumo_bibliografico/

Consulte os templates em `TEMPLATE_ESTUDO/estudo_dirigido/resumo_bibliografico/` e crie os arquivos no projeto.

---

## ESTRUTURA DE UM PROJETO LIMPO

```
{NOME_DO_ESTUDO}/
│
├── README.md                    ← Personalizado para o estudo
│
├── estudo/                      ← Conteúdo dos capítulos
│   ├── capitulo_01/
│   │   ├── 01_Titulo_EN.md
│   │   ├── 01_Titulo_PT.md
│   │   └── 01_Titulo_PT_v1.md
│   └── capitulo_02/
│       └── ...
│
├── decks/                       ← Decks gerados
│   ├── 01-capitulo-1/
│   │   └── index.html
│   └── 02-capitulo-2/
│       └── index.html
│
├── estudo_dirigido/             ← Planos de estudo
│   ├── resumo_bibliografico/
│   │   ├── sobre_autor.md       ← Criado com base no TEMPLATE
│   │   ├── sobre_obra.md        ← Criado com base no TEMPLATE
│   │   ├── contexto_historico.md
│   │   └── referencias_externas.md
│   ├── capitulo_01/
│   │   ├── plano-de-estudo.md   ← Criado com base no TEMPLATE
│   │   ├── leitura-base.md      ← Criado com base no TEMPLATE
│   │   ├── visual-html.md       ← Criado com base no TEMPLATE
│   │   └── videos-apoio.md      ← Criado com base no TEMPLATE
│   └── capitulo_02/
│       └── ...
│
└── docs/                        ← Documentação específica
    ├── diversos/
    └── referencias/
```

**Nota:** Nenhum template é copiado fisicamente. Todos são consultados no TEMPLATE_ESTUDO quando necessário.

---

## VANTAGENS DESTA ARQUITETURA

### 1. Projetos Limpos

- Sem redundância de templates
- Apenas conteúdo específico do estudo
- Fácil navegação

### 2. Evolução Centralizada

- Atualizações no TEMPLATE afetam todos os projetos automaticamente
- Um lugar para manutenção
- Sem necessidade de atualizar múltiplas cópias

### 3. Consistência Garantida

- Todas as IAs usam a mesma fonte de verdade
- Sem versões desatualizadas de templates
- Padrões uniformes em todos os projetos

### 4. Eficiência

- Menos espaço em disco
- Projetos mais leves
- Manutenção simplificada

---

## EXEMPLO DE FLUXO DE TRABALHO

### Usuário: "Vamos criar um estudo sobre Teologia da Adoração"

### IA (Fluxo Correto):

```
1. Peço informações do estudo

2. Crio estrutura de pastas:
   - estudo/
   - decks/
   - estudo_dirigido/
   - docs/

3. Consulto TEMPLATE_ESTUDO para:
   - Ler template de sobre_autor.md
   - Criar arquivo no projeto com dados do autor

4. Para cada capítulo:
   - Leio templates do TEMPLATE
   - Crio arquivos no projeto
   - Nunca copio templates fisicamente
```

---

## VERIFICAÇÃO DE SEGURANÇA

Antes de qualquer operação, pergunte:

- [ ] Estou CRIANDO arquivo no projeto, não copiando template?
- [ ] Sei que o TEMPLATE é READ-ONLY?
- [ ] Consultei o TEMPLATE apenas como referência?
- [ ] O projeto fica limpo sem templates duplicados?

---

## RESUMO

### Fonte de Verdade

- **TEMPLATE_ESTUDO** em `f:/ESTUDOS_BIBLICOS/TEMPLATE_ESTUDO/`
- **READ-ONLY** para IAs
- **Consultado**, nunca copiado

### Projetos

- **Conteúdo apenas**
- **Sem templates replicados**
- **Limpos e focados**

### Para o ARQUITETO (Eduardo)

- Evolução do modelo fica no TEMPLATE
- Projetos preservam seu conhecimento específico
- Arquitetura limpa e escalável

---

> *"A simplicidade é o último grau de sofisticação."* — Leonardo da Vinci

---

**Versão**: 2.0 (Arquitetura Centralizada)
**Data**: 17 de Junho de 2026
**Princípio**: TEMPLATE = Fonte de Verdade (READ-ONLY)
