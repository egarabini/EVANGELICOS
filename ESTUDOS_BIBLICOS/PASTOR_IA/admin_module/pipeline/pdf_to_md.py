"""
pdf_to_md.py — Fase 1 do Pipeline: PDF → Markdown limpo

Converte PDFs de livros cristãos em Markdown preservando estrutura de capítulos.

Conversor primário: marker-pdf (melhor qualidade de estrutura)
Fallback: PyMuPDF (mais rápido, texto mais bruto)

Uso:
    python pdf_to_md.py caminho/para/livro.pdf
    python pdf_to_md.py caminho/para/livro.pdf --output pasta/destino/
    python pdf_to_md.py caminho/para/livro.pdf --force-pymupdf
"""

import sys
import re
import argparse
from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def converter_com_marker(pdf_path: Path, output_dir: Path) -> Path | None:
    """
    Converte PDF → Markdown usando marker-pdf (conversor primário).
    Retorna o caminho do .md gerado ou None se falhar.
    """
    try:
        from marker.convert import convert_single_pdf
        from marker.models import load_all_models

        console.print("[cyan]⚙️  Usando marker-pdf (conversor primário)...[/cyan]")

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as p:
            p.add_task("Carregando modelos marker-pdf (CPU-only)...", total=None)
            models = load_all_models()

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as p:
            p.add_task(f"Convertendo {pdf_path.name}...", total=None)
            texto_md, _, _ = convert_single_pdf(
                str(pdf_path),
                models,
                langs=["Portuguese"],
                batch_multiplier=1,  # conservativo para CPU
            )

        if not texto_md or len(texto_md.strip()) < 100:
            console.print("[yellow]⚠️  marker-pdf gerou output vazio ou muito curto[/yellow]")
            return None

        output_path = output_dir / f"{pdf_path.stem}_marker.md"
        output_path.write_text(texto_md, encoding="utf-8")
        return output_path

    except ImportError:
        console.print("[yellow]⚠️  marker-pdf não instalado. Execute: pip install marker-pdf[/yellow]")
        return None
    except Exception as e:
        console.print(f"[yellow]⚠️  marker-pdf falhou: {e}[/yellow]")
        return None


def converter_com_pymupdf(pdf_path: Path, output_dir: Path) -> Path:
    """
    Converte PDF → Markdown usando PyMuPDF (fallback).
    Sempre funciona mas produz estrutura mais simples.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        console.print("[red]❌ PyMuPDF não instalado. Execute: pip install pymupdf[/red]")
        sys.exit(1)

    console.print("[cyan]⚙️  Usando PyMuPDF (fallback)...[/cyan]")

    doc = fitz.open(str(pdf_path))
    linhas_md = []
    paginas_processadas = 0

    for num_pagina, pagina in enumerate(doc, start=1):
        blocos = pagina.get_text("dict")["blocks"]

        for bloco in blocos:
            if bloco.get("type") != 0:  # 0 = texto
                continue

            for linha in bloco.get("lines", []):
                texto_linha = " ".join(
                    span["text"] for span in linha.get("spans", [])
                ).strip()

                if not texto_linha:
                    continue

                # Heurística para detectar títulos (font size maior)
                tamanho_fonte = max(
                    (span.get("size", 12) for span in linha.get("spans", [])),
                    default=12
                )
                flags = linha.get("spans", [{}])[0].get("flags", 0)
                is_bold = bool(flags & 16)  # bit 4 = negrito

                if tamanho_fonte >= 16 or (is_bold and tamanho_fonte >= 14):
                    linhas_md.append(f"\n## {texto_linha}\n")
                elif tamanho_fonte >= 14 or is_bold:
                    linhas_md.append(f"\n### {texto_linha}\n")
                else:
                    linhas_md.append(texto_linha)

        paginas_processadas += 1
        linhas_md.append("\n")  # Separação entre páginas

    doc.close()

    texto_md = "\n".join(linhas_md)
    output_path = output_dir / f"{pdf_path.stem}_pymupdf.md"
    output_path.write_text(texto_md, encoding="utf-8")

    console.print(f"[green]✅ PyMuPDF converteu {paginas_processadas} páginas[/green]")
    return output_path


def validar_qualidade(md_path: Path, nome_pdf: str) -> dict:
    """
    Valida a qualidade do Markdown gerado.
    Retorna dict com métricas e flag de aprovação.
    """
    conteudo = md_path.read_text(encoding="utf-8")
    linhas = conteudo.splitlines()

    cabecalhos = [l for l in linhas if l.strip().startswith("#")]
    palavras = len(conteudo.split())

    metricas = {
        "total_palavras": palavras,
        "total_linhas": len(linhas),
        "cabecalhos_encontrados": len(cabecalhos),
        "tamanho_bytes": md_path.stat().st_size,
    }

    # Critérios de aprovação
    aprovado = (
        palavras >= 500              # Mínimo de conteúdo
        and len(cabecalhos) >= 3     # Pelo menos 3 títulos/seções detectadas
    )

    metricas["aprovado"] = aprovado
    return metricas


def main():
    parser = argparse.ArgumentParser(
        description="Converte PDF de livro cristão em Markdown estruturado"
    )
    parser.add_argument("pdf", type=Path, help="Caminho para o arquivo PDF")
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Pasta de destino (padrão: mesma pasta do PDF)"
    )
    parser.add_argument(
        "--force-pymupdf",
        action="store_true",
        help="Pular marker-pdf e usar PyMuPDF diretamente"
    )
    args = parser.parse_args()

    pdf_path = args.pdf.resolve()
    if not pdf_path.exists():
        console.print(f"[red]❌ Arquivo não encontrado: {pdf_path}[/red]")
        sys.exit(1)

    output_dir = (args.output or pdf_path.parent).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"\n[bold green]📄 DAVID Pastoral — Conversor PDF → Markdown[/bold green]")
    console.print(f"Arquivo: {pdf_path.name}")
    console.print(f"Destino: {output_dir}\n")

    # Tenta converter
    md_path = None

    if not args.force_pymupdf:
        md_path = converter_com_marker(pdf_path, output_dir)
        if md_path is None:
            console.print("[yellow]↩️  Usando fallback: PyMuPDF[/yellow]")

    if md_path is None:
        md_path = converter_com_pymupdf(pdf_path, output_dir)

    # Valida qualidade
    console.print(f"\n[cyan]⚙️  Validando qualidade do Markdown...[/cyan]")
    metricas = validar_qualidade(md_path, pdf_path.stem)

    console.print(f"  Palavras: {metricas['total_palavras']:,}")
    console.print(f"  Linhas: {metricas['total_linhas']:,}")
    console.print(f"  Cabeçalhos detectados: {metricas['cabecalhos_encontrados']}")
    console.print(f"  Tamanho: {metricas['tamanho_bytes'] / 1024:.1f} KB")

    if metricas["aprovado"]:
        console.print(f"\n[bold green]✅ Conversão aprovada![/bold green]")
        console.print(f"[green]Arquivo gerado: {md_path}[/green]")
        console.print(f"\n[dim]Próximo passo: python md_to_estudo.py {md_path}[/dim]")
    else:
        console.print(f"\n[bold yellow]⚠️  Qualidade abaixo do esperado.[/bold yellow]")
        console.print("Verifique o arquivo gerado manualmente antes de prosseguir.")
        console.print(f"Arquivo: {md_path}")

    return md_path


if __name__ == "__main__":
    main()
