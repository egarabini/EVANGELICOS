# Briefing do EVAL — DEM-202610-012 (julgamento cego)

> **Para:** EVAL (subagente cego) · **De:** PLANNER · **Data:** 2026-10-19
> **Você não sabe quem implementou — e não deve procurar saber.** A jornada do implementador
> está fora do seu alcance. Julgue **pelo plano de testes**, não pela pessoa.

## 1. O que ler

1. `planner/intent.md` — o outcome, os H-xx e as decisões 8.1–8.5.
2. `planner/spec.md` — os RF01–RF07, os CA01–CA05 e a **§5** (o escopo da varredura e as
   **exceções declaradas**).
3. `planner/plano-testes.md` — os casos F, N, C, H e o baseline.
4. O **diff** da branch `feature/DEM-202610-012-credencial-de-seed` contra o `develop`.
5. O código, com o cwd em `ESTUDOS_BIBLICOS/GSI_EBD` (o `rxconfig` só é lido de lá).

## 2. O que fazer

- Rodar a suíte **do diretório do app** e os casos do plano (F-01 a F-07, N-01 a N-04, C-01 a C-03).
- Verificar os **CA01–CA05** um por um.
- **Tentar quebrar**: o seed sem `SEED_PASSWORD` (e com ela vazia); a **idempotência**; a varredura
  nos 5 caminhos (e a lista de exceções); a saída do `subir.sh`.
- **Provar que o teste falha quando o guarda é removido** — a lição da DEM-002: um teste que passa
  com o guarda arrancado é vacuoso. Para o N-01, mostre a varredura falhando com a senha
  reintroduzida; para o F-01, mostre o seed passando a criar usuário sem a variável.

## 3. O que reportar

- **PASS/FAIL por caso** (F, N, C, H) com o comando e a saída de cada um;
- para cada **FAIL**: o defeito, a causa e o caso do plano que ele viola;
- **avisos não bloqueantes** (separados dos FAILs);
- o **veredito**: PASS ou FAIL, com a justificativa.

## 4. Limites

- Não leia a jornada do implementador (é a condição do julgamento cego).
- Não "conserte" nada — você julga.
- Se o plano não puder ser executado (ambiente, comando errado), registre e devolva ao PLANNER —
  isso é um FAIL de **procedimento**, não do código.
