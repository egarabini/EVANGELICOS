# DEM-202610-012 — credencial de seed

## Finalidade

Tirar a **senha conhecida** do seed (`senha123`), que, com o repositório público e o site no ar,
deixava qualquer leitor entrar como **admin** — e que depois da DEM-002 é o único papel que aprova
estudo, gerencia usuários e vê leads.

## Elo com a governança

- Intent, spec e plano: [`planner/`](planner/) — **intent assinado em 2026-10-19** (as 4 decisões 8.1-8.5)
- ADRs: **008** (segredos) · **018** (D-01, D-10) · **ADR-016** (a publicação)
- O executor: **o Codex** (a decisão da [DEM-014](../DEM-202610-014-codex-como-devs/README.md))
- A base: `gsi_ebd/data/seed.py`

## Estado

- [x] Intent assinado; spec e plano (v2, com os 4 ajustes de 19/10 e a D-10 fora do escopo)
- [x] Implementação pelo Codex — **PR #3** (`427e8bb`): 6 arquivos, **exatamente** o escopo
- [x] **EVAL cego: PASS** — [`eval/parecer.md`](eval/parecer.md): **128 testes** (rodados do diretório do app), os **RF01-RF07** com evidência
- [x] **CI verde**; **mergeado no `develop`** (`dbbfc09`) e a branch apagada
- [ ] **Aceite do ARQUITECT** — junto com o release da v1
- [ ] **D-01** — a rotação das contas em produção e o repasse do `SEED_PASSWORD` no Compose **não** são desta DEM
- [ ] **D-11** — o achado do Copilot (abaixo)

## As ressalvas (que o EVAL registrou — e eu concordo)

1. **O Compose não repassa `SEED_PASSWORD` ao contêiner.** O `--env-file .env` alimenta a
   interpolação do compose, **não** o ambiente do container, a menos que a variável esteja no
   `environment:` do serviço. Com isso, **só pôr a senha no `.env` da VPS não basta** — a
   semeadura de um banco novo pelo pipeline continua bloqueada até o Compose ser ajustado (operação
   de infraestrutura, autorização do ARQUITECT).
2. **A rotação das contas que já existem é manual e do ARQUITECT.** A `senha123` do admin **atual**
   de produção continua valendo até ele trocar. Por isso a DEM-012 **não fecha a D-01 nem a D-10**.
3. **O banco de teste é SQLite temporário.** A verificação não cobre a produção.

## O achado do Copilot — a D-11

O revisor automático apontou um gap **real**: a troca obrigatória é um **redirecionamento** no
login, mas `guarda_rota`/`exige` **não verificam** `must_change_password`. Ou seja: o admin
recém-criado pode navegar direto para `/admin` e executar `activate_user` **sem trocar a senha**.

É um gap **pré-existente** (o `create_gestor` já criava contas com a flag, e o mesmo buraco
valia), **não introduzido** por este PR — mas agora ele afeta **todos** os usuários do seed.

**Registrado como D-11** (gatilho: antes de dados reais), com a proposta de ser a **DEM-015**
(nível 3, pequena): bloquear as rotas e os eventos protegidos enquanto a flag estiver ativa,
preservando o acesso à troca de senha e ao logout; e os testes de acesso direto e de evento antes
da troca — o teste atual só cobre o redirecionamento.
