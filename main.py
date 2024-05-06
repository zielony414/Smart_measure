import sys
import pyvisa
from PyQt5 import QtWidgets, QtCore
from BurySmartMeasure import Ui_BurySmartMeasureClass
import BKprecision8601
import FLUKE8808A

steps_number = 1    # number of all steps
step = 1            # number of selected step
freq = 1.0          # data gathering frequency
time_per_step = 120  # time per step in seconds
steps_list = ()
rm = pyvisa.ResourceManager()
# TODO add list of data


def initial_ui_config():
    ui.step_num2_lbl.setEnabled(0)
    ui.step_num2_combo.setEnabled(0)
    ui.set_temp_radio.setEnabled(0)
    ui.set_gradient_radio.setEnabled(0)
    ui.set_temp_lbl.setEnabled(0)
    ui.set_temp_spb.setEnabled(0)
    ui.set_humidity_lbl.setEnabled(0)
    ui.set_humidity_spb.setEnabled(0)
    ui.use_allowable_humidity_err_chkbox.setEnabled(0)
    ui.use_allowable_temp_err_chkbox.setEnabled(0)
    ui.gr_temp_step_lbl.setEnabled(0)
    ui.gr_temp_step_spb.setEnabled(0)
    ui.gr_temp_lbl.setEnabled(0)
    ui.gr_temp_spb.setEnabled(0)
    ui.gr_humidity_step_lbl.setEnabled(0)
    ui.gr_humidity_step_spb.setEnabled(0)
    ui.gr_humidity_lbl.setEnabled(0)
    ui.gr_humidity_spb.setEnabled(0)
    ui.gr_temp_step_info_lbl.setEnabled(0)
    ui.gr_humidity_step_info_lbl.setEnabled(0)
    ui.allowable_temp_err_lbl.setEnabled(0)
    ui.allowable_temp_err_spb.setEnabled(0)
    ui.allowable_humidity_err_lbl.setEnabled(0)
    ui.allowable_humidity_err_spb.setEnabled(0)


# TODO Scanning for new devices
def refresh_devices():
    # Add scanning devices code
    adress = rm.list_resources()
    list = []
    for i in adress:
        if i[:4] == "ASRL":
            # Próba połączenia z Multimetrem i zasilaczem
            Multimeter = FLUKE8808A.Fluke_8808A(i, 19200)
            name = Multimeter.it_is()
            list.append((i, name))

        elif i[:3] == "USB":
            # Próba połączenia z DCLoad
            DCLoad = BKprecision8601.BKprecision8601(i)
            name = DCLoad.it_is()
            list.append((i, name))

        else: k = 2

    return list

# Switching to next tab
def next_page():
    current_index = ui.tabWidget.currentIndex()
    tab_count = ui.tabWidget.count()
    next_index = (current_index + 1) % tab_count
    ui.tabWidget.setCurrentIndex(next_index)


# TODO tworzenie list
def steps_set():
    global steps_number
    steps_number = ui.steps_spb.value()
    ui.step_num1_combo.clear()
    ui.step_num2_combo.clear()
    for i in range(1, steps_number + 1):
        ui.step_num1_combo.addItem(str(i))
        ui.step_num2_combo.addItem(str(i))
        # jeżeli lista nr i nie istnieje, stwórz ją pustą
        # jeżeli istnieje, zostaw
        # jeżeli są, usuń wszystkie listy o nr większym niż steps_number


# ------------TEMP CHAMBER--------------
# When using chamber, enable functions
def use_chamber():
    if ui.use_temp_chamber_chkbox.isChecked():
        ui.step_num2_lbl.setEnabled(1)
        ui.step_num2_combo.setEnabled(1)
        ui.set_temp_radio.setEnabled(1)
        ui.set_gradient_radio.setEnabled(1)
        ui.set_temp_lbl.setEnabled(1)
        ui.set_temp_spb.setEnabled(1)
        ui.set_humidity_lbl.setEnabled(1)
        ui.set_humidity_spb.setEnabled(1)
        ui.use_allowable_humidity_err_chkbox.setEnabled(1)
        ui.use_allowable_temp_err_chkbox.setEnabled(1)
    else:
        ui.step_num2_lbl.setEnabled(0)
        ui.step_num2_combo.setEnabled(0)
        ui.set_temp_radio.setEnabled(0)
        ui.set_gradient_radio.setEnabled(0)
        ui.set_temp_lbl.setEnabled(0)
        ui.set_temp_spb.setEnabled(0)
        ui.set_humidity_lbl.setEnabled(0)
        ui.set_humidity_spb.setEnabled(0)
        ui.use_allowable_humidity_err_chkbox.setEnabled(0)
        ui.use_allowable_temp_err_chkbox.setEnabled(0)


