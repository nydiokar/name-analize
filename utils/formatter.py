from rich.console import Console
from rich.panel import Panel
from rich.traceback import install
from analyzers.cultural_patterns import CulturalAnalyzer

# Install rich traceback handler
install()

console = Console()

# Initialize LLM mode
USE_LLM = True
try:
    from analyzers.llm_interpreter import NameInterpreter
    interpreter = NameInterpreter()
except Exception as e:
    USE_LLM = False
    console.print(Panel(
        f"[red]Error initializing AI mode:[/red]\n" +
        f"[yellow]{str(e)}[/yellow]\n\n" +
        "[white]Would you like to:[/white]\n" +
        "1. Continue in basic mode\n" +
        "2. Quit and fix Ollama setup",
        title="AI Setup Error"
    ))
    choice = console.input("\nEnter choice [1/2]: ")
    if choice != "1":
        raise SystemExit(1)

def get_challenge_meaning(challenge):
    """Interpret challenge numbers."""
    meanings = {
        1: "self-expression and independence",
        2: "cooperation and sensitivity",
        3: "creativity and social interaction",
        4: "structure and stability",
        5: "freedom and adaptability",
        6: "responsibility and nurturing",
        7: "analysis and understanding",
        8: "material and spiritual balance",
        9: "completion and transformation"
    }
    return meanings.get(challenge, "personal growth")

def format_results(name, report):
    """Format analysis results for display using rich."""    
    # Header with styling
    console.print(Panel(
        f"[bold cyan]Analysis Results for:[/bold cyan] [bold white]{name}[/bold white]",
        style="bold magenta"
    ))
    
    # Technical Analysis Section
    console.print(Panel(
        "\n".join([
            "[bold cyan]Technical Analysis[/bold cyan]",
            "",
            f"[yellow]Destiny Number:[/yellow] {report.get('analyses', {}).get('numerology', {}).get('destiny_number', 'N/A')}",
            f"[yellow]Base Frequency:[/yellow] {report.get('analyses', {}).get('vibration', {}).get('base_frequency', 'N/A')} Hz",
            f"[yellow]Consonants/Vowels:[/yellow] {report.get('analyses', {}).get('phonetics', {}).get('consonant_count', 'N/A')}/{report.get('analyses', {}).get('phonetics', {}).get('vowel_count', 'N/A')}"
        ]),
        title="📊 Metrics",
        border_style="cyan"
    ))
    
    # Interpretation Section
    interpretation = report.get('analyses', {}).get('interpretation', '')
    if interpretation:
        sections = interpretation.split('\n\n')
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            if section.lower().startswith('overall impression'):
                title = "✨ Overall Impression"
            elif section.lower().startswith('key strengths'):
                title = "💪 Key Strengths"
            elif section.lower().startswith('growth areas'):
                title = "🌱 Growth Areas"
            elif section.lower().startswith('life path insights'):
                title = "🌊 Life Path Insights"
            elif section.lower().startswith('deeper analysis'):
                title = "🔮 Deeper Analysis"
            else:
                title = None
            
            if title:
                content = section.split(':', 1)[1].strip() if ':' in section else section
                console.print(f"\n[bold cyan]{title}[/bold cyan]")
                if title in ["💪 Key Strengths", "🌱 Growth Areas"]:
                    for line in content.split('\n'):
                        if line.strip():
                            console.print(f"• {line.strip()}")
                else:
                    console.print(content)
            else:
                console.print(section)

def _print_basic_interpretation(console, numerology, cultural, phonetics):
    """Fallback interpretation when AI is not available."""
    sections = [
        ("✨ Overall Impression", f"Your name's destiny number {numerology['destiny_number']} indicates {get_challenge_meaning(numerology['destiny_number'])}"),
        ("💪 Key Strengths", ["Natural talents based on numerological patterns"]),
        ("🌱 Growth Areas", ["Areas for personal development"]),
        ("🌊 Life Path Insights", cultural['structure_notes'][0] if cultural.get('structure_notes') else 'Path insights not available'),
        ("🔮 Deeper Analysis", cultural['patterns'][0]['meaning'] if cultural.get('patterns') else 'Cultural analysis not available'),
        ("☀️ Vibrational Insight", "Basic vibrational patterns detected")
    ]
    
    for title, content in sections:
        console.print(f"\n[bold cyan]{title}[/bold cyan]")
        if isinstance(content, list):
            for item in content:
                console.print(f"• {item}")
        else:
            console.print(content)
