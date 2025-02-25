import os
from openai import OpenAI
import requests
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv
import threading
import time
import json

# Load environment variables at the start
load_dotenv(override=True)  # Add override=True to ensure values are updated

console = Console()

class NameInterpreter:
    def __init__(self):
        """Initialize LLM interpreter based on environment configuration."""
        # Get and clean the provider value
        raw_provider = os.getenv("LLM_PROVIDER", "openai")
        self.provider = raw_provider.lower().strip().split('#')[0].strip()
        
        console.print(f"[yellow]Using LLM Provider: {self.provider}[/yellow]")
        
        if self.provider == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
            self.client = OpenAI(api_key=self.api_key)
            self.model = "gpt-3.5-turbo"
            console.print("[green]Successfully initialized OpenAI client[/green]")
        elif self.provider == "ollama":
            raw_model = os.getenv("OLLAMA_MODEL", "mistral")
            self.model = raw_model.strip().split('#')[0].strip()
            console.print(f"[yellow]Debug: Using Ollama model: {self.model}[/yellow]")
            self.base_url = "http://localhost:11434"
            
            # Test Ollama connection and model availability
            try:
                # Check if service is running
                response = requests.get(f"{self.base_url}/api/tags")
                if response.status_code != 200:
                    raise ConnectionError("Ollama service not running")
                
                # Check if model exists
                model_check = requests.post(
                    f"{self.base_url}/api/show",
                    json={"name": self.model}
                )
                if model_check.status_code != 200:
                    raise ValueError(f"Model '{self.model}' not found in Ollama. Please pull it first with: ollama pull {self.model}")
                    
            except requests.exceptions.ConnectionError:
                raise ConnectionError("Cannot connect to Ollama service. Is it running?")
            except Exception as e:
                raise ConnectionError(f"Cannot connect to Ollama: {str(e)}")
        
        console.print(f"\n[cyan]Using {self.provider.upper()} model: {self.model}[/cyan]")

        # Add interpretation templates
        self.interpretation_templates = {
            'high_resonance': {
                'summary': "Your name carries strong, vibrant energy",
                'strengths': ["Natural leadership", "Clear communication"],
                'challenges': ["May come across as intense"],
                'life_path': "You're drawn to positions of influence and expression"
            },
            'medium_resonance': {
                'summary': "Your name holds balanced, harmonious energy",
                'strengths': ["Adaptability", "Good mediator"],
                'challenges': ["May sometimes lack decisiveness"],
                'life_path': "You excel in roles requiring balance and harmony"
            },
            'low_resonance': {
                'summary': "Your name carries grounding, stable energy",
                'strengths': ["Reliability", "Deep thinking"],
                'challenges': ["May resist quick changes"],
                'life_path': "You're suited for roles requiring depth and persistence"
            }
        }

    def generate_interpretation(self, analysis_data):
        """Generate interpretation using selected LLM provider."""
        try:
            prompt = self._create_prompt(analysis_data)
            
            # Generate interpretation
            if self.provider == "openai":
                raw_interpretation = self._generate_openai(prompt)
            elif self.provider == "ollama":
                raw_interpretation = self._generate_ollama(prompt)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
            
            # Clean up the raw interpretation and return it directly
            cleaned_text = raw_interpretation.strip()
            
            # Debug output to console
            console.print("[yellow]Generated interpretation:[/yellow]")
            console.print(Panel(cleaned_text, title="Interpretation", border_style="green"))
            
            return cleaned_text
            
        except Exception as e:
            console.print(f"[red]Interpretation error: {e}[/red]")
            return "Unable to generate interpretation."

    def _generate_openai(self, prompt):
        """Generate interpretation using OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": """You are a name analysis expert. Structure your response with these exact section headers:

Overall Impression:
Key Strengths:
Growth Areas:
Life Path Insights:
Deeper Analysis:

