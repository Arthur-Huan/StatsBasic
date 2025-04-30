from scipy.stats import shapiro
from PySide6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

from calculator_tabs.abstract_calculator_tab import AbstractCalculatorTab

# TODO: Implement Kolmogorov-Smirnov test and add selector to choose the test
class NormalityTab(AbstractCalculatorTab):
    def __init__(self, data_manager, parent=None):
        super().__init__(data_manager, parent)

        self.layout = QVBoxLayout(self)

        # Header for table
        self.results_table_header = QLabel("Shapiro-Wilk test results")
        self.layout.addWidget(self.results_table_header)

        # Table to display results
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Series", "W-statistic", "p-Value"])
        self.layout.addWidget(self.results_table)

    def update_results(self):
        """Perform Shapiro-Wilk test and display results in the results table.
        :return: feedback/error message (empty string if success) to display in CalculatorWidget
        """
        data = self.data_manager.get_data()
        if data is None or data.empty:
            return "No data loaded."

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

        return ""
