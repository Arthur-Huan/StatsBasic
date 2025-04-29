import os
from io import StringIO
import pandas as pd
from PySide6.QtWidgets import QWidget, QLineEdit, QLabel, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout

class InputWidget(QWidget):
    def __init__(self, data_manager, parent=None):
        super(InputWidget, self).__init__(parent)

        self.data_manager = data_manager

        self.layout = QVBoxLayout(self)

        # Input field for path to load data from specified file
        self.file_path_input = FilePathInput(self.data_manager, self)
        self.layout.addWidget(self.file_path_input)

        # Input field to directly put in data
        self.text_input = TextInput(self.data_manager, self)
        self.layout.addWidget(self.text_input)

        # Label to display feedback
        self.feedback_label = QLabel("")
        # Fix the height of the label
        self.feedback_label.setFixedHeight(self.feedback_label.fontMetrics().height())
        self.layout.addWidget(self.feedback_label)

        # Buttons to load the data
        self.load_path_button = QPushButton("Load from Path")
        self.load_text_button = QPushButton("Load from Text")
        # Connect the `returnPressed` signal to the `get_path` method
        self.load_path_button.clicked.connect(self.load_data_from_path)
        self.load_text_button.clicked.connect(self.load_data_from_text)

        # Put the two buttons side-by-side
        self.load_data_buttons = QWidget()
        load_data_layout = QHBoxLayout()
        load_data_layout.addWidget(self.load_path_button)
        load_data_layout.addWidget(self.load_text_button)
        self.load_data_buttons.setLayout(load_data_layout)
        self.layout.addWidget(self.load_data_buttons)

    def set_status(self, status):
        self.feedback_label.setText(status)

    def load_data_from_path(self):
        status = self.file_path_input.load_data()
        self.set_status(status)

    def load_data_from_text(self):
        status = self.text_input.load_data()
        self.set_status(status)


class FilePathInput(QLineEdit):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager

    def load_data(self):
        """
        Loads data from the file path input field into `self.data_manager`
        :return: Status message in string
        """
        status = self.validate_path()
        if status == 1:
            df = self.read_file()
            self.data_manager.set_data(df)
            return "Data loaded from file."
        else:
            return status

    # TODO: Validate that the file can be read correctly, not just if path is okay
    def validate_path(self):
        """
        :return: 1 if validated, string status message otherwise
        """
        path = self.text()
        valid_extensions = (".csv", ".xls", ".xlsx")
        if path == "":
            return "Path is empty."
        # Check if is a directory
        if  os.path.isdir(path):
            return "The path is a directory."
        # Check if is a file
        if not os.path.isfile(path):
            return "Missing file at the path."
        # Check file extension
        if not path.lower().endswith(valid_extensions):
            return "File type is not supported."
        # File extension is valid
        else:
            return 1

    def read_file(self):
        path = self.text()
        return pd.read_csv(path)


class TextInput(QTextEdit):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager

    def load_data(self):
        """
        Loads data from the text input field into `self.data_manager`
        :return: Status message in string
        """
        status = self.validate_text()
        if status == 1:
            df = self.read_text()
            self.data_manager.set_data(df)
            return "Data loaded from text input."
        else:
            return status

    def validate_text(self): # TODO: Actually validate the string properly
        """
        :return: 1 if validated, string status message otherwise
        """
        text = self.toPlainText()
        if text == "":
            return "Text input is empty."
        return 1

    def read_text(self):
        text = self.toPlainText()
        text_csv = StringIO(text)
        df = pd.read_csv(text_csv)
        return df
