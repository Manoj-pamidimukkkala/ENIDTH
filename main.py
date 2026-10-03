import os
import sys

from dotenv import load_dotenv
from google import genai
from vision import VisionEngine
from voice import VoiceEngine
from system_actions import SystemController

# Load environment configuration
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY or API_KEY == "your_actual_gemini_api_key_here":
    print("[Error] Please set your GEMINI_API_KEY in the .env file.")
    sys.exit(1)

# Initialize Client & Modules
client = genai.Client(api_key=API_KEY)
vision_engine = VisionEngine()
voice_engine = VoiceEngine()
sys_control = SystemController()

SYSTEM_PROMPT = """You are AURA, an AI companion capable of multimodal perception.
You can see through the user's webcam and assist with system control, environment observation, and daily tasks.
Keep your spoken responses concise, helpful, and natural."""

def process_prompt(user_input, attach_camera=False):
    """Sends multimodal prompt (text + optional image) to Gemini."""
    try:
        contents = []

        if attach_camera:
            print("[Camera] Capturing frame from webcam...")
            image = vision_engine.capture_frame()
            if image:
                contents.append(image)
                contents.append("Look at what is currently in front of the camera and answer the user's question.")
            else:
                voice_engine.speak("Webcam capture failed. Responding text-only.")

        contents.append(f"{SYSTEM_PROMPT}\nUser Request: {user_input}")

        # Multimodal request using latest API
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents
        )

        return response.text.strip()
    except Exception as e:
        print(f"[API Error]: {e}")
        return "I encountered an error processing your query."

def main():
    voice_engine.speak("AURA online. Vision, voice, and system control active.")

    while True:
        print("\n" + "="*50)
        print("AURA COMMAND MENU: [V] Voice Input | [T] Text Input | [C] See & Describe | [Q] Quit")
        choice = input("Select input method (V/T/C/Q): ").strip().upper()

        user_query = None
        attach_camera = False

        if choice == 'Q':
            voice_engine.speak("Shutting down. Goodbye!")
            break

        elif choice == 'V':
            user_query = voice_engine.listen()
            if not user_query:
                print("No voice input detected.")
                continue

        elif choice == 'T':
            user_query = input("\nType command for AURA: ").strip()

        elif choice == 'C':
            user_query = input("\nWhat should I look for through the camera? (Press Enter for general overview): ").strip()
            if not user_query:
                user_query = "Describe what you see in detail."
            attach_camera = True

        else:
            print("Invalid selection.")
            continue

        if user_query:
            # Check for local system action triggers
            action_result = sys_control.execute_command(user_query)
            if action_result:
                voice_engine.speak(action_result)
                continue

            # Query multimodal AI intelligence
            ai_response = process_prompt(user_query, attach_camera=attach_camera)
            voice_engine.speak(ai_response)

if __name__ == "__main__":
    main()
