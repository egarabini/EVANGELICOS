# Design — DEM-202610-004 / CI/CD (Fase A3) — Etapa 1

> Dono: PLANNER. O **como** da Etapa 1 (CI). A Etapa 2 (CD) será desenhada quando a CI
> estiver verde e a chave de deploy existir.

## 1. Referência

Spec: [`spec.md`](spec.md) · Intent: [`intent.md`](intent.md) — signed 2026-10-17

## 2. Componentes

| O quê | Onde |
|---|---|
| Workflow de CI | `ESTUDOS_BIBLICOS/GSI_EBD/.github/workflows/ci.yml` *(novo)* |
| Proteção de branch | configuração no GitHub (`main` e `develop`), via `gh api` |
| Nada mais | **nenhum** código de aplicação, nenhuma dependência nova |

## 3. Fluxo

1. O workflow entra em `develop` (é a base dos PRs — a CI roda a partir da base).
2. O push dispara a primeira execução; ela precisa ficar **verde** (82 testes).
3. Proteção ligada em `develop` e `main` exigindo o check `testes (pytest)`.
4. O PR #1 (DEM-001) é ressincronizado (close/reopen) para rodar a CI sobre o código dele.

## 4. Decisões técnicas

- **`ubuntu-latest`** (runner do GitHub, decisão 9.3/ADR-010): nenhum acesso à VPS nesta etapa.
- **Python 3.12** — a mesma versão da imagem de produção; divergir aqui esconde regressão.
- **`pip install -r requirements.txt` + cache** — o `requirements.txt` do repo já é a lista
  completa (foi montado a partir do venv real); cache por arquivo, para não reinstalar a cada PR.
- **`pytest tests -q`** — a mesma suíte local (82 testes), incluindo `tests/test_paginas.py`,
  que é o gate de compilação das páginas.
- **Sem corpus, sem ChromaDB, sem Ollama:** os testes usam dublês; a CI não precisa de nada disso.
- **`permissions: contents: read`** — o workflow não precisa escrever nada.
- **`concurrency`** — push novo cancela a execução anterior da mesma ref.
- **`timeout-minutes: 20`** — instalação do Reflex é pesada; o teto evita job pendurado.

## 5. Migrations / mudanças de dados

- [x] Nenhuma.

## 6. Impacto em código existente

- Nenhum. O workflow é um arquivo novo em `.github/`; a aplicação não o lê.

## 7. O que não muda

- O deploy (continua manual até a Etapa 2), o corpus, a lição, o banco.

## 8. Ordem

1. Criar `.github/workflows/ci.yml`
2. Commit em `develop` e push (bootstrap: ainda não há proteção — ela é o passo 4)
3. Conferir a execução (`gh run list`) até verde
4. Ligar a proteção em `develop` e `main`
5. Ressincronizar o PR #1 e conferir o check nele

## 9. Riscos

- **Instalação pesada** (Reflex + ChromaDB): 3–6 min no primeiro run; o cache resolve nos
  seguintes. Se estourar o timeout, aumenta-se o teto — não se remove teste.
- **Teste dependente do ambiente** (algo que passe só local): a primeira execução é justamente
  o que revela; se aparecer, o DEVS corrige o teste, não a CI.
- **Proteção cedo demais**: se ligada antes do primeiro verde, ninguém mergeia. Por isso o
  verde vem antes.
