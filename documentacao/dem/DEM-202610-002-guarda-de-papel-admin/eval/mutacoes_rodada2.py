"""Mutacoes EM MEMORIA da rodada 2 (DEM-202610-002).

Cada invocacao roda num processo novo, do diretorio do app, e NAO toca em
arquivo nenhum: muta o objeto Python e chama o teste correspondente.

Uso:  python mutacoes_rodada2.py m1|m2|m3|m4|m5|m6
Saida: "REPROVOU" (o teste pegou a mutacao) ou "NAO REPROVOU" (furo de teste).
"""
import os
import sys

APP = r"C:\Projetos\EM_ESTUDO\EVANGELICOS\ESTUDOS_BIBLICOS\GSI_EBD"
os.chdir(APP)
sys.path.insert(0, APP)

CASO = (sys.argv[1] if len(sys.argv) > 1 else "").lower()


def veredito(nome, funcao, *args):
    try:
        funcao(*args)
    except AssertionError as e:
        print(f"REPROVOU  {nome}: {str(e)[:500]}")
        return True
    except Exception as e:  # erro tambem e reprovacao (o teste nao passou)
        print(f"REPROVOU  {nome} com {type(e).__name__}: {str(e)[:500]}")
        return True
    print(f"NAO REPROVOU  {nome} (o teste passou com a mutacao)")
    return False


