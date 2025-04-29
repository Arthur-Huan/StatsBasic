from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QComboBox, QWidget, QPushButton

from calculator_tabs.abstract_calculator_tab import AbstractCalculatorTab
from calculator_tabs.normality_tab import NormalityTab
from calculator_tabs.t_test_tab import TTestTab
from calculator_tabs.chi_squared_tab import ChiSquaredTab
from calculator_tabs.correlation_coefficient_tab import CorrelationCoefficientTab
from calculator_tabs.anova_tab import ANOVATab


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
            "ANOVA"
        ])
        self.dropdown.setCurrentIndex(0)
        self.layout.addWidget(self.dropdown)

        # Create the tabs
        self.tabs_widget = QTabWidget()
        self.normality_tab = NormalityTab(self.data_manager, self)
        self.t_test_tab = TTestTab(self.data_manager, self)
        self.chi_squared_tab = ChiSquaredTab(self.data_manager, self)
        self.correlation_coefficient_tab = CorrelationCoefficientTab(self.data_manager, self)
        self.anova_tab = ANOVATab(self.data_manager, self)

        # Create the tabs widget with all the tabs
        self.tabs_widget.addTab(self.normality_tab, "Normality")
        self.tabs_widget.addTab(self.t_test_tab, "T-test")
        self.tabs_widget.addTab(self.chi_squared_tab, "Chi-squared test")
        self.tabs_widget.addTab(self.correlation_coefficient_tab, "Correlation coefficient")
        self.tabs_widget.addTab(self.anova_tab, "ANOVA")
        self.layout.addWidget(self.tabs_widget)

        # Sync the dropdown selector and tab selector
        self.tabs_widget.currentChanged.connect(self.dropdown.setCurrentIndex)
        self.dropdown.currentIndexChanged.connect(self.tabs_widget.setCurrentIndex)

        # Button to update the results
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_results)
        self.layout.addWidget(self.update_button)

    def update_results(self):
        current_tab = self.tabs_widget.currentWidget()
        if isinstance(current_tab, AbstractCalculatorTab):
            current_tab.update_results()
        else:
            raise TypeError("Tab needs to be AbstractCalculatorTab class.")
