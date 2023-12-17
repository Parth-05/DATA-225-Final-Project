import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QPainter, QPixmap
from utils import make_connection
import utils

# Component Imports
from UpdateProfileDailog import UpdateProfileDialog
from MenuDialog import MenuDialog
from ErrorMessageDialog import ErrorMessageDialog
from ConfirmationMessageDialog import ConfirmationMessageDialog
from OrderHistoryDialog import OrderHistoryDialog
from AllUsersDialog import AllUsersDialog
from DashboardDialog import DashboardDialog
from AllOrdersDialog import AllOrdersDialog
from ReservationDialog import ReservationDialog
from ViewReservationsDialog import ViewReservationsDialog
from mplwidget import MplWidget  # This is your custom Matplotlib widget class

import pandas as pd
import matplotlib.pyplot as plt

class BackgroundWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(r"Project\Python Files\Images\BackgroundImage.jpg")  # Update with correct path
        painter.drawPixmap(self.rect(), pixmap)

class UserProfileDialog(QDialog):
    '''
    The user profile dialog
    '''
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        # self.ui = uic.loadUi(r'UIFiles\UserProfile.ui')
        self.ui = uic.loadUi(r'UIFiles\HomePage.ui')
        self.ui.setWindowTitle("User Profile")
        self.ui.setStyleSheet("QDialog { background-image: url('Images/BackgroundImage.jpg'); }")
        self.background_widget = BackgroundWidget()

        self._hide_admin_functionalities()


        # update profile action
        self.update_profile_dialog = UpdateProfileDialog()
        self.ui.updateProfileBtn.clicked.connect(self.show_update_profile_dialog)

        # menu button action
        self._menu_dialog_ = MenuDialog()
        self.ui.menuButton.clicked.connect(self.show_menu_dialog)

        # reservation button action
        self.ui.reservationBtn.clicked.connect(self.show_reservation_dialog)

        # order history button
        self.ui.orderHistoryBtn.clicked.connect(self.show_order_history_dialog)

        # all users button
        self.ui.showAllUsersBtn.clicked.connect(self.show_all_users_dialog)

        # dashboard button
        self.ui.dashboardBtn.clicked.connect(self.show_dashboard_dialog)

        # show all orders button
        self.ui.allOrdersBtn.clicked.connect(self.show_all_orders_dialog)

        # show view reservations button
        self.ui.allReservationsBtn.clicked.connect(self.show_view_reservations_dialog)

        self._initialize_categories_menu()
        self.ui.menuCategoryFilter.currentIndexChanged.connect(self.plot_top_menu_item_visualization)

        self.ui.exitBtn.clicked.connect(self.close_dialog)



    # Show user profile dialog
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()

    # hide admin functionalities if user is a customer
    def _hide_admin_functionalities(self):
        self.is_user_admin = True if utils.loggedInUser[3].lower() == 'admin' else False
        if self.is_user_admin:
            self.ui.showAllUsersBtn.setVisible(True)
            self.ui.dashboardBtn.setVisible(True)
            self.ui.allReservationsBtn.setVisible(True)
            self.ui.allOrdersBtn.setVisible(True)
        else:
            self.ui.showAllUsersBtn.setVisible(False)
            self.ui.dashboardBtn.setVisible(False)
            self.ui.allReservationsBtn.setText("View My Reservations")
            self.ui.allOrdersBtn.setVisible(False)
    

    def show_update_profile_dialog(self):
        self.update_profile_dialog.show_dialog()

    # Set the name of Logged in User
    def setLoggedInUserName(self, user):
        self.ui.userNameLabel.setText("Hi " + user[0])

    def show_menu_dialog(self):
        self._menu_dialog_.show_dialog()

    def show_reservation_dialog(self):
        self._reservation_dialog_ = ReservationDialog()
        self._reservation_dialog_.show_dialog()

    def show_order_history_dialog(self):
        self._order_history_dialog = OrderHistoryDialog()
        self._order_history_dialog.show_dialog()

    def show_all_users_dialog(self):
        self._all_users_dialog = AllUsersDialog()
        self._all_users_dialog.show_dialog()
        # self.ui.close()

    def show_dashboard_dialog(self):
        self._dashboard_dialog = DashboardDialog()
        self._dashboard_dialog.show_dialog()

    def show_all_orders_dialog(self):
        self._all_orders_dialog = AllOrdersDialog()
        self._all_orders_dialog.show_dialog()
        # self.ui.close()

    def show_view_reservations_dialog(self):
        self._view_reservations_dialog = ViewReservationsDialog()
        self._view_reservations_dialog.show_dialog()
        # self.ui.close()

    def _initialize_categories_menu(self):
        """
        Initialize the category menu combo box with menu categories.
        """
        wh_conn = make_connection(config_file='wh_config.ini')
        wh_cursor = wh_conn.cursor()

        try:
        
            sql = """
                SELECT DISTINCT(Category) 
                FROM menu_dim;
                """
            
            wh_cursor.execute(sql)
            rows = wh_cursor.fetchall()
            rows.append
            # Set the menu categories names.
            categories = [row for row in rows]
            # Add 'All' to the beginning of the categories list
            categories.insert(0, ('All',))
            for row in categories:
                category = row[0]
                self.ui.menuCategoryFilter.addItem(category, row)
        except Exception as e:
            print( "Error initializing the categories menu: ", e)
        finally:
            #  Close connection
            wh_cursor.close()
            wh_cursor.close()
            self.plot_top_menu_item_visualization()

    def plot_top_menu_item_visualization(self):
        wh_conn = make_connection(config_file='wh_config.ini')
        wh_cursor = wh_conn.cursor()
        selected_category = self.ui.menuCategoryFilter.currentData()
        try:
            if selected_category[0] == "All":
                top_3_items = """
                    SELECT 
                    m.menu_id,
                    m.item_name,
                    ROUND(AVG(m.rating), 2) as average_rating
                FROM 
                    menu_dim AS m
                JOIN 
                    sales_fact AS s ON m.menu_id = s.menu_id
                GROUP BY 
                    m.menu_id, 
                    m.item_name
                ORDER BY 
                    average_rating DESC
                LIMIT 3;
                """
                wh_cursor.execute(top_3_items)
            else:
                top_3_items = '''
                    SELECT 
                    m.menu_id,
                    m.item_name,
                    ROUND(AVG(m.rating), 2) as average_rating
                FROM 
                    menu_dim AS m
                JOIN 
                    sales_fact AS s ON m.menu_id = s.menu_id
                WHERE 
                    m.category = %s
                GROUP BY 
                    m.menu_id, 
                    m.item_name
                ORDER BY 
                    average_rating DESC
                LIMIT 3;
                    '''

                wh_cursor.execute(top_3_items, (selected_category[0],))

            rows = wh_cursor.fetchall()

            # Create DataFrame from the query result
            top_3_items_df = pd.DataFrame(rows, columns=[desc[0] for desc in wh_cursor.description])
            top_appetizers = top_3_items_df[['item_name', 'average_rating']]

            # Initialize mplwidget only once
            if not hasattr(self, 'mplwidget'):
                self.mplwidget = MplWidget(self.ui.display_graph_widget)
                layout = self.ui.display_graph_widget.layout()

                if layout is None:
                    layout = QVBoxLayout(self.ui.display_graph_widget)
                    self.ui.display_graph_widget.setLayout(layout)
                
                layout.addWidget(self.mplwidget)
                self.mplwidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Use the MplWidget to plot data
            ax = self.mplwidget.figure.clear()  # Clear the figure
            ax = self.mplwidget.figure.add_subplot(111)
            # Clear the existing plot before redrawing
            ax.clear()  # Clear any existing plot
            ax.bar(top_appetizers['item_name'], top_appetizers['average_rating'], color='skyblue')
            if selected_category[0] == "All":
                ax.set_title('Top 3 Rated Menu Items')
            else:
                ax.set_title('Top 3 Rated ' + selected_category[0])
            ax.set_xlabel('Menu Item')
            ax.set_ylabel('Average Rating')
            ax.set_ylim(0, 5)  # Assuming the rating is out of 5
            self.mplwidget.canvas.draw()

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            wh_cursor.close()
            wh_conn.close()

    # def filter_top_menu_item_visualization(self)

    def close_dialog(self):
        self.ui.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = UserProfileDialog()
    form.show_dialog()
    sys.exit(app.exec_())  