from scipy.stats import chi2_contingency
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem

from calculator_tabs.abstract_calculator_tab import AbstractCalculatorTab


class ChiSquaredTab(AbstractCalculatorTab):
    def __init__(self, data_manager, parent=None):
        super().__init__(data_manager, parent)

        self.layout = QVBoxLayout(self)

        # Header for table
        self.results_table_header = QLabel("Chi-Squared Test Results")
        self.layout.addWidget(self.results_table_header)

        # Table to display results
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Statistic", "Value"])
        self.layout.addWidget(self.results_table)

    def update_results(self):
        """Calculate the chi-squared statistic for the contingency table.
        :return: feedback/error message (empty string if success) to display in CalculatorWidget
        """
        # Retrieve data, should be a contingency table
        data = self.data_manager.get_df()
        if data is None or data.empty:
            return "No data loaded."

        try:
            # Perform chi-squared test
            chi2, p, dof, expected = chi2_contingency(data)

            # Display results in the table widget
            self.results_table.setRowCount(3)
            self.results_table.setItem(0, 0, QTableWidgetItem("Chi-Squared"))
            self.results_table.setItem(0, 1, QTableWidgetItem(f"{chi2:.4f}"))
            self.results_table.setItem(1, 0, QTableWidgetItem("p-value"))
            self.results_table.setItem(1, 1, QTableWidgetItem(f"{p:.4f}"))
            self.results_table.setItem(2, 0, QTableWidgetItem("Degrees of Freedom"))
            self.results_table.setItem(2, 1, QTableWidgetItem(f"{dof}"))

        except Exception as e:
            return f"Error processing contingency table: {e}"

        return ""
