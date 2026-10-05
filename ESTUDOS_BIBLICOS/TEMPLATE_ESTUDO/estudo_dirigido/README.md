# estudo_dirigido/ — Planos de Estudo Dirigido

> **Trilha pedagógica evolutiva, capítulo a capítulo, para acompanhamento estruturado do estudo**

---

## ⚠️ AVISO CRÍTICO

**ESTE É O TEMPLATE_ESTUDO — BASE DE TODOS OS PROJETOS**

Este TEMPLATE **NÃO PODE** ser alterado, a não ser que o **ARQUITETO (Eduardo)** peça explicitamente.

Ele serve como **BASE** para todos os estudos futuros. Quando você for criar um novo estudo, **COPIE** todo o TEMPLATE para a nova pasta e **PERSONALIZE** as informações lá.

**Não altere este TEMPLATE** — ele é a referência para todas as IAs e projetos.

---

## Propósito

Este estudo dirigido não substitui o livro nem os slides do deck. Ele **conduz o estudante pela mão**, em etapas curtas e progressivas, garantindo que cada conceito seja:

1. **Despertado** (curiosidade antes da resposta)
2. **Apresentado** (leitura focada nos pontos centrais)
3. **Testado** (autoavaliação de entendimento)
4. **Comentado** (espaço para reflexão pessoal)
5. **Aplicado** (ponte para a vida cristã)
6. **Consolidado** (síntese e revisão antes do próximo capítulo)

---

## Estrutura da Pasta

```
estudo_dirigido/
├── README.md                              ← Este arquivo
├── _template_plano-de-estudo.md          ← Template para novos planos
├── resumo_bibliografico/                 ← Dados do autor e da obra
│   ├── sobre_autor.md
│   ├── sobre_obra.md
│   ├── contexto_historico.md
│   └── referencias_externas.md
├── capitulo_template/                    ← Template de estrutura de capítulo
│   ├── plano-de-estudo.md
│   ├── leitura-base.md
│   ├── visual-html.md
│   └── videos-apoio.md
├── capitulo_01/                          ← Plano do capítulo 1
│   ├── plano-de-estudo.md
│   ├── leitura-base.md
│   ├── visual-html.md
│   └── videos-apoio.md
├── capitulo_02/                          ← Plano do capítulo 2
│   ├── plano-de-estudo.md
│   ├── leitura-base.md
│   ├── visual-html.md
│   └── videos-apoio.md
└── ...
```

---

## Seção: resumo_bibliografico/

Contém informações biográficas, históricas e contextuais sobre o autor e a obra.

### Arquivos

| Arquivo | Conteúdo |
|---------|----------|
| `sobre_autor.md` | Biografia, formação, carreira do autor |
| `sobre_obra.md` | Histórico, edições, contexto da obra |
| `contexto_historico.md` | Contexto histórico do tema |
| `referencias_externas.md` | Referências bibliográficas adicionais |

**Quando criar um novo estudo**: Personalize os arquivos em `resumo_bibliografico/` com as informações específicas do novo autor e obra.

---

## Seção: capitulo_XX/

Cada capítulo tem **quatro arquivos** que guiam o estudante de forma completa.

### Arquivos por Capítulo

| Arquivo | Propósito |
|---------|-----------|
| `plano-de-estudo.md` | Plano geral de 6 etapas (aquecimento → consolidação) |
| `leitura-base.md` | Roteiro de leitura focada e guiada do capítulo |
| `visual-html.md` | Guia para os slides animados do capítulo |
| `videos-apoio.md` | Curadoria de vídeos complementares |

---

## Como Funciona Cada Arquivo

### 1. plano-de-estudo.md

Segue **sempre a mesma estrutura de 6 etapas**:

| Etapa | Nome | O que o estudante faz |
|-------|------|----------------------|
| **1** | 🔥 Aquecimento | Responde 3 perguntas-gatilho **antes** de ler |
| **2** | 📖 Leitura guiada | Lê o capítulo PT_v1 e o deck |
| **3** | 🧠 Conceitos-chave | Memoriza definições centrais |
| **4** | ✍️ Teste de entendimento | Responde questões e autoavalia |
| **5** | 💭 Reflexão pessoal | Escreve comentários e aplicações |
| **6** | 🏁 Consolidação | Síntese, farol e libera próximo |

### 2. leitura-base.md

Roteiro para leitura focada:

- Objetivos da leitura
- Seção por seção com pontos de foco
- Perguntas de compreensão
- Pós-leitura com verificação
- Estratégias de marcação

### 3. visual-html.md

Guia para os slides animados:

- Estrutura dos slides do deck
- Conexões com o texto do capítulo
- O que observar em cada slide
- Como revisar rapidamente

### 4. videos-apoio.md

Curadoria de vídeos complementares:

- Vídeos principais com detalhes
- Vídeos complementares
- Priorização (alta/média/baixa)
- Sequência recomendada

---

## Recursos Pedagógicos Comuns

### Caixas de Seleção

Use `- [ ]` para marcar progresso:

```markdown
- [ ] Li a seção Perguntas centrais
- [ ] Assisti ao deck animado
```

### Espaços de Resposta

Use `> _Resposta:_` para o estudante escrever:

```markdown
**q1.1** Qual é a pergunta?
> _Resposta:_
```

### Rubrica de Autoavaliação

