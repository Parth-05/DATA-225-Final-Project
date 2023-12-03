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

class DashboardDialog(QDialog):
    '''
    The dashboard profile dialog
    '''
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        # self.ui = uic.loadUi(r'UIFiles\UserProfile.ui')
        self.ui = uic.loadUi(r'UIFiles\DashboardDialog.ui')
        self.ui.setWindowTitle("User Profile")
        self.ui.setStyleSheet("QDialog { background-image: url('Images/BackgroundImage.jpg'); }")
        self.background_widget = BackgroundWidget()

        self._initialize_month_filter()
        self._initialize_year_filter()

        self.ui.monthFilter.currentIndexChanged.connect(self.plot_daily_sales_revenue)
        self.ui.yearFilter.currentIndexChanged.connect(self.plot_daily_sales_revenue)
        # self.plot_daily_sales_revenue()
        # self.top_selling_menu_items()
        self._initialize_chart_filter_menu()
        self.ui.chartFilter.currentIndexChanged.connect(self._plot_visualization)

    # Show dialog
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()

    def _initialize_chart_filter_menu(self):
        """
        Initialize the chart_categories.
        """

        try:
            # Set the chart_categories.
            chart_categories = ["Daily Sales Revenue", "Top Selling Menu Items"]
            # Add 'All' to the beginning of the categories list
            for row in chart_categories:
                category = row
                self.ui.chartFilter.addItem(category, row)
        except Exception as e:
            print( "Error initializing the chart categories menu: ", e)
        finally:
            # self.plot_top_menu_item_visualization()
            self._plot_visualization()
    
    def _plot_visualization(self):
        selected_chart_category = self.ui.chartFilter.currentData()
        if selected_chart_category == "Daily Sales Revenue":
            self.ui.monthFilter.setVisible(True)
            self.ui.yearFilter.setVisible(True)
            self.plot_daily_sales_revenue()
        elif selected_chart_category == "Top Selling Menu Items":
            self.ui.monthFilter.setVisible(False)
            self.ui.yearFilter.setVisible(False)
            self.top_selling_menu_items()
        else:
            self.plot_daily_sales_revenue()
    

    def _initialize_month_filter(self):
        """
        Initialize the category combo box with months.
        """
        wh_conn = make_connection(config_file='wh_config.ini')
        wh_cursor = wh_conn.cursor()

        try:
        
            sql = """
                SELECT DISTINCT
                CASE month
                    WHEN 1 THEN 'January'
                    WHEN 2 THEN 'February'
                    WHEN 3 THEN 'March'
                    WHEN 4 THEN 'April'
                    WHEN 5 THEN 'May'
                    WHEN 6 THEN 'June'
                    WHEN 7 THEN 'July'
                    WHEN 8 THEN 'August'
                    WHEN 9 THEN 'September'
                    WHEN 10 THEN 'October'
                    WHEN 11 THEN 'November'
                    WHEN 12 THEN 'December'
                END as month_name
                FROM date_dim
                ORDER BY month;

                """
            
            wh_cursor.execute(sql)
            rows = wh_cursor.fetchall()
            # Set the menu months names.
            months = [row for row in rows]
            # Add 'All' to the beginning of the months list
            for row in months:
                category = row[0]
                self.ui.monthFilter.addItem(category, row)
        except Exception as e:
            print( "Error initializing the months menu: ", e)
        finally:
            #  Close connection
            wh_cursor.close()
            wh_cursor.close()

    def _initialize_year_filter(self):
        """
        Initialize the category combo box with months.
        """
        wh_conn = make_connection(config_file='wh_config.ini')
        wh_cursor = wh_conn.cursor()

        try:
        
            sql = """
                SELECT DISTINCT
                CASE year
                    WHEN 2023 THEN '2023'
                    WHEN 2022 THEN '2022'
                    WHEN 2021 THEN '2021'
                    WHEN 2020 THEN '2020'
                END as Year
                FROM date_dim
                ORDER BY year;

                """
            
            wh_cursor.execute(sql)
            rows = wh_cursor.fetchall()
            # Set the menu months names.
            months = [row for row in rows]
            # Add 'All' to the beginning of the months list
            for row in months:
                category = row[0]
                self.ui.yearFilter.addItem(category, row)
        except Exception as e:
            print( "Error initializing the year filter: ", e)
        finally:
            #  Close connection
            wh_cursor.close()
            wh_cursor.close()

    def plot_daily_sales_revenue(self):
        wh_conn = make_connection(config_file='wh_config.ini')
        wh_cursor = wh_conn.cursor()

        try:
            month_mapping = {
                'January': 1,
                'February': 2,
                'March': 3,
                'April': 4,
                'May': 5,
                'June': 6,
                'July': 7,
                'August': 8,
                'September': 9,
                'October': 10,
                'November': 11,
                'December': 12
            }
            selected_year = self.ui.yearFilter.currentData()  
            selected_month_name = self.ui.monthFilter.currentData()
            selected_month = month_mapping[selected_month_name[0]]
            # Query to get daily sales revenue
            daily_sales_query = """
                SELECT 
                d.day, 
                SUM(s.total_sale_amount) as daily_sales
            FROM 
                sales_fact s
            JOIN 
                date_dim d ON s.date_id_day = d.day 
                AND s.date_id_month = d.month 
                AND s.date_id_year = d.year
            WHERE 
                d.year = %s AND d.month = %s
            GROUP BY 
                d.day
            ORDER BY 
                d.day;
            """
            # Execute the query
            wh_cursor.execute(daily_sales_query, (selected_year[0], selected_month))
            rows = wh_cursor.fetchall()

            # Create DataFrame from the query result
            daily_sales_df = pd.DataFrame(rows, columns=[desc[0] for desc in wh_cursor.description])
            daily_sales = daily_sales_df[['day', 'daily_sales']]

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
            ax.plot(daily_sales['day'], daily_sales['daily_sales'], marker='o', color='blue')
            ax.set_title('Daily Sales Revenue')
            ax.set_xlabel('Day of the Month')
            ax.set_ylabel('Total Sales ($)')
            ax.grid(True)  # Optional: Add grid for better readability
            self.mplwidget.canvas.draw()

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            wh_cursor.close()
            wh_conn.close()
    
    def top_selling_menu_items(self):
        wh_conn = make_connection(config_file='wh_config.ini')
        wh_cursor = wh_conn.cursor()

        try:
            # Query to get the top selling menu items
            top_selling_items_query = """
                SELECT 
                    m.item_name, 
                    SUM(s.quantity) as total_quantity_sold
                FROM 
                    menu_dim m
                JOIN 
                    sales_fact s ON m.menu_id = s.menu_id
                GROUP BY 
                    m.item_name
                ORDER BY 
                    total_quantity_sold DESC
                LIMIT 3;
            """
            # Execute the query
            wh_cursor.execute(top_selling_items_query)
            rows = wh_cursor.fetchall()

            # Create DataFrame from the query result
            top_selling_items_df = pd.DataFrame(rows, columns=[desc[0] for desc in wh_cursor.description])
            top_selling_items = top_selling_items_df[['item_name', 'total_quantity_sold']]

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
            ax2 = self.mplwidget.figure.clear()  # Clear the figure
            ax2 = self.mplwidget.figure.add_subplot(111)
            ax2.clear()  # Clear any existing plot
            ax2.bar(top_selling_items['item_name'], top_selling_items['total_quantity_sold'], color='skyblue')
            ax2.set_title('Top Selling Menu Items')
            ax2.set_xlabel('Menu Item')
            ax2.set_ylabel('Quantity Sold')
            ax2.set_ylim(0, top_selling_items['total_quantity_sold'].max() + 10)  # Add a little space on top
            self.mplwidget.canvas.draw()

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            wh_cursor.close()
            wh_conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = DashboardDialog()
    form.show_dialog()
    sys.exit(app.exec_())  