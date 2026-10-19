# Despacho — DEM-202610-011, fatia 1 (Codex)

> **PLANNER → Codex** · 2026-10-19. O briefing completo é o [`briefing.md`](briefing.md); este
> documento é o **contrato do despacho**: o que ele recebe, o que entrega e o que acontece depois.

## 1. O alvo

- **Branch**: `feature/DEM-202610-011-fatia1-dominio`, a partir do **`develop` em `dbbfc09`** (o
  merge do PR #3). O checkout local do código está limpo nesse ponto.
- **A entrega**: a branch + o **PR → develop** + o **relatório final** (o formato da DEM-012).
- **O escopo**: **só o domínio** — sem tela, sem deploy, sem Compose, sem segredo. Os modelos
  (`ObraVersao`, os campos novos), o `flow.py`, o hash canônico e os testes do plano, incluindo a
  **prova de mutação**.

## 2. O que o Codex recebe

- o [`briefing.md`](briefing.md) (o que ler, a tarefa, as regras, o DoD);
- o pacote: [`intent`](../planner/intent.md) (signed), [`spec`](../planner/spec.md) (**aprovada**),
  [`design`](../planner/design.md) (**o alvo**), [`plano-testes`](../planner/plano-testes.md);
- os guardas do repositório (`ESTUDOS_BIBLICOS/GSI_EBD/AGENTS.md` + `CONVENTIONS.md`);
- as ADRs **011** (a aprovação assinada) e **019** (a emenda — a assinatura como intervalo).

## 3. O prompt (para a sessão do Codex)

```text
Você é o DEVS da DEM-202610-011 (fatia 1 — o domínio do fluxo de obras e estudos) no
repositório C:\Projetos\EM_ESTUDO\EVANGELICOS\ESTUDOS_BIBLICOS\GSI_EBD.

Leia, nesta ordem:
1. documentacao/dem/DEM-202610-011-fluxo-de-obras-e-estudos/dev/briefing.md (o seu briefing)
2. o intent, a spec (aprovada), o design (o alvo) e o plano de testes da mesma pasta
3. ESTUDOS_BIBLICOS/GSI_EBD/AGENTS.md e CONVENTIONS.md
4. as ADRs 011 e 019

Implemente a fatia 1: os modelos do design (ObraVersao, os campos novos em Obra e Adendo), o
flow.py (importar/revisar/recusar/liberar/alterar/contestar), o hash canônico, a
fonte_decisao() e os testes do plano — com a prova de mutação.

Regras: branch feature/DEM-202610-011-fatia1-dominio a partir do develop; PR; python -m pytest
do diretório do app; sem tela, sem deploy, sem Compose, sem segredo; sem acento no código.
Se o design tiver lacuna, registre no relatório — não invente escopo.
```

## 4. O que o PLANNER faz depois

1. lê o **diff** e confere o escopo (como fiz na DEM-012);
2. confere o **CI** do PR;
3. dispara o **EVAL cego** com o `metodo/templates/briefing-eval.md` e o plano da fatia 1;
4. com o **PASS**: o **merge** no `develop`, o registro no painel e a **fatia 2** (as telas, na v1)
   agendada.

## 4a. Aviso ao Codex — o design foi para a **v3** (19/10)

Três correções entraram **depois** do seu último despacho, e mudam o que você ia codar:

1. o **instantâneo "visto"**: o `revisar` cria a cópia do conteúdo que o Revisor leu (além do
   instantâneo da liberação); a diferença da RF11b mostra **o texto**, não só o hash;
2. o **`hash_esperado`**: `revisar`/`recusar` recebem o hash que o Revisor viu e **recusam** se o
   conteúdo atual for outro ("o conteúdo mudou desde que você abriu") — e há um teste novo;
3. o **`alterar` recebe o conteúdo novo** (`capitulos` + `adendos` da base) e o aplica à obra; e o
   `flow.py` **não pode importar `reflex`** (um teste de grep prova).

Releia o **design v3** e o **plano v3** antes de codar. O JSON `itens_visto` **não existe mais** —
ele é derivado do instantâneo visto.

## 5. O que **não** é deste despacho

A fatia 2 (as telas), o `planejar` (a 9.5, fatia posterior), o `Study`, o banco `didasko_v1` (o
marco 1 da DEM-005), o deploy, a publicação.

