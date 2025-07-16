"""
Phone number commands
"""
import typer
from rich.console import Console

from ..core.client import get_client
from ..core.utils import format_json_output

app = typer.Typer(help="Phone number management commands")
console = Console()

@app.command("list")
def list_phone_numbers(
    page: int = typer.Option(1, "--page", "-p", help="Page number"),
    page_size: int = typer.Option(10, "--page-size", "-s", help="Page size")
):
    """List phone numbers"""
    client = get_client()
    
    try:
        numbers = client.phone_number.list(page=page, page_size=page_size)
        format_json_output(numbers, f"Phone Numbers (Page {page})")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

@app.command("attach")
def attach_phone_number(
    phone_number_id: int = typer.Argument(..., help="Phone number ID"),
    agent_id: int = typer.Argument(..., help="Agent ID")
):
    """attach phone number to agent"""
    client = get_client()
    
    try:
        result = client.phone_number.attach(phone_number_id, agent_id)
        console.print(f"[green]Phone number {phone_number_id} attached to agent {agent_id} successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error attaching phone number: {e}[/red]")
        raise typer.Exit(1)

@app.command("detach")
def detach_phone_number(
    phone_number_id: int = typer.Argument(..., help="Phone number ID")
):
    """Detach phone number from agent"""
    client = get_client()
    
    try:
        result = client.phone_number.detach(phone_number_id)
        console.print(f"[green]Phone number {phone_number_id} detached successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error detaching phone number: {e}[/red]")
        raise typer.Exit(1)
