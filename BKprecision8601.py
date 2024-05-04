import pyvisa
import time


class BKprecision8601:
    """Inicjalizacja połączenia z urządzeniem"""
    def __init__(self, port):
        self.instr = pyvisa.ResourceManager().open_resource(port)

    """Metoda zwracająca nazwę urządzenia"""
    def it_is(self):
        return self.instr.query("*IDN?\n")

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
