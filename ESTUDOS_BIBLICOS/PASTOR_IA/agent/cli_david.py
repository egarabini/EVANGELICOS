"""
cli_david.py -- Interface de linha de comando para testar o DAVID
Uso: python agent/cli_david.py
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.david_agent import DAVIDAgent
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.rule import Rule

console = Console()

BANNER = """
  ____    _    __     _____ ____
 |  _ \\  / \\   \\ \\   / /_ _|  _ \\
 | | | |/ _ \\   \\ \\ / / | || | | |
 | |_| / ___ \\   \\ V /  | || |_| |
 |____/_/   \\_\\   \\_/  |___|____/

  Agente de Estudo Biblico
  Em honra a David Livingstone (1813-1873)
  "Eu colocarei nenhum valor em nada que tenho ou possuo,
   exceto em relacao ao reino de Cristo."
"""

def main():
    console.print(Panel(BANNER, style="bold green", border_style="green"))

    david = DAVIDAgent()

    console.print("[dim]Conectando ao ChromaDB e carregando modelo de embeddings...[/dim]")
    total = david.total_versiculos
    console.print(f"[green]OK: {total:,} versiculos biblicos disponiveis[/green]")
    console.print(f"[dim]Modelo LLM: hermes3:8b via Ollama | Embedding: MiniLM-L12-v2[/dim]")
    console.print()
    console.print("[yellow]Comandos: 'sair' para encerrar | 'nova sessao' para limpar historico | 'rag: <query>' para busca direta[/yellow]")
    console.print(Rule(style="green"))
    console.print()

    # Apresentacao inicial do DAVID
    console.print("[dim]Aguardando DAVID se apresentar (pode levar ~30-60s na primeira vez em CPU)...[/dim]")
    try:
        apresentacao = david.responder("Apresente-se brevemente como DAVID.")
        console.print(Panel(
            Text(apresentacao, style="white"),
            title="[bold green]DAVID[/bold green]",
            border_style="green"
        ))
    except Exception as e:
        console.print(f"[red]DAVID nao respondeu: {e}[/red]")
        console.print("[yellow]Verifique se o Ollama esta rodando com hermes3:8b[/yellow]")

    console.print()

    while True:
        try:
            entrada = Prompt.ask("[bold cyan]Voce[/bold cyan]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Encerrando... Que Deus o abencoe![/yellow]")
            break

        if not entrada:
            continue

        if entrada.lower() in ("sair", "exit", "quit"):
            console.print("[yellow]Que Deus o abencoe! Ate a proxima![/yellow]")
            break

        if entrada.lower() == "nova sessao":
            david.nova_sessao()
            console.print("[dim]Historico limpo. Nova conversa iniciada.[/dim]")
            continue

        # Modo debug: busca RAG direto
        if entrada.lower().startswith("rag:"):
            query = entrada[4:].strip()
            console.print(f"[dim]Buscando no RAG: '{query}'[/dim]")
            versiculos = david.buscar_versiculos(query)
            if versiculos:
                for v in versiculos:
                    console.print(f"  [{v['referencia']}] score={v['score']:.3f} -- {v['texto'][:80]}...")
            else:
                console.print("[yellow]Nenhum versiculo encontrado com score >= 0.55[/yellow]")
            continue

        # Resposta normal do DAVID
        console.print("[dim]DAVID esta pensando...[/dim]")
        try:
            resposta = david.responder(entrada)
            console.print(Panel(
                Text(resposta, style="white"),
                title="[bold green]DAVID[/bold green]",
                border_style="green"
            ))
        except Exception as e:
            console.print(f"[red]Erro ao chamar DAVID: {e}[/red]")
            console.print("[dim]Dica: a primeira geracao em CPU pode demorar 1-3 minutos[/dim]")

        console.print()


if __name__ == "__main__":
    main()
