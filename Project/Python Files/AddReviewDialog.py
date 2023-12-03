import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView, QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QPainter, QPixmap
from utils import make_connection
import utils

# component imports
from ConfirmationMessageDialog import ConfirmationMessageDialog
from ErrorMessageDialog import ErrorMessageDialog

class BackgroundWidget(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(r"Project\Python Files\Images\BackgroundImage.jpg")  # Update with correct path
        painter.drawPixmap(self.rect(), pixmap)

class AddReviewDialog(QDialog):
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
        self.ui = uic.loadUi(r'UIFiles\AddReviewDialog.ui')
        self.ui.setWindowTitle("Add Review")

        self.ui.setStyleSheet("QDialog { background-image: url('Images/BackgroundImage.jpg'); }")
        self.background_widget = BackgroundWidget()

        self.ui.addReviewBtn.clicked.connect(self.add_review)

    # Show user profile dialog
    def show_dialog(self):
        """
        Show this dialog.
        """
        self.ui.show()
    
    def set_menu_id(self, selected_menu_id):
        self.selected_order_menu_id = selected_menu_id

    def add_review(self):
        conn = make_connection(config_file = 'db_config.ini')
        cursor = conn.cursor()
        try:
            user_id = utils.loggedInUser[4]
            rating = self.ui.rating_text.value()
            comments = self.ui.comments_text.toPlainText()
            conn.start_transaction()
            add_review_query  = """
                    INSERT INTO review (Rating, Comment, Menu_ID, User_ID)
                    VALUES (%s, %s, %s, %s)
                """
            reservation_record = (rating, comments, self.selected_order_menu_id, user_id)
            cursor.execute(add_review_query , reservation_record)

            # Commit the transaction
            conn.commit()
            print("Review added successfully")
            self.ui.close()
            confirmationMessage = "Review added successfully."
            self._confirmation_message_dialog_ = ConfirmationMessageDialog()
            self._confirmation_message_dialog_.setMessageText(confirmationMessage)
            self._confirmation_message_dialog_.show_dialog()
            
        except Exception as e:
            conn.rollback()
            print("Error in adding the review: ", e)
            self.ui.close()
            errorMessage = "Error in adding the review"
            self._error_message_dialog_ = ErrorMessageDialog()
            self._error_message_dialog_.setErrorMessageText(errorMessage)
            self._error_message_dialog_.show_dialog()
        finally:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = AddReviewDialog()
    form.show_dialog()
    sys.exit(app.exec_()) 