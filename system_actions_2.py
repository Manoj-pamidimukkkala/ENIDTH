import os
import sys
import psutil
import webbrowser
import subprocess
import pyautogui

class SystemController:
    @staticmethod
    def get_system_health():
        """Returns live CPU, Memory, and Disk stats."""
        cpu = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        return f"CPU utilization is at {cpu}%, RAM memory at {memory}%, and primary storage at {disk}% capacity."

    @staticmethod
    def execute_gui_automation(action, *args):
        """Executes mouse and keyboard automation commands."""
        pyautogui.FAILSAFE = True
        try:
            if action == "type":
                pyautogui.write(" ".join(args), interval=0.03)
                return "Typed text into active window."
            elif action == "press":
                pyautogui.press(args[0])
                return f"Pressed {args[0]} key."
            elif action == "hotkey":
                pyautogui.hotkey(*args)
                return f"Executed key combination: {' + '.join(args)}"
            elif action == "screenshot":
                pyautogui.screenshot("screenshot_captured.png")
                return "Saved desktop screenshot as screenshot_captured.png."
        except Exception as e:
            return f"Automation error: {e}"

    @staticmethod
    def execute_command(command_text):
        """Parses intent and handles direct system execution."""
        cmd = command_text.lower()

        # System Health Diagnostics
        if "system status" in cmd or "cpu usage" in cmd or "memory usage" in cmd:
            return SystemController.get_system_health()

        # Navigation & Launching
        elif "open browser" in cmd or "open google" in cmd:
            webbrowser.open("https://google.com")
            return "Opening web browser."

        elif "open youtube" in cmd:
            webbrowser.open("https://youtube.com")
            return "Launching YouTube."

        elif "search for" in cmd or "google search" in cmd:
            query = cmd.replace("search for", "").replace("google search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching Google for {query}."

        # Desktop App Controls
        elif "open notepad" in cmd or "open editor" in cmd:
            app = 'notepad.exe' if sys.platform.startswith('win') else ('open -a TextEdit' if sys.platform.startswith('darwin') else 'gedit')
            subprocess.Popen(app, shell=True)
            return "Opening text editor."

        elif "open terminal" in cmd or "open prompt" in cmd:
            term = 'cmd.exe' if sys.platform.startswith('win') else ('open -a Terminal' if sys.platform.startswith('darwin') else 'xterm')
            subprocess.Popen(term, shell=True)
            return "Opening terminal."

        # GUI Hotkey Short-cuts
        elif "take screenshot" in cmd:
            return SystemController.execute_gui_automation("screenshot")

        elif "switch window" in cmd or "next window" in cmd:
            hotkey = ('alt', 'tab') if sys.platform.startswith('win') else ('command', 'tab')
            return SystemController.execute_gui_automation("hotkey", *hotkey)

        return None
