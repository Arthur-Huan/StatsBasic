from scipy.stats import shapiro
from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QTableWidget, \
    QTableWidgetItem, QPushButton


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
        self.anova_tab = ANNOVATab(self.data_manager, self)
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
        self.dropdown.currentIndexChanged.connect(self.tabs_widget.setCurrentIndex)
        layout.addWidget(self.dropdown)


class NormalityTab(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)

        self.data_manager = data_manager

        self.layout = QVBoxLayout(self)

        # Label to display instructions
        self.info_label = QLabel("Shapiro-Wilk Test Results")
        self.layout.addWidget(self.info_label)

        # Table to display results
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Series", "W-statistic", "p-Value"])
        self.layout.addWidget(self.results_table)

        # Button to update the results table
        self.update_button = QPushButton("Update")
        self.update_button.clicked.connect(self.update_results)
        self.layout.addWidget(self.update_button)

    def update_results(self):
        data = self.data_manager.get_data()
        if data is None or data.empty:
            self.info_label.setText("No data available.")
            return

        # Clear the table
        self.results_table.setRowCount(0)

        # Perform Shapiro-Wilk test for each series (excluding the first column)
        x_col = data.columns[0]
        for col in data.columns[1:]:
            series = data[col].dropna()  # Drop NaN values
            w_stat, p_value = shapiro(series)

            # Add results to the table
            row_idx = self.results_table.rowCount()
            self.results_table.insertRow(row_idx)
            self.results_table.setItem(row_idx, 0, QTableWidgetItem(col))
            self.results_table.setItem(row_idx, 1, QTableWidgetItem(f"{w_stat:.4f}"))
            self.results_table.setItem(row_idx, 2, QTableWidgetItem(f"{p_value:.4f}"))


class TTestTab(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)

        self.data_manager = data_manager

        pass


class ChiSquaredTab(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)

        self.data_manager = data_manager

        pass


class CorrelationCoefficientTab(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)

        self.data_manager = data_manager

        pass


class ANNOVATab(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)

        self.data_manager = data_manager

        pass
