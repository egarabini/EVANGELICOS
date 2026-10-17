# CONVENTIONS.md

> Padrões de código, testes, documentação, segurança e processo. Consulte antes de escrever qualquer código. Preencha os `[preencher: …]` com o perfil do projeto.

## Idioma

- Documentação, comentários e identificadores em **[preencher: ex.: pt-BR]**.
- Logs internos podem seguir o padrão do framework.

## Código

- **Stack:** [preencher: linguagem/runtime/framework — ver perfil.]
- **Arquitetura de camadas:** [preencher: ex.: endpoints finos; lógica em services; acesso a dados isolado.]
- **Assíncrono / cancelamento:** [preencher: convenção de I/O.]
- **Migrations / mudanças de dados:** geradas e revisadas em passo dedicado, nunca como efeito colateral.

## UI (se houver)

- **Biblioteca de UI padrão:** [preencher.] **Não misturar** bibliotecas visuais.
- Tema/estilos centralizados; nada de cores/spacing hard-coded em componentes.
- Estado de UI explícito (loading/erro/vazio); responsividade.
- Sem regra de negócio no componente — delegar a services.

## Documentação (Markdown)

- `UTF-8` sem BOM; um `# H1` por arquivo; listas com `-`; code fences com linguagem.
- Templates de DEM: copiar de `documentacao/metodo/templates/`, **nunca apagar seções** (se não se aplica, "N/A" + motivo).

## Commits (Conventional Commits + rastreio)

- Formato: `tipo(escopo): descrição curta`.
- Tipos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`, `build`, `ci`.
- Trailers de rastreio: [preencher: o(s) trailer(s) do seu rastreador] + o id da DEM.
- O **hash do commit** é registrado no `changelog.md` da DEM.

## Branches (GitFlow)

- `feature/DEM-...` a partir de `develop`.
- `[preencher: main|master]` = produção (tags SemVer); `develop` = integração; `release/x.y.z`; `hotfix/x.y.z`.
- Detalhe e regras duras em `documentacao/metodo/04-estrutura-dem/gitflow.md`.

## Testes

- **Rastreabilidade requisito ↔ teste obrigatória:** o nome do teste referencia o requisito (ex.: `Test_RF03_...`).
- Todo requisito implementado tem teste correspondente (critério de conclusão da DEM).
- Caminho novo: ao menos um teste de caminho feliz, um de erro/edge.

## Segurança

- **Segredos via [preencher: user-secrets / cofre / variáveis]**, **nunca** no repositório.
- [preencher: formato de segredos em repouso, se houver.]
- Dado sensível nunca em log, exceção, cookie, URL ou UI.
- [preencher: restrição de IA — ex.: sem dado sensível para LLM em cloud.]
- Validação/autorização por filtro/middleware dedicado, não inline.

## Definition of Ready / Done (por fase)

| Entrar em… | Precisa ter… |
|---|---|
| Intent | problema em linguagem crua do ARQUITECT |
| Spec | `intent.md` `signed`; `prd.md` sem ambiguidade pendente |
| Design | `spec.md` aprovada, requisitos verificáveis, contratos se houver |
| Implementação | documentos anteriores aprovados; ADRs relevantes citadas |
| Fechamento | testes verdes cobrindo os requisitos; hash do commit; checklist de regressão arquitetural OK |

**Done de fase** = documento completo (sem `[placeholder]`) + ARQUITECT aprovou + conflitos com ADRs sinalizados + itens em aberto registrados.