For Key Strengths and Growth Areas, use numbered points (1., 2., etc.)."""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            console.print(f"[red]OpenAI API error: {str(e)}[/red]")
            raise

    def _generate_ollama(self, prompt):
        """Generate interpretation using Ollama with timeout."""
        def request_target():
            nonlocal response_data
            try:
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "num_predict": 500
                        }
                    },
                    timeout=30
                )
                response_data['response'] = response
            except Exception as e:
                response_data['error'] = e

        with console.status("[cyan]Generating interpretation with Ollama...[/cyan]") as status:
            try:
                # Initialize response data
                response_data = {'response': None, 'error': None}
                interrupted = False
                
                # Create and start request thread
                request_thread = threading.Thread(target=request_target)
                request_thread.daemon = True  # Allow the thread to be killed
                request_thread.start()
                
                # Wait for response with timeout
                start_time = time.time()
                while request_thread.is_alive():
                    if time.time() - start_time > 30:  # 30 seconds timeout
                        raise RequestTimeout("Request took too long")
                    if interrupted: 
                        raise KeyboardInterrupt
                    time.sleep(0.1)
                
                # Check for errors
                if response_data['error']:
                    raise response_data['error']
                
                response = response_data['response']
                if response.status_code != 200:
                    raise ConnectionError(f"Ollama API error: {response.text}")
                
                interpretation = response.json()["response"].strip()
                if not interpretation:
                    raise ValueError("Empty response from Ollama")
                
                return self.clean_text(interpretation.split('\n'))
                
            except KeyboardInterrupt:
                console.print("\n[red]Operation cancelled by user[/red]")
                raise
            except RequestTimeout:
                console.print("\n[red]Request timed out. Cancelling...[/red]")
                raise ConnectionError("Request timed out")
            except Exception as e:
                raise ConnectionError(f"Ollama error: {str(e)}")

    def _create_prompt(self, analysis_data):
        """Create a structured prompt for the LLM based on analysis data."""
        try:
            # Extract data with safe fallbacks
            name = analysis_data.get('name', 'Unknown')
            numerology = analysis_data.get('numerology', {}) or {}
            vibration = analysis_data.get('vibration', {}) or {}
            phonetics = analysis_data.get('phonetics', {}) or {}
            
            # Extract key values
            destiny_number = numerology.get('destiny_number', 'Unknown')
            base_freq = vibration.get('base_frequency', 'Unknown')
            resonance = vibration.get('resonance_strength', 'Unknown')
            frequency_character = vibration.get('frequency_character', 'Unknown')
            consonant_count = phonetics.get('consonant_count', 'Unknown')
            vowel_count = phonetics.get('vowel_count', 'Unknown')
            
            prompt = f"""Based on the following data, provide a structured analysis for the name {name}:

ANALYSIS DATA:
- Numerology: Destiny Number {destiny_number} ({self._get_numerology_meaning(destiny_number)})
- Vibration: {base_freq} Hz, {resonance} resonance, {frequency_character} character
- Phonetics: {consonant_count} consonants, {vowel_count} vowels, {self._analyze_sound_pattern(phonetics)}

Structure your response exactly as follows:

Overall Impression:
[Provide a brief overview of how these elements combine to create a unique energy signature]

Key Strengths:
1. [First key strength]
2. [Second key strength]
3. [Third key strength]

Growth Areas:
1. [First growth area]
2. [Second growth area]

Life Path Insights:
[Describe how these elements influence career paths, relationships, and personal growth]

Deeper Analysis:
[Connect all elements into a cohesive picture]

Keep each section concise and focused. Use natural language and avoid technical jargon.
"""
            return prompt
            
        except Exception as e:
            console.print(f"[red]Error creating prompt: {str(e)}[/red]")
            return f"Please analyze the name '{analysis_data.get('name', 'Unknown')}' in natural language paragraphs."

    def _analyze_sound_pattern(self, phonetics):
        """Analyze the sound pattern of the name."""
        consonants = phonetics.get('consonant_count', 0)
        vowels = phonetics.get('vowel_count', 0)
        
        if consonants > vowels * 2:
            return "strong consonant emphasis, suggesting direct expression"
        elif vowels > consonants:
            return "flowing vowel emphasis, indicating emotional expression"
        else:
            return "balanced sound pattern, showing harmonious expression"

    def _get_numerology_meaning(self, number):
        """Get detailed numerological meaning."""
        meanings = {
            1: "leadership and innovation",
            2: "cooperation and sensitivity",
            3: "creativity and expression",
            4: "structure and stability",
            5: "freedom and change",
            6: "harmony and responsibility",
            7: "analysis and spirituality",
            8: "power and abundance",
            9: "humanitarian and completion"
        }
        try:
            num = int(number)
            return meanings.get(num, "universal potential")
        except:
            return "universal potential"

    def clean_text(self, text_input):
        """Clean and format the generated text."""
        # Handle both string and list inputs
        if isinstance(text_input, str):
            paragraphs = text_input.split('\n')
        else:
            paragraphs = text_input
        
        unique_paragraphs = []
        seen_content = set()
        
        for paragraph in paragraphs:
            if not isinstance(paragraph, str):
                continue
            
            normalized = ' '.join(paragraph.lower().split())
            if normalized and not any(
                self._similar_content(normalized, seen) for seen in seen_content
            ):
                seen_content.add(normalized)
                unique_paragraphs.append(paragraph)
        
        return '\n'.join(unique_paragraphs) if unique_paragraphs else "No valid interpretation generated."

    def _similar_content(self, text1, text2, threshold=0.7):
        """Check if two pieces of text are similar."""
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return False
            
        overlap = len(words1.intersection(words2))
        similarity = overlap / max(len(words1), len(words2))
        
        return similarity > threshold

    def format_interpretation(self, text, analysis_data):
        """Return the raw LLM response as a single string."""
        try:
            return text.strip()
        except Exception as e:
            console.print(f"[red]Error in formatting: {str(e)}[/red]")
            return "No interpretation available."

class RequestTimeout(Exception):
    pass
