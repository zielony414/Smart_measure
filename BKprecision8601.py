import pyvisa
import time

"""sterowanie prądem i mocą"""

class BKprecision8601:
    """Inicjalizacja połączenia z urządzeniem"""
    def __init__(self, port):
        try:
            self.instr = pyvisa.ResourceManager().open_resource(port)
        except pyvisa.Error as e:
            print("Błąd inicjalizacji urządzenia: ", e)

    """Metoda zwracająca nazwę urządzenia"""
    def it_is(self):
        answer = ""
        self.instr.clear()
        try:
            answer = self.instr.query("*IDN?")
        except pyvisa.Error as e:
            print("Błąd odczytu nazwy urządzenia: ", e)
        return answer

    """Metoda ustawiająca natężenie"""
    def set_current(self, current):
        self.instr.write("CURR " + str(current) + "\n")  # ustawienie natężenia
        time.sleep(1)

    """Metoda ustawiająca moc"""
    def set_power(self, power):
        self.instr.write("POW " + str(power) + "\n")
        time.sleep(1)

    """Metoda ustawiająca napięcie"""
    def set_voltage(self, voltage):
        self.instr.write("VOLT " + str(voltage) + "\n")
        time.sleep(1)

    """Metoda odczytująca natężenie napiecie i moc"""
    def read(self):
        answer = ""
        try:
            answer = self.instr.query("CURR?\n")
            answer += self.instr.query("VOLT?\n")
            answer += self.instr.query("POW?\n")
        except pyvisa.Error as e:
            print("Błąd odczytu wartości: ", e)
        return answer

    """Metoda ustawiająca tryb pracy"""
    def set_mode(self, mode):
        self.instr.write("FUNC " + mode + "\n")
        time.sleep(1)

    """Metoda odczytująca tryb pracy"""
    def read_mode(self):
        answer = ""
        try:
            answer = self.instr.query("FUNC?\n")
        except pyvisa.Error as e:
            print("Błąd odczytu trybu pracy: ", e)
        return answer

    """Metoda zmieniająca ustawienia w czasie"""
    async def set_change(self, current_value, step, mode, duration, step_freq):
        start_time = time.time()
        while time.time() - start_time < duration:
            if mode == "VOLT":
                self.instr.write("VOLT " + str(current_value) + "\n")
            elif mode == "CURR":
                self.instr.write("CURR " + str(current_value) + "\n")
            elif mode == "POW":
                self.instr.write("POW " + str(current_value) + "\n")
            time.sleep(1)
            current_value = current_value + step
            await time.sleep(step_freq)



    """Metoda włączająca zasilanie"""
    def power_on(self):
        self.instr.write("OUTP ON\n")
        time.sleep(1)

    """Metoda wyłączająca zasilanie"""
    def power_off(self):
        self.instr.write("OUTP OFF\n")
        time.sleep(1)

    """Metoda resetująca urządzenie"""
    def reset(self):
        self.instr.write("*RST\n")
        time.sleep(1)
