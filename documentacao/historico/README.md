# Histórico — antes do método

Este diretório é o começo do histórico documentado da evolução. Os documentos
abaixo **nasceram antes** de adotarmos INTENT+SDD (2026-10-16) e ficam onde estão, por
um motivo prático: **comentários de código apontam para eles** (por exemplo
`escritura_service.py` e `load_biblia.py` citam `Diagnostico/referencias-cruzadas.md`).
Movê-los agora obrigaria a mexer em código e redeployar — vira item da DEM piloto.

| Documento | O que registra |
|---|---|
| `GSI_EBD/Diagnostico/arquitetura-atual.md` | retrato da arquitetura na época |
| `GSI_EBD/Diagnostico/plano-bibliotecas.md` | a spec das bibliotecas, **v1 → v2** (o v1 errou o modelo; o v2 tem a correção do Eduardo) |
| `GSI_EBD/Diagnostico/referencias-cruzadas.md` | spike de viabilidade, as duas falhas encontradas e os números medidos |
| `GSI_EBD/Diagnostico/roteiro-de-testes.md` | roteiro de validação do que foi entregue |
| `GSI_EBD/Diagnostico/plano-de-acao.md` | plano antigo (anterior ao método) |
| `GSI_EBD/Diagnostico/plano-hierarquia-e-equipes.md` | estudo de hierarquia |
| `GSI_EBD/Deploy/DEPLOY.md` | runbook de deploy (vira insumo do workflow) |
| `GSI_EBD/Visão.md` · `Evolução.md` | visão inicial e evolução do produto |

> **Regra daqui para frente:** documento novo de governança nasce em
> `documentacao/`. O que é análise pontual de uma mudança nasce dentro da DEM.
