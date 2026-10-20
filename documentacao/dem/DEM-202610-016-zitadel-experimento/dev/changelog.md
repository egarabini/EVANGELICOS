# Changelog — DEM-016

- 20/10, retomada da tentativa controlada: E-01..E-03 PASS, E-04 PASS, E-05 FAIL (mediana 2,474 s). CA local não usada. Recomendação: adiar. Sem commit novo.


- `ceb7d45`: prepara o cliente OIDC isolado, interface, provisão, Compose, testes e ferramentas.
- `8d894aa`: preserva o UID oficial do Login V2, documenta permissões do PAT e registra digests consultados.
- [PR #6 draft](https://github.com/egarabini/gsi_ebd/pull/6), base develop 7670aec. Nenhum merge nem adoção.
- Relatório parcial e evidências ficam nesta pasta (repositório pai); infraestrutura aguarda autorização a-e.


## Entrega da fase 1 e CI

Commit `8d894aad283b2cb6a9639a63d6cc0d528a7f3d3f`; [PR #6 draft aberto](https://github.com/egarabini/gsi_ebd/pull/6). [CI do experimento](https://github.com/egarabini/gsi_ebd/actions/runs/39343258566): **40 testes passaram**, Python 3.12, e Compose validado. [CI de regressão](https://github.com/egarabini/gsi_ebd/actions/runs/39343258578): **269 testes passaram**. Ambos verdes no commit entregue. Diff limitado a experiments/ e um workflow isolado; gsi_ebd/, v1/ e deploy/ sem alterações. Worktree limpo.

Autorização a–e solicitada com configuração revisável; nenhuma resposta de aprovação recebida nesta etapa. Fases 2–3 não executadas. Não marcar E-01..E-05 reais como PASS.


## CI do ajuste autorizado

Commit `dcf136acdc906b0eec9f3e81a7d3dcfbc3c3e1a6`, no mesmo [PR #6 draft aberto](https://github.com/egarabini/gsi_ebd/pull/6). [Experimento](https://github.com/egarabini/gsi_ebd/actions/runs/39344948691): **42 testes verdes** e Compose validado. [Regressão](https://github.com/egarabini/gsi_ebd/actions/runs/39344948669): **269 testes verdes**. Nenhum diff em gsi_ebd/, v1/ ou deploy/. Nenhum merge. O CI não executa a homologação nem resolve a divergência do clone; permanece a devolução ao PLANNER e a pendência de credencial Basic Auth do ARQUITECT.


CA explicita: commit `320bdf56095cfb7340723aaf367b3d54e1bc55a4`, mesmo [PR#6](https://github.com/egarabini/gsi_ebd/pull/6). [CI do experimento](https://github.com/egarabini/gsi_ebd/actions/runs/39401372787): **47 testes passaram**; [regressao](https://github.com/egarabini/gsi_ebd/actions/runs/39401372798): **269 passaram**. Ambos verdes. Nao equivalem a logins reais; terminador e app pendentes da definicao de rota.
