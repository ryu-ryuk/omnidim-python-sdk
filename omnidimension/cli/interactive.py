"""
Interactive CLI mode using InquirerPy with catp colors 
"""
import sys
from InquirerPy import inquirer
from InquirerPy.utils import get_style
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.table import Table

from .core.client import get_client
from .core.config import CLIConfig
from .commands import agents, calls, simulations, kb, phone, integrations

console = Console()

# catp mocha colors
CATPPUCCIN_COLORS = {
    "rosewater": "#f5e0dc",
    "flamingo": "#f2cdcd",
    "pink": "#f5c2e7",
    "mauve": "#cba6f7",
    "red": "#f38ba8",
    "maroon": "#eba0ac",
    "peach": "#fab387",
    "yellow": "#f9e2af",
    "green": "#a6e3a1",
    "teal": "#94e2d5",
    "sky": "#89dceb",
    "sapphire": "#74c7ec",
    "blue": "#89b4fa",
    "lavender": "#b4befe",
    "text": "#cdd6f4",
    "subtext1": "#bac2de",
    "subtext0": "#a6adc8",
    "overlay2": "#9399b2",
    "overlay1": "#7f849c",
    "overlay0": "#6c7086",
    "surface2": "#585b70",
    "surface1": "#45475a",
    "surface0": "#313244",
    "base": "#1e1e2e",
    "mantle": "#181825",
    "crust": "#11111b"
}

# enhancing style
MENU_STYLE = {
    "questionmark": "#cba6f7 bold",  # mauve
    "question": "#cdd6f4 bold",     # text  
    "pointer": "#f5c2e7 bold",      # pink pointer
    "highlighted": "#a6e3a1 bold",  # green text for highlighted
    "selected": "#89b4fa bold",     # blue for selected
    "separator": "#6c7086",         # overlay0
    "instruction": "#bac2de",       # subtext1
    "answer": "#a6e3a1 bold",       # green for answers
}

INPUT_STYLE = {
    "questionmark": "#cba6f7 bold",  # mauve
    "question": "#cdd6f4 bold",     # text
    "answer": "#a6e3a1 bold",       # green
}

def create_welcome_banner():
    """welcome banner """
    
    # main title
    title = Text()
    title.append("Omni", style="bold #f5c2e7")  # pink
    title.append("Dimension", style="bold #cba6f7")  # mauve  
    title.append(" CLI", style="bold #89b4fa")  # blue
    
    # subtitle
    subtitle = Text("Interactive Voice Agent Management", style="italic #bac2de")
    
    # Feature list with better colors and spacing  
    features = Text.assemble(
        Text("\n~  ", style="#f5c2e7"), Text("Manage agents, calls, and simulations", style="#a6e3a1 bold"),
        Text("\n~  ", style="#fab387"), Text("Build powerful voice experiences", style="#94e2d5 bold"),  
        Text("\n~  ", style="#f9e2af"), Text("Test and optimize with ease", style="#89dceb bold"),
        Text("\n~  ", style="#cba6f7"), Text("Beautiful Catppuccin interface", style="#b4befe bold"),
    )
    
    # assemble with proper spacing
    content = Text.assemble(
        title, "\n",
        subtitle,
        features
    )
    
    return Panel(
        Align.center(content),
        title="[bold #f5c2e7]🌟 Welcome 🌟[/bold #f5c2e7]",
        border_style="#cba6f7",  # mauve border
        padding=(1, 3),
        style="#1e1e2e on #1e1e2e"  # catp base bg  
    )

def create_section_banner(title, emoji=""):
    """section banner"""
    display_text = Text()
    if emoji:
        display_text.append(f"{emoji} ", style="#f5c2e7 bold")
    display_text.append(title, style="#89b4fa bold")
    
    return Panel(
        Align.center(display_text),
        border_style="#94e2d5",  # teal
        title="[bold #94e2d5]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold #94e2d5]",
        padding=(0, 2),
        style="#1e1e2e on #1e1e2e"
    )

def create_success_message(message):
    """success message panel"""
    return Panel(
        Text.assemble(
            Text("✨ ", style="#a6e3a1 bold"),
            Text(message, style="#a6e3a1 bold")
        ),
        border_style="#a6e3a1",
        title="[bold #a6e3a1]!! Success[/bold #a6e3a1]",
        padding=(0, 1),
        style="#1e1e2e on #1e1e2e"
    )

def create_error_message(message):
    """error message panel"""
    return Panel(
        Text.assemble(
            Text("💥 ", style="#f38ba8 bold"),
            Text(message, style="#f38ba8 bold")
        ),
        border_style="#f38ba8",
        title="[bold #f38ba8]!! Error[/bold #f38ba8]",
        padding=(0, 1),
        style="#1e1e2e on #1e1e2e"
    )

def create_warning_message(message):
    """warning message panel"""
    return Panel(
        Text.assemble(
            Text("⚠️ ", style="#f9e2af bold"),
            Text(message, style="#f9e2af bold")
        ),
        border_style="#f9e2af",
        title="[bold #f9e2af]!!  Warning[/bold #f9e2af]",
        padding=(0, 1),
        style="#1e1e2e on #1e1e2e"
    )

def create_info_message(message):
    """info message panel"""
    return Panel(
        Text.assemble(
            Text("ℹ️ ", style="#89dceb bold"),
            Text(message, style="#89dceb")
        ),
        border_style="#89dceb",
        title="[bold #89dceb]Info[/bold #89dceb]",
        padding=(0, 1),
        style="#1e1e2e on #1e1e2e"
    )

