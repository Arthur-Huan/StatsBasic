from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel, QLineEdit


class CalculatorWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the "f-test" tab
        self.f_test_tab = QWidget()
        self.addTab(self.f_test_tab, "f-test")
        self.setup_f_test_tab()

        # Create the "chi-squared" tab
        self.chi_squared_tab = QWidget()
        self.addTab(self.chi_squared_tab, "chi-squared")
        self.setup_chi_squared_tab()

    def setup_f_test_tab(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Input 1:"))
        layout.addWidget(QLineEdit())
        layout.addWidget(QLabel("Input 2:"))
        layout.addWidget(QLineEdit())
        self.f_test_tab.setLayout(layout)

    def setup_chi_squared_tab(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Observed:"))
        layout.addWidget(QLineEdit())
        layout.addWidget(QLabel("Expected:"))
        layout.addWidget(QLineEdit())
        self.chi_squared_tab.setLayout(layout)
