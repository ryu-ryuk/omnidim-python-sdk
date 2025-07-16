"""
Agent commands
"""

import typer
import json
from typing import Optional
from rich.console import Console

from ..core.client import get_client
from ..core.utils import (
    format_json_output,
    create_agents_table,
    validate_json_input,
    extract_id_from_response,
)

app = typer.Typer(help="Agent management commands")
console = Console()


@app.command("list")
def list_agents(
    page: int = typer.Option(1, "--page", "-p", help="Page number"),
    page_size: int = typer.Option(30, "--page-size", "-s", help="Page size"),
    format_output: str = typer.Option(
        "table", "--format", "-f", help="Output format: table, json"
    ),
):
    """list all agents"""
    client = get_client()

    result = client.agent.list(page=page, page_size=page_size)

    if format_output == "json":
        format_json_output(result, f"Agents (Page {page})")
        return

    if isinstance(result, dict):
        if "json" in result:
            agent_list = result["json"].get("bots", [])
            total_records = result["json"].get("total_records", 0)
        else:
            agent_list = result.get("bots", [])
            total_records = result.get("total_records", 0)
    else:
        agent_list = []
        total_records = 0

    if not agent_list:
        console.print("[yellow]No agents found[/yellow]")
        return

    table = create_agents_table(agent_list)
    console.print(
        f"\n[bold cyan]Agents (Page {page}, Total: {total_records})[/bold cyan]"
    )
    console.print(table)


@app.command("get")
def get_agent(agent_id: int = typer.Argument(..., help="Agent ID")):
    """get agent details"""
    client = get_client()

    try:
        agent = client.agent.get(agent_id)
        format_json_output(agent, f"Agent {agent_id}")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("create")
