# plano-template-estudo/ — Templates de Planejamento

> **Templates e padrões para planejamento de estudos, slides e reflexões**

---

## Estrutura da Pasta

```
plano-template-estudo/
├── template_capitulo.md         ← Template para capítulos
├── template_slide.md            ← Template para slides
├── template_reflexao.md         ← Template para reflexões
└── README.md                    ← Este arquivo
```

---

## Templates Disponíveis

### template_capitulo.md

Template para estruturar um novo capítulo do estudo.

**Quando usar**:
- Ao adicionar um novo capítulo ao estudo
- Para garantir consistência de formatação
- Para manter estrutura padrão

**Contém**:
- Estrutura markdown padrão
- Seções principais e subseções
- Formatação de definições
- Notas de rodapé

### template_slide.md

Template para planejar um novo slide do Mira.

**Quando usar**:
- Ao planejar a estrutura de slides
- Para garantir consistência visual
- Para manter padrão de animação

**Contém**:
- Estrutura HTML padrão
- CSS variables do tema
- Placeholder para animação D3.js
- Campos para título, descrição e pílulas

### template_reflexao.md

Template para criar reflexões e aplicações práticas.

**Quando usar**:
- Ao criar questões de reflexão
- Para desenvolver aplicações práticas
- Para estruturar devocionais

**Contém**:
- Questões de reflexão
- Espaços para aplicação
- Campos para oração
- Links para passagens bíblicas

---

## Como Usar os Templates

### 1. Copiar Template

```bash
# Copiar template
cp plano-template-estudo/template_capitulo.md estudo/capitulo_XX/XX_Titulo_PT_v1.md
```

### 2. Personalizar

Edite o arquivo copiado com as informações específicas do capítulo.

### 3. Salvar

Salve no local apropriado seguindo as convenções de nomenclatura.

---

## Estrutura de template_capitulo.md

```markdown
# {TÍTULO DO CAPÍTULO EM PORTUGUÊS}

> **Capítulo {N}** — {Título Original em Inglês}

## Perguntas centrais

- q1. {Primeira pergunta}?
- q2. {Segunda pergunta}?
- q3. {Terceira pergunta}?

## I. Explicação e Base Bíblica

### A. {Primeira seção principal}

#### 1. {Subseção}

{Conteúdo...}

> **Definição**: {Termo teológico}

{Explicação...}

### B. {Segunda seção principal}

#### 1. {Subseção}

{Conteúdo...}

## II. {Outra seção principal}

### A. {Seção secundária}

{Conteúdo...}

## Notas

[^1]: {Primeira nota}
[^2]: {Segunda nota}
```

---

## Estrutura de template_slide.md

```html
<!-- Slide: {NOME DO SLIDE} -->
<div class="slide" data-slide="{N}">
  <div class="mira-card">
    <!-- Header -->
    <div class="card-header">
      <span class="card-label">{LABEL}</span>
      <h2 class="card-title">{TÍTULO DO SLIDE}</h2>
    </div>

    <!-- Canvas de animação -->
    <div class="card-canvas">
      <svg id="animacao-{N}" viewBox="0 0 1920 800">
        <!-- D3.js animation placeholder -->
      </svg>
    </div>

    <!-- Base -->
    <div class="card-base">
      <p class="card-description">{DESCRIÇÃO OU LEGENDA}</p>
      <div class="card-pills">
        <span class="pill" style="background: var(--mira-primary);">{PÍLULA 1}</span>
        <span class="pill" style="background: var(--mira-secondary);">{PÍLULA 2}</span>
        <span class="pill" style="background: var(--mira-accent);">{PÍLULA 3}</span>
      </div>
    </div>
  </div>
</div>
```

---

## Estrutura de template_reflexao.md

```markdown
# Reflexão: {TEMA}

> **Referência**: {LIVRO CAPÍTULO:VERSÍCULO}

## Questões de Reflexão

### 1. Compreensão

{Questão sobre entendimento do conceito}

> _Resposta:_

### 2. Aplicação Pessoal

{Questão sobre aplicação à vida}

> _Resposta:_

### 3. Oração

{Oração relacionada ao tema}

> _Oração:_

## Versículos-chave

- {REFERÊNCIA 1} — {TEMA}
- {REFERÊNCIA 2} — {TEMA}
- {REFERÊNCIA 3} — {TEMA}

## Aplicação Prática

Como isso muda minha vida esta semana?

1. {Ação 1}
2. {Ação 2}
3. {Ação 3}
```

---

## Convenções

### Nomenclatura de Arquivos

- **Templates**: `template_nome.md` (kebab-case)
- **Cópia de uso**: `{nome_especifico}.md`

### Placeholders

Use chaves para placeholders:

```markdown
{NOME_DO_CAMPO}    ← Para substituir
{N}                ← Para números
{TÍTULO}           ← Para títulos
```

---

## Como Criar Novo Template

### 1. Criar Arquivo

```bash
touch plano-template-estudo/template_novo-template.md
```

### 2. Definir Estrutura

```markdown
# template_novo-template.md

> **Propósito**: {Descrição do propósito}

## Quando Usar

- {Caso de uso 1}
- {Caso de uso 2}

## Estrutura

{Estrutura do template}
```

### 3. Documentar

Adicione comentários explicando cada seção.

---

## Exemplos de Uso

### Criar Novo Capítulo

```bash
# 1. Copiar template
cp plano-template-estudo/template_capitulo.md estudo/capitulo_35/35_Titulo_PT_v1.md

# 2. Editar com informações do capítulo 35
# 3. Salvar
```

### Planejar Slide

```bash
# 1. Copiar template
cp plano-template-estudo/template_slide.md decks/35-capitulo/plano-slide-1.md

# 2. Personalizar com conteúdo do slide
# 3. Salvar
```

---

## Checklist de Qualidade

Antes de considerar um template completo:

- [ ] Tem propósito claro
- [ ] Tem instruções de uso
- [ ] Tem placeholders bem definidos
- [ ] Segue convenções do projeto
- [ ] Está documentado
- [ ] Tem exemplos de uso

---

> *"O planejamento é a substituição do acaso pelo erro."* — Albert Einstein

---

**Nota**: Este é o espaço para templates de planejamento. Os estudos finais estão em `estudo/`, os slides em `decks/` e os planos dirigidos em `estudo_dirigido/`.
