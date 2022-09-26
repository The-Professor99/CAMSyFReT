import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMessageBox,
    QPushButton,
    QLabel,
    QLineEdit,
)
from PyQt6.QtGui import QFont, QPixmap
import pickle
from os import path

def resourcePath(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        
        base_path = sys._MEIPASS
        base_path = path.join(base_path, "Final_Project")
    except Exception:
        base_path = path.dirname(__file__)
    return path.join(base_path, relative_path)

class CreateNewUser(QWidget):
    def __init__(self):
        super().__init__()

        self.initializeUI()  # call our function use to set up window

    def initializeUI(self):
        """
        Initialize the window and display its contents to the screen
        """
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle("Sign Up")

        self.displayWidgetsToCollectInfo()

        self.show()
    directory = path.dirname(__file__)

    def displayWidgetsToCollectInfo(self):
        """
        Create widgets that will be used to collect information
        from the user to create a new account.
        """
        # create label for image
        new_user_image = path.join(self.directory, 'images', "new_user_icon.png")
        try:
            with open(new_user_image):
                new_user = QLabel(self)
                pixmap = QPixmap(new_user_image)
                new_user.setPixmap(pixmap)
                new_user.move(150, 60)
        except FileNotFoundError:
            pass
            # # print("Image not found.")

        login_label = QLabel(self)
        login_label.setText("Sign Up")
        login_label.move(140, 20)
        login_label.setFont(QFont("Arial", 20))

        # username and fullname labels and line edit widgets
        name_label = QLabel("Email:", self)
        name_label.move(50, 180)

        self.name_entry = QLineEdit(self)
        self.name_entry.move(130, 180)
        self.name_entry.resize(200, 20)

        name_label = QLabel("Full Name:", self)
        name_label.move(50, 210)

        name_entry = QLineEdit(self)
        name_entry.move(130, 210)
        name_entry.resize(200, 20)

        # create password and confirm password labels and line edit widgets
        pswd_label = QLabel("Password:", self)
        pswd_label.move(50, 240)

        self.pswd_entry = QLineEdit(self)
        self.pswd_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.pswd_entry.move(130, 240)
        self.pswd_entry.resize(200, 20)

        confirm_label = QLabel("Confirm:", self)
        confirm_label.move(50, 270)

        self.confirm_entry = QLineEdit(self)
        self.confirm_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_entry.move(130, 270)
        self.confirm_entry.resize(200, 20)

        # create sign up button
        sign_up_button = QPushButton("Sign Up", self)
        sign_up_button.move(100, 310)
        sign_up_button.resize(200, 40)
        sign_up_button.clicked.connect(self.confirmSignUp)

    def confirmSignUp(self):
        """
        When user presses sign up, check if the passwords match.
        If they match, then save username and password text to users.txt.
        """
        pswd_text = self.pswd_entry.text()
        confirm_text = self.confirm_entry.text()

        if pswd_text != confirm_text:
            # display messagebox if passwords don't match
            QMessageBox.warning(
                self,
                "Error Message",
                "The passwords you entered do not match. Please try again.",
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close,
            )
        else:
            filename = resourcePath(path.join('files', 'users.pkl'))
            try:
                with open(filename, "rb") as f:
                    QMessageBox.warning(
                        self,
                        "Error Message",
                        "This system has already been signed up on, please input your Login details to login.",
                        QMessageBox.StandardButton.Close,
                        QMessageBox.StandardButton.Close,
                    )
            except FileNotFoundError:
                with open(filename, "ab") as f:
                    pickle.dump(self.name_entry.text() + " " + pswd_text + "\n", f)
            #                     pickle.dump(pswd_text + "\n", f)

            self.close()


# Run program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreateNewUser()
    sys.exit(app.exec_())
