
import sys
import sqlite3

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QLineEdit,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
)


class ShopManagement(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shop Management System")
        self.resize(1000, 650)

        self.create_database()

        central = QWidget()
        self.setCentralWidget(central)

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

        dashboard_button = QPushButton("📊 Dashboard")
        products_button = QPushButton("📦 Products")

        sidebar_layout.addWidget(dashboard_button)
        sidebar_layout.addWidget(products_button)

        sidebar_layout.addWidget(QPushButton("🛒 Sales"))
        sidebar_layout.addWidget(QPushButton("👥 Customers"))
        sidebar_layout.addWidget(QPushButton("📈 Reports"))
        sidebar_layout.addWidget(QPushButton("⚙️ Settings"))

        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar)

        # Main area
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)

        main_layout.addWidget(self.content)

        dashboard_button.clicked.connect(self.show_dashboard)
        products_button.clicked.connect(self.show_products)

        self.show_dashboard()

    def create_database(self):
        connection = sqlite3.connect("shop.db")
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                purchase_price REAL NOT NULL,
                sale_price REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    def clear_content(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

    def show_dashboard(self):
        self.clear_content()

        heading = QLabel("Dashboard")
        heading.setStyleSheet(
            "font-size: 30px; font-weight: bold; padding: 15px;"
        )

        welcome = QLabel("Welcome to your Shop Management System!")
        welcome.setStyleSheet("font-size: 18px; padding: 10px;")

        self.content_layout.addWidget(heading)
        self.content_layout.addWidget(welcome)

        stats_layout = QHBoxLayout()

        stats = [
            ("Today's Sales", "Rs. 0"),
            ("Today's Profit", "Rs. 0"),
            ("Total Products", self.get_product_count()),
            ("Low Stock", self.get_low_stock_count()),
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

            value_label = QLabel(str(value))
            value_label.setStyleSheet(
                "font-size: 24px; font-weight: bold;"
            )

            card_layout.addWidget(name_label)
            card_layout.addWidget(value_label)

            stats_layout.addWidget(card)

        self.content_layout.addLayout(stats_layout)
        self.content_layout.addStretch()

    def show_products(self):
        self.clear_content()

        heading = QLabel("Products")
        heading.setStyleSheet(
            "font-size: 30px; font-weight: bold; padding: 10px;"
        )

        self.content_layout.addWidget(heading)

        # Product input fields
        form = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Product name")

        self.purchase_input = QLineEdit()
        self.purchase_input.setPlaceholderText("Purchase price")

        self.sale_input = QLineEdit()
        self.sale_input.setPlaceholderText("Sale price")

        self.stock_input = QLineEdit()
        self.stock_input.setPlaceholderText("Stock quantity")

        add_button = QPushButton("Add Product")
        add_button.clicked.connect(self.add_product)

        form.addWidget(self.name_input)
        form.addWidget(self.purchase_input)
        form.addWidget(self.sale_input)
        form.addWidget(self.stock_input)
        form.addWidget(add_button)

        self.content_layout.addLayout(form)

        # Products table
        self.table = QTableWidget()

        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Product Name",
            "Purchase Price",
            "Sale Price",
            "Stock"
        ])

        self.content_layout.addWidget(self.table)

        self.load_products()

    def add_product(self):
        name = self.name_input.text().strip()

        try:
            purchase_price = float(self.purchase_input.text())
            sale_price = float(self.sale_input.text())
            stock = int(self.stock_input.text())
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Input",
                "Please enter valid prices and stock quantity."
            )
            return

        if not name:
            QMessageBox.warning(
                self,
                "Missing Product",
                "Please enter a product name."
            )
            return

        connection = sqlite3.connect("shop.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO products
            (name, purchase_price, sale_price, stock)
            VALUES (?, ?, ?, ?)
        """, (name, purchase_price, sale_price, stock))

        connection.commit()
        connection.close()

        self.name_input.clear()
        self.purchase_input.clear()
        self.sale_input.clear()
        self.stock_input.clear()

        self.load_products()

        QMessageBox.information(
            self,
            "Success",
            "Product added successfully!"
        )

    def load_products(self):
        connection = sqlite3.connect("shop.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, purchase_price, sale_price, stock
            FROM products
            ORDER BY id DESC
        """)

        products = cursor.fetchall()

        connection.close()

        self.table.setRowCount(len(products))

        for row, product in enumerate(products):
            for column, value in enumerate(product):
                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value))
                )

    def get_product_count(self):
        connection = sqlite3.connect("shop.db")
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM products")
        count = cursor.fetchone()[0]

        connection.close()

        return count

    def get_low_stock_count(self):
        connection = sqlite3.connect("shop.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM products
            WHERE stock <= 5
        """)

        count = cursor.fetchone()[0]

        connection.close()

        return count


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ShopManagement()
    window.show()

    sys.exit(app.exec())
