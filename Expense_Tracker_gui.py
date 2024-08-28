import sys
import csv
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QScrollArea, QSizePolicy, QComboBox, QHeaderView, QFrame,
                             QStackedWidget, QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon



class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.dark_mode = QCheckBox("Dark Mode")
        self.notifications = QCheckBox("Enable Notifications")
        self.auto_save = QCheckBox("Auto-save Expenses")

        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)

        layout.addWidget(QLabel("Settings"))
        layout.addWidget(self.dark_mode)
        layout.addWidget(self.notifications)
        layout.addWidget(self.auto_save)
        layout.addWidget(save_button)

    def save_settings(self):
        # Here you would typically save these settings to a file or database
        QMessageBox.information(self, "Settings Saved", "Your settings have been saved.")


class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        about_text = """
        Expense Tracker

        This application helps you keep track of your daily expenses.
        Features include:
        - Adding new expenses
        - Categorizing expenses
        - Viewing expense history
        - Basic reporting and analytics

        Version: 1.0
        Developed by: Muneeb Nasir/Ever Design
        """

        layout.addWidget(QLabel(about_text))


class SlidingMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(0)
        self.setMaximumWidth(250)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                border-right: 1px solid #dcdcdc;
            }
            QPushButton {
                text-align: left;
                padding: 10px;
                border: none;
                background-color: transparent;
                color: #333;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QLabel {
                padding: 10px;
                color: #333;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        title = QLabel("Expense Tracker")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 20px 10px;")
        layout.addWidget(title)

        self.account_btn = QPushButton("🔶 Account Details")
        self.account_btn.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.account_btn)

        self.settings_btn = QPushButton("Settings")
        layout.addWidget(self.settings_btn)

        self.about_btn = QPushButton("About")
        layout.addWidget(self.about_btn)

        self.add_expense_btn = QPushButton("Add New Expense")
        layout.addWidget(self.add_expense_btn)

        self.delete_expense_btn = QPushButton("Delete Expense")
        layout.addWidget(self.delete_expense_btn)

        layout.addStretch()

        copyright = QLabel("@Copyright 2024")
        copyright.setStyleSheet("color: #888; padding: 10px; font-size: 12px;")
        layout.addWidget(copyright)

        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setStyleSheet("""
            color: red;
            border-top: 1px solid #dcdcdc;
        """)
        layout.addWidget(self.logout_btn)

        self.animation = QPropertyAnimation(self, b"maximumWidth")
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self.animation.setDuration(250)

    def toggle(self):
        if self.width() == 0:
            self.animation.setEndValue(250)
        else:
            self.animation.setEndValue(0)
        self.animation.start()


class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 1000, 600)

        # Set color scheme
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        self.setPalette(palette)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Create and add sliding menu
        self.sliding_menu = SlidingMenu(self)
        main_layout.addWidget(self.sliding_menu)

        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Create and add pages

        self.main_page = self.create_main_page()
        self.settings_page = SettingsPage(self)
        self.about_page = AboutPage(self)


        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.settings_page)
        self.stacked_widget.addWidget(self.about_page)

        # Connect menu buttons
        self.sliding_menu.settings_btn.clicked.connect(self.show_settings_page)
        self.sliding_menu.about_btn.clicked.connect(self.show_about_page)
        self.sliding_menu.add_expense_btn.clicked.connect(self.show_main_page)
        self.sliding_menu.logout_btn.clicked.connect(self.logout)


    def create_main_page(self):
        main_page = QWidget()
        layout = QVBoxLayout(main_page)

        # Add toggle menu button
        toggle_btn = QPushButton("≡")
        toggle_btn.clicked.connect(self.sliding_menu.toggle)
        layout.addWidget(toggle_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        # Create input fields
        input_layout = QHBoxLayout()
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Amount")
        self.category_input = QComboBox()
        self.category_input.addItems(["Food", "Transportation", "Entertainment", "Utilities", "Other"])
        self.category_input.setEditable(True)
        self.category_input.setPlaceholderText("Category")
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Description")

        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(self.category_input)
        input_layout.addWidget(self.description_input)

        # Create add expense button
        add_button = QPushButton("Add Expense")
        add_button.clicked.connect(self.add_expense)
        input_layout.addWidget(add_button)

        layout.addLayout(input_layout)

        # Create table for displaying expenses
        self.expense_table = QTableWidget()
        self.expense_table.setColumnCount(5)
        self.expense_table.setHorizontalHeaderLabels(["Date", "Amount", "Category", "Description", "Action"])
        self.expense_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.expense_table.setAlternatingRowColors(True)
        self.expense_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d3d3d3;
                background-color: white;
                alternate-background-color: #f9f9f9;
                color: black;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 4px;
                border: 1px solid #d3d3d3;
                font-weight: bold;
                color: black;
            }
            QTableWidget::item {
                border: 1px solid #d3d3d3;
            }
            QPushButton {
                background-color: #f0f0f0;
                color: #0000ff;
                border: 1px solid #d3d3d3;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        # Create a scroll area for the table
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.expense_table)

        layout.addWidget(scroll_area)

        # Load existing expenses
        self.load_expenses()

        return main_page

    def show_main_page(self):
        self.stacked_widget.setCurrentWidget(self.main_page)

    def show_settings_page(self):
        self.stacked_widget.setCurrentWidget(self.settings_page)

    def show_about_page(self):
        self.stacked_widget.setCurrentWidget(self.about_page)

    def logout(self):
        self.stacked_widget.setCurrentWidget(self.login_page)
        self.sliding_menu.setFixedWidth(0)

    def add_expense(self):
        amount = self.amount_input.text()
        category = self.category_input.currentText()
        description = self.description_input.text()
        date = datetime.now().strftime("%Y-%m-%d")

        if amount and category:
            row_position = self.expense_table.rowCount()
            self.expense_table.insertRow(row_position)
            self.expense_table.setItem(row_position, 0, QTableWidgetItem(date))
            self.expense_table.setItem(row_position, 1, QTableWidgetItem(amount))
            self.expense_table.setItem(row_position, 2, QTableWidgetItem(category))
            self.expense_table.setItem(row_position, 3, QTableWidgetItem(description))

            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, row=row_position: self.delete_expense(row))
            self.expense_table.setCellWidget(row_position, 4, delete_button)

            self.save_expense(date, amount, category, description)

            # Clear input fields after adding expense
            self.amount_input.clear()
            self.category_input.setCurrentIndex(0)
            self.description_input.clear()

    def save_expense(self, date, amount, category, description):
        with open('expenses.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, amount, category, description])

    def load_expenses(self):
        try:
            with open('expenses.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    row_position = self.expense_table.rowCount()
                    self.expense_table.insertRow(row_position)
                    for column, item in enumerate(row):
                        self.expense_table.setItem(row_position, column, QTableWidgetItem(str(item)))

                    delete_button = QPushButton("Delete")
                    delete_button.clicked.connect(lambda _, row=row_position: self.delete_expense(row))
                    self.expense_table.setCellWidget(row_position, 4, delete_button)
        except FileNotFoundError:
            print("No existing expense file found. A new one will be created when you add an expense.")

    def delete_expense(self, row):
        self.expense_table.removeRow(row)
        self.update_csv_file()

    def update_csv_file(self):
        with open('expenses.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for row in range(self.expense_table.rowCount()):
                row_data = []
                for column in range(4):  # Only save the first 4 columns (exclude the delete button)
                    item = self.expense_table.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                writer.writerow(row_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExpenseTracker()
    window.show()
    sys.exit(app.exec())