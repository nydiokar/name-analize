from analyzers.numerology import get_numerology
from analyzers.phonetics import analyze_phonetics
from analyzers.frequency import analyze_frequency
from analyzers.vibration import VibrationAnalyzer
from analyzers.cultural_patterns import CulturalAnalyzer
from utils.formatter import format_results
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from analyzers.llm_interpreter import NameInterpreter

console = Console()

def analyze_name(name):
    """Perform complete analysis of a name."""
    results = {
        'name': name,  # Add the name to results
        'cultural_roots': [],
        'patterns': []
    }
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        try:
            # Input validation
            if not name or not any(c.isalpha() for c in name):
                raise ValueError("Please enter a valid name containing letters.")
                
            # Cultural pre-analysis
            progress.add_task("Analyzing cultural patterns...", total=None)
            cultural = CulturalAnalyzer.analyze_cultural_elements(name)
            results.update(cultural)  # Add cultural analysis to results
            
            # Adjust analysis based on cultural context
            resonance_profile = cultural.get('resonance_profile', {})
            
            # Numerological analysis
            progress.add_task("Analyzing numerological patterns...", total=None)
            results['numerology'] = get_numerology(name)
            
            # Phonetic analysis
            progress.add_task("Analyzing phonetic patterns...", total=None)
            results['phonetics'] = analyze_phonetics(name)
            
            # Frequency analysis with cultural weight
            progress.add_task("Computing frequency patterns...", total=None)
            results['frequency'] = analyze_frequency(name)
            
            # Vibrational analysis with cultural tuning
            progress.add_task("Calculating vibrational resonance...", total=None)
            base_freq = resonance_profile.get('base_frequency', 432)
            cultural_weight = resonance_profile.get('cultural_weight', 1.0)
            results['vibration'] = VibrationAnalyzer.analyze_name_vibration(
                name, base_frequency=base_freq, cultural_weight=cultural_weight
            )
            
            # Create interpreter instance and generate interpretation
            interpreter = NameInterpreter()
            
            # Prepare the data with correct numerology format
            analysis_data = {
                'name': name,
                'numerology': {
                    'destiny': results['numerology']['destiny_number'],  # Use the actual number
                },
                'cultural_roots': results.get('cultural_roots', []),
                'phonetics': results['phonetics']['phonetic_description'],
                'frequency': results['frequency'],
                'vibration': results['vibration']
            }
            
            interpretation = interpreter.generate_interpretation(analysis_data)
            
            # Format and display results
            format_results(
                name,
                results['numerology'],
                results['phonetics'],
                results['frequency'],
                results['vibration'],
                interpretation
            )
            
        except ValueError as e:
            console.print(f"[red]Input Error: {str(e)}[/red]")
        except Exception as e:
            console.print(f"[red]Analysis Error: {str(e)}[/red]")

def main():
    """Main program loop."""
    console.clear()
    console.print("[bold magenta]Name Analysis Tool - Advanced Edition[/bold magenta]")
    console.print("[dim]Analyzing names through numerology, phonetics, and cultural patterns[/dim]")
    console.print("[dim]Enter a name to analyze (or 'quit' to exit)[/dim]\n")
    
    while True:
        try:
            name = Prompt.ask("[cyan]Name[/cyan]").strip()
            
            if name.lower() == 'quit':
                console.print("\n[yellow]Thank you for using the Name Analysis Tool![/yellow]")
                break
                
            if not name:
                console.print("[red]Please enter a valid name.[/red]")
                continue
                
            analyze_name(name)
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Analysis interrupted. Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]An unexpected error occurred: {str(e)}[/red]")
            console.print("[yellow]Please try again with a different name.[/yellow]")
            continue

if __name__ == "__main__":
    main()
