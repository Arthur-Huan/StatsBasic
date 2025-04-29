from scipy.stats import pearsonr
from PySide6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

from calculator_tabs.abstract_calculator_tab import AbstractCalculatorTab


class CorrelationCoefficientTab(AbstractCalculatorTab):
    def __init__(self, data_manager, parent=None):
        super().__init__(data_manager, parent)

        self.layout = QVBoxLayout(self)

        # Label to display instructions
        self.info_label = QLabel("Pearson Correlation Coefficients")
        self.layout.addWidget(self.info_label)

        # Table to display results
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Series", "r", "p-Value"])
        self.layout.addWidget(self.results_table)

    def update_results(self):
        data = self.data_manager.get_data()
        if data is None or data.empty:
            return "No data loaded."

        # Clear table
        self.results_table.setRowCount(0)

        # Use the first column as the x-axis
        x_series = data.iloc[:, 0].dropna()

        # Calculate Pearson correlation coefficient for each series (excluding the first column)
        for col in data.columns[1:]:
            y_series = data[col].dropna()

            # Align the x and y series to handle missing values
            aligned_x, aligned_y = x_series.align(y_series, join="inner")

            if len(aligned_x) > 1:  # Ensure there are enough data points
                r, p_value = pearsonr(aligned_x, aligned_y)

                # Add results to the table
                row_idx = self.results_table.rowCount()
                self.results_table.insertRow(row_idx)
                self.results_table.setItem(row_idx, 0, QTableWidgetItem(col))
                self.results_table.setItem(row_idx, 1, QTableWidgetItem(f"{r:.4f}"))
                self.results_table.setItem(row_idx, 2, QTableWidgetItem(f"{p_value:.4f}"))
            else:
                # Handle missing data (or invalid data)
                row_idx = self.results_table.rowCount()
                self.results_table.insertRow(row_idx)
                self.results_table.setItem(row_idx, 0, QTableWidgetItem(col))
                self.results_table.setItem(row_idx, 1, QTableWidgetItem("N/A"))
                self.results_table.setItem(row_idx, 2, QTableWidgetItem("N/A"))

        return ""
