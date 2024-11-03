from PySide6.QtCore import QDate, QSize
from PySide6.QtGui import QIcon, Qt, QPixmap
from PySide6.QtWidgets import QMainWindow, QScrollArea, QVBoxLayout, QPushButton, \
    QHBoxLayout, QLabel, QMessageBox, QWidget, QDialog, QTableWidget, QComboBox, QSpinBox, QCheckBox, \
    QTableWidgetItem, QFileDialog

import os
import pandas as pd
import pdf_workers


class MainWindow(QMainWindow):
    endsem_dropdown: QComboBox
    assignments_spinbox: QSpinBox
    missed_quiz_checkbox: QCheckBox
    quiz_spinbox: QSpinBox
    num_days_spinner: QSpinBox
    table: QTableWidget
    save_button: QPushButton
    add_button: QPushButton
    remove_button: QPushButton
    load_button: QPushButton
    missed_midsem_checkbox: QCheckBox
    midsem_checkbox: QCheckBox
    right_panel: QWidget
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

        horizontal_layout = QHBoxLayout()
        horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        horizontal_layout.addWidget(self.block_select)
        horizontal_layout.addSpacing(15)
        horizontal_layout.addWidget(area)
        horizontal_layout.addSpacing(15)
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

        title = QLabel("Attendance / Marks Sheet Generator")
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

        self.load_button = QPushButton("Load")
        self.load_button.setToolTip("Load students list from csv file")
        self.load_button.setStyleSheet("""
            QPushButton {
                background-color: #021002;
                color: #16DB65;
                font-family: Century Gothic;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #16DB65;
                color: #021002;
                border: 2px solid #021002;
                font-weight: bold;
            }
            QToolTip {
                background-color: #021002;
                color: #16DB65;
                font-family: Century Gothic;
                font-size: 14px;
                border: 1px solid #16DB65;
                border-radius: 10px;
            }
        """)
        self.load_button.setMinimumSize(100, 30)
        self.load_button.setMaximumSize(100, 30)

        self.save_button = QPushButton("Save")
        self.save_button.setToolTip("Save students list to csv file")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #021002;
                color: #16DB65;
                font-family: Century Gothic;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #16DB65;
                color: #021002;
                border: 2px solid #021002;
                font-weight: bold;
            }
            QToolTip {
                background-color: #021002;
                color: #16DB65;
                font-family: Century Gothic;
                font-size: 14px;
                border: 1px solid #16DB65;
                border-radius: 10px;
            }
        """)
        self.save_button.setMinimumSize(100, 30)
        self.save_button.setMaximumSize(100, 30)

        self.add_button = QPushButton("Add")
        self.add_button.setToolTip("Add a new student to the list")
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #021002;
                color: #16DB65;
                font-family: Century Gothic;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #16DB65;
                color: #021002;
                border: 2px solid #021002;
                font-weight: bold;
            }
            QToolTip {
                background-color: #021002;
                color: #16DB65;
                font-family: Century Gothic;
                font-size: 14px;
                border: 1px solid #16DB65;
                border-radius: 10px;
            }
        """)
        self.add_button.setMinimumSize(100, 30)
        self.add_button.setMaximumSize(100, 30)

        self.remove_button = QPushButton("Remove")
        self.remove_button.setToolTip("Remove selected student from the list")
        self.remove_button.setStyleSheet("""
            QPushButton {
                background-color: #021002;
                color: #16DB65;
                font-family: Century Gothic;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #16DB65;
                color: #021002;
                border: 2px solid #021002;
                font-weight: bold;
            }
            QToolTip {
                background-color: #021002;
                color: #16DB65;
                font-family: Century Gothic;
                font-size: 14px;
                border: 1px solid #16DB65;
                border-radius: 10px;
            }
        """)
        self.remove_button.setMinimumSize(100, 30)
        self.remove_button.setMaximumSize(100, 30)

        self.load_button.clicked.connect(self.on_load_button_pressed)
        self.save_button.clicked.connect(self.on_save_button_pressed)
        self.add_button.clicked.connect(self.on_add_button_pressed)
        self.remove_button.clicked.connect(self.on_remove_button_pressed)

        action_buttons_layout.addWidget(self.load_button)
        action_buttons_layout.addWidget(self.save_button)
        action_buttons_layout.addWidget(self.add_button)
        action_buttons_layout.addWidget(self.remove_button)

        ####################################################

        self.table = QTableWidget()
        self.table.setRowCount(64)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Reg. No.", "Name"])
        self.table.setStyleSheet("""
            QScrollBar { background-color: #38AD6B; }
            QScrollBar::handle { background-color: #021002; }
            QScrollBar::add-line, QScrollBar::sub-line { background: none; }
            QScrollBar::add-page, QScrollBar::sub-page { background: none; }

            QHeaderView::section {
                background-color: #021002;
                font-family: "Montserrat";
                font-size: 14px;
            }

            QTableWidget::item {
                background-color: #38AD6B;
                font-family: "Montserrat";
                font-size: 14px;
                color: #021002;
            }

            QTableWidget::item:selected {
                background-color: #0078D7;
                color: #021002;
                font-family: "Montserrat";
                font-size: 14px;
            }
        """)

        # Set table to stretch and fill the window
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setStretchLastSection(True)

        self.table.horizontalHeader().setFixedHeight(40)
        self.table.horizontalHeader().setDefaultSectionSize(150)
        self.table.verticalHeader().setDefaultSectionSize(30)

        layout.addLayout(action_buttons_layout)
        layout.addWidget(self.table)

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
        self.class_dropdown.addItem("Lab-integrated")
        self.class_dropdown.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 18px;
            font-weight: bold;
        """)
        self.class_dropdown.setMinimumSize(180, 30)
        self.class_dropdown.setMaximumSize(180, 30)
        self.class_dropdown.currentIndexChanged.connect(self.on_class_dropdown_changed)

        top_layout = QVBoxLayout()
        top_layout.setSpacing(10)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        top_layout.addWidget(label1)
        top_layout.addWidget(self.class_dropdown)

        #########################################################################

        requirements_layout = QVBoxLayout()
        requirements_layout.setSpacing(10)
        requirements_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        # 2 buttons - temporary attendance and full attendance
        temp_attendance_button = QPushButton("Temporary Attendance")
        temp_attendance_button.setStyleSheet("""
            QPushButton {
                background-color: #021002;
                color: #16DB65;
                font-family: Century Gothic;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #16DB65;
                color: #021002;
                border: 2px solid #021002;
                font-weight: bold;
            }
        """)
        temp_attendance_button.setMinimumSize(200, 40)
        temp_attendance_button.setMaximumSize(200, 40)

        attendance_button = QPushButton("Attendance")
        attendance_button.setStyleSheet("""
            QPushButton {
                background-color: #021002;
                color: #16DB65;
                font-family: Century Gothic;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #16DB65;
                color: #021002;
                border: 2px solid #021002;
                font-weight: bold;
            }
        """)
        attendance_button.setMinimumSize(200, 40)
        attendance_button.setMaximumSize(200, 40)

        marks_button = QPushButton("Marks")
        marks_button.setStyleSheet("""
            QPushButton {
                background-color: #021002;
                color: #16DB65;
                font-family: Century Gothic;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #16DB65;
                color: #021002;
                border: 2px solid #021002;
                font-weight: bold;
            }
        """)
        marks_button.setMinimumSize(200, 40)
        marks_button.setMaximumSize(200, 40)

        attendance_marks_button = QPushButton("Attendance + Marks")
        attendance_marks_button.setStyleSheet("""
            QPushButton {
                background-color: #021002;
                color: #16DB65;
                font-family: Century Gothic;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #16DB65;
                color: #021002;
                border: 2px solid #021002;
                font-weight: bold;
            }
        """)
        attendance_marks_button.setMinimumSize(200, 40)
        attendance_marks_button.setMaximumSize(200, 40)

        temp_attendance_button.clicked.connect(self.on_temp_attendance_button_clicked)
        attendance_button.clicked.connect(self.on_attendance_button_clicked)
        marks_button.clicked.connect(self.on_marks_button_clicked)
        attendance_marks_button.clicked.connect(self.on_attendance_marks_button_clicked)

        # Add everything to the main layout
        requirements_layout.addWidget(temp_attendance_button)
        requirements_layout.addWidget(attendance_button)
        requirements_layout.addWidget(marks_button)
        requirements_layout.addWidget(attendance_marks_button)

        #########################################################################

        block_select_layout = QVBoxLayout()
        block_select_layout.addLayout(top_layout)
        block_select_layout.addLayout(requirements_layout)

        self.block_select = QWidget()
        self.block_select.setMaximumWidth(210)
        self.block_select.setLayout(block_select_layout)

    def create_actions_list(self):  # sourcery skip: extract-duplicate-method

        attendance_label = QLabel("Attendance")
        attendance_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        attendance_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 24px;
            color: #16DB65;
            font-weight: bold;
        """)

        line = QLabel()
        line.setFixedHeight(3)
        line.setStyleSheet("""background-color: #16DB65;""")

        num_days_label = QLabel("Number of Days")
        num_days_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        num_days_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        self.num_days_spinner = QSpinBox()
        self.num_days_spinner.setMinimum(1)
        self.num_days_spinner.setMaximum(100)
        self.num_days_spinner.setValue(1)
        self.num_days_spinner.setFixedWidth(70)
        self.num_days_spinner.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
        """)

        hlayout = QHBoxLayout()
        hlayout.addWidget(num_days_label)
        hlayout.addStretch()
        hlayout.addWidget(self.num_days_spinner)

        ##########################################################################

        marks_label = QLabel("Marks")
        marks_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        marks_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 24px;
            color: #16DB65;
            font-weight: bold;
        """)

        line2 = QLabel()
        line2.setFixedHeight(3)
        line2.setStyleSheet("""background-color: #16DB65;""")

        midsem_label = QLabel("Mid Semester")
        midsem_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        midsem_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        self.midsem_checkbox = QCheckBox()
        self.midsem_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 30px;
                height: 30px;
            }
            QCheckBox {
                font-family: Century Gothic;
                font-size: 16px;
            }
        """)
        self.midsem_checkbox.setChecked(True)
        self.midsem_checkbox.checkStateChanged.connect(self.on_midsem_checkbox_changed)

        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(midsem_label)
        hlayout2.addStretch()
        hlayout2.addWidget(self.midsem_checkbox)

        missed_midsem_label = QLabel("Missed Mid Semester")
        missed_midsem_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        missed_midsem_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        self.missed_midsem_checkbox = QCheckBox()
        self.missed_midsem_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 30px;
                height: 30px;
            }
            QCheckBox {
                font-family: Century Gothic;
                font-size: 16px;
            }
        """)
        self.missed_midsem_checkbox.setEnabled(False)
        self.missed_midsem_checkbox.setChecked(True)

        hlayout3 = QHBoxLayout()
        hlayout3.addWidget(missed_midsem_label)
        hlayout3.addStretch()
        hlayout3.addWidget(self.missed_midsem_checkbox)

        quiz_label = QLabel("Quiz")
        quiz_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        quiz_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        self.quiz_spinbox = QSpinBox()
        self.quiz_spinbox.setMinimum(0)
        self.quiz_spinbox.setMaximum(5)
        self.quiz_spinbox.setFixedWidth(70)
        self.quiz_spinbox.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
        """)

        hlayout4 = QHBoxLayout()
        hlayout4.addWidget(quiz_label)
        hlayout4.addStretch()
        hlayout4.addWidget(self.quiz_spinbox)

        missed_quiz_label = QLabel("Missed Quiz")
        missed_quiz_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        missed_quiz_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        self.missed_quiz_checkbox = QCheckBox()
        self.missed_quiz_checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 30px;
                height: 30px;
            }
            QCheckBox {
                font-family: Century Gothic;
                font-size: 16px;
            }
        """)

        hlayout5 = QHBoxLayout()
        hlayout5.addWidget(missed_quiz_label)
        hlayout5.addStretch()
        hlayout5.addWidget(self.missed_quiz_checkbox)

        assignments_label = QLabel("Assignments")
        assignments_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        assignments_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        self.assignments_spinbox = QSpinBox()
        self.assignments_spinbox.setMinimum(0)
        self.assignments_spinbox.setMaximum(5)
        self.assignments_spinbox.setFixedWidth(70)
        self.assignments_spinbox.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
        """)

        hlayout6 = QHBoxLayout()
        hlayout6.addWidget(assignments_label)
        hlayout6.addStretch()
        hlayout6.addWidget(self.assignments_spinbox)

        # sessional_label = QLabel("Sessional")
        # sessional_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # sessional_label.setStyleSheet("""
        #     font-family: Century Gothic;
        #     font-size: 16px;
        #     color: #16DB65;
        # """)
        #
        # sessional_checkbox = QCheckBox()
        # sessional_checkbox.setStyleSheet("""
        #     QCheckBox::indicator {
        #         width: 30px;
        #         height: 30px;
        #     }
        #     QCheckBox {
        #         font-family: Century Gothic;
        #         font-size: 16px;
        #     }
        # """)
        #
        # hlayout6 = QHBoxLayout()
        # hlayout6.addWidget(sessional_label)
        # hlayout6.addStretch()
        # hlayout6.addWidget(sessional_checkbox)

        endsem_label = QLabel("End Semester")
        endsem_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        endsem_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)
        self.endsem_dropdown = QComboBox()
        self.endsem_dropdown.addItem("Written")
        self.endsem_dropdown.addItem("Project")
        self.endsem_dropdown.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
        """)
        self.endsem_dropdown.setMinimumSize(120, 30)
        self.endsem_dropdown.setMaximumSize(120, 30)

        hlayout7 = QHBoxLayout()
        hlayout7.addWidget(endsem_label)
        hlayout7.addStretch()
        hlayout7.addWidget(self.endsem_dropdown)

        attendance_marks_layout = QVBoxLayout()
        attendance_marks_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        attendance_marks_layout.setSpacing(10)

        attendance_marks_layout.addWidget(attendance_label)
        attendance_marks_layout.addWidget(line)
        attendance_marks_layout.addLayout(hlayout)
        attendance_marks_layout.addWidget(marks_label)
        attendance_marks_layout.addWidget(line2)
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
        pass

    def on_midsem_checkbox_changed(self, state):
        self.missed_midsem_checkbox.setChecked(state == Qt.CheckState.Checked)

    def on_load_button_pressed(self):

        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")

        # If the user selects a file
        if not file_name:
            return

        data_frame = pd.read_csv(file_name)

        self.table.setRowCount(len(data_frame))

        # Iterate over the DataFrame and populate the table
        for row_index in range(len(data_frame)):
            for column_index in range(data_frame.shape[1]):
                # Get the item from the dataframe
                item = str(data_frame.iloc[row_index, column_index])
                table_item = QTableWidgetItem(item)
                # Set the item in the table
                self.table.setItem(row_index, column_index, table_item)

    def on_remove_button_pressed(self):
        # Get the selected row
        # todo: when the user clicks on remove button without selecting any row, the program has unexpected behavior
        # todo: multi select rows and remove them all at once

        selected_row = self.table.currentRow()
        self.table.removeRow(selected_row)
        # self.table.setRowCount(self.table.rowCount() - 1)

    def on_add_button_pressed(self):
        # Add a new row to the table after the selected row
        selected_row = self.table.currentRow()
        self.table.insertRow(selected_row + 1)

    def create_data_frame(self):
        data = []

        for row_index in range(self.table.rowCount()):
            row = []
            for column_index in range(self.table.columnCount()):
                item = self.table.item(row_index, column_index)
                if item is not None:
                    row.append(item.text())
                else:
                    row.append("")
            data.append(row)

        return pd.DataFrame(data)

    def on_save_button_pressed(self):

        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")

        if not file_name:
            return

        self.create_data_frame().to_csv(file_name, index=False)

    def on_temp_attendance_button_clicked(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)")

        if not file_name:
            return

        pdf_workers.attendance_sheet_pdf.generate_attendance_sheet(self.create_data_frame(), 20, file_name)

    def on_attendance_button_clicked(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)")

        if not file_name:
            return

        pdf_workers.attendance_sheet_pdf.generate_attendance_sheet(self.create_data_frame(),
                                                                   self.num_days_spinner.value(), file_name)

    def on_marks_button_clicked(self):

        requirements_dict = {
            'Roll No.': (1, 10),
            'Reg. No.': (1, 40),
            'Name of Student': (1, 60),
            'Mid Sem': (self.midsem_checkbox.isChecked(), 20),
            'Missed Mid Sem': (self.missed_midsem_checkbox.isChecked(), 25),
            'Quiz': (self.quiz_spinbox.value(), 13),
            'Missed Quiz': (self.missed_quiz_checkbox.isChecked(), 20),
            'Assignment': (self.assignments_spinbox.value(), 20),
            'Sessional Marks': (1, 25),
            f'End Sem ({self.endsem_dropdown.currentText()})': (1, 25),
            'Total Marks': (1, 20),
            'Grade': (1, 15)
        }

        file_name, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)")

        if not file_name:
            return

        pdf_workers.marks_sheet_pdf.generate_marks_sheet(self.create_data_frame(), requirements_dict, file_name)

    def on_attendance_marks_button_clicked(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)")

        if not file_name:
            return

        pdf_workers.attendance_sheet_pdf.generate_attendance_sheet(self.create_data_frame(),
                                                                   self.num_days_spinner.value(), 'a.pdf')

        requirements_dict = {
            'Roll No.': (1, 10),
            'Reg. No.': (1, 40),
            'Name of Student': (1, 60),
            'Mid Sem': (self.midsem_checkbox.isChecked(), 20),
            'Missed Mid Sem': (self.missed_midsem_checkbox.isChecked(), 25),
            'Quiz': (self.quiz_spinbox.value(), 13),
            'Missed Quiz': (self.missed_quiz_checkbox.isChecked(), 20),
            'Assignment': (self.assignments_spinbox.value(), 20),
            'Sessional Marks': (1, 25),
            f'End Sem ({self.endsem_dropdown.currentText()})': (1, 25),
            'Total Marks': (1, 20),
            'Grade': (1, 15)
        }

        pdf_workers.marks_sheet_pdf.generate_marks_sheet(self.create_data_frame(), requirements_dict, 'm.pdf')

        pdf_workers.merger.merge_pdfs('a.pdf', 'm.pdf', file_name)

        os.remove('a.pdf')
        os.remove('m.pdf')
