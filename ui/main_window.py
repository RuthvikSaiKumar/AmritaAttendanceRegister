from PySide6.QtCore import QDate, QSize
from PySide6.QtGui import QIcon, Qt, QPixmap
from PySide6.QtWidgets import QMainWindow, QScrollArea, QVBoxLayout, QPushButton, \
    QHBoxLayout, QLabel, QMessageBox, QWidget, QDialog, QTableWidget, QComboBox, QSpinBox, QCheckBox


class MainWindow(QMainWindow):
    right_panel: QWidget
    requirements_title_label: QLabel
    class_dropdown: QComboBox
    sheet_dropdown: QComboBox
    block_select: QWidget
    attendance_panel: QWidget
    attendance_scroll_list: QScrollArea
    date_label: QLabel
    settings_button: QPushButton
    github: QPushButton
    switch_theme_button: QPushButton
    help_button: QPushButton
    hlayout: QHBoxLayout
    app_usage_list_label: QLabel

    # todo: make all single use buttons to local and return the button from function instead of making global

    def __init__(self):
        super().__init__()

        self.init_window()

        self.create_title_bar()

        self.create_block_select()
        self.create_attendance_list()
        self.create_actions_list()

        area = QWidget()
        area.setStyleSheet("""
            background-color: #38AD6B;
            border-radius: 10px;
        """)
        dummy_layout = QHBoxLayout()
        dummy_layout.addWidget(self.attendance_panel)
        area.setLayout(dummy_layout)
        area.setMaximumWidth(700)

        ############################################

        # todo: add spacing and vertical lines as separators

        horizontal_layout = QHBoxLayout()
        horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        horizontal_layout.addWidget(self.block_select)
        horizontal_layout.addWidget(area)
        horizontal_layout.addWidget(self.right_panel)

        central_widget = QWidget()
        central_widget.setLayout(horizontal_layout)

        ###############################################################################################

        self.create_help_button()
        self.create_switch_theme_button()
        self.create_github_link()
        self.create_settings_button()
        self.create_date_display()

        left_layout = QHBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        left_layout.addWidget(self.date_label)

        right_layout = QHBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        right_layout.addWidget(self.settings_button)
        right_layout.addWidget(self.switch_theme_button)
        right_layout.addWidget(self.help_button)
        right_layout.addWidget(self.github)

        bottom_bar = QHBoxLayout()
        bottom_bar.addLayout(left_layout)
        bottom_bar.addLayout(right_layout)

        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addWidget(central_widget)
        self.vlayout.addLayout(bottom_bar)

        self.dummy_widget = QWidget()
        self.dummy_widget.setLayout(self.vlayout)
        self.setCentralWidget(self.dummy_widget)

    def init_window(self):
        self.setWindowTitle("Attendance ")
        self.setMinimumSize(1200, 600)
        icon = QIcon("assets/icon1.png")
        self.setWindowIcon(icon)
        self.setStyleSheet("""
                background-color: #021002;
        """)
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

    def create_title_bar(self):
        image = QLabel()
        image.setPixmap(QPixmap("assets/icon1.png"))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image.setScaledContents(True)
        image.setMinimumSize(50, 50)
        image.setMaximumSize(50, 50)

        title = QLabel("Attendance/Marks Sheet Generator")
        title.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        title.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 24px;
            color: #38AD6B;
            font-weight: bold;
        """)

        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(image)
        self.hlayout.addSpacing(10)
        self.hlayout.addWidget(title)

    def create_attendance_list(self):  # sourcery skip: extract-duplicate-method

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        ####################################################

        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        load_button = QPushButton("Load")
        load_button.setToolTip("Load students list from csv file")
        load_button.setStyleSheet("""
            background-color: #021002;
            color: #16DB65;
            font-family: Century Gothic;
            font-size: 16px;
        """)
        load_button.setMinimumSize(100, 30)
        load_button.setMaximumSize(100, 30)

        save_button = QPushButton("Save")
        save_button.setToolTip("Save students list to csv file")
        save_button.setStyleSheet("""
            background-color: #021002;
            color: #16DB65;
            font-family: Century Gothic;
            font-size: 16px;
        """)
        save_button.setMinimumSize(100, 30)
        save_button.setMaximumSize(100, 30)

        add_button = QPushButton("Add")
        add_button.setToolTip("Add a new student to the list")
        add_button.setStyleSheet("""
            background-color: #021002;
            color: #16DB65;
            font-family: Century Gothic;
            font-size: 16px;
        """)
        add_button.setMinimumSize(100, 30)
        add_button.setMaximumSize(100, 30)

        remove_button = QPushButton("Remove")
        remove_button.setToolTip("Remove selected student from the list")
        remove_button.setStyleSheet("""
            background-color: #021002;
            color: #16DB65;
            font-family: Century Gothic;
            font-size: 16px;
        """)
        remove_button.setMinimumSize(100, 30)
        remove_button.setMaximumSize(100, 30)

        action_buttons_layout.addWidget(load_button)
        action_buttons_layout.addWidget(save_button)
        action_buttons_layout.addWidget(add_button)
        action_buttons_layout.addWidget(remove_button)

        ####################################################

        table = QTableWidget()
        table.setRowCount(640)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Reg. No.", "Name"])
        table.setStyleSheet("""
            QScrollBar { width: 10px; background-color: #38AD6B; }
            QScrollBar::handle { background-color: #021002; }
            QScrollBar::add-line, QScrollBar::sub-line { background: none; }
            QScrollBar::add-page, QScrollBar::sub-page { background: none; }

            QHeaderView::section {
                background-color: #021002;
                color: white;
                font-family: "Roboto";
                font-size: 14px;
            }

            QTableWidget::item {
                background-color: #38AD6B;
                color: white;
                font-family: "Roboto";
                font-size: 12px;
            }

            QTableWidget::item:selected {
                background-color: #0078D7;
                color: white;
                font-family: "Roboto";
                font-size: 12px;
            }
        """)

        # Set table to stretch and fill the window
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setStretchLastSection(True)

        table.horizontalHeader().setFixedHeight(40)
        table.horizontalHeader().setDefaultSectionSize(150)
        table.verticalHeader().setDefaultSectionSize(30)

        layout.addLayout(action_buttons_layout)
        layout.addWidget(table)

        self.attendance_panel = QWidget()
        self.attendance_panel.setLayout(layout)

    def create_block_select(self):  # sourcery skip: extract-duplicate-method
        label1 = QLabel("Select Class")
        label1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label1.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
            font-weight: bold;
        """)

        self.class_dropdown = QComboBox()
        self.class_dropdown.addItem("Theory")
        self.class_dropdown.addItem("Lab")
        self.class_dropdown.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            font-weight: bold;
        """)
        self.class_dropdown.setMinimumSize(180, 30)
        self.class_dropdown.setMaximumSize(180, 30)
        self.class_dropdown.currentIndexChanged.connect(self.on_class_dropdown_changed)

        label2 = QLabel("Select Sheet")
        label2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        label2.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
            font-weight: bold;
        """)

        self.sheet_dropdown = QComboBox()
        self.sheet_dropdown.addItem("Attendance")
        self.sheet_dropdown.addItem("Marks")
        self.sheet_dropdown.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            font-weight: bold;
        """)
        self.sheet_dropdown.setMinimumSize(180, 30)
        self.sheet_dropdown.setMaximumSize(180, 30)

        top_layout = QVBoxLayout()
        top_layout.setSpacing(10)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        top_layout.addWidget(label1)
        top_layout.addWidget(self.class_dropdown)
        top_layout.addWidget(label2)
        top_layout.addWidget(self.sheet_dropdown)

        #########################################################################

        requirements_layout = QVBoxLayout()
        requirements_layout.setSpacing(10)
        requirements_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        # todo: Requirements for the selected sheet (Theory/Lab)
        self.requirements_title_label = QLabel("Requirements")
        self.requirements_title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.requirements_title_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
            font-weight: bold;
        """)
        self.on_class_dropdown_changed(0)

        # First requirement: Roll No.
        requirement1 = QHBoxLayout()
        requirement1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        requirement1_label = QLabel("Attendance")
        requirement1_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        requirement1_image = QLabel()
        requirement1_image.setPixmap(QPixmap("assets/check-button.png"))
        requirement1_image.setScaledContents(True)
        requirement1_image.setMinimumSize(20, 20)
        requirement1_image.setMaximumSize(20, 20)

        # Add the label to the layout, then a stretch, then the image
        requirement1.addWidget(requirement1_label)
        requirement1.addStretch()  # This pushes the image to the right
        requirement1.addWidget(requirement1_image)
        requirement1.addWidget(QWidget())  # This gives margin to the right

        # Second requirement: Reg. No.
        requirement2 = QHBoxLayout()
        requirement2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        requirement2_label = QLabel("Marks")
        requirement2_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        requirement2_image = QLabel()
        requirement2_image.setPixmap(QPixmap("assets/cross-mark.png"))
        requirement2_image.setScaledContents(True)
        requirement2_image.setMinimumSize(20, 20)
        requirement2_image.setMaximumSize(20, 20)

        # Add the label to the layout, then a stretch, then the image
        requirement2.addWidget(requirement2_label)
        requirement2.addStretch()  # This pushes the image to the right
        requirement2.addWidget(requirement2_image)
        requirement2.addWidget(QWidget())  # This gives margin to the right

        # Add everything to the main layout
        requirements_layout.addWidget(self.requirements_title_label)
        requirements_layout.addLayout(requirement1)
        requirements_layout.addLayout(requirement2)

        #########################################################################

        block_select_layout = QVBoxLayout()
        block_select_layout.addLayout(top_layout)
        block_select_layout.addLayout(requirements_layout)

        self.block_select = QWidget()
        self.block_select.setMaximumWidth(210)
        self.block_select.setLayout(block_select_layout)

    def create_actions_list(self):  # sourcery skip: extract-duplicate-method

        # todo: make the title words have an underline like separator and a border for the whole panel
        # todo: disable the underline for the checkboxes
        # todo: manage the stretch going too far to the right

        attendance_label = QLabel("Attendance")
        attendance_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        attendance_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 24px;
            color: #16DB65;
            font-weight: bold;
        """)

        num_days_label = QLabel("Number of Days")
        num_days_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        num_days_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        num_days_spinner = QSpinBox()
        num_days_spinner.setMinimum(1)
        num_days_spinner.setMaximum(100)
        num_days_spinner.setValue(1)
        num_days_spinner.setFixedWidth(70)
        num_days_spinner.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
        """)

        hlayout = QHBoxLayout()
        hlayout.addWidget(num_days_label)
        hlayout.addStretch()
        hlayout.addWidget(num_days_spinner)

        ##########################################################################

        marks_label = QLabel("Marks")
        marks_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        marks_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 24px;
            color: #16DB65;
            font-weight: bold;
        """)

        midsem_label = QLabel("Midsem")
        midsem_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        midsem_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        midsem_checkbox = QCheckBox()
        midsem_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 30px;
                height: 30px;
            }
            QCheckBox {
                font-family: Century Gothic;
                font-size: 16px;
            }
        """)

        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(midsem_label)
        hlayout2.addStretch()
        hlayout2.addWidget(midsem_checkbox)

        t3_label = QLabel("T3")
        t3_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        t3_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        t3_checkbox = QCheckBox()
        t3_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 30px;
                height: 30px;
            }
            QCheckBox {
                font-family: Century Gothic;
                font-size: 16px;
            }
        """)

        hlayout3 = QHBoxLayout()
        hlayout3.addWidget(t3_label)
        hlayout3.addStretch()
        hlayout3.addWidget(t3_checkbox)

        qx_label = QLabel("Qx")
        qx_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        qx_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        qx_spinbox = QSpinBox()
        qx_spinbox.setMinimum(1)
        qx_spinbox.setMaximum(5)
        qx_spinbox.setValue(1)
        qx_spinbox.setFixedWidth(70)
        qx_spinbox.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
        """)

        hlayout4 = QHBoxLayout()
        hlayout4.addWidget(qx_label)
        hlayout4.addStretch()
        hlayout4.addWidget(qx_spinbox)

        quiz_label = QLabel("Quiz")
        quiz_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        quiz_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        quiz_spinbox = QSpinBox()
        quiz_spinbox.setMinimum(1)
        quiz_spinbox.setMaximum(5)
        quiz_spinbox.setValue(1)
        quiz_spinbox.setFixedWidth(70)
        quiz_spinbox.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
        """)

        hlayout5 = QHBoxLayout()
        hlayout5.addWidget(quiz_label)
        hlayout5.addStretch()
        hlayout5.addWidget(quiz_spinbox)

        sessional_label = QLabel("Sessional")
        sessional_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        sessional_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        sessional_checkbox = QCheckBox()
        sessional_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 30px;
                height: 30px;
            }
            QCheckBox {
                font-family: Century Gothic;
                font-size: 16px;
            }
        """)

        hlayout6 = QHBoxLayout()
        hlayout6.addWidget(sessional_label)
        hlayout6.addStretch()
        hlayout6.addWidget(sessional_checkbox)

        endsem_label = QLabel("Endsem")
        endsem_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        endsem_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)
        endsem_checkbox = QCheckBox()
        endsem_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 30px;
                height: 30px;
            }
            QCheckBox {
                font-family: Century Gothic;
                font-size: 16px;
            }
        """)

        hlayout7 = QHBoxLayout()
        hlayout7.addWidget(endsem_label)
        hlayout7.addStretch()
        hlayout7.addWidget(endsem_checkbox)

        attendance_marks_layout = QVBoxLayout()
        attendance_marks_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        attendance_marks_layout.setSpacing(10)

        attendance_marks_layout.addWidget(attendance_label)
        attendance_marks_layout.addLayout(hlayout)
        attendance_marks_layout.addWidget(marks_label)
        attendance_marks_layout.addLayout(hlayout2)
        attendance_marks_layout.addLayout(hlayout3)
        attendance_marks_layout.addLayout(hlayout4)
        attendance_marks_layout.addLayout(hlayout5)
        attendance_marks_layout.addLayout(hlayout6)
        attendance_marks_layout.addLayout(hlayout7)

        self.right_panel = QWidget()
        self.right_panel.setMaximumWidth(500)
        self.right_panel.setLayout(attendance_marks_layout)

    def create_help_button(self):
        self.help_button = QPushButton()
        self.help_button.setIcon(QIcon("assets/help.png"))
        self.help_button.setIconSize(QSize(20, 20))
        self.help_button.setToolTip("Help / Getting Started")
        self.help_button.setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
            border-radius: 10px;
            font-family: Century Gothic;
            font-size: 16px;
            font-weight: bold;
        """)
        self.help_button.setMinimumSize(30, 30)
        self.help_button.setMaximumSize(30, 30)

        self.help_button.clicked.connect(self.on_help_button_clicked)

    @staticmethod
    def on_help_button_clicked():
        # todo: make this a popup, and more visually appealing
        help_dialog = QDialog()
        help_dialog.setWindowTitle("Help")
        help_dialog.setMinimumSize(800, 400)
        help_dialog.setStyleSheet("""
                background-color: #021002;
        """)
        help_dialog.setWindowIcon(QIcon("assets/ReConnect Logo.png"))

        with open("assets/help.txt", "r") as file:
            help_text = file.read()
        help_text = QLabel(help_text)

        help_text.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        layout = QVBoxLayout()
        layout.addWidget(help_text)
        help_dialog.setLayout(layout)

        help_dialog.exec()

    def create_switch_theme_button(self):
        self.switch_theme_button = QPushButton()
        self.switch_theme_button.setIcon(QIcon("assets/theme.png"))
        self.switch_theme_button.setIconSize(QSize(20, 20))
        self.switch_theme_button.setToolTip("Switch Theme")
        self.switch_theme_button.setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
            font-family: Century Gothic;
            font-size: 16px;
            font-weight: bold;
        """)
        self.switch_theme_button.setMinimumSize(30, 30)
        self.switch_theme_button.setMaximumSize(30, 30)

        self.switch_theme_button.clicked.connect(self.on_switch_theme_button_clicked)

    @staticmethod
    def on_switch_theme_button_clicked():
        # todo: switch between dark and light theme

        notification = QMessageBox()
        notification.setWindowTitle("Switch Theme")
        notification.setText(
            "Feature Under Development\n\n"
            "This button will allow you to change the theme of the app."
        )
        notification.setStandardButtons(QMessageBox.StandardButton.Ok)
        notification.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 15px;
            color: #16DB65;
        """)
        notification.setWindowIcon(QIcon("assets/ReConnect Logo.png"))
        notification.button(QMessageBox.StandardButton.Ok).setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
        """)
        notification.exec()

    def create_github_link(self):
        self.github = QPushButton()
        self.github.setIcon(QIcon("assets/github.png"))
        self.github.setIconSize(QSize(20, 20))
        self.github.setToolTip("Open GitHub Repository")
        self.github.setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
            border-radius: 10px;
            font-family: Century Gothic;
            font-size: 16px;
            font-weight: bold;
        """)
        self.github.setMinimumSize(30, 30)
        self.github.setMaximumSize(30, 30)

        self.github.clicked.connect(self.on_github_clicked)

    @staticmethod
    def on_github_clicked():
        import webbrowser
        # todo: change it to organization's repository
        url = "https://github.com/RuthvikSaiKumar/AmritaAttendanceRegister"
        webbrowser.open(url)

    def create_settings_button(self):
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon("assets/settings.png"))
        self.settings_button.setIconSize(QSize(20, 20))
        self.settings_button.setToolTip("Settings")
        self.settings_button.setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
            border-radius: 10px;
            font-family: Century Gothic;
            font-size: 16px;
            font-weight: bold;
        """)
        self.settings_button.setMinimumSize(30, 30)
        self.settings_button.setMaximumSize(30, 30)

        self.settings_button.clicked.connect(self.on_settings_button_clicked)

    @staticmethod
    def on_settings_button_clicked():
        # todo: make this a popup
        notification = QMessageBox()
        notification.setWindowTitle("Settings")
        notification.setText(
            "Feature Under Development\n\n"
            "This button will allow you to change the settings of the app."
        )
        notification.setStandardButtons(QMessageBox.StandardButton.Ok)
        notification.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 15px;
            color: #16DB65;
        """)
        notification.setWindowIcon(QIcon("assets/ReConnect Logo.png"))
        notification.button(QMessageBox.StandardButton.Ok).setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
        """)
        notification.exec()

    def create_date_display(self):
        self.date_label = QLabel(QDate.currentDate().toString("dd MMM, yyyy - ddd"))
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

    #########################################################################################
    # EVENTS
    #########################################################################################

    def on_class_dropdown_changed(self, index):
        if index == 0:
            self.requirements_title_label.setText("Requirements for Theory")
        else:
            self.requirements_title_label.setText("Requirements for Lab")
        self.requirements_title_label.update()
