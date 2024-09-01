import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "c551fc8ee8b74104b0fa499d301d3ca4"




def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 



def aiProcess(command):
    client = OpenAI(api_key="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",

    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content


def processCommand(c):
   if "open google" in c.lower():
      webbrowser.open("https://google.com")

   elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
   elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
   elif  "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
   elif "open netflix" in c.lower():
        webbrowser.open("https://www.netflix.com/browse")
   elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
   elif "news" in c.lower():
       r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=c551fc8ee8b74104b0fa499d301d3ca4")
   if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
   
   

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # listen for the wake word "jarvis"

        r = sr.Recognizer()
       

        print("recognizing...")
        try:
             with sr.Microphone() as source:
                print("Listenig...")
                audio = r.listen(source, timeout=1, phrase_time_limit=2)

             word = r.recognize_google(audio)
             if(word.lower() == "jarvis"):
               speak("yes sir")
               #listen for command
               with sr.Microphone() as source:
                print("Jarvis Active...")
                audio = r.listen(source)
                command = r.recognize_google(audio)

                processCommand(command)



        
        except Exception as e:
            print("Error; {0}".format(e))

