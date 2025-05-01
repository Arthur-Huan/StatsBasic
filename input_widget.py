import os
from io import StringIO
import pandas as pd
from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QWidget, QLineEdit, QLabel, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, \
    QTableWidget, QTableWidgetItem, QMenu


# TODO: Add a selection widget so that when data is loaded, the user can save it and load it later again
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

        # UI to manage the data and interact with the data_manager
        self.data_manager_ui = DataManagerUI(self.data_manager, self)
        self.layout.addWidget(self.data_manager_ui)

    def set_status(self, status):
        self.feedback_label.setText(status)

    def load_data_from_path(self):
        status = self.file_path_input.import_data()
        self.set_status(status)

    def load_data_from_text(self):
        status = self.text_input.import_data()
        self.set_status(status)


class FilePathInput(QLineEdit):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager

    def import_data(self):
        """Loads data from the file path input field into `self.data_manager`
        :return: Status message in string
        """
        status = self.validate_path()
        if status == 1:
            df = self.read_file()
            self.data_manager.save_df(df)
            return "Data loaded from file."
        else:
            return status

    # TODO: Validate that the file can be read correctly, not just if path is okay
    def validate_path(self):
        """ Check if the file path is valid
         But NOT if the file itself is formatted correctly
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

    def import_data(self):
        """Loads data from the text input field into `self.data_manager`
        :return: Status message in string
        """
        status = self.validate_text()
        if status == 1:
            df = self.read_text()
            self.data_manager.save_d(df)
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


class DataManagerUI(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)

        self.data_manager = data_manager

        self.results_table = QTableWidget()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.results_table)

        # Set up behavior for when cells in the table are clicked
        self.results_table.cellClicked.connect(self.on_row_click)

        # Set up the context menu
        self.results_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.results_table.customContextMenuRequested.connect(self.show_context_menu)

        self.data_manager.data_changed.connect(self.update_ui)

        self.update_ui()

    def update_ui(self):
        # Get all DataFrames
        all_df = self.data_manager.get_df_list()
        if all_df is None:
            self.results_table.setRowCount(0)
            self.results_table.setColumnCount(0)
            return

        # Set table dimensions
        self.results_table.setRowCount(len(all_df))
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["ID", "Name", "Data"])

        # Populate the table with data
        for row_idx, (df_id, df_name, df_json) in enumerate(all_df):
            self.results_table.setItem(row_idx, 0, QTableWidgetItem(str(df_id)))
            self.results_table.setItem(row_idx, 1, QTableWidgetItem(df_name))
            self.results_table.setItem(row_idx, 2, QTableWidgetItem(df_json))

        # Resize columns
        self.results_table.resizeColumnToContents(0)

    def on_row_click(self, row, column):
        # Get the ID of the selected DataFrame
        df_id = int(self.results_table.item(row, 0).text())
        # Select the DataFrame in the data manager
        self.data_manager.select_df(df_id)

    def show_context_menu(self, position: QPoint):
        menu = QMenu(self)
        delete_row_action = menu.addAction("Delete")
        delete_all_action = menu.addAction("Delete All")
        action = menu.exec(self.results_table.mapToGlobal(position))

        if action == delete_row_action:
            row = self.results_table.currentRow()
            if row >= 0:
                df_id = int(self.results_table.item(row, 0).text())
                self.data_manager.delete_df(df_id)
                self.update_ui()
        elif action == delete_all_action:
            self.data_manager.delete_all_df()
            self.update_ui()

