from rich.console import Console
from rich.panel import Panel
import subprocess
import sys
import os
import requests
from install import install_dependencies

console = Console()

def check_llm_configuration():
    """Check LLM configuration."""
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            console.print("[yellow]OpenAI API key not found.[/yellow]")
            console.print("Add to .env file: OPENAI_API_KEY=your-api-key-here")
            return False
    elif provider == "ollama":
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code != 200:
                console.print("[yellow]Ollama service not running.[/yellow]")
                console.print("Start Ollama service before running the tool.")
                return False
        except:
            console.print("[yellow]Ollama service not accessible.[/yellow]")
            console.print("Make sure Ollama is installed and running.")
            return False
    else:
        console.print(f"[red]Unsupported LLM provider: {provider}[/red]")
        return False
    
    return True

def setup_environment():
    """Set up the environment for name analysis tool."""
    console.print(Panel("[bold magenta]Name Analysis Tool Setup[/bold magenta]"))
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        console.print("[red]Error: Python 3.8 or higher is required[/red]")
        return False
    
    # Install dependencies using the new install script
    if not install_dependencies():
        return False
    
    # Check LLM configuration
    console.print("\n[cyan]Checking LLM configuration...[/cyan]")
    if not check_llm_configuration():
        return False
    
    console.print("\n[green]Setup completed successfully![/green]")
    console.print("\nYou can now run the tool with:")
    console.print("[cyan]streamlit run app.py[/cyan]")
    
    return True

if __name__ == "__main__":
    setup_environment()
