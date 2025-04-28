import os
import pandas as pd
from PySide6.QtWidgets import QWidget, QLineEdit, QLabel, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout


class DataWidget(QWidget):
    def __init__(self, data_manager, parent=None):
        super(DataWidget, self).__init__(parent)
        self.data_manager = data_manager

        self.layout = QVBoxLayout()

        # Input field for path to load data from specified file
        self.file_path_input = QLineEdit()
        self.layout.addWidget(self.file_path_input)
        # Input field to directly put in data
        self.text_input = QTextEdit()
        self.layout.addWidget(self.text_input)
        # Label to display feedback
        self.feedback_label = QLabel()
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

        self.setLayout(self.layout)

    def load_data_from_path(self):
        path = self.file_path_input.text()
        status = validate_path(path)
        if status == 1:
            data = read_file(path)
            self.data_manager.set_data(data)
            self.set_feedback("Data loaded from file.")
        else:
            self.set_feedback(status)

    def load_data_from_text(self):
        text = self.text_input.toPlainText()
        status = validate_text(text)
        if status == 1:
            data = read_text(text)
            self.data_manager.set_data(data)
            self.set_feedback("Data loaded from text input.")
        else:
            self.set_feedback(status)

    def set_feedback(self, status):
        self.feedback_label.setText(str(status))


def validate_path(path):
    """
    :param path:
    :return:
        0: Empty field
        1: Valid path
        -1: Is a directory
        -2: Is not a file
        -3: File type not supported
    """
    valid_extensions = (".csv", ".xls", ".xlsx")
    if path == "":
        return "Path is empty"
    # Check if is a directory
    if  os.path.isdir(path):
        return "The path is a directory"
    # Check if is a file
    if not os.path.isfile(path):
        return "Missing file at the path"
    # Check file extension
    if not path.lower().endswith(valid_extensions):
        return "File type is not supported"
    # File extension is valid
    else:
        return 1

def validate_text(text):
    """

    :param text:
    :return:
    """
    return "Text inputted, doing nothing tho"

def read_file(path):
    return pd.read_csv(path)

def read_text(text):
    return ""