# Enabling limiting temp error
def chamber_temp_limit():
    if ui.use_allowable_temp_err_chkbox.isChecked():
        ui.allowable_temp_err_lbl.setEnabled(1)
        ui.allowable_temp_err_spb.setEnabled(1)
    else:
        ui.allowable_temp_err_lbl.setEnabled(0)
        ui.allowable_temp_err_spb.setEnabled(0)


# Enabling limiting humidity error
def chamber_humidity_limit():
    if ui.use_allowable_humidity_err_chkbox.isChecked():
        ui.allowable_humidity_err_lbl.setEnabled(1)
        ui.allowable_humidity_err_spb.setEnabled(1)
    else:
        ui.allowable_humidity_err_lbl.setEnabled(0)
        ui.allowable_humidity_err_spb.setEnabled(0)


# Selecting temperature chamber mode, gradient or fixed temp
def select_chamber_mode():
    if ui.set_temp_radio.isChecked():
        ui.set_temp_lbl.setEnabled(1)
        ui.set_temp_spb.setEnabled(1)
        ui.set_humidity_lbl.setEnabled(1)
        ui.set_humidity_spb.setEnabled(1)
        ui.gr_temp_step_lbl.setEnabled(0)
        ui.gr_temp_step_spb.setEnabled(0)
        ui.gr_temp_lbl.setEnabled(0)
        ui.gr_temp_spb.setEnabled(0)
        ui.gr_humidity_step_lbl.setEnabled(0)
        ui.gr_humidity_step_spb.setEnabled(0)
        ui.gr_humidity_lbl.setEnabled(0)
        ui.gr_humidity_spb.setEnabled(0)
        ui.gr_temp_step_info_lbl.setEnabled(0)
        ui.gr_humidity_step_info_lbl.setEnabled(0)
    else:
        ui.gr_temp_step_lbl.setEnabled(1)
        ui.gr_temp_step_spb.setEnabled(1)
        ui.gr_temp_lbl.setEnabled(1)
        ui.gr_temp_spb.setEnabled(1)
        ui.gr_humidity_step_lbl.setEnabled(1)
        ui.gr_humidity_step_spb.setEnabled(1)
        ui.gr_humidity_lbl.setEnabled(1)
        ui.gr_humidity_spb.setEnabled(1)
        ui.gr_temp_step_info_lbl.setEnabled(1)
        ui.gr_humidity_step_info_lbl.setEnabled(1)
        ui.set_temp_lbl.setEnabled(0)
        ui.set_temp_spb.setEnabled(0)
        ui.set_humidity_lbl.setEnabled(0)
        ui.set_humidity_spb.setEnabled(0)

# Calculating estimated difference in temp or humidity in step
# (only when using gradient)
def chamber_temp_calc():
    global time_per_step
    temp1 = ui.gr_temp_step_spb.value()
    temp2 = ui.gr_humidity_step_spb.value()
    TPS_min = time_per_step/60

    ui.gr_temp_step_info_lbl.setText("Exp. temp. change in step: "+str(round(temp1*TPS_min,2))+" °C")
    ui.gr_humidity_step_info_lbl.setText("Exp. humid. change in step: "+str(round(temp2*TPS_min,2))+" %rH")



# ------------STEPS FUNCTIONS--------------
# Step change
# TODO Loading step data from list
def step_change():
    global step
    if ui.step_num1_combo.currentText() != step:
        step = ui.step_num1_combo.currentText()
    else:
        step = ui.step_num2_combo.currentText()
    # Load and display data of selected step


# Step change from button
def steps_increment():
    ui.step_num1_combo.setCurrentIndex(ui.step_num1_combo.currentIndex()+1)
    step_change()


def tps_change():
    global time_per_step
    mins = ui.timePS_min_spb.value()*60
    sec = ui.timePS_sec_spb.value()

    time_per_step = mins + sec
    chamber_temp_calc()


def freq_change():
    global freq
    freq = ui.freq_spb.value()


