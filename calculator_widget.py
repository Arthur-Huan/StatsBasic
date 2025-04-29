from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QComboBox

from calculator_tabs.normality_tab import NormalityTab
from calculator_tabs.t_test_tab import TTestTab
from calculator_tabs.chi_squared_tab import ChiSquaredTab
from calculator_tabs.correlation_coefficient_tab import CorrelationCoefficientTab
from calculator_tabs.anova_tab import ANOVATab


class CalculatorWidget(QTabWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)

        self.data_manager = data_manager

        layout = QVBoxLayout(self)

        self.tabs_widget = QTabWidget()
        self.normality_tab = NormalityTab(self.data_manager, self)
        self.tabs_widget.addTab(self.normality_tab, "Normality")
        self.t_test_tab = TTestTab(self.data_manager, self)
        self.tabs_widget.addTab(self.t_test_tab, "T-test")
        self.chi_squared_tab = ChiSquaredTab(self.data_manager, self)
        self.tabs_widget.addTab(self.chi_squared_tab, "Chi-squared test")
        self.correlation_coefficient_tab = CorrelationCoefficientTab(self.data_manager, self)
        self.tabs_widget.addTab(self.correlation_coefficient_tab, "Correlation coefficient")
        self.anova_tab = ANOVATab(self.data_manager, self)
        self.tabs_widget.addTab(self.anova_tab, "ANOVA")
        layout.addWidget(self.tabs_widget)

        self.dropdown = QComboBox()
        self.dropdown.addItems([
            "Normality",
            "T-test",
            "Chi-squared test",
            "Correlation coefficient",
            "ANOVA"
        ])
        self.dropdown.setCurrentIndex(0)
        layout.addWidget(self.dropdown)

        # Sync the dropdown selector and tab selector
        self.tabs_widget.currentChanged.connect(self.dropdown.setCurrentIndex)
        self.dropdown.currentIndexChanged.connect(self.tabs_widget.setCurrentIndex)
