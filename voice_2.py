import speech_recognition as sr
import pyttsx3
import threading
import os

class VoiceEngine:
    def __init__(self, wake_word="aura"):
        self.wake_word = wake_word.lower()
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 3000
        self.recognizer.dynamic_energy_threshold = True

    def speak(self, text):
        """Non-blocking asynchronous voice synthesizer."""
        print(f"\n[AURA]: {text}")
        def _speech_thread():
            engine = pyttsx3.init()
            engine.setProperty('rate', int(os.getenv("DEFAULT_SPEECH_RATE", 180)))
            voices = engine.getProperty('voices')
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id)
            engine.say(text)
            engine.runAndWait()

        threading.Thread(target=_speech_thread, daemon=True).start()

    def listen(self, timeout=6):
        """Listens via microphone and converts speech to string."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                print(f"[Speech Detected]: {text}")
                return text
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                return None
            except Exception as e:
                print(f"[Mic Error]: {e}")
                return None

    def listen_for_wake_word(self):
        """Continuously monitors microphone stream for the wake keyword."""
        print(f"\n[Passive Monitoring] Listening for wake word: '{self.wake_word}'...")
        while True:
            spoken = self.listen(timeout=4)
            if spoken and self.wake_word in spoken.lower():
                self.speak("System listening.")
                # Extract prompt following wake word if present
                parts = spoken.lower().split(self.wake_word, 1)
                return parts[1].strip() if len(parts) > 1 and parts[1].strip() else True
