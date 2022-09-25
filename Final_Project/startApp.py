import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QMessageBox,
    QLineEdit,
    QPushButton,
    QCheckBox,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import time
from .Registration import CreateNewUser
from .main_app2 import MainWindow
import pickle
from os import path


class LoginUI(QWidget):
    def __init__(self):  # constructor
        super().__init__()

        self.initializeUI()

    def initializeUI(self):
        """
        Initialize the window and display its contents to the screen
        """
        self.setGeometry(100, 100, 400, 230)
        self.setWindowTitle("Login Page")
        self.loginUserInterface()

        self.show()
    directory = path.dirname(__file__)

    def loginUserInterface(self):
        """
        Create the login GUI.
        """
        login_label = QLabel(self)
        login_label.setText("Login")
        login_label.move(180, 10)
        login_label.setFont(QFont("Arial", 20))

        # username and password labels and line edit widgets
        name_label = QLabel("Email:", self)
        name_label.move(30, 60)

        self.name_entry = QLineEdit(self)
        self.name_entry.move(110, 60)
        self.name_entry.resize(220, 20)

        password_label = QLabel("Password:", self)
        password_label.move(30, 90)

        self.password_entry = QLineEdit(self)
        self.password_entry.move(110, 90)
        self.password_entry.resize(220, 20)

        # sign in push button
        sign_in_button = QPushButton("Login", self)
        sign_in_button.move(100, 140)
        sign_in_button.resize(200, 40)
        sign_in_button.clicked.connect(self.clickLogin)

        # display show password check box
        show_password_cb = QCheckBox("show password", self)
        show_password_cb.move(110, 115)
        show_password_cb.stateChanged.connect(self.displayPassword)
        show_password_cb.toggle()
        show_password_cb.setChecked(False)

        # display sign up label and push button
        not_a_member = QLabel("Not Reqistered?", self)
        not_a_member.move(100, 200)

        sign_up = QPushButton("Sign Up", self)
        sign_up.move(230, 195)
        sign_up.clicked.connect(self.createNewUser)

    def clickLogin(self):
        """
        When user clicks sign in button, check if username and password
        match any existing profiles in users.txt.
        If they exist, display messagebox and close program.
        If they don't, display error messagebox.
        """
        users = {}
        filename =  path.join(self.directory, 'files', 'users.pkl')
        try:
            with open(filename, "rb") as pkl_file:
                f = pickle.load(pkl_file)
                user_fields = f.split(" ")
                username = user_fields[0]
                password = user_fields[1].strip("\n")
                users[username] = password
        except FileNotFoundError:
            QMessageBox.information(
                self,
                "No User Registered!",
                "No user has been registered on this system, please go to the sign up page to register!",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok,
            )
            return None
        username = self.name_entry.text()
        # print(username)
        password = self.password_entry.text()
        if (username, password) in users.items():
            QMessageBox.information(
                self,
                "Login Successful!",
                "Login Successful!",
                QMessageBox.StandardButton.Ok,
                QMessageBox.StandardButton.Ok,
            )
            self.close()
            self.create_new_user_dialog = MainWindow()
            self.create_new_user_dialog.show()

        else:
            QMessageBox.warning(
                self,
                "Error Message",
                "The username or password is incorrect.",
                QMessageBox.StandardButton.Close,
                QMessageBox.StandardButton.Close,
            )

    def displayPassword(self, state):
        """
        If checkbutton is enabled, view password.
        Else, mask password so others can not see it.
        """
        if state == Qt.CheckState.Checked.value:
            self.password_entry.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)

    def createNewUser(self):
        """
        When the sign up button is clicked, open
        a new window and allow the user to create a new account.
        """
        self.create_new_user_dialog = CreateNewUser()
        self.create_new_user_dialog.show()


#     def closeEvent(self, event):
#         """
#         Display a QMessageBox when asking the user if they want to
#         quit the program.
#         """
#         # set up message box
#         answer = QMessageBox.question(self, "Quit Application?",
#             "Are you sure you want to Quit?", QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes,
#             QMessageBox.StandardButton.Yes)
#         if answer == QMessageBox.StandardButton.Yes or confirmation == "Yes":
#             event.accept() # accept the event and close the application
#         else:
#             event.ignore()

# Run program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginUI()
    sys.exit(app.exec_())
