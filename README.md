# Name Analysis Tool with AI Enhancement

A comprehensive tool for analyzing names through numerology, phonetics, cultural patterns, and AI-powered interpretation using Ollama.

## Features

- Numerological analysis with master numbers and karmic debt detection
- Cultural pattern recognition (Slavic, Germanic, Celtic, Latin)
- Phonetic analysis with sound patterns
- AI-powered natural language interpretation
- Frequency and vibrational analysis
- Real-time, local AI processing

## Installation

1. Install Ollama:
   - **Windows**: Download from [ollama.ai/download](https://ollama.ai/download)
   - **macOS/Linux**: `curl https://ollama.ai/install.sh | sh`

2. Clone and set up the project:
```bash
git clone https://github.com/yourusername/name-analyzer.git
cd name-analyzer
python setup.py
```

The setup script will:
- Install Python dependencies
- Check Ollama installation
- Guide you through any missing requirements

## Usage

1. Start Ollama service (if not running)
2. Run the analyzer:
```bash
python main.py
```

Enter any name when prompted. The tool will provide:
- Numerological significance
- Cultural pattern analysis
- Phonetic characteristics
- AI-generated unique interpretation

## Operating Modes

The tool operates in two modes:

1. **AI-Enhanced Mode (Default)**
   - Uses Ollama for natural language interpretation
   - Provides detailed cultural analysis
   - Generates unique, context-aware insights

2. **Basic Mode (Fallback)**
   - Uses pattern matching
   - Works without Ollama
   - Provides essential analysis

## Requirements

- Python 3.8+
- Ollama installed and running
- 4GB RAM minimum
- Internet connection (for first-time model download)

## Technical Details

- Uses Mistral model through Ollama for AI interpretation
- Combines traditional numerology with modern AI analysis
- Cultural pattern recognition engine
- Advanced phonetic analysis system

## Contributing

Contributions welcome! Areas of interest:
- Additional cultural patterns
- Enhanced AI prompts
- New analysis methods
- Performance improvements

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Ollama team for the amazing local LLM runtime
- Mistral AI for the base model
- Contributors to the numerology and phonetics modules
