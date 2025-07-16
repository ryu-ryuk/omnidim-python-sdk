"""
Shared utilities for CLI
"""
import json
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from typing import List, Dict, Any, Optional, Tuple


console = Console()


def format_file_size(size_bytes: int, compact: bool = False) -> str:
    """Format file size in human-readable format"""
    if compact:
        if size_bytes > 1024*1024:
            return f"{size_bytes/(1024*1024):.1f}M"
        elif size_bytes > 1024:
            return f"{size_bytes/1024:.1f}K"
        else:
            return f"{size_bytes}B"
    else:
        if size_bytes > 1024*1024:
            return f"{size_bytes/(1024*1024):.1f} MB"
        elif size_bytes > 1024:
            return f"{size_bytes/1024:.1f} KB"
        else:
            return f"{size_bytes} B"

def validate_positive_integer(value: str, field_name: str = "ID") -> Tuple[bool, int, str]:
    """
    Validate that a string is a positive integer
    
    Returns:
        Tuple[bool, int, str]: (is_valid, parsed_value, error_message)
    """
    try:
        parsed = int(value)
        if parsed <= 0:
            return False, 0, f"{field_name} must be a positive integer"
        return True, parsed, ""
    except ValueError:
        return False, 0, f"{field_name} must be a valid integer"

