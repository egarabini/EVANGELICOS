# Decisões de Arquitetura (ADRs)

Uma ADR registra uma **decisão estrutural** — lei do projeto até ser substituída.
Nenhuma DEM pode contrariar uma ADR `Accepted`: se precisar, o ARQUITECT cria a
ADR que a substitui **antes** da DEM começar.

| ADR | Assunto | Status |
|---|---|---|
| [ADR-001](ADR-001-stack-fixa.md) | Stack fixa: Python/Reflex | Accepted |
| [ADR-002](ADR-002-corpus-local-nao-redistribuido.md) | Corpus bíblico local, não redistribuído | Accepted |
| [ADR-003](ADR-003-escritura-por-igualdade.md) | Escritura por igualdade, não similaridade | Accepted |
| [ADR-004](ADR-004-referencias-cruzadas-curadoria.md) | Referências cruzadas e sua curadoria | Accepted |
| [ADR-005](ADR-005-modelo-obra-adendos-estudo.md) | Modelo Obra + Adendos → Estudo | Accepted |
| [ADR-006](ADR-006-guard-rails-tlc-arquivos-de-guarda.md) | Guard-rails de agente + TLC + guardas | Accepted |
| [ADR-007](ADR-007-estrutura-dem-gate-intent.md) | Estrutura de DEM + gate INTENT | Accepted |
| [ADR-008](ADR-008-segredos-e-senhas-demo.md) | Segredos e senhas de demonstração | Accepted |
| [ADR-009](ADR-009-gitflow.md) | GitFlow e revisão por Copilot Enterprise | Accepted |
| [ADR-010](ADR-010-publicacao-por-ci.md) | Publicação por CI/CD, nunca por agente | Accepted |
| [ADR-011](ADR-011-aprovacao-de-conteudo-assinada.md) | Aprovação de conteúdo assinada e amarrada ao hash | Accepted |

Todas as 001–011 são **retroativas**: registram decisões já tomadas e
implementadas, para o projeto deixar de depender de memória de sessão.
