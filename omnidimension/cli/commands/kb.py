"""
Knowledge Base commands
"""

import typer
import base64
from typing import Optional
from rich.console import Console

from ..core.client import get_client
from ..core.utils import format_json_output, extract_id_from_response

app = typer.Typer(help="Knowledge base management commands")
console = Console()


@app.command("list")
def list_files():
    """list knowledge base files"""
    client = get_client()

    try:
        files = client.knowledge_base.list()
        format_json_output(files, "Knowledge Base Files")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("attach")
def attach_files(
    agent_id: int = typer.Argument(..., help="Agent ID"),
    file_ids: str = typer.Argument(..., help="Comma-separated file IDs"),
    when_to_use: Optional[str] = typer.Option(
        None, "--when-to-use", help="When to use these files"
    ),
):
    """Attach knowledge base files to an agent"""
    client = get_client()

    try:
        file_id_list = [int(fid.strip()) for fid in file_ids.split(",")]
    except ValueError:
        console.print("[red]File IDs must be comma-separated integers[/red]")
        raise typer.Exit(1)

    try:
        result = client.knowledge_base.attach(file_id_list, agent_id, when_to_use)
        console.print(f"[green]Files attached to agent {agent_id} successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error attaching files: {e}[/red]")
        raise typer.Exit(1)


@app.command("detach")
def detach_files(
    agent_id: int = typer.Argument(..., help="Agent ID"),
    file_ids: str = typer.Argument(..., help="Comma-separated file IDs"),
):
    """Detach knowledge base files from an agent"""
    client = get_client()

    try:
        file_id_list = [int(fid.strip()) for fid in file_ids.split(",")]
    except ValueError:
        console.print("[red]File IDs must be comma-separated integers[/red]")
        raise typer.Exit(1)

    try:
        result = client.knowledge_base.detach(file_id_list, agent_id)
        console.print(
            f"[green]Files detached from agent {agent_id} successfully[/green]"
        )
    except Exception as e:
        console.print(f"[red]Error detaching files: {e}[/red]")
        raise typer.Exit(1)


@app.command("create")
def create_file(
    file_path: str = typer.Argument(..., help="Path to PDF file to upload"),
    filename: Optional[str] = typer.Option(
        None, "--name", help="Custom filename (optional)"
    ),
):
    """Upload a PDF file to knowledge base"""
    client = get_client()

    try:
        with open(file_path, "rb") as f:
            file_data = base64.b64encode(f.read()).decode("utf-8")

        # Use custom filename or extract from path
        if not filename:
            import os

            filename = os.path.basename(file_path)

        # Ensure it's a PDF
        if not filename.lower().endswith(".pdf"):
            console.print("[red]Only PDF files are supported[/red]")
            raise typer.Exit(1)

        result = client.knowledge_base.create(file_data, filename)
        file_id = extract_id_from_response(result, "file_id")
        if file_id:
            console.print(f"[green]File uploaded successfully. File ID: {file_id}[/green]")
        else:
            console.print("[yellow]File uploaded but ID not found in response.[/yellow]")
    except FileNotFoundError:
        console.print(f"[red]File not found: {file_path}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error uploading file: {e}[/red]")
        raise typer.Exit(1)


@app.command("delete")
def delete_file(
    file_id: int = typer.Argument(..., help="File ID to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete a file from knowledge base"""
    client = get_client()

    if not force:
        if not typer.confirm(f"Delete file {file_id}?"):
            console.print("[yellow]Cancelled[/yellow]")
            return

    try:
        result = client.knowledge_base.delete(file_id)
        console.print(f"[green]File {file_id} deleted successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error deleting file: {e}[/red]")
        raise typer.Exit(1)


@app.command("can-upload")
def check_upload(
    file_path: str = typer.Argument(..., help="Path to file to check"),
    file_type: str = typer.Option("pdf", "--type", help="File type"),
):
    """Check if a file can be uploaded"""
    client = get_client()

    try:
        import os

        file_size = os.path.getsize(file_path)

        result = client.knowledge_base.can_upload(file_size, file_type)
        format_json_output(result, f"Upload Check for {file_path}")
    except FileNotFoundError:
        console.print(f"[red]File not found: {file_path}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error checking upload: {e}[/red]")
        raise typer.Exit(1)
