# Spec — DEM-202610-011 / fluxo de obras e estudos

> Dono: PLANNER. **Nível 3** (ADR-018): aprovação e dados — processo completo.
> **Depende de:** ADR-011 (a aprovação assinada) — com a **emenda da decisão 9.1(a)** do intent,
> que precisa virar **ADR-019** antes do aceite desta spec (o processo não muda ADR Accepted em
> silêncio). As telas são construídas **na v1** (DEM-005); esta spec governa o **domínio e o fluxo**.

## 1. Referência

Intent: [`intent.md`](intent.md) — **signed** 2026-10-19 · [ADR-011](../../../adr/ADR-011-aprovacao-de-conteudo-assinada.md) · ADR-012 (fontes) · ADR-018 (nível 3) · DEM-005 (a v1)

## 2. O que existe hoje (o ponto de partida real)

| Entidade | Como está | O que falta para o fluxo |
|---|---|---|
| `Obra` (`models/obra.py`) | `titulo`, `tipo`, `descricao`, `doutrina_id`, `origem` — **sem status, sem hash, sem revisão** | os **estados**, a versão e a assinatura |
| `ObraCapitulo` | a divisão da obra | — |
| `Adendo` | `obra_id`, `obra_capitulo_id`, `codigo`, `titulo`, `texto`, `autor_id` | o **`ambiente_id`** (o adendo do coordenador; o da base é `None`) — a base da **D-06** |
| `Study` (`models/study.py`) | `status` (`rascunho|proposto|em_revisao|aprovado|rejeitado|arquivado`), `aprovado_por`, `approved_at`, `feedback_admin` | o enum **novo** do fluxo; o **hash** (a ADR-011 não está implementada — é a D-07) |
| `StudyVersion` | `version`, `content_md`, `questions_json` | o status por versão e o hash |
| `Estudo`/`EstudoCapitulo` | o estudo aplicável (DEM-001) | entra no mesmo fluxo |

**Não existe hoje:** a versão da obra, a assinatura com hash, o parecer estruturado, o estado
`aguardando_admin`, o adendo por ambiente (a D-06). Tudo isso nasce **nesta DEM**, no design.

## 3. Requisitos funcionais

- [ ] **RF01 — os estados e as transições.** A obra e o estudo percorrem: `em_revisao` → (revisor)
  `aguardando_admin` → (admin) `liberada`. Uma alteração depois de `liberada` cria uma **nova
  versão** em `em_revisao` (o "pendente de revisão") sem despublicar a liberada. — *(intent §2)*
- [ ] **RF02 — as permissões por estado.** Só o **Admin** importa, altera e libera; só o **Revisor**
  registra o parecer e avança para `aguardando_admin`; o **Coordenador** vincula/desvincula e
  adenda; o **Instrutor/Aluno** só consomem a versão `liberada`.
- [ ] **RF03 — o parecer do Revisor.** Ao avaliar, o Revisor registra: o parecer (texto), os
  ajustes propostos (lista) e a **assinatura** (revisor_id + data + **hash da versão que ele viu**).
  Sem assinatura, a transição para `aguardando_admin` é **bloqueada no código** (a ADR-011).
- [ ] **RF04 — os ajustes do Admin (a emenda 9.1a).** O Admin lê o parecer, **descreve** e
  **implementa** os ajustes, e libera. O registro guarda a **diferença**: o hash da versão vista
  pelo Revisor × o hash da versão liberada. Os ajustes **dentro do ciclo** **não** reabrem a revisão.
  — *(decisão 9.1a; a regra 5 do intent vale só depois de `liberada`)*
- [ ] **RF05 — as versões.** A versão `liberada` **permanece disponível** aos coordenadores
  enquanto a nova espera revisão; o coordenador **adota** a nova quando quiser (a versão que ele
  usa não muda sozinha). — *(decisão 9.2)*
- [ ] **RF06 — o coordenador e os adendos.** O Coordenador vincula/desvincula a obra ao **seu
  ambiente** e cria/edita os **adendos do ambiente** (a sobreposição): identificados como dele, não
  alteram a obra base nem passam por revisão. — *(decisão 9.3)*
- [ ] **RF07 — o portão de licença em duas etapas.** Só se **importa** obra cuja fonte esteja
  `entra` no inventário (a `nao_entra` **bloqueia na importação**); a fonte `depende` **bloqueia
  na liberação** (importa e revisa, mas não libera até virar `entra`). — *(decisão 9.4)*
- [ ] **RF08 — a trilha.** Cada passo registra **quem, quando e o hash**; o histórico é imutável
  (não se apaga um parecer nem uma liberação).
