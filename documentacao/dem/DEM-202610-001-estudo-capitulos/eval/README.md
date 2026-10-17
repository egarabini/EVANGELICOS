# eval/ — evidência do EVAL

Pasta de dono único: **o EVAL**. O PLANNER lê, não edita.

| Arquivo | O que é | Dono |
|---|---|---|
| `jornada.md` | jornada, evidência colada e **veredito** (PASS/FAIL/BLOCKED por caso) | EVAL |
| `_eval_seed.py` | probe: monta a fixture própria do EVAL (obra + 34 capítulos + 5 exemplos) | EVAL |
| `_eval_after.py` | probe: exercita o CLI real e confere contagens/estado depois da carga | EVAL |
| `_eval_nn.py` | probe: insere casos de N:N e de capítulo sem origem, e lê pela tela | EVAL |
| `_eval_hash.py` | probe: sha256 das tabelas antes×depois (prova de que nada existente muda) | EVAL |

Os probes rodam contra **SQLite descartável em `%TEMP%`** — nunca contra produção. São
**evidência reproduzível**, não código de produção: o prefixo `_` é do EVAL e foi
mantido de propósito.

> Foram versionados junto com o parecer do PLANNER (commit `c936375`) porque o commit
> os varreu; a decisão foi **mantê-los** para que a verificação do EVAL possa ser
> reproduzida por qualquer pessoa, em vez de virar relato.
