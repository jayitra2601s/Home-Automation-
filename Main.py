# Importing all necessary Module 
import sys
import dotenv
import os
import time
import subprocess
import signal
import pyttsx3
import time
import random
import math
import speedtest
import pyjokes
import requests
import pywhatkit
import speech_recognition as s
import pyautogui as py

from datetime import datetime
from random import choice
from decouple import config
from tkinter import messagebox

# Importing PyQt5 Module
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import QThread, pyqtSignal

# Importing the PyFirmata module for the arduino board
from pyfirmata2 import Arduino, OUTPUT

from utills import opening_text
from check import FindArduino

# Read data from the ENV (.env) file
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)  

# Storing all data that are read from the ".env" file into variables
# Configuring data using config function from the decouple module
USERNAME = config('USER', default='Username')
BOTNAME = config('BOT', default='Botname')
MASTER = config('MASTER', default='None')
port1 = config('PORT1', default='port 1')
port2 = config('PORT2', default='port 2')
port3 = config('PORT3', default='port 3')
port4 = config('PORT4', default='port 4')
port5 = config('PORT5', default='port 5')
port6 = config('PORT6', default='port 6')
port7 = config('PORT7', default='port 7')
port8 = config('PORT8', default='port 8')
port9 = config('PORT9', default='port 9')

# Running the FindArduino() func. imported from the "Check.py" file
FindArduino()
COMPORT = config('COMPORT', default='None')

# Checking if the Arduino board is connected or not
# If yes then defining the Arduino board with its output pins
if "None" not in COMPORT:      
    board = Arduino(COMPORT)
    board.digital[2].mode = OUTPUT
    board.digital[3].mode = OUTPUT
    board.digital[4].mode = OUTPUT
    board.digital[5].mode = OUTPUT
    board.digital[6].mode = OUTPUT
    board.digital[7].mode = OUTPUT
    board.digital[8].mode = OUTPUT
    board.digital[9].mode = OUTPUT
    board.digital[10].mode = OUTPUT
    board.digital[2].write(0)
    board.digital[3].write(0)
    board.digital[4].write(0)
    board.digital[5].write(0)
    board.digital[6].write(0)
    board.digital[7].write(0)
    board.digital[8].write(0)
    board.digital[9].write(0)
    board.digital[10].write(0)

    board.digital[11].mode = OUTPUT   #Blue led
    board.digital[12].mode = OUTPUT   #Green led
    board.digital[13].mode = OUTPUT   #Red led


# API key for GNews API
apikey = '0d7edb17e23a6878cdbf1306a0494330'


# Calling sapi5 for text to speech conversion 
engine = pyttsx3.init('sapi5')
# Set voice (Male/Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# Set the voice speech rate
engine.setProperty('rate', 170)
# Defining the Speak function to convert text into audio
def speak(audio):
    disable_stop(main_screen, True)
    engine.say(audio)
    engine.runAndWait()
    

def disable_stop(main_screen_instance, is_disable):
    if is_disable:
        main_screen_instance.stop.setEnabled(False)
    else:
        main_screen_instance.stop.setEnabled(True)



# This uses to greet the current User
current_time = int(time.strftime('%H'))
if current_time >= 4 and current_time < 11:
    welcome="Good Morning  ☀"
elif current_time >= 11 and current_time < 15:
    welcome = "Good Noon  ☀"
elif current_time >= 15 and current_time < 18:
    welcome = "Good Afternoon 🌤️"
elif current_time >= 18 and current_time <= 21:
    welcome = "Good Evening  🌙"
else:
    welcome = "Good Night  🌙"


# Defining the Main window with functions and the UI