def interactive_mode():
    """main interactive mode"""
    console.clear()
    console.print(create_welcome_banner())
    console.print()

    while True:
        try:
            action = inquirer.select(
                message="What would you like to do?",
                choices=[
                    Choice("agents", name="Manage Agents"),
                    Choice("calls", name="Manage Calls"),
                    Choice("simulations", name="Manage Simulations"),
                    Separator(),
                    Choice("kb", name="Knowledge Base"),
                    Choice("phone", name="Phone Numbers"),
                    Choice("integrations", name="Integrations"),
                    Separator(), 
                    Choice("config", name="Configuration"),
                    Choice("exit", name="Exit")
                ],
                pointer="▶",
                vi_mode=True,
                style=get_style(MENU_STYLE)
            ).execute()

            if action == "exit":
                console.print(Panel(
                    Text.assemble(
                        Text("✨ ", style="#f5c2e7 bold"),
                        Text("Thank you for using ", style="#a6e3a1 bold"),
                        Text("OmniDimension CLI", style="#89b4fa bold"),
                        Text("! ", style="#a6e3a1 bold"),
                        Text("\n~ ", style="#fab387 bold"),
                        Text("Quitting Omnidim !", style="#94e2d5 bold")
                    ),
                    title="[bold #cba6f7]🌟 See You! 🌟[/bold #cba6f7]",
                    border_style="#cba6f7",
                    padding=(1, 2),
                    style="#1e1e2e on #1e1e2e"
                ))
                break
            elif action == "agents":
                console.print(create_section_banner("Agent Management", "≡")) 
                agent_menu()
            elif action == "calls":
                console.print(create_section_banner("Call Management", "✆"))  
                call_menu()
            elif action == "simulations":
                console.print(create_section_banner("Simulation Management", "⧉")) 
                simulation_menu()
            elif action == "kb":
                console.print(create_section_banner("Knowledge Base", "✎"))  
                kb_menu()
            elif action == "phone":
                console.print(create_section_banner("Phone Numbers", "#"))  
                phone_menu()
            elif action == "integrations":
                console.print(create_section_banner("Integrations", "⛓")) 
                integration_menu()
            elif action == "config":
                console.print(create_section_banner("Configuration", "⚙"))
                config_menu()

                
        except KeyboardInterrupt:
            console.print("\n[color(251)]Returning to main menu...[/color(251)]")
            continue
        except Exception as e:
            console.print(create_error_message(f"Unexpected error: {e}"))

def agent_menu():
    """agent management submenu"""
    while True:
        try:
            action = inquirer.select(
                message="Agent Management",
                choices=[
                    Choice("list", name="List All Agents"),
                    Choice("list_detailed", name="List Agents (with details)"),
                    Choice("create", name="Create New Agent"),
                    Choice("get", name="Get Agent Details"),
                    Choice("update", name="Update Agent"),
                    Choice("delete", name="Delete Agent"),
                    Separator(),
                    Choice("back", name="← Back to Main Menu")
                ],
                vi_mode=True,
                style=get_style(MENU_STYLE)
            ).execute()
            
            if action == "back":
                break
            elif action == "list":
                try:
                    client = get_client()
                    result = client.agent.list(page=1, page_size=10)
                    
                    if isinstance(result, dict) and "bots" in result:
                        agent_list = result["bots"]
                    elif isinstance(result, dict) and "json" in result:
                        agent_list = result["json"].get("bots", [])
                    else:
                        agent_list = []
                    
                    if not agent_list:
                        console.print(create_warning_message("No agents found"))
                    else:
                        from .core.utils import create_agents_table
                        table = create_agents_table(agent_list)
                        console.print(table)
                        console.print()
                except Exception as e:
                    console.print(create_error_message(f"Failed to list agents: {e}"))
                    
            elif action == "list_detailed":
                try:
                    console.print(create_section_banner("Fetching Detailed Agent Information"))
                    console.print("[dim yellow]Note: Fetching comprehensive agent data including features, ASR settings, contexts, files, and integrations (rate limited)...[/dim yellow]")
                    
                    client = get_client()
                    result = client.agent.list(page=1, page_size=10)
                    if isinstance(result, dict) and "bots" in result:
                        agent_list = result["bots"]
                    elif isinstance(result, dict) and "json" in result:
                        agent_list = result["json"].get("bots", [])
                    else:
                        agent_list = []
                    
                    if not agent_list:
                        console.print(create_warning_message("No agents found"))
                    else:
                        from .core.utils import create_agents_table
                        table = create_agents_table(agent_list, client=client, show_details=True)
                        console.print(table)
                        console.print()
                        console.print("[dim green]!! Comprehensive agent details fetched successfully[/dim green]")
                        console.print("[dim]Columns show: Features (Web search, Fillers, Transfer, etc.), ASR (Speech-to-text), Context count, Attached files, Integrations, and Welcome message[/dim]")
                except Exception as e:
                    console.print(create_error_message(f"Failed to list agents with details: {e}"))
                    
            elif action == "create":
                create_agent_interactive()
            elif action == "get":
                from .core.utils import safe_int_input
                agent_id = safe_int_input("Enter agent ID", "Agent ID")
                try:
                    console.print(create_section_banner("Fetching Agent Details", "[>]"))
                    client = get_client()
                    from .core.utils import create_agent_details_ui
                    console.print()
                    create_agent_details_ui(agent_id, client=client)
                    console.print()
                except Exception as e:
                    console.print(create_error_message(f"Failed to get agent: {e}"))
            elif action == "update":
                update_agent_interactive()
            elif action == "delete":
                delete_agent_interactive()
                
        except KeyboardInterrupt:
            break

