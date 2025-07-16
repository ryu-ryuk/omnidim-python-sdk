"""
Integration commands
TODO: It needs more improvements and edge cases handling
"""

import json
import typer
from rich.console import Console

from ..core.client import get_client
from ..core.utils import format_json_output, extract_id_from_response

app = typer.Typer(help="Integration management commands")
console = Console()


@app.command("create-api")
def create_api_integration(
    name: str = typer.Option(..., "--name", "-n", help="Integration name"),
    url: str = typer.Option(..., "--url", "-u", help="API URL"),
    method: str = typer.Option(
        "GET", "--method", "-m", help="HTTP method (GET, POST, PUT, DELETE, PATCH)"
    ),
    description: str = typer.Option("", "--description", "-d", help="Description"),
    headers: str = typer.Option(None, "--headers", help="Headers as JSON string"),
    body_type: str = typer.Option(
        None, "--body-type", help="Body type (none, json, form)"
    ),
    body_content: str = typer.Option(None, "--body-content", help="Body content"),
    query_params: str = typer.Option(
        None, "--query-params", help="Query params as JSON string"
    ),
    timeout: int = typer.Option(10, "--timeout", help="Request timeout in seconds"),
):
    """custom API integration"""

    client = get_client()

    # parse JSON params
    headers_list = None
    if headers:
        try:
            headers_list = json.loads(headers)
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON in headers[/red]")
            raise typer.Exit(1)

    query_params_list = None
    if query_params:
        try:
            query_params_list = json.loads(query_params)
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON in query_params[/red]")
            raise typer.Exit(1)

    try:
        response = client.integrations.create_custom_api_integration(
            name=name,
            url=url,
            method=method,
            description=description,
            headers=headers_list,
            body_type=body_type,
            body_content=body_content,
            query_params=query_params_list,
            request_timeout=timeout,
        )

        # extract the integration ID from response
        integration_id = extract_id_from_response(response, "integration_id") or extract_id_from_response(response)

        if integration_id:
            console.print(
                f"[green]Integration created successfully. ID: {integration_id}[/green]"
            )
        else:
            console.print(
                f"[yellow]Integration created but ID not found in response.[/yellow]"
            )
    except Exception as e:
        console.print(f"[red]Error creating integration: {e}[/red]")
        raise typer.Exit(1)


@app.command("attach")
def attach_integration(
    agent_id: int = typer.Argument(..., help="Agent ID"),
    integration_id: int = typer.Argument(..., help="Integration ID"),
):
    """attach integration to agent"""
    client = get_client()

    try:
        result = client.integrations.add_integration_to_agent(
            agent_id=agent_id, integration_id=integration_id
        )
        console.print(
            f"[green]Integration {integration_id} attached to agent {agent_id} successfully[/green]"
        )
    except Exception as e:
        console.print(f"[red]Error attaching integration: {e}[/red]")
        raise typer.Exit(1)


@app.command("list")
def list_user_integrations():
    """List all user integrations"""
    client = get_client()

    try:
        integrations = client.integrations.get_user_integrations()
        format_json_output(integrations, "User Integrations")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("list-agent")
def list_agent_integrations(agent_id: int = typer.Argument(..., help="Agent ID")):
    """List integrations for a specific agent"""
    client = get_client()

    try:
        integrations = client.integrations.get_agent_integrations(agent_id)
        format_json_output(integrations, f"Agent {agent_id} Integrations")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("create-cal")
def create_cal_integration(
    name: str = typer.Option(..., "--name", "-n", help="Integration name"),
    cal_api_key: str = typer.Option(..., "--api-key", help="Cal.com API key"),
    cal_id: str = typer.Option(..., "--cal-id", help="Cal.com ID"),
    cal_timezone: str = typer.Option(..., "--timezone", help="Cal.com timezone"),
    description: str = typer.Option("", "--description", "-d", help="Description"),
):
    """Create Cal.com integration"""
    client = get_client()

    try:
        response = client.integrations.create_cal_integration(
            name=name,
            cal_api_key=cal_api_key,
            cal_id=cal_id,
            cal_timezone=cal_timezone,
            description=description,
        )
        integration_id = extract_id_from_response(response)
        if integration_id:
            console.print(
                f"[green]Cal.com integration created successfully. ID: {integration_id}[/green]"
            )
        else:
            console.print("[yellow]Cal.com integration created but ID not found in response.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error creating Cal.com integration: {e}[/red]")
        raise typer.Exit(1)


@app.command("create-from-json")
def create_integration_from_json(
    file_path: str = typer.Argument(
        ..., help="Path to JSON file with integration data"
    ),
):
    """Create integration from JSON file"""
    client = get_client()

    try:
        with open(file_path, "r") as f:
            integration_data = json.load(f)

        response = client.integrations.create_integration_from_json(integration_data)
        integration_id = extract_id_from_response(response)
        if integration_id:
            console.print(
                f"[green]Integration created successfully. ID: {integration_id}[/green]"
            )
        else:
            console.print("[yellow]Integration created but ID not found in response.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error creating integration: {e}[/red]")
        raise typer.Exit(1)


@app.command("detach")
def detach_integration(
    agent_id: int = typer.Argument(..., help="Agent ID"),
    integration_id: int = typer.Argument(..., help="Integration ID"),
):
    """Remove integration from agent"""
    client = get_client()

    try:
        result = client.integrations.remove_integration_from_agent(
            agent_id=agent_id, integration_id=integration_id
        )
        console.print(
            f"[green]Integration {integration_id} removed from agent {agent_id} successfully[/green]"
        )
    except Exception as e:
        console.print(f"[red]Error removing integration: {e}[/red]")
        raise typer.Exit(1)
