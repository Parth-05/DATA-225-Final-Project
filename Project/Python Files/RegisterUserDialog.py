import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView
from utils import make_connection

class RegisterUserDialog(QDialog):
    '''
    The register user dialog
    '''
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi('UIFiles\RegisterUserPage.ui')

        # register user
        self.ui.registerButton.clicked.connect(self.register_user)

    # Show register user dialog
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()

    # Register/Create a new user
    def register_user(self):
        try:
            name = self.ui.name.text()
            email = self.ui.email.text()
            password = self.ui.password.text()
            phone = self.ui.phone.text()
            role = 'Customer'

            conn = make_connection(config_file = 'db_config.ini')
            cursor = conn.cursor()
            conn.start_transaction()

            # sql = "INSERT INTO users (Name, Email, Password, Phone, Role) VALUES (%s, %s, %s, %s, %s)"
            sql = "CALL RegisterUser(%s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, email, password, phone, role))
            conn.commit()
            # Loading loginMessageDialogUi
            self.loginMessageDialogUi = uic.loadUi('UIFiles\LoginMessageDialog.ui')
            self.loginMessageDialogUi.LoginMessageLabel.setText('User Created Successfully.')
            self.loginMessageDialogUi.show()
        except Exception as e:
            conn.rollback()
            print(e)
            self.loginMessageDialogUi = uic.loadUi('UIFiles\LoginMessageDialog.ui')
            self.loginMessageDialogUi.LoginMessageLabel.setText('Error encountered while creating the user!')
            self.loginMessageDialogUi.show()
        finally:
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = RegisterUserDialog()
    form.show_dialog()
    sys.exit(app.exec_())  