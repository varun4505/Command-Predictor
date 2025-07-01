import os
import json
import subprocess
import platform
from typing import List, Dict, Optional
from datetime import datetime
import re

class HistoryCapture:
    
    def __init__(self, max_commands: int = 5):
        self.max_commands = max_commands
        self.platform = platform.system().lower()
    
    def get_last_commands(self, ignore_patterns: List[str] = None) -> List[Dict]:
        """
        Capture the last N commands from terminal history
        Returns a list of command dictionaries with timestamp and command text
        """
        if ignore_patterns is None:
            ignore_patterns = []
        
        try:
            if self.platform == "windows":
                return self._get_windows_history(ignore_patterns)
            else:
                return self._get_unix_history(ignore_patterns)
        except Exception as e:
            print(f"Error capturing history: {e}")
            return []
    
    def _get_windows_history(self, ignore_patterns: List[str]) -> List[Dict]:
        """Get command history from Windows PowerShell or Command Prompt"""
        commands = []
        
        try:
            # Try PowerShell history first
            ps_history_path = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\PowerShell\\PSReadline\\ConsoleHost_history.txt")
            
            if os.path.exists(ps_history_path):
                with open(ps_history_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                
                # Get last commands, filtering out ignored patterns
                filtered_lines = []
                for line in lines:
                    line = line.strip()
                    if line and not any(pattern.lower() in line.lower() for pattern in ignore_patterns):
                        filtered_lines.append(line)
                
                # Take the last N commands
                recent_commands = filtered_lines[-self.max_commands:]
                
                for i, cmd in enumerate(recent_commands):
                    commands.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "command": cmd,
                        "index": i + 1
                    })
            
            # Fallback: try to get from doskey if PowerShell history is not available
            if not commands:
                try:
                    result = subprocess.run(['doskey', '/history'], 
                                          capture_output=True, text=True, shell=True)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        filtered_lines = [line.strip() for line in lines 
                                        if line.strip() and not any(pattern.lower() in line.lower() 
                                        for pattern in ignore_patterns)]
                        
                        recent_commands = filtered_lines[-self.max_commands:]
                        for i, cmd in enumerate(recent_commands):
                            commands.append({
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "command": cmd,
                                "index": i + 1
                            })
                except:
                    pass
        
        except Exception as e:
            print(f"Error reading Windows history: {e}")
        
        return commands
    
    def _get_unix_history(self, ignore_patterns: List[str]) -> List[Dict]:
        """Get command history from Unix-like systems (Linux/macOS)"""
        commands = []
        
        try:
            # Try to read from bash history
            history_file = os.path.expanduser("~/.bash_history")
            
            if not os.path.exists(history_file):
                # Try zsh history
                history_file = os.path.expanduser("~/.zsh_history")
            
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                
                # Filter out ignored patterns and empty lines
                filtered_lines = []
                for line in lines:
                    line = line.strip()
                    # Handle zsh history format (timestamps)
                    if line.startswith(':') and ';' in line:
                        line = line.split(';', 1)[1].strip()
                    
                    if line and not any(pattern.lower() in line.lower() for pattern in ignore_patterns):
                        filtered_lines.append(line)
                
                # Get the last N commands
                recent_commands = filtered_lines[-self.max_commands:]
                
                for i, cmd in enumerate(recent_commands):
                    commands.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "command": cmd,
                        "index": i + 1
                    })
            
            # Fallback: use history command
            if not commands:
                try:
                    result = subprocess.run(['history'], 
                                          capture_output=True, text=True, shell=True)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        # Parse history output (usually has numbers at the beginning)
                        filtered_commands = []
                        for line in lines:
                            # Remove leading numbers and whitespace
                            cmd = re.sub(r'^\s*\d+\s*', '', line).strip()
                            if cmd and not any(pattern.lower() in cmd.lower() for pattern in ignore_patterns):
                                filtered_commands.append(cmd)
                        
                        recent_commands = filtered_commands[-self.max_commands:]
                        for i, cmd in enumerate(recent_commands):
                            commands.append({
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "command": cmd,
                                "index": i + 1
                            })
                except:
                    pass
        
        except Exception as e:
            print(f"Error reading Unix history: {e}")
        
        return commands

    def format_commands_for_analysis(self, commands: List[Dict]) -> str:
        """Format captured commands for AI analysis"""
        if not commands:
            return "No recent commands found."
        
        formatted = "Recent Terminal Commands:\n"
        formatted += "=" * 30 + "\n"
        
        for cmd in commands:
            formatted += f"{cmd['index']}. {cmd['command']}\n"
            if cmd.get('timestamp'):
                formatted += f"   Time: {cmd['timestamp']}\n"
        
        return formatted
