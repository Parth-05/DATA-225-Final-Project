import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView
from utils import make_connection
import utils

class ErrorMessageDialog(QDialog):
    '''
    The update user profile dialog
    '''
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi(r'UIFiles\ErrorMessageDialog.ui')
    
    # Show Error Message Dialog
    def show_dialog(self):
        self.ui.show()

    '''
    This method sets the text in the error message dialog label
    '''
    def setErrorMessageText(self, message):
        self.ui.errorMessageLabel.setText(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ErrorMessageDialog()
    form.show_dialog()
    sys.exit(app.exec_())  