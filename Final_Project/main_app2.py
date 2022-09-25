import sys
import os
import numpy as np
import pandas as pd
import csv
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from .designer_app import Ui_MainWindow
from .dialog import Ui_SettingsDialog
from .build_face_dataset import start_capture
from .recognize_video1 import takeAttendance, pandas_manipulation
from .train_model1 import train_model
from os import path
from dateutil.parser import parse


class CsvTableModel(qtc.QAbstractTableModel):
    """The model for a CSV table."""

    def __init__(self, csv_file):
        super().__init__()
        self.filename = csv_file
        with open(self.filename) as fh:
            csvreader = csv.reader(fh)
            self._headers = next(csvreader)
            self._data = list(csvreader)

    # Minimum necessary methods:
    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._headers)

    def data(self, index, role):
        # original if statement:
        # if role == qtc.Qt.DisplayRole:
        # Add EditRole so that the cell is not cleared when editing
        if role in (qtc.Qt.DisplayRole, qtc.Qt.EditRole):
            return self._data[index.row()][index.column()]

    # Additional features methods:

    def headerData(self, section, orientation, role):

        if orientation == qtc.Qt.Horizontal and role == qtc.Qt.DisplayRole:
            return self._headers[section]
        else:
            return super().headerData(section, orientation, role)

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()  # needs to be emitted before a sort
        self._data.sort(key=lambda x: x[column])
        if order == qtc.Qt.DescendingOrder:
            self._data.reverse()
        self.layoutChanged.emit()  # needs to be emitted after a sort

    # Methods for Read/Write

    def flags(self, index):
        return super().flags(index) | qtc.Qt.ItemIsEditable

    def setData(self, index, value, role):
        if index.isValid() and role == qtc.Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    # Methods for inserting or deleting

    def insertRows(self, position, rows, parent):
        self.beginInsertRows(parent or qtc.QModelIndex(), position, position + rows - 1)

        for i in range(rows):
            default_row = [""] * len(self._headers)
            self._data.insert(position, default_row)
        self.endInsertRows()

    def removeRows(self, position, rows, parent):
        self.beginRemoveRows(parent or qtc.QModelIndex(), position, position + rows - 1)
        for i in range(rows):
            del self._data[position]
        self.endRemoveRows()

    # method for saving
    def save_data(self):
        # commented out code below to fix issue with additional lines being added after saving csv file from the window.
        # with open(self.filename, 'w', encoding='utf-8') as fh:
        with open(self.filename, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(self._headers)
            writer.writerows(self._data)


class SettingsDialog(qtw.QDialog, Ui_SettingsDialog):
    """Dialog for setting the settings"""

    def __init__(self, settings, parent=None):
        super().__init__(parent, modal=True)
        self.setupUi(self)
        #         self.setLayout(qtw.QFormLayout())
        self.settings = settings
        #         self.layout().addRow(
        #             qtw.QLabel("<h1>Application Settings</h1>"),
        #         )

        self.show_warnings_cb.setChecked(
            settings.value("show_warnings", False, type=bool)
        )
        protopath = path.join(self.directory, 'constants', 'deploy.prototxt.txt')
        modelpath = path.join(self.directory, 'constants', 'res10_300x300_ssd_iter_140000.caffemodel')
        outpath = path.join(self.directory, 'changes', 'dataset')
        self.prototxt_file.setText(
            settings.value("prototxt_file", protopath, type=str)
        )
        self.model_file.setText(
            settings.value(
                "model_file",
                modelpath,
                type=str,
            )
        )
        self.output_folder.setText(
            settings.value("output_folder", outpath, type=str)
        )
        self.confidence_1.setValue(settings.value("confidence_1", 0.80, type=float))
        self.confidence_2.setValue(settings.value("confidence_2", 0.80, type=float))

        self.pushButton_ptf.clicked.connect(lambda: self.openFile(self.prototxt_file))
        self.pushButton_mf.clicked.connect(lambda: self.openFile(self.model_file))
        self.pushButton_opf.clicked.connect(
            lambda: self.openFile(self.output_folder, typ="folder")
        )
        self.pushButton_reset.clicked.connect(self.reset)
        
    directory = path.dirname(__file__)

    def accept(self):
        self.settings.setValue("show_warnings", self.show_warnings_cb.isChecked())
        self.settings.setValue("prototxt_file", self.prototxt_file.text())
        self.settings.setValue("model_file", self.model_file.text())
        self.settings.setValue("output_folder", self.output_folder.text())
        self.settings.setValue("confidence_1", self.confidence_1.value())
        self.settings.setValue("confidence_2", self.confidence_2.value())
        #         self.settings["show_warnings"] = self.show_warnings_cb.isChecked()
        super().accept()

    def reset(self):
        self.prototxt_file.setText(protopath)
        self.model_file.setText(modelpath)
        self.output_folder.setText(outpath)
        self.confidence_1.setProperty("value", 0.8)
        self.confidence_2.setProperty("value", 0.8)

    #         self.accept()
    #         self.settings.setValue(
    #             "prototxt_file",
    #             self.prototxt_file.text()
    #         )
    #         self.settings.setValue(
    #             "model_file",
    #             self.model_file.text()
    #         )
    #         self.settings.setValue(
    #             "output_folder",
    #             self.output_folder.text()
    #         )
    #         self.settings["show_warnings"] = self.show_warnings_cb.isChecked()
    #         super().accept()

    def openFile(self, file_returned, typ="file"):
        if typ == "file":
            filename, _ = qtw.QFileDialog.getOpenFileName(
                self,
                "Select a text file to open...",
                qtc.QDir.homePath(),
                "Text Files (*.txt) ;;Python Files (*.py) ;;All Files (*)",
                "Python Files (*.py)",
                #             qtw.QFileDialog.DontUseNativeDialog | qtw.QFileDialog.DontResolveSymlinks
            )
        else:
            filename = qtw.QFileDialog.getExistingDirectory(self, "Select Folder")
        if filename:
            try:
                #                 with open(filename, "r") as fh:
                #                     self.textedit.setText(fh.read())
                file_returned.setText(filename)
            except Exception as e:
                qtw.QMessageBox.critical(f"Could not load File: {e}")


class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    settings = qtc.QSettings(
        "Ihechi Festus000001", "Class Attendance | Face Recognition"
    )
    model = None

    def __init__(self):
        """MainWindow constructor"""
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Class Attendance Management System")
        # Main UI code goes here
        # Icons#
        start_recognitionIcon = self.style().standardIcon(qtw.QStyle.SP_MediaPlay)
        settingsIcon = self.style().standardIcon(qtw.QStyle.SP_DialogHelpButton)
        self.actionSettings.setIcon(settingsIcon)
        self.actionStart_Recognition.setIcon(start_recognitionIcon)

        self.toolBar.addAction(self.actionStart_Recognition)
        self.toolBar.addAction(self.actionSettings)

        self.actionStart_Recognition.triggered.connect(self.startAttendance)
        self.actionSettings.triggered.connect(self.show_settings)
        self.capture_button.clicked.connect(self.capture_biometrics)
        self.actionQuit.triggered.connect(self.close)
        self.takeAttendancebutton.clicked.connect(self.startAttendance)
        self.trainModelbutton.clicked.connect(self.startTraining)
        self.openFile_button.clicked.connect(self.select_file)
        self.saveFile_button.clicked.connect(self.save_and_refresh)
        self.course_btn.clicked.connect(self.view_course_details)

        if self.settings.value("show_warnings", True, type=bool):
            qtw.QMessageBox.information(
                self,
                "Important Information!",
                "Make sure to capture atleast 10 images of the face at different angles, pose and illumination etc!!!, Press q to exit the camera and k to save images.",
                qtw.QMessageBox.Ok,
                qtw.QMessageBox.Ok,
            )
        # End main UI code
        self.show()

    def startTraining(self):

        notice = qtw.QMessageBox.information(
            self,
            "Training Model!",
            "Please wait as this may take some time!",
            qtw.QMessageBox.Ok,
            qtw.QMessageBox.Ok,
        )
        confidence_1 = self.settings.value("confidence_1", 0.8, type=float)
        tm = train_model(confidence_1)
        qtw.QMessageBox.information(
            self,
            "Trained Model!",
            "Face embeddings have been extracted and the model trained!",
            qtw.QMessageBox.Ok,
            qtw.QMessageBox.Ok,
        )
    directory = path.dirname(__file__)

    def startAttendance(self):
        confidence_2 = self.settings.value("confidence_2", 0.8, type=float)
        students = takeAttendance(confidence_2)
        if students:
            qtw.QMessageBox.information(
                self,
                "Attendance Taken!",
                str(students) + " found and attendance record updated",
                qtw.QMessageBox.Ok,
                qtw.QMessageBox.Ok,
            )
        else:
            qtw.QMessageBox.information(
                self,
                "Attendance Taken!",
                "No student details updated",
                qtw.QMessageBox.Ok,
                qtw.QMessageBox.Ok,
            )

    def capture_biometrics(self):
        
        protopath = path.join(self.directory, 'constants', 'deploy.prototxt.txt')
        modelpath = path.join(self.directory, 'constants', 'res10_300x300_ssd_iter_140000.caffemodel')
        outpath = path.join(self.directory, 'changes', 'dataset')
        prototxt_file = self.settings.value(
            "prototxt_file", protopath, type=str
        )
        model_file = self.settings.value(
            "model_file", modelpath, type=str
        )
        output_folder = self.settings.value(
            "output_folder", outpath, type=str
        )
        confidence_1 = self.settings.value("confidence_1", 0.8, type=float)

        student_surname = self.surname.text().title()
        student_first_name = self.first_name.text().title()
        student_other_names = self.other_names.text().title()
        course = self.course_code.text().lower()
        matric_num = self.mat_no.text().upper()
        email_add = self.email.text().lower()
        program = self.program.text().title()
        level = self.level.value()
        name = student_surname + " " + student_first_name + " " + student_other_names
        # print(name, course, matric_num)
        if all(
            [
                student_surname,
                student_first_name,
                student_other_names,
                matric_num,
                course,
                program,
                level,
            ]
        ):
            self.check_details(name, matric_num, course, email_add, level, program)
            total = start_capture(
                name, prototxt_file, model_file, output_folder, confidence_1
            )
            self.reset_form()
            qtw.QMessageBox.information(
                self,
                "Face Capture Successful!",
                str(total) + " face images of " + str(name) + " stored",
                qtw.QMessageBox.Ok,
                qtw.QMessageBox.Ok,
            )
        else:

            qtw.QMessageBox.warning(
                self,
                "Error Message",
                "You have not Entered all the required details. Please Enter the required details and try again.",
                qtw.QMessageBox.Close,
                qtw.QMessageBox.Close,
            )
            ## print("Couldn't process, all fields not filled")

    def show_settings(self):
        settings_dialog = SettingsDialog(self.settings, self)
        settings_dialog.exec()

    def reset_form(self):
        self.surname.setText("")
        self.first_name.setText("")
        self.other_names.setText("")
        self.course_code.setText("")
        self.mat_no.setText("")
        self.email.setText("")
        self.program.setText("")
        self.level.setProperty("value", 100)
        self.year.setProperty("value", 2021)

    def check_details(self, name, mat_no, course, email_add, level, program):
        student_details = []

        student_details.append(
            {
                "Name of the Student": name,
                "Matriculation Number": mat_no,
                "Program": program,
                "Level": level,
                "Email Address": email_add,
            }
        )

        course_data_file = path.join(self.directory, course + "_Students_data.csv")
        if not os.path.exists(course_data_file):
            # print("Yeah creating...")
            with open(course_data_file, "w+") as f:
                outputWriter = csv.writer(f)
                outputWriter.writerow(
                    [
                        "Name of the Student",
                        "Matriculation Number",
                        "Program",
                        "Level",
                        "Email Address",
                    ]
                )
                f.close()

        record = pd.read_csv(course_data_file)
        status = mat_no in list(record["Matriculation Number"])
        # for no in list(record["Matriculation Number"]):
        # print(mat_no, no, type(mat_no), type(no), mat_no == no)
        # print(status)

        if not status:
            student_details = pd.DataFrame(student_details)
            student_details.to_csv(
                course_data_file, mode="a", index=False, header=False
            )
        else:
            confirm = qtw.QMessageBox.question(
                self,
                "Register Again?",
                "User Details already registered, Do you want to continue?",
                qtw.QMessageBox.No | qtw.QMessageBox.Yes,
                qtw.QMessageBox.Yes,
            )
            if confirm != qtw.QMessageBox.Yes:
                # print("[ERROR] Exiting Application")
                sys.exit(-1)

    #                 CSV
    def select_file(self):
        try:
            filename = path.join(self.directory, 'attendance_records', 'Attendance_Records.csv')
            self.model = CsvTableModel(filename)
        except FileNotFoundError:
            # print("Here 1")
            self.save_and_refresh(first=1)
        self.tableView.setModel(self.model)

    def view_course_details(self):
        course_code = self.course_detail.text().lower()
        if course_code:
            try:
                filename = path.join(self.directory, course_code + "_Students_data.csv") 
                self.model = CsvTableModel(filename)
                self.tableView.setModel(self.model)
            except FileNotFoundError:
                 qtw.QMessageBox.warning(
                    self,
                    "Course Not Found!",
                    "No details found for " + course_code + ", Please try a new entry.",
                    qtw.QMessageBox.Close,
                    qtw.QMessageBox.Close,
                )

    def save_file(self):
        if self.model:
            self.model.save_data()

    def is_date(self, string, fuzzy=False):
        """
        Return whether the string can be interpreted as a date.

        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """
        try: 
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False

    def manipulate_data(self):
        file_name = path.join(self.directory, 'attendance_records', 'Attendance_Records.csv')
        try:
            v = pd.read_csv(file_name)
            v.drop(
                [
                    "Unnamed: 0",
                    "Total Number of classes Held",
                    "Total Number of classes Attended",
                    "Percentage Attendance",
                ],
                axis=1,
                inplace=True,
            )
        except FileNotFoundError:
            dirs = path.join(self.directory, 'changes', 'dataset')
            all_names = os.listdir(dirs)
            x = []
            for name in all_names:
                if name != "unknown":
                    x.append(name.title())
            all_names = x
            v = pd.DataFrame()
            v["Student's Name"] = all_names
            return v
        j = 0
        for i in v.columns:
            if self.is_date(i):
                j += 1
        v["Total Number of classes Attended"] = v.values[:, 1:].sum(axis=1)
        v["Total Number of classes Held"] = j
        
        v["Percentage Attendance"] = (
            v["Total Number of classes Attended"] / v["Total Number of classes Held"]
        ) * 100
        v["Percentage Attendance"] = v["Percentage Attendance"].astype("float").round()
        return v

    def save_and_refresh(self, first=None):
        path_ =  path.join(self.directory, 'attendance_records')
        if not first:
            # print("Here")
            self.save_file()
        records = self.manipulate_data()
        if not os.path.exists(path_):
            # print("Creating Folder!")
            os.makedirs(path_)
        file_name = "Attendance_Records.csv"
        # print(file_name)
        # print(path)
        full_path = os.path.join(path_, file_name)
        # print(full_path)
        records.to_csv(full_path)
        # print("Saved")
        self.select_file()

    def remove_rows(self):
        selected = self.tableView.selectedIndexes()
        num_rows = len(set(index.row() for index in selected))
        if selected:
            self.model.removeRows(selected[0].row(), num_rows, None)

    #                 CSV
    def closeEvent(self, event):
        """
        Display a QMessageBox when asking the user if they want to
        quit the program.
        """
        # set up message box
        answer = qtw.QMessageBox.question(
            self,
            "Quit Application?",
            "Are you sure you want to Quit?",
            qtw.QMessageBox.No | qtw.QMessageBox.Yes,
            qtw.QMessageBox.Yes,
        )
        if answer == qtw.QMessageBox.Yes:
            event.accept()  # accept the event and close the application
        else:
            event.ignore()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
