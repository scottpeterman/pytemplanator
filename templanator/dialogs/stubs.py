# templanator/dialogs/stubs.py
from PyQt6.QtWidgets import QDialog

class TTPWizardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TTP Wizard")
        self.setMinimumSize(400, 300)

class NapalmDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Napalm Tool")
        self.setMinimumSize(400, 300)

class DBToolDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DB Tool")
        self.setMinimumSize(400, 300)

class TTPFireDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TTP Fire")
        self.setMinimumSize(400, 300)

class TFSMFireDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TFSM Fire")
        self.setMinimumSize(400, 300)