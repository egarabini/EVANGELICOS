# DEM-202610-011 — relatório da fatia 1, ADR-020 / design v7

- **Branch:** `feature/DEM-202610-011-fatia1-dominio`, criada de `develop` (`dbbfc09`).
- **Mesmo PR:** https://github.com/egarabini/gsi_ebd/pull/4 → `develop`, aberto, sem merge.
- **Commit deste delta:** `bab117e67ce8c5ed5ae684f0b9cd7483ab9fc5d0`.
- **Referência:** ADR-020 aceita, design v7 e plano v4, relidos antes da implementação e após a clarificação do ARQUITECT sobre estado editorial × publicação.
- **Arquivos:** `gsi_ebd/models/obra.py`, `gsi_ebd/models/__init__.py`, `gsi_ebd/services/flow.py`, `tests/test_flow.py`.

## A autoridade e a entrega

O estado editorial pertence à versão: `revisar` leva a `aguardando_admin` e `recusar` a `devolvida`. Isso **não altera o ponteiro publicado nem a disponibilidade**. Só o Admin importa, abre, suspende, cancela e libera ciclos. `Obra.status` acompanha o estado da versão corrente; o que está no ar é identificado por `versao_liberada_id`.

`contestar` foi removido do serviço. O teste antigo que exigia reabrir e despublicar a mesma versão foi removido e substituído pelo F-06 do plano v4. A semântica v5 está superada pela ADR-020; os registros históricos dos deltas anteriores são mantidos na jornada.

Modelos:

- `Obra.disponibilidade`: `aberta` ou `suspensa_para_novos`, separada do estado editorial.
- Novo `VinculoObra`, registrado no metadata: ambiente, obra, versão fixada, coordenador, ativo e data.
- Versões, snapshots LF/NFC, rodada e trilha de eventos continuam. A unicidade das snapshots inclui versão/momento/rodada e ordem/código porque há uma linha por item.

Operações novas:

- `solicitar_revisao(sessao, versao, revisor, motivo)` registra evento/pedido e retorna o evento, sem mudar publicação, disponibilidade ou a versão liberada.
- `aceitar_solicitacao(sessao, obra, admin)` cria a próxima versão e suspende novas vinculações; retorna a versão nova.
- `dispensar_solicitacao(sessao, obra, admin, motivo)` exige motivo não vazio e retorna o evento da resposta, referenciando o pedido. O texto fica na trilha, acessível à futura UI do Revisor.
- `cancelar_ciclo(sessao, obra, admin)` cancela logicamente a versão pendente e reabre a disponibilidade, mantendo N como liberada.
- `posicionar(sessao, versao, revisor, posicao, texto)` registra `posicao`, com `concordo`/`objeto` e texto, sem bloquear o Admin.
- `vincular(sessao, ambiente, obra, coordenador)` exige o dono do ambiente, disponibilidade aberta e versão liberada; grava `versao_id` fixo. A leitura posterior do vínculo/snapshots não depende da disponibilidade corrente.

Solicitações são representadas pela trilha append-only existente: `revisao_solicitada`, `solicitacao_aceita` e `solicitacao_dispensada`, as respostas com `solicitacao_id`. Um pedido pendente por obra e um ciclo pendente por obra. Não foi criada outra tabela de solicitações.

`alterar` cria N+1 e suspende para novos, sem mudar a N publicada ou seus instantâneos. `liberar` exige assinatura e Admin; ao publicar N+1, marca N como `substituida`, atualiza o ponteiro e volta a `aberta`. Vínculos anteriores permanecem fixados em N, ainda legível. Pedido e posição do Revisor nunca suspendem nada.

## Rodadas dentro da versão

A rodada continua apenas dentro de versão **ainda não publicada**. A recusa pode retirar um parecer em `aguardando_admin`; o Admin reenvia e o próximo `revisar` abre outra rodada. `revisar`/`recusar` não aceitam versão liberada. Snapshots e pareceres anteriores permanecem nas snapshots/trilha. F-11 foi reescrito para esse caminho, removendo a contestação da versão publicada.

## Testes

No diretório do app, sempre via Python:

