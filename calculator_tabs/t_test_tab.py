from scipy.stats import ttest_1samp, ttest_ind
from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem

from calculator_tabs.abstract_calculator_tab import AbstractCalculatorTab


class TTestTab(AbstractCalculatorTab):
    def __init__(self, data_manager, parent=None):
        super().__init__(data_manager, parent)

        self.layout = QVBoxLayout(self)
        
        # Dropdowns for column selection
        self.column_selector_1 = QComboBox()
        self.column_selector_2 = QComboBox()
        self.layout.addWidget(QLabel("Select Column(s):"))
        self.layout.addWidget(self.column_selector_1)
        self.layout.addWidget(self.column_selector_2)

        # Input field for population mean (single-sample t-test)
        self.population_mean_input = QLineEdit()
        self.population_mean_input.setPlaceholderText("Population Mean (for single-sample t-test)")
        self.layout.addWidget(self.population_mean_input)

        # Header for table
        self.results_table_header = QLabel("Student's t-test results")
        self.layout.addWidget(self.results_table_header)

        # Table to display results
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Statistic", "Value"])
        self.layout.addWidget(self.results_table)

        # Populate column selectors when data changes
        self.data_manager.data_changed.connect(self.populate_columns)

    def populate_columns(self):
        """Populate column selectors with column names from the data.
        """
        data = self.data_manager.get_df()
        self.column_selector_1.clear()
        self.column_selector_2.clear()
        if data is None or data.empty:
            return
        self.column_selector_2.addItem("(None)")
        self.column_selector_1.addItems(data.columns)
        self.column_selector_2.addItems(data.columns)

    def update_results(self):
        """Perform the t-test and display in the results table.
        :return: feedback/error message (empty string if success) to display in CalculatorWidget
        """
        data = self.data_manager.get_df()
        if data is None or data.empty:
            return "No data loaded."

        # Clear the table
        self.results_table.setRowCount(0)

        # Get selected columns
        col1 = self.column_selector_1.currentText()
        col2 = self.column_selector_2.currentText()

        try:
            if col2 == "None":  # Single-sample t-test
                population_mean = float(self.population_mean_input.text())
                sample = data[col1].dropna()
                t_stat, p_value = ttest_1samp(sample, population_mean)
            else:  # Two-sample t-test
                sample1 = data[col1].dropna()
                sample2 = data[col2].dropna()
                t_stat, p_value = ttest_ind(sample1, sample2)

            # Display results
            self.results_table.setRowCount(2)
            self.results_table.setItem(0, 0, QTableWidgetItem("t-Statistic"))
            self.results_table.setItem(0, 1, QTableWidgetItem(f"{t_stat:.4f}"))
            self.results_table.setItem(1, 0, QTableWidgetItem("p-Value"))
            self.results_table.setItem(1, 1, QTableWidgetItem(f"{p_value:.4f}"))
        except ValueError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
        return ""
