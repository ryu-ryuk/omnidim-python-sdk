"""
Call commands
"""

import typer
from typing import Optional
from rich.console import Console

import json
from ..core.client import get_client
from ..core.utils import format_json_output, create_calls_table, extract_id_from_response

app = typer.Typer(help="Call management commands")
console = Console()


@app.command("list")
def list_calls(
    page: int = typer.Option(1, "--page", "-p", help="Page number"),
    page_size: int = typer.Option(10, "--page-size", "-s", help="Page size"),
    agent_id: Optional[int] = typer.Option(
        None, "--agent-id", help="Filter by agent ID"
    ),
    format_output: str = typer.Option(
        "table", "--format", "-f", help="Output format: table, json"
    ),
):
    """List call logs"""
    client = get_client()

    try:
        result = client.call.get_call_logs(
            page=page, page_size=page_size, agent_id=agent_id
        )

        if format_output == "json":
            format_json_output(result, f"Call Logs (Page {page})")
            return

        calls = result.get("json", {}).get("calls", [])

        if not calls:
            console.print("[yellow]No calls found[/yellow]")
            return

        table = create_calls_table(calls)
        console.print(f"\n[bold cyan]Call Logs (Page {page})[/bold cyan]")
        console.print(table)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("get")
def get_call(call_id: str = typer.Argument(..., help="Call ID")):
    """Get call details"""
    client = get_client()

    try:
        call = client.call.get_call_log(call_id)
        format_json_output(call, f"Call {call_id}")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("dispatch")
def dispatch_call(
    agent_id: int = typer.Argument(..., help="Agent ID"),
    to_number: str = typer.Argument(..., help="Phone number to call"),
    context: Optional[str] = typer.Option(
        None, "--context", help="Call context (JSON)"
    ),
):
    """Dispatch a call"""
    client = get_client()

    call_context = {}
    if context:
        try:
            call_context = json.loads(context)
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON in context[/red]")
            raise typer.Exit(1)

    try:
        result = client.call.dispatch_call(agent_id, to_number, call_context)
        call_id = extract_id_from_response(result)
        if call_id:
            console.print(f"[green]Call dispatched successfully. ID: {call_id}[/green]")
        else:
            console.print("[yellow]Call dispatched but ID not found in response.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error dispatching call: {e}[/red]")
        raise typer.Exit(1)
