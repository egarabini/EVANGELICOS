# Parecer EVAL — DEM-202610-012

**Resultado: PASS** para `427e8bbffee73b3f1146b3daa25a91736136dbe7`, branch `feature/DEM-202610-012-credencial-de-seed`, em 2026-10-19.

Avaliação cega: leitura dos guardas, perfil, índice de ADRs, intent, spec e plano de testes; inspeção do diff contra `develop`, código pertinente e testes. Não foram consultados briefing, jornada ou história do implementador. Nenhum código foi alterado; nenhum commit ou deploy foi executado.

## Evidências

Executado do diretório `ESTUDOS_BIBLICOS/GSI_EBD`:

```text
.venv/Scripts/python.exe -m pytest tests -q --basetemp=.pytest_cache/dem012-eval
128 passed, 18 warnings in 27.22s
```

A suíte inclui as páginas e os 15 casos novos do seed. Os avisos são de depreciação de `datetime.utcnow()` em código existente; não houve falhas.

| Requisito | Verificação | Resultado |
|---|---|---|
| RF01 | Seed completo em SQLite temporário; bcrypt confere a senha aleatória recebida pelo ambiente em todas as cinco contas | PASS |
| RF02 | Variável ausente e vazia, com banco vazio e populado; nenhuma sessão/conexão permitida antes do aborto | PASS |
| RF03 | Cinco contas com troca obrigatória; login parametrizado pelos cinco papéis redireciona para `/perfil/alterar-senha`, incluindo admin | PASS |
| RF04 | Varredura dos caminhos previstos sem a senha histórica; teste do repositório lista e restringe as exceções | PASS |
| RF05 | Reexecução com outra senha preserva IDs, hashes, nomes e flags das contas existentes | PASS |
| RF06 | `.env.example` contém exatamente `SEED_PASSWORD=` sem valor | PASS |
| RF07 | Removida a linha final com login/e-mail/senha de `subir.sh`; teste verifica sua ausência | PASS |

O teste de execução também verifica que a senha aleatória não aparece na saída. A revisão do seed confirma a remoção das impressões de senha. Verificação adicional pelo entrypoint real, com `SEED_PASSWORD` removida do ambiente: mensagem `Defina SEED_PASSWORD no ambiente para rodar o seed.` e exit code **1**.

O diff altera somente `.env.example`, `README.md`, `deploy/DEPLOY.md`, `deploy/subir.sh`, `gsi_ebd/data/seed.py` e `tests/test_seed.py`. Nenhuma dependência, schema ou Compose foi alterado. O fluxo de login já encaminhava a flag sem exceção de admin; o novo teste demonstra esse comportamento sem exigir mudança adjacente.

## Achados e limites

Não foram encontrados defeitos bloqueadores no escopo autorizado. A integração operacional permanece pendente conforme decisão explícita do ARQUITECT: o Compose não repassa `SEED_PASSWORD`; somente incluí-la no `.env` da VPS não habilita o seed no contêiner. Essa necessidade está registrada em `deploy/DEPLOY.md`; o PASS não aprova seed de banco novo por esse pipeline antes do repasse autorizado.

A rotação das contas existentes continua manual, sob responsabilidade do ARQUITECT. A execução local não comprova CI remoto verde nem valida produção. Os testes de banco usam SQLite temporário. O teste de varredura geral percorre os arquivos de texto selecionados no repositório Git da aplicação; não constitui auditoria de todos os formatos binários ou do repositório guarda-chuva.
