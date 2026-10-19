# Spec — DEM-202610-011 / fluxo de obras e estudos (**v2** — revisão de 19/10)

> Dono: PLANNER. **Nível 3** (ADR-018).
> **Aprovada pelo ARQUITECT em 2026-10-19** (com a ADR-019 aceita). **Revisão v2** (19/10): acrescenta o estado `devolvida` (recusa do Revisor), o aviso de
> **origem alterada** no estudo derivado, a **transparência do intervalo** (a salvaguarda do
> trade-off da ADR-019), a pergunta do **"como" do coordenador** e o **fatiamento** (o domínio
> pode ser feito antes das telas). As 4 decisões 9.1-9.4 **são as do ARQUITECT** (mensagem de
> 19/10, registradas no intent §9) — a ADR-019 as consolida.

## 1. Referência

Intent: [`intent.md`](intent.md) — **signed** · [ADR-011](../../../adr/ADR-011-aprovacao-de-conteudo-assinada.md) (emendada pela **[ADR-019](../../../adr/ADR-019-fluxo-de-obras-e-estudos.md)**) · ADR-012 · ADR-018 · DEM-005 · DEM-010 (o ambiente)

## 2. O que existe hoje

| Entidade | Como está | O que falta |
|---|---|---|
| `Obra` | `titulo`, `tipo`, `descricao`, `doutrina_id`, `origem` — **sem status, hash ou versão** | os estados, a versão, a assinatura |
| `Adendo` | `obra_id`, `obra_capitulo_id`, `codigo`, `titulo`, `texto`, `autor_id` | o **`ambiente_id`** (o adendo do coordenador) |
| `Study` | enum antigo (`aprovado`), `aprovado_por`, `approved_at`, **sem hash** | o enum novo, o hash (a ADR-011 nunca foi implementada — D-07) |
| `StudyVersion` | `version`, `content_md`, `questions_json` | o status por versão e o hash |
| `EstudoCapitulo`/`EstudoCapituloOrigem` | o estudo aplicável e o mapa de origem (DEM-001) | a ligação com a versão da obra |

## 3. Requisitos funcionais

- [ ] **RF01 — os estados** (obra e estudo): `em_revisao` → (Revisor aprova) `aguardando_admin` → (Admin libera) `liberada`. **(novo)** O Revisor pode **recusar** → `devolvida` (o Admin ajusta e devolve → volta a `em_revisao`). Alteração depois de `liberada` → nova versão em `em_revisao` (a "pendente de revisão").
- [ ] **RF02 — as permissões por estado**: só o **Admin** importa/altera/libera; só o **Revisor** assina o parecer e move para `aguardando_admin`/`devolvida`; o **Coordenador** vincula/desvincula, adenda e **planeja**; o **Instrutor/Aluno** consomem a versão `liberada`.
- [ ] **RF03 — o parecer assinado**: o Revisor registra o parecer + os ajustes propostos + **revisor_id + data + hash da versão vista**. Sem assinatura, a transição é **bloqueada no código** (a ADR-011).
- [ ] **RF04 — os ajustes do Admin (9.1a)**: o Admin descreve e implementa os ajustes; libera; o registro guarda **os dois hashes** (visto × liberado). Os ajustes no ciclo **não** reabrem a revisão.
- [ ] **RF05 — as versões (9.2)**: a `liberada` **permanece disponível** enquanto a nova espera revisão; o coordenador **adota** a nova quando quiser.
- [ ] **RF06 — o coordenador (9.3 + o "como")**: vincula/desvincula ao **seu ambiente** e cria/edita os **adendos do ambiente** (sobreposição, sem revisão). **(a confirmar)** O **"como"**: o coordenador define **quais capítulos usa, em que ordem e com qual calendário** (o plano de trabalho do ambiente) — ver a pergunta 9.5.
- [ ] **RF07 — o portão de licença (9.4), em duas etapas**: `nao_entra` **bloqueia a importação**; `depende` **bloqueia a liberação** (importa e revisa, mas não libera até virar `entra`).
- [ ] **RF08 — a trilha**: cada passo registra quem, quando e o hash; imutável.
- [ ] **RF09 — o estudo no mesmo fluxo** (obra e estudo).
- [ ] **RF10 — as telas (na v1)**: admin, revisor e coordenador, com a matriz papel × rota.
- [ ] **RF11 — a transparência do intervalo (a salvaguarda da ADR-019)**: (a) no **momento da liberação**, o Admin vê o **tamanho do que mudou** em relação à versão vista pelo Revisor; (b) **depois** da liberação, o Revisor vê a **diferença final** (só leitura) e tem o botão **"contestar"**, que **reabre a revisão** (a obra volta a `em_revisao`).
- [ ] **RF12 — o estudo derivado**: se a obra ganha versão nova, o estudo que nasceu dela e o mapa de origem recebem o aviso **"origem alterada"** (não bloqueia; quem consome decide).

## 4. Requisitos não funcionais

