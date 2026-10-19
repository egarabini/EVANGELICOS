# Spec — DEM-202610-012 / credencial de seed

> Dono: PLANNER. **Nível 3** (segurança) — processo completo (ADR-018). Executor do piloto: **Codex**.

## 1. Referência

Intent: [`intent.md`](intent.md) — draft · ADR-008 (segredos) · ADR-018 (D-01)

## 2. Requisitos funcionais

- [ ] **RF01:** o seed lê a senha de **`SEED_PASSWORD`** (variável de ambiente); **não há default
  no código**. — *(intent §8.1)*
- [ ] **RF02:** sem `SEED_PASSWORD`, o seed **aborta** com exit ≠ 0 e mensagem que diga como
  definir a variável — sem criar nenhum usuário. — *(§8.2)*
- [ ] **RF03:** **todos** os usuários criados pelo seed nascem com `must_change_password=True`,
  incluindo o admin. — *(§8.3)*
- [ ] **RF04:** nenhuma referência a `senha123` no **código** (`gsi_ebd/`), nas **docs**
  (`documentacao/`, `*.md`) e nos **testes** (`tests/`). — *(H-11)*
- [ ] **RF05:** o seed continua **idempotente** — usuário existente é pulado, nada é sobrescrito.
- [ ] **RF06:** `.env.example` documenta `SEED_PASSWORD=` **sem valor real** (placeholder).

## 3. Requisitos não funcionais

- **Segurança:** nenhum segredo no repositório (ADR-008); a senha nunca é impressa em log.
- **Compatibilidade:** o hash continua bcrypt; nenhuma dependência nova.
- **Escopo:** não mexer em `create_gestor` (registrar como dívida nova se mantiver o padrão).
- **Testes:** rodar do diretório do app (`ESTUDOS_BIBLICOS/GSI_EBD`) — a lição da DEM-002.

## 4. Contratos

```python
# gsi_ebd/data/seed.py
SENHA_SEED = os.environ.get("SEED_PASSWORD")   # None se ausente
def seed_admin(session) -> User: ...           # must_change_password=True
```

## 5. Edge cases

- `.env` com `SEED_PASSWORD` vazia (`SEED_PASSWORD=`) → **é ausente**: abortar.
- Seed em ambiente **já populado** (`Admin já existe`) → pular, **sem** falhar (RF05).
- `must_change_password=True` no admin → o login precisa encaminhar à troca (já implementado? **verificar**; se não, é bug desta DEM).
- Testes que criam usuários: usar a fixture, **nunca** a senha real.

## 6. Critérios de aceitação

- [ ] **CA01:** `pytest tests -q` do diretório do app → **113 + novos** verdes.
- [ ] **CA02:** sem `SEED_PASSWORD`, um seed em banco limpo **não cria nenhum usuário** e sai ≠ 0.
- [ ] **CA03:** com `SEED_PASSWORD`, todos os usuários do seed têm `must_change_password=True` (o admin incluso).
- [ ] **CA04:** a varredura do repo por `senha123` retorna **zero** ocorrências.
- [ ] **CA05:** nenhuma dependência/schema novo; o CI verde.
