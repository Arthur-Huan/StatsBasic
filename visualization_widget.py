from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy, \
    QSplitter


class VisualizationWidget(QSplitter):
    def __init__(self, data_manager, parent=None):
        super().__init__(Qt.Vertical, parent)

        self.data_manager = data_manager

        # Table widget
        self.table_widget = TableWidget(self.data_manager, self)
        self.addWidget(self.table_widget)

        # Graph widget
        self.graph_widget = GraphWidget(self.data_manager, self)
        self.addWidget(self.graph_widget)


class TableWidget(QTableWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.data_manager.data_changed.connect(self.update_table)

    def update_table(self):
        """
        Update the table with the latest data from the data manager.
        """
        data = self.data_manager.get_data()
        if data is None or data.empty:
            self.setRowCount(0)
            self.setColumnCount(0)
            return

        # Set the number of rows and columns
        self.setRowCount(len(data))
        self.setColumnCount(len(data.columns))

        # Set the column headers
        self.setHorizontalHeaderLabels(data.columns)

        # Populate the table with data
        for row_idx, row in data.iterrows():
            for col_idx, value in enumerate(row):
                self.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))


class GraphWidget(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager

        self.layout = QVBoxLayout(self)

        # Label to display feedback
        self.feedback_label = QLabel("Load data to plot a scatter plot.")
        self.layout.addWidget(self.feedback_label)

        # Plot figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Button to plot the graph
        self.plot_button = QPushButton("Plot Scatter Plot", self)
        self.plot_button.clicked.connect(self.plot_scatter)
        self.layout.addWidget(self.plot_button)

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
            x_col = data.columns[0]
            ax = self.figure.add_subplot(111)
            if len(data.columns) > 2:
                ax.set_ylabel("Values")
            for y_col in data.columns[1:]:
                sns.scatterplot(data=data, x=x_col, y=y_col, ax=ax, label=y_col)
            # Draw the plot on the canvas
            self.canvas.draw()
        except Exception as e:
            self.feedback_label.setText(f"Error plotting scatter plot: {e}")
