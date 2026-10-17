# O projeto — visão e arquitetura atual

## O que é

Uma plataforma de **estudos bíblicos dirigidos**: o aluno percorre um estudo
capítulo a capítulo, responde questões (objetivas, de preenchimento e abertas),
recebe correção humana nos pareceres e tem a **Escritura verificada** ao lado da
lição. Multi-tenant: cada instituição (igreja/escola) tem seu ambiente, com
coordenador, instrutores e alunos.

## Princípio inegociável

**A Escritura vem do corpus, nunca do modelo.** O texto bíblico é recuperado por
igualdade do corpus local (ACF 2007) e o LLM é instruído a não citar versículo de
memória. É o que evita alucinação em conteúdo doutrinário.

## Arquitetura atual

```
Navegador ── HTTPS ── Traefik ── app (Reflex: front + back em Python)
                                   ├── PostgreSQL  (usuários, estudos, progresso, referências cruzadas)
                                   ├── ChromaDB    (31.102 versículos ACF + comentários)
                                   └── Ollama      (gemma2:9b, parecer preliminar)
```

Dois repositórios: **conteúdo** (este, `EVANGELICOS`) e **código**
(`ESTUDOS_BIBLICOS/GSI_EBD`). O conteúdo chega ao container por volume `:ro`.

## Pipeline de conteúdo

```
markdown (obra + plano de estudo)  →  importadores  →  PostgreSQL / ChromaDB
```

- **Obra** = a fonte (livro/coletânea/condensado), em `DOUTRINAS_CRISTAS/docs/base`
- **Estudo** = o material aplicável, em `estudo_dirigido/` (34 capítulos do Grudem)
- **Adendos** = notas de admin+revisor que, com a obra, definem a base do estudo

## O que já funciona (em produção)

Site e HTTPS · login e RBAC (admin/coordenador/instrutor/aluno) · lição com
Escritura e **passagens relacionadas** (OpenBible) · validação de estudo pelo
admin (individual e em lote) · disponibilização de estudo ao aluno · correção
humana com parecer por IA.

## O que ainda não existe

- **Autoria pela interface**: estudo nasce do importador (markdown), não de uma tela
- **Modelo Obra → Estudo** no banco (hoje cada capítulo é um `Study`) — DEM piloto
- **CI/CD** e GitFlow pleno
- **Homologação** e **observabilidade** (alguém avisado quando o site cai)
- **Troca das senhas de demonstração** (ADR-008)
