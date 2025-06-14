import sys
from PySide6.QtWidgets import QApplication
from src.Interface_grafica import PatrimonyApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PatrimonyApp()
    window.show()
    sys.exit(app.exec())