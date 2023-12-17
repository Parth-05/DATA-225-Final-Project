import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QWidget
from utils import make_connection
import utils
from PyQt5.QtGui import QPainter, QPixmap

# Components
from ErrorMessageDialog import ErrorMessageDialog
from ConfirmationMessageDialog import ConfirmationMessageDialog

class BackgroundWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(r"Project\Python Files\Images\BackgroundImage.jpg")  # Update with correct path
        painter.drawPixmap(self.rect(), pixmap)

class UpdatePasswordDialog(QDialog):
    '''
    The update user profile dialog
    '''
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi(r'UIFiles\UpdatePasswordDialog.ui')
        self.ui.setWindowTitle("Update Password")

        self.ui.setStyleSheet("QDialog { background-image: url('Images/BackgroundImage.jpg'); }")
        self.background_widget = BackgroundWidget()

        # Action to perform on click of update password button
        self.ui.updatePasswordBtn.clicked.connect(self.updated_password)

    # Show update password dialog
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()

    # Update Password
    def updated_password(self):
        new_password = self.ui.newPassword.text()
        confirm_password = self.ui.confirmPassword.text()

        if new_password == confirm_password:
            self.perform_password_update(new_password)
        else:
            errorMessage = "Passwords do not match!"
            self._error_message_dialog_ = ErrorMessageDialog()
            self._error_message_dialog_.setErrorMessageText(errorMessage)
            self._error_message_dialog_.show_dialog()

    def perform_password_update(self, updated_password):
        name = utils.loggedInUser[0]
        email = utils.loggedInUser[1]
        phone = utils.loggedInUser[2]
        role = utils.loggedInUser[3]
        user_id = utils.loggedInUser[4]
        password = updated_password
        
        conn = utils.make_connection(config_file = 'db_config.ini')
        cursor = conn.cursor()
        try: 
            sql = """
                UPDATE users SET Password = %s WHERE User_ID = %s
                """
            cursor.execute(sql, (updated_password, user_id))
            conn.commit()

            # Update the loggedInUser global variable
            utils.loggedInUser = (name, email, phone, role, user_id, password)

            confirmationMessage = "Password updated successfully."
            self._confirmation_message_dialog_ = ConfirmationMessageDialog()
            self._confirmation_message_dialog_.setMessageText(confirmationMessage)
            self._confirmation_message_dialog_.show_dialog()
            self.ui.close()

        except Exception as e:
            errorMessage = "Error Updating the password"
            self._error_message_dialog_ = ErrorMessageDialog()
            self._error_message_dialog_.setErrorMessageText(errorMessage)
            self._error_message_dialog_.show_dialog()
            self.ui.close()
            print( "Error updating the password: ", e)
        finally:
            cursor.close()
            conn.close()
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = UpdatePasswordDialog()
    form.show_dialog()
    sys.exit(app.exec_())  