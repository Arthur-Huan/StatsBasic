from PySide6.QtWidgets import QWidget

from calculator_tabs.abstract_calculator_tab import AbstractCalculatorTab


class ANOVATab(AbstractCalculatorTab):
    def __init__(self, data_manager, parent=None):
        super().__init__(data_manager, parent)
        
