# Name Analysis Tool

A comprehensive name analysis tool that combines numerology, phonetics, cultural patterns, and AI-powered interpretation to provide deep insights into names.

## Features

- **AI-Powered Analysis**: Uses OpenAI GPT-3.5 or Ollama for intelligent name interpretation
- **Numerological Analysis**: Calculates destiny numbers and identifies master numbers
- **Phonetic Analysis**: Analyzes sound patterns and syllabic structure
- **Cultural Pattern Recognition**: Identifies cultural roots and patterns
- **Frequency Analysis**: Analyzes letter distribution patterns
- **Vibrational Analysis**: Calculates name vibration frequencies

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/name-analize.git
cd name-analize
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

## Configuration

The tool supports two LLM (Language Model) providers:

### 1. OpenAI (Default)
- Requires an API key from OpenAI
- Configure in `.env`:
```
LLM_PROVIDER=openai
OPENAI_API_KEY=your-api-key-here
```

### 2. Ollama (Local)
- Requires Ollama installed locally
- Configure in `.env`:
```
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral  # or any other model you have installed
```

To use Ollama:
1. Install Ollama from https://ollama.ai
2. Start the Ollama service
3. Pull your preferred model:
```bash
ollama pull mistral
```

## Usage

1. Run the setup script:
```bash
python setup.py
```

2. Run the main script:
```bash
python main.py
```

3. Enter any name when prompted, and the tool will provide:
- Cultural analysis
- Numerological significance
- Phonetic patterns
- Frequency distribution
- Vibrational resonance
- AI-generated interpretation

## Requirements

- Python 3.8+
- OpenAI API key (if using OpenAI)
- Ollama installation (if using Ollama)
- Required packages (see requirements.txt)

## Privacy & Security

- Never commit your `.env` file containing API keys
- The tool processes names locally except for AI interpretation
- API calls are made securely using official clients
- When using Ollama, all processing is done locally on your machine

## Troubleshooting

### OpenAI Issues
- Verify your API key is correct
- Ensure you have sufficient API credits
- Check your internet connection

### Ollama Issues
- Verify Ollama is installed and running
- Check if the selected model is downloaded
- Ensure port 11434 is available

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
