# Referências cruzadas do OpenBible

Dado de terceiros usado para enriquecer os planos de estudo com passagens
relacionadas **verificadas** — nunca texto gerado pelo modelo.

## Procedência

| | |
|---|---|
| Fonte | https://www.openbible.info/labs/cross-references/ |
| Download | https://a.openbible.info/data/cross-references.zip |
| Arquivo | `cross_references.txt` (TSV, ~7,9 MB) |
| Licença | **CC-BY 4.0** — atribuição obrigatória a OpenBible.info |
| Geração | 2026-10-12 (a data vem no cabeçalho do próprio arquivo) |
| Base | *Treasury of Scripture Knowledge* (domínio público) + votos da comunidade |

O cabeçalho do arquivo carrega a atribuição e **deve ser preservado**:

```
From Verse	To Verse	Votes	#www.openbible.info CC-BY 2026-10-12
```

## Por que está versionado

São 7,9 MB — o oposto do corpus bíblico (378 MB), que fica fora do git e é copiado
por `scp` para a VPS. Versionar este aqui elimina um passo manual a cada deploy: o
clone do repositório de conteúdo já traz o dado, e o container do app enxerga tudo
em `/conteudo/ESTUDOS_BIBLICOS/DADOS_EXTERNOS/openbible/` pelo volume `:ro`.

## Formato

Colunas separadas por TAB: `From Verse`, `To Verse`, `Votes`.

- Chave no estilo OSIS: `Gen.1.1`, `Ps.115.15`, `1Cor.13.4`. O mapa canônico dos
  66 livros está em `ESTUDOS_BIBLICOS/GSI_EBD/gsi_ebd/utils/livros.py` (campo `osis`).
- **Os dois lados podem ser intervalo**: `Rom.8.5-Rom.8.8`,
  `Matt.13.11-Matt.13.17`. Quem consumir precisa tratar isso.
- `Votes` é a votação da comunidade — use como corte de qualidade.

## Estado

Ainda **não há código de ingestão**. A avaliação de viabilidade (cobertura sobre os
34 planos, o bug de mapeamento de livros que apareceu no caminho e as decisões de
curadoria) está em
`ESTUDOS_BIBLICOS/GSI_EBD/Diagnostico/referencias-cruzadas.md`.

Decisão de curadoria já tomada: **no máximo 5 passagens relacionadas por capítulo**.
No corte de votos ≥ 10 a média era de 21,7 por citação — exibir isso cru seria pior
que não exibir.

## Como atualizar

O autor publica cortes periódicos. Para atualizar:

```bash
curl -L -o /tmp/cr.zip https://a.openbible.info/data/cross-references.zip
unzip -o /tmp/cr.zip cross_references.txt -d ESTUDOS_BIBLICOS/DADOS_EXTERNOS/openbible/
```

Depois confira a nova data no cabeçalho e registre a mudança no commit.
