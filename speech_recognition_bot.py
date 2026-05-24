import os
import subprocess
import psutil
import re
import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Speak out the response"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice input and convert to text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("SystemBot: Sorry, I didn’t catch that.")
        return ""
    except sr.RequestError:
        print("SystemBot: Speech service unavailable.")
        return ""

def get_intent(user_input):
    """Simple NLP intent recognition using regex"""
    user_input = user_input.lower()

    if re.search(r"(open|launch|start).*browser", user_input):
        return "open_browser"
    elif re.search(r"(cpu|processor).*usage", user_input):
        return "cpu_usage"
    elif re.search(r"(quit|exit|stop)", user_input):
        return "quit"
    else:
        return "unknown"

def chatbot():
    speak("SystemBot ready. Say 'quit' to exit.")
    while True:
        user_input = listen()
        if not user_input:
            continue

        intent = get_intent(user_input)

        if intent == "quit":
            speak("Goodbye!")
            break

        elif intent == "open_browser":
            subprocess.run(["start", "chrome"], shell=True)  # Windows example
            speak("Opening your browser...")

        elif intent == "cpu_usage":
            usage = psutil.cpu_percent(interval=1)
            response = f"Current CPU usage is {usage} percent."
            print(response)
            speak(response)

        else:
            speak("I didn’t understand that command. Try again.")

if __name__ == "__main__":
    chatbot()
