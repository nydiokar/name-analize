from rich.console import Console
from rich.panel import Panel
import subprocess
import webbrowser
import sys
import platform
import os

console = Console()

def check_openai_api():
    """Check if OpenAI API key is configured."""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        return bool(api_key)
    except:
        return False

def setup_environment():
    """Set up the environment for name analysis tool."""
    console.print(Panel("[bold magenta]Name Analysis Tool Setup[/bold magenta]"))
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        console.print("[red]Error: Python 3.8 or higher is required[/red]")
        return False
    
    # Install requirements
    console.print("\n[cyan]Installing Python requirements...[/cyan]")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error installing requirements: {str(e)}[/red]")
        return False
    
    # Check OpenAI API key
    console.print("\n[cyan]Checking OpenAI API configuration...[/cyan]")
    if not check_openai_api():
        console.print("[yellow]OpenAI API key not found.[/yellow]")
        console.print("\nTo set up OpenAI API:")
        console.print("1. Get your API key from: [blue]https://platform.openai.com/api-keys[/blue]")
        console.print("2. Create a .env file in the project root")
        console.print("3. Add this line to the .env file:")
        console.print("[green]OPENAI_API_KEY=your-api-key-here[/green]")
        return False
    
    console.print("\n[green]Setup completed successfully![/green]")
    console.print("\nYou can now run the tool with:")
    console.print("[cyan]python main.py[/cyan]")
    
    return True

if __name__ == "__main__":
    setup_environment()
