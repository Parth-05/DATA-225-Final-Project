import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QWidget
from utils import make_connection
import utils

# Components
from ErrorMessageDialog import ErrorMessageDialog
from ConfirmationMessageDialog import ConfirmationMessageDialog
from ConfirmOrderDialog import ConfirmOrderDialog
from PyQt5.QtGui import QPainter, QPixmap

class BackgroundWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(r"Project\Python Files\Images\BackgroundImage.jpg")  # Update with correct path
        painter.drawPixmap(self.rect(), pixmap)

class MenuDialog(QDialog):
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
        self.ui = uic.loadUi(r'UIFiles\Menu.ui')

        self.ui.setWindowTitle("Menu")

        self.ui.setStyleSheet("QDialog { background-image: url('Images/BackgroundImage.jpg'); }")
        self.background_widget = BackgroundWidget()

        # Initialize menu table
        self._initialize_menu_table()
        # Initialize categories menu
        self._initialize_categories_menu()

        #  category filter
        self.ui.categoryFilter.currentIndexChanged.connect(self.filter_results_by_category)

        # add to cart button
        self.ui.addToCartBtn.clicked.connect(self.add_to_cart)

        # proceed to oder confirmation button
        self.ui.proceedBtn.clicked.connect(self.proceed_to_confirm_order)

    
    # Show dialog
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
    
    def _initialize_categories_menu(self):
        """
        Initialize the category menu combo box with menu categories.
        """
        conn = make_connection(config_file = 'db_config.ini')
        cursor = conn.cursor()

        try:
        
            sql = """
                SELECT DISTINCT(Category) 
                FROM menu;
                """
            
            cursor.execute(sql)
            rows = cursor.fetchall()
            rows.append
            # Set the menu categories names.
            categories = [row for row in rows]
            # Add 'All' to the beginning of the categories list
            categories.insert(0, ('All',))
            for row in categories:
                category = row[0]
                self.ui.categoryFilter.addItem(category, row)  
        except Exception as e:
            print( "Error initializing the categories menu: ", e)
        finally:
            #  Close connection
            cursor.close()
            conn.close()

    def _adjust_column_widths(self):
        """
        Adjust the column widths of the products table to fit the contents.
        """
        header = self.ui.menuTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

    def _initialize_menu_table(self):
        """
        Clear the table and set the column headers.
        """
        self.ui.menuTable.clear()

        col = ['  Menu ID ','  Category ', '   Item Name   ', '   Price   ']
        self.ui.menuTable.setColumnCount(4)
        self.ui.menuTable.verticalHeader().setVisible(False)
        self.ui.menuTable.setHorizontalHeaderLabels(col)

        # Populate menu table
        self.populate_menu_table()

    def populate_menu_table(self):
        conn = make_connection(config_file = 'db_config.ini')
        cursor = conn.cursor()
        try:
            sql = """
                SELECT  Menu_ID, Category, Item_Name, Price
                FROM menu;
            """
        
            cursor.execute(sql)
            rows = cursor.fetchall()

            self.menu_items = rows

            self.ui.menuTable.setRowCount(len(rows))

            for row_index, row_data in enumerate(rows):
                for col_index, col_data in enumerate(row_data):
                    # Ensure col_data is a single value and create a QTableWidgetItem
                    item = QTableWidgetItem(str(col_data))
                    self.ui.menuTable.setItem(row_index, col_index, item) 

            self._adjust_column_widths()
        except Exception as e:
            print("Error in pupulating the menu table: ", e)
        finally:
            cursor.close()
            conn.close()
    
    def filter_results_by_category(self):
        conn = make_connection(config_file = 'db_config.ini')
        cursor = conn.cursor()
        selected_category = self.ui.categoryFilter.currentData()
        # self.ui.title_label.setText("Showing products whose Category ID = " + "".join(map(str, selected_category)))
        if selected_category[0] == "All":
            sql = """
                SELECT  Menu_ID, Category, Item_Name, Price
                FROM menu;
            """
            cursor.execute(sql)
        else:
            sql = """
                SELECT  Menu_ID, Category, Item_Name, Price
                    FROM menu Where Category = %s
                """
            cursor.execute(sql, (selected_category))
       
        rows = cursor.fetchall()

        # self.menu_items = rows

        self.ui.menuTable.setRowCount(len(rows))

        for row_index, row_data in enumerate(rows):
            for col_index, col_data in enumerate(row_data):
                # Ensure col_data is a single value and create a QTableWidgetItem
                item = QTableWidgetItem(str(col_data))
                self.ui.menuTable.setItem(row_index, col_index, item) 

        self._adjust_column_widths()
        cursor.close()
        conn.close()

    def add_to_cart(self):
        selectedItems = self.ui.menuTable.selectionModel().selectedRows()
        for row in selectedItems:
            item_id = self.ui.menuTable.item(row.row(), 0).text()  
            # Check if the item is already in the cart

            # Find if the item is already in the cart
            item_to_add = self.menu_items[int(item_id) - 1]
            item_found = False
            for i in range(len(self.cart)):
                # Assuming the first element of the tuple is the item ID
                if self.cart[i][0] == item_to_add[0]:
                    # Increase the quantity of the existing item
                    new_quantity = self.cart[i][-1] + 1
                    self.cart[i] = self.cart[i][:-1] + (new_quantity,)
                    item_found = True
                    break
            if not item_found:
                # Item not in cart, add it with a default quantity of 1
                self.cart.append(item_to_add + (1,))
            
            # # Old Correct Working Logic
            # if not item_found:
            #     # Item not in cart, add it with a default quantity of 1
            #     self.cart.append(item_to_add + (1,))

            # if self.menu_items[int(item_id) - 1] not in self.cart:
            #     item_to_add = self.menu_items[int(item_id) - 1]
            #     self.cart.append(item_to_add)
            # else:
            #     print("Item already present")  
            # print(self.menu_items[int(item_id) - 1])

    def proceed_to_confirm_order(self):
        utils.cart_items = self.cart
        self._confirm_order_dialog_ = ConfirmOrderDialog()
        self._confirm_order_dialog_.show_dialog()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MenuDialog()
    form.show_dialog()
    sys.exit(app.exec_())  