import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QWidget, QHBoxLayout, QPushButton
from utils import make_connection
import utils
import datetime

# Components
from ErrorMessageDialog import ErrorMessageDialog
from ConfirmationMessageDialog import ConfirmationMessageDialog

class ConfirmOrderDialog(QDialog):
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
        self.ui = uic.loadUi(r'UIFiles\ConfirmOrderDialog.ui')

        # Initialize menu table
        self._initialize_confirm_order_table()

        # Increase Qty
        self.ui.incQtyBtn.clicked.connect(self.increase_quantity)
        # Decrease Qty
        self.ui.decQtyBtn.clicked.connect(self.decrease_quantity)
        # Remove Items
        self.ui.removeItemsBtn.clicked.connect(self.remove_items)

        # Place Order
        self.ui.placeOrderBtn.clicked.connect(self.place_order)

        # print(utils.cart_items)

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
        header = self.ui.confirmOrderTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)


    def _initialize_confirm_order_table(self):
        """
        Clear the table and set the column headers.
        """
        self.ui.confirmOrderTable.clear()

        col = ['  Menu ID ','  Category ', '   Item Name   ', '   Price   ', 'Quantity']
        self.ui.confirmOrderTable.setColumnCount(5)
        self.ui.confirmOrderTable.verticalHeader().setVisible(False)
        self.ui.confirmOrderTable.setHorizontalHeaderLabels(col)

        self._populate_confirm_order_table()

    def _populate_confirm_order_table(self):
        self.ui.confirmOrderTable.setRowCount(len(utils.cart_items))
    
        for row_index, row_data in enumerate(utils.cart_items):
                for col_index, col_data in enumerate(row_data):
                    # Ensure col_data is a single value and create a QTableWidgetItem
                    item = QTableWidgetItem(str(col_data))
                    self.ui.confirmOrderTable.setItem(row_index, col_index, item)

        self._adjust_column_widths() 


    def increase_quantity(self):
        selectedItems = self.ui.confirmOrderTable.selectionModel().selectedRows()
        for row in selectedItems:
            item_id = self.ui.confirmOrderTable.item(row.row(), 0).text()
            # Check if the item is already in the cart

            # Find if the item is already in the cart
            item_to_add = utils.cart_items[int(item_id) - 1]
            item_found = False

            for i in range(len(utils.cart_items)):
                # Assuming the first element of the tuple is the item ID
                if utils.cart_items[i][0] == item_to_add[0]:
                    # Increase the quantity of the existing item
                    new_quantity = utils.cart_items[i][-1] + 1
                    utils.cart_items[i] = utils.cart_items[i][:-1] + (new_quantity,)
                    item_found = True
                    break
            self._populate_confirm_order_table()

    def decrease_quantity(self):
        selectedItems = self.ui.confirmOrderTable.selectionModel().selectedRows()
        for row in selectedItems:
            item_id = self.ui.confirmOrderTable.item(row.row(), 0).text()
            # Check if the item is already in the cart

            # Find if the item is already in the cart
            item_to_add = utils.cart_items[int(item_id) - 1]

            for i in range(len(utils.cart_items)):
                # Assuming the first element of the tuple is the item ID
                if utils.cart_items[i][0] == item_to_add[0]:
                    # Increase the quantity of the existing item
                    new_quantity = utils.cart_items[i][-1] - 1
                    utils.cart_items[i] = utils.cart_items[i][:-1] + (new_quantity,)

                    if new_quantity > 0:
                        # Update the quantity of the existing item
                        utils.cart_items[i] = utils.cart_items[i][:-1] + (new_quantity,)
                    else:
                        # Remove the item from the cart
                        del utils.cart_items[i]
                    break
            self._populate_confirm_order_table()

    def remove_items(self):
        selectedItems = self.ui.confirmOrderTable.selectionModel().selectedRows()
        ids_to_remove = set()

        # Gather the IDs of all selected items
        for row in selectedItems:
            item_id = int(self.ui.confirmOrderTable.item(row.row(), 0).text())
            ids_to_remove.add(item_id)

        # Remove items from the cart
        utils.cart_items = [item for item in utils.cart_items if item[0] not in ids_to_remove]

        # Update the table to reflect the changes
        self._populate_confirm_order_table()

    def place_order(self):
        print(utils.cart_items)
        # Get the current system date and time
        now = datetime.datetime.now()
        day_of_week = now.weekday() + 1 # Monday is 1 and Sunday is 7
        month = now.month
        year = now.year
        # date = now.strftime('%Y-%m-%d')  # Format the date as YYYY-MM-DD
        # order_time = now.strftime('%H:%M:%S')  # 
        date_of_month = now.day
        order_hr_time = now.hour
        user_id = utils.loggedInUser[4]

        order_record = (day_of_week, month, year, date_of_month, order_hr_time, user_id)

        conn = make_connection(config_file = 'db_config.ini')
        cursor = conn.cursor()

        # Create Order
        try:
            # Start a transaction
            conn.start_transaction()
            insert_order_query  = """
                    INSERT INTO orders (Day_Of_week, Month, Year, Date, Order_Time, User_ID)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
            
            cursor.execute(insert_order_query , order_record)

            # Get the Order_ID of the newly inserted order
            order_id = cursor.lastrowid

            # Step 2: Insert selected items into the order_details table
            insert_order_details_query = """
                                            INSERT INTO order_details (Unit_Price, Quantity, Menu_ID, Order_ID)
                                            VALUES (%s, %s, %s, %s)
                                        """
            
            for item in utils.cart_items:
                menu_id = item[0]
                price = item[3]
                quantity = item[4]
                order_details_data = (price, quantity, menu_id, order_id)
                cursor.execute(insert_order_details_query, order_details_data)

            # Commit the transaction
            conn.commit()
            print("Order inserted successfully")
        except Exception as e:
            # Rollback the transaction in case of error
            conn.rollback()
            print("Error creating the order: ", e)
        finally:
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ConfirmOrderDialog()
    form.show_dialog()
    sys.exit(app.exec_())  