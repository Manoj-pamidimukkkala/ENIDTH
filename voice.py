import speech_recognition as sr
import pyttsx3
import threading

class VoiceEngine:
    def __init__(self):
        # Initialize Text-to-Speech Engine
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 180)  # Speaking speed
        voices = self.tts.getProperty('voices')
        if len(voices) > 1:
            self.tts.setProperty('voice', voices[1].id) # Female/Alternative voice if available

        # Initialize Speech Recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000

    def speak(self, text):
        """Non-blocking text-to-speech engine."""
        print(f"\n[AURA]: {text}")
        def _say():
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        threading.Thread(target=_say).start()

    def listen(self):
        """Listens to microphone and converts audio to text."""
        with sr.Microphone() as source:
            print("\n[Listening...] Speak now or type command below.")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                command = self.recognizer.recognize_google(audio)
                print(f"[You (Voice)]: {command}")
                return command
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("[Voice] Could not understand audio speech.")
                return None
            except Exception as e:
                print(f"[Voice Error]: {e}")
                return None