def main():
    import tests.test_rbac as t

    if CASO in ("m1", "m1b"):
        # Remover o @exige de um handler = trocar o fn decorado pelo __wrapped__.
        from gsi_ebd.states.admin import AdminState
        from gsi_ebd.states.revisao import RevisaoState

        alvos = ((AdminState, "load_coordenadores"),) if CASO == "m1" else \
                ((RevisaoState, "abrir_resposta"),)
        for estado, nome in alvos:
            h = estado.event_handlers[nome]
            estado.event_handlers[nome] = h.__class__(fn=h.fn.__wrapped__, state=estado)
            print(f"mutado: {estado.__name__}.{nome} sem __exige__ "
                  f"(fn={estado.event_handlers[nome].fn!r})")
        return 0 if veredito("m1 varredura F-12", t.test_todo_evento_tem_marcador_exige) else 2

    if CASO == "m2":
        # Remover o guarda do on_load de /admin.
        from gsi_ebd.gsi_ebd import app

        pagina = app._unevaluated_pages["admin"]
        antes = [getattr(h.fn, "__qualname__", "?") for h in pagina.on_load]
        novo = [h for h in pagina.on_load
                if getattr(h.fn, "__qualname__", "") != "AuthState.guarda_admin"]
        object.__setattr__(pagina, "on_load", novo)  # UnevaluatedPage e frozen
        depois = [getattr(h.fn, "__qualname__", "?") for h in pagina.on_load]
        print(f"mutado: on_load /admin {antes} -> {depois}")
        return 0 if veredito("m2 fiacao on_load", t.test_fiacao_on_load_das_rotas_guardadas) else 2

    if CASO == "m3":
        # Tirar o REVISOR de rota:/admin.
        from gsi_ebd.models.user import Role
        from gsi_ebd.utils import rbac as r

        r.PERMISSOES["rota:/admin"] = (Role.ADMIN,)
        print(f"mutado: rota:/admin = {r.PERMISSOES['rota:/admin']}")
        falhou_matriz = veredito(
            "m3 test_matriz_de_rotas(/admin)",
            t.test_matriz_de_rotas,
            "/admin", (Role.ADMIN, Role.REVISOR),
            (Role.COORDENADOR, Role.INSTRUTOR, Role.ALUNO),
        )
        # O teste do guarda real le a MESMA matriz como oraculo: ver o que ele faz.
        veredito("m3 test_guarda_real_bloqueia_e_libera", t.test_guarda_real_bloqueia_e_libera)
        return 0 if falhou_matriz else 2

    if CASO == "m4":
        # Dar catalogo_aprovar ao REVISOR.
        from gsi_ebd.models.user import Role
        from gsi_ebd.utils import rbac as r

        r.PERMISSOES["acao:catalogo_aprovar"] = (Role.ADMIN, Role.REVISOR)
        print(f"mutado: acao:catalogo_aprovar = {r.PERMISSOES['acao:catalogo_aprovar']}")
        return 0 if veredito(
            "m4 test_matriz_de_acoes(catalogo_aprovar)",
            t.test_matriz_de_acoes,
            "acao:catalogo_aprovar", (Role.ADMIN,),
            (Role.REVISOR, Role.COORDENADOR, Role.INSTRUTOR, Role.ALUNO),
        ) else 2

    if CASO == "m6":
        # Extra (nao pedida): destino do redirect deixa de ser a casa do papel.
        from gsi_ebd.utils import rbac as r

        original = r.home_do_papel
        r.home_do_papel = lambda papel: "/login"
        print("mutado: home_do_papel -> /login para todo papel")
        falhas = []
        for nome in ("test_invariante_casa_do_papel",
                     "test_home_consistente_com_authservice",
                     "test_guarda_real_bloqueia_e_libera",
                     "test_guarda_rota_redireciona_e_libera"):
            try:
                getattr(t, nome)()
                print(f"passou  {nome} (nao pegou a mutacao)")
            except Exception as e:
                print(f"REPROVOU {nome}: {str(e)[:300]}")
                falhas.append(nome)
        r.home_do_papel = original
        # A suite inteira acusaria? Este caso isolado basta para o achado.
        return 0 if falhas else 2

    if CASO == "m7":
        # Extra (nao pedida): @exige com a CHAVE ERRADA (mesmo marcador, poder
        # maior). load_leads deixa de ser acao:leads e vira acao:catalogo_ler,
        # que inclui o REVISOR.
        from gsi_ebd.models.user import Role
        from gsi_ebd.states.admin import AdminState
        from gsi_ebd.utils.rbac import exige as decorar

        h = AdminState.event_handlers["load_leads"]
        novo = decorar("acao:catalogo_ler")(h.fn.__wrapped__)
        AdminState.event_handlers["load_leads"] = h.__class__(fn=novo, state=AdminState)
        print(f"mutado: AdminState.load_leads __exige__={AdminState.event_handlers['load_leads'].fn.__exige__}")
        # A suite relevante: marcador presente, matriz intacta, lista congelada igual.
        for nome in ("test_todo_evento_tem_marcador_exige",):
            try:
                getattr(t, nome)()
                print(f"passou  {nome}")
            except Exception as e:
                print(f"REPROVOU {nome}: {str(e)[:300]}")
        try:
            t.test_lista_de_eventos_congelada("AdminState")
            print("passou  test_lista_de_eventos_congelada(AdminState)")
        except Exception as e:
            print(f"REPROVOU test_lista_de_eventos_congelada: {str(e)[:300]}")
        # O comportamento real: REVISOR agora entra no load_leads.
        from gsi_ebd.states.auth import AuthState
        auth = AuthState(_reflex_internal_init=True)
        auth.is_authenticated = True
        auth.current_user_role = Role.REVISOR
        sub = auth.substates[AdminState.get_name()]
        import reflex as _rx
        from unittest.mock import patch

        class Acesso(Exception):
            pass

        def sessao(*a, **k):
            raise Acesso()

        try:
            with patch.object(_rx, "session", sessao):
                sub.event_handlers["load_leads"].fn(sub)
            print("NAO VAZOU  (revisor nao delegou)")
            return 2
        except Acesso:
            print("VAZOU  load_leads delegou para REVISOR - suite nao acusou (FURO de cobertura)")
            return 2

    print("uso: mutacoes_rodada2.py m1|m1b|m2|m3|m4|m5|m6|m7")
    return 1


if __name__ == "__main__":
    # m5 precisa que os estados sejam importados DEPOIS do patch: trata antes do
    # import de tests.test_rbac (que importa os estados no topo).
    if CASO == "m5":
        from reflex_base.config import get_config

        cfg = get_config()
        cfg.state_auto_setters = True
        print(f"mutado: state_auto_setters={cfg.state_auto_setters} antes de importar os estados")
        import tests.test_rbac as t  # importa os estados com a flag ligada

        from gsi_ebd.states.admin import AdminState
        print(f"  set_current_user_role existe? {getattr(AdminState, 'set_current_user_role', None) is not None}")
        try:
            ev = AdminState.setvar("current_user_role", 1)
            print(f"  setvar(current_user_role, 1) -> {type(ev).__name__} (o cliente escreve a identidade)")
        except Exception as e:
            print(f"  setvar(current_user_role, 1) -> {type(e).__name__}: {e}")
        falhou = veredito("m5 test_nenhum_setter_de_identidade", t.test_nenhum_setter_de_identidade)
        veredito("m5 test_state_auto_setters_desligado", t.test_state_auto_setters_desligado)
        sys.exit(0 if falhou else 2)

    sys.exit(main())
