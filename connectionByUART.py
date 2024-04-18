import serial
from time import sleep
import numpy as np


class UART():
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=1000000, #115200
            #parity=serial.PARITY_NONE,
            #stopbits=serial.STOPBITS_ONE,
            timeout=0
        )  # Open port with baud rate

    def readU(self):
        try:
            # read serial port
            received_data = self.ser.readline().decode('utf-8').strip()
            data = received_data.split()

        except serial.SerialException as e:
            print(f"SerialException: {e}")
            data = []

        #print("table" + str(data))
        #print(data)

        return data
