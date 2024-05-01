import pyvisa
import time

class Fluke_8808A:


    def __init__(self, port, baud_rate, mode = 1, timeout=500):
        self.instr = pyvisa.ResourceManager().open_resource(port)
        self.mode = mode #tryb działania multimetru (only info)
        self.instr.baud_rate = baud_rate
        self.instr.timeout = timeout
        #ustawić format odbiranych danych na notację naukową

    async def start_measure(self, duration, gather_freq ,file):
        #zrobić z HOLD i można odczytywać co jakiś ustalony czas ESSA
        pass

    def reset(self):
        self.instr.write('*RST')
        time.sleep(14)
        self.instr.clear()

    def it_is(self):
        answer = ""
        self.instr.clear()
        try:
            self.instr.read()
            answer = self.instr.query("*IDN?")
        except Exception as err:
            print(f"ERROR Unexpected {err=}, {type(err)=}")
        return answer

        

#rm = pyvisa.ResourceManager()
#print(rm.list_resources())
#visa_device = rm.open_resource('ASRL4::INSTR')

stm = Fluke_8808A('ASRL4::INSTR', 19200)

#stm.reset()
print(stm.it_is())
