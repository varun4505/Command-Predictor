#!/usr/bin/env python3
"""
AI Agent Terminal Command Analyzer
Main application that coordinates the primary and secondary agents
"""

import os
import sys
import json
import argparse
import logging
from dotenv import load_dotenv
from src.history_capture import HistoryCapture
from src.ai_agents import PrimaryAgent, SecondaryAgent
from src.utils import ConfigManager, OutputManager

class TerminalAnalyzer:
    """Main application class that coordinates the AI agents"""
    
    def __init__(self, config_path: str = "config/config.json"):
        # Load environment variables
        load_dotenv(".env")
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.config = ConfigManager.load_config(config_path)
        
        # Validate configuration
        if not ConfigManager.validate_config(self.config):
            self.logger.error("Invalid configuration. Please check your config.json file.")
            sys.exit(1)
        
        # Check Groq API key
        if not os.getenv("GROQ_API_KEY"):
            self.logger.error("GROQ_API_KEY not found in environment variables.")
            self.logger.error("Please set your Groq API key in the .env file.")
            sys.exit(1)
        
        self.logger.info("✅ Groq API configured successfully")
        
        # Initialize components
        self.history_capture = HistoryCapture(
            max_commands=self.config["history"]["max_commands"]
        )
        
        self.primary_agent = PrimaryAgent(self.config["primary_agent"])
        self.secondary_agent = SecondaryAgent(self.config["secondary_agent"])
        self.output_manager = OutputManager(self.config["output"])
    
    def analyze_commands(self) -> dict:
        """
        Main analysis workflow:
        1. Capture terminal history
        2. Summarize with primary agent
        3. Predict next commands with secondary agent
        """
        self.logger.info("Starting command analysis...")
        
        # Step 1: Capture command history
        self.logger.info("Capturing command history...")
        commands = self.history_capture.get_last_commands(
            ignore_patterns=self.config["history"]["ignore_patterns"]
        )
        
        if not commands:
            self.logger.warning("No commands found in history.")
            return {"error": "No commands found in history"}
        
        self.logger.info(f"Captured {len(commands)} commands")
        
        # Format commands for analysis
        commands_text = self.history_capture.format_commands_for_analysis(commands)
        
        # Step 2: Primary agent summarization
        self.logger.info("Generating command summary...")
        try:
            summary = self.primary_agent.summarize_commands(commands_text)
        except Exception as e:
            self.logger.error(f"Error in primary agent: {e}")
            return {"error": f"Primary agent error: {e}"}
        
        # Step 3: Secondary agent analysis (command prediction)
        self.logger.info("Predicting next commands...")
        try:
            command_predictions = self.secondary_agent.analyze_summary(summary, commands_text)
        except Exception as e:
            self.logger.error(f"Error in secondary agent: {e}")
            return {"error": f"Secondary agent error: {e}"}
        
        # Format output
        output = self.output_manager.format_analysis_output(
            commands, summary, command_predictions
        )
        
        self.logger.info("Analysis complete!")
        return output
    

    
    def run_once(self, output_format: str = "console"):
        """Run analysis once and exit"""
        result = self.analyze_commands()
        
        if "error" in result:
            print(f"Error: {result['error']}")
            return 1
        
        if output_format.lower() == "json":
            print(json.dumps(result, indent=2))
        else:
            self.output_manager.print_formatted_output(result)
        
        if self.output_manager.save_to_file:
            filepath = self.output_manager.save_output(result)
            if filepath:
                print(f"\nPredictions saved to: {filepath}")
        
        return 0

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AI Terminal Command Predictor")
    parser.add_argument("--config", "-c", default="config/config.json", 
                       help="Path to configuration file")
    parser.add_argument("--output-format", choices=["console", "json"], default="console",
                       help="Output format")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        analyzer = TerminalAnalyzer(config_path=args.config)
        
        exit_code = analyzer.run_once(output_format=args.output_format)
        sys.exit(exit_code)
    
    except Exception as e:
        logging.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()