class MainScreen(QDialog):  # Callig QDialog from the PyQt5 module
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("Main.ui", self)  # Declareing the UI file for the Main window
        
        # self.setWindowIcon(QIcon('icon.png'))
        # # setting icon text
        # self.setWindowIconText("logo")

        self.thread = {}  # Creating the Dictionary

        self.greeting.setText(welcome)
        self.greet_user.setText(USERNAME + "  :)")  # Greeting the user

        # Using setCursor function to change the mouse pointer
        self.settings.setCursor(QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.reset.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.play.setCursor(QCursor(QtCore.Qt.PointingHandCursor))  
        self.stop.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.view_code.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.reboot.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.exit.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        

        # Using clicked.connect function to connect a specific function with a button
        # Connecting all buttons with its specified function 
        self.settings.clicked.connect(self.gotologin)
        self.reset.clicked.connect(self.reset_env)
        self.play.clicked.connect(self.call_ai)
        self.stop.clicked.connect(self.deactivate_ai)
        self.view_code.clicked.connect(self.ViewCode)
        self.reboot.clicked.connect(self.Reboot)
        self.exit.clicked.connect(self.Exit)
        # Using setEnabled to enable or disable any button passing the bool argument
        self.stop.setEnabled(False)


        if 'None' in COMPORT:  

            self.play.setEnabled(False) 
            self.label_8.setEnabled(False)
            self.stop.setEnabled(False)
            self.label_9.setEnabled(False)
            # messagebox.showerror() basically shows the error window
            messagebox.showerror("Arduino error*", "# No Arduino Board is found, connect your arduino first...")
            # Using setText function to display any text in the Main UI by the Label name
            self.error1.setText("# Error with the Arduino board... Click on view code &")
            self.error.setText("upload the code into the Arduino Board...")
            self.view_code.setGeometry(420, 210, 111, 31)

        else:
            self.play.setEnabled(True)



    # Declaring a function that will reset all data in the .env file
    def reset_env(self):    
        os.environ["USER"] = "Username"   # Reset to data
        os.environ["MASTER"] = "None"
        os.environ["BOT"] = "Botname"
        dotenv.set_key(dotenv_file, "USER", os.environ["USER"])
        dotenv.set_key(dotenv_file, "MASTER", os.environ["MASTER"])
        dotenv.set_key(dotenv_file, "BOT", os.environ["BOT"])
        
        for i in range (1, 10):    
            os.environ[(f"PORT{i}")] = (f"port {i}")
            dotenv.set_key(dotenv_file, (f"PORT{i}"), os.environ[(f"PORT{i}")])
            i = i+1
        
        # That basically used to restart the code
        current_pid = os.getpid()
        subprocess.Popen([sys.executable, 'Main.py'])
        os.kill(current_pid, signal.SIGTERM)



    # Declaring a function that Call the another .ui file
    def gotologin(self):
        login = LoginScreen()  # Calling the LoginScreen class 
        widget.addWidget(login)
        widget.setFixedHeight(621)
        widget.setFixedWidth(891)
        widget.setCurrentIndex(widget.currentIndex()+1)  # Set index for calling the another ui


    # Calling the main function 
    def call_ai(self):  # Start the main function in background by using thread 
        self.thread[1] = MainThread(parent=None, index=1)  # Calling the main function using thread 
        self.thread[1].start()  # By using thread.start() we can call the thread 

        self.status.setGeometry(10, 210, 541, 31)
        self.green.setGeometry(140, 200, 31, 41)
        self.blue.setGeometry(270, 200, 31, 41)
        self.red.setGeometry(420, 200, 31, 41)
        self.reset.setEnabled(False)
        self.label_6.setEnabled(False)
        self.settings.setEnabled(False)
        self.label_7.setEnabled(False)
        self.play.setEnabled(False)
        self.label_8.setEnabled(False)

        self.stop.setEnabled(True)
   


    # Deactivating the main function
    def deactivate_ai(self): # Stop the running thread
        self.status.setGeometry(10, 370, 541, 31)
        self.green.setGeometry(140, 360, 31, 41)
        self.blue.setGeometry(270, 360, 31, 41)
        self.red.setGeometry(420, 360, 31, 41)
        self.reset.setEnabled(True)
        self.label_6.setEnabled(True)
        self.settings.setEnabled(True)
        self.label_7.setEnabled(True)
        self.play.setEnabled(True)
        self.label_8.setEnabled(True)
        self.stop.setEnabled(False)
        self.thread[1].stop()  # By using thread.stop() we can stop the thread 



    def ViewCode(self):  # Appear a option to view the Arduino code
        dir = os.getcwd()
        print(dir)
        code_dir = os.path.join(dir, "Code")
        print("Code Directory Path:", code_dir)

        if os.path.exists(code_dir):
            os.startfile(code_dir)  # Open the file location in Windows Explorer
        else:
            print("Error: Specified path does not exist.")

        self.view_code.setGeometry(580, 190, 111, 31)
        self.reboot.setGeometry(290, 210, 111, 31)
        self.exit.setGeometry(420, 210, 111, 31)
        self.error1.setText("After uploading you can tap on the restart button &")
        self.error.setText("restart the application...")
 


    def Reboot(self):  # Restart function
        current_pid = os.getpid()
        print(current_pid)
        subprocess.Popen([sys.executable, 'Main.py'])
        os.kill(current_pid, signal.SIGTERM)



    def Exit(self):  # Exit the application
        sys.exit(app.exec_())   

            


class LoginScreen(QDialog):  # Display the login screen
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("Login.ui", self)  # Load the .ui file

        self.continue1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.male.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.female.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.back_button1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.continue1.clicked.connect(self.loginfunction)  

        # If any changes is needed to the settings then execute
        if "Username" not in USERNAME and "None" not in MASTER:
            self.welcome.setText(f"Welcome {MASTER},")
            self.information.setText("  Make whatever changes you want")
            self.tabname.setText("⚙ Settings")
            self.back_button1.clicked.connect(self.gotomain)
            self.back_button1.setGeometry(10, 570, 41, 41)
            self.back_button1_text.setGeometry(60, 570, 51, 41)
            
        if "Username" not in USERNAME:
            self.username.setText(USERNAME)
        if "Botname" not in BOTNAME:
            self.botname.setText(BOTNAME)
        if "Sir" in MASTER:
            self.male.setChecked(True)   # Used to select default data
        elif "Mam" in MASTER:
            self.female.setChecked(True)     
       

    def loginfunction(self):    # For the new User 
        user = self.username.text()   # text() is used to read text what user has entered
        bot = self.botname.text()

        if len(user) == 0:
            self.err1.setText("*(This field is required)")   # Shows the necessary fields
        if len(bot) == 0:
            self.err3.setText("*(This field is required)")           
        if self.male.isChecked() == True:
            som = "Sir"
        elif self.female.isChecked() == True:
            som = "Mam"
        else:
            som = "None"
            self.err2.setText("*(This field is required)")
        
        if len(user) != 0 and len(bot) != 0 and 'None' not in som:
            os.environ["USER"] = user
            os.environ["MASTER"] = som
            os.environ["BOT"] = bot
            dotenv.set_key(dotenv_file, "USER", os.environ["USER"])
            dotenv.set_key(dotenv_file, "MASTER", os.environ["MASTER"])
            dotenv.set_key(dotenv_file, "BOT", os.environ["BOT"])

            self.all_port()   # Call the new .ui file via function 
            
        else:
            print("Please check all required field")


    def gotomain(self):   # Call the main screen 
        main_screen = MainScreen()
        widget.addWidget(main_screen)
        widget.setFixedHeight(311)   # Height of the UI
        widget.setFixedWidth(551)   # Width of the UI
        widget.setCurrentIndex(widget.currentIndex()-1)   # Call priveous ui by setting the index 


    def all_port(self):   # Call the next scrren i.e. UiScreen
        ports = UiScreen()
        widget.addWidget(ports)
        widget.setFixedHeight(681)   # Height of the UI
        widget.setFixedWidth(961)   # Width of the UI
        widget.setCurrentIndex(widget.currentIndex()+1)   # Call next ui by setting the index 



class UiScreen(QDialog):  # Open the another .ui file 
    def __init__(self):
        super(UiScreen, self).__init__()
        loadUi("GUI.ui", self)   # Load file

        self.save.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.exit.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.back_button2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        if 'Sir' in MASTER:
            self.hello_user.setText("Hello Sir...")   
            self.port_tabname.setText("⚙ Settings")
        elif 'Mam' in MASTER:
            self.hello_user.setText("Hello Mam...")
            self.port_tabname.setText("⚙ Settings")
        else:
            self.change_portname.setText("Create name for all Arduino ports & Click on Save")
        if 'None' not in MASTER:
            self.save.setText("Save Changes")
            self.back_button2.setGeometry(10, 630, 41, 41)
            self.back_button2_text.setGeometry(60, 630, 51, 41)
            self.back_button2.clicked.connect(self.gotologin)   # Back to the previous UI

        self.save.clicked.connect(self.save_restart)   # Restart the application
        self.exit.clicked.connect(self.exitapp)   # Exit the application

        # Set the default text
        self.port1.setText(port1)
        self.port2.setText(port2)
        self.port3.setText(port3)
        self.port4.setText(port4)
        self.port5.setText(port5)
        self.port6.setText(port6)
        self.port7.setText(port7)
        self.port8.setText(port8)
        self.port9.setText(port9)


    def gotologin(self):   # Go back to the login page
        login = LoginScreen()
        widget.addWidget(login)
        widget.setFixedHeight(621)   # Height of the UI
        widget.setFixedWidth(891)   # Width of the UI
        widget.setCurrentIndex(widget.currentIndex()-1)   # Call the previous UI


    def save_restart(self):
        
        port1 = self.port1.text().lower()
        os.environ["PORT1"] = port1
        if len(port1) != 0:
            dotenv.set_key(dotenv_file, "PORT1", os.environ["PORT1"])
        else:
            dotenv.set_key(dotenv_file, "PORT1", "port1")

        port2 = self.port2.text().lower()
        os.environ["PORT2"] = port2
        if len(port2) != 0:
            dotenv.set_key(dotenv_file, "PORT2", os.environ["PORT2"])
        else:
            dotenv.set_key(dotenv_file, "PORT2", "port2")

        port3 = self.port3.text().lower()
        os.environ["PORT3"] = port3
        if len(port3) != 0:
            dotenv.set_key(dotenv_file, "PORT3", os.environ["PORT3"])
        else:
            dotenv.set_key(dotenv_file, "PORT3", "port3")

        port4 = self.port4.text().lower()
        os.environ["PORT4"] = port4
        if len(port4) != 0:
            dotenv.set_key(dotenv_file, "PORT4", os.environ["PORT4"])
        else:
            dotenv.set_key(dotenv_file, "PORT4", "port4")

        port5 = self.port5.text().lower()
        os.environ["PORT5"] = port5
        if len(port5) != 0:
            dotenv.set_key(dotenv_file, "PORT5", os.environ["PORT5"])
        else:
            dotenv.set_key(dotenv_file, "PORT5", "port5")

        port6 = self.port6.text().lower()
        os.environ["PORT6"] = port6
        if len(port6) != 0:
            dotenv.set_key(dotenv_file, "PORT6", os.environ["PORT6"])
        else:
            dotenv.set_key(dotenv_file, "PORT6", "port6")

        port7 = self.port7.text().lower()
        os.environ["PORT7"] = port7
        if len(port7) != 0:
            dotenv.set_key(dotenv_file, "PORT7", os.environ["PORT7"])
        else:
            dotenv.set_key(dotenv_file, "PORT7", "port7")

        port8 = self.port8.text().lower()
        os.environ["PORT8"] = port8
        if len(port8) != 0:
            dotenv.set_key(dotenv_file, "PORT8", os.environ["PORT8"])
        else:
            dotenv.set_key(dotenv_file, "PORT8", "port8")                           

        port9 = self.port9.text().lower()
        os.environ["PORT9"] = port9
        if len(port9) != 0:
            dotenv.set_key(dotenv_file, "PORT9", os.environ["PORT9"])
        else:
            dotenv.set_key(dotenv_file, "PORT9", "port9")
        
        # Call massagebox and take input
        answer = messagebox.askquestion("Save","Data saved sucessfully! \nDo you want to restart the application ?")
        if answer == 'yes':   # Restart the application 
            os.environ["COMPORT"] = "None"
            dotenv.set_key(dotenv_file, "COMPORT", os.environ["COMPORT"])

            current_pid = os.getpid()
            subprocess.Popen([sys.executable, 'Main.py'])
            os.kill(current_pid, signal.SIGTERM)
        else:
            sys.exit(app.exec())   # Exit the application


    def exitapp(self):   # Function to exit the application
        sys.exit(app.exec())




class MainThread(QThread):  # Calling thread in  class
    any_signal = pyqtSignal(int)

    def __init__(self, parent=None, index=0):
        super(MainThread, self).__init__(parent)
        self.index = index  # set index of current object
        self.is_running = True   # To run self


    def run(self):  # Main function, execute by using QThread 
        print("Start... ", self.index)
        self.MainTask()  # Calling the function


    def stop(self):  # Stop the running QThread
        hour = datetime.now().hour
        if hour >= 22 and hour < 5:
            speak(f"Good night {MASTER}, Take care!")
        elif hour >= 5 and hour <= 16:
            speak(f'Thanks for using me! Have a good day {MASTER}!')
        else:
            speak(f'Thanks for using me {MASTER}, Take care!')
        board.digital[11].write(0)
        board.digital[12].write(0)
        board.digital[13].write(0)
        self.is_running = False
        engine.stop()
        print("Stop... ", self.index)
        self.terminate()  # Asking OS to kill the thread process


    def greet(self):  # Greeting the user according to the time
        hour = int(datetime.now().hour)
        if hour>=4 and hour<13:
            speak(f"Good Morning {USERNAME}")
        elif hour>=13 and hour<15:
            speak(f"Good Noon {USERNAME}")
        elif hour>=15 and hour<18:
            speak(f"Good Afternoon {USERNAME}")
        elif hour>=18 and hour<=20:
            speak(f"Good Evening {USERNAME}")
        else:
            speak(f"Good Night {USERNAME}")
        speak(f"I am {BOTNAME}, your personal home AI assistant. I am here to asist you. Please tell me how can I help you?")  # Introduce


    def listen(self):   
        # It confirms AI is listening us
        board.digital[11].write(0)  # Turning on the green LED
        board.digital[12].write(1)
        board.digital[13].write(0)

    def recognize(self):
        # It confirms AI is recognizing what we said
        board.digital[11].write(1)
        board.digital[12].write(0)  # Turning on the blue LED
        board.digital[13].write(0)

    def execute(self):
        # It confirms AI is working on our command
        board.digital[11].write(0)
        board.digital[12].write(0)  # Turning on the red LED
        board.digital[13].write(1)


    def takeCommand(self):  # Creating a function that takes command from user
        disable_stop(main_screen, False)
        sr = s.Recognizer()
          # Calling the speech recognition module 
        with s.Microphone() as source:  # Use default microphone to listen
            self.listen()  # LED status
            print("Listening......") 
            sr.energy_threshold = 500  # To increase or decrease microphone's sensetivity 
            sr.pause_threshold = 1
            audio = sr.listen(source)  # l
        try: 
            self.recognize()  # LED status
            print("Recognizing......")  
            query = sr.recognize_google(audio, language='en-IN')  # Recognized audio stored into a variable 
        except Exception as e:
            print("Say that again Please... I can't hear clearly...")  # Print error AI does not recognize us
            time.sleep(1)  # Sleep the program for 1 second
            return "None" 

        return query

    def regional_news(self):
        speak ("which types of news you want to listen now... business, entertainment, general, health, science, sports, or technology")
        query = self.takeCommand().lower()
        speak(f"Wait {MASTER}, finding the latest newz for you")
        if 'business' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&country=in&max=10&apikey={apikey}"
        elif 'entertainment' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=entertainment&lang=en&country=in&max=10&apikey={apikey}"
        elif 'general' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=general&lang=en&country=in&max=10&apikey={apikey}"
        elif 'health' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=health&lang=en&country=in&max=10&apikey={apikey}"
        elif 'science' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=science&lang=en&country=in&max=10&apikey={apikey}"
        elif 'sports' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=sports&lang=en&country=in&max=10&apikey={apikey}"
        elif 'technology' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=technology&lang=en&country=in&max=10&apikey={apikey}"

        return url

    
    def world_news(self):
        speak ("which types of news you want to listen now...business, entertainment, general, health, science, sports, or technology")
        query = self.takeCommand().lower()
        speak(f"Wait {MASTER}, finding the latest newz for you")
        if 'business' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=business&lang=en&max=10&apikey={apikey}"
        elif 'entertainment' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=entertainment&lang=en&max=10&apikey={apikey}"
        elif 'general' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=general&lang=en&max=10&apikey={apikey}"
        elif 'health' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=health&lang=en&max=10&apikey={apikey}"
        elif 'science' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=science&lang=en&max=10&apikey={apikey}"
        elif 'sports' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=sports&lang=en&max=10&apikey={apikey}"
        elif 'technology' in query:
            url = f"https://gnews.io/api/v4/top-headlines?category=technology&lang=en&max=10&apikey={apikey}"
        
        return url
    



    def MainTask(self):
        
        try:
            self.greet()
            while True:
                query = self.takeCommand().lower()  # Calling the takeCommand() func.
                print("\nYou said: ", query)  
                self.execute()  # LED status
            
                if 'the time' in query:
                    Time = datetime.now().strftime("%Ho%M:%p")  # Specifies the current tieme
                    speak(f"{MASTER}, the time is {Time}")

                elif 'the date' in query:
                    if 'date and time' in query:  # Current date & time
                        now = datetime.now()
                        date = now.strftime("%d")
                        month = now.strftime("%B")
                        year = now.strftime("%Y")
                        hour = now.strftime("%I")
                        minn = now.strftime("%M")
                        apm = now.strftime("%p")
                        speak(f"{MASTER}! the date is {date}... {month} {year} an the time is {hour} {minn} {apm}")
                    else:
                        Date = datetime.now().strftime("%d:%B:%Y")  # Today date
                        speak(f"{MASTER},the date is {Date}") 

                elif 'hello' in query:
                    speak(f"hello {MASTER}! Tell me what can I do for you")
                    # speak(choice(opening_text))


                # ALL funtions to turn on or off the ports 
                elif (f"{port1} on") in query or (f"on {port1}") in query or (f"on the {port1}") in query:
                    speak(choice(opening_text))    # Speak a random string from the list
                    speak(f"Turning on the {port1}")
                    board.digital[2].write(1)    # Output 1 to the arduino pin  
                    speak(f"Turned on the {port1} successfully...")
                elif (f"{port1} off") in query or (f"off {port1}") in query or (f"off the {port1}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning off the {port1}")
                    board.digital[2].write(0)    # Output 0 to the arduino pin
                    speak(f"Turned off the {port1} successfully...")

                
                elif (f"{port2} on") in query or (f"on {port2}") in query or (f"on the {port2}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning on the {port2}")
                    board.digital[3].write(1)    # Output 1 to the arduino pin 
                    speak(f"Turned on the {port2} successfully...")
                elif (f"{port2} off") in query or (f"off {port2}") in query or (f"off the {port2}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning off the {port2}")
                    board.digital[3].write(0)    # Output 0 to the arduino pin
                    speak(f"Turned off the {port2} successfully...")


                elif (f"{port3} on") in query or (f"on {port3}") in query or (f"on the {port3}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning on the {port3}")
                    board.digital[4].write(1)    # Output 1 to the arduino pin 
                    speak(f"Turned on the {port3} successfully...")
                elif (f"{port3} off") in query or (f"off {port3}") in query or (f"off the {port3}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning off the {port3}")
                    board.digital[4].write(0)    # Output 0 to the arduino pin
                    speak(f"Turned off the {port3} successfully...")


                elif (f"{port4} on") in query or (f"on {port4}") in query or (f"on the {port4}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning on the {port4}")
                    board.digital[5].write(1)    # Output 1 to the arduino pin 
                    speak(f"Turned on the {port4} successfully...")
                elif (f"{port4} off") in query or (f"off {port4}") in query or (f"off the {port4}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning off the {port4}")
                    board.digital[5].write(0)    # Output 0 to the arduino pin
                    speak(f"Turned off the {port4} successfully...")
                    

                elif (f"{port5} on") in query or (f"on {port5}") in query or (f"on the {port5}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning on the {port5}")
                    board.digital[6].write(1)    # Output 1 to the arduino pin 
                    speak(f"Turned on the {port5} successfully...")
                elif (f"{port5} off") in query or (f"off {port5}") in query or (f"off the {port5}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning off the {port5}")
                    board.digital[6].write(0)    # Output 0 to the arduino pin
                    speak(f"Turned off the {port5} successfully...")
                    

                elif (f"{port6} on") in query or (f"on {port6}") in query or (f"on the {port6}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning on the {port6}")
                    board.digital[7].write(1)    # Output 1 to the arduino pin 
                    speak(f"Turned on the {port6} successfully...")
                elif (f"{port6} off") in query or (f"off {port6}") in query or (f"off the {port6}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning off the {port6}")
                    board.digital[7].write(0)    # Output 0 to the arduino pin
                    speak(f"Turned off the {port6} successfully...")

                    
                elif (f"{port7} on") in query or (f"on {port7}") in query or (f"on the {port7}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning on the {port7}")
                    board.digital[8].write(1)    # Output 1 to the arduino pin 
                    speak(f"Turned on the {port7} successfully...")
                elif (f"{port7} off") in query or (f"off {port7}") in query or (f"off the {port7}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning off the {port7}")
                    board.digital[8].write(0)    # Output 0 to the arduino pin
                    speak(f"Turned off the {port7} successfully...")


                elif (f"{port8} on") in query or (f"on {port8}") in query or (f"on the {port8}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning on the {port8}")
                    board.digital[9].write(1)    # Output 1 to the arduino pin 
                    speak(f"Turned on the {port8} successfully...")
                elif (f"{port8} off") in query or (f"off {port8}") in query or (f"off the {port8}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning off the {port8}")
                    board.digital[9].write(0)    # Output 0 to the arduino pin
                    speak(f"Turned off the {port8} successfully...")

                    
                elif (f"{port9} on") in query or (f"on {port9}") in query or (f"on the {port9}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning on the {port9}")
                    board.digital[10].write(1)    # Output 1 to the arduino pin 
                    speak(f"Turned on the {port9} successfully...")
                elif (f"{port9} off") in query or (f"off {port9}") in query or (f"off the {port9}") in query:
                    speak(choice(opening_text))
                    speak(f"Turning off the {port9}")
                    board.digital[10].write(0)    # Output 0 to the arduino pin
                    speak(f"Turned off the {port9} successfully...")


                elif 'turn on all' in query:
                    speak(choice(opening_text))
                    speak(random.choice(["Turning on all of your appliances...", "Turning on all of your gadgets..."]))
                    board.digital[2].write(1)   # Output 1 to the arduino pin 
                    board.digital[3].write(1)   # Output 1 to the arduino pin 
                    board.digital[4].write(1)   # Output 1 to the arduino pin 
                    board.digital[5].write(1)   # Output 1 to the arduino pin 
                    board.digital[6].write(1)   # Output 1 to the arduino pin 
                    board.digital[7].write(1)   # Output 1 to the arduino pin 
                    board.digital[8].write(1)   # Output 1 to the arduino pin 
                    board.digital[9].write(1)   # Output 1 to the arduino pin 
                    board.digital[10].write(1)   # Output 1 to the arduino pin 
                    speak("Turned on all successfully...")
                elif 'turn off all' in query:
                    speak(choice(opening_text))
                    speak(random.choice(["Turning off all of your appliances...", "Turning off all of your gadgets..."]))
                    board.digital[2].write(0)   # Output 0 to the arduino pin
                    board.digital[3].write(0)   # Output 0 to the arduino pin
                    board.digital[4].write(0)   # Output 0 to the arduino pin
                    board.digital[5].write(0)   # Output 0 to the arduino pin
                    board.digital[6].write(0)   # Output 0 to the arduino pin
                    board.digital[7].write(0)   # Output 0 to the arduino pin
                    board.digital[8].write(0)   # Output 0 to the arduino pin
                    board.digital[9].write(0)   # Output 0 to the arduino pin
                    board.digital[10].write(0)   # Output 0 to the arduino pin
                    speak("Turned off all successfully...")


                elif 'date and time' in query:
                    now = datetime.datetime.now()
                    date = now.strftime("%d")
                    month = now.strftime("%B")
                    year = now.strftime("%Y")
                    hour = now.strftime("%I")
                    minn = now.strftime("%M")
                    apm = now.strftime("%p")
                    speak(f"{MASTER} the date is {date}... {month} {year} an the time is {hour} {minn} {apm}")

                
                elif 'shut down the system' in query:
                    speak(f"bye bye {MASTER}! shutting down the system")
                    time.sleep(2)
                    os.system("shutdown /s /t 5")

                elif 'restart the system' in query:
                    speak(f"see you soon {MASTER}! restarting the system")
                    time.sleep(2)
                    os.system("shutdown /r /t 5")

                elif 'sleep the system' in query:
                    speak(f"bye bye {MASTER}! see you after some time")
                    time.sleep(2)
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

                elif 'internet speed' in query:
                    speak(f"{MASTER}, please wait for 5 to 10 seconds")
                    st = speedtest.Speedtest()
                    ds = str(math.floor(st.download()/8000000))
                    us = str(math.floor(st.upload()/8000000))
                    speak("Your download speed is "+ds+" mb p s and upload speed is "+us+" mb p s... but why are you checking for ?")

                elif 'tell me a joke' in query:
                    joke = pyjokes.get_joke()
                    speak(joke)

                elif 'headlines' in query or 'news' in query:
                    try:
                        if 'of india' in query or 'regional' in query:
                            url = self.regional_news()
                        elif 'of the world' in query:
                            url = self.world_news()
                        else:
                            speak(f"{MASTER}, are you want to know your region news or all over the world")
                            query = self.takeCommand().lower()
                            if 'only india' in query or 'regional' in query:
                                url = self.regional_news()
                            elif 'over the world' in query:
                                url = self.world_news()

                        main_page = requests.get(url).json()
                        articles = main_page["articles"]
                        head = []
                        day = ["first", "second", "third", "fourth", "fifth"]
                        print("#====================================<<< HEADLINES >>>====================================#")
                        for ar in articles:
                            head.append(ar["title"])
                        for i in range (len(day)):
                            print(f" {i+1} >>>  {head[i]}...")
                            speak(f"today's {day[i]} news is {head[i]}")
                            time.sleep(1)
                            
                        speak(f"{MASTER}, is it okay or you want to know more?")
                        query = self.takeCommand().lower()
                        if 'its ok' in query or 'no' in query or 'know' in query:
                            pass
                        elif 'know more' in query or 'no more' in query:
                            speak(f"okay {MASTER},")
                            day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
                            for ar in articles:
                                head.append(ar["title"])               
                            for i in range (len(day)):
                                if i<5:
                                    print(f" {i+6} >>>  {head[i+5]}...")
                                    speak(f"today's {day[i+5]} news is {head[i+5]}")
                                    time.sleep(1)
                                else:
                                    pass
                        
                    except Exception as e:
                        speak(f"Sorry {MASTER}! due to an network issue I am unable to fetch the news")
                        pass
                

                elif 'where i am' in query or 'where we are' in query or 'location' in query:
                    speak(f"wait {MASTER}! let me check the data, please wait")
                    api_key = 'at_JoSlqILFUewI5lpdGhd9z8NPpDKTA'
                    ipify_url = f"https://geo.ipify.org/api/v2/country,city?apiKey={api_key}"
                    response = requests.get(ipify_url)
                    try:
                        if response.status_code == 200:
                            # Replace 'your_api_key_here' with your actual IPify API key
                            ip_data = response.json()
                            city = ip_data['location']['city']
                            state = ip_data['location']['region']
                            country = ip_data['location']['country']
                            pincode = ip_data['location']['postalCode']
                            latitude = ip_data['location']['lat']
                            longitude = ip_data['location']['lng']

                            speak(f"{MASTER} I am not sure, but as I can see we are in {city} city, of {state}, in {country} country...")
                            if pincode != "":
                                speak(f"and our postal code is {pincode}.")
                            speak(f"In latitude {latitude} and longitude {longitude}")
                        else:
                            speak(f"Sorry {MASTER}, Due to network issue I can not able to fetch our current location.")

                    except Exception as e:
                        speak(f"Sorry {MASTER}, Some unexpected error is occured during fetching the location...")


                elif 'search in youtube' in query or 'song in youtube' in query or 'search on youtube' in query or 'song on youtube' in query:
                    try:
                        if 'song' in query:
                            speak(f"{MASTER}...which song should I search in youTube")
                        else: 
                            speak(f"{MASTER}...What should I search in youTube")
                        song = self.takeCommand().lower()
                        speak(f"Searching for {song} in youtube")
                        pywhatkit.playonyt(song)
                    except:
                        speak(f"Sorry {MASTER}! an unknown error occured")


        except:
            # Show error massage if any error occured in code
            # Error using messagebox() function Tkinter
            messagebox.showwarning("Warning*", "An unknown error occured! \nClose the application, and try again.")


# main
if __name__ == "__main__":

    # Creating a pyQt5 application
    app = QApplication(sys.argv)
    # setting name to the application
    app.setApplicationName("AutoHome")
    app.setWindowIcon(QIcon('icon.png'))

    if 'Username' in USERNAME and 'Botname' in BOTNAME and 'None' in MASTER:
        # Creating a main window object
        main_screen = LoginScreen()
        widget = QtWidgets.QStackedWidget()
        widget.addWidget(main_screen)
        widget.setFixedHeight(621)   # Height of the UI
        widget.setFixedWidth(891)
        widget.show()   # Show the widget


    else:
        # Creating a main window object
        main_screen = MainScreen()
        widget = QtWidgets.QStackedWidget()
        widget.addWidget(main_screen)
        widget.setFixedHeight(311)   # Height of the UI
        widget.setFixedWidth(551)   # Width of the UI
        widget.show()   # Show the widget


    try:
        print("try exit")
        sys.exit(app.exec())  # Loop
    except:
        if COMPORT != 'None':
            board.digital[11].write(0)
            board.digital[12].write(0)
            board.digital[13].write(0)
        print("Exiting")

