import subprocess
import sys
from rich.console import Console

console = Console()

def install_dependencies():
    """Install all required packages in the correct order."""
    try:
        # First, upgrade pip and install basic requirements
        console.print("[cyan]Upgrading pip and installing basic dependencies...[/cyan]")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools", "wheel"])
        
        # Then install the rest of the requirements
        console.print("[cyan]Installing project requirements...[/cyan]")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        console.print("[green]Successfully installed all dependencies![/green]")
        return True
        
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error installing dependencies: {str(e)}[/red]")
        return False

if __name__ == "__main__":
    install_dependencies() 