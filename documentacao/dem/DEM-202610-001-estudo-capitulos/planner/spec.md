# Spec — DEM-202610-001 / Estudo com capítulos próprios e mapa de origem

> Dono: PLANNER. Cada capacidade cita um **outcome** (intent §2), um **non-goal**
> (§4 Out) ou uma **constraint** (§5). Capacidade órfã = a spec inflou.

## 1. Referência

PRD: [`prd.md`](prd.md) · Intent: [`intent.md`](intent.md) — **signed** em 2026-10-16
(`open_questions_open: 0`)

## 2. Requisitos funcionais

- [ ] **RF01:** O sistema mantém um **Estudo**, ligado a uma Obra, com título, descrição,
      doutrina (opcional) e status. — *(intent §2)*
- [ ] **RF02:** O Estudo possui **capítulos próprios**, com ordem única e contínua dentro
      do estudo, título e conteúdo. — *(intent §2)*
- [ ] **RF03:** Cada capítulo do estudo pode declarar **uma ou mais origens** (capítulo da
      obra + adendo opcional). A origem é **opcional**. — *(intent §2 · §8.5)*
- [ ] **RF04:** Um capítulo da obra pode originar **vários** capítulos do estudo, e vários
      capítulos da obra podem alimentar um só. — *(intent §2)*
- [ ] **RF05:** Carga inicial **idempotente**: cria 1 estudo "Doutrinas Cristãs — Estudo
      Dirigido" com os **34 capítulos** já importados e a origem 1:1 nos 34 capítulos da
      obra. — *(intent §4 In · §8.2)*
- [ ] **RF06:** Todo capítulo criado nasce em **rascunho**; nenhum nasce disponível. —
      *(intent §5 · ADR-011)*
- [ ] **RF07:** Tela do admin: lista o estudo, seus capítulos e, por capítulo, a origem
      (obra + capítulo + adendos associados). **Somente leitura**. — *(intent §4 In · §8.1 · §8.4)*
- [ ] **RF08:** A lição do aluno e o fluxo atual **não mudam**: continuam servidos por
      `Study` / `StudyVersion`. — *(intent §5)*
- [ ] **RF09:** A carga **não altera nem remove** os `Study` / `StudyVersion` existentes. —
      *(intent §5 · H-04)*
- [ ] **RF10:** Capítulo do estudo **sem origem** é válido e a tela mostra "sem origem
      declarada". — *(intent §2 · §8.5)*

## 3. Requisitos não funcionais

- **Idempotência:** RF05 executado duas vezes → 0 novos, 0 duplicados.
- **Performance:** a tela lista 34 capítulos e origens em **< 1 s** no ambiente local.
- **Segurança:** **alvo** — tela e importador exigem papel **ADMIN**.
  **Pendência conhecida (descoberta pelo EVAL em 2026-10-16, vira DEM-202610-002):**
  hoje `/admin` usa `AuthState.check_auth` → `require_login` (só login, sem papel) e os
  **loaders** de estado não têm guarda `is_admin` — a checagem existe apenas nas ações
  que gravam (`states/admin.py` linhas ~193/289/320/355). É rota **pré-existente**, fora
  do diff desta DEM, portanto não é regressão; mas este RNF é **alvo, não estado atual**.
- **Observabilidade:** o importador reporta contagens (estudo, capítulos novos/atualizados,
  origens criadas).
- **Compatibilidade:** nenhum contrato existente muda; `Study`, `StudyVersion` e
  `StudyAssignment` ficam intactos.
- **Conteúdo:** o modelo novo **não toca** o caminho da Escritura (ADR-003) e não gera texto
  bíblico.

## 4. Contratos (interface)

Importador (CLI, mesmo padrão dos demais):

```
python -m gsi_ebd.scripts.importar_estudo_aplicado [--apply] [--autoteste]
    sem --apply  → apenas confere e reporta (nada gravado)
    --autoteste  → roda em SQLite descartável
```

Tela: rota `/admin`, aba **Estudos**.

## 5. Modelo de dados (lógico)

- **Estudo** — obra de origem, título, descrição, doutrina (opcional), status.
- **EstudoCapitulo** — estudo, ordem, título, conteúdo, questões, status (rascunho).
- **EstudoCapituloOrigem** — capítulo do estudo, capítulo da obra, adendo (opcional).

Relações: `Estudo 1:N EstudoCapitulo`; `EstudoCapitulo N:N ObraCapitulo` via origem.
Tipos, índices e nomes físicos ficam no `design.md`.

## 6. Edge cases

- Capítulo **sem origem** → exibe "sem origem declarada", sem erro (RF10).
- Capítulo da obra com **3 adendos** → exibe os três.
- Carga rodada **duas vezes** → 0 novos (RNF idempotência).
- Estudo **sem capítulos** → tela mostra estado vazio explicitamente.
- **Ordem duplicada** no mesmo estudo → rejeitada na gravação.
- Capítulo de **43 mil caracteres** → a lista mostra título e contagem; o conteúdo nunca é
  truncado em silêncio.
- Estudo apontando para **obra inexistente** → rejeitado.

## 7. Critérios de aceitação

- [ ] **CA01:** 1 estudo com 34 capítulos, cada um com origem no capítulo correspondente da obra.
- [ ] **CA02:** A tela exibe estudo, capítulos e origens em modo leitura.
- [ ] **CA03:** Rodar a carga duas vezes não duplica (contagens idênticas).
- [ ] **CA04:** Os 34 `Study` e seus `StudyVersion` mantêm contagem e conteúdo.
- [ ] **CA05:** A lição do Cap. 21 continua exibindo Escritura ("João 3:16") e 5 passagens relacionadas.
- [ ] **CA06:** Todo capítulo criado nasce em rascunho.
