import os
import sys
import webbrowser
import subprocess

class SystemController:
    @staticmethod
    def execute_command(command_text):
        """Parses intent and executes desktop actions."""
        cmd = command_text.lower()

        # Web search & Browser Controls
        if "open browser" in cmd or "open youtube" in cmd:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube in browser."

        elif "search for" in cmd:
            query = cmd.split("search for")[-1].strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching Google for {query}."

        # Desktop Applications Launching (Cross-platform)
        elif "open notepad" in cmd or "open text editor" in cmd:
            if sys.platform.startswith('win'):
                subprocess.Popen(['notepad.exe'])
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', '-a', 'TextEdit'])
            else:
                subprocess.Popen(['gedit'])
            return "Opening text editor."

        elif "open terminal" in cmd or "open command prompt" in cmd:
            if sys.platform.startswith('win'):
                subprocess.Popen(['cmd.exe'])
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', '-a', 'Terminal'])
            else:
                subprocess.Popen(['xterm'])
            return "Opening Terminal."

        return None
