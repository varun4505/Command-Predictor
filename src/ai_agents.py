import requests
import json
import os
from typing import Dict
from datetime import datetime

class AIAgent:
    """Base class for AI agents using Groq API"""
    
    def __init__(self, model_type: str = "groq", model_name: str = None, 
                 system_prompt: str = "", max_tokens: int = 500, temperature: float = 0.7):
        self.model_type = model_type
        self.model_name = model_name or "llama3-8b-8192"
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.conversation_history = []
        
        # Setup Groq API
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
    
    def generate_response(self, user_input: str, context: str = "") -> str:
        """Generate a response using the Groq API"""
        try:
            # Prepare messages
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            if context:
                messages.append({"role": "system", "content": f"Context: {context}"})
            
            messages.append({"role": "user", "content": user_input})
            
            # Make API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            response = requests.post(self.api_url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            return result["choices"][0]["message"]["content"]
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def add_to_history(self, user_input: str, response: str):
        """Add conversation to history"""
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "response": response
        })

class PrimaryAgent(AIAgent):
    """Primary agent responsible for summarizing terminal commands"""
    
    def __init__(self, config: Dict):
        super().__init__(
            model_type=config.get("model_type", "groq"),
            model_name=config.get("model_name", "llama3-8b-8192"),
            system_prompt=config.get("system_prompt", 
                "You are a command summarization expert. Analyze terminal commands and create concise, informative summaries."),
            max_tokens=config.get("max_tokens", 400),
            temperature=config.get("temperature", 0.7)
        )
    
    def summarize_commands(self, commands_text: str) -> str:
        """Summarize the captured terminal commands"""
        prompt = f"""
        Please analyze the following terminal commands and provide a concise summary that includes:
        1. What the user was trying to accomplish
        2. The types of commands used (file operations, system commands, development tasks, etc.)
        3. Any patterns or workflows you notice
        4. Key files or directories being worked with
        
        Commands to analyze:
        {commands_text}
        
        Provide a clear, structured summary in 2-3 paragraphs.
        """
        
        response = self.generate_response(prompt)
        self.add_to_history(commands_text, response)
        return response

class SecondaryAgent(AIAgent):
    """Secondary agent responsible for predicting next commands based on user workflow"""
    
    def __init__(self, config: Dict):
        super().__init__(
            model_type=config.get("model_type", "groq"),
            model_name=config.get("model_name", "llama3-70b-8192"),
            system_prompt=config.get("system_prompt", 
                "You are an intelligent command predictor. Based on terminal command history, predict the most likely next commands the user should run to continue their workflow."),
            max_tokens=config.get("max_tokens", 400),
            temperature=config.get("temperature", 0.6)
        )
    
    def analyze_summary(self, summary: str, original_commands: str = "") -> str:
        """Predict the next commands based on workflow analysis"""
        prompt = f"""
        Based on the following command summary and original commands, predict the most likely next commands the user should run to continue their workflow.
        
        Command Summary:
        {summary}
        
        Original Commands Context:
        {original_commands}
        
        Please provide ONLY the next recommended commands to run. Format your response exactly like this:
        
        command1
        command2
        command3
        
        Rules:
        - Provide 2-5 practical commands that logically follow the current workflow
        - Use actual executable commands (no explanatory text)
        - Consider common development/system administration patterns
        - Each command should be on a separate line
        - Do not include any markers, headers, or explanatory text
        - Only provide the raw commands, one per line
        """
        
        response = self.generate_response(prompt, context=summary)
        self.add_to_history(summary, response)
        return response
    
    def extract_commands(self, response: str) -> list:
        """Extract commands from the response (no markers needed)"""
        try:
            # Split by lines and filter out empty lines and any unwanted text
            lines = response.strip().split('\n')
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
    
    def get_predicted_commands_list(self, response: str) -> list:
        """Get the predicted commands as a simple list for programmatic use"""
        return self.extract_commands(response)
