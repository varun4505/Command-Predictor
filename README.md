## 🚀 Quick Start

### Linux/macOS
```bash
# Make the run script executable
chmod +x run.sh

# Install dependencies
pip3 install -r requirements.txt

# Set up your Groq API key
cp .env.example .env
# Edit .env and add your Groq API key

# Run the predictor
./run.sh                    # Easy start
python3 main.py             # Direct run
```

### Windows
```bash
# Install dependencies
pip install -r requirements.txt

# Your API key should already be in .env

# Run the predictor
run.bat                     # Easy start
python main.py              # Direct run
```

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key (free at [groq.com](https://groq.com/))

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/varun4505/Command-Predictor.git
   cd Command-Predictor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Groq API key
   ```

## 🎯 Features

- **Command History Capture**: Automatically captures your last 5 terminal commands
- **AI-Powered Prediction**: Uses Groq's free API to predict your next logical commands
- **Workflow Understanding**: Analyzes patterns in your command usage to suggest next steps
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Easy Command Extraction**: Clear demarcation for extracting predicted commands

## ⚙️ Configuration

Edit `config.json` to customize:
- AI model settings
- Number of commands to analyze
- Output preferences
- Command filtering

## 🔧 Usage Examples

### Linux/macOS
```bash
# Basic command prediction
./run.sh
python3 main.py

# JSON output (includes predicted commands)
python3 main.py --output-format json
```

### Windows
```bash
# Basic command prediction
run.bat
python main.py

# JSON output (includes predicted commands)
python main.py --output-format json
```

## 🤖 How It Works

1. **Capture**: Reads your recent terminal commands from history
2. **Summarize**: Primary AI agent creates a workflow summary
3. **Predict**: Secondary AI agent predicts the next logical commands to run
4. **Extract**: Commands are clearly marked for easy extraction and execution

## 💡 Example Output

```
WORKFLOW SUMMARY
The user performed a typical Git workflow: checking status, adding files, 
and committing changes. They appear to be in the middle of a development cycle.

PREDICTED NEXT COMMANDS
NEXT_COMMANDS_START
git push origin main
git checkout -b feature/new-feature
npm test
NEXT_COMMANDS_END
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Groq](https://groq.com/)
- Python community for excellent libraries
- Open source contributors

---

