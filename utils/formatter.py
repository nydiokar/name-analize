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

def format_results(name, numerology, phonetics, frequency, vibration=None, interpretation=None):
    """Format analysis results for display using rich."""    
    # Get cultural analysis
    cultural = CulturalAnalyzer.analyze_cultural_elements(name)
    
    # Header
    console.print(Panel(f"Analysis Results for: {name}", style="bold magenta"))
    
    # Core Numbers
    console.print("\n[bold cyan]Core Numbers[/bold cyan]")
    console.print(f"Destiny Number: [green]{numerology['destiny_number']}[/green]")
    
    if numerology.get('is_master_number'):
        console.print(f"[bold yellow]Master Number Detected: {numerology['master_number_meaning']}[/bold yellow]")
    
    if numerology.get('karmic_debt'):
        console.print(f"[bold red]Karmic Debt: {numerology['karmic_debt']['number']}[/bold red]")
    
    # Cultural Elements
    if cultural['patterns'] or cultural['dominant_culture']:
        console.print("\n[bold cyan]Cultural Essence[/bold cyan]")
        if cultural['dominant_culture']:
            console.print(f"Primary Heritage: [green]{cultural['dominant_culture'].title()}[/green]")
        for pattern in cultural['patterns']:
            if isinstance(pattern['meaning'], tuple):
                console.print(f"Pattern: [green]{pattern['pattern']}[/green] - {pattern['meaning'][1]}")
            else:
                console.print(f"Pattern: [green]{pattern['pattern']}[/green] - {pattern['meaning']}")
    
    # Name Structure
    console.print("\n[bold cyan]Name Structure[/bold cyan]")
    syllables = phonetics['phonetic_description']['syllable_count']
    balance = phonetics['phonetic_description']['sound_balance']
    console.print(f"Composition: [green]{syllables} syllables with {balance}[/green]")
    
    if cultural['structure_notes']:
        for note in cultural['structure_notes']:
            console.print(f"Pattern: [green]{note}[/green]")
    
    # Letter Distribution
    console.print("\n[bold cyan]Letter Pattern[/bold cyan]")
    console.print(frequency['visualization'])
    
    # Vibration Analysis (if provided)
    if vibration:
        console.print("\n[bold cyan]Vibrational Analysis[/bold cyan]")
        for key, value in vibration.items():
            console.print(f"{key}: [green]{value}[/green]")
    
    # Display interpretation if provided directly
    if interpretation:
        console.print("\n[bold magenta]Name Interpretation[/bold magenta]")
        console.print(Panel("\n\n".join(interpretation), style="bold white"))
    else:
        # Generate interpretation using existing logic
        console.print("\n[bold magenta]Name Interpretation[/bold magenta]")
        try:
            if USE_LLM:
                # Prepare analysis data
                analysis_data = {
                    'name': name,
                    'numerology': {
                        'destiny': numerology['destiny_number'],
                        'is_master': numerology.get('is_master_number', False),
                        'master_meaning': numerology.get('master_number_meaning', None),
                        'karmic_debt': numerology.get('karmic_debt', None)
                    },
                    'cultural_roots': cultural['cultural_roots'],
                    'phonetics': {
                        'syllables': syllables,
                        'balance': balance,
                        'patterns': cultural['structure_notes']
                    },
                    'special_meanings': cultural.get('special_meanings', [])
                }
                
                # Generate AI interpretation
                interpretations = interpreter.generate_interpretation(analysis_data)
                console.print(Panel("\n\n".join(interpretations), style="bold white"))
                
            else:
                # Use basic interpretation
                _print_basic_interpretation(console, numerology, cultural, phonetics)
                
        except Exception as e:
            console.print(Panel(
                f"[red]Error during AI interpretation:[/red]\n" +
                f"[yellow]{str(e)}[/yellow]\n\n" +
                "[white]Falling back to basic analysis...[/white]",
                title="AI Error"
            ))
            _print_basic_interpretation(console, numerology, cultural, phonetics)
    
    console.print("\n" + "=" * 50)

def _print_basic_interpretation(console, numerology, cultural, phonetics):
    """Fallback interpretation when AI is not available."""
    interpretation = []
    
    # Add core meaning
    if numerology.get('is_master_number'):
        interpretation.append(f"Your name carries the Master Number {numerology['destiny_number']}, "
                           f"suggesting {numerology['master_number_meaning'].lower()}")
    else:
        interpretation.append(f"Your name's destiny number {numerology['destiny_number']} "
                           f"indicates {get_challenge_meaning(numerology['destiny_number'])}")
    
    # Add cultural significance if available
    if cultural['patterns']:
        pattern = cultural['patterns'][0]
        if isinstance(pattern['meaning'], tuple):
            interpretation.append(f"The {pattern['pattern']} pattern suggests {pattern['meaning'][1]}")
        else:
            interpretation.append(f"The {pattern['pattern']} pattern suggests {pattern['meaning']}")
    
    # Add sound pattern insight
    if cultural['structure_notes']:
        interpretation.append(cultural['structure_notes'][0])
    
    console.print(Panel("\n\n".join(interpretation), style="bold white"))
