# Pasta capitulo_template — Exemplo de Uso

> **Esta pasta serve como exemplo de como organizar um capítulo**

---

## Estrutura da Pasta

```
capitulo_XX/
├── XX_Titulo_EN.md          ← Original em inglês (NUNCA editar)
├── XX_Titulo_PT.md          ← Tradução preservada (NUNCA editar)
└── XX_Titulo_PT_v1.md       ← Versão corrigida (EDITAR ESTE)
```

---

## Como Criar Novo Capítulo

### 1. Copiar Template

```bash
# Copiar o template de capítulo
cp plano-template-estudo/template_capitulo.md estudo/capitulo_XX/XX_Titulo_PT_v1.md
```

### 2. Adicionar Arquivos

```bash
# Criar pasta
mkdir estudo/capitulo_XX

# Criar arquivos
touch estudo/capitulo_XX/XX_Titulo_EN.md
touch estudo/capitulo_XX/XX_Titulo_PT.md
touch estudo/capitulo_XX/XX_Titulo_PT_v1.md
```

### 3. Preencher Conteúdo

- **XX_Titulo_EN.md**: Colocar o texto original em inglês
- **XX_Titulo_PT.md**: Colocar a tradução original
- **XX_Titulo_PT_v1.md**: Colocar a versão corrigida e formatada

---

## Exemplo de Nomenclatura

### Capítulo 01

```
capitulo_01/
├── 01_Introduction_to_Systematic_Theology_EN.md
├── 01_Introduction_to_Systematic_Theology_PT.md
└── 01_Introduction_to_Systematic_Theology_PT_v1.md
```

### Capítulo 34

```
capitulo_34/
├── 34_The_New_Heavens_and_New_Earth_EN.md
├── 34_The_New_Heavens_and_New_Earth_PT.md
└── 34_The_New_Heavens_and_New_Earth_PT_v1.md
```

---

## Regras Críticas

### ❌ NUNCA Editar

- **Arquivos `*_EN.md`**: São os originais em inglês. Preserve intactos.
- **Arquivos `*_PT.md`**: São as traduções originais. Preserve intactas.

### ✅ SEMPRE Editar

- **Arquivos `*_PT_v1.md`**: São as versões corrigidas e formatadas. Edite livremente.

---

## Formato de Capítulo (_PT_v1.md)

Use o template em `plano-template-estudo/template_capitulo.md`:

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

---

## Abreviações Bíblicas

Use SEMPRE abreviações em português:

### Antigo Testamento

Gn, Êx, Lv, Nm, Dt, Js, Jz, Rt, 1Sm, 2Sm, 1Rs, 2Rs, 1Cr, 2Cr, Ed, Ne, Et, Jó, Sl, Pv, Ec, Ct, Is, Jr, Lm, Ez, Dn, Os, Jl, Am, Ob, Jn, Mq, Na, Hc, Sf, Ag, Zc, Ml

### Novo Testamento

Mt, Mc, Lc, Jo, At, Rm, 1Co, 2Co, Gl, Ef, Fp, Cl, 1Ts, 2Ts, 1Tm, 2Tm, Tt, Fm, Hb, Tg, 1Pe, 2Pe, 1Jo, 2Jo, 3Jo, Jd, Ap

---

## Próximos Passos

1. **Copie** esta estrutura para criar um novo capítulo
2. **Use** o template em `plano-template-estudo/template_capitulo.md`
3. **Preencha** com o conteúdo do capítulo
4. **Siga** as convenções de nomenclatura

---

> *"A Palavra de Deus é viva, eficaz e mais cortante do que qualquer espada de dois gumes."* — Hebreus 4.12
