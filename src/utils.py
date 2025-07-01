import os
import json
from typing import Dict, Any
from datetime import datetime
import logging

class OutputManager:
    """Manages output formatting and saving"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.output_dir = config.get("output_directory", "outputs")
        self.save_to_file = config.get("save_to_file", True)
        self.include_raw_commands = config.get("include_raw_commands", False)
        
        # Create output directory if it doesn't exist
        if self.save_to_file:
            os.makedirs(self.output_dir, exist_ok=True)
    
    def format_analysis_output(self, commands: list, summary: str, predictions: str) -> Dict[str, Any]:
        """Format the complete analysis output"""
        # Extract predicted commands as a list
        predicted_commands_list = self._extract_commands_from_predictions(predictions)
        
        output = {
            "timestamp": datetime.now().isoformat(),
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "command_count": len(commands),
            "summary": summary,
            "predicted_commands_list": predicted_commands_list,
        }
        
        if self.include_raw_commands:
            output["raw_commands"] = commands
        
        return output
    
    def _extract_commands_from_predictions(self, predictions: str) -> list:
        """Extract commands from the predictions text"""
        try:
            # Split by lines and filter out empty lines and any unwanted text
            lines = predictions.strip().split('\n')
            commands = []
            
            for line in lines:
                line = line.strip()
                # Skip empty lines and any explanatory text
                if line and not line.startswith('#') and not line.startswith('//') and not line.lower().startswith('note'):
                    # Remove any numbering like "1. command" -> "command"
                    if line and line[0].isdigit() and '.' in line:
                        line = line.split('.', 1)[1].strip()
                    commands.append(line)
            
            return commands
        except Exception:
            return []
    
    def save_output(self, output: Dict[str, Any]) -> str:
        """Save output to file and return the filename"""
        if not self.save_to_file:
            return ""
        
        filename = f"analysis_{output['session_id']}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            return filepath
        except Exception as e:
            logging.error(f"Error saving output: {e}")
            return ""
    
    def print_formatted_output(self, output: Dict[str, Any]):
        """Print formatted output to console"""
        print("\n" + "="*60)
        print("AI COMMAND PREDICTOR REPORT")
        print("="*60)
        print(f"Session ID: {output['session_id']}")
        print(f"Timestamp: {output['timestamp']}")
        print(f"Commands Analyzed: {output['command_count']}")
        
        print("\n" + "-"*40)
        print("WORKFLOW SUMMARY")
        print("-"*40)
        print(output['summary'])
        
        # Show the predicted commands list for easy copying
        if output.get('predicted_commands_list'):
            print("\n" + "-"*40)
            print("PREDICTED NEXT COMMANDS")
            print("-"*40)
            for i, cmd in enumerate(output['predicted_commands_list'], 1):
                print(f"{i}. {cmd}")
        
        if output.get('raw_commands'):
            print("\n" + "-"*40)
            print("RECENT COMMANDS")
            print("-"*40)
            for i, cmd in enumerate(output['raw_commands'], 1):
                print(f"{i}. {cmd['command']}")
        
        print("\n" + "="*60)

class ConfigManager:
    """Manages configuration loading and validation"""
    
    @staticmethod
    def load_config(config_path: str = "config.json") -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {config_path} not found. Using defaults.")
            return ConfigManager.get_default_config()
        except json.JSONDecodeError as e:
            print(f"Error parsing config file: {e}. Using defaults.")
            return ConfigManager.get_default_config()
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "primary_agent": {
                "model": "gpt-3.5-turbo",
                "max_tokens": 500,
                "temperature": 0.7,
                "system_prompt": "You are a command summarization expert. Analyze terminal commands and create concise, informative summaries."
            },
            "secondary_agent": {
                "model": "gpt-4",
                "max_tokens": 1000,
                "temperature": 0.8,
                "system_prompt": "You are an intelligent command analyst. Analyze command summaries and provide insights, suggestions, and helpful responses."
            },
            "history": {
                "max_commands": 5,
                "ignore_patterns": ["ls", "pwd", "clear", "history"],
                "include_timestamps": True
            },
            "output": {
                "save_to_file": True,
                "output_directory": "./outputs",
                "include_raw_commands": False
            }
        }
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """Validate configuration structure"""
        required_sections = ["primary_agent", "secondary_agent", "history", "output"]
        return all(section in config for section in required_sections)
