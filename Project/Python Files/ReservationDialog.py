from PyQt5 import uic
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QDateEdit
from PyQt5.QtCore import QDate, QTime
import utils

# Component Imports
from AvailableTablesDialog import AvailableTablesDialog


class ReservationDialog(QWindow):
    """
    The main application window.
    """
    
    def __init__(self):
        """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        self.ui = uic.loadUi('UIFiles\ReservationDialog.ui')

        self.initialize_reservation_widgets()

        self.ui.chheckAvailabilityBtn.clicked.connect(self.check_reservation_availability)

    def show_dialog(self):
        self.ui.show()

    def initialize_reservation_widgets(self):
        # Date Widget
        self.ui.reservationDate.setMinimumDate(QDate.currentDate())
        self.ui.reservationDate.setMaximumDate(QDate.currentDate().addDays(14))

        # Time Widget
        self.ui.reservationTime.setMinimumTime(QTime(10, 0) if QDate.currentDate() == self.ui.reservationDate.selectedDate() else QTime.current())

        # Connect the calendar's signal to update the time range
        # self.ui.reservationDate.selectionChanged.connect(self.updateTimeRange)

    # Kind of Dead code function.
    def updateTimeRange(self):
        # Check if the selected date is today
        if self.ui.reservationDate.selectedDate() == QDate.currentDate():
            current_time = QTime.currentTime()
            # If the current time is past the operational hours
            if current_time.hour() >= 21:
                # Disable time edit if current hour is past 9 PM
                self.ui.reservationTime.setDisabled(True)
            elif current_time.hour() < 10:
                # If it's before 10 AM, set the minimum time to 10 AM
                self.ui.reservationTime.setDisabled(False)
                self.ui.reservationTime.setMinimumTime(QTime(10, 0))
            elif current_time.minute() > 0:
                # Set the minimum time to the next hour if current minutes are not 00
                self.ui.reservationTime.setDisabled(False)
                self.ui.reservationTime.setMinimumTime(QTime(current_time.hour() + 1, 0))
            else:
                # Set the minimum time to the current hour
                self.ui.reservationTime.setDisabled(False)
                self.ui.reservationTime.setMinimumTime(current_time)
        else:
            # If the selected date is not today, reset the time range to 10 AM - 9 PM
            self.ui.reservationTime.setDisabled(False)
            self.ui.reservationTime.setTimeRange(QTime(10, 0), QTime(21, 0))

    def check_reservation_availability(self):
        date = self.ui.reservationDate.selectedDate().toPyDate().strftime("%Y-%m-%d")
        time = self.ui.reservationTime.time().hour()
        number_of_guests = self.ui.noOfGuestsText.value()
        # print("Selected Date: ", date)
        print("Selected Time: ", time)
        print(number_of_guests)

        self._show_available_tables_dialog = AvailableTablesDialog()
        self._show_available_tables_dialog.check_table_availability(date, time, number_of_guests)
        self._show_available_tables_dialog.show_dialog()

    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = ReservationDialog()
    form.show_dialog()
    sys.exit(app.exec_())  