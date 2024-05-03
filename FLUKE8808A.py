import pyvisa
import asyncio
import time
import datetime

class Fluke_8808A:

    '''Konstruktor ustawiajacy wszystkie najważniejsze pozycje'''
    def __init__(self, port, baud_rate, mode = 1, timeout=5000):
        self.instr = pyvisa.ResourceManager().open_resource(port)
        self.mode = mode #tryb działania multimetru (only info)
        self.instr.baud_rate = baud_rate
        self.instr.timeout = timeout

    '''Wstepna konfiguracja "dla bezpieczeństwa" w razie czego jakby na multimetrze były włączone inne funckje'''
    def configure(self):
        self.instr.write("TRIGGER 4\n") # BARDZO WAŻNE funkcja wyzwala pomiary zewnętrznym źródłem
        time.sleep(1)
        self.instr.write("FORMAT 2\n") # notacja z jednostkami
        time.sleep(1)
        self.instr.write("DBCLR\n") # pokazuje normalne jednostki nie Po i nie dB
        time.sleep(1)
        self.instr.write("MMCLR\n") # wyłączenie modyfikatora min max
        time.sleep(1)
        self.instr.write("RELCLR\n") # wyłacza wartośc bezwzględną
        time.sleep(1)
        self.instr.write("COMPCLR\n") # wychodzi z funkcji porównania
        time.sleep(1)
        self.instr.write("RATE F\n") #BARDZO WAŻNE predkosc przesyłąnia F-fast M-medium S-slow
        time.sleep(1)
        self.instr.write("PRINT 1\n") # BARDZO WAŻNE również funkcja szybkości przesyłania, patrz tabelka w dokumentacji
        time.sleep(1)
        self.instr.write("AUTO\n")
        time.sleep(1)

    '''Główna metoda startujaca pomiary'''
    async def start_measure(self, duration, gather_freq):
        start_time = time.time()
        self.instr.clear()

        while time.time() - start_time < duration:

            #BARDZO WAŻNA sekcja pobiera wyniki z multimetru
            #odczyt wykonuje się 3 razy ponieważ urządzenie przesyła jeszcze monity ("=>")
            reader = self.instr.query('*TRG\n')
            self.instr.read()
            self.instr.read()

            czas = datetime.datetime.now().strftime("%X.%f")[:-4]
            string = str(czas + " " + reader)

            print(string)
            #file.write(string)
            
            time.sleep(gather_freq)
            #await asyncio.sleep(gather_freq)
        return 1

    '''Metoda resetuje urzadzenie pomiarowe'''
    def reset(self):
        self.instr.write('*RST')
        time.sleep(14) # czas ustalony "na oko"
        self.instr.clear()

    '''Metoda zwracająca jakim urzadzeniem jesteś'''
    def it_is(self):
        answer = ""
        self.instr.clear()
        try:
            answer = self.instr.query("*IDN?")
        except Exception as err:
            print(f"ERROR Unexpected {err=}, {type(err)=}")
        return answer

    '''Metoda ustawiajaca multimetr w tryb voltomierza'''
    def set_DCvolts(self):
        self.instr.write("VDC\n")
        time.sleep(5)
        return 1
    
    '''Metoda ustawiajaca multimetr w tryb amperomierza'''
    def set_DCcurrent(self):
        self.instr.write("ADC\n")
        time.sleep(5)
        return 1


# try:
#     stm = Fluke_8808A('ASRL4::INSTR', 19200)
# except Exception as err:
#     print(f"ERROR_CONNECTED Unexpected {err=}, {type(err)=}")

# stm.configure()

# print(stm.it_is())


# try:
#     stm.start_measure(5, 0.5)
# except Exception as err:
#     print(f"ERROR_MEASURE Unexpected {err=}, {type(err)=}")


