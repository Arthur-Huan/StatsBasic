from PySide6.QtWidgets import QWidget

class AbstractCalculatorTab(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)

        self.data_manager = data_manager

    def update_results(self):
        raise NotImplementedError("Subclasses should implement this method.")
