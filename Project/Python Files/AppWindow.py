from PyQt5 import uic
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QDateEdit
from PyQt5.QtCore import QDate
import utils

# Component Imports
from RegisterUserDialog import RegisterUserDialog
from UserProfileDialog import UserProfileDialog


class AppWindow(QWindow):
    """
    The main application window.
    """
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        self.ui = uic.loadUi('UIFiles\LoginPage.ui')
        self.ui.show()

        # Register Users dialog.
        self._register_user_dialog = RegisterUserDialog()
        self.ui.registerButton.clicked.connect(self._show_register_user_dialog)

        # Action to perform on Login Button Click
        self.ui.loginButton.clicked.connect(self.login)

    def show_dialog(self):
        self.ui.show()

    def _show_register_user_dialog(self):
        """
        Show the register user dialog.
        """
        self._register_user_dialog.show_dialog()

    def login(self):
        # Get the entered email and password
        email = self.ui.email.text()
        password = self.ui.password.text()

        conn = utils.make_connection(config_file = 'db_config.ini')
        cursor = conn.cursor()
        sql = """
              SELECT * FROM users 
              WHERE Email = %s
              AND Password = %s
             """

        cursor.execute(sql, (email, password))
        user = cursor.fetchone()

        # Loading loginMessageDialogUi
        self.loginMessageDialogUi = uic.loadUi('UIFiles\LoginMessageDialog.ui')
        if user is not None:
            
            # set isUserLoggedIn to True
            utils.isUserLoggedIn = True
            utils.loggedInUser = user
            
            # User Profile dialog.
            self.user_profile_dialog = UserProfileDialog()
            self.user_profile_dialog.setLoggedInUserName(user)
            self.user_profile_dialog.show_dialog()

            # close ui and connection
            self.ui.close()
            conn.close()
        else:
            self.loginMessageDialogUi.LoginMessageLabel.setText('Incorrect Email or Password!')
            self.loginMessageDialogUi.show()
            
            # set isUserLoggedIn to True
            utils.isUserLoggedIn = False
            utils.loggedInUser = None

            print(utils.isUserLoggedIn)
            conn.close()