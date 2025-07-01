# AI Terminal Command Predictor

An intelligent system that analyzes your terminal command history and predicts the next commands you should run to continue your workflow.

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

## 🎯 Features

- **Command History Capture**: Automatically captures your last 5 terminal commands
- **AI-Powered Prediction**: Uses Groq's free API to predict your next logical commands
- **Workflow Understanding**: Analyzes patterns in your command usage to suggest next steps
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Easy Command Extraction**: Clear demarcation for extracting predicted commands

## 📁 Project Structure

```
AI Agent/
├── main.py              # Main application entry point
├── ai_agents.py         # AI agent implementations (Primary & Secondary)
├── history_capture.py   # Terminal history capture logic
├── utils.py            # Configuration and output management
├── config.json         # Agent configuration settings
├── .env               # API keys and environment variables
├── requirements.txt   # Python dependencies
└── outputs/          # Analysis results (auto-created)
```

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

## 🆓 Free API Usage

- **Groq**: 1000 requests/day (recommended)
- **HuggingFace**: Unlimited local models (slower)
- **Ollama**: Unlimited local models (requires installation)

## 📄 License

Open source project - feel free to modify and use!
