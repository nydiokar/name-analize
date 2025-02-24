import os
from openai import OpenAI
import requests
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv
import threading
import time

load_dotenv()  # Load environment variables from .env file
console = Console()

class NameInterpreter:
    def __init__(self):
        """Initialize LLM interpreter based on environment configuration."""
        # Get and clean the provider value
        raw_provider = os.getenv("LLM_PROVIDER", "openai")
        self.provider = raw_provider.lower().strip().split('#')[0].strip()  # Remove any comments
        
        console.print(f"[yellow]Debug: Raw LLM_PROVIDER={raw_provider}[/yellow]")
        console.print(f"[yellow]Debug: Cleaned LLM_PROVIDER={self.provider}[/yellow]")
        
        if self.provider not in ["openai", "ollama"]:
            raise ValueError(f"Unsupported LLM provider: '{self.provider}'. Use 'openai' or 'ollama'")
            
        if self.provider == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your environment variables.")
            self.client = OpenAI(api_key=self.api_key)
            self.model = "gpt-3.5-turbo"
        else:  # ollama
            raw_model = os.getenv("OLLAMA_MODEL", "mistral")
            self.model = raw_model.strip().split('#')[0].strip()  # Remove any comments
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

    def generate_interpretation(self, analysis_data):
        """Generate interpretation using selected LLM provider."""
        prompt = self._create_prompt(analysis_data)
        
        # Print the prompt being sent to LLM
        console.print("\n[yellow]Sending this prompt to LLM:[/yellow]")
        console.print(Panel(prompt, title="Prompt", border_style="blue"))
        
        try:
            if self.provider == "openai":
                return self._generate_openai(prompt)
            else:
                return self._generate_ollama(prompt)
                
        except Exception as e:
            raise ConnectionError(f"Error generating interpretation: {str(e)}")

    def _generate_openai(self, prompt):
        """Generate interpretation using OpenAI."""
        with console.status("[cyan]Generating interpretation with OpenAI...[/cyan]"):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500,
            )
            
            interpretation = response.choices[0].message.content.strip()
            return self.clean_text(interpretation.split('\n'))

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

class RequestTimeout(Exception):
    pass
