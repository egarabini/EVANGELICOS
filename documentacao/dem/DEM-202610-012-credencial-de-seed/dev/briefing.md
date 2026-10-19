# Briefing do DEVS — DEM-202610-012 (Codex)

> **Para:** Codex (DEVS) · **De:** PLANNER · **Data:** 2026-10-19
> A DEM está **assinada** (`intent.md`, `status: signed`) e as duas perguntas foram fechadas.
> **Nada aqui é para publicar** — a entrega é branch + PR (ADR-016: o DEPLOY publica, e só tag aceita).

## 1. O que ler, nesta ordem

1. `ESTUDOS_BIBLICOS/GSI_EBD/AGENTS.md` — o guarda do código (stack fixa, sem acento, a suíte).
2. `ESTUDOS_BIBLICOS/GSI_EBD/CONVENTIONS.md`.
3. `documentacao/dem/DEM-202610-012-credencial-de-seed/planner/intent.md` — assinado.
4. `.../planner/spec.md` — os RF01–RF07 e a **§5 (o escopo da varredura e as exceções)**.
5. `.../planner/plano-testes.md` — F, N, C, H.

## 2. A tarefa (o escopo é a spec, não além)

- o seed lê a senha de **`SEED_PASSWORD`**; sem ela (ou vazia) **aborta**, antes de tocar no banco;
- **todos** os usuários do seed com `must_change_password=True` — inclusive o admin;
- remover `senha123` de: `gsi_ebd/data/seed.py`, `tests/`, `README.md`, `deploy/DEPLOY.md`,
  `deploy/subir.sh`;
- `.env.example` com `SEED_PASSWORD=` sem valor;
- os testes do plano (inclusive a varredura com a lista e as exceções).

**NÃO faça** (é a D-10, fora desta DEM): `create_gestor` e o texto da tela em
`gsi_ebd/states/admin.py` / `pages/admin.py`. **Não** altere os guardas, o CI, o deploy, os
segredos, a VPS nem o `.env`.

## 3. As regras (não negociáveis)

- **Branch a partir do `develop`**: `feature/DEM-202610-012-credencial-de-seed`; commits pequenos
  em pt-BR explicando o porquê; **PR → develop**.
- **Rodar a suíte do diretório do app** (`ESTUDOS_BIBLICOS/GSI_EBD`) — é lá que o `rxconfig` é lido;
  rodar da raiz faz a suíte falhar por motivo errado.
- **Sem acento** em código e comentários; **com acento** nos docs.
- Não reescreva o domínio; não "melhore" o adjacente.
- Se um teste falhar por causa de uma linha **fora do escopo** (o `create_gestor`), registre no
  relatório em vez de "consertar".

## 4. Definition of Done

- os **CA01–CA05** da spec;
- a suíte do diretório do app: **113 + novos** verdes;
- o **CI verde** no PR;
- o relatório: o que mudou (arquivos), os testes, as decisões, o que ficou fora e por quê.

## 5. O relatório final (o formato)

```
DEM-202610-012 — relatório
- branch: ... | PR: ...
- arquivos: ...
- testes: ... (o comando e o resultado)
- decisões: ...
- fora de escopo (registrado, não corrigido): ...
- riscos/pendências: ...
```

> A D-10 e as demais dívidas são **registro**, não tarefa desta DEM. O EVAL cego julga pelo plano.