def validate_phone_number(phone: str) -> Tuple[bool, str]:
    """
    Basic phone number validation
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not phone:
        return False, "Phone number cannot be empty"
    
    # Remove spaces and dashes for validation
    clean_phone = phone.replace(" ", "").replace("-", "")
    
    # Must start with + for international format
    if not clean_phone.startswith("+"):
        return False, "Phone number must start with + (international format)"
    
    # Check length (minimum 7 digits after +, maximum 15)
    digits_only = clean_phone[1:]  # Remove the +
    if not digits_only.isdigit():
        return False, "Phone number can only contain digits after +"
    
    if len(digits_only) < 7 or len(digits_only) > 15:
        return False, "Phone number must be 7-15 digits after +"
    
    return True, ""

def safe_int_input(prompt: str, field_name: str = "ID") -> int:
    """
    Safely get integer input with validation and retry
    """
    from InquirerPy import inquirer
    from InquirerPy.utils import get_style
    
    INPUT_STYLE = {
        "questionmark": "#cba6f7 bold",
        "question": "#cdd6f4 bold",
        "answer": "#a6e3a1 bold",
    }
    
    while True:
        value = inquirer.text(
            message=prompt,
            style=get_style(INPUT_STYLE)
        ).execute()
        
        is_valid, parsed_value, error_msg = validate_positive_integer(value, field_name)
        if is_valid:
            return parsed_value
        else:
            console.print(f"[red]❌ {error_msg}. Please try again.[/red]")

def safe_phone_input(prompt: str) -> str:
    """
    Safely get phone number input with validation and retry
    """
    from InquirerPy import inquirer
    from InquirerPy.utils import get_style
    
    INPUT_STYLE = {
        "questionmark": "#cba6f7 bold",
        "question": "#cdd6f4 bold",
        "answer": "#a6e3a1 bold",
    }
    
    while True:
        value = inquirer.text(
            message=prompt,
            style=get_style(INPUT_STYLE)
        ).execute()
        
        is_valid, error_msg = validate_phone_number(value)
        if is_valid:
            return value
        else:
            console.print(f"[red]❌ {error_msg}. Please try again.[/red]")

def extract_id_from_response(response, id_field="id"):
    """
    Extract ID from standard SDK response format
    
    Args:
        response: SDK response object 
        id_field: Name of the ID field to extract (default: "id")
        
    Returns:
        The extracted ID or None if not found
    """
    if isinstance(response, dict):
        return response.get("json", {}).get(id_field)
    return None

def format_json_output(data: Any, title: str = None):
    """format and display JSON data"""
    if title:
        console.print(f"\n[bold cyan]{title}[/bold cyan]")
    
    if isinstance(data, dict) and 'json' in data:
        console.print_json(data=data['json'])
    else:
        console.print_json(data=data)

def create_agents_table(agents: List[Dict], client=None, show_details: bool = False) -> Table:
    """create table for displaying agents with optional detailed info"""
    table = Table(show_header=True, header_style="bold #cba6f7")  # mauve
    table.add_column("ID", style="#89b4fa", width=6)  # blue
    table.add_column("Name", style="#a6e3a1", min_width=15)  # green
    table.add_column("Model", style="#f9e2af", width=12)  # yellow
    table.add_column("Voice", style="#f5c2e7", width=12)  # pink
    table.add_column("Status", style="#94e2d5", width=10)  # teal
    
    if show_details:
        table.add_column("Features", style="#fab387", min_width=20)  # peach
        table.add_column("ASR", style="#89dceb", width=12)  # sky
        table.add_column("Context", style="#cba6f7", width=8)  # lavender
        table.add_column("Files", style="#f38ba8", width=6)  # red
        table.add_column("Integrations", style="#a6e3a1", width=8)  # green
        table.add_column("Welcome", style="#cdd6f4", min_width=25)  # text

    for i, agent in enumerate(agents):
        # delaying to handle rate limit
        if show_details and client and i > 0:
            time.sleep(0.2)  # 200ms
            
        voice_provider = agent.get("voice_provider", "")
        voice_id = agent.get("voice_external_id", agent.get("voice", ""))
        
        if voice_id and str(voice_id) != "false":
            if len(str(voice_id)) > 8:
                voice_info = f"{voice_provider} ({str(voice_id)[:6]}...)"
            else:
                voice_info = f"{voice_provider} ({voice_id})"
        else:
            voice_info = voice_provider or "None"
        
        status = agent.get("status_of_building_flow", "Unknown")
        if status.lower() == "completed":
            status_display = f"[green]{status}[/green]"
        elif "building" in status.lower():
            status_display = f"[yellow]{status}[/yellow]"
        else:
            status_display = f"[red]{status}[/red]"
        
        row_data = [
            str(agent.get("id", "")),
            agent.get("name", "Unknown"),
            agent.get("llm_service", "Unknown"),
            voice_info,
            status_display
        ]
        
        if show_details and client:
            features_info = "Basic"
            asr_info = "Unknown"
            context_count = "0"
            files_count = "0"
            integrations_count = "0"
            welcome_msg = "N/A"
            
            try:
                agent_details = client.agent.get(agent.get("id"))
                
                # Parse agent details
                detail_data = None
                if isinstance(agent_details, dict):
                    if 'json' in agent_details:
                        detail_data = agent_details['json']
                    else:
                        detail_data = agent_details
                else:
                    try:
                        detail_data = getattr(agent_details, 'json', agent_details)
                    except:
                        detail_data = agent_details
                
                if detail_data and isinstance(detail_data, dict):
                    # Features analysis
                    features = []
                    if detail_data.get("enable_web_search"):
                        search_engine = detail_data.get("web_search_engine", "default")
                        features.append(f"Web({search_engine})")
                    if detail_data.get("filler_enable") or detail_data.get("is_filler_enable"):
                        filler_delay = detail_data.get("filler_after_sec", 0)
                        features.append(f"Filler({filler_delay}s)")
                    if detail_data.get("is_transfer_enabled"):
                        transfer_count = len(detail_data.get("transfer_options", []))
                        features.append(f"Transfer({transfer_count})")
                    if detail_data.get("is_end_call_enabled"):
                        features.append("EndCall")
                    if detail_data.get("should_apply_noise_reduction"):
                        features.append("NoiseRed")
                    
                    features_info = " • ".join(features) if features else "Basic"
                    if len(features_info) > 18:
                        features_info = features_info[:15] + "..."
                    
                    # ASR info
                    asr_service = detail_data.get("asr_service", "Unknown")
                    asr_lang = detail_data.get("asr_deepgram_language", detail_data.get("asr_cartesia_language", ""))
                    if asr_lang:
                        asr_info = f"{asr_service} ({asr_lang})"
                    else:
                        asr_info = asr_service
                    if len(asr_info) > 10:
                        asr_info = asr_info[:7] + "..."
                    
                    # Context count
                    context_breakdown = detail_data.get("context_breakdown", [])
                    active_contexts = [c for c in context_breakdown if c.get("is_enabled", True)]
                    context_count = f"{len(active_contexts)}/{len(context_breakdown)}" if context_breakdown else "0"
                    
                    # Files count
                    attached_files = detail_data.get("attach_file_ids", [])
                    files_count = str(len(attached_files)) if attached_files else "0"
                    
                    # Integrations count
                    integrations_list = detail_data.get("integrations", [])
                    integration_ids = detail_data.get("integration_ids", [])
                    total_integrations = len(integrations_list) + len(integration_ids)
                    integrations_count = str(total_integrations) if total_integrations > 0 else "0"
                    
                    # Welcome message
                    welcome_msg = detail_data.get("welcome_message", "N/A")
                    if not welcome_msg or welcome_msg == "false" or welcome_msg is False:
                        welcome_msg = "[dim]Not set[/dim]"
                    elif len(str(welcome_msg)) > 22:
                        welcome_msg = str(welcome_msg)[:19] + "..."
                else:
                    welcome_msg = "Error parsing"
                    
            except Exception as e:
                features_info = "Error"
                asr_info = "Error"
                context_count = "?"
                files_count = "?"
                integrations_count = "?"
                welcome_msg = "Error fetching"
                console.print(f"[dim red]Warning: Could not fetch details for agent {agent.get('id')}: {e}[/dim red]")
            
            row_data.extend([
                features_info,
                asr_info,
                context_count,
                files_count,
                integrations_count,
                welcome_msg
            ])
        
        table.add_row(*row_data)

    return table


def create_calls_table(calls: List[Dict]) -> Table:
    """table for displaying calls"""
    table = Table(show_header=True, header_style="bold #cba6f7")  # mauve
    table.add_column("ID", style="#89b4fa", width=8)  # blue
    table.add_column("Agent", style="#a6e3a1", width=15)  # green
    table.add_column("To Number", style="#89dceb", width=15)  # sky
    table.add_column("Status", style="#f9e2af", width=12)  # yellow
    table.add_column("Duration", style="#bac2de", width=10)  # subtext1
    table.add_column("Date", style="#a6adc8", width=12)  # subtext0

    for call in calls:
        duration = call.get("duration", call.get("call_duration", 0))
        if duration:
            duration_str = f"{duration}s"
        else:
            duration_str = "N/A"
            
        # get agent name or ID
        agent_info = call.get("agent_name", call.get("agent_id", "Unknown"))
        
        # format date
        date_str = ""
        if call.get("created_at"):
            date_str = call.get("created_at")[:10]
        elif call.get("start_time"):
            date_str = call.get("start_time")[:10]

        table.add_row(
            str(call.get("id", "")),
            str(agent_info),
            call.get("to_number", call.get("phone_number", "")),
            call.get("status", call.get("call_status", "")),
            duration_str,
            date_str
        )

    return table

def create_simulations_table(simulations: List[Dict]) -> Table:
    """Create table for displaying simulations"""
    table = Table(show_header=True, header_style="bold #cba6f7")  # mauve
    table.add_column("ID", style="#89b4fa", width=8)  # blue
    table.add_column("Name", style="#a6e3a1")  # green
    table.add_column("Agent ID", style="#89dceb", width=10)  # sky
    table.add_column("Status", style="#f9e2af", width=15)  # yellow
    table.add_column("Calls", style="#bac2de", width=8)  # subtext1

    for sim in simulations:
        table.add_row(
            str(sim.get("id", "")),
            sim.get("name", ""),
            str(sim.get("agent_id", "")),
            sim.get("status", ""),
            str(sim.get("number_of_call_to_make", ""))
        )

    return table

def validate_json_input(json_str: str) -> tuple[bool, Any]:
    """Validate JSON input"""
    try:
        data = json.loads(json_str)
        return True, data
    except json.JSONDecodeError as e:
        return False, str(e)

def create_agent_details_ui(agent_data, client=None):
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    
    # fetch fresh data from API if needed
    if client and isinstance(agent_data, (str, int)):
        try:
            agent_id = str(agent_data)
            fresh_data = client.agent.get(agent_id)
            
            if isinstance(fresh_data, dict):
                if 'json' in fresh_data:
                    agent_data = fresh_data['json']
                else:
                    agent_data = fresh_data
            else:
                try:
                    agent_data = getattr(fresh_data, 'json', fresh_data)
                except:
                    agent_data = fresh_data
                    
        except Exception as e:
            console.print(f"[dim red]Warning: Could not fetch fresh agent data: {e}[/dim red]")
            if not isinstance(agent_data, dict):
                console.print("[bold red]!! Error: Invalid agent data provided[/bold red]")
                return
    
    if isinstance(agent_data, dict):
        if 'json' in agent_data:
            agent = agent_data['json']
        else:
            agent = agent_data
    else:
        agent = agent_data
    
    # a single consolidated table with all information
    main_table = Table.grid(padding=(0, 2))
    main_table.add_column(style="bold cyan", min_width=15)
    main_table.add_column(style="white")
    
    main_table.add_row(
        "[bold blue]∑ AGENT OVERVIEW[/bold blue]",
        ""
    )
    main_table.add_row("", "")
    
    # basics
    # status = agent.get("status_of_building_flow", "Unknown")
    # status_color = "green" if status.lower() == "completed" else "yellow" if "building" in status.lower() else "red"
    # status_display = f"[{status_color}]{status}[/{status_color}]"
    
    main_table.add_row("ID", f"{agent.get('id', 'N/A')}")
    main_table.add_row("Name", f"{agent.get('name', 'Unknown')}")
    main_table.add_row("Type", f"{agent.get('bot_type', 'prompt')}")
    # main_table.add_row("Status", status_display)
    main_table.add_row("Call Type", f"{agent.get('bot_call_type', agent.get('call_type', 'N/A'))}")
    
    # Bot action ID if available
    bot_action_id = agent.get("bot_action_id")
    if bot_action_id and bot_action_id != "false" and bot_action_id is not False:
        main_table.add_row("Bot Action ID", f"{bot_action_id}")
    
    # langs
    languages = agent.get("languages", [])
    if languages:
        main_table.add_row("Languages", f"{', '.join(languages)}")
    
    secret_key = agent.get("secret_key", "")
    secret_display = f"{secret_key[:12]}..." if secret_key else "Not set"
    main_table.add_row("Secret Key", f"[dim]{secret_display}[/dim]")
    
    # AI config
    main_table.add_row("", "") 
    main_table.add_row(
        "[bold green]� AI CONFIGURATION[/bold green]",
        ""
    )
    main_table.add_row("", "")
    
    # LLM details
    llm_service = agent.get("llm_service", "Unknown")
    temperature = agent.get("llm_temperature", "0.7")
    streaming = agent.get("llm_straming_enabled", False)
    
    main_table.add_row("Model", f"{llm_service}")
    main_table.add_row("Temperature", f"{temperature}")
    main_table.add_row("Streaming", "[green]✓[/green]" if streaming else "[red]✗[/red]")
    
    # voice config
    voice_provider = agent.get("voice_provider", "Unknown")
    voice_id = agent.get("voice_external_id", "")
    
    main_table.add_row("Voice Provider", voice_provider)
    if voice_id and voice_id != "None":
        main_table.add_row("Voice ID", f"[dim]{voice_id}[/dim]")
    
    # ASR config
    asr_service = agent.get("asr_service", "Unknown")
    main_table.add_row("Speech-to-Text", asr_service)
    
    # Provider-specific ASR settings
    if asr_service == "deepgram_stream":
        asr_lang = agent.get("asr_deepgram_language", "")
        asr_model = agent.get("asr_deepgram_model", "")
        if asr_lang:
            main_table.add_row("ASR Language", asr_lang)
        if asr_model:
            main_table.add_row("ASR Model", asr_model)
        
        # Deepgram features
        asr_features = []
        if agent.get("asr_deepgram_numerals"):
            asr_features.append("numerals")
        if agent.get("asr_deepgram_punctuate"):
            asr_features.append("punctuate")
        if agent.get("asr_deepgram_smart_format"):
            asr_features.append("smart-format")
        if agent.get("asr_deepgram_diarize"):
            asr_features.append("diarize")
        if asr_features:
            main_table.add_row("ASR Features", "[dim]" + " • ".join(asr_features) + "[/dim]")
    
    elif asr_service == "cartesia":
        asr_lang = agent.get("asr_cartesia_language", "")
        asr_model = agent.get("asr_cartesia_model", "")
        if asr_lang:
            main_table.add_row("ASR Language", asr_lang)
        if asr_model:
            main_table.add_row("ASR Model", asr_model)
    
    elif asr_service == "sarvam":
        asr_lang = agent.get("asr_sarvam_language", "")
        asr_model = agent.get("asr_sarvam_model", "")
        if asr_lang and asr_lang != "unknown":
            main_table.add_row("ASR Language", asr_lang)
        if asr_model:
            main_table.add_row("ASR Model", asr_model)
    
    main_table.add_row("", "")  
    main_table.add_row(
        "[bold yellow]⚙ FEATURES & SETTINGS[/bold yellow]",
        ""
    )
    main_table.add_row("", "")  
    
    # active features
    features = []
    if agent.get("enable_web_search"):
        search_engine = agent.get("web_search_engine", "default")
        if search_engine and search_engine != "false":
            features.append(f"Web Search ({search_engine})")
        else:
            features.append("Web Search (enabled)")
    
    # filler config
    filler_enabled = agent.get("filler_enable", agent.get("is_filler_enable", False))
    if filler_enabled:
        filler_delay = agent.get("filler_after_sec", 0)
        features.append(f"Fillers ({filler_delay}s delay)")
        
        # show filler details if available
        fillers = agent.get("fillers")
        if fillers and fillers != "false":
            main_table.add_row("Filler Details", f"[dim]Custom fillers configured[/dim]")
    
    if agent.get("is_transfer_enabled"):
        transfer_options = agent.get("transfer_options", [])
        transfer_count = len(transfer_options)
        features.append(f"Transfer ({transfer_count} options)")
        
        # show transfer options details
        if transfer_options:
            for i, option in enumerate(transfer_options[:3]):  # Show first 3
                option_display = str(option) if isinstance(option, str) else f"Option {i+1}"
                label = "" if i > 0 else "Transfer Options"
                main_table.add_row(label, f"[dim]• {option_display}[/dim]")
    
    if agent.get("is_end_call_enabled"):
        features.append("Auto End Call")
        end_call_condition = agent.get("end_call_condition")
        end_call_message = agent.get("end_call_message")
        if end_call_condition and end_call_condition != "false":
            main_table.add_row("End Call Condition", f"[dim]{end_call_condition}[/dim]")
        if end_call_message and end_call_message != "false":
            main_table.add_row("End Call Message", f"[dim]{end_call_message}[/dim]")
    
    if agent.get("should_apply_noise_reduction"):
        features.append("Noise Reduction")

    if features:
        main_table.add_row("Active Features", 
                        "\n".join([f"[green]• {f}[/green]" for f in features]))
    else:
        main_table.add_row("Active Features", "[dim]Basic features only[/dim]")

    # timeout settings
    silence_timeout = agent.get("silence_timeout", 600)
    speech_timeout = agent.get("speech_start_timeout", 150)
    main_table.add_row("Timeouts", f"Silence: {silence_timeout}s, Speech: {speech_timeout}s")
    
    main_table.add_row("", "") 
    main_table.add_row(
        "[bold bright_magenta]¶ KNOWLEDGE BASE[/bold bright_magenta]",
        ""
    )
    main_table.add_row("", "")
    
    # context breakdown
    context_breakdown = agent.get("context_breakdown", [])
    if context_breakdown:
        active_contexts = [c for c in context_breakdown if c.get("is_enabled", True)]
        main_table.add_row("Contexts", f"{len(active_contexts)}/{len(context_breakdown)} active")
        
        for i, context in enumerate(active_contexts[:3]):  # first 3 in details
            context_title = context.get("context_title", "Untitled")
            context_id = context.get("id", "")
            is_enabled = context.get("is_enabled", True)
            status_icon = "✓" if is_enabled else "✗"
            status_color = "green" if is_enabled else "red"
            
            label = "" if i > 0 else "Context Details"
            main_table.add_row(label, f"[{status_color}]{status_icon}[/{status_color}] {context_title} [dim](#{context_id})[/dim]")
            
            # show context body preview
            context_body = context.get("context_body", "")
            if context_body:
                body_preview = context_body[:80] + "..." if len(context_body) > 80 else context_body
                main_table.add_row("", f"[dim]└─ {body_preview}[/dim]")
        
        if len(active_contexts) > 3:
            main_table.add_row("", f"[dim]... +{len(active_contexts) - 3} more contexts[/dim]")
    else:
        main_table.add_row("Contexts", "[dim]None configured[/dim]")
    
    # raw context field (if different from breakdown)
    raw_context = agent.get("context", "")
    if raw_context and raw_context.strip() and raw_context != " \n < Test > \n body\n </ Test > \n":
        # Only show if it's not just the default context pattern
        context_preview = raw_context[:100] + "..." if len(raw_context) > 100 else raw_context
        main_table.add_row("Raw Context", f"[dim]{context_preview}[/dim]")

    attached_files = agent.get("attach_file_ids", [])
    if attached_files:
        main_table.add_row("Attached Files", f"{len(attached_files)} files")
        file_ids = ', '.join(map(str, attached_files[:5]))
        if len(attached_files) > 5:
            file_ids += f", ... +{len(attached_files) - 5} more"
        main_table.add_row("File IDs", f"[dim]{file_ids}[/dim]")
        
        # File access description
        file_access_desc = agent.get("attach_file_access_description")
        if file_access_desc and file_access_desc != "false":
            main_table.add_row("File Access Desc", f"[dim]{file_access_desc}[/dim]")
    else:
        main_table.add_row("Attached Files", "[dim]None attached[/dim]")

    dynamic_vars = agent.get("dynamic_variables", [])
    if dynamic_vars:
        main_table.add_row("Variables", f"{len(dynamic_vars)} configured")
    
    flow_data = agent.get("flow_data")
    if flow_data and flow_data != "false":
        main_table.add_row("", "")
        main_table.add_row(
            "[bold bright_yellow]∴ FLOW CONFIGURATION[/bold bright_yellow]",
            ""
        )
        main_table.add_row("", "") 
        main_table.add_row("Flow Data", "[green]Configured[/green]")
        main_table.add_row("Build Status", agent.get("status_of_building_flow", "Unknown"))
    
    main_table.add_row("", "")
    main_table.add_row(
        "[bold bright_cyan]∞ INTEGRATIONS[/bold bright_cyan]",
        ""
    )
    main_table.add_row("", "")
    
    integrations_list = agent.get("integrations", [])
    integration_ids = agent.get("integration_ids", [])
    
    if integrations_list:
        main_table.add_row("Active Integrations", f"{len(integrations_list)} integrations")
        for i, integration in enumerate(integrations_list[:3]):  # first 3
            int_name = integration.get("name", "Unnamed")
            int_type = integration.get("integration_type", "unknown")
            int_id = integration.get("id", "")
            label = "" if i > 0 else "Integration List"
            main_table.add_row(label, f"[dim]• {int_name} ({int_type}) #{int_id}[/dim]")
        if len(integrations_list) > 3:
            main_table.add_row("", f"[dim]... +{len(integrations_list) - 3} more[/dim]")
    elif integration_ids:
        main_table.add_row("Configured IDs", f"{len(integration_ids)} integrations")
        main_table.add_row("", f"[dim]{', '.join(map(str, integration_ids))}[/dim]")
    else:
        main_table.add_row("Integrations", "[dim]None configured[/dim]")

    # post-call configurations
    post_call_configs = agent.get("post_call_config_ids", [])
    if post_call_configs:
        main_table.add_row("Post-call Configs", f"{len(post_call_configs)} configurations")
    
    widget_config = agent.get("widget_config", {})
    if widget_config:
        main_table.add_row("", "") 
        main_table.add_row(
            "[bold bright_blue]⊕ WIDGET CONFIGURATION[/bold bright_blue]",
            ""
        )
        main_table.add_row("", "") 

        widget_title = widget_config.get("title", "")
        widget_type = widget_config.get("widgetType", "")
        widget_position = widget_config.get("position", "")
        widget_size = f"{widget_config.get('iframeWidth', '')} × {widget_config.get('iframeHeight', '')}"
        
        if widget_title:
            main_table.add_row("Widget Title", widget_title)
        if widget_type:
            main_table.add_row("Widget Type", widget_type)
        if widget_position:
            main_table.add_row("Position", widget_position)
        if widget_size.strip(" ×"):
            main_table.add_row("Size", widget_size)
        
        widget_background = widget_config.get("background", "")
        widget_text_color = widget_config.get("textColor", "")
        if widget_background:
            main_table.add_row("Background", widget_background)
        if widget_text_color:
            main_table.add_row("Text Color", widget_text_color)
    
    welcome = agent.get("welcome_message", "")
    if welcome and welcome != "false" and welcome is not False:
        main_table.add_row("", "") 
        main_table.add_row(
            "[bold bright_green]✎ WELCOME MESSAGE[/bold bright_green]",
            ""
        )
        main_table.add_row("", "") 
        main_table.add_row("Message", f"[italic]{welcome}[/italic]")
    
    # display the consolidated panel
    consolidated_panel = Panel(
        main_table,
        title="[bold blue]⌨ Agent Details[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    )
    
    console.print(consolidated_panel)


def create_knowledge_base_table(files: List[Dict]) -> Table:
    table = Table(show_header=True, header_style="bold #cba6f7")
    table.add_column("ID", style="#89b4fa", width=8, justify="right")
    table.add_column("Name", style="#a6e3a1", min_width=20, max_width=25)
    table.add_column("Size", style="#f9e2af", width=10, justify="right")
    table.add_column("Type", style="#f5c2e7", width=6, justify="center")
    table.add_column("Status", style="#94e2d5", width=8, justify="center")
    table.add_column("Uploaded", style="#cdd6f4", width=10, justify="center")
    table.add_column("Download", style="#fab387", min_width=15, max_width=40)

    for file in files:
        # format file size
        size_bytes = file.get('file_size', 0)
        size_str = format_file_size(size_bytes, compact=True)
        
        mime_type = file.get('mime_type', 'unknown')
        if 'pdf' in mime_type:
            type_display = "PDF"
        elif 'image' in mime_type:
            type_display = "IMG"
        elif 'text' in mime_type:
            type_display = "TXT"
        else:
            type_display = mime_type.split('/')[-1].upper()[:4]  # truncate to 4 chars
        
        # format upload date - shorter format
        upload_date = file.get('upload_date', 'Unknown')
        if upload_date != 'Unknown':
            try:
                # convert MM/DD/YYYY HH:MM:SS to just MM/DD/YY
                date_parts = upload_date.split(' ')
                if len(date_parts) >= 1:
                    date_part = date_parts[0]
                    if '/' in date_part:
                        month, day, year = date_part.split('/')
                        upload_date = f"{month}/{day}/{year[-2:]}"  # Use 2-digit year
            except:
                pass
        
        # status - simplified and shorter
        status = file.get('upload_status', 'unknown')
        status_display = "✓ OK" if status == 'uploaded' else f"⚠ {status[:4]}"
        
        # Download URL - make it clickable and truncated
        download_url = file.get('download_url', '')
        if download_url:
            # Create a clickable link with a shortened display
            if len(download_url) > 35:
                display_url = download_url[:32] + "..."
            else:
                display_url = download_url
            download_display = f"[link={download_url}][blue underline]{display_url}[/blue underline][/link]"
        else:
            download_display = "[dim]No URL[/dim]"
        
        table.add_row(
            str(file.get('id', '')),
            file.get('name', 'Unknown'),
            size_str,
            type_display,
            status_display,
            upload_date,
            download_display
        )
    
    return table


def create_kb_files_ui(kb_data):
    if isinstance(kb_data, dict):
        if 'json' in kb_data:
            data = kb_data['json']
        else:
            data = kb_data
    else:
        data = kb_data
    
    files = data.get("files", [])
    
    if not files:
        console.print(Panel(
            Text("No files found in the knowledge base", style="#6c7086"),
            title="[#f9e2af]Knowledge Base Files[/#f9e2af]",
            border_style="#f9e2af",
            padding=(1, 2)
        ))
        return
    
    # use the table that includes download links
    table = create_knowledge_base_table(files)
    
    # summary info
    total_files = len(files)
    total_size = sum(f.get("file_size", 0) for f in files)
    total_size_str = format_file_size(total_size)
    
    summary_text = Text.assemble(
        "📊 Total Files: ", Text(str(total_files), style="bold #a6e3a1"),
        "  •  ",
        "💾 Total Size: ", Text(total_size_str, style="bold #f9e2af"),
    )
    
    summary_panel = Panel(
        Align.center(summary_text),
        title="[#94e2d5]Knowledge Base Summary[/#94e2d5]",
        border_style="#94e2d5",
        padding=(0, 2)
    )
    
    # display everything
    console.print(summary_panel)
    console.print()
    console.print(table)
    
    note_text = Text.assemble(
        "💡 ", Text("Tip: ", style="bold #f9e2af"),
        "Click on the download links to access files directly.\n",
    )
    note_panel = Panel(
        note_text,
        title="[#89b4fa]Download Info[/#89b4fa]",
        border_style="#89b4fa",
        padding=(0, 2)
    )
    console.print()
    console.print(note_panel)

def safe_comma_separated_ids(prompt: str, field_name: str = "IDs") -> list:
    """
    Safely get comma-separated integer IDs with validation
    """
    from InquirerPy import inquirer
    from InquirerPy.utils import get_style
    
    INPUT_STYLE = {
        "questionmark": "#cba6f7 bold",
        "question": "#cdd6f4 bold",
        "answer": "#a6e3a1 bold",
    }
    
    while True:
        value = inquirer.text(
            message=prompt,
            style=get_style(INPUT_STYLE)
        ).execute()
        
        try:
            ids = [int(id_str.strip()) for id_str in value.split(",")]
            if all(id_val > 0 for id_val in ids):
                return ids
            else:
                console.print(f"[red]✖ All {field_name} must be positive integers. Please try again.[/red]")
        except ValueError:
            console.print(f"[red]✖ {field_name} must be comma-separated integers (e.g., 1,2,3). Please try again.[/red]")
