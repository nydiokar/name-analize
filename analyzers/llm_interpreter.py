import os
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
console = Console()

class NameInterpreter:
    def __init__(self, model=None):
        """Initialize OpenAI interpreter."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model or "gpt-3.5-turbo"  # Default to GPT-3.5 if no model specified
        
        console.print(f"\n[cyan]Using OpenAI model: {self.model}[/cyan]")

    def generate_interpretation(self, analysis_data):
        """Generate natural interpretation using OpenAI."""
        prompt = self._create_prompt(analysis_data)
        
        # Print the prompt being sent to OpenAI
        console.print("\n[yellow]Sending this prompt to OpenAI:[/yellow]")
        console.print(Panel(prompt, title="Prompt", border_style="blue"))
        
        try:
            with console.status("[cyan]Generating interpretation...[/cyan]"):
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500,
                )
                
                interpretation = response.choices[0].message.content.strip()
                
                # Print the raw response
                console.print("\n[yellow]Raw OpenAI response:[/yellow]")
                console.print(Panel(interpretation, title="Response", border_style="green"))
                
                # Split into paragraphs and clean
                paragraphs = [p.strip() for p in interpretation.split('\n') if p.strip()]
                
                if not paragraphs:
                    raise ValueError("No meaningful response generated")
                    
                return self.clean_text(paragraphs)
                
        except Exception as e:
            raise ConnectionError(f"Error generating interpretation: {str(e)}")

    def _create_prompt(self, analysis_data):
        """Create a detailed prompt for the LLM based on analysis data."""
        try:
            # Format the frequency data safely - only include the character distribution
            freq_str = ""
            if isinstance(analysis_data.get('frequency', {}), dict):
                char_dist = analysis_data['frequency'].get('character_distribution', {})
                if isinstance(char_dist, dict):
                    freq_items = []
                    for k, v in char_dist.items():
                        # Convert numpy string types to regular strings
                        key = str(k).replace("np.str_('", "").replace("')", "")
                        freq_items.append(f"{key}: {float(v):.3f}")
                    freq_str = ', '.join(freq_items)

            # Format cultural patterns safely
            patterns_str = ""
            if analysis_data.get('patterns'):
                patterns_str = ', '.join(
                    f"{p.get('pattern', '')} ({p.get('meaning', '')})" 
                    for p in analysis_data.get('patterns', [])
                )

            # Format vibration data safely and cleanly
            vibration_str = ""
            if isinstance(analysis_data.get('vibration', {}), dict):
                vib_items = []
                for k, v in analysis_data.get('vibration', {}).items():
                    if k == 'frequency_character':
                        vib_items.append(f"Character: {v}")
                    elif isinstance(v, (int, float)):
                        vib_items.append(f"{k.replace('_', ' ').title()}: {v:.3f}")
                    else:
                        vib_items.append(f"{k.replace('_', ' ').title()}: {v}")
                vibration_str = '\n'.join(vib_items)

            # Get phonetics data safely
            phonetics = analysis_data.get('phonetics', {})
            syllables = phonetics.get('syllable_count', 'Unknown')
            balance = phonetics.get('sound_balance', 'Unknown')
            pattern = phonetics.get('pattern', 'N/A')

            prompt = f"""Analyze this name in detail:

            Name: {analysis_data.get('name', 'Unknown')}
            
            Cultural Analysis:
            - Heritage: {', '.join(analysis_data.get('cultural_roots', [])) if analysis_data.get('cultural_roots') else 'Universal'}
            - Cultural Elements: {patterns_str}
            
            Phonetic Profile:
            - Syllables: {syllables}
            - Sound Balance: {balance}
            - Vowel-Consonant Pattern: {pattern}
            
            Letter Frequency:
            {freq_str}
            
            Numerological Aspects:
            - Destiny Number: {analysis_data.get('numerology', {}).get('destiny')}

            Vibrational Analysis:
            {vibration_str}
            
            Please provide:

            1. PERSONALITY TRAITS:
            - Key Strengths:
            - Potential Challenges:
            - Natural Talents:

            2. LIFE PATH INDICATORS:
            - Career Affinities:
            - Relationship Approach:
            - Life Lessons:

            3. DETAILED ANALYSIS:
            [Provide 2-3 paragraphs analyzing how the name's numerology, phonetics, and cultural elements combine to influence the person]

            Format the first two sections as clear bullet points, followed by the detailed analysis in paragraph form."""
            
            return prompt
            
        except Exception as e:
            console.print(f"[red]Error creating prompt: {str(e)}[/red]")
            return f"Please analyze the name '{analysis_data.get('name', 'Unknown')}' and provide a brief interpretation."

    def clean_text(self, paragraphs):
        """Clean and format the generated text."""
        unique_paragraphs = []
        seen_content = set()
        
        for paragraph in paragraphs:
            normalized = ' '.join(paragraph.lower().split())
            if normalized and not any(
                self._similar_content(normalized, seen) for seen in seen_content
            ):
                seen_content.add(normalized)
                unique_paragraphs.append(paragraph)
        
        return unique_paragraphs

    def _similar_content(self, text1, text2, threshold=0.7):
        """Check if two pieces of text are similar."""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return False
            
        overlap = len(words1.intersection(words2))
        similarity = overlap / max(len(words1), len(words2))
        
        return similarity > threshold
