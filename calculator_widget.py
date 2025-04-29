from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel, QLineEdit


class CalculatorWidget(QTabWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)

        self.data_manager = data_manager

        # Create the "t-test" tab
        self.t_test_tab = QWidget()
        self.addTab(self.t_test_tab, "t-test")
        self.setup_t_test_tab()

        # Create the "chi-squared" tab
        self.chi_squared_tab = QWidget()
        self.addTab(self.chi_squared_tab, "chi-squared")
        self.setup_chi_squared_tab()

    def setup_t_test_tab(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Input 1:"))
        layout.addWidget(QLineEdit())
        layout.addWidget(QLabel("Input 2:"))
        layout.addWidget(QLineEdit())
        self.t_test_tab.setLayout(layout)

    def setup_chi_squared_tab(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Observed:"))
        layout.addWidget(QLineEdit())
        layout.addWidget(QLabel("Expected:"))
        layout.addWidget(QLineEdit())
        self.chi_squared_tab.setLayout(layout)
