from PySide6.QtCore import QObject, Signal

class DataManager(QObject):
    data_changed = Signal()

    def __init__(self, parent=None):
        super(DataManager, self).__init__(parent)
        self.data = None

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
        self.data_changed.emit()
