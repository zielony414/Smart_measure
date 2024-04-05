import sys
from PyQt5 import QtWidgets, QtCore
from BurySmartMeasure import Ui_BurySmartMeasureClass

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BurySmartMeasureClass = QtWidgets.QMainWindow()
    ui = Ui_BurySmartMeasureClass()
    ui.setupUi(BurySmartMeasureClass)
    BurySmartMeasureClass.show()



    sys.exit(app.exec_())
