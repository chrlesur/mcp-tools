# -*- coding: utf-8 -*-
"""
Fonctions d'affichage Rich partagées entre CLI Click et Shell interactif.

Chaque outil MCP devrait avoir sa propre fonction show_xxx_result() ici.
Ces fonctions sont importées dans commands.py ET shell.py (DRY).
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


# =============================================================================
# Utilitaires communs
# =============================================================================

def show_error(msg: str):
    """Affiche un message d'erreur."""
    console.print(f"[red]❌ {msg}[/red]")


def show_success(msg: str):
    """Affiche un message de succès."""
    console.print(f"[green]✅ {msg}[/green]")


def show_warning(msg: str):
    """Affiche un avertissement."""
    console.print(f"[yellow]⚠️  {msg}[/yellow]")


def show_json(data: dict):
    """Affiche un dict en JSON coloré."""
    import json
    console.print(Syntax(
        json.dumps(data, indent=2, ensure_ascii=False), "json"
    ))


# =============================================================================
# Affichage des outils système
# =============================================================================

def show_health_result(result: dict):
    """Affiche le résultat de system_health."""
    status = result.get("status", "?")
    service_name = result.get("service_name", "?")
    services = result.get("services", {})

    icon = "✅" if status in ("ok", "healthy") else "❌"
    color = "green" if status == "ok" else "red"

    table = Table(title=f"{icon} {service_name} — Health Check", show_header=True)
    table.add_column("Service", style="cyan bold")
    table.add_column("Statut", style=color)
    table.add_column("Détails", style="dim")

    for name, info in services.items():
        s = info.get("status", "?")
        s_icon = "✅" if s == "ok" else "❌"
        details = info.get("message", info.get("uptime", ""))
        table.add_row(name, f"{s_icon} {s}", str(details))

    console.print(table)


def show_about_result(result: dict):
    """Affiche le résultat de system_about."""
    name = result.get("service_name", "?")
    version = result.get("version", "?")
    py_version = result.get("python_version", "?")
    tools_count = result.get("tools_count", 0)
    tools = result.get("tools", [])

    console.print(Panel.fit(
        f"[bold]Service :[/bold] [cyan]{name}[/cyan]\n"
        f"[bold]Version :[/bold] [green]{version}[/green]\n"
        f"[bold]Python  :[/bold] {py_version}\n"
        f"[bold]Outils  :[/bold] {tools_count}",
        title="ℹ️  À propos",
        border_style="blue",
    ))

    if tools:
        table = Table(title=f"🔧 Outils MCP ({tools_count})", show_header=True)
        table.add_column("Nom", style="cyan bold")
        table.add_column("Description", style="dim", max_width=60)
        for t in tools:
            table.add_row(t.get("name", "?"), t.get("description", ""))
        console.print(table)
