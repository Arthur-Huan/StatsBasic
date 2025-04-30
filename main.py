import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QSplitter

from database import DataManager
from input_widget import InputWidget
from calculator_widget import CalculatorWidget
from visualization_widget import VisualizationWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.data_manager = DataManager("data.sqlite", self)

        # Left: Input data, including from a file path or directly entering
        self.left_widget = InputWidget(self.data_manager, self)
        # Middle: Select the tests
        self.middle_widget = CalculatorWidget(self.data_manager, self)
        self.middle_widget.setMinimumSize(400, 0)
        # Right: Graphical representation of the data
        self.right_widget = VisualizationWidget(self.data_manager, self)

        # Set up the central widget as QSplitter
        self.central_splitter = QSplitter(Qt.Horizontal, self)
        self.central_splitter.addWidget(self.left_widget)
        self.central_splitter.addWidget(self.middle_widget)
        self.central_splitter.addWidget(self.right_widget)

        self.central_splitter.setStretchFactor(0, 1)
        self.central_splitter.setStretchFactor(1, 2)
        self.central_splitter.setStretchFactor(2, 1)

        self.setCentralWidget(self.central_splitter)

        self.setWindowTitle("StatsBasic")
        self.resize(1200, 750)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if "Breeze" in QApplication.style().objectName():
        app.setStyle("Breeze")
    else:
        app.setStyle("Fusion")
        print("Breeze is not available, using Fusion.")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
