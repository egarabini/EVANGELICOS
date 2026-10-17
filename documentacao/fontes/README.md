# Fontes — inventário de licenças do acervo

> Dono: PLANNER. Rege-se pela **ADR-012** e pela spec da
> [DEM-202610-003](../dem/DEM-202610-003-inventario-de-fontes/planner/spec.md).

## O que é

`inventario.csv` é o catálogo de **todas as fontes do acervo**: uma linha por **fonte
ocorrendo num projeto**. Responde, para qualquer fonte: *posso exibir isto ao aluno?* — e,
quando a resposta é "ainda não", diz **o que** falta, **com quem** e **quando**.

Ele é o embrião do registro de fontes que a **DEM-B** vai persistir e a base que a **DEM-C**
consulta antes de ingerir qualquer dado.

## Como verificar

```
python documentacao/fontes/verificar_inventario.py
```

O verificador confere estrutura (BOM, `;`, 17 colunas), enums, obrigatoriedade de motivo e
de gatilho, e a **cobertura** contra a lista fechada do Anexo A da spec. É o instrumento do
EVAL: ele lê o CSV, não o código que o gerou.

## Regras de manutenção

1. **Fonte nova = linha nova.** Sem linha, a fonte não existe para a política.
2. **Nunca resolver `a confirmar` sem evidência.** Trocar por uma licença exige citar onde
   foi confirmada (URL, e-mail, contrato) em `observacoes`.
3. **`decisao ≠ entra` exige `motivo`.** Motivo objetivo, não "não convém".
4. **`adequacao_doutrinaria` é preenchida pelo PLANNER e revisada pelo ARQUITECT.** Ao
   revisar, preencher `revisado_por` e `revisado_em` — é o registro de que a linha foi
   olhada por gente.
5. **Dúvida vira `a_revisar`.** Inventário que finge saber é pior que inventário que declara
   a dúvida.
6. **Na dúvida entre regimes, o mais restritivo** (spec §6.1).

## Como ler as 17 colunas

| Coluna | O que significa |
|---|---|
| `id` | identificador da linha (`F-001`…) |
| `fonte` | nome da fonte; para o Sensus: `Sensus — <id>: <título>` |
| `tipo` | `corpus` · `referencia_cruzada` · `obra` · `adendo` · `fonte_dados` · `codigo` · `conteudo` · `ferramenta` |
| `titular` | quem detém o direito, ou `a confirmar` |
| `licenca` | licença identificada (ou `a confirmar`) |
| `licenca_verificada` | `sim`/`nao` — se a licença foi conferida na fonte |
| `regime_exibicao` | `curto` (trecho ao aluno) · `integral_interno` (só os quatro papéis) · `nao_exibir` |
| `atribuicao_exigida` | texto a exibir, ou `não` |
| `versao_data` | versão, edição ou data |
| `adequacao_doutrinaria` | `ok` · `atencao` · `fora` · `a_revisar` |
| `decisao` | `entra` · `nao_entra` · `depende` |
| `motivo` | obrigatório quando a decisão não é `entra` |
| `localizacao` | onde a fonte está no repositório |
| `adr_referencia` | a ADR (ou decisão) que rege a linha |
| `observacoes` | gatilho (**o quê · com quem · quando**) e notas |
| `revisado_por` / `revisado_em` | preenchidos na revisão do ARQUITECT |

## Pendências conhecidas (registradas, não escondidas)

| Pendência | Estado |
|---|---|
| **Medida objetiva de "curto"** (nº de palavras, % do capítulo) | proposta do PLANNER, a fechar pelo ARQUITECT. Não trava o inventário: o regime já está classificado. Vira requisito da DEM que construir o "detalhar". |
| **Limite de citação da ACF** | depende da SBTB (F-001) |
| **Titularidade/licença da tradução PT** | a **obra** está em `direito reservado` (F-004, F-007, F-008); o que falta identificar é a **tradução**. Henry PT é `a confirmar` (F-002) |
| **`adequacao_doutrinaria` das fontes adventistas e dispensacionalistas** | provisória (`atencao`); o ARQUITECT revisa. Não é exclusão — é identificação de tradição. |
| **Autoria dos resumos do `biblia-plataforma`** | `a confirmar` (F-074) |
| **Duplicidade de fontes entre projetos** (Bíblia Livre, OpenBible) | catálogo registra a ocorrência; a normalização (fonte única + N:N com projeto) é da **DEM-B** |

## O que o inventário NÃO faz

- não ingere dado (DEM-C);
- não persiste no banco (DEM-B);
- não verifica juridicamente licença (a resposta correta hoje é `a confirmar` + gatilho);
- não decide doutrina — registra a decisão de quem decide.
