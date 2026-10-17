# PRD — DEM-202610-001 / Estudo com capítulos próprios e mapa de origem

> Dono: PLANNER. Escrito **após** o `intent.md` estar `signed`.

## 1. Referência

Intent: [`intent.md`](intent.md) — status **signed** em 2026-10-16

## 2. Problema

Hoje o material aplicável e a fonte se confundem: cada capítulo do livro é um `Study`
isolado, **sem vínculo com a obra** importada na Fase 1. Não existe a unidade "estudo" —
e é ela que o coordenador escolhe, que o revisor avalia capítulo a capítulo e que o aluno
percorre em progressão. A origem do texto também se perde: ninguém sabe de qual capítulo
da obra saiu este capítulo do estudo.

## 3. Objetivo

O material aplicável passa a existir como **um estudo** com **capítulos próprios**, cada
capítulo declarando sua origem na obra — opcionalmente — e o admin enxergando essa árvore
numa tela. **O aluno não percebe diferença**: a lição continua exatamente como hoje.

## 4. Componentes / atores afetados

- **Admin** (dono do catálogo): importa e enxerga o estudo.
- **Revisor** (futuro): vai avaliar capítulo a capítulo — fora desta DEM, mas é o motivo de
  o capítulo ser uma entidade própria.
- **Coordenador** (futuro): vai escolher o estudo na biblioteca dele (Ação 2).
- **Aluno**: consome a lição — deve seguir idêntico.
- **Sistema**: 3 entidades novas, um importador e uma aba no admin.

## 5. Critérios de sucesso (mensuráveis)

- [ ] **1 estudo com 34 capítulos**, cada um com a origem apontando para o capítulo
      correspondente da obra.
- [ ] A tela do admin mostra estudo, capítulos e origem **em modo leitura**, sem erro.
- [ ] A carga é **idempotente**: a segunda execução não cria nem duplica nada.
- [ ] Os **34 `Study` originais permanecem intactos** (mesma contagem e mesmo conteúdo).
- [ ] A lição do Cap. 21 continua exibindo Escritura e passagens relacionadas.

## 6. Escopo

### Incluído nesta versão

- O estudo como artefato, com capítulos próprios e ordem definida
- O mapa de origem N:N entre capítulo do estudo e capítulo da obra (adendo como referência)
- A carga inicial dos 34 capítulos a partir do que já está importado
- A tela do admin **somente leitura**

### Fora do escopo (intent §4 Out)

- Ação 1: agendamento de leitura, ressalvas e fluxo de aprovação
- Ações 2 e 3: bibliotecas do coordenador e do instrutor, níveis, treinamento
- Ação 4: liberação e classificação de alunos
- **Migração da lição** para o capítulo do estudo (DEM própria, com janela)
- Autoria/edição de capítulo pela interface
- Mover os `Diagnostico/*.md`

## 7. Restrições

- **Arquitetural (ADRs):** 002 (corpus intocado), 003 (Escritura), 005 (modelo Obra→Estudo),
  010 (publicação pelo CI), 011 (aprovação assinada).
- **Operacional:** entrega por PR; o agente não publica.
- **Segurança:** tela e importador restritos a ADMIN.
- **Dados:** nenhum dado existente é alterado ou removido pela carga.
- **Prazo:** sem prazo — entrega por gate, não por data.

## 8. Dependências

- **ADR:** 005 (base do modelo) e 011 (por que o capítulo nasce em rascunho).
- **DEM(s) pai:** Fase 1 — a Obra já está importada (1 obra, 34 capítulos, 6 doutrinas).
- **Contrato interno:** o conteúdo já existente em `Study` + `StudyVersion` é a fonte da carga.
