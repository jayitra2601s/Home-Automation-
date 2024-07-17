
import serial.tools.list_ports
import dotenv
import os

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

def FindArduino():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'USB' in p.description or 'Arduino' in p.description # may need tweaking to match new arduinos
    ]

    if arduino_ports:  
        # print(arduino_ports)
        os.environ["COMPORT"] = arduino_ports[0]
        dotenv.set_key(dotenv_file, "COMPORT", os.environ["COMPORT"])
    else:
        os.environ["COMPORT"] = "None"
        print("No Arduino found")  
        dotenv.set_key(dotenv_file, "COMPORT", os.environ["COMPORT"])