# ------------WATTS CALCULATION--------------
def watts_calc():
    DCload_amp = ui.DCload_amp_load_spb.value()
    DCload_volts = ui.DCload_volt_load_spb.value()
    DCload_amp_unit = ui.DCload_amp_unit_combo.currentText()
    DCload_volt_unit = ui.DCload_volt_unit_combo.currentText()

    PSU_amp = ui.PSU_amp_pwr_spb.value()
    PSU_volts = ui.PSU_volt_pwr_spb.value()
    PSU_amp_unit = ui.PSU_amp_unit_combo.currentText()
    PSU_volt_unit = ui.PSU_volt_unit_combo.currentText()

    if DCload_amp_unit == "mA":
        DCload_amp *= 0.001
    elif DCload_amp_unit == "µA":
        DCload_amp * 0.001 * 0.001

    if DCload_volt_unit == "mV":
        DCload_volts *= 0.001
    elif DCload_volt_unit == "µV":
        DCload_volts * 0.001 * 0.001
    elif DCload_volt_unit == "kV":
        DCload_volts *= 1000

    if PSU_volt_unit == "mV":
        PSU_volts *= 0.001
    elif PSU_volt_unit == "µV":
        PSU_volts * 0.001 * 0.001
    elif PSU_volt_unit == "kV":
        PSU_volts *= 1000

    if PSU_amp_unit == "mA":
        PSU_amp *= 0.001
    elif DCload_amp_unit == "µA":
        PSU_amp * 0.001 * 0.001

    ui.PSU_watts_lbl.setText("Watts: "+str(round(PSU_volts*PSU_amp, 5))+" W")
    ui.DCload_watts_lbl.setText("Watts: "+str(round(DCload_amp*DCload_volts, 5))+" W")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    BurySmartMeasureClass = QtWidgets.QMainWindow()
    ui = Ui_BurySmartMeasureClass()
    ui.setupUi(BurySmartMeasureClass)
    initial_ui_config()

    chamber_radio_gr = QtWidgets.QButtonGroup()
    chamber_radio_gr.addButton(ui.set_gradient_radio)
    chamber_radio_gr.addButton(ui.set_temp_radio)

    # ---------Connect buttons to functions-------------
    ui.refresh_dev_btn.clicked.connect(refresh_devices)
    # navigation
    ui.config_dev.clicked.connect(next_page)
    ui.next_pg1_btn.clicked.connect(next_page)
    ui.next_pg2_btn.clicked.connect(next_page)
    # temp chamber settings
    ui.use_temp_chamber_chkbox.toggled.connect(use_chamber)
    ui.use_allowable_temp_err_chkbox.stateChanged.connect(chamber_temp_limit)
    ui.use_allowable_humidity_err_chkbox.stateChanged.connect(chamber_humidity_limit)
    ui.set_temp_radio.toggled.connect(select_chamber_mode)
    ui.set_gradient_radio.toggled.connect(select_chamber_mode)
    ui.gr_temp_step_spb.valueChanged.connect(chamber_temp_calc)
    ui.gr_humidity_step_spb.valueChanged.connect(chamber_temp_calc)
    # steps
    ui.timePS_min_spb.valueChanged.connect(tps_change)
    ui.timePS_sec_spb.valueChanged.connect(tps_change)
    ui.steps_spb.valueChanged.connect(steps_set)
    ui.step_num1_combo.currentIndexChanged.connect(step_change)
    ui.step_num2_combo.currentIndexChanged.connect(step_change)
    ui.next_step_btn.clicked.connect(steps_increment)
    ui.next_step1_btn.clicked.connect(steps_increment)
    ui.freq_spb.valueChanged.connect(freq_change)
    # watts calculation
    ui.DCload_amp_load_spb.valueChanged.connect(watts_calc)
    ui.DCload_volt_load_spb.valueChanged.connect(watts_calc)
    ui.DCload_amp_unit_combo.currentIndexChanged.connect(watts_calc)
    ui.DCload_volt_unit_combo.currentIndexChanged.connect(watts_calc)
    ui.PSU_amp_pwr_spb.valueChanged.connect(watts_calc)
    ui.PSU_volt_pwr_spb.valueChanged.connect(watts_calc)
    ui.PSU_amp_unit_combo.currentIndexChanged.connect(watts_calc)
    ui.PSU_volt_unit_combo.currentIndexChanged.connect(watts_calc)

    BurySmartMeasureClass.show()
    sys.exit(app.exec_())
