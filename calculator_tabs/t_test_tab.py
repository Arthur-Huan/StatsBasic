from PySide6.QtWidgets import QWidget


class TTestTab(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)

        self.data_manager = data_manager

        pass
