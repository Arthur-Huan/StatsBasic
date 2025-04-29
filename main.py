import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget

from database import DataManager
from data_widget import DataWidget
from calculator_widget import CalculatorWidget
from visualization_widget import VisualizationWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.data_manager = DataManager()

        # Left: Input data, including from a file path or directly entering
        self.left_widget = DataWidget(self.data_manager, self)
        # Middle: Select the tests
        self.middle_widget = CalculatorWidget(self)
        # Right: Graphical representation of the data
        self.right_widget = VisualizationWidget(self.data_manager, self)

        self.central_widget = QWidget(self)
        grid_central = QHBoxLayout(self.central_widget)
        grid_central.addWidget(self.left_widget)
        grid_central.addWidget(self.middle_widget)
        grid_central.addWidget(self.right_widget)
        self.setCentralWidget(self.central_widget)

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
