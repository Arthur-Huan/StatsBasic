from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem


class VisualizationWidget(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)

        self.data_manager = data_manager
        self.data_manager.data_changed.connect(self.update_table)

        self.layout = QVBoxLayout(self)

        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

        # Label to display feedback
        self.feedback_label = QLabel("Load data to plot a scatter plot.")
        self.layout.addWidget(self.feedback_label)

        # Button to plot the graph
        self.plot_button = QPushButton("Plot Scatter Plot", self)

        # Connect the button to the plot method
        self.plot_button.clicked.connect(self.plot_scatter)

        # Plot figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.layout.addWidget(self.canvas)

    def update_table(self):
        """
        Update the table with the latest data from the data manager.
        """
        data = self.data_manager.get_data()
        if data is None or data.empty:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            return

        # Set the number of rows and columns
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(data.columns))

        # Set the column headers
        self.table_widget.setHorizontalHeaderLabels(data.columns)

        # Populate the table with data
        for row_idx, row in data.iterrows():
            for col_idx, value in enumerate(row):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
    
    def plot_scatter(self):
        """
        Plot a scatter plot
        """
        data = self.data_manager.get_data()
        if data is None:
            self.feedback_label.setText("No data loaded.")
            return

        # Check if there are at least two columns for plotting
        if len(data.columns) < 2:
            self.feedback_label.setText("CSV must have at least two columns for plotting.")
            return

        try:
            # Clear the figure
            self.figure.clear()

            # Use the first two columns for the scatter plot
            x_col, y_col = data.columns[:2]
            ax = self.figure.add_subplot(111)
            sns.scatterplot(data=data, x=x_col, y=y_col, ax=ax)
            ax.set_title("Scatter Plot")

            # Refresh the canvas
            self.canvas.draw()
        except Exception as e:
            self.feedback_label.setText(f"Error plotting scatter plot: {e}")
