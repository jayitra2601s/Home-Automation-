import speech_recognition as s
import time
import pyttsx3 

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommand(): 

    sr = s.Recognizer()
    with s.Microphone() as source:  
        print("Listening......") 
        sr.energy_threshold = 500  
        audio = sr.listen(source)  

    try: 
        print("Recognizing......")  
        query = sr.recognize_google(audio, language='en-IN') 
        print("\nYou said: ", query)   
   
    except Exception as e:
        print("Say that again Please... I can't hear clearly...") 
        time.sleep(1)  
        return "None" 

    return query


if __name__ == "__main__":
    while True:
        query = takeCommand().lower()

        print(query)
        speak(query)