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
| [ADR-012](ADR-012-politica-de-fontes-e-licencas.md) | Política de fontes e licenças do acervo | Accepted |
| [ADR-013](ADR-013-componente-de-mapa-em-javascript.md) | Componente de mapa em JavaScript (exceção à ADR-001) | Accepted |
| [ADR-014](ADR-014-saida-do-reflex.md) | Saída do Reflex: FastAPI + Jinja2 + HTMX (**substitui a ADR-001**) | **Proposed** |
| [ADR-015](ADR-015-acesso-operacional-do-agente.md) | Acesso operacional do agente à VPS (lista fechada; **emenda a ADR-010 em parte**) | **Accepted** (2026-10-19) |
| [ADR-016](ADR-016-delegacao-de-publicacao-ao-deploy.md) | **Delegação da publicação ao perfil DEPLOY** (emenda a ADR-010 e a ADR-015) | **Accepted** (2026-10-19) |

As **001–011** são **retroativas**: registram decisões já tomadas e implementadas, para o
projeto deixar de depender de memória de sessão. As **012–013** nascem da OLPF da frente de
base de conhecimento (2026-10-17). A **014** é a troca de framework pedida pelo ARQUITECT
(2026-10-18) — **Proposed**: quando aceita, a ADR-001 passa a `Superseded by ADR-014`.
A **015** separa **operação** de **deploy**: o agente pode instalar chave pública e
diagnosticar (lista fechada), e continua proibido de publicar — a ADR-010 permanece no que
importa.
