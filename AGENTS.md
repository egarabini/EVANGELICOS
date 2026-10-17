# AGENTS.md — guarda do projeto Didasko

> Este repositório é o **guarda-chuva** do projeto. Ele contém o **conteúdo** dos
> estudos; o **código** da aplicação vive em `ESTUDOS_BIBLICOS/GSI_EBD/`.
> Guardas mais específicos vencem: `ESTUDOS_BIBLICOS/GSI_EBD/AGENTS.md` (código) e
> `ESTUDOS_BIBLICOS/DOUTRINAS_CRISTAS/AGENTS.md` (autoria de conteúdo).

## Antes de escrever qualquer coisa

1. `documentacao/perfil-do-projeto.md` — stack, ambientes, restrições.
2. `documentacao/adr/README.md` — as 11 decisões **Accepted**. Nenhuma tarefa pode
   contrariar uma delas; se precisar, uma ADR nova é escrita **antes**.
3. O guarda específico do caminho em que você vai trabalhar.
4. A DEM em `documentacao/dem/`, se existir — leia `planner/intent.md` primeiro.

## Regras absolutas

- **IA não executa deploy em produção** (ADR-010). Publicação é do GitHub Actions.
- **Segredos nunca no repositório** (ADR-008). Token nunca em chat.
- O **corpus bíblico é `:ro` e não versionado** (ADR-002).
- **Escritura sempre do corpus**, nunca do modelo (ADR-003).
- Não contrariar ADR `Accepted` em silêncio.
- **Documentação em pt-BR com acentuação**; **código e comentários sem acento**
  (padrão histórico do repositório).
- Cerca de objetivo: se o *porquê* mudou, **para e reabre o intent** — não patcha a spec.

## Fluxo (TLC)

`Think` (assunções e ambiguidades) → `List` (arquivos + riscos + ordem, **aguarde
aprovação**) → `Code`. Dúvida antes de executar? Registre e devolva ao PLANNER.

Detalhe do método: `documentacao/metodo/README.md`.