- **Segurança:** a transição é **servidor-side**, verificada no código; a autorização pela matriz (DEM-002).
- **Integridade:** o hash cobre o conteúdo da versão (o algoritmo é fixado e **versionado** no design).
- **Imutabilidade:** parecer/liberação/versão não são editados — correção é nova versão.
- **Escopo:** **não** implementa o multi-ambiente real (D-06) nem a busca (DEM-D); o adendo/plano por ambiente nasce com o ambiente que existe.
- **Testes:** os invariantes + as permissões por papel; nomes citam o RF; a prova de mutação nos gates.

## 5. Contratos (o design detalha os modelos)

```python
importar(fonte, obra) -> Obra                          # RF01, RF07 (nao_entra → erro)
revisar(obra, parecer, ajustes, revisor) -> Obra       # RF03
recusar(obra, parecer, revisor) -> Obra                # RF01 (devolvida)
liberar(obra, ajustes_descritos, admin) -> Obra        # RF04, RF07 (depende → erro)
alterar(obra, conteudo, admin) -> ObraVersao           # RF05
vincular(ambiente, obra, coordenador) -> None          # RF06
adendar(ambiente, obra, texto, coordenador) -> Adendo  # RF06
planejar(ambiente, obra, capitulos, ordem, calendario) -> Plano   # RF06 (a confirmar — 9.5)
contestar(obra, revisor) -> Obra                       # RF11 (reabre a revisão)
```

**Invariante central:** nenhuma obra/estudo chega a `liberada` sem a assinatura do Revisor **para a versão vista** e sem o Admin ter registrado os ajustes; a alteração pós-`liberada` **não** substitui a versão em uso; e a recusa do Revisor **não** deixa a obra em `aguardando_admin`.

## 6. Edge cases

- O Revisor recusa → `devolvida`; o Admin ajusta e **reenvia** (o estado não é `aguardando_admin`) (RF01).
- O Admin libera sem ter lido o parecer → permitido (o registro fica); a salvaguarda é a RF11.
- A fonte vira `depende` **depois** da importação → a liberação é bloqueada (a consulta é no momento da liberação).
- O coordenador adenda/planeja obra **não vinculada** ao ambiente → bloqueado.
- O adendo do coordenador e o da base no **mesmo** capítulo → coexistem (a sobreposição é a regra).
- A versão liberada é adotada no meio de uma atribuição em curso → a atribuição **mantém** a versão; a adoção vale para as próximas.
- A obra ganha versão nova com estudo derivado → o estudo recebe o aviso **"origem alterada"** (RF12).

## 7. Critérios de aceitação

- [ ] **CA01:** o fluxo completo por papel (importar → opinar → ajustar → liberar → vincular/adendar/planejar) — H-14.
- [ ] **CA02:** a alteração pós-`liberada` cria versão nova e **não** despublica a liberada — H-15.
- [ ] **CA03:** `nao_entra` não importa; `depende` importa mas não libera — H-16.
- [ ] **CA04:** a transição a `aguardando_admin`/`liberada` falha no código sem a assinatura/o hash.
- [ ] **CA05:** a **recusa** leva a `devolvida`; o reenvio volta a `em_revisao` (RF01).
- [ ] **CA06:** a **liberação mostra o tamanho** e o Revisor vê a diferença + o **contestar** reabre (RF11).
- [ ] **CA07:** o estudo derivado recebe o aviso de origem alterada (RF12).
- [ ] **CA08:** a matriz papel × rota cobre as telas novas; a suíte verde; o CI.

## 8. Rastreabilidade RF → H

| RF | H | Prova |
|---|---|---|
| RF01-RF05 | **H-14** | o teste de jornada dos três papéis |
| RF05 | **H-15** | a nova versão + a liberada intacta |
| RF07 | **H-16** | os dois gates de licença |
| RF03/RF08 | a assinatura/hash | o teste da transição sem assinatura (a mutação) |
| RF06 | o adendo/plano | o teste do coordenador |
| RF11/RF12 | (novos) | o teste da diferença + o contestar + o aviso |

## 9. O fatiamento (por que ele pode começar agora)

**A parte de domínio não depende de tela.** O `flow.py`, os modelos (`ObraVersao`, a assinatura,
o `Adendo.ambiente_id`), os hashes e os testes de invariante podem ser implementados **em paralelo**
à base nova da v1 (DEM-005) — e é uma boa **segunda tarefa para o Codex** depois da DEM-012.

| Fatia | O quê | Depende de |
|---|---|---|
| **1 — domínio (agora)** | os modelos, o `flow.py`, os hashes, os gates, os testes | nada da v1 |
| **2 — as telas** | as telas do fluxo (na v1) | a DEM-005 |

## 10. O "como" do coordenador (decidido em 2026-10-19 — a 9.5)

O coordenador define **quais capítulos usa, em que ordem e com qual calendário** — mas em
**fatia posterior** (nível 2), com o padrão **"obra inteira, na ordem da obra, sem calendário"**.
O plano **nunca** altera a obra base. O `planejar(ambiente, obra, capítulos, ordem, calendário)`
fica fora desta fatia; a RF06 desta fatia cobre **vincular/desvincular e o adendo do ambiente**.
