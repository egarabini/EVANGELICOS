# Changelog — DEM-016

- `ceb7d45`: prepara o cliente OIDC isolado, interface, provisão, Compose, testes e ferramentas.
- `8d894aa`: preserva o UID oficial do Login V2, documenta permissões do PAT e registra digests consultados.
- [PR #6 draft](https://github.com/egarabini/gsi_ebd/pull/6), base develop 7670aec. Nenhum merge nem adoção.
- Relatório parcial e evidências ficam nesta pasta (repositório pai); infraestrutura aguarda autorização a-e.


## Entrega da fase 1 e CI

Commit `8d894aad283b2cb6a9639a63d6cc0d528a7f3d3f`; [PR #6 draft aberto](https://github.com/egarabini/gsi_ebd/pull/6). [CI do experimento](https://github.com/egarabini/gsi_ebd/actions/runs/39343258566): **40 testes passaram**, Python 3.12, e Compose validado. [CI de regressão](https://github.com/egarabini/gsi_ebd/actions/runs/39343258578): **269 testes passaram**. Ambos verdes no commit entregue. Diff limitado a experiments/ e um workflow isolado; gsi_ebd/, v1/ e deploy/ sem alterações. Worktree limpo.

Autorização a–e solicitada com configuração revisável; nenhuma resposta de aprovação recebida nesta etapa. Fases 2–3 não executadas. Não marcar E-01..E-05 reais como PASS.
