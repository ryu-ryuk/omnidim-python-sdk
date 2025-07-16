"""
Client management for CLI
"""
import typer
from rich.console import Console
from omnidimension.client import Client
from .config import CLIConfig

console = Console()

def get_client() -> Client:
    """Get authenticated client"""
    config = CLIConfig()
    api_key = config.get_api_key()
    
    if not api_key:
        console.print(
            "[bold red]No API key found[/bold red]\n"
            "Set your API key using: [cyan]omnidim config --set-key YOUR_KEY[/cyan]\n"
            "Or set environment variable: [cyan]export OMNIDIM_API_KEY=your_key[/cyan]"
        )
        raise typer.Exit(1)

    try:
        base_url = config.get_base_url()
        client = Client(api_key, base_url=base_url)
        return client
    except Exception as e:
        console.print(f"[red]Failed to initialize client: {e}[/red]")
        raise typer.Exit(1)
