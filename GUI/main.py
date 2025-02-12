import os
import subprocess as sp
from datetime import datetime
from random import choice
import pyttsx3
import speech_recognition as sr
import wolframalpha
import webbrowser
import imdb
from decouple import config
import keyboard

from conv import random_text
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast

# Initialize pyttsx3
engine = pyttsx3.init()
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 220)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

USER = config('USER')
HOSTNAME = config('BOT')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_me():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good morning {USER}")
    elif 12 <= hour < 16:
        speak(f"Good afternoon {USER}")
    elif 16 <= hour < 19:
        speak(f"Good evening {USER}")
    speak(f"I am {HOSTNAME}. How may I assist you? {USER}")

listening = False

def start_listening():
    global listening
    listening = True
    print("Started listening")

def pause_listening():
    global listening
    listening = False
    print("Stopped listening")

keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(query)
        if 'stop' not in query and 'exit' not in query:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if 21 <= hour < 6:
                speak("Good night sir, take care!")
            else:
                speak("Have a good day sir!")
            exit()
    except Exception:
        speak("Sorry I couldn't understand. Can you please repeat that?")
        query = 'None'
    return query

if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak("I am absolutely fine sir. What about you")

            elif "open terminal" in query:
                speak("Opening Terminal")
                os.system('open -a Terminal')

            elif "open camera" in query:
                speak("Opening camera sir")
                sp.run('open /System/Applications/Photo\\ Booth.app', shell=True)

            elif "open notepad" in query:
                speak("Opening TextEdit for you sir")
                os.system('open -a TextEdit')

            elif "open discord" in query:
                speak("Opening Discord for you sir")
                discord_path = "/Applications/Discord.app"
                os.system(f'open {discord_path}')

            elif 'ip address' in query:
                ip_address = find_my_ip()
                speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                print(f'Your IP Address is {ip_address}')

            elif "open youtube" in query:
                speak("What do you want to play on YouTube sir?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak(f"What do you want to search on Google {USER}")
                query = take_command().lower()
                search_on_google(query)

            elif "wikipedia" in query:
                speak("What do you want to search on Wikipedia sir?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to Wikipedia, {results}")
                speak("I am printing it on the terminal")
                print(results)

            elif "send an email" in query:
                speak("On what email address do you want to send sir? Please enter in the terminal")
                receiver_add = input("Email address: ")
                speak("What should be the subject sir?")
                subject = take_command().capitalize()
                speak("What is the message?")
                message = take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("Something went wrong. Please check the error log")

            elif "give me news" in query:
                speak(f"I am reading out the latest headlines of today, sir")
                speak(get_news())
                speak("I am printing it on the screen sir")
                print(*get_news(), sep='\n')

