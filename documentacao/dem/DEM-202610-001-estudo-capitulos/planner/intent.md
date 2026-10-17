# Intent: DEM-202610-001 / estudo-capitulos

status: signed
owner: PLANNER
signed_by: ARQUITECT
origin: ADR-005 + especificação do ARQUITECT (fluxo de bibliotecas, Ações 1–4)
signed_at: 2026-10-16
supersedes: —
open_questions_open: 0
spec_citations: 100% — todo RF de `spec.md` cita §2, §4 In, §5 ou uma decisão do §8
nota_de_assinatura: o ARQUITECT autorizou as recomendações do PLANNER ("segue a sua leitura", 2026-10-16) e delegou o fechamento das questões; as decisões estão registradas no §8.

## 1. Problema

Hoje o material que o aluno estuda e a fonte de onde ele nasceu são a mesma coisa: cada
capítulo do livro é um `Study` isolado, sem vínculo com a obra. Consequência prática: não
existe a unidade "estudo" — a mesma que o coordenador escolhe, que o revisor avalia capítulo
por capítulo e que o aluno percorre em progressão. E a origem se perde: ninguém consegue
dizer de qual capítulo da obra saiu este capítulo do estudo.

Evidência: 34 `Study` criados na proporção 1:1 com os capítulos do livro; a obra importada
na Fase 1 não tem vínculo com eles; e o plano das bibliotecas precisou de duas versões
porque o modelo estava errado — a v1 agrupava os estudos existentes, a especificação exige
**separar a fonte da aplicação**.

Quem sente: o admin/revisor (não tem onde registrar ressalva por capítulo), o coordenador
(não vê o estudo como curso) e a plataforma (não consegue liberar capítulo a capítulo).

## 2. Outcome

O material aplicável passa a existir como **um estudo com capítulos próprios**, e cada
capítulo do estudo declara sua **origem** na obra — inclusive no caso em que um capítulo da
obra alimenta vários do estudo. O admin enxerga a árvore inteira (estudo, capítulos,
origens) numa tela; o aluno continua fazendo a lição **sem diferença perceptível**.

## 3. Afetados

Admin e revisor (avaliam), coordenador e instrutor (recebem nas Ações 2–3), aluno (consome),
e o código: lição, fila de revisão e progresso.

**Intocáveis:** a lição em produção, o caminho da Escritura (ADR-003) e o corpus (ADR-002).

## 4. Escopo

**In**
- o estudo como artefato, com capítulos próprios e ordem definida
- o mapa de origem entre capítulo do estudo e capítulo da obra (N:N)
- a carga inicial: os 34 capítulos atuais passam a existir como capítulos de um estudo
- a tela do admin para ver estudo, capítulos e origem

**Out (non-goals)**
- agendamento de leitura, ressalvas e o fluxo de avaliação da Ação 1 — **DEM própria**
- bibliotecas do coordenador e do instrutor, níveis e treinamento (Ações 2 e 3)
- liberação e classificação de alunos (Ação 4)
- repontar a lição do aluno para o capítulo do estudo — **DEM própria, com janela**
- autoria de capítulo pela interface
- mover os `Diagnostico/*.md` (há comentários de código apontando para eles)

## 5. Constraints (duras)

- A lição em produção **não pode regredir**: o caminho atual continua servindo o aluno.
- Conteúdo criado nasce **em rascunho**; virar disponível exige aprovação **assinada e
  amarrada ao conteúdo** (ADR-011).
- O corpus e o caminho da Escritura não são tocados.
- O agente não publica: entrega por PR, publicação pelo CI (ADR-010).
- Nada que contrarie ADR-001, 002, 003, 005.

## 6. Health metrics

- **H-01** · suíte de testes verde · baseline **76 testes passando** (`pytest tests`) · porteiro **EVAL**
- **H-02** · a lição do Cap. 21 continua com Escritura e passagens relacionadas · baseline **HTTP 200 + bloco com "João 3:16" e 5 passagens** (verificado em produção) · porteiro **EVAL**
- **H-03** · o conteúdo atual não perde nada · baseline **Cap. 21 com 4 citações e 10 questões** · porteiro **EVAL**
- **H-04** · nada é apagado na carga inicial · baseline **39 estudos · 31.102 versículos · 344.799 referências cruzadas** · porteiro **EVAL**

## 7. Sinal de sucesso

O ARQUITECT abre a tela do estudo, vê os capítulos do estudo e a origem de cada um, e
confirma que a lição do aluno está idêntica. **Isso é o aceite.** A suíte é a evidência, não
o aceite.

## 8. Perguntas abertas — fechadas pelo ARQUITECT em 2026-10-16

**Nenhuma aberta.** As decisões abaixo são do ARQUITECT (autorizadas por "segue a sua
leitura") e regem a `spec.md`.

| # | Pergunta | Decisão |
|---|---|---|
| 8.1 | A tela é só de leitura? | **Sim, somente leitura.** Criar/editar capítulo pela interface é DEM própria. |
| 8.2 | A carga inclui os 5 estudos de exemplo? | **Não, só os 34 capítulos do Grudem.** Os exemplos não têm origem na obra. |
| 8.3 | O mapa precisa registrar o trecho? | **Não. Basta o vínculo capítulo↔capítulo.** Trecho é refinamento que ninguém pediu. |
| 8.4 | O adendo entra nesta DEM? | **Só como referência exibida** na origem. O uso no fluxo de avaliação é da Ação 1. |
| 8.5 | Capítulo sem origem é válido? | **Sim.** É o que permite material original; a tela informa "sem origem declarada". |

## 9. Fora de julgamento

Stack, schema/tabelas, nomes de campos, telas detalhadas e decomposição em tarefas. Também
não decide aqui **quando** a migração da lição acontece — só que ela **não é desta DEM**.
