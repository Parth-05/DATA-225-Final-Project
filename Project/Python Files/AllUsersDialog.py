import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView
from utils import make_connection
import utils

# Component Imports
from UpdateProfileDailog import UpdateProfileDialog
from MenuDialog import MenuDialog
from ErrorMessageDialog import ErrorMessageDialog
from ConfirmationMessageDialog import ConfirmationMessageDialog
from OrderHistoryDialog import OrderHistoryDialog

class AllUsersDialog(QDialog):
    '''
    The user profile dialog
    '''
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi(r'UIFiles\AllUsersDialog.ui')

        self._initialize_all_users_table()

    def show_dialog(self):
        self.ui.show()

    def _adjust_column_widths(self):
        """
        Adjust the column widths of the products table to fit the contents.
        """
        header = self.ui.allUsersTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

    def _initialize_all_users_table(self):
        """
        Clear the table and set the column headers.
        """
        self.ui.allUsersTable.clear()

        col = ['  User ID ','  Name ', '   Email   ', '   Phone   ', '   Role   ']
        self.ui.allUsersTable.setColumnCount(4)
        self.ui.allUsersTable.verticalHeader().setVisible(False)
        self.ui.allUsersTable.setHorizontalHeaderLabels(col)

        # Populate menu table
        self.populate_all_users_table()

    def populate_all_users_table(self):
        conn = make_connection(config_file = 'db_config.ini')
        cursor = conn.cursor()
        try:
            sql = """
                SELECT  User_ID, Name, Email, Phone, Role
                FROM Users;
            """
        
            cursor.execute(sql)
            rows = cursor.fetchall()

            self.menu_items = rows

            self.ui.allUsersTable.setRowCount(len(rows))

            for row_index, row_data in enumerate(rows):
                for col_index, col_data in enumerate(row_data):
                    # Ensure col_data is a single value and create a QTableWidgetItem
                    item = QTableWidgetItem(str(col_data))
                    self.ui.allUsersTable.setItem(row_index, col_index, item) 

            self._adjust_column_widths()
        except Exception as e:
            print("Error fetching all users: ", e)
        finally:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = AllUsersDialog()
    form.show_dialog()
    sys.exit(app.exec_())  