"""
CLI configuration management
"""
import os
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

class CLIConfig:
    def __init__(self):
        self.config_dir = Path.home() / ".omnidim"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        
    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def save_config(self, config):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            console.print(f"[red]Error saving config: {e}[/red]")
            return False
    
    def get_api_key(self):
        api_key = os.getenv("OMNIDIM_API_KEY") or os.getenv("OMNIDIMENSION_API_KEY")
        if api_key:
            return api_key
            
        config = self.load_config()
        return config.get("api_key")
    
    def set_api_key(self, api_key):
        config = self.load_config()
        config["api_key"] = api_key
        if self.save_config(config):
            console.print("[green]API key saved[/green]")
            return True
        return False
    
    def get_base_url(self):
        config = self.load_config()
        return config.get("base_url", "https://backend.omnidim.io/api/v1")
    
    def set_base_url(self, url):
        config = self.load_config()
        config["base_url"] = url
        if self.save_config(config):
            console.print(f"[green]Base URL set to: {url}[/green]")
            return True
        return False
    
    def show(self):
        config = self.load_config()
        api_key = self.get_api_key()
        
        config_display = {
            "API Key": "***" + api_key[-8:] if api_key and len(api_key) > 8 else "Not set",
            "Base URL": config.get("base_url", "Default"),
            "Config File": str(self.config_file)
        }
        
        console.print(Panel.fit(
            "\n".join([f"[bold]{k}:[/bold] {v}" for k, v in config_display.items()]),
            title="CLI Configuration",
            border_style="cyan"
        ))
