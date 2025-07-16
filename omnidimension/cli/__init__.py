"""
OmniDimension CLI - Main entry point
"""
import typer
import sys
from typing import Optional

from .commands import agents, calls, simulations, kb, phone, integrations
from .core.config import CLIConfig
from .core.client import get_client
from .interactive import interactive_mode

app = typer.Typer(
    help="OmniDimension CLI - Voice agent management",
    no_args_is_help=False,  # no arg = interactive mode
    invoke_without_command=True
)

app.add_typer(agents.app, name="agents")
app.add_typer(calls.app, name="calls") 
app.add_typer(simulations.app, name="simulations")
app.add_typer(kb.app, name="kb")
app.add_typer(phone.app, name="phone")
app.add_typer(integrations.app, name="integrations")

@app.callback(invoke_without_command=True)
def main_callback(ctx: typer.Context):
    """Main callback - launches interactive mode if no command provided"""
    if ctx.invoked_subcommand is None:
        interactive_mode()

@app.command()
def config(
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
    set_key: Optional[str] = typer.Option(None, "--set-key", help="Set API key"),
    set_url: Optional[str] = typer.Option(None, "--set-url", help="Set base URL")
):
    """Manage CLI configuration"""
    config_manager = CLIConfig()
    
    if show:
        config_manager.show()
    elif set_key:
        config_manager.set_api_key(set_key)
    elif set_url:
        config_manager.set_base_url(set_url)
    else:
        config_manager.show()

@app.command()
def interactive():
    """Launch interactive mode"""
    interactive_mode()

def main():
    """Main entry point"""
    app()

if __name__ == "__main__":
    main()
