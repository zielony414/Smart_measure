import pyvisa
import ConfigData
import BKprecision8601
import FLUKE8808A
import FLUKE8846A
import TTI_CPX400DP
import CTS_T6550


class UiSettings:

    # TODO dodać sprawdzenie czy DCLoad time per change nie jest większy niż time per step
    # TODO dodać opcję ustawienia stałej wartości bez zmiany w DCLoad
    # TODO dodać informację o tym że na multimetrach musi być ustawiony domyślny baud rate

    def __init__(self, ui):
        self.ui = ui
        self.rm = pyvisa.ResourceManager()
        self.steps_number = 1  # number of all steps
        self.step_no = 0  # number of selected step
        self.freq = 1.0  # data gathering frequency
        self.time_per_step = 120  # time per step in seconds
        self.steps_list = []  # list of steps
        self.DeviceList = []  # list of devices

        self.ui.step_num2_lbl.setEnabled(0)
        self.ui.step_num2_combo.setEnabled(0)
        self.ui.set_temp_radio.setEnabled(0)
        self.ui.set_gradient_radio.setEnabled(0)
        self.ui.set_temp_lbl.setEnabled(0)
        self.ui.set_temp_spb.setEnabled(0)
        self.ui.set_humidity_lbl.setEnabled(0)
        self.ui.set_humidity_spb.setEnabled(0)
        self.ui.use_allowable_humidity_err_chkbox.setEnabled(0)
        self.ui.use_allowable_temp_err_chkbox.setEnabled(0)
        self.ui.gr_temp_step_lbl.setEnabled(0)
        self.ui.gr_temp_step_spb.setEnabled(0)
        self.ui.gr_temp_lbl.setEnabled(0)
        self.ui.gr_temp_spb.setEnabled(0)
        self.ui.gr_humidity_step_lbl.setEnabled(0)
        self.ui.gr_humidity_step_spb.setEnabled(0)
        self.ui.gr_humidity_lbl.setEnabled(0)
        self.ui.gr_humidity_spb.setEnabled(0)
        self.ui.gr_temp_step_info_lbl.setEnabled(0)
        self.ui.gr_humidity_step_info_lbl.setEnabled(0)
        self.ui.allowable_temp_err_lbl.setEnabled(0)
        self.ui.allowable_temp_err_spb.setEnabled(0)
        self.ui.allowable_humidity_err_lbl.setEnabled(0)
        self.ui.allowable_humidity_err_spb.setEnabled(0)
        first_step = ConfigData.ConfigData()
        self.steps_list.append(first_step)
        self.steps_output()

    # Scanning for new devices
    def refresh_devices(self):
        try:
            # Add scanning devices code
            adress = self.rm.list_resources()

            adress = adress[::-1]

            for i in adress:
                print(i)
                if i[:4] == "ASRL":
                    # Próba połączenia z Multimetrem i zasilaczem
                    Multimeter = FLUKE8808A.Fluke_8808A(i)
                    PowerSupply = TTI_CPX400DP.TTI_CPX400DP(i)
                    Multimeter.configure()
                    name = Multimeter.it_is()
                    name2 = PowerSupply.it_is()
                    print(name)
                    print(name2)
                    available = True
                    self.DeviceList.append((i, name, available))
                    self.DeviceList.append((i, name2, available))

                elif i[:3] == "USB":
                    # Próba połączenia z DCLoad
                    DCLoad = BKprecision8601.BKprecision8601(i)
                    name = DCLoad.it_is()
                    available = True
                    self.DeviceList.append((i, name, available))

            print(self.DeviceList)
        except Exception as e:
            print(f"An error occurred: {e}")

        # ui.refresh_dev_lbl.setText("Devices found: "+str(len(list)))

        # return list
        """
        for i in adress:
            try:
                print(i)
                instr = rm.open_resource(i)
            except pyvisa.Error as e:
                print("Błąd inicjalizacji urządzenia: ", e)

            try:
                answer = ""
                instr.clear()

                answer = instr.query("*IDN?")
                print(answer)
            except pyvisa.Error as e:
                print("Błąd odczytu nazwy urządzenia: ", e)

        """

        # Starting test

    def start_test(self):
        for i in range(len(self.DeviceList)):
            if self.DeviceList[i][1] == "nazwa_BKprecision8601":
                DCLoad = BKprecision8601.BKprecision8601(self.DeviceList[i][0])

                if "CC" in self.steps_list[0].dcl_step:
                    DCLoad.set_mode("CURR")
                elif "CV" in self.steps_list[0].dcl_step:
                    DCLoad.set_mode("VOLT")

                DCLoad.set_current(self.steps_list[0].dcl_start)


            elif self.DeviceList[i][1] == "nazwa_Fluke8808A":
                if self.DeviceList[i][3] == "inlet_amm":
                    inlet_amm = FLUKE8808A.Fluke_8808A(self.DeviceList[i][0])
                    inlet_amm.configure()

                elif self.DeviceList[i][3] == "inlet_volt":
                    inlet_volt = FLUKE8808A.Fluke_8808A(self.DeviceList[i][0])
                    inlet_volt.configure()

                elif self.DeviceList[i][3] == "out_amm":
                    out_amm = FLUKE8808A.Fluke_8808A(self.DeviceList[i][0])
                    out_amm.configure()

                elif self.DeviceList[i][3] == "out_volt":
                    out_volt = FLUKE8808A.Fluke_8808A(self.DeviceList[i][0])
                    out_volt.configure()


            elif self.DeviceList[i][1] == "nazwa_Fluke8846A":
                if self.DeviceList[i][3] == "inlet_amm":
                    inlet_amm = FLUKE8846A.Fluke_8846A(self.DeviceList[i][0])
                    inlet_amm.configure()

                elif self.DeviceList[i][3] == "inlet_volt":
                    inlet_volt = FLUKE8846A.Fluke_8846A(self.DeviceList[i][0])
                    inlet_volt.configure()

                elif self.DeviceList[i][3] == "out_amm":
                    out_amm = FLUKE8846A.Fluke_8846A(self.DeviceList[i][0])
                    out_amm.configure()

                elif self.DeviceList[i][3] == "out_volt":
                    out_volt = FLUKE8846A.Fluke_8846A(self.DeviceList[i][0])
                    out_volt.configure()


            elif self.DeviceList[i][1] == "nazwa_TTI_CPX400DP":
                power_supply = TTI_CPX400DP.TTI_CPX400DP(self.DeviceList[i][0])

                power_supply.set_voltage(self.steps_list[0].psu_volt)
                power_supply.set_current(self.steps_list[0].psu_amm)

            elif self.DeviceList[i][1] == "nazwa_CTS_T6550":
                pass  # << na razie

    # Switching to next tab
    def next_page(self):
        current_index = self.ui.tabWidget.currentIndex()
        tab_count = self.ui.tabWidget.count()
        next_index = (current_index + 1) % tab_count
        self.ui.tabWidget.setCurrentIndex(next_index)

    # changing number of steps
    def steps_set(self):
        self.steps_number = self.ui.steps_spb.value()
        self.ui.step_num1_combo.clear()
        self.ui.step_num2_combo.clear()
        for i in range(1, self.steps_number + 1):
            self.ui.step_num1_combo.addItem(str(i))
            self.ui.step_num2_combo.addItem(str(i))

            # jeżeli lista nr i nie istnieje, stwórz ją pustą.
            # jeżeli istnieje, zostaw.

            if len(self.steps_list) < i:
                step = self.create_step(i)
                self.steps_list.append(step)

        # jeżeli są, usuń wszystkie listy o nr większym niż steps_number
        while len(self.steps_list) > self.steps_number:
            self.steps_list.pop()

        if self.step_no > self.steps_number:
            self.step_no = self.steps_number

        self.steps_output()

    # creating step object
    def create_step(self, nr):
        chamber_on = self.ui.use_temp_chamber_chkbox.isChecked()
        chamber_mod = self.ui.set_temp_radio.isChecked()
        temp_err = self.ui.use_allowable_temp_err_chkbox.isChecked()
        humid_err = self.ui.use_allowable_humidity_err_chkbox.isChecked()
        step = ConfigData.ConfigData(nr, chamber_on, chamber_mod, temp_err, humid_err)
        return step

    # ------------TEMP CHAMBER--------------
    # When using chamber, enable functions
    def use_chamber(self):
        if self.ui.use_temp_chamber_chkbox.isChecked():
            self.ui.step_num2_lbl.setEnabled(1)
            self.ui.step_num2_combo.setEnabled(1)
            self.ui.set_temp_radio.setEnabled(1)
            self.ui.set_gradient_radio.setEnabled(1)
            self.ui.set_temp_lbl.setEnabled(1)
            self.ui.set_temp_spb.setEnabled(1)
            self.ui.set_humidity_lbl.setEnabled(1)
            self.ui.set_humidity_spb.setEnabled(1)
            self.ui.use_allowable_humidity_err_chkbox.setEnabled(1)
            self.ui.use_allowable_temp_err_chkbox.setEnabled(1)
        else:
            self.ui.step_num2_lbl.setEnabled(0)
            self.ui.step_num2_combo.setEnabled(0)
            self.ui.set_temp_radio.setEnabled(0)
            self.ui.set_gradient_radio.setEnabled(0)
            self.ui.set_temp_lbl.setEnabled(0)
            self.ui.set_temp_spb.setEnabled(0)
            self.ui.set_humidity_lbl.setEnabled(0)
            self.ui.set_humidity_spb.setEnabled(0)
            self.ui.use_allowable_humidity_err_chkbox.setEnabled(0)
            self.ui.use_allowable_temp_err_chkbox.setEnabled(0)
        # self.steps_output()

    # Enabling limiting temp error
    def chamber_temp_limit(self):
        if self.ui.use_allowable_temp_err_chkbox.isChecked():
            self.ui.allowable_temp_err_lbl.setEnabled(1)
            self.ui.allowable_temp_err_spb.setEnabled(1)
        else:
            self.ui.allowable_temp_err_lbl.setEnabled(0)
            self.ui.allowable_temp_err_spb.setEnabled(0)

        self.steps_output()

    # Enabling limiting humidity error
    def chamber_humidity_limit(self):
        if self.ui.use_allowable_humidity_err_chkbox.isChecked():
            self.ui.allowable_humidity_err_lbl.setEnabled(1)
            self.ui.allowable_humidity_err_spb.setEnabled(1)
        else:
            self.ui.allowable_humidity_err_lbl.setEnabled(0)
            self.ui.allowable_humidity_err_spb.setEnabled(0)

        self.steps_output()

    # Selecting temperature chamber mode, gradient or fixed temp
    def select_chamber_mode(self):
        if self.ui.set_temp_radio.isChecked():
            self.ui.set_temp_lbl.setEnabled(1)
            self.ui.set_temp_spb.setEnabled(1)
            self.ui.set_humidity_lbl.setEnabled(1)
            self.ui.set_humidity_spb.setEnabled(1)
            self.ui.gr_temp_step_lbl.setEnabled(0)
            self.ui.gr_temp_step_spb.setEnabled(0)
            self.ui.gr_temp_lbl.setEnabled(0)
            self.ui.gr_temp_spb.setEnabled(0)
            self.ui.gr_humidity_step_lbl.setEnabled(0)
            self.ui.gr_humidity_step_spb.setEnabled(0)
            self.ui.gr_humidity_lbl.setEnabled(0)
            self.ui.gr_humidity_spb.setEnabled(0)
            self.ui.gr_temp_step_info_lbl.setEnabled(0)
            self.ui.gr_humidity_step_info_lbl.setEnabled(0)
        else:
            self.ui.gr_temp_step_lbl.setEnabled(1)
            self.ui.gr_temp_step_spb.setEnabled(1)
            self.ui.gr_temp_lbl.setEnabled(1)
            self.ui.gr_temp_spb.setEnabled(1)
            self.ui.gr_humidity_step_lbl.setEnabled(1)
            self.ui.gr_humidity_step_spb.setEnabled(1)
            self.ui.gr_humidity_lbl.setEnabled(1)
            self.ui.gr_humidity_spb.setEnabled(1)
            self.ui.gr_temp_step_info_lbl.setEnabled(1)
            self.ui.gr_humidity_step_info_lbl.setEnabled(1)
            self.ui.set_temp_lbl.setEnabled(0)
            self.ui.set_temp_spb.setEnabled(0)
            self.ui.set_humidity_lbl.setEnabled(0)
            self.ui.set_humidity_spb.setEnabled(0)

        self.steps_output()

    # Calculating estimated difference in temp or humidity in step
    # (only when using gradient)
    def chamber_temp_calc(self):
        temp1 = self.ui.gr_temp_step_spb.value()
        temp2 = self.ui.gr_humidity_step_spb.value()
        TPS_min = self.time_per_step / 60

        self.ui.gr_temp_step_info_lbl.setText("Exp. temp. change in step: " + str(round(temp1 * TPS_min, 2)) + " °C")
        self.ui.gr_humidity_step_info_lbl.setText(
            "Exp. humid. change in step: " + str(round(temp2 * TPS_min, 2)) + " %rH")
        self.steps_output()

    # ------------STEPS FUNCTIONS--------------
    def step_btn1_clicked(self):
        if self.ui.step_num1_combo.currentIndex() == self.ui.step_num2_combo.currentIndex():
            self.step_change(self.ui.step_num1_combo.currentIndex())
        else:
            self.ui.step_num2_combo.setCurrentIndex(self.ui.step_num1_combo.currentIndex())

    def step_btn2_clicked(self):
        if self.ui.step_num2_combo.currentIndex() == self.ui.step_num1_combo.currentIndex():
            self.step_change(self.ui.step_num2_combo.currentIndex())
        else:
            self.ui.step_num1_combo.setCurrentIndex(self.ui.step_num2_combo.currentIndex())

    # Step change
    def step_change(self, number):
        self.step_no = number
        print("numer kroku: " + str(self.step_no))
        print("ilosc kroków: " + str(self.steps_number))

        # Load and display data of selected step
        step = self.steps_list[int(self.step_no)]

        self.ui.amp_inlet_combo.setCurrentText(step.amm_inl_unit)
        self.ui.volt_inlet_combo.setCurrentText(step.volt_inl_unit)

        self.ui.amp_outlet_combo.setCurrentText(step.amm_out_unit)
        self.ui.volt_outlet_combo.setCurrentText(step.volt_out_unit)

        self.ui.PSU_volt_pwr_spb.setValue(step.psu_volt)
        self.ui.PSU_amp_pwr_spb.setValue(step.psu_amm)
        self.ui.PSU_volt_unit_combo.setCurrentText(step.psu_amm_unit)
        self.ui.PSU_amp_unit_combo.setCurrentText(step.psu_volt_unit)

        self.ui.DCload_mode_combo.setCurrentText(step.dcl_mode)
        self.ui.DCload_step_spb.setValue(step.dcl_step)
        self.ui.DCload_time_spb.setValue(step.dcl_time)
        self.ui.DCload_start_spb.setValue(step.dcl_start)
        self.DCload_mode_change()

        self.ui.use_temp_chamber_chkbox.setChecked(step.use_chamber)
        if step.chamber_mode:
            self.ui.set_temp_radio.setChecked(True)
            self.ui.set_temp_spb.setValue(step.chb_temp)
            self.ui.set_humidity_spb.setValue(step.chb_humidity)
        else:
            self.ui.set_gradient_radio.setChecked(True)
            self.ui.gr_temp_step_spb.setValue(step.chb_temp_step)
            self.ui.gr_temp_spb.setValue(step.chb_start_temp)
            self.ui.gr_humidity_step_spb.setValue(step.chb_humidity_step)
            self.ui.gr_humidity_spb.setValue(step.chb_start_humidity)

        self.ui.use_allowable_temp_err_chkbox.setChecked(step.chb_allow_temp_err)
        self.ui.use_allowable_humidity_err_chkbox.setChecked(step.chb_allow_humidity_err)

        if self.ui.use_allowable_temp_err_chkbox.isChecked():
            self.ui.allowable_temp_err_spb.setValue(step.chb_temp_err)

        if self.ui.use_allowable_humidity_err_chkbox.isChecked():
            self.ui.allowable_humidity_err_spb.setValue(step.chb_humidity_err)

        self.use_chamber()

    # Step change from button
    def steps_increment(self):
        if self.ui.step_num1_combo.currentIndex() == self.steps_number - 1:
            self.ui.step_num1_combo.setCurrentIndex(0)
            self.step_change(self.ui.step_num1_combo.currentIndex())
        else:
            self.ui.step_num1_combo.setCurrentIndex(self.ui.step_num1_combo.currentIndex() + 1)
            self.step_change(self.ui.step_num1_combo.currentIndex())

    def tps_change(self):
        mins = self.ui.timePS_min_spb.value() * 60
        sec = self.ui.timePS_sec_spb.value()

        self.time_per_step = mins + sec
        self.chamber_temp_calc()

    def freq_change(self):
        self.freq = self.ui.freq_spb.value()

    # outputting data to the screen
    def steps_output(self):
        self.ui.steps_textEdit.clear()
        self.ui.steps_textEdit2.clear()
        for i in range(self.steps_number):
            step = self.steps_list[i]

            if step.dcl_mode == "Constant voltage (CV)":
                unit_list = 'V'
            else:
                unit_list = 'A'

            self.ui.steps_textEdit.append(
                "Step " + str(i + 1) + ": PSU " + str(step.psu_volt) + step.psu_volt_unit + ", " + str(
                    step.psu_amm) + step.psu_amm_unit + "; DCL " + ", start:" + str(
                    step.dcl_start) + unit_list + " step " + str(step.dcl_step) + unit_list + " every " + str(
                    step.dcl_time) + "s, ")

            if not step.chb_allow_temp_err:
                temp_err_text = "Temp err: off"
            else:
                temp_err_text = str("Temp err: " + str(step.chb_temp_err) + "°C")

            if not step.chb_allow_humidity_err:
                humidity_err_text = "Humid err: off"
            else:
                humidity_err_text = str("Humid err: " + str(step.chb_humidity_err) + "%rH")

            if step.chamber_mode:
                self.ui.steps_textEdit2.append(
                    "Step " + str(i + 1) + ": PSU " + str(step.psu_volt) + step.psu_volt_unit +
                    ", " + str(step.psu_amm) + step.psu_amm_unit + "; DCL " + ", start:" + str(
                        step.dcl_start) + unit_list + " step " + str(step.dcl_step) + unit_list + " every " + str(
                        step.dcl_time) + "s, CHB: " + str(step.chb_temp) + "°C, " + str(step.chb_humidity) + "%, " +
                    temp_err_text + ", " + humidity_err_text)
            else:
                self.ui.steps_textEdit2.append(
                    "Step " + str(i + 1) + ": PSU " + str(step.psu_volt) + step.psu_volt_unit + ", " + str(
                        step.psu_amm) + step.psu_amm_unit + "; DCL " + ", start:" + str(
                        step.dcl_start) + unit_list + " step " + str(step.dcl_step) + unit_list + " every " + str(
                        step.dcl_time) + "s, CHB: " + str(step.chb_start_temp) + "°C, " + str(step.chb_temp_step) +
                    "°C/min, " + temp_err_text + ", " + humidity_err_text)

    def DCload_mode_change(self):
        if self.ui.DCload_mode_combo.currentText() == "Constant current (CC)":
            self.ui.DCload_step_spb.setSuffix(" A/Min")
            self.ui.DCload_start_lbl.setText("Start current:")
            self.ui.DCload_start_spb.setSuffix(" A")
            if self.ui.DCload_time_spb.value() == 0:
                exp_value_change = 0
            else:
                exp_value_change = round(
                    (self.time_per_step / self.ui.DCload_time_spb.value()) * self.ui.DCload_step_spb.value(), 2)
            self.ui.DCload_step_info_lbl.setText("Exp. current change in step: " + str(exp_value_change) + " A")

        elif self.ui.DCload_mode_combo.currentText() == "Constant voltage (CV)":
            self.ui.DCload_step_spb.setSuffix(" V/Min")
            self.ui.DCload_start_lbl.setText("Start voltage:")
            self.ui.DCload_start_spb.setSuffix(" V")
            if self.ui.DCload_time_spb.value() == 0:
                exp_value_change = 0
            else:
                exp_value_change = round(
                    (self.time_per_step / self.ui.DCload_time_spb.value()) * self.ui.DCload_step_spb.value(), 2)
            self.ui.DCload_step_info_lbl.setText(
                "Exp. current change in step: " + str(round(exp_value_change, 2)) + " V")

    # Save data from UI to ConfigData object
    def save_config(self):
        self.steps_list[self.step_no].amm_inl_unit = self.ui.amp_inlet_combo.currentText()
        self.steps_list[self.step_no].volt_inl_unit = self.ui.volt_inlet_combo.currentText()
        self.steps_list[self.step_no].amm_out_unit = self.ui.amp_outlet_combo.currentText()
        self.steps_list[self.step_no].volt_out_unit = self.ui.volt_outlet_combo.currentText()
        self.steps_list[self.step_no].psu_volt = round(float(self.ui.PSU_volt_pwr_spb.value()), 2)
        self.steps_list[self.step_no].psu_volt_unit = self.ui.PSU_volt_unit_combo.currentText()
        self.steps_list[self.step_no].psu_amm = round(float(self.ui.PSU_amp_pwr_spb.value()), 2)
        self.steps_list[self.step_no].psu_amm_unit = self.ui.PSU_amp_unit_combo.currentText()

        self.steps_list[self.step_no].dcl_mode = self.ui.DCload_mode_combo.currentText()
        self.steps_list[self.step_no].dcl_step = round(float(self.ui.DCload_step_spb.value()), 4)
        self.steps_list[self.step_no].dcl_time = round(float(self.ui.DCload_time_spb.value()), 2)
        self.steps_list[self.step_no].dcl_start = round(float(self.ui.DCload_start_spb.value()), 4)

        self.steps_list[self.step_no].use_chamber = self.ui.use_temp_chamber_chkbox.isChecked()
        self.steps_list[self.step_no].chamber_mode = self.ui.set_temp_radio.isChecked()

        self.steps_list[self.step_no].chb_temp = round(float(self.ui.set_temp_spb.value()), 2)
        self.steps_list[self.step_no].chb_humidity = round(float(self.ui.set_humidity_spb.value()), 2)

        self.steps_list[self.step_no].chb_temp_step = round(float(self.ui.gr_temp_step_spb.value()), 2)
        self.steps_list[self.step_no].chb_start_temp = round(float(self.ui.gr_temp_spb.value()), 2)
        self.steps_list[self.step_no].chb_humidity_step = round(float(self.ui.gr_humidity_step_spb.value()), 2)
        self.steps_list[self.step_no].chb_start_humidity = round(float(self.ui.gr_humidity_spb.value()), 2)

        self.steps_list[self.step_no].chb_allow_temp_err = self.ui.use_allowable_temp_err_chkbox.isChecked()
        self.steps_list[self.step_no].chb_allow_humidity_err = self.ui.use_allowable_humidity_err_chkbox.isChecked()
        self.steps_list[self.step_no].chb_temp_err = round(float(self.ui.allowable_temp_err_spb.value()), 2)
        self.steps_list[self.step_no].chb_humidity_err = round(float(self.ui.allowable_humidity_err_spb.value()), 2)

        self.steps_output()

    """
    1 - inlet amm
    2 - inlet volt
    3 - outlet amm
    4 - outlet volt
    5 - DC load
    6 - power supply
    7 - temp chamber
    """

    def dev1_set(self):
        text = self.ui.device1.currentText()

        for i in range(len(self.DeviceList)):
            if self.DeviceList[i][1] == text and self.DeviceList[0][2]:
                self.DeviceList[i].append("inlet_amm")

    def dev2_set(self):
        text = self.ui.device2.currentText()

        for i in range(len(self.DeviceList)):
            if self.DeviceList[i][1] == text and self.DeviceList[i][2]:
                self.DeviceList[i].append("inlet_volt")

    def dev3_set(self):
        text = self.ui.device3.currentText()

        for i in range(len(self.DeviceList)):
            if self.DeviceList[i][1] == text and self.DeviceList[i][2]:
                self.DeviceList[i].append("out_amm")

    def dev4_set(self):
        text = self.ui.device4.currentText()

        for i in range(len(self.DeviceList)):
            if self.DeviceList[i][1] == text and self.DeviceList[i][2]:
                self.DeviceList[i].append("out_volt")

    def dev5_set(self):
        text = self.ui.device4.currentText()

        for i in range(len(self.DeviceList)):
            if self.DeviceList[i][1] == text and self.DeviceList[i][2]:
                self.DeviceList[i].append("DCL")

    def dev6_set(self):
        text = self.ui.device4.currentText()

        for i in range(len(self.DeviceList)):
            if self.DeviceList[i][1] == text and self.DeviceList[i][2]:
                self.DeviceList[i].append("PSU")

    def dev7_set(self):
        text = self.ui.device4.currentText()

        for i in range(len(self.DeviceList)):
            if self.DeviceList[i][1] == text and self.DeviceList[i][2]:
                self.DeviceList[i].append("TempChamber")
