import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

class Small_window():

    def show_error(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText("An error occured: " + text)
        msg.setStandardButtons(QMessageBox.Ok)

        # Get the directory of the current script
        script_dir = os.path.dirname(__file__)
        # Construct the full path to the image
        image_path = os.path.join(script_dir, "qrcode.png")
    
        # Create an HTML string that includes the image
        html_text = f'<img src="{image_path}" width="200" height="200"><br>'
        msg.setInformativeText(html_text)
        msg.setTextFormat(Qt.RichText)

        msg.exec_()

    def show_warning(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setText("It is warning: " + text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def show_info(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Information")
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