def create_agent(
    name: str = typer.Option(..., "--name", "-n", help="Agent name"),
    welcome_message: str = typer.Option(..., "--welcome", "-w", help="Welcome message"),
    context: str = typer.Option(..., "--context", "-c", help="Context (text or JSON)"),
    call_type: Optional[str] = typer.Option(
        None, "--call-type", help="Call type: Incoming, Outgoing"
    ),
    # voice configuration
    voice_provider: Optional[str] = typer.Option(
        None,
        "--voice-provider",
        help="Voice provider: eleven_labs, deepgram, google, cartesia, rime",
    ),
    voice_id: Optional[str] = typer.Option(
        None, "--voice-id", help="Voice ID from provider (e.g., ElevenLabs: JBFqnCBsd6RMkjVDRZzb, Deepgram: aura-asteria-en)"
    ),
    # Model configuration
    model: Optional[str] = typer.Option(
        None,
        "--model",
        help="LLM model: gpt-4o, gpt-4o-mini, gpt-3.5-turbo, gemini-1.5-pro",
    ),
    temperature: Optional[float] = typer.Option(
        None, "--temperature", help="Model temperature (0.0-1.0)"
    ),
    # Transcriber configuration
    transcriber_provider: Optional[str] = typer.Option(
        None,
        "--transcriber-provider",
        help="Transcriber provider: whisper, deepgram_stream, azure_stream",
    ),
    transcriber_model: Optional[str] = typer.Option(
        None, "--transcriber-model", help="Transcriber model (e.g., nova-3, nova-2)"
    ),
    # Web search
    enable_web_search: Optional[bool] = typer.Option(
        None, "--enable-web-search", help="Enable web search"
    ),
    web_search_provider: Optional[str] = typer.Option(
        None, "--web-search-provider", help="Web search provider: DuckDuckGo, OpenAI"
    ),
    # Filler configuration
    enable_filler: Optional[bool] = typer.Option(
        None, "--enable-filler", help="Enable filler phrases"
    ),
    filler_after_sec: Optional[int] = typer.Option(
        None, "--filler-after-sec", help="Filler delay in seconds"
    ),
    from_file: Optional[str] = typer.Option(
        None, "--file", "-f", help="Load configuration from JSON file"
    ),
    show_details: Optional[bool] = typer.Option(
        False, "--show-details", help="Show detailed agent info after creation"
    ),
):
    """create a new agent"""
    client = get_client()

    if from_file:
        try:
            with open(from_file, "r") as f:
                config = json.load(f)
            response = client.agent.create(**config)
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
            raise typer.Exit(1)
    else:
        try:
            context_breakdown = json.loads(context)
            if not isinstance(context_breakdown, list):
                raise ValueError
        except Exception:
            context_breakdown = [{"title": "Purpose", "body": context}]

        kwargs = {
            "name": name,
            "welcome_message": welcome_message,
            "context_breakdown": context_breakdown,
        }

        if call_type:
            kwargs["call_type"] = call_type

        # voice configuration
        if voice_provider and voice_id:
            # Validate voice provider
            valid_voice_providers = ["eleven_labs", "deepgram", "google", "cartesia", "rime"]
            if voice_provider not in valid_voice_providers:
                console.print(f"[red]Error: Invalid voice provider '{voice_provider}'. Valid options: {', '.join(valid_voice_providers)}[/red]")
                raise typer.Exit(code=1)
            kwargs["voice"] = {"provider": voice_provider, "voice_id": voice_id}
        elif voice_provider and not voice_id:
            console.print(f"[red]Error: Voice ID is required when voice provider is specified[/red]")
            raise typer.Exit(code=1)
        elif voice_id and not voice_provider:
            console.print(f"[red]Error: Voice provider is required when voice ID is specified[/red]")
            raise typer.Exit(code=1)

        # model configuration
        if model:
            model_config = {"model": model}
            if temperature is not None:
                model_config["temperature"] = temperature
            kwargs["model"] = model_config

        # transcriber configuration
        if transcriber_provider:
            transcriber_config = {"provider": transcriber_provider}
            if transcriber_model:
                transcriber_config["model"] = transcriber_model
            kwargs["transcriber"] = transcriber_config

        # web search configuration
        if enable_web_search is not None:
            if enable_web_search and web_search_provider:
                # Validate web search provider
                valid_providers = ["DuckDuckGo", "OpenAI"]
                if web_search_provider not in valid_providers:
                    console.print(f"[red]Error: Invalid web search provider '{web_search_provider}'. Valid options: {', '.join(valid_providers)}[/red]")
                    raise typer.Exit(code=1)
                kwargs["web_search_provider"] = web_search_provider
            elif enable_web_search and not web_search_provider:
                console.print(f"[red]Error: Web search provider is required when enabling web search[/red]")
                raise typer.Exit(code=1)

        # filler configuration
        if enable_filler is not None:
            filler_config = {"enabled": enable_filler}
            if filler_after_sec is not None:
                filler_config["after_sec"] = filler_after_sec
            kwargs["filler"] = filler_config

    try:
        response = client.agent.create(**kwargs)
        agent_id = extract_id_from_response(response)
        if agent_id:
            console.print(f"[green]Agent created successfully. ID: {agent_id}[/green]")

            # Show detailed info if requested
            if show_details:
                try:
                    agent_details = client.agent.get(agent_id)
                    from ..core.utils import create_agent_details_ui

                    create_agent_details_ui(agent_details)
                except Exception as e:
                    console.print(
                        f"[yellow]Could not fetch agent details: {e}[/yellow]"
                    )
        else:
            console.print(
                "[yellow]Agent created but ID not found in response.[/yellow]"
            )
    except Exception as e:
        error_message = str(e)
        # Check for provider-specific errors and provide helpful feedback
        if "web_search_provider" in error_message.lower() or "provider" in error_message.lower():
            console.print(f"[red]Error creating agent: {error_message}[/red]")
            console.print("[yellow]Note: Valid web search providers are 'DuckDuckGo' and 'OpenAI'. Check API documentation for current supported providers.[/yellow]")
        else:
            console.print(f"[red]Error creating agent: {error_message}[/red]")
        raise typer.Exit(1)


@app.command("update")
def update_agent(
    agent_id: int = typer.Argument(..., help="Agent ID"),
    data: Optional[str] = typer.Option(
        None, "--data", "-d", help="JSON data for update"
    ),
    from_file: Optional[str] = typer.Option(
        None, "--file", "-f", help="Load update data from JSON file"
    ),
):
    """update an existing agent"""
    client = get_client()

    if from_file:
        try:
            with open(from_file, "r") as f:
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
        result = client.agent.update(agent_id, update_data)
        console.print(f"[green]Agent {agent_id} updated successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error updating agent: {e}[/red]")
        raise typer.Exit(1)


@app.command("delete")
def delete_agent(
    agent_id: int = typer.Argument(..., help="Agent ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """delete an agent"""
    client = get_client()

    if not force:
        if not typer.confirm(f"Delete agent {agent_id}?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

    try:
        result = client.agent.delete(agent_id)
        console.print(f"[green]Agent {agent_id} deleted successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error deleting agent: {e}[/red]")
        raise typer.Exit(1)