- `.venv/Scripts/python.exe -m pytest tests/test_flow.py tests/test_fontes.py -q --basetemp=C:/Windows/Temp/dem011-v7-dirigidos`: **141 passaram**.
- `.venv/Scripts/python.exe -m pytest -q --basetemp=C:/Windows/Temp/dem011-v7-suite-final`: **269 passaram**, com 18 avisos de depreciação existentes. Inclui os 128 testes anteriores ao domínio e 141 de domínio/fontes, com o gate de páginas na suíte. A contagem anterior de 236 não é tratada como simples soma: os testes v5/v6 superados foram reescritos/removidos.
- F-06: versão nova somente pelo Admin, N e snapshots intactos; pedido sem alteração; parecer/recusa da N+1 sem mudar a publicação/disponibilidade.
- F-06b/F-12: ambos os caminhos de abertura (alterar/aceitar) suspendem; liberar/cancelar reabrem; a N é substituída só na nova liberação.
- F-13: dispensa com motivo visível; vínculo entre pedido/resposta; matriz de papéis; pedido duplicado/ciclo paralelo bloqueados; rollback do aceite mantém o pedido pendente.
- F-14: vínculo existente fixa N durante suspensão e depois da substituição; vínculo novo bloqueado na suspensão e fixado em N+1 após liberar; outro coordenador não vincula ao ambiente alheio.
- F-15: cancelamento preserva evidências, impede liberar a descartada, não altera N e permite próximo ciclo.
- F-16: posição concordo/objeto registrada e não bloqueia a liberação; só Revisor pode pedir/posicionar.
- F-02/F-03, demais F/N/C e regressão da canonização/normalização, leitura fresca, assinatura, rodada, payload malformado e trilha permanecem verdes.

`git diff --check` e ASCII nas linhas novas passaram. `flow.py` não importa Reflex. Runtime local Python 3.14.6; Python 3.12 no CI existente.

## As três provas de mutação

Cópias fiéis de código/testes fora do app, sem caches. Cada seletor passou antes da alteração e falhou por comportamento depois, sem erro de coleta. Originais intactos.

| Mutação | Seletor | Baseline | Mutante |
|---|---|---|---|
| Remover checagem ADMIN de alterar | F-06, quatro papéis não Admin | 4 passaram | 4 falharam |
| Remover suspensão para novos | F-12, quatro combinações abrir/fechar | 4 passaram | 4 falharam |
| Fazer revisar alterar ponteiro publicado e disponibilidade | F-06 | 4 passaram | 4 falharam |

Logs/JSON: [`evidencias-mutacao-v7/`](evidencias-mutacao-v7/). Provas históricas preservadas em suas pastas, sem afirmar reexecução dos mutantes antigos neste commit.

## Integração e limites

O cancelamento é lógico (`status=cancelada`, evento `ciclo_cancelado`), evitando apagar versão, snapshots ou eventos. A numeração continua monotônica, inclusive após cancelamento. **A v7 não define restauração da cópia de trabalho ao cancelar**: o serviço descarta o ciclo publicável, sem apagar a cópia de trabalho. A publicação retomada e os vínculos existentes leem N pelos instantâneos. Uma política de restauração/remoção do rascunho precisa considerar mapa de origem e adendos de ambiente; não foi inventada nesta fatia.

A camada de rotas controla commit/rollback; o domínio só faz flush. Aviso aos já vinculados, telas de solicitação/posição e atribuições de Study são das fatias posteriores; esta entrega fixa e bloqueia **VinculoObra** no domínio, sem alterar Study. A exibição deve usar a versão fixada e seus instantâneos, inclusive quando N estiver `substituida`.

Schema da v1 deve incluir `Obra.disponibilidade` e `vinculoobra` com suas FKs/índices, além dos modelos anteriores e rodada. `create_all` não acrescenta colunas a tabelas existentes; banco próprio/baseline permanecem com DEM-005. `CAMINHO_INVENTARIO` deve apontar para CSV acessível no contêiner; ambos os gates relêem. Trigger/ACL contra SQL direto é do deploy da v1.

Sem merge, deploy, telas, revisão Alembic, Compose, segredos, corpus ou alteração do inventário/verificador. Remoção de capítulos/adendos, Study, planejar e multiambiente completo continuam fora. Documentação/evidências no repositório pai `EVANGELICOS/documentacao`, fora do Git do app. EVAL de verificação e aceite posteriores a este delta.

CI da ADR-020/design v7 **verde** em Python 3.12, commit `bab117e67ce8c5ed5ae684f0b9cd7483ab9fc5d0`: https://github.com/egarabini/gsi_ebd/actions/runs/39326405453. PR #4 confirmado aberto, árvore do app limpa. Sem merge, deploy, telas ou Alembic. EVAL de verificação ainda não executado por este DEVS.
