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

## As ressalvas (o relatório final do EVAL — e eu concordo)

1. **A-1 — no local apenas; NÃO é pré-requisito do D-01.** O `.env` sozinho não é lido (o
   `seed_password()` roda antes do `load_dotenv()` do rxconfig) — mas **em produção o seed roda no
   contêiner e o `.dockerignore` exclui o `.env` da imagem**: não há `.env` para carregar lá. O
   A-1 só ajudaria rodadas locais. **Não despachar o Codex para isso.** Se tocar no `seed.py` por
   outro motivo, aproveitar o **A-6**: `SEED_PASSWORD` com um espaço deve ser recusada (`.strip()`).
2. **A-2 — o Compose não repassa `SEED_PASSWORD`** ao serviço `app` (linhas 72-97); o DEPLOY.md
   documenta a pendência (117-120). É *fail-safe* (o seed aborta), mas a **operação está
   bloqueada**. **Duas opções** (decisão do ARQUITECT — infra, ADR-016):
   **(a) preferida** — passar só no momento do seed: `docker compose exec -e SEED_PASSWORD ...`
   no `subir.sh`, com o valor vindo do **ambiente do script** (não da linha de comando);
   **(b)** gravar no `environment:` do Compose — fica **permanente** no contêiner.
3. **A rotação das contas que já existem é manual e do ARQUITECT.** A `senha123` do admin **atual**
   continua valendo até ele trocar — a DEM **não fecha a D-01 nem a D-10**.
4. **O banco de teste é SQLite temporário.** A verificação não cobre a produção.

**Não bloqueantes (A-3 a A-6):** o F-07 é mais fraco que o N-01; o N-04 só enxerga o repositório
do app (as exceções de DEM/EVAL/ADR-008 são do guarda-chuva); o `tests/` é varrido só em `*.py`;
e `SEED_PASSWORD=" "` (um espaço) é aceita — a spec só proíbe vazio.

**A recomendação do EVAL:** PASS de **código**; o fechamento da **D-01** fica **condicionado à
decisão A-1/A-2** — a variável precisa **chegar de fato** ao processo/contêiner.

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
