> **RESOLVIDO:** o ARQUITECT autorizou criar o clone; criado em dcf136a. Este documento preserva o histórico. O impedimento atual está em impedimento-tls.md.

# DEM-016 — devolução ao PLANNER: preflight do clone

Status: infraestrutura interrompida; configuração local atualizada no PR #6, commit dcf136a.

## Evidência somente de leitura

- `ssh -o BatchMode=yes -o ConnectTimeout=10 didasko-vps 'id -un'` => didasko-deploy, exit0.
- `test -d /home/didasko-deploy/experimentos/didasko/.git` => clone=absent. O teste não identificou o clone Git próprio esperado; não afirma se existe um diretório vazio ou arquivo .git. Não foi tentada criação, correção ou outro caminho.
- `sudo -n docker network inspect deploy_didasko --format 'edge_network={{.Name}}'` => edge_network=deploy_didasko.
- Listagens de containers e volumes filtradas por `com.docker.compose.project=experimento-oidc` sem recursos retornados.

## Providência do PLANNER / ARQUITECT

Confirmar a preparação do clone próprio no caminho autorizado ou esclarecer a divergência antes de retomar. O alias SSH funciona; não é necessário fornecer chave pelo chat. A credencial Basic Auth deve ser disponibilizada pelo ARQUITECT em arquivo600/canal seguro; informar somente caminho, nunca usuário/senha/hash no chat. As condições a-d já estão autorizadas e foram aplicadas à configuração; nenhuma infraestrutura foi criada. Desmonte continua dependente da confirmação na hora.

Texto do relatório até existirem números: **o código está pronto; o veredito depende da homologação**. Nenhuma recomendação nem FAIL técnico do provedor resulta desse impedimento. Sem login real, medidas reais, carga Ollama, geração de segredo ou alteração na VPS.


## CI do ajuste autorizado

Commit `dcf136acdc906b0eec9f3e81a7d3dcfbc3c3e1a6`, no mesmo [PR #6 draft aberto](https://github.com/egarabini/gsi_ebd/pull/6). [Experimento](https://github.com/egarabini/gsi_ebd/actions/runs/39344948691): **42 testes verdes** e Compose validado. [Regressão](https://github.com/egarabini/gsi_ebd/actions/runs/39344948669): **269 testes verdes**. Nenhum diff em gsi_ebd/, v1/ ou deploy/. Nenhum merge. O CI não executa a homologação nem resolve a divergência do clone; permanece a devolução ao PLANNER e a pendência de credencial Basic Auth do ARQUITECT.
