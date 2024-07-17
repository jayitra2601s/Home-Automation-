# Importing all necessary Module 
import sys
import dotenv
import os
import time
import pyttsx3 
import speech_recognition as s
from decouple import config
from datetime import datetime
from random import choice
from tkinter import messagebox

# Importing PyQt5 Module
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import QThread, pyqtSignal

# Importing the PyFirmata module for the arduino board
from pyfirmata import Arduino
from pyfirmata import OUTPUT

# Importing the other needed Python (.py) file
from check import FindArduino
from utills import opening_text

# Read data from the ENV (.env) file
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)  

# Storing all data that are read from the ".env" file into variables
# Configuring data using config function from the decouple module
USERNAME = config('USER')
BOTNAME = config('BOT')
MASTER = config('MASTER')
port1 = config('PORT1')
port2 = config('PORT2')
port3 = config('PORT3')
port4 = config('PORT4')
port5 = config('PORT5')
port6 = config('PORT6')
port7 = config('PORT7')
port8 = config('PORT8')
port9 = config('PORT9')


# Running the FindArduino() func. imported from the "Check.py" file
FindArduino()
COMPORT = config('COMPORT')

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
    board.digital[11].mode = OUTPUT
    board.digital[12].mode = OUTPUT
    board.digital[13].mode = OUTPUT
    board.digital[2].write(0)
    board.digital[3].write(0)
    board.digital[4].write(0)
    board.digital[5].write(0)
    board.digital[6].write(0)
    board.digital[7].write(0)
    board.digital[8].write(0)
    board.digital[9].write(0)
    board.digital[10].write(0)


# Calling sapi5 for text to speech conversion 
engine = pyttsx3.init('sapi5')

# Set voice (Male/Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Set the voice speech rate
engine.setProperty('rate', 170)


# Defining the Speak function to convert text into audio
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


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
        self.settings.setCursor(QCursor(QtCore.Qt.PointingHandCursor))    
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
        sys.stdout.flush()
        os.execl(sys.executable, 'python', __file__, *sys.argv[1:])



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
        new_dir = dir.replace("\\", "/")  
        code_dir = new_dir+"\Code"
        path = os.path.realpath(code_dir) # Initializing the path of the Code folder
        os.startfile(path)   # Open file location with windows explorer
        self.view_code.setGeometry(580, 190, 111, 31)
        self.reboot.setGeometry(290, 210, 111, 31)
        self.exit.setGeometry(420, 210, 111, 31)
        self.error1.setText("After uploading you can tap on the restart button &")
        self.error.setText("restart the application...")



    def Reboot(self):  # Restart function
        sys.stdout.flush()
        os.execl(sys.executable, 'python', __file__, *sys.argv[1:])



    def Exit(self):  # Exit the application
        sys.exit(app.exec_())   




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
            speak("Good night sir, Take care!")
        elif hour >= 5 and hour <= 16:
            speak('Have a good day sir!')
        else:
            speak('Thanks for using me Sir, Take care!')
        self.is_running = False
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
        speak(f"I am {BOTNAME}, an AI. I am here to asist you. Please tell me how can I help you?")  # Introduce


    def listen(self):   
        # It confirms AI is listening us
        board.digital[11].write(1)  # Turning on the green LED
        board.digital[12].write(0)
        board.digital[13].write(0)

    def recognize(self):
        # It confirms AI is recognizing what we said
        board.digital[11].write(0)
        board.digital[12].write(1)  # Turning on the blue LED
        board.digital[13].write(0)

    def execute(self):
        # It confirms AI is working on our command
        board.digital[11].write(0)
        board.digital[12].write(0)  # Turning on the red LED
        board.digital[13].write(1)


    def takeCommand(self):  # Creating a function that takes command from user
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
            print("\nYou said: ", query)   
        except Exception as e:
            print("Say that again Please... I can't hear clearly...")  # Print error AI does not recognize us
            time.sleep(1)  # Sleep the program for 1 second
            return "None" 

        return query


    def MainTask(self):
        
        try:
            self.greet()
            while True:
                query = self.takeCommand().lower()  # Calling the takeCommand() func.
                self.execute()  # LED status
            
                if 'the time' in query:
                    Time = datetime.now().strftime("%Ho%M:%p")  # Specifies the current tieme
                    speak(f"Sir, the time is {Time}")

                elif 'the date' in query:
                    if 'date and time' in query:  # Current date & time
                        now = datetime.now()
                        date = now.strftime("%d")
                        month = now.strftime("%B")
                        year = now.strftime("%Y")
                        hour = now.strftime("%I")
                        minn = now.strftime("%M")
                        apm = now.strftime("%p")
                        speak(f"Sir! the date is {date}... {month} {year} an the time is {hour} {minn} {apm}")
                    else:
                        Date = datetime.now().strftime("%d:%B:%Y")  # Today date
                        speak(f"Sir,the date is {Date}") 

                elif 'hello' in query:
                    speak("hello sir! Tell me what can I do for you")
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
                    speak("Turning on all...")
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
                    speak("Turning off all...")
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

        except:
            # Show error massage if any error occured in code
            # Error using messagebox() function Tkinter
            messagebox.showwarning("Warning*", "An unknown error occured! \nClose the application, and try again.")

 
            


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
            sys.stdout.flush()
            os.execl(sys.executable, 'python', __file__, *sys.argv[1:]) 
        else:
            sys.exit(app.exec())   # Exit the application


    def exitapp(self):   # Function to exit the application
        sys.exit(app.exec())




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
        print("Exiting")

