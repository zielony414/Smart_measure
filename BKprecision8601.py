import pyvisa
import time


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
            answer = self.instr.query("*IDN?\n")
        except pyvisa.Error as e:
            print("Błąd odczytu nazwy urządzenia: ", e)
        return answer

    """Metoda ustawiająca napięcie i natężenie"""
    def set_voltage_current(self, voltage, current):
        self.instr.write("VOLT " + str(voltage) + "\n")  # ustawienie napięcia
        time.sleep(1)
        self.instr.write("CURR " + str(current) + "\n")  # ustawienie natężenia
        time.sleep(1)

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
