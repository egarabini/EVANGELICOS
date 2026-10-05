# estudo/ — Conteúdo Principal do Estudo

> **Capítulos, textos originais e traduções do estudo**

---

## Estrutura da Pasta

```
estudo/
├── capitulo_01/          ← Capítulo 1
│   ├── 01_Titulo_EN.md       ← Original em inglês (NUNCA editar)
│   ├── 01_Titulo_PT.md       ← Tradução preservada (NUNCA editar)
│   └── 01_Titulo_PT_v1.md    ← Versão corrigida (EDITAR ESTE)
├── capitulo_02/          ← Capítulo 2
├── capitulo_03/          ← Capítulo 3
└── README.md             ← Este arquivo
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

## Como Adicionar Novo Capítulo

```bash
# Criar pasta
mkdir estudo/capitulo_XX

# Criar arquivos
touch estudo/capitulo_XX/XX_Titulo_EN.md
touch estudo/capitulo_XX/XX_Titulo_PT.md
touch estudo/capitulo_XX/XX_Titulo_PT_v1.md
```

---

## Convenções de Nomenclatura

### Pastas

- **Formato**: `capitulo_XX/`
- **Exemplo**: `capitulo_01/`, `capitulo_34/`
- **Regra**: Sempre dois dígitos, zero à esquerda para 01-09

### Arquivos

| Tipo | Sufixo | Descrição |
|------|--------|-----------|
| Original | `_EN.md` | Texto original em inglês |
| Tradução | `_PT.md` | Tradução preservada |
| Corrigido | `_PT_v1.md` | Versão corrigida |

---

## Checklist de Qualidade

Antes de considerar um capítulo completo:

- [ ] Acentuação 100% correta
- [ ] Seguiu estrutura padrão
- [ ] Usou abreviações bíblicas corretas
- [ ] Definições em blockquote
- [ ] Notas de rodapé formatadas
- [ ] Não editou _EN.md ou _PT.md

---

> *"A Palavra de Deus é viva, eficaz e mais cortante do que qualquer espada de dois gumes."* — Hebreus 4.12
