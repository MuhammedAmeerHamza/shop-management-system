import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Shop Management System")
window.resize(900, 600)

label = QLabel("Welcome to Shop Management System")
label.setStyleSheet("font-size: 24px; padding: 30px;")
window.setCentralWidget(label)

window.show()

sys.exit(app.exec())