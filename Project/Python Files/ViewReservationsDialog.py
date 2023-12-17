import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QWidget, QHBoxLayout, QPushButton
from utils import make_connection
import utils
import datetime
from PyQt5.QtGui import QPainter, QPixmap

# Components
from ErrorMessageDialog import ErrorMessageDialog
from ConfirmationMessageDialog import ConfirmationMessageDialog

class BackgroundWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(r"Project\Python Files\Images\BackgroundImage.jpg")  # Update with correct path
        painter.drawPixmap(self.rect(), pixmap)

class ViewReservationsDialog(QDialog):
    '''
    The update user profile dialog
    '''
    cart = []
    menu_items = []
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi(r'UIFiles\ViewReservationsDialog.ui')

        self.ui.setWindowTitle("All Reservations")

        self.ui.setStyleSheet("QDialog { background-image: url('Images/BackgroundImage.jpg'); }")
        self.background_widget = BackgroundWidget()

        self._initialize_confirm_order_table()

    # Show dialog
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
    
    def _adjust_column_widths(self):
        """
        Adjust the column widths of the products table to fit the contents.
        """
        header = self.ui.viewReservationsTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)


    def _initialize_confirm_order_table(self):
        """
        Clear the table and set the column headers.
        """
        self.ui.viewReservationsTable.clear()

        col = ['  Reservation ID ', '    User ID     ', '  Reservation Date ', '   Reservation Time   ', 
               '   Number of Guests   ', '   Table ID   ', '   Name   ', '   Email   ',
               '   Phone   ', '   Table Location   ']
        self.ui.viewReservationsTable.setColumnCount(10)
        self.ui.viewReservationsTable.verticalHeader().setVisible(False)
        self.ui.viewReservationsTable.setHorizontalHeaderLabels(col)

        self._populate_confirm_order_table()

    def _populate_confirm_order_table(self):
        user_role = utils.loggedInUser[3]
        conn = make_connection(config_file = 'db_config.ini')
        cursor = conn.cursor()
        try:
            self.is_user_admin = True if utils.loggedInUser[3].lower() == 'admin' else False
            if self.is_user_admin:
                sql = """
                    SELECT 
                    r.Reservation_ID,
                    r.User_ID,
                    r.Date,
                    r.Reservation_Time,
                    r.Number_of_Guests,
                    r.Table_ID,
                    u.Name AS Name,
                    u.Email,
                    u.Phone,
                    t.Location
                FROM 
                    reservation r
                JOIN 
                    users u ON r.User_ID = u.User_ID
                JOIN 
                    table_details t ON r.Table_ID = t.Table_ID
                ORDER BY r.Reservation_ID;
                """
                cursor.execute(sql)
            else:
                user_id = utils.loggedInUser[4]
                sql = """
                    SELECT 
                    r.Reservation_ID,
                    r.User_ID,
                    r.Date,
                    r.Reservation_Time,
                    r.Number_of_Guests,
                    r.Table_ID,
                    u.Name AS Name,
                    u.Email,
                    u.Phone,
                    t.Location
                FROM 
                    reservation r
                JOIN 
                    users u ON r.User_ID = u.User_ID
                JOIN 
                    table_details t ON r.Table_ID = t.Table_ID
                WHERE r.User_ID = %s
                ORDER BY r.Reservation_ID;
                """
                cursor.execute(sql, (user_id, ))
        
            
            rows = cursor.fetchall()

            self.menu_items = rows

            self.ui.viewReservationsTable.setRowCount(len(rows))

            for row_index, row_data in enumerate(rows):
                for col_index, col_data in enumerate(row_data):
                    # Ensure col_data is a single value and create a QTableWidgetItem
                    item = QTableWidgetItem(str(col_data))
                    self.ui.viewReservationsTable.setItem(row_index, col_index, item) 

            self._adjust_column_widths()
        except Exception as e:
            print("Error fetching the reservations: ", e)
        finally:
            cursor.close()
            conn.close() 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ViewReservationsDialog()
    form.show_dialog()
    sys.exit(app.exec_())  