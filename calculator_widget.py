from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QComboBox, QWidget, QPushButton, QLabel

from calculator_tabs.abstract_calculator_tab import AbstractCalculatorTab
from calculator_tabs.normality_tab import NormalityTab
from calculator_tabs.t_test_tab import TTestTab
from calculator_tabs.chi_squared_tab import ChiSquaredTab
from calculator_tabs.correlation_coefficient_tab import CorrelationCoefficientTab


class CalculatorWidget(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)

        self.data_manager = data_manager

        self.layout = QVBoxLayout(self)

        # Dropdown menu as alternative way to pick a tab
        self.dropdown = QComboBox()
        self.dropdown.addItems([
            "Normality",
            "T-test",
            "Chi-squared test",
            "Correlation coefficient",
        ])
        self.dropdown.setCurrentIndex(0)
        self.layout.addWidget(self.dropdown)

        # Create the tabs
        self.normality_tab = NormalityTab(self.data_manager, self)
        self.t_test_tab = TTestTab(self.data_manager, self)
        self.chi_squared_tab = ChiSquaredTab(self.data_manager, self)
        self.correlation_coefficient_tab = CorrelationCoefficientTab(self.data_manager, self)

        # Create the tabs widget with all the tabs
        self.tabs_widget = QTabWidget()
        self.tabs_widget.addTab(self.normality_tab, "Normality")
        self.tabs_widget.addTab(self.t_test_tab, "T-test")
        self.tabs_widget.addTab(self.chi_squared_tab, "Chi-squared test")
        self.tabs_widget.addTab(self.correlation_coefficient_tab, "Correlation coefficient")
        # Hide the tabs bar
        self.tabs_widget.tabBar().setVisible(False)
        self.layout.addWidget(self.tabs_widget)

        # Sync the dropdown selector and tab selector
        self.tabs_widget.currentChanged.connect(self.dropdown.setCurrentIndex)
        self.dropdown.currentIndexChanged.connect(self.tabs_widget.setCurrentIndex)

        # Create feedback label
        self.feedback_label = QLabel("")
        self.layout.addWidget(self.feedback_label)
        # Fix the height of the label
        self.feedback_label.setFixedHeight(self.feedback_label.fontMetrics().height())

        # Button to update the results
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_results)
        self.layout.addWidget(self.update_button)

    def update_results(self):
        """Call the current widget to carry out the actual updating."""
        current_tab = self.tabs_widget.currentWidget()
        # Make sure tab is of the correct type and will have the required methods
        if isinstance(current_tab, AbstractCalculatorTab):
            # Call `update_results()` from the tab to actually update the results
            status = current_tab.update_results()
            self.feedback_label.setText(status)
        else:
            raise TypeError("Tab needs to be AbstractCalculatorTab class.")
