
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)


class ShopManagement(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shop Management System")
        self.resize(1000, 650)

        # Main widget
        central = QWidget()
        self.setCentralWidget(central)

        # Main layout
        main_layout = QHBoxLayout(central)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
            }
            QPushButton {
                color: white;
                background-color: transparent;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)

        title = QLabel("SHOP MANAGER")
        title.setStyleSheet(
            "color: white; font-size: 20px; font-weight: bold; padding: 20px;"
        )
        sidebar_layout.addWidget(title)

        sidebar_layout.addWidget(QPushButton("📊 Dashboard"))
        sidebar_layout.addWidget(QPushButton("📦 Products"))
        sidebar_layout.addWidget(QPushButton("🛒 Sales"))
        sidebar_layout.addWidget(QPushButton("👥 Customers"))
        sidebar_layout.addWidget(QPushButton("📈 Reports"))
        sidebar_layout.addWidget(QPushButton("⚙️ Settings"))

        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar)

        # Dashboard area
        dashboard = QWidget()
        dashboard_layout = QVBoxLayout(dashboard)

        heading = QLabel("Dashboard")
        heading.setStyleSheet(
            "font-size: 30px; font-weight: bold; padding: 15px;"
        )
        dashboard_layout.addWidget(heading)

        welcome = QLabel("Welcome to your Shop Management System!")
        welcome.setStyleSheet("font-size: 18px; padding: 10px;")
        dashboard_layout.addWidget(welcome)

        # Statistics
        stats_layout = QHBoxLayout()

        stats = [
            ("Today's Sales", "Rs. 0"),
            ("Today's Profit", "Rs. 0"),
            ("Total Products", "0"),
            ("Low Stock", "0"),
        ]

        for name, value in stats:
            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #ecf0f1;
                    border-radius: 10px;
                    padding: 15px;
                }
            """)

            card_layout = QVBoxLayout(card)

            name_label = QLabel(name)
            name_label.setStyleSheet("font-size: 15px;")

            value_label = QLabel(value)
            value_label.setStyleSheet(
                "font-size: 24px; font-weight: bold;"
            )

            card_layout.addWidget(name_label)
            card_layout.addWidget(value_label)

            stats_layout.addWidget(card)

        dashboard_layout.addLayout(stats_layout)
        dashboard_layout.addStretch()

        main_layout.addWidget(dashboard)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ShopManagement()
    window.show()

    sys.exit(app.exec())

