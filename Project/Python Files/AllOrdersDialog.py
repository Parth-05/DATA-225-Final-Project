import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QWidget, QApplication, QTableWidgetItem, QHeaderView
from utils import make_connection
import utils
from PyQt5.QtGui import QPainter, QPixmap

# Component Imports
from UpdateProfileDailog import UpdateProfileDialog
from MenuDialog import MenuDialog
from ErrorMessageDialog import ErrorMessageDialog
from ConfirmationMessageDialog import ConfirmationMessageDialog

class BackgroundWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(r"Project\Python Files\Images\BackgroundImage.jpg")  # Update with correct path
        painter.drawPixmap(self.rect(), pixmap)

class AllOrdersDialog(QDialog):
    '''
    The user profile dialog
    '''
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi(r'UIFiles\AllOrdersDialog.ui')
        self.ui.setWindowTitle("All Orders")

        self.ui.setStyleSheet("QDialog { background-image: url('Images/BackgroundImage.jpg'); }")
        self.background_widget = BackgroundWidget()
        
         # Initialize menu table
        self._initialize_order_history_table()

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
        header = self.ui.allOrdersTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

    def _initialize_order_history_table(self):
        """
        Clear the table and set the column headers.
        """
        self.ui.allOrdersTable.clear()

        col = ['  Order ID ','  Date ', '   Order Time (Hour)   ', '   Menu ID   ', '   Item Name   ', '   Unit Price   '
               , '   Quantity   ', '   User ID   ', '   Total   ']
        self.ui.allOrdersTable.setColumnCount(8)
        self.ui.allOrdersTable.verticalHeader().setVisible(False)
        self.ui.allOrdersTable.setHorizontalHeaderLabels(col)

        # Populate menu table
        self.populate_order_history_table()
    
    def populate_order_history_table(self):
        user_id = utils.loggedInUser[4]
        conn = make_connection(config_file = 'db_config.ini')
        cursor = conn.cursor()

        try:
            user_order_history_query = """
                        SELECT 
                        o.Order_ID,
                        o.Date,
                        o.Order_Time,
                        od.Menu_ID,
                        m.Item_Name,
                        od.Unit_Price,
                        od.Quantity,
                        o.User_ID,
                        ROUND(od.Unit_Price * od.Quantity, 2) AS Total_Price
                    FROM 
                        orders AS o
                    JOIN 
                        order_details AS od ON o.Order_ID = od.Order_ID
                    JOIN 
                        menu AS m ON od.Menu_ID = m.Menu_ID
                    ORDER BY 
                        o.Order_ID ASC, o.Date DESC, o.Order_Time DESC;

            """

            cursor.execute(user_order_history_query)
            rows = cursor.fetchall()

            self.ui.allOrdersTable.setRowCount(len(rows))

            for row_index, row_data in enumerate(rows):
                for col_index, col_data in enumerate(row_data):
                    # Ensure col_data is a single value and create a QTableWidgetItem
                    item = QTableWidgetItem(str(col_data))
                    self.ui.allOrdersTable.setItem(row_index, col_index, item) 

            self._adjust_column_widths()
        except Exception as e:
            print("Error fetching the order history! ", e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = AllOrdersDialog()
    form.show_dialog()
    sys.exit(app.exec_())  