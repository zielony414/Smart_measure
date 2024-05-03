import sys
from PyQt5 import QtWidgets, QtCore
from BurySmartMeasure import Ui_BurySmartMeasureClass

steps_number = 1


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


# Scanning for new devices
def refresh_devices():
    # Add scanning devices code
    ui.state_lbl.setText("test")


# Switching to next tab
def next_page():
    current_index = ui.tabWidget.currentIndex()
    tab_count = ui.tabWidget.count()
    next_index = (current_index + 1) % tab_count
    ui.tabWidget.setCurrentIndex(next_index)


def steps_change():
    global steps_number
    steps_number = ui.steps_spb.value()
    ui.step_num1_combo.clear()
    ui.step_num2_combo.clear()
    for i in range(1, steps_number + 1):
        ui.step_num1_combo.addItem(str(i))
        ui.step_num2_combo.addItem(str(i))


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
def chamber_temp_limit(state):
    if ui.use_allowable_temp_err_chkbox.isChecked():
        ui.allowable_temp_err_lbl.setEnabled(1)
        ui.allowable_temp_err_spb.setEnabled(1)
    else:
        ui.allowable_temp_err_lbl.setEnabled(0)
        ui.allowable_temp_err_spb.setEnabled(0)


# Enabling limiting humidity error
def chamber_humidity_limit(state):
    if ui.use_allowable_humidity_err_chkbox.isChecked():
        ui.allowable_humidity_err_lbl.setEnabled(1)
        ui.allowable_humidity_err_spb.setEnabled(1)
    else:
        ui.allowable_humidity_err_lbl.setEnabled(0)
        ui.allowable_humidity_err_spb.setEnabled(0)


def select_limit_mode(button):
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    BurySmartMeasureClass = QtWidgets.QMainWindow()
    ui = Ui_BurySmartMeasureClass()
    ui.setupUi(BurySmartMeasureClass)
    initial_ui_config()

    chamber_radio_gr = QtWidgets.QButtonGroup()
    chamber_radio_gr.addButton(ui.set_gradient_radio)
    chamber_radio_gr.addButton(ui.set_temp_radio)

    # Connect buttons to functions
    ui.refresh_dev_btn.clicked.connect(refresh_devices)
    ui.config_dev.clicked.connect(next_page)
    ui.next_pg1_btn.clicked.connect(next_page)
    ui.next_pg2_btn.clicked.connect(next_page)
    ui.steps_spb.valueChanged.connect(steps_change)
    ui.use_temp_chamber_chkbox.toggled.connect(use_chamber)
    ui.use_allowable_temp_err_chkbox.stateChanged.connect(chamber_temp_limit)
    ui.use_allowable_humidity_err_chkbox.stateChanged.connect(chamber_humidity_limit)
    ui.set_temp_radio.toggled.connect(select_limit_mode)
    ui.set_gradient_radio.toggled.connect(select_limit_mode)

    BurySmartMeasureClass.show()
    sys.exit(app.exec_())


