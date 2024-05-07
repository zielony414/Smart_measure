import pyvisa
import time

class BKprecision8601:
    """Initializing the connection to the device"""
    def __init__(self, port):
        try:
            self.instr = pyvisa.ResourceManager().open_resource(port)
        except pyvisa.Error as e:
            print("Device initialization error: ", e)

    """Method that returns the device name"""
    def it_is(self):
        answer = ""
        self.instr.clear()
        try:
            answer = self.instr.query("*IDN?")
        except pyvisa.Error as e:
            print("Error reading device name: ", e)
        return answer

    """Method that sets the intensity"""
    def set_current(self, current):
        self.instr.write("CURR " + str(current) + "\n")  # ustawienie natężenia
        time.sleep(1)

    """A method that sets the power"""
    def set_power(self, power):
        self.instr.write("POW " + str(power) + "\n")
        time.sleep(1)

    """A method that sets the voltage"""
    def set_voltage(self, voltage):
        self.instr.write("VOLT " + str(voltage) + "\n")
        time.sleep(1)

    """A method that reads current voltage and power"""
    def read(self):
        answer = ""
        try:
            answer = self.instr.query("CURR?\n")
            answer += self.instr.query("VOLT?\n")
            answer += self.instr.query("POW?\n")
        except pyvisa.Error as e:
            print("Value reading error: ", e)
        return answer

    """Method that sets the mode of device"""
    def set_mode(self, mode):
        self.instr.write("FUNC " + mode + "\n")
        time.sleep(1)

    """Method that reads the mode of device"""
    def read_mode(self):
        answer = ""
        try:
            answer = self.instr.query("FUNC?\n")
        except pyvisa.Error as e:
            print("Błąd odczytu trybu pracy: ", e)
        return answer

    """A method that changes settings over time"""
    async def set_change(self, current_value, step, mode, duration, gather_freq):
        start_time = time.time()
        while time.time() - start_time < duration:
            if mode == "VOLT":
                self.set_voltage(current_value)
            elif mode == "CURR":
                self.set_current(current_value)
            elif mode == "POW":
                self.set_power(current_value)
            time.sleep(1)
            current_value = current_value + step
            await time.sleep(gather_freq)
        return 1

    """Method of powering on the device"""
    def power_on(self):
        self.instr.write("OUTP ON\n")
        time.sleep(1)

    """Method of powering of the device"""
    def power_off(self):
        self.instr.write("OUTP OFF\n")
        time.sleep(1)

    """Method to reset the device"""
    def reset(self):
        self.instr.write("*RST\n")
        time.sleep(1)