- [ ] **RF09 — o estudo no mesmo fluxo.** O fluxo vale para **obra e estudo** (o intent §2), com os
  mesmos estados e gates.
- [ ] **RF10 — as telas (na v1).** As telas do Admin (importar/ajustar/liberar), do Revisor
  (parecer) e do Coordenador (vincular/adendar) — construídas na v1 (DEM-005), com a matriz
  papel × rota aplicada.

## 4. Requisitos não funcionais

- **Segurança:** a transição de estado é **servidor-side** e **verificada no código** (não só na
  tela); a autorização segue a matriz papel × rota (DEM-002).
- **Integridade:** o **hash** cobre o conteúdo da obra/versão (o mesmo algoritmo do projeto — o
  design fixa e versiona o algoritmo).
- **Imutabilidade:** os registros de parecer/liberação/versão não são editados — uma correção é
  **nova versão**.
- **Escopo:** **não** implementa o multi-ambiente real (D-06) nem a busca (DEM-D); o adendo por
  ambiente nasce com o ambiente que existe.
- **Testes:** os invariantes de estado e as permissões por papel, com a matriz (DEM-002).

## 5. Contratos (as operações do domínio — o design detalha os modelos)

```python
# domain/flow.py (a implementar no design)
importar(fonte: FonteInventario, obra: Obra) -> Obra          # RF01, RF07 (nao_entra → erro)
revisar(obra: Obra, parecer: str, ajustes: list[str], revisor: User) -> Obra   # RF03
liberar(obra: Obra, ajustes_descritos: str, admin: User) -> Obra               # RF04, RF07 (depende → erro)
alterar(obra: Obra, conteudo: str, admin: User) -> ObraVersao                   # RF05 (nova versão em em_revisao)
vincular(ambiente: Ambiente, obra: Obra, coordenador: User) -> None            # RF06
adendar(ambiente: Ambiente, obra: Obra, texto: str, coordenador: User) -> Adendo  # RF06
```

**Invariante central (o que os testes provam):** nenhuma obra/estudo chega a `liberada` sem a
assinatura do Revisor **para a versão vista** e sem o Admin ter registrado os ajustes; e uma
alteração pós-`liberada` **não** substitui a versão em uso.

## 6. Edge cases

- O Revisor **recusa** a liberação (o parecer reprova) → a obra volta ao Admin com o parecer; o
  Admin ajusta e **reenvia ao Revisor**. *(o estado `aguardando_admin` não existe sem parecer)*
- O Admin libera **sem ter lido** o parecer → permitido tecnicamente, mas o registro fica (e é
  auditável). O fluxo **não** impede o Admin — a barreira é o registro, não a boa vontade.
- A fonte vira `depende` **depois** da importação (o inventário muda) → a liberação é bloqueada (a
  consulta ao inventário é no momento da liberação, não só na importação).
- O coordenador adenda uma obra que **não está vinculada** ao ambiente → bloqueado.
- O `Adendo` do coordenador e o da base no **mesmo** capítulo → coexistem (a sobreposição é a
  regra; o design define a ordem de exibição).
- A versão liberada é adotada **no meio** de uma atribuição em curso → o design decide (recomendo:
  a atribuição mantém a versão; a adoção vale para as **próximas**).

## 7. Critérios de aceitação

- [ ] **CA01:** o fluxo completo por papel (admin importa → revisor opina → admin ajusta e libera → coordenador vincula e adenda) — H-14.
- [ ] **CA02:** a alteração pós-`liberada` cria versão nova e **não** despublica a liberada — H-15.
- [ ] **CA03:** a fonte `nao_entra` **não importa**; a `depende` **importa mas não libera** — H-16.
- [ ] **CA04:** a transição para `aguardando_admin`/`liberada` **falha no código** sem a assinatura/o hash.
- [ ] **CA05:** o parecer e a liberação guardam revisor/admin + data + hash; o histórico é imutável.
- [ ] **CA06:** a matriz papel × rota cobre as telas novas (DEM-002 migrada).
- [ ] **CA07:** a suíte verde; o CI; a spec citada nos testes (o nome do teste cita o RF).

## 8. Rastreabilidade RF → H (as métricas do intent)

| RF | H | Onde se prova |
|---|---|---|
| RF01-RF05 | **H-14** (o fluxo completo) | o teste de jornada do admin/revisor/admin |
| RF05 | **H-15** (a alteração volta à revisão) | o teste da nova versão + a liberada intacta |
| RF07 | **H-16** (o portão) | os testes das duas fontes (`nao_entra`, `depende`) |
| RF03/RF08 | a assinatura/hash | o teste da transição sem assinatura (a prova de mutação) |
| RF06 | a sobreposição | o teste do adendo do coordenador |