Tabela para autoavaliação (0–5):

```markdown
| Critério | Nota |
|----------|------|
| Domínio das definições | _/5 |
| Uso correto das passagens bíblicas | _/5 |
| Clareza nas respostas | _/5 |
| Aplicação à vida | _/5 |
```

### Farol Final

Sinalização de progresso:

```markdown
- [ ] 🟢 **Dominado** — posso avançar
- [ ] 🟡 **Em maturação** — voltarei aqui
- [ ] 🔴 **Reler** — refazer etapas 2 e 3
```

---

## Cabeçalho YAML

Cada `plano-de-estudo.md` começa com metadados:

```yaml
---
capitulo: XX
parte: "{I-VII}"
titulo: "{TÍTULO DO CAPÍTULO}"
estudante: ""
status: nao_iniciado        # nao_iniciado | em_andamento | concluido
farol: ""                   # verde | amarelo | vermelho
nota_autoavaliacao: 0       # 0 a 20
data_inicio: ""
data_conclusao: ""
---
```

---

## Como Criar Novo Capítulo

### Método 1: Copiar Templates

```bash
# Copiar plano de estudo
cp estudo_dirigido/_template_plano-de-estudo.md estudo_dirigido/capitulo_XX/plano-de-estudo.md

# Copiar outros arquivos
cp estudo_dirigido/capitulo_template/leitura-base.md estudo_dirigido/capitulo_XX/
cp estudo_dirigido/capitulo_template/visual-html.md estudo_dirigido/capitulo_XX/
cp estudo_dirigido/capitulo_template/videos-apoio.md estudo_dirigido/capitulo_XX/
```

### Método 2: Usar IA

Peça à IA para criar os arquivos baseados no capítulo.

---

## Postura Recomendada ao Estudante

1. **Estude com oração.** A teologia é atividade espiritual (1Co 2.14).
2. **Estude com humildade.** Conhecer mais não autoriza superioridade (1Pe 5.5).
3. **Estude com ritmo.** Um capítulo por semana é saudável.
4. **Escreva no arquivo.** Respostas e dúvidas ficam registradas.
5. **Não pule etapas.** O teste só faz sentido se 1, 2 e 3 foram feitas.
6. **Releia quando ficar 🔴.** Não há vergonha em revisitar.

---

## Como o Progresso é Registrado

Os próprios arquivos são os cadernos do estudante. Cada caixa marcada, cada resposta preenchida e cada farol pintado **fica salvo nos arquivos**.

---

## Convenções de Nomenclatura

### Pastas

- **Formato**: `capitulo_XX/`
- **Exemplo**: `capitulo_01/`, `capitulo_34/`

### Arquivos

- `plano-de-estudo.md` — Plano principal
- `leitura-base.md` — Leitura guiada
- `visual-html.md` — Guia dos slides
- `videos-apoio.md` — Vídeos complementares

---

## Checklist de Qualidade

Antes de considerar um capítulo completo:

- [ ] `plano-de-estudo.md` tem todas as 6 etapas
- [ ] `leitura-base.md` tem seção por seção
- [ ] `visual-html.md` lista todos os slides
- [ ] `videos-apoio.md` tem vídeos priorizados
- [ ] Todos têm links para recursos
- [ ] Cabeçalho YAML preenchido
- [ ] Farol final presente

---

## Exemplo de Estrutura Completa

```markdown
---
capitulo: 01
parte: "I"
titulo: "Introdução à Teologia Sistemática"
estudante: ""
status: nao_iniciado
farol: ""
nota_autoavaliacao: 0
data_inicio: ""
data_conclusao: ""
---

# Capítulo 01 — Introdução à Teologia Sistemática

> **Parte I** — A Doutrina das Escrituras
> Plano de Estudo Dirigido — {Nome do Estudo}

---

## 🔥 Etapa 1 — Aquecimento

**q1.1** O que é teologia?
> _Resposta:_

[...]

## 🏁 Etapa 6 — Consolidação

### Farol final

- [ ] 🟢 **Dominado**
- [ ] 🟡 **Em maturação**
- [ ] 🔴 **Reler**

---

➡️ **Próximo capítulo:** [Capítulo 02](../capitulo_02/plano-de-estudo.md)
```

---

## Para o ARQUITETO (Eduardo)

### Como Criar Novo Estudo

1. **Copie** todo o TEMPLATE_ESTUDO para a nova pasta
2. **Personalize** o README.md principal
3. **Personalize** os arquivos em `resumo_bibliografico/`
4. **Ajuste** o CLAUDE.md e AGENTS.md
5. **Atualize** o mira.config.json

### Instrução para IAs

Quando você pedir para criar um novo estudo, a IA deve:

1. **Pedir** o nome da pasta do novo estudo
2. **Copiar** todo o TEMPLATE para aquela pasta
3. **Usar** o TEMPLATE como referência para todas as tarefas
4. **Direcionar** todas as operações para a nova pasta, nunca alterando o TEMPLATE

---

> *"O conhecimento ensoberbece, mas o amor edifica."* — 1 Coríntios 8.1

---

**Nota**: Este é o TEMPLATE_ESTUDO. Ao criar um novo estudo, copie tudo para a nova pasta e personalize lá.

**Não altere este TEMPLATE a não ser que o ARQUITETO peça explicitamente.**
