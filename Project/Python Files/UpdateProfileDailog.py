import sys

from ErrorMessageDialog import ErrorMessageDialog
from ConfirmationMessageDialog import ConfirmationMessageDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QTableWidgetItem, QHeaderView
from utils import make_connection
from PyQt5.QtGui import QPainter, QPixmap
import utils

class BackgroundWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(r"Project\Python Files\Images\BackgroundImage.jpg")  # Update with correct path
        painter.drawPixmap(self.rect(), pixmap)

# Components
from UpdatePasswordDialog import UpdatePasswordDialog

class UpdateProfileDialog(QDialog):
    '''
    The update user profile dialog
    '''
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi(r'UIFiles\UpdateProfileDialog.ui')
        self.ui.setWindowTitle("Update Profile")

        self.ui.setStyleSheet("QDialog { background-image: url('Images/BackgroundImage.jpg'); }")
        self.background_widget = BackgroundWidget()

        self.ui.saveBtn.clicked.connect(self.update_user)

        # UpdatePasswordDialog Component
        self.user_profile_dialog = UpdatePasswordDialog()
        self.ui.updatePasswordBtn.clicked.connect(self.open_update_password_dialog)

    
    # Show update profile dialog
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.nameTextField.setText(utils.loggedInUser[0])
        self.ui.emailTextField.setText(utils.loggedInUser[1])
        self.ui.phoneTextField.setText(utils.loggedInUser[2])
        self.ui.show()

    def update_user(self):
        conn = utils.make_connection(config_file = 'db_config.ini')
        cursor = conn.cursor()
        
        try:
            name = self.ui.nameTextField.text()
            email = self.ui.emailTextField.text()
            phone = self.ui.phoneTextField.text()
            role = utils.loggedInUser[3]
            userID = utils.loggedInUser[4]
            password = utils.loggedInUser[5]
            conn.start_transaction()
            sql = """
                    UPDATE users
                    SET Name = %s, Email = %s, Phone = %s 
                    WHERE User_ID = %s;
                """

            cursor.execute(sql, (name, email, phone, userID))
            conn.commit()

            # Update the loggedInUser global variable
            utils.loggedInUser = (name, email, phone, role, userID, password)

            print("User profile updated successfully.")
            self.ui.close()
            confirmationMessage = "Profile Updated Successfully."
            self._confirmation_message_dialog_ = ConfirmationMessageDialog()
            self._confirmation_message_dialog_.setMessageText(confirmationMessage)
            self._confirmation_message_dialog_.show_dialog()

        except Exception as e:
            conn.rollback()
            print("Error Updating the User Profile!")
            self.ui.close()
            errorMessage = "Error Updating the User Profile!"
            self._error_message_dialog_ = ErrorMessageDialog()
            self._error_message_dialog_.setErrorMessageText(errorMessage)
            self._error_message_dialog_.show_dialog()
        finally:
            cursor.close()
            conn.close()

    def open_update_password_dialog(self):
        self.user_profile_dialog.show_dialog()
        self.ui.close()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = UpdateProfileDialog()
    form.show_dialog()
    sys.exit(app.exec_())  