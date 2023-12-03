from PyQt5 import uic
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QDateEdit
from PyQt5.QtCore import QDate, QTime
from utils import make_connection
import utils
from datetime import datetime

# Component Imports
class AvailableTablesDialog(QWindow):
    """
    The main application window.
    """
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        self.ui = uic.loadUi('UIFiles\AvailableTablesDialog.ui')

        # Initialize table
        self._initialize_confirm_order_table()

        self.ui.confirmReservationBtn.clicked.connect(self.confirm_Reservation)

    def show_dialog(self):
        self.ui.show()

    def _adjust_column_widths(self):
        """
        Adjust the column widths of the products table to fit the contents.
        """
        header = self.ui.availableTablesTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
    
    def _initialize_confirm_order_table(self):
        """
        Clear the table and set the column headers.
        """
        self.ui.availableTablesTable.clear()

        col = ['  Table Number ','  Seating Capacity ', '   Table Location   ']
        self.ui.availableTablesTable.setColumnCount(3)
        self.ui.availableTablesTable.verticalHeader().setVisible(False)
        self.ui.availableTablesTable.setHorizontalHeaderLabels(col)


    def check_table_availability(self, res_date, res_time, guest_count):
        self.res_date = res_date
        self.res_time = res_time
        self.guest_count = guest_count
        conn = make_connection(config_file = 'db_config.ini')
        cursor = conn.cursor()
        try:
            sql = """
                SELECT td.Table_ID, td.Seating_Capacity, td.Location
                FROM table_details td
                WHERE td.Table_ID NOT IN (
                    SELECT r.Table_ID
                    FROM reservation r
                    WHERE r.Date = %s
                    AND r.Reservation_Time = %s
                )
                AND td.Seating_Capacity >= %s
            """
            reservation_details = (res_date, res_time, guest_count)
            cursor.execute(sql, reservation_details)
            rows = cursor.fetchall()

            self.menu_items = rows

            self.ui.availableTablesTable.setRowCount(len(rows))

            for row_index, row_data in enumerate(rows):
                for col_index, col_data in enumerate(row_data):
                    # Ensure col_data is a single value and create a QTableWidgetItem
                    item = QTableWidgetItem(str(col_data))
                    self.ui.availableTablesTable.setItem(row_index, col_index, item) 

            self._adjust_column_widths()
        except Exception as e: 
            print("Error fetching available tables: ", e)
        finally:
            cursor.close()
            conn.close()

    def confirm_Reservation(self):
        selectedTable = self.ui.availableTablesTable.selectionModel().selectedRows()
        row_index = selectedTable[0].row()
        values = [self.ui.availableTablesTable.item(row_index, column).text() for column in range(self.ui.availableTablesTable.columnCount())]
        self.selected_table_id = values[0]
        print(values[0])  # This will print all the values from the selected row
        print(self.res_date, self.res_time, self.guest_count)

        # Convert the string to a datetime object
        date_obj = datetime.strptime(self.res_date, "%Y-%m-%d")
        self.day_of_week = (date_obj.weekday() + 1) % 7  # Monday is 0 and Sunday is 6
        user_id = utils.loggedInUser[4]
        
        conn = make_connection(config_file = 'db_config.ini')
        cursor = conn.cursor()
        try:
            pass
            # Start a transaction
            conn.start_transaction()
            make_reservation_query  = """
                    INSERT INTO reservation (Day_Of_Week, date, Reservation_Time, Number_of_Guests, User_ID, Table_ID)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
            reservation_record = (self.day_of_week, self.res_date, self.res_time, self.guest_count, user_id, self.selected_table_id)
            cursor.execute(make_reservation_query , reservation_record)

            # Commit the transaction
            conn.commit()
            print("Reservation made successfully")
        except Exception as e:
            # Rollback the transaction in case of error
            conn.rollback()
            print("Error making the reservation: ", e)
        finally:
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = AvailableTablesDialog()
    form.show_dialog()
    sys.exit(app.exec_()) 