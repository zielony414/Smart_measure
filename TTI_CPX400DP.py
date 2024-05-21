import pyvisa
import time

class TTI_CPX400DP:

    def __init__(self, port):
        try:
            self.instr = pyvisa.ResourceManager().open_resource(port)
        except pyvisa.Error as e:
            print("Device initialization error: ", e)

    def it_is(self):
        answer = ""
        self.instr.clear()
        try:
            answer = self.instr.query("*IDN?")
        except pyvisa.Error as e:
            print("Error reading device name: ", e)
        return answer

    def set_current(self, current):
        self.instr.write("CURR " + str(current) + "\n")
        time.sleep(1)

    def set_voltage(self, voltage):
        self.instr.write("VOLT " + str(voltage) + "\n")
        time.sleep(1)

    def read(self):
        answer, voltR, currR = "", "", ""
        try:
            voltR += self.instr.query("VOLT?")
            time.sleep(1)
            currR += self.instr.query("CURR?")
            time.sleep(1)

            answer = "Voltage: " + voltR + "Current: " + currR
        except pyvisa.Error as e:
            print("Value reading error: ", e)
        return answer

    def set_mode(self, mode):
        self.instr.write("FUNC " + mode)
        time.sleep(1)

    def read_mode(self):
        answer = ""
        try:
            answer = self.instr.query("FUNC?")
        except pyvisa.Error as e:
            print("Mode reading error: ", e)
        return answer

    def reset(self):
        self.instr.write("*RST")
        time.sleep(1)

