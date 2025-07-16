"""
Simulation commands
"""
import typer
import json
from typing import Optional
from rich.console import Console

from ..core.client import get_client
from ..core.utils import format_json_output, create_simulations_table, validate_json_input, extract_id_from_response

app = typer.Typer(help="Simulation management commands")
console = Console()

@app.command("list")
def list_simulations(
    page: int = typer.Option(1, "--page", "-p", help="Page number"),
    page_size: int = typer.Option(10, "--page-size", "-s", help="Page size"),
    format_output: str = typer.Option("table", "--format", "-f", help="Output format: table, json")
):
    """List simulations"""
    client = get_client()
    
    try:
        result = client.simulation.list(pageno=page, pagesize=page_size)
        
        if format_output == "json":
            format_json_output(result, f"Simulations (Page {page})")
            return
        
        simulations = result.get("json", {}).get("simulations", [])
        if not simulations:
            console.print("[yellow]No simulations found[/yellow]")
            return

        table = create_simulations_table(simulations)
        console.print(f"\n[bold cyan]Simulations (Page {page})[/bold cyan]")
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

@app.command("get")
def get_simulation(simulation_id: int = typer.Argument(..., help="Simulation ID")):
    """Get simulation details"""
    client = get_client()
    
    try:
        simulation = client.simulation.get(simulation_id)
        format_json_output(simulation, f"Simulation {simulation_id}")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

@app.command("create")
def create_simulation(
    name: str = typer.Option(..., "--name", "-n", help="Simulation name"),
    agent_id: int = typer.Option(..., "--agent-id", "-a", help="Agent ID"),
    calls: int = typer.Option(1, "--calls", "-c", help="Number of calls per scenario"),
    concurrent: int = typer.Option(3, "--concurrent", help="Concurrent calls"),
    duration: int = typer.Option(3, "--duration", "-d", help="Max call duration in minutes"),
    from_file: Optional[str] = typer.Option(None, "--file", "-f", help="Load configuration from JSON file")
):
    """Create a simulation"""
    client = get_client()
    
    if from_file:
        try:
            with open(from_file, 'r') as f:
                config = json.load(f)
            response = client.simulation.create(**config)
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
            raise typer.Exit(1)
    else:
        config = {
            "name": name,
            "agent_id": agent_id,
            "number_of_call_to_make": calls,
            "concurrent_call_count": concurrent,
            "max_call_duration_in_minutes": duration
        }
        response = client.simulation.create(**config)
    
    try:
        sim_id = extract_id_from_response(response)
        if sim_id:
            console.print(f"[green]Simulation created successfully. ID: {sim_id}[/green]")
        else:
            console.print("[yellow]Simulation created but ID not found in response.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error creating simulation: {e}[/red]")
        raise typer.Exit(1)

@app.command("update")
def update_simulation(
    simulation_id: int = typer.Argument(..., help="Simulation ID"),
    data: Optional[str] = typer.Option(None, "--data", "-d", help="JSON data for update"),
    from_file: Optional[str] = typer.Option(None, "--file", "-f", help="Load update data from JSON file")
):
    """Update a simulation"""
    client = get_client()
    
    if from_file:
        try:
            with open(from_file, 'r') as f:
                update_data = json.load(f)
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
            raise typer.Exit(1)
    elif data:
        valid, update_data = validate_json_input(data)
        if not valid:
            console.print(f"[red]Invalid JSON: {update_data}[/red]")
            raise typer.Exit(1)
    else:
        console.print("[red]Either --data or --file must be provided[/red]")
        raise typer.Exit(1)

    try:
        result = client.simulation.update(simulation_id, update_data)
        console.print(f"[green]Simulation {simulation_id} updated successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error updating simulation: {e}[/red]")
        raise typer.Exit(1)

@app.command("delete")
def delete_simulation(
    simulation_id: int = typer.Argument(..., help="Simulation ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation")
):
    """Delete a simulation"""
    client = get_client()
    
    if not force:
        if not typer.confirm(f"Delete simulation {simulation_id}?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

    try:
        result = client.simulation.delete(simulation_id)
        console.print(f"[green]Simulation {simulation_id} deleted successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error deleting simulation: {e}[/red]")
        raise typer.Exit(1)

@app.command("start")
def start_simulation(simulation_id: int = typer.Argument(..., help="Simulation ID")):
    """Start a simulation"""
    client = get_client()
    
    try:
        result = client.simulation.start(simulation_id)
        console.print(f"[green]Simulation {simulation_id} started successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error starting simulation: {e}[/red]")
        raise typer.Exit(1)

@app.command("stop")
def stop_simulation(simulation_id: int = typer.Argument(..., help="Simulation ID")):
    """Stop a running simulation"""
    client = get_client()
    
    try:
        result = client.simulation.stop(simulation_id)
        console.print(f"[green]Simulation {simulation_id} stopped successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error stopping simulation: {e}[/red]")
        raise typer.Exit(1)

@app.command("enhance-prompt")
def enhance_prompt(simulation_id: int = typer.Argument(..., help="Simulation ID")):
    """Get enhanced prompt suggestions"""
    client = get_client()
    
    try:
        result = client.simulation.enhance_prompt(simulation_id)
        format_json_output(result, f"Enhanced Prompt Suggestions for Simulation {simulation_id}")
    except Exception as e:
        console.print(f"[red]Error getting enhanced prompt: {e}[/red]")
        raise typer.Exit(1)
