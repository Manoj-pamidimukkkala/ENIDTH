import os
import sys
from dotenv import load_dotenv
from google import genai

from vision import VisionEngine
from voice import VoiceEngine
from system_actions import SystemController
from file_manager import FileManager

# Initialization & Config Validation
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY or API_KEY == "your_gemini_api_key_here":
    print("[Error] Please set your GEMINI_API_KEY inside the .env file.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
vision_engine = VisionEngine(camera_index=int(os.getenv("CAMERA_INDEX", 0)))
voice_engine = VoiceEngine(wake_word=os.getenv("WAKE_WORD", "aura"))

SYSTEM_PROMPT = """You are AURA, an advanced personal multimodal desktop AI assistant.
You possess real-time vision capabilities (webcam and live screen capture), system control mechanisms, and voice output.
Keep all spoken audio responses concise, smart, direct, and actionable."""

def process_ai_query(user_prompt, camera_feed=False, screen_feed=False):
    """Pipeline handling textual, visual, and screen context for Gemini 2.5."""
    try:
        contents = []

        if camera_feed:
            print("[Perception] Capturing webcam feed...")
            img = vision_engine.capture_webcam()
            if img:
                contents.append(img)
                contents.append("Analyze what is visible through the camera.")

        if screen_feed:
            print("[Perception] Capturing screen monitor feed...")
            screen_img = vision_engine.capture_screen()
            if screen_img:
                contents.append(screen_img)
                contents.append("Look at the user's current computer display screen to assist them.")

        contents.append(f"{SYSTEM_PROMPT}\nUser Prompt: {user_prompt}")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )
        return response.text.strip()

    except Exception as e:
        print(f"[API Processing Error]: {e}")
        return "I encountered an issue processing your request through the AI engine."

def run_assistant():
    voice_engine.speak("AURA Multimodal Assistant v2 active. Vision, Screen, and Voice systems initialized.")

    while True:
        print("\n" + "="*60)
        print("AURA MODE SELECTOR:")
        print("[W] Wake Word Continuous Mode | [T] Text Command | [C] Camera Perception | [S] Screen Vision | [Q] Quit")
        choice = input("Enter Selection (W/T/C/S/Q): ").strip().upper()

        user_query = None
        use_camera = False
        use_screen = False

        if choice == 'Q':
            voice_engine.speak("Deactivating system modules. Goodbye!")
            break

        elif choice == 'W':
            result = voice_engine.listen_for_wake_word()
            if isinstance(result, str):
                user_query = result
            elif result is True:
                user_query = voice_engine.listen(timeout=7)

            if not user_query:
                print("No active voice payload received.")
                continue

        elif choice == 'T':
            user_query = input("\nType command: ").strip()

        elif choice == 'C':
            user_query = input("\nCamera query (e.g. 'What am I holding?'): ").strip()
            if not user_query:
                user_query = "Describe what is visible through the camera."
            use_camera = True

        elif choice == 'S':
            user_query = input("\nScreen context query (e.g. 'Summarize this document/code'): ").strip()
            if not user_query:
                user_query = "Analyze the open windows on my screen."
            use_screen = True

        else:
            print("Invalid input selection.")
            continue

        if user_query:
            # 1. Custom File Automation
            if "find file" in user_query.lower() or "search file" in user_query.lower():
                fname = user_query.lower().replace("find file", "").replace("search file", "").strip()
                res = FileManager.search_files(fname)
                voice_engine.speak(res)
                continue

            elif "take note" in user_query.lower() or "save note" in user_query.lower():
                note = user_query.lower().replace("take note", "").replace("save note", "").strip()
                res = FileManager.create_quick_note(note)
                voice_engine.speak(res)
                continue

            # 2. Local OS Actions Execution
            action_output = SystemController.execute_command(user_query)
            if action_output:
                voice_engine.speak(action_output)
                continue

            # 3. Multimodal AI Processing
            response_text = process_ai_query(user_query, camera_feed=use_camera, screen_feed=use_screen)
            voice_engine.speak(response_text)

if __name__ == "__main__":
    run_assistant()
