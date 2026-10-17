# ADR-005: Modelo Obra + Adendos → Estudo

- **Status:** Accepted
- **Data:** 2026-10-16
- **Decisores:** ARQUITECT (Eduardo)
- **Gatilho:** Novo Horizonte (adoção de método) / decisão já implementada

---

## Contexto e Problema

Hoje **cada capítulo é um `Study`**: 34 capítulos = 34 estudos. A especificação do
ARQUITECT define três artefatos: **OBRA** (a fonte: livro, coletânea ou condensado),
**ADENDOS** (notas de admin+revisor) e **ESTUDO** (o artefato aplicável). Os capítulos
do estudo **não correspondem** aos da obra — um capítulo da obra pode gerar vários do
estudo.

## Decisão

Modelar os três artefatos com mapa N:N entre capítulos de obra e de estudo, em
`models/obra.py` mais as tabelas de Estudo. **Fase 1 (Obra) já entregue**; o Estudo
vem na DEM piloto.

## Consequências

**Positivas:**
- Separa fonte de aplicação; permite condensar e redistribuir capítulos.
- Habilita os níveis como trilhas de profundidade paralelas.

**Negativas / trade-offs:**
- Exige migrar conteúdo de `StudyVersion` para `EstudoCapitulo` (Fase 4, com janela de risco).
- Mais tabelas e mais estados.

## Impacto nas DEMs

- **DEM piloto** (DEM-202610-001).
- A ADR-011 refina esta: a aprovação do estudo passa a ser assinada e amarrada ao hash.
