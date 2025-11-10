import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout,
    QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect,
    QMainWindow, QStackedWidget, QFormLayout, QComboBox,
    QRadioButton, QFileDialog, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QButtonGroup, QTextEdit, QSpinBox,
    QDoubleSpinBox, QTabWidget
)
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime


# --- (Code from previous step) ---
# ---     LOGIN WINDOW     ---
# --- (This code is identical to the previous step) ---

class FrostedCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(218, 196, 168, 220))
        self.setPalette(palette)
        self.setStyleSheet("border-radius: 15px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_window = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('JLPOS - Employee Login')
        self.setFixedSize(450, 550)
        self.setStyleSheet("background-color: #F5F5DC;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignCenter)

        self.logo_label = QLabel("JLPOS")
        self.logo_label.setFont(QFont('Arial', 40, QFont.Bold))
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setStyleSheet("color: #4A4A4A; margin-bottom: 20px;")

        self.card = FrostedCard(self)
        self.card.setFixedSize(350, 350)
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setAlignment(Qt.AlignCenter)

        self.error_label = QLabel("")
        self.error_label.setFont(QFont('Arial', 9))
        self.error_label.setStyleSheet("color: red; padding-bottom: 10px;")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.hide()
        card_layout.addWidget(self.error_label)

        self.emp_num_label = QLabel("Employee Number")
        self.emp_num_label.setHidden(True)
        self.emp_num_input = QLineEdit()
        self.emp_num_input.setPlaceholderText("Employee Number")
        self.emp_num_label.setBuddy(self.emp_num_input)

        self.password_label = QLabel("Password")
        self.password_label.setHidden(True)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_label.setBuddy(self.password_input)

        controls_layout = QHBoxLayout()
        self.remember_check = QCheckBox("Remember Me")
        self.forgot_button = QPushButton("Forgot Password?")
        self.forgot_button.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; color: #555; text-decoration: underline; }
            QPushButton:hover { color: #000; }
        """)

        controls_layout.addWidget(self.remember_check)
        controls_layout.addStretch()
        controls_layout.addWidget(self.forgot_button)

        self.login_button = QPushButton("Login")
        self.login_button.setObjectName("login_button")

        card_layout.addWidget(self.emp_num_label)
        card_layout.addWidget(self.emp_num_input)
        card_layout.addWidget(self.password_label)
        card_layout.addWidget(self.password_input)
        card_layout.addSpacing(15)
        card_layout.addLayout(controls_layout)
        card_layout.addSpacing(20)
        card_layout.addWidget(self.login_button)

        main_layout.addWidget(self.logo_label)
        main_layout.addWidget(self.card)

        self.set_styles()
        self.login_button.clicked.connect(self.handle_login)

    def set_styles(self):
        self.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF; border: 1px solid #CCC;
                padding: 12px 15px; border-radius: 8px;
                font-size: 14px; min-height: 25px;
            }
            QLineEdit:focus { border: 1px solid #32CD32; }
            QCheckBox { font-size: 13px; color: #333; }
            QPushButton#login_button {
                background-color: #32CD32; color: white;
                font-size: 16px; font-weight: bold;
                padding: 12px; border-radius: 8px; border: none;
            }
            QPushButton#login_button:hover { background-color: #28A745; }
        """)

    def handle_login(self):
        emp_num = self.emp_num_input.text()
        password = self.password_input.text()

        if not emp_num or not password:
            self.error_label.setText("Employee Number and Password are required.")
            self.error_label.show()
            return

        if not emp_num.isdigit():
            self.error_label.setText("Employee Number must be numeric.")
            self.error_label.show()
            return

        if emp_num == "123456" and password == "admin":
            print("Login Successful!")
            # Pass the logged-in user's info to the main window
            self.main_window = MainWindow(emp_id="123456", emp_name="Basilio, Ralph")
            self.main_window.show()
            self.close()
        else:
            self.error_label.setText("Invalid Employee Number or Password.")
            self.error_label.show()


# --- END OF LOGIN WINDOW CODE ---


# --- START OF UPDATED MAINWINDOW CODE ---

class MainWindow(QMainWindow):
    # --- NEW: Accept user info on login ---
    def __init__(self, emp_id, emp_name):
        super().__init__()
        # Store user info
        self.current_user_id = emp_id
        self.current_user_name = emp_name

        self.setWindowTitle('JLPOS Dashboard')
        self.setGeometry(100, 100, 1200, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.create_sidebar()
        self.create_main_content()

        self.main_layout.addWidget(self.sidebar_widget, 1)
        self.main_layout.addWidget(self.content_widget, 5)

    def create_sidebar(self):
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setStyleSheet("background-color: #F0E6D2; border-right: 1px solid #D3D3D3;")

        sidebar_layout = QVBoxLayout(self.sidebar_widget)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setAlignment(Qt.AlignTop)

        self.sidebar_logo = QLabel("JLPOS")
        self.sidebar_logo.setFont(QFont('Arial', 24, QFont.Bold))
        self.sidebar_logo.setAlignment(Qt.AlignCenter)
        self.sidebar_logo.setStyleSheet("color: #4A4A4A; margin-bottom: 30px;")
        sidebar_layout.addWidget(self.sidebar_logo)

        # Navigation Buttons
        self.btn_staff = QPushButton(" Staff")
        self.btn_inventory = QPushButton(" Inventory")
        # --- NEW: Renamed 'Reports' to 'Help & About' ---
        self.btn_help = QPushButton(" Help & About")
        self.btn_settings = QPushButton(" Settings")

        # --- UPDATED: Button list ---
        nav_buttons = [self.btn_staff, self.btn_inventory, self.btn_help, self.btn_settings]

        self.nav_button_group = QButtonGroup(self)
        self.nav_button_group.setExclusive(True)

        for btn in nav_buttons:
            btn.setFont(QFont('Arial', 12))
            btn.setIconSize(QSize(24, 24))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent; border: none;
                    color: #333; padding: 10px; text-align: left;
                    border-radius: 5px;
                }
                QPushButton:hover { background-color: #E0D6C2; }
                QPushButton:checked {
                    background-color: #D3C6B2; font-weight: bold;
                }
            """)
            btn.setCheckable(True)
            sidebar_layout.addWidget(btn)
            self.nav_button_group.addButton(btn)

        self.btn_staff.setChecked(True)

        sidebar_layout.addStretch()

        version_label = QLabel("V1.0")
        version_label.setFont(QFont('Arial', 9))
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: #888;")
        sidebar_layout.addWidget(version_label)

    def create_main_content(self):
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: #FDFDFD;")

        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # --- Top Header (Logo/Date) ---
        top_header_widget = QWidget()
        top_header_widget.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E0E0E0;")
        top_header_layout = QHBoxLayout(top_header_widget)

        header_logo = QLabel("JLPOS")
        header_logo.setFont(QFont('Arial', 16, QFont.Bold))
        header_logo.setStyleSheet("color: #333; padding: 10px;")

        self.datetime_label = QLabel()
        self.datetime_label.setFont(QFont('Arial', 12))
        self.datetime_label.setStyleSheet("color: #555; padding: 10px;")

        timer = QTimer(self)
        timer.timeout.connect(self.update_datetime)
        timer.start(1000)
        self.update_datetime()

        top_header_layout.addWidget(header_logo)
        top_header_layout.addStretch()
        top_header_layout.addWidget(self.datetime_label)

        # --- Stacked Widget (for switching pages) ---
        self.stacked_widget = QStackedWidget()

        # --- Create ALL pages ---
        self.staff_page_widget = self.create_staff_page()  # Page 0
        self.staff_form_widget = self.create_staff_form()  # Page 1
        self.inventory_page_widget = self.create_inventory_page()  # Page 2
        self.inventory_form_widget = self.create_inventory_form()  # Page 3

        # --- NEW: Help & About Page (replaces Reports) ---
        self.help_about_page_widget = self.create_help_about_page()  # Page 4

        self.settings_page_widget = self.create_placeholder_page("Settings")  # Page 5

        # --- Add pages to stack in order ---
        self.stacked_widget.addWidget(self.staff_page_widget)  # Index 0
        self.stacked_widget.addWidget(self.staff_form_widget)  # Index 1
        self.stacked_widget.addWidget(self.inventory_page_widget)  # Index 2
        self.stacked_widget.addWidget(self.inventory_form_widget)  # Index 3
        self.stacked_widget.addWidget(self.help_about_page_widget)  # Index 4
        self.stacked_widget.addWidget(self.settings_page_widget)  # Index 5

        # --- Connect ALL sidebar buttons ---
        self.btn_staff.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_inventory.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_help.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(4))
        self.btn_settings.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(5))

        content_layout.addWidget(top_header_widget)
        content_layout.addWidget(self.stacked_widget)

    def update_datetime(self):
        now = QDateTime.currentDateTime()
        self.datetime_label.setText(now.toString(Qt.DefaultLocaleLongDate))

    def create_placeholder_page(self, title):
        page_widget = QWidget()
        layout = QVBoxLayout(page_widget)
        layout.setContentsMargins(20, 10, 20, 20)
        layout.setAlignment(Qt.AlignCenter)

        red_header = QWidget()
        red_header.setStyleSheet("background-color: #C0392B; border-radius: 5px;")
        red_header_layout = QHBoxLayout(red_header)
        page_title = QLabel(title)
        page_title.setFont(QFont('Arial', 16, QFont.Bold))
        page_title.setStyleSheet("color: white; padding: 10px;")
        red_header_layout.addWidget(page_title)

        coming_soon = QLabel(f"{title} Page - Coming Soon!")
        coming_soon.setFont(QFont('Arial', 20))
        coming_soon.setAlignment(Qt.AlignCenter)

        layout.addWidget(red_header, 0, Qt.AlignTop)
        layout.addWidget(coming_soon, 1)

        return page_widget

    # --- Staff Page (Identical to before) ---
    def create_staff_page(self):
        page_widget = QWidget()
        layout = QVBoxLayout(page_widget)
        layout.setContentsMargins(20, 10, 20, 20)

        red_header = QWidget()
        red_header.setStyleSheet("background-color: #C0392B; border-radius: 5px;")
        red_header_layout = QHBoxLayout(red_header)
        page_title = QLabel("Employees")
        page_title.setFont(QFont('Arial', 16, QFont.Bold))
        page_title.setStyleSheet("color: white; padding: 10px;")
        red_header_layout.addWidget(page_title)
        red_header_layout.addStretch()
        layout.addWidget(red_header)
        layout.addSpacing(15)

        controls_layout = QHBoxLayout()
        view_combo = QComboBox()
        view_combo.addItems(["View All", "Admins", "Staff", "Kitchen Staff"])
        view_combo.setFixedWidth(150)
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search Staff")

        self.add_employee_btn = QPushButton("+ Add Employee")
        self.add_employee_btn.setObjectName("add_button")
        self.add_employee_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        controls_layout.addWidget(view_combo)
        controls_layout.addWidget(search_bar)
        controls_layout.addStretch()
        controls_layout.addWidget(self.add_employee_btn)

        layout.addLayout(controls_layout)
        layout.addSpacing(15)

        self.staff_table = QTableWidget()
        self.staff_table.setColumnCount(6)
        self.staff_table.setHorizontalHeaderLabels([
            "Last Name", "First Name", "Employee Number",
            "Phone Number", "Role", "Date Log"
        ])

        data = [
            ("Basilio", "Ralph", "123456", "09099505232", "Admin", "Jan 1, 2025 | 9:00 AM"),
            ("Baldovino", "Gabriel", "123457", "09918654321", "Staff", "Jan 1, 2025 | 9:00 AM"),
            ("Francisco", "Yuan", "123458", "09683576284", "Kitchen Staff", "Jan 1, 2025 | 9:00 AM")
        ]

        self.staff_table.setRowCount(len(data))
        for row, item in enumerate(data):
            for col, val in enumerate(item):
                self.staff_table.setItem(row, col, QTableWidgetItem(val))

        self.staff_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.staff_table.setAlternatingRowColors(True)
        self.staff_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.staff_table.verticalHeader().setVisible(False)

        layout.addWidget(self.staff_table)

        page_widget.setStyleSheet(self.get_page_style())
        return page_widget

    # --- Staff Form (Identical to before) ---
    def create_staff_form(self):
        form_widget = QWidget()
        layout = QVBoxLayout(form_widget)
        layout.setContentsMargins(20, 10, 20, 20)

        red_header = QWidget()
        red_header.setStyleSheet("background-color: #C0392B; border-radius: 5px;")
        red_header_layout = QHBoxLayout(red_header)
        page_title = QLabel("Add New Employee")
        page_title.setFont(QFont('Arial', 16, QFont.Bold))
        page_title.setStyleSheet("color: white; padding: 10px;")
        red_header_layout.addWidget(page_title)
        layout.addWidget(red_header)
        layout.addSpacing(15)

        self.staff_form_error_label = QLabel("")
        self.staff_form_error_label.setFont(QFont('Arial', 10))
        self.staff_form_error_label.setStyleSheet(
            "color: red; padding: 10px; background-color: #FADBD8; border-radius: 5px;")
        self.staff_form_error_label.setAlignment(Qt.AlignCenter)
        self.staff_form_error_label.setWordWrap(True)
        self.staff_form_error_label.hide()
        layout.addWidget(self.staff_form_error_label)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.sf_first_name = QLineEdit()
        self.sf_last_name = QLineEdit()
        self.sf_emp_num = QLineEdit()
        self.sf_phone = QLineEdit()
        self.sf_role = QComboBox()
        self.sf_role.addItems(["Admin", "Staff", "Kitchen Staff"])
        self.sf_email = QLineEdit()
        self.sf_password = QLineEdit()
        self.sf_password.setEchoMode(QLineEdit.Password)
        self.sf_confirm_password = QLineEdit()
        self.sf_confirm_password.setEchoMode(QLineEdit.Password)

        self.status_groupbox = QGroupBox("Account Status")
        status_layout = QHBoxLayout()
        self.sf_status_active = QRadioButton("Active")
        self.sf_status_disabled = QRadioButton("Disabled")
        self.sf_status_active.setChecked(True)
        status_layout.addWidget(self.sf_status_active)
        status_layout.addWidget(self.sf_status_disabled)
        self.status_groupbox.setLayout(status_layout)

        self.sf_photo_btn = QPushButton("Upload Profile Photo")
        self.sf_photo_label = QLabel("No file selected.")
        self.sf_photo_btn.clicked.connect(self.select_photo)
        photo_layout = QHBoxLayout()
        photo_layout.addWidget(self.sf_photo_btn)
        photo_layout.addWidget(self.sf_photo_label)

        form_layout.addRow(QLabel("First Name:"), self.sf_first_name)
        form_layout.addRow(QLabel("Last Name:"), self.sf_last_name)
        form_layout.addRow(QLabel("Employee Number:"), self.sf_emp_num)
        form_layout.addRow(QLabel("Phone Number:"), self.sf_phone)
        form_layout.addRow(QLabel("Role:"), self.sf_role)
        form_layout.addRow(QLabel("Email Address:"), self.sf_email)
        form_layout.addRow(QLabel("Set Password:"), self.sf_password)
        form_layout.addRow(QLabel("Confirm Password:"), self.sf_confirm_password)
        form_layout.addRow(self.status_groupbox)
        form_layout.addRow(QLabel("Profile Photo:"), photo_layout)

        layout.addLayout(form_layout)
        layout.addStretch()

        button_layout = QHBoxLayout()
        self.sf_save_btn = QPushButton("Save Employee")
        self.sf_save_btn.setObjectName("save_button")
        self.sf_cancel_btn = QPushButton("Cancel")
        self.sf_cancel_btn.setObjectName("cancel_button")

        button_layout.addStretch()
        button_layout.addWidget(self.sf_cancel_btn)
        button_layout.addWidget(self.sf_save_btn)

        layout.addLayout(button_layout)

        self.sf_save_btn.clicked.connect(self.validate_staff_form)
        self.sf_cancel_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        form_widget.setStyleSheet(self.get_form_style())
        return form_widget

    def select_photo(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Image files (*.jpg *.png)")
        if fname:
            self.sf_photo_label.setText(fname.split('/')[-1])

    def validate_staff_form(self):
        errors = []
        first_name = self.sf_first_name.text()
        last_name = self.sf_last_name.text()
        emp_num = self.sf_emp_num.text()
        email = self.sf_email.text()
        password = self.sf_password.text()
        confirm_pass = self.sf_confirm_password.text()

        if not first_name: errors.append("First Name is required.")
        if not last_name: errors.append("Last Name is required.")
        if not emp_num: errors.append("Employee Number is required.")
        if not email: errors.append("Email Address is required.")
        if emp_num and not emp_num.isdigit(): errors.append("Employee Number must be numeric.")
        if email and "@" not in email: errors.append("Please enter a valid Email Address.")
        if password and len(password) < 8: errors.append("Password must be at least 8 characters.")
        if password != confirm_pass: errors.append("Passwords do not match.")

        if errors:
            self.staff_form_error_label.setText("\n".join(errors))
            self.staff_form_error_label.show()
            return

        self.staff_form_error_label.hide()
        print("--- Staff Form Validation Successful ---")
        self.stacked_widget.setCurrentIndex(0)

    # --- Inventory Page (Identical to before) ---
    def create_inventory_page(self):
        page_widget = QWidget()
        layout = QVBoxLayout(page_widget)
        layout.setContentsMargins(20, 10, 20, 20)

        red_header = QWidget()
        red_header.setStyleSheet("background-color: #C0392B; border-radius: 5px;")
        red_header_layout = QHBoxLayout(red_header)
        page_title = QLabel("Inventory")
        page_title.setFont(QFont('Arial', 16, QFont.Bold))
        page_title.setStyleSheet("color: white; padding: 10px;")
        red_header_layout.addWidget(page_title)
        red_header_layout.addStretch()
        layout.addWidget(red_header)
        layout.addSpacing(15)

        controls_layout = QHBoxLayout()
        view_combo = QComboBox()
        view_combo.addItems(["View All", "cat1", "cat2"])
        view_combo.setFixedWidth(150)
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search Inventory")

        self.add_item_btn = QPushButton("+ Add")
        self.add_item_btn.setObjectName("add_button")
        self.add_item_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

        controls_layout.addWidget(view_combo)
        controls_layout.addWidget(search_bar)
        controls_layout.addStretch()
        controls_layout.addWidget(self.add_item_btn)

        layout.addLayout(controls_layout)
        layout.addSpacing(15)

        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(6)
        self.inventory_table.setHorizontalHeaderLabels([
            "order ID", "Product", "Category",
            "Sales channel", "Instruction", "Items"
        ])

        data = [
            ("#7676", "Potato", "cat1", "Store name", "Stock adjustment", "80/100"),
            ("#7676", "Carrot", "cat2", "Store name", "Stock adjustment", "80/100"),
            ("#7676", "Ginger", "cat2", "Store name", "Stock adjustment", "80/100")
        ]

        self.inventory_table.setRowCount(len(data))
        for row, item in enumerate(data):
            chkBoxItem = QTableWidgetItem()
            chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            chkBoxItem.setCheckState(Qt.Unchecked)
            self.inventory_table.setItem(row, 0, chkBoxItem)
            for col, val in enumerate(item):
                self.inventory_table.setItem(row, col, QTableWidgetItem(val))

        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.inventory_table.setAlternatingRowColors(True)
        self.inventory_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.inventory_table.verticalHeader().setVisible(False)

        layout.addWidget(self.inventory_table)

        page_widget.setStyleSheet(self.get_page_style())
        return page_widget

    # --- Inventory Form (Identical to before) ---
    def create_inventory_form(self):
        form_widget = QWidget()
        layout = QVBoxLayout(form_widget)
        layout.setContentsMargins(20, 10, 20, 20)

        red_header = QWidget()
        red_header.setStyleSheet("background-color: #C0392B; border-radius: 5px;")
        red_header_layout = QHBoxLayout(red_header)
        page_title = QLabel("Add New Inventory Item")
        page_title.setFont(QFont('Arial', 16, QFont.Bold))
        page_title.setStyleSheet("color: white; padding: 10px;")
        red_header_layout.addWidget(page_title)
        layout.addWidget(red_header)
        layout.addSpacing(15)

        self.inv_form_error_label = QLabel("")
        self.inv_form_error_label.setFont(QFont('Arial', 10))
        self.inv_form_error_label.setStyleSheet(
            "color: red; padding: 10px; background-color: #FADBD8; border-radius: 5px;")
        self.inv_form_error_label.setAlignment(Qt.AlignCenter)
        self.inv_form_error_label.setWordWrap(True)
        self.inv_form_error_label.hide()
        layout.addWidget(self.inv_form_error_label)

        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.inv_product_name = QLineEdit()
        self.inv_sku = QLineEdit()
        self.inv_category = QComboBox()
        self.inv_category.addItems(["cat1", "cat2", "Add New..."])
        self.inv_description = QTextEdit()
        self.inv_description.setPlaceholderText("Enter item description...")
        self.inv_description.setFixedHeight(80)

        self.inv_stock = QSpinBox()
        self.inv_stock.setRange(0, 9999)
        self.inv_reorder_level = QSpinBox()
        self.inv_reorder_level.setRange(0, 9999)

        self.inv_cost_price = QDoubleSpinBox()
        self.inv_cost_price.setRange(0.00, 99999.99)
        self.inv_cost_price.setPrefix("₱ ")
        self.inv_sell_price = QDoubleSpinBox()
        self.inv_sell_price.setRange(0.00, 99999.99)
        self.inv_sell_price.setPrefix("₱ ")

        self.inv_image_btn = QPushButton("Upload Product Image")
        self.inv_image_label = QLabel("No file selected.")
        self.inv_image_btn.clicked.connect(self.select_inv_image)
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.inv_image_btn)
        image_layout.addWidget(self.inv_image_label)

        self.inv_perishable = QCheckBox("Item is Perishable")

        form_layout.addRow(QLabel("Product Name:"), self.inv_product_name)
        form_layout.addRow(QLabel("SKU:"), self.inv_sku)
        form_layout.addRow(QLabel("Category:"), self.inv_category)
        form_layout.addRow(QLabel("Description:"), self.inv_description)
        form_layout.addRow(QLabel("Current Stock:"), self.inv_stock)
        form_layout.addRow(QLabel("Reorder Level:"), self.inv_reorder_level)
        form_layout.addRow(QLabel("Cost Price:"), self.inv_cost_price)
        form_layout.addRow(QLabel("Selling Price:"), self.inv_sell_price)
        form_layout.addRow(QLabel("Product Image:"), image_layout)
        form_layout.addRow(QLabel(""), self.inv_perishable)

        layout.addLayout(form_layout)
        layout.addStretch()

        button_layout = QHBoxLayout()
        self.inv_save_btn = QPushButton("Save Item")
        self.inv_save_btn.setObjectName("save_button")
        self.inv_cancel_btn = QPushButton("Cancel")
        self.inv_cancel_btn.setObjectName("cancel_button")

        button_layout.addStretch()
        button_layout.addWidget(self.inv_cancel_btn)
        button_layout.addWidget(self.inv_save_btn)

        layout.addLayout(button_layout)

        self.inv_save_btn.clicked.connect(self.validate_inventory_form)
        self.inv_cancel_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        form_widget.setStyleSheet(self.get_form_style())
        return form_widget

    def select_inv_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Image files (*.jpg *.png)")
        if fname:
            self.inv_image_label.setText(fname.split('/')[-1])

    def validate_inventory_form(self):
        errors = []
        product_name = self.inv_product_name.text()
        sku = self.inv_sku.text()
        stock = self.inv_stock.value()
        sell_price = self.inv_sell_price.value()

        if not product_name: errors.append("Product Name is required.")
        if not sku: errors.append("SKU is required.")
        if stock <= 0: errors.append("Current Stock must be greater than 0.")
        if sell_price <= 0.0: errors.append("Selling Price must be set.")

        if errors:
            self.inv_form_error_label.setText("\n".join(errors))
            self.inv_form_error_label.show()
            return

        self.inv_form_error_label.hide()
        print("--- Inventory Form Validation Successful ---")
        self.stacked_widget.setCurrentIndex(2)

    # --- NEW: SUPPORTING FORM 2 (HELP & ABOUT PAGE) ---
    def create_help_about_page(self):
        """Creates the 'Help & About' page with tabs, implementing the flowchart."""
        page_widget = QWidget()
        layout = QVBoxLayout(page_widget)
        layout.setContentsMargins(20, 10, 20, 20)

        # Red Header
        red_header = QWidget()
        red_header.setStyleSheet("background-color: #C0392B; border-radius: 5px;")
        red_header_layout = QHBoxLayout(red_header)
        page_title = QLabel("Help & About")
        page_title.setFont(QFont('Arial', 16, QFont.Bold))
        page_title.setStyleSheet("color: white; padding: 10px;")
        red_header_layout.addWidget(page_title)
        layout.addWidget(red_header)
        layout.addSpacing(15)

        # --- Tab Widget for 'SELECT TOPIC' ---
        tab_widget = QTabWidget()

        # Create the two tabs
        help_feedback_tab = self.create_help_feedback_tab()  # "Yes" path
        about_tab = self.create_about_tab()  # "No" path

        tab_widget.addTab(help_feedback_tab, "Help & Feedback")
        tab_widget.addTab(about_tab, "About")

        layout.addWidget(tab_widget)
        page_widget.setStyleSheet(self.get_form_style())  # Use form styling
        return page_widget

    def create_about_tab(self):
        """Creates the 'About' tab content. (Flowchart 'No' path)"""
        about_widget = QWidget()
        layout = QVBoxLayout(about_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("About JLPOS")
        title.setFont(QFont('Arial', 14, QFont.Bold))

        version = QLabel("Version: 1.0 (Mock-up)")
        developer = QLabel("Developer: [Your Group Name Here]")
        credits = QLabel("Built with: Python 3, PyQt5")

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(version)
        layout.addWidget(developer)
        layout.addWidget(credits)

        return about_widget

    def create_help_feedback_tab(self):
        """Creates the 'Help' tab with FAQ and the Feedback Form. (Flowchart 'Yes' path)"""
        help_widget = QWidget()
        layout = QVBoxLayout(help_widget)
        layout.setContentsMargins(10, 15, 10, 10)

        # --- 1. 'DISPLAY HELP CONTENT' ---
        faq_group = QGroupBox("Frequently Asked Questions (FAQ)")
        faq_layout = QVBoxLayout()

        faq_text = QTextEdit()
        faq_text.setReadOnly(True)
        faq_text.setHtml("""
            <b>Q: How do I add a new employee?</b>
            <p>A: Navigate to the 'Staff' page from the sidebar and click the '+ Add Employee' button.</p>

            <b>Q: How do I edit an item in the inventory?</b>
            <p>A: On the 'Inventory' page, click the 'Edit' icon (not yet implemented) on the row of the item you wish to change.</p>

            <b>Q: I forgot my password, what do I do?</b>
            <p>A: On the login screen, click the 'Forgot Password?' link. (This feature is a placeholder).</p>
        """)
        faq_layout.addWidget(faq_text)
        faq_group.setLayout(faq_layout)

        # --- 2. 'NEED MORE ASSISTANCE?' -> 'SHOW SUPPORT CONTACT' (The Form) ---
        contact_group = QGroupBox("Need More Assistance? Submit a Ticket")
        contact_layout = QFormLayout()
        contact_layout.setSpacing(15)

        # Feedback Form Controls (10+ controls)
        self.fb_name = QLineEdit(self.current_user_name)
        self.fb_name.setReadOnly(True)

        self.fb_emp_num = QLineEdit(self.current_user_id)
        self.fb_emp_num.setReadOnly(True)

        self.fb_type = QComboBox()
        self.fb_type.addItems(["Bug Report", "Feature Request", "General Question"])

        self.fb_subject = QLineEdit()
        self.fb_subject.setPlaceholderText("e.g., Cannot add new employee")

        self.fb_message = QTextEdit()
        self.fb_message.setPlaceholderText("Please describe the issue in detail...")
        self.fb_message.setMinimumHeight(100)

        self.fb_urgency_group = QGroupBox("Urgency")
        urgency_layout = QHBoxLayout()
        self.fb_urg_low = QRadioButton("Low")
        self.fb_urg_med = QRadioButton("Medium")
        self.fb_urg_high = QRadioButton("High")
        self.fb_urg_low.setChecked(True)
        urgency_layout.addWidget(self.fb_urg_low)
        urgency_layout.addWidget(self.fb_urg_med)
        urgency_layout.addWidget(self.fb_urg_high)
        self.fb_urgency_group.setLayout(urgency_layout)

        self.fb_submit_btn = QPushButton("Submit Feedback")
        self.fb_submit_btn.setObjectName("save_button")  # Use green style

        # Error/Success labels
        self.fb_error_label = QLabel("")
        self.fb_error_label.setStyleSheet("color: red;")
        self.fb_error_label.hide()

        self.fb_success_label = QLabel("Success! Your feedback has been submitted.")
        self.fb_success_label.setStyleSheet("color: green; font-weight: bold;")
        self.fb_success_label.hide()

        # Add to form
        contact_layout.addRow(QLabel("Your Name:"), self.fb_name)
        contact_layout.addRow(QLabel("Employee Number:"), self.fb_emp_num)
        contact_layout.addRow(QLabel("Feedback Type:"), self.fb_type)
        contact_layout.addRow(QLabel("Subject:"), self.fb_subject)
        contact_layout.addRow(QLabel("Message:"), self.fb_message)
        contact_layout.addRow(self.fb_urgency_group)
        contact_layout.addRow(self.fb_error_label)
        contact_layout.addRow(self.fb_success_label)
        contact_layout.addRow(self.fb_submit_btn)

        contact_group.setLayout(contact_layout)

        # Connect button
        self.fb_submit_btn.clicked.connect(self.validate_feedback_form)

        layout.addWidget(faq_group, 1)  # 1 stretch
        layout.addWidget(contact_group, 2)  # 2 stretch

        return help_widget

    def validate_feedback_form(self):
        """Validates and 'submits' the feedback form."""
        self.fb_error_label.hide()
        self.fb_success_label.hide()

        subject = self.fb_subject.text()
        message = self.fb_message.toPlainText()

        errors = []
        if not subject:
            errors.append("Subject is required.")
        if not message:
            errors.append("Message is required.")
        if len(message) < 20:
            errors.append("Message must be at least 20 characters.")

        if errors:
            self.fb_error_label.setText("\n".join(errors))
            self.fb_error_label.show()
            return

        # --- Functionality (Data Handling) ---
        print("--- Feedback Form Submitted ---")
        print(f"From: {self.current_user_name} ({self.current_user_id})")
        print(f"Type: {self.fb_type.currentText()}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")

        # Clear form and show success
        self.fb_subject.clear()
        self.fb_message.clear()
        self.fb_success_label.show()

    # --- Reusable Stylesheet Functions ---
    def get_page_style(self):
        return """
            QTableWidget {
                border: 1px solid #E0E0E0; gridline-color: #E0E0E0;
            }
            QHeaderView::section {
                background-color: #F8F8F8; padding: 4px;
                border: 1px solid #E0E0E0; font-weight: bold;
            }
            QTableWidget::item { padding: 5px; }
            QTableWidget::item:alternate { background-color: #FDF5E6; }
            QPushButton#add_button {
                background-color: #C0392B; color: white;
                font-weight: bold; padding: 8px 15px;
                border-radius: 5px; border: none;
            }
            QPushButton#add_button:hover { background-color: #A93226; }
            QLineEdit, QComboBox {
                padding: 5px 10px; border: 1px solid #CCC;
                border-radius: 5px;
            }
        """

    def get_form_style(self):
        return """
            QLabel { font-size: 13px; }
            QLineEdit, QComboBox, QTextEdit, QSpinBox, QDoubleSpinBox, QTabWidget::pane {
                padding: 8px; border: 1px solid #CCC;
                border-radius: 5px;
            }
            QTabWidget::tab-bar { left: 10px; }
            QTabBar::tab {
                background: #E0E0E0; border: 1px solid #C0C0C0;
                border-bottom: none; border-top-left-radius: 5px;
                border-top-right-radius: 5px; padding: 8px 15px;
            }
            QTabBar::tab:selected {
                background: white; font-weight: bold;
            }
            QGroupBox {
                border: 1px solid #CCC; border-radius: 5px;
                margin-top: 10px; font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin; subcontrol-position: top left;
                padding: 0 3px; left: 10px;
            }
            QPushButton {
                padding: 8px 15px; border-radius: 5px;
                border: 1px solid #CCC; background-color: #F0F0E0;
            }
            QPushButton#save_button {
                background-color: #28A745; color: white;
                font-weight: bold; border: none;
            }
            QPushButton#save_button:hover { background-color: #218838; }
            QPushButton#cancel_button:hover { background-color: #E0E0E0; }
        """


# --- Main execution ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont('Arial', 10))
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