def create_agent_interactive():
    """agent creation"""
    try:
        console.print(create_section_banner("Create New Agent", "+"))
        
        name = inquirer.text(
            message="Agent name",
            style=get_style(INPUT_STYLE)
        ).execute()
        
        welcome_message = inquirer.text(
            message="Welcome message",
            style=get_style(INPUT_STYLE)
        ).execute()
        
        context = inquirer.text(
            message="Agent context/purpose",
            style=get_style(INPUT_STYLE)
        ).execute()
        
        context_breakdown = [{"title": "Purpose", "body": context}]
        
        # ask for advanced configuration
        advanced = inquirer.confirm(
            message="Configure advanced settings?",
            default=False,
            style=get_style(INPUT_STYLE)
        ).execute()
        
        kwargs = {
            "name": name,
            "welcome_message": welcome_message,
            "context_breakdown": context_breakdown
        }
        
        if advanced:
            # call type
            call_type = inquirer.select(
                message="Call type",
                choices=["Incoming", "Outgoing", "transcriber", "Skip"],
                style=get_style(MENU_STYLE)
            ).execute()
            if call_type != "Skip":
                kwargs["call_type"] = call_type
                
            # voice settings
            if inquirer.confirm(
                message="Configure voice?",
                default=False,
                style=get_style(INPUT_STYLE)
            ).execute():
                provider = inquirer.select(
                    message="Voice provider",
                    choices=["eleven_labs", "deepgram", "google", "cartesia", "rime"],
                    style=get_style(MENU_STYLE)
                ).execute()
                voice_id = inquirer.text(
                    message="Voice ID",
                    default="JBFqnCBsd6RMkjVDRZzb",
                    style=get_style(INPUT_STYLE)
                ).execute()
                kwargs["voice"] = {"provider": provider, "voice_id": voice_id}
                
            # model settings
            if inquirer.confirm(
                message="Configure model?",
                default=False,
                style=get_style(INPUT_STYLE)
            ).execute():
                model = inquirer.select(
                    message="Model",
                    choices=["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "gemini-1.5-pro", "gemini-2.0-flash", "Llama"],
                    style=get_style(MENU_STYLE)
                ).execute()
                temperature = float(inquirer.text(
                    message="Temperature (0.0-1.0)",
                    default="0.7",
                    style=get_style(INPUT_STYLE)
                ).execute())
                kwargs["model"] = {"model": model, "temperature": temperature}
                
            # transcriber settings
            if inquirer.confirm(
                message="Configure transcriber (speech-to-text)?",
                default=False,
                style=get_style(INPUT_STYLE)
            ).execute():
                provider = inquirer.select(
                    message="Transcriber provider",
                    choices=["whisper", "deepgram_stream", "azure_stream"],
                    style=get_style(MENU_STYLE)
                ).execute()
                transcriber_config = {"provider": provider}
                
                if provider == "deepgram_stream":
                    model = inquirer.select(
                        message="Deepgram model",
                        choices=["nova-3", "nova-2"],
                        style=get_style(MENU_STYLE)
                    ).execute()
                    transcriber_config["model"] = model
                    
                    # Additional deepgram options
                    if inquirer.confirm("Configure advanced Deepgram options?", default=False, style=get_style(INPUT_STYLE)).execute():
                        if inquirer.confirm("Convert numbers to digits?", default=True, style=get_style(INPUT_STYLE)).execute():
                            transcriber_config["numerals"] = True
                        if inquirer.confirm("Add punctuation?", default=True, style=get_style(INPUT_STYLE)).execute():
                            transcriber_config["punctuate"] = True
                        if inquirer.confirm("Smart formatting?", default=True, style=get_style(INPUT_STYLE)).execute():
                            transcriber_config["smart_format"] = True
                        if inquirer.confirm("Speaker diarization?", default=False, style=get_style(INPUT_STYLE)).execute():
                            transcriber_config["diarize"] = True
                
                kwargs["transcriber"] = transcriber_config
                
            # web search settings
            if inquirer.confirm(
                message="Enable web search?",
                default=False,
                style=get_style(INPUT_STYLE)
            ).execute():
                provider = inquirer.select(
                    message="Web search provider",
                    choices=["DuckDuckGo", "OpenAI"],  # Both providers are documented in API
                    style=get_style(MENU_STYLE)
                ).execute()
                kwargs["web_search_provider"] = provider
                
            # filler settings
            if inquirer.confirm(
                message="Configure filler phrases?",
                default=False,
                style=get_style(INPUT_STYLE)
            ).execute():
                enabled = inquirer.confirm(
                    message="Enable filler phrases?",
                    default=True,
                    style=get_style(INPUT_STYLE)
                ).execute()
                filler_config = {"enabled": enabled}
                
                if enabled:
                    after_sec = int(inquirer.text(
                        message="Play filler after how many seconds?",
                        default="3",
                        style=get_style(INPUT_STYLE)
                    ).execute())
                    filler_config["after_sec"] = after_sec
                    
                    # Ask for custom fillers
                    if inquirer.confirm("Add custom filler phrases?", default=False, style=get_style(INPUT_STYLE)).execute():
                        fillers = []
                        while True:
                            filler = inquirer.text(
                                message="Filler phrase (or press Enter to finish)",
                                default="",
                                style=get_style(INPUT_STYLE)
                            ).execute()
                            if not filler:
                                break
                            fillers.append(filler)
                        if fillers:
                            filler_config["fillers"] = fillers
                
                kwargs["filler"] = filler_config
        
        client = get_client()
        response = client.agent.create(**kwargs)
        
        from .core.utils import extract_id_from_response
        agent_id = extract_id_from_response(response)
        
        if agent_id:
            console.print(create_success_message(f"Agent created successfully! ID: {agent_id}"))
            
            # Show detailed agent info
            try:
                agent_details = client.agent.get(agent_id)
                from .core.utils import create_agent_details_ui
                create_agent_details_ui(agent_details)
            except Exception as e:
                console.print(create_warning_message(f"Could not fetch agent details: {e}"))
        else:
            console.print(create_warning_message("Agent created but ID not found in response."))
        
    except Exception as e:
        error_message = str(e)
        console.print(create_error_message(f"Failed to create agent: {error_message}"))
        
        # Check for provider-specific errors and provide helpful feedback
        if "web_search_provider" in error_message.lower() or "provider" in error_message.lower():
            console.print(create_warning_message("Note: Valid web search providers are 'DuckDuckGo' and 'OpenAI'. Check API documentation for current supported providers."))

def update_agent_interactive():
    """agent update"""
    try:
        console.print(create_section_banner("Update Agent", "✏️"))
        
        from .core.utils import safe_int_input
        agent_id = safe_int_input("Agent ID to update", "Agent ID")
        
        update_type = inquirer.select(
            message="What to update?",
            choices=[
                Choice("name", name="Name"),
                Choice("welcome_message", name="Welcome Message"),
                Choice("json", name="Custom JSON")
            ],
            style=get_style(MENU_STYLE)
        ).execute()
        
        if update_type == "name":
            new_name = inquirer.text(
                message="New name",
                style=get_style(INPUT_STYLE)
            ).execute()
            update_data = {"name": new_name}
        elif update_type == "welcome_message":
            new_welcome = inquirer.text(
                message="New welcome message",
                style=get_style(INPUT_STYLE)
            ).execute()
            update_data = {"welcome_message": new_welcome}
        else:
            json_data = inquirer.text(
                message="JSON update data",
                style=get_style(INPUT_STYLE)
            ).execute()
            import json
            update_data = json.loads(json_data)
        
        client = get_client()
        result = client.agent.update(agent_id, update_data)
        console.print(create_success_message(f"Agent {agent_id} updated successfully"))
        
    except Exception as e:
        console.print(create_error_message(f"Failed to update agent: {e}"))

def delete_agent_interactive():
    """agent deletion"""
    try:
        console.print(create_section_banner("Delete Agent", "[del]"))
        
        from .core.utils import safe_int_input
        agent_id = safe_int_input("Agent ID to delete", "Agent ID")
        
        if inquirer.confirm(
            f"Delete agent {agent_id}? This cannot be undone.",
            default=False,
            style=get_style(INPUT_STYLE)
        ).execute():
            client = get_client()
            result = client.agent.delete(agent_id)
            console.print(create_success_message(f"Agent {agent_id} deleted successfully"))
        else:
            console.print(create_warning_message("Deletion cancelled"))
            
    except Exception as e:
        console.print(create_error_message(f"Failed to delete agent: {e}"))

# TODO: testing 
def call_menu():
    """call management"""
    while True:
        try:
            action = inquirer.select(
                message="Call Management",
                choices=[
                    Choice("list", name="List Calls"),
                    Choice("dispatch", name="Dispatch Call"),
                    Choice("get", name="Get Call Details"),
                    Separator(),
                    Choice("back", name="← Back to Main Menu")
                ],
                vi_mode=True,
                style=get_style(MENU_STYLE)
            ).execute()
            
            if action == "back":
                break
            elif action == "list":
                try:
                    client = get_client()
                    result = client.call.get_call_logs(page=1, page_size=10)
                    # Handle direct response
                    if isinstance(result, dict) and "calls" in result:
                        calls = result["calls"]
                    elif isinstance(result, dict) and "json" in result:
                        calls = result["json"].get("calls", [])
                    else:
                        calls = []
                    
                    if not calls:
                        console.print(create_warning_message("No calls found"))
                    else:
                        from .core.utils import create_calls_table
                        table = create_calls_table(calls)
                        console.print(table)
                        console.print()
                except Exception as e:
                    console.print(create_error_message(f"Failed to list calls: {e}"))
                    
            elif action == "dispatch":
                try:
                    console.print(create_section_banner("Dispatch Call", "📞"))
                    
                    from .core.utils import safe_int_input, safe_phone_input
                    agent_id = safe_int_input("Agent ID", "Agent ID")
                    to_number = safe_phone_input("Phone number to call (e.g., +1234567890)")
                    
                    client = get_client()
                    result = client.call.dispatch_call(agent_id, to_number, {})
                    # Handle direct response
                    if isinstance(result, dict) and "id" in result:
                        call_id = result["id"]
                    elif isinstance(result, dict) and "json" in result:
                        call_id = result["json"].get("id")
                    else:
                        call_id = "Unknown"
                    console.print(create_success_message(f"Call dispatched successfully! ID: {call_id}"))
                except Exception as e:
                    console.print(create_error_message(f"Failed to dispatch call: {e}"))
                
            elif action == "get":
                try:
                    call_id = inquirer.text(
                        message="Call ID",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    client = get_client()
                    call = client.call.get_call_log(call_id)
                    from .core.utils import format_json_output
                    format_json_output(call, f"Call {call_id}")
                except Exception as e:
                    console.print(create_error_message(f"Failed to get call details: {e}"))
                    
        except KeyboardInterrupt:
            break

# TODO: testing
def simulation_menu():
    """simulation management submenu """
    while True:
        try:
            action = inquirer.select(
                message="Simulation Management",
                choices=[
                    Choice("list", name="List Simulations"),
                    Choice("create", name="Create Simulation"),
                    Choice("get", name="Get Simulation Details"),
                    Choice("start", name="Start Simulation"),
                    Choice("stop", name="Stop Simulation"),
                    Separator(),
                    Choice("back", name="← Back to Main Menu")
                ],
                vi_mode=True,
                style=get_style(MENU_STYLE)
            ).execute()
            
            if action == "back":
                break
            elif action == "list":
                try:
                    client = get_client()
                    result = client.simulation.list(pageno=1, pagesize=10)
                    if isinstance(result, dict) and "simulations" in result:
                        simulations = result["simulations"]
                    elif isinstance(result, dict) and "json" in result:
                        simulations = result["json"].get("simulations", [])
                    else:
                        simulations = []
                    
                    if not simulations:
                        console.print(create_warning_message("No simulations found"))
                    else:
                        from .core.utils import create_simulations_table
                        table = create_simulations_table(simulations)
                        console.print(table)
                        console.print()
                except Exception as e:
                    console.print(create_error_message(f"Failed to list simulations: {e}"))
                    
            elif action == "create":
                try:
                    console.print(create_section_banner("Create Simulation", "➕"))
                    
                    name = inquirer.text(
                        message="Simulation name",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    agent_id = int(inquirer.text(
                        message="Agent ID",
                        style=get_style(INPUT_STYLE)
                    ).execute())
                    
                    client = get_client()
                    config = {
                        "name": name,
                        "agent_id": agent_id,
                        "number_of_call_to_make": 1,
                        "concurrent_call_count": 3,
                        "max_call_duration_in_minutes": 3
                    }
                    response = client.simulation.create(**config)
                    if isinstance(response, dict) and "id" in response:
                        sim_id = response["id"]
                    elif isinstance(response, dict) and "json" in response:
                        sim_id = response["json"].get("id")
                    else:
                        sim_id = "Unknown"
                    console.print(create_success_message(f"Simulation created successfully! ID: {sim_id}"))
                except Exception as e:
                    console.print(create_error_message(f"Failed to create simulation: {e}"))
                
            elif action == "get":
                try:
                    sim_id = int(inquirer.text(
                        message="Simulation ID",
                        style=get_style(INPUT_STYLE)
                    ).execute())
                    
                    client = get_client()
                    simulation = client.simulation.get(sim_id)
                    from .core.utils import format_json_output
                    format_json_output(simulation, f"Simulation {sim_id}")
                except Exception as e:
                    console.print(create_error_message(f"Failed to get simulation: {e}"))
                
            elif action == "start":
                try:
                    sim_id = int(inquirer.text(
                        message="Simulation ID to start",
                        style=get_style(INPUT_STYLE)
                    ).execute())
                    
                    client = get_client()
                    result = client.simulation.start(sim_id)
                    console.print(create_success_message(f"Simulation {sim_id} started successfully"))
                except Exception as e:
                    console.print(create_error_message(f"Failed to start simulation: {e}"))
                
            elif action == "stop":
                try:
                    sim_id = int(inquirer.text(
                        message="Simulation ID to stop",
                        style=get_style(INPUT_STYLE)
                    ).execute())
                    
                    client = get_client()
                    result = client.simulation.stop(sim_id)
                    console.print(create_success_message(f"Simulation {sim_id} stopped successfully"))
                except Exception as e:
                    console.print(create_error_message(f"Failed to stop simulation: {e}"))
                    
        except KeyboardInterrupt:
            break

def kb_menu():
    """knowledge base submenu """
    while True:
        try:
            action = inquirer.select(
                message="Knowledge Base",
                choices=[
                    Choice("list", name="☰ List Files"),
                    Choice("quota", name="∎ Show Quota Status"),
                    Choice("upload", name="⇧ Upload File"),
                    Separator(),
                    Choice("attach", name="⛶ Attach Files to Agent"),
                    Choice("detach", name="⛶✖ Detach Files from Agent"),
                    Separator(),
                    Choice("delete", name="✖ Delete File"),
                    Choice("check-upload", name="✔ Check Upload Eligibility"),
                    Separator(),
                    Choice("back", name="← Back to Main Menu")
                ],
                vi_mode=True,
                style=get_style(MENU_STYLE)
            ).execute()

            if action == "back":
                break
            elif action == "list":
                try:
                    client = get_client()
                    files = client.knowledge_base.list()
                    from .core.utils import create_kb_files_ui
                    console.print()
                    create_kb_files_ui(files)
                    console.print()
                except Exception as e:
                    console.print(create_error_message(f"Failed to list files: {e}"))
            
            elif action == "quota":
                try:
                    console.print(create_section_banner("Knowledge Base Quota Status", "▤"))
                    client = get_client()
                    
                    # using a dummy small file size to get quota information
                    result = client.knowledge_base.can_upload(1024, "pdf")  # 1KB dummy check
                    
                    if isinstance(result, dict):
                        data = result.get("json", result)
                        quota = data.get("quota", {})
                        
                        if quota:
                            from rich.table import Table
                            from rich.panel import Panel
                            
                            quota_table = Table(show_header=True, header_style="bold cyan")
                            quota_table.add_column("Metric", style="cyan", width=15)
                            quota_table.add_column("Value", style="white", width=15)
                            quota_table.add_column("Details", style="dim white")
                            
                            total = quota.get("total", 0)
                            used = quota.get("used", 0)
                            remaining = quota.get("remaining", 0)
                            usage_percent = (used/total*100) if total > 0 else 0
                            
                            # color coding based on usage
                            usage_color = "green" if usage_percent < 70 else "yellow" if usage_percent < 90 else "red"
                            
                            quota_table.add_row("Total Quota", f"{total:.2f} MB", "Maximum storage available")
                            quota_table.add_row("Used", f"{used:.2f} MB", f"Files currently stored")
                            quota_table.add_row("Remaining", f"{remaining:.2f} MB", "Space available for new files")
                            quota_table.add_row("Usage", f"[{usage_color}]{usage_percent:.1f}%[/{usage_color}]", 
                                            f"Percentage of quota used")
                            
                            quota_panel = Panel(
                                quota_table,
                                title="[bold blue]▤ Knowledge Base Quota[/bold blue]",
                                border_style="blue",
                                padding=(1, 2)
                            )
                            
                            console.print()
                            console.print(quota_panel)
                            
                            if usage_percent > 90:
                                console.print(create_warning_message("⚠ Quota nearly full! Consider deleting unused files or upgrading."))
                            elif usage_percent > 70:
                                console.print(create_info_message("ℹ Quota usage is getting high. Monitor your storage."))
                            else:
                                console.print(create_success_message("✔ Plenty of quota remaining for new uploads."))

                            console.print()

                        else:
                            console.print(create_warning_message("No quota information available"))
                    else:
                        console.print(create_error_message("Could not retrieve quota information"))
                        
                except Exception as e:
                    console.print(create_error_message(f"Failed to get quota status: {e}"))
            
            elif action == "upload":
                try:
                    console.print(create_section_banner("Upload File to Knowledge Base", "📤"))

                    # get file path 
                    file_path = inquirer.text(
                        message="Full path to file (e.g., /path/to/document.pdf)",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    # validate file 
                    import os
                    import base64
                    
                    if not os.path.exists(file_path):
                        console.print(create_error_message(f"File not found: {file_path}"))
                        continue
                    
                    if not file_path.lower().endswith('.pdf'):
                        console.print(create_error_message("Only PDF files are currently supported"))
                        continue
                    
                    # check file size
                    file_size = os.path.getsize(file_path)
                    if file_size > 10 * 1024 * 1024:  # 10MB limit
                        console.print(create_error_message("File too large (max 10MB)"))
                        continue
                    
                    # get filename 
                    filename = inquirer.text(
                        message="Filename (or press Enter to use original)",
                        default=os.path.basename(file_path),
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    # check quota before uploading
                    client = get_client()
                    console.print(f"[dim yellow]Checking upload eligibility for {filename} ({file_size/1024:.1f} KB)...[/dim yellow]")
                    
                    try:
                        quota_check = client.knowledge_base.can_upload(file_size, "pdf")
                        if isinstance(quota_check, dict):
                            data = quota_check.get("json", quota_check)
                            success = data.get("success", False)
                            can_upload = data.get("can_upload", success)
                            
                            if not success or not can_upload:
                                message = data.get("message", "Upload not allowed")
                                console.print(create_error_message(f"❌ Cannot upload: {message}"))
                                
                                # show quota if available
                                quota = data.get("quota", {})
                                if quota:
                                    used = quota.get("used", 0)
                                    total = quota.get("total", 0)
                                    console.print(f"[dim]Quota usage: {used:.2f}/{total:.2f} MB[/dim]")
                                continue
                            else:
                                console.print(f"[dim green]✔ Upload allowed - proceeding...[/dim green]")
                    except Exception as e:
                        console.print(create_warning_message(f"Could not check quota, proceeding anyway: {e}"))
                    
                    # upload file
                    console.print(f"[dim yellow]Uploading {filename}...[/dim yellow]")
                    
                    with open(file_path, "rb") as file:
                        file_data = base64.b64encode(file.read()).decode('utf-8')
                    
                    result = client.knowledge_base.create(file_data, filename)
                    
                    if isinstance(result, dict) and "file" in result:
                        file_info = result["file"]
                        file_id = file_info.get("id", "Unknown")
                        console.print(create_success_message(f"File uploaded successfully! ID: {file_id}"))
                    elif isinstance(result, dict) and "json" in result:
                        file_info = result["json"].get("file", {})
                        file_id = file_info.get("id", "Unknown")
                        console.print(create_success_message(f"File uploaded successfully! ID: {file_id}"))
                    else:
                        console.print(create_success_message("File uploaded successfully!"))
                        
                except Exception as e:
                    console.print(create_error_message(f"Failed to upload file: {e}"))
                
            elif action == "delete":
                try:
                    console.print(create_section_banner("Delete File", "🗑️"))
                    
                    from .core.utils import safe_int_input
                    file_id = safe_int_input("File ID to delete", "File ID")
                    
                    confirm = inquirer.confirm(
                        message=f"Are you sure you want to delete file ID {file_id}?",
                        default=False,
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    if confirm:
                        client = get_client()
                        result = client.knowledge_base.delete(file_id)
                        console.print(create_success_message(f"File {file_id} deleted successfully"))
                    else:
                        console.print("[dim yellow]Deletion cancelled[/dim yellow]")
                        
                except Exception as e:
                    console.print(create_error_message(f"Failed to delete file: {e}"))
                
            elif action == "attach":
                try:
                    console.print(create_section_banner("Attach Files", "📎"))
                    
                    from .core.utils import safe_int_input, safe_comma_separated_ids
                    agent_id = safe_int_input("Agent ID", "Agent ID")
                    file_id_list = safe_comma_separated_ids("File IDs (comma-separated)", "File IDs")
                    
                    when_to_use = inquirer.text(
                        message="When to use these files (optional)",
                        default="",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    client = get_client()
                    result = client.knowledge_base.attach(file_id_list, agent_id, when_to_use if when_to_use else None)
                    console.print(create_success_message(f"Files attached to agent {agent_id} successfully"))
                except Exception as e:
                    console.print(create_error_message(f"Failed to attach files: {e}"))
            
            elif action == "detach":
                try:
                    console.print(create_section_banner("Detach Files", "⚠"))
                    
                    from .core.utils import safe_int_input, safe_comma_separated_ids
                    agent_id = safe_int_input("Agent ID", "Agent ID")
                    file_id_list = safe_comma_separated_ids("File IDs to detach (comma-separated)", "File IDs")
                    
                    client = get_client()
                    result = client.knowledge_base.detach(file_id_list, agent_id)
                    console.print(create_success_message(f"Files detached from agent {agent_id} successfully"))
                except Exception as e:
                    console.print(create_error_message(f"Failed to detach files: {e}"))
            
            elif action == "check-upload":
                try:
                    console.print(create_section_banner("Check Upload Eligibility", "✔"))
                    
                    file_path = inquirer.text(
                        message="Path to file to check",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    import os
                    if not os.path.exists(file_path):
                        console.print(create_error_message(f"File not found: {file_path}"))
                        continue
                    
                    file_size = os.path.getsize(file_path)
                    client = get_client()
                    result = client.knowledge_base.can_upload(file_size, "pdf")
                    
                    if isinstance(result, dict):
                        data = result.get("json", result)
                        success = data.get("success", False)
                        can_upload = data.get("can_upload", success)
                        
                        if success and can_upload:
                            console.print(create_success_message(f"✔ File can be uploaded! (Size: {file_size/1024:.1f} KB)"))
                        else:
                            message = data.get("message", "Unknown reason")
                            console.print(create_error_message(f"✖ File cannot be uploaded: {message}"))
                        
                        # show quota information if available
                        quota = data.get("quota", {})
                        if quota:
                            from rich.table import Table
                            quota_table = Table(show_header=True, header_style="bold cyan")
                            quota_table.add_column("Metric", style="cyan")
                            quota_table.add_column("Value", style="white")
                            
                            total = quota.get("total", 0)
                            used = quota.get("used", 0)
                            remaining = quota.get("remaining", 0)
                            
                            quota_table.add_row("Total Quota", f"{total:.2f} MB")
                            quota_table.add_row("Used", f"{used:.2f} MB")
                            quota_table.add_row("Remaining", f"{remaining:.2f} MB")
                            quota_table.add_row("Usage %", f"{(used/total*100):.1f}%" if total > 0 else "0%")
                            
                            console.print("\n📊 Knowledge Base Quota:")
                            console.print(quota_table)
                            console.print()
                    else:
                        console.print(create_info_message("Upload check completed"))
                        
                except Exception as e:
                    console.print(create_error_message(f"Failed to check upload eligibility: {e}"))
                    
        except KeyboardInterrupt:
            break

# TODO: testing
def phone_menu():
    """phone number submenu"""
    while True:
        try:
            action = inquirer.select(
                message="Phone Numbers",
                choices=[
                    Choice("list", name="▤ List Phone Numbers"),
                    Choice("attach", name="⛓ Attach to Agent"),
                    Choice("detach", name="✖ Detach from Agent"),
                    Separator(),
                    Choice("back", name="← Back to Main Menu")
                ],
                vi_mode=True,
                style=get_style(MENU_STYLE)
            ).execute()
            
            if action == "back":
                break
            elif action == "list":
                try:
                    client = get_client()
                    numbers = client.phone_number.list(page=1, page_size=10)
                    from .core.utils import format_json_output
                    format_json_output(numbers, "Phone Numbers")
                except Exception as e:
                    console.print(create_error_message(f"Failed to list phone numbers: {e}"))
                
            elif action == "attach":
                try:
                    console.print(create_section_banner("Attach Phone Number", "�"))
                    
                    from .core.utils import safe_int_input
                    phone_id = safe_int_input("Phone number ID", "Phone Number ID")
                    agent_id = safe_int_input("Agent ID", "Agent ID")
                    
                    client = get_client()
                    result = client.phone_number.attach(phone_id, agent_id)
                    console.print(create_success_message(f"Phone number {phone_id} attached to agent {agent_id}"))
                except Exception as e:
                    console.print(create_error_message(f"Failed to attach phone number: {e}"))
                    
            elif action == "detach":
                try:
                    console.print(create_section_banner("Detach Phone Number", "❌"))
                    
                    from .core.utils import safe_int_input
                    phone_id = safe_int_input("Phone number ID", "Phone Number ID")
                    
                    client = get_client()
                    result = client.phone_number.detach(phone_id)
                    console.print(create_success_message(f"Phone number {phone_id} detached successfully"))
                except Exception as e:
                    console.print(create_error_message(f"Failed to detach phone number: {e}"))
                    
        except KeyboardInterrupt:
            break

def integration_menu():
    """integration menu"""
    while True:
        try:
            action = inquirer.select(
                message="Integrations",
                choices=[
                    Choice("list", name="☰ List User Integrations"),
                    Choice("list-agent", name="⚙ List Agent Integrations"),
                    Separator(),
                    Choice("create-api", name="⊕ Create API Integration"),
                    Choice("create-cal", name="🗓 Create Cal.com Integration"),
                    Choice("create-json", name="☷ Create from JSON File"),
                    Separator(),
                    Choice("attach", name="⎋ Attach to Agent"),
                    Choice("detach", name="✖ Detach from Agent"),
                    Separator(),
                    Choice("back", name="← Back to Main Menu")
                ],
                vi_mode=True,
                style=get_style(MENU_STYLE)
            ).execute()
            
            if action == "back":
                break
                
            elif action == "list":
                try:
                    console.print(create_section_banner("User Integrations", "📋"))
                    client = get_client()
                    integrations = client.integrations.get_user_integrations()
                    
                    if isinstance(integrations, dict):
                        data = integrations.get("json", integrations)
                        if isinstance(data, list) and data:
                            # create a table for integrations
                            table = Table(show_header=True, header_style="bold cyan")
                            table.add_column("ID", style="yellow")
                            table.add_column("Name", style="green")
                            table.add_column("Type", style="blue")
                            table.add_column("URL", style="magenta")
                            
                            for integration in data[:10]:  # show first 10
                                table.add_row(
                                    str(integration.get("id", "")),
                                    integration.get("name", ""),
                                    integration.get("integration_type", ""),
                                    integration.get("url", "")[:50] + "..." if len(integration.get("url", "")) > 50 else integration.get("url", "")
                                )
                            console.print(table)
                        else:
                            console.print(create_info_message("No integrations found"))
                    else:
                        console.print(create_info_message("No integrations found"))
                        
                except Exception as e:
                    console.print(create_error_message(f"Failed to list integrations: {e}"))
                    
            elif action == "list-agent":
                try:
                    console.print(create_section_banner("Agent Integrations", "⎋"))
                    
                    agent_id = int(inquirer.text(
                        message="Enter agent ID",
                        style=get_style(INPUT_STYLE)
                    ).execute())
                    
                    client = get_client()
                    integrations = client.integrations.get_agent_integrations(agent_id)
                    
                    if isinstance(integrations, dict):
                        data = integrations.get("json", integrations)
                        if isinstance(data, list) and data:
                            table = Table(show_header=True, header_style="bold cyan")
                            table.add_column("ID", style="yellow")
                            table.add_column("Name", style="green")
                            table.add_column("Type", style="blue")
                            
                            for integration in data:
                                table.add_row(
                                    str(integration.get("id", "")),
                                    integration.get("name", ""),
                                    integration.get("integration_type", "")
                                )
                            console.print(table)
                        else:
                            console.print(create_info_message(f"No integrations found for agent {agent_id}"))
                    else:
                        console.print(create_info_message(f"No integrations found for agent {agent_id}"))
                        
                except Exception as e:
                    console.print(create_error_message(f"Failed to list agent integrations: {e}"))
            
            elif action == "create-api":
                try:
                    console.print(create_section_banner("Create API Integration", "➕"))
                    
                    name = inquirer.text(
                        message="Integration name",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    url = inquirer.text(
                        message="API URL",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    method = inquirer.select(
                        message="HTTP method",
                        choices=["GET", "POST", "PUT", "DELETE", "PATCH"],
                        style=get_style(MENU_STYLE)
                    ).execute()
                    
                    description = inquirer.text(
                        message="Description (optional)",
                        default="",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    # ask if they want to add headers or query params
                    add_advanced = inquirer.confirm(
                        message="Add headers or query parameters?",
                        default=False,
                        style=get_style(MENU_STYLE)
                    ).execute()
                    
                    headers_list = None
                    query_params_list = None
                    
                    if add_advanced:
                        headers_json = inquirer.text(
                            message="Headers (JSON format, optional)",
                            default="",
                            style=get_style(INPUT_STYLE)
                        ).execute()
                        
                        if headers_json.strip():
                            try:
                                import json
                                headers_list = json.loads(headers_json)
                            except:
                                console.print(create_error_message("Invalid JSON for headers, skipping..."))
                        
                        query_params_json = inquirer.text(
                            message="Query parameters (JSON format, optional)",
                            default="",
                            style=get_style(INPUT_STYLE)
                        ).execute()
                        
                        if query_params_json.strip():
                            try:
                                import json
                                query_params_list = json.loads(query_params_json)
                            except:
                                console.print(create_error_message("Invalid JSON for query params, skipping..."))
                    
                    client = get_client()
                    response = client.integrations.create_custom_api_integration(
                        name=name, 
                        url=url, 
                        method=method,
                        description=description,
                        headers=headers_list,
                        query_params=query_params_list
                    )
                    
                    # extract integration ID correctly
                    integration_id = None
                    if isinstance(response, dict):
                        if "json" in response:
                            integration_id = response["json"].get("integration_id") or response["json"].get("id")
                        else:
                            integration_id = response.get("integration_id") or response.get("id")
                    
                    if integration_id:
                        console.print(create_success_message(f"Integration created successfully! ID: {integration_id}"))
                    else:
                        console.print(create_success_message("Integration created successfully!"))
                        
                except Exception as e:
                    console.print(create_error_message(f"Failed to create integration: {e}"))
                    
            elif action == "create-cal":
                try:
                    console.print(create_section_banner("Create Cal.com Integration", "▤"))
                    
                    name = inquirer.text(
                        message="Integration name",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    cal_api_key = inquirer.secret(
                        message="Cal.com API key",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    cal_id = inquirer.text(
                        message="Cal.com ID",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    cal_timezone = inquirer.text(
                        message="Cal.com timezone",
                        default="America/New_York",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    description = inquirer.text(
                        message="Description (optional)",
                        default="",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    client = get_client()
                    response = client.integrations.create_cal_integration(
                        name=name,
                        cal_api_key=cal_api_key,
                        cal_id=cal_id,
                        cal_timezone=cal_timezone,
                        description=description
                    )
                    
                    integration_id = None
                    if isinstance(response, dict):
                        if "json" in response:
                            integration_id = response["json"].get("integration_id") or response["json"].get("id")
                        else:
                            integration_id = response.get("integration_id") or response.get("id")
                    
                    if integration_id:
                        console.print(create_success_message(f"Cal.com integration created successfully! ID: {integration_id}"))
                    else:
                        console.print(create_success_message("Cal.com integration created successfully!"))
                        
                except Exception as e:
                    console.print(create_error_message(f"Failed to create Cal.com integration: {e}"))
                    
            elif action == "create-json":
                try:
                    console.print(create_section_banner("Create Integration from JSON", "▤"))
                    
                    file_path = inquirer.text(
                        message="Path to JSON file",
                        style=get_style(INPUT_STYLE)
                    ).execute()
                    
                    import json
                    with open(file_path, 'r') as f:
                        integration_data = json.load(f)
                    
                    client = get_client()
                    response = client.integrations.create_integration_from_json(integration_data)
                    
                    integration_id = None
                    if isinstance(response, dict):
                        if "json" in response:
                            integration_id = response["json"].get("integration_id") or response["json"].get("id")
                        else:
                            integration_id = response.get("integration_id") or response.get("id")
                    
                    if integration_id:
                        console.print(create_success_message(f"Integration created successfully! ID: {integration_id}"))
                    else:
                        console.print(create_success_message("Integration created successfully!"))
                        
                except Exception as e:
                    console.print(create_error_message(f"Failed to create integration from JSON: {e}"))
                
            elif action == "attach":
                try:
                    console.print(create_section_banner("Attach Integration", "⛓"))
                    
                    from .core.utils import safe_int_input
                    agent_id = safe_int_input("Agent ID", "Agent ID")
                    integration_id = safe_int_input("Integration ID", "Integration ID")
                    
                    client = get_client()
                    result = client.integrations.add_integration_to_agent(
                        agent_id=agent_id, integration_id=integration_id
                    )
                    console.print(create_success_message(f"Integration {integration_id} attached to agent {agent_id}"))
                except Exception as e:
                    console.print(create_error_message(f"Failed to attach integration: {e}"))
                    
            elif action == "detach":
                try:
                    console.print(create_section_banner("Detach Integration", "✖"))
                    
                    from .core.utils import safe_int_input
                    agent_id = safe_int_input("Agent ID", "Agent ID")
                    integration_id = safe_int_input("Integration ID", "Integration ID")
                    
                    client = get_client()
                    result = client.integrations.remove_integration_from_agent(
                        agent_id=agent_id, integration_id=integration_id
                    )
                    console.print(create_success_message(f"Integration {integration_id} removed from agent {agent_id}"))
                except Exception as e:
                    console.print(create_error_message(f"Failed to detach integration: {e}"))
                    
        except KeyboardInterrupt:
            break

def config_menu():
    """configuration submenu"""
    while True:
        try:
            action = inquirer.select(
                message="Configuration",
                choices=[
                    Choice("show", name="Show Current Config"),
                    Choice("key", name="Set API Key"),
                    Choice("url", name="Set Base URL"),
                    Separator(),
                    Choice("back", name="← Back to Main Menu")
                ],
                vi_mode=True,
                style=get_style(MENU_STYLE)
            ).execute()
            
            if action == "back":
                break
                
            config = CLIConfig()
            
            if action == "show":
                config.show()
            elif action == "key":
                api_key = inquirer.secret(
                    message="Enter API key",
                    style=get_style(INPUT_STYLE)
                ).execute()
                config.set_api_key(api_key)
                console.print(create_success_message("API key updated successfully"))
            elif action == "url":
                url = inquirer.text(
                    message="Base URL",
                    default="https://backend.omnidim.io/api/v1",
                    style=get_style(INPUT_STYLE)
                ).execute()
                config.set_base_url(url)
                console.print(create_success_message("Base URL updated successfully"))
                
        except KeyboardInterrupt:
            break
