# Jornada — DEM-016

- Leituras: intent, autorização de infra, briefing, documentação oficial de arquitetura/API/licença, design DEM-005, AGENTS, PROJECT_CONTEXT e CONVENTIONS.
- Think/List: usuário autorizou expressamente fase 1 sem espera; experimento, interface, configuração, ferramentas, testes e CI isolados. Nenhuma autorização de infra implícita.
- Worktree preexistente C:/Projetos/EM_ESTUDO/EVANGELICOS/.worktrees/DEM-016, branch feature/DEM-202610-016-zitadel, base develop 7670aec; rascunho não commitado aproveitado. Sem checkout/reset no app da DEM-011.
- Corrigido rascunho: host da app separado do issuer, origem CSRF da app, nomes neutros, erros JOSE devolvem 401, issuer fixado no Authlib.
- Código de cliente movido para experiments/identity_client; experiments/zitadel reservado à configuração. Ressalva E-07 registrada.
- Versão oficial consultada via GitHub: v4.19.5. API por h2c, Login V2 separado, licença na tag. Configuração não executada.
- Tentativa de preparar API/Login root rejeitada pela revisão automática; alternativa final usa UID1000:1000, com preparação do volume pendente de autorização. Nenhum comando de infra executado.
- Primeiro teste: 29 passaram, um falhou por comparação case-sensitive dos flags do cookie. Teste corrigido para atributo HTTP case-insensitive.
- Resultado local final: 40 passaram. Compose config --no-interpolate --quiet exit0. Artefatos/resultados de cálculo sintéticos não são métricas da VPS.
- Relatório parcial registra E-01..E-05 não testados em homologação, E-06 estimado, E-07 com ressalva explícita; recomendação adiar adoção.

- Manifests públicos GHCR confirmam API e Login v4.19.5; digests no relatório. Fonte Dockerfiles oficial identifica Login UID1001: ajuste rootless e fluxo API primeiro / permissão PAT 0640 / Login depois, ainda não executado.


## Entrega da fase 1 e CI

Commit `8d894aad283b2cb6a9639a63d6cc0d528a7f3d3f`; [PR #6 draft aberto](https://github.com/egarabini/gsi_ebd/pull/6). [CI do experimento](https://github.com/egarabini/gsi_ebd/actions/runs/39343258566): **40 testes passaram**, Python 3.12, e Compose validado. [CI de regressão](https://github.com/egarabini/gsi_ebd/actions/runs/39343258578): **269 testes passaram**. Ambos verdes no commit entregue. Diff limitado a experiments/ e um workflow isolado; gsi_ebd/, v1/ e deploy/ sem alterações. Worktree limpo.

Autorização a–e solicitada com configuração revisável; nenhuma resposta de aprovação recebida nesta etapa. Fases 2–3 não executadas. Não marcar E-01..E-05 reais como PASS.
