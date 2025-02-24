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
import signal
import sys
import os

console = Console()

# Global flag for interruption
interrupted = False

def signal_handler(signum, frame):
    """Handle interrupt signal."""
    global interrupted
    interrupted = True
    console.print("\n[yellow]Interrupting... Please wait or press Ctrl+C again to force quit.[/yellow]")
    # Set a more aggressive handler for subsequent interrupts
    signal.signal(signal.SIGINT, force_quit_handler)

def force_quit_handler(signum, frame):
    """Force quit the program."""
    console.print("\n[red]Force quitting...[/red]")
    os._exit(1)  # More aggressive exit

def analyze_name(name):
    """Perform complete analysis of a name."""
    global interrupted
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    results = {
        'name': name,
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
            # Check for interruption
            if interrupted:
                raise KeyboardInterrupt
                
            # Input validation
            if not name or not any(c.isalpha() for c in name):
                raise ValueError("Please enter a valid name containing letters.")
                
            # Cultural pre-analysis
            progress.add_task("Analyzing cultural patterns...", total=None)
            cultural = CulturalAnalyzer.analyze_cultural_elements(name)
            results.update(cultural)
            
            if interrupted:
                raise KeyboardInterrupt
                
            # Adjust analysis based on cultural context
            resonance_profile = cultural.get('resonance_profile', {})
            
            # Numerological analysis
            progress.add_task("Analyzing numerological patterns...", total=None)
            results['numerology'] = get_numerology(name)
            
            if interrupted:
                raise KeyboardInterrupt
                
            # Phonetic analysis
            progress.add_task("Analyzing phonetic patterns...", total=None)
            results['phonetics'] = analyze_phonetics(name)
            
            if interrupted:
                raise KeyboardInterrupt
                
            # Frequency analysis with cultural weight
            progress.add_task("Computing frequency patterns...", total=None)
            results['frequency'] = analyze_frequency(name)
            
            if interrupted:
                raise KeyboardInterrupt
                
            # Vibrational analysis with cultural tuning
            progress.add_task("Calculating vibrational resonance...", total=None)
            base_freq = resonance_profile.get('base_frequency', 432)
            cultural_weight = resonance_profile.get('cultural_weight', 1.0)
            results['vibration'] = VibrationAnalyzer.analyze_name_vibration(
                name, base_frequency=base_freq, cultural_weight=cultural_weight
            )
            
            if interrupted:
                raise KeyboardInterrupt
                
            # Create interpreter instance and generate interpretation
            interpreter = NameInterpreter()
            
            # Prepare the data with correct numerology format
            analysis_data = {
                'name': name,
                'numerology': {
                    'destiny': results['numerology']['destiny_number'],
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
            
        except KeyboardInterrupt:
            console.print("\n[red]Analysis interrupted by user.[/red]")
            return None
        except ValueError as e:
            console.print(f"[red]Input Error: {str(e)}[/red]")
        except Exception as e:
            console.print(f"[red]Analysis Error: {str(e)}[/red]")
        finally:
            # Reset the interrupt flag
            interrupted = False

def main():
    """Main program loop."""
    console.clear()
    console.print("[bold magenta]Name Analysis Tool - Advanced Edition[/bold magenta]")
    console.print("[dim]Analyzing names through numerology, phonetics, and cultural patterns[/dim]")
    console.print("[dim]Enter a name to analyze (or 'quit' to exit)[/dim]")
    console.print("[dim]Press Ctrl+C at any time to interrupt the analysis[/dim]\n")
    
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
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]An unexpected error occurred: {str(e)}[/red]")
            console.print("[yellow]Please try again with a different name.[/yellow]")
            continue

if __name__ == "__main__":
    main()
