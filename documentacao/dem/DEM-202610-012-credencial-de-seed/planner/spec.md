# Spec — DEM-202610-012 / credencial de seed

> Dono: PLANNER. **Nível 3** (segurança) — processo completo (ADR-018). Executor: **Codex** (DEVS).
> **Revisão de 19/10**: o escopo do RF04 foi definido com o ARQUITECT, com **lista de exceções**;
> `create_gestor` e o texto da tela saíram do escopo e viraram a **D-10**.

## 1. Referência

Intent: [`intent.md`](intent.md) — **signed** 2026-10-19 · ADR-008 (segredos) · ADR-018 (D-01, D-10)

## 2. Requisitos funcionais

- [ ] **RF01:** o seed lê a senha de **`SEED_PASSWORD`** (ambiente); **não há default no código**. — *(§8.1)*
- [ ] **RF02:** sem `SEED_PASSWORD` (ou com ela **vazia**), o seed **aborta** com exit ≠ 0 e
  mensagem que diga como definir a variável — sem criar nenhum usuário. — *(§8.2)*
- [ ] **RF03:** **todos** os usuários criados pelo seed nascem com `must_change_password=True`,
  incluindo o admin. — *(§8.3)*
- [ ] **RF04:** a senha `senha123` **não aparece** em:
  `gsi_ebd/data/seed.py` · `tests/` · `README.md` · `deploy/DEPLOY.md` · `deploy/subir.sh`.
  *(§4 "In" — o escopo é uma **lista**, não o repositório inteiro.)*
- [ ] **RF05:** o seed continua **idempotente** — usuário existente é pulado, nada é sobrescrito.
- [ ] **RF06:** `.env.example` documenta `SEED_PASSWORD=` **sem valor real** (placeholder).
- [ ] **RF07:** o fim do `subir.sh` **não imprime** e-mail/senha de login no log do deploy.

## 3. Requisitos não funcionais

- **Segurança:** nenhum segredo no repositório (ADR-008); a senha nunca é impressa em log.
- **Compatibilidade:** o hash continua bcrypt; nenhuma dependência nova.
- **Escopo:** **não** mexer em `create_gestor` nem no texto da tela — são a **D-10**.
- **Testes:** rodar do diretório do app (`ESTUDOS_BIBLICOS/GSI_EBD`) — a lição da DEM-002.

## 4. Contratos

```python
# gsi_ebd/data/seed.py
SENHA_SEED = os.environ.get("SEED_PASSWORD") or None   # vazio conta como ausente
if not SENHA_SEED:  # fail-fast, antes de qualquer consulta ao banco
    raise SystemExit("defina SEED_PASSWORD para rodar o seed")
def seed_admin(session) -> User: ...                    # must_change_password=True
```

## 5. O escopo da varredura e as exceções (a revisão de 19/10)

| Entra na varredura (RF04/H-11/N-01) | **Fica de fora (declarado)** |
|---|---|
| `gsi_ebd/data/seed.py` | `documentacao/adr/ADR-008*` — o registro da dívida |
| `tests/` | registros de **DEM/EVAL** (citam por histórico) |
| `README.md` | `Diagnostico/*.md` — registro histórico do projeto |
| `deploy/DEPLOY.md` | `gsi_ebd/states/admin.py` e `gsi_ebd/pages/admin.py` — **D-10** |
| `deploy/subir.sh` | |

**Por que a lista e não o repositório**: uma varredura "zero no repo" é **impossível de manter** —
as ADRs, as DEMs e os EVALs citam a senha por necessidade. A lista é verificável e honesta.

## 6. Edge cases

- `SEED_PASSWORD=` (vazia) → **é ausente**: abortar (RF02).
- Seed em ambiente **já populado** (`Admin já existe`) → pular, **sem** falhar (RF05).
- Testes que criam usuários: usar a fixture, **nunca** a senha real.
- `subir.sh`: remover a **linha de eco**; o login continua, o que sai é a credencial.

## 7. Critérios de aceitação

- [ ] **CA01:** `pytest tests -q` do diretório do app → **113 + novos** verdes.
- [ ] **CA02:** sem `SEED_PASSWORD`, um seed em banco limpo **não cria nenhum usuário** e sai ≠ 0.
- [ ] **CA03:** com `SEED_PASSWORD`, todos os usuários do seed têm `must_change_password=True` (o admin incluso).
- [ ] **CA04:** a varredura dos **5 caminhos do RF04** retorna **zero**; a varredura do repositório retorna **apenas** as exceções declaradas na §5 (e o teste lista quais são).
- [ ] **CA05:** nenhuma dependência/schema novo; o CI verde.
