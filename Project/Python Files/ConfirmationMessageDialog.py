import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QWidget, QApplication, QTableWidgetItem, QHeaderView
from utils import make_connection
import utils
from PyQt5.QtGui import QPainter, QPixmap

class BackgroundWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(r"Project\Python Files\Images\BackgroundImage.jpg")  # Update with correct path
        painter.drawPixmap(self.rect(), pixmap)

class ConfirmationMessageDialog(QDialog):
    '''
    The update user profile dialog
    '''
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi(r'UIFiles\ConfirmationDialog.ui')
        self.ui.setWindowTitle("Confirmation Dialog")

        self.ui.setStyleSheet("QDialog { background-image: url('Images/BackgroundImage.jpg'); }")
        self.background_widget = BackgroundWidget()
    
    # Show Error Message Dialog
    def show_dialog(self):
        self.ui.show()

    '''
    This method sets the text in the error message dialog label
    '''
    def setMessageText(self, message):
        self.ui.messageLabel.setText(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ConfirmationMessageDialog()
    form.show_dialog()
    sys.exit(app.exec_())  