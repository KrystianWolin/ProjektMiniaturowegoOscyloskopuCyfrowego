import serial


class UART():
    port_name = 'COM6'
    baud_rate = 1000000 #115200
    timeout = 1
    bytesize = serial.EIGHTBITS
    parity = serial.PARITY_NONE

    def __init__(self):
        self.ser = serial.Serial(
            self.port_name,
            self.baud_rate,
            #bytesize=self.bytesize,
            #parity=self.parity,
            timeout=self.timeout
        )
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def readU(self):
        try:
            # read serial port
            received_data = self.ser.readline().decode('utf-8').strip()
            data = received_data.split()

            #print("table" + str(data))

        except serial.SerialException as e:
            print(f"SerialException: {e}")
            data = []

        return data