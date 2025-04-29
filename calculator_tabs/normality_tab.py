from scipy.stats import shapiro
from PySide6.QtWidgets import QTableWidgetItem, QWidget, QVBoxLayout, QTableWidget, QLabel, QPushButton

from calculator_tabs.abstract_calculator_tab import AbstractCalculatorTab


class NormalityTab(AbstractCalculatorTab): # TODO: Implement Kolmogorov-Smirnov test and add selector to choose the test
    def __init__(self, data_manager, parent=None):
        super().__init__(data_manager, parent)

        self.layout = QVBoxLayout(self)

        # Label to display instructions
        self.info_label = QLabel("Shapiro-Wilk Test Results")
        self.layout.addWidget(self.info_label)

        # Table to display results
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Series", "W-statistic", "p-Value"])
        self.layout.addWidget(self.results_table)

    def update_results(self):
        data = self.data_manager.get_data()

        # Clear the table
        self.results_table.setRowCount(0)

        # Perform Shapiro-Wilk test for each series (excluding the first column)
        for col in data.columns[1:]:
            series = data[col].dropna()  # Drop NaN values
            w_stat, p_value = shapiro(series)

            # Add results to the table
            row_idx = self.results_table.rowCount()
            self.results_table.insertRow(row_idx)
            self.results_table.setItem(row_idx, 0, QTableWidgetItem(col))
            self.results_table.setItem(row_idx, 1, QTableWidgetItem(f"{w_stat:.4f}"))
            self.results_table.setItem(row_idx, 2, QTableWidgetItem(f"{p_value:.4f}"))
