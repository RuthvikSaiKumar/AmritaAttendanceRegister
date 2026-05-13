import pandas as pd
from PySide6.QtCore import QDate, QSize, Qt, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QPoint
from PySide6.QtGui import QIcon, Qt, QPixmap, QColor

from PySide6.QtWidgets import (
    QMainWindow, QScrollArea, QVBoxLayout, QPushButton,
    QHBoxLayout, QLabel, QWidget, QDialog, QTableWidget, QComboBox, QSpinBox, QCheckBox,
    QTableWidgetItem, QFileDialog, QFrame, QSizePolicy, QGraphicsDropShadowEffect
)

import os, subprocess, sys

import pdf_workers


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


# ─── Colour palettes ─────────────────────────────────────────────────────────

DARK = {
    "bg": "#1A1F2E",
    "surface": "#242938",
    "surface_alt": "#2D3347",
    "border": "#3A4060",
    "accent": "#4A7CF7",
    "accent_hover": "#3D6EE8",
    "text_primary": "#E8EAF0",
    "text_secondary": "#9BA3B8",
    "text_on_accent": "#FFFFFF",
    "danger": "#E05252",
    "success": "#4CAF88",
    "header_bg": "#1A1F2E",
}

LIGHT = {
    "bg": "#F4F6FA",
    "surface": "#FFFFFF",
    "surface_alt": "#EEF1F8",
    "border": "#D0D6E8",
    "accent": "#3B6EF0",
    "accent_hover": "#2E5FDC",
    "text_primary": "#1C2340",
    "text_secondary": "#5C6480",
    "text_on_accent": "#FFFFFF",
    "danger": "#D44",
    "success": "#2E8B5A",
    "header_bg": "#FFFFFF",
}


def _btn_style(c: dict, variant: str = "ghost") -> str:
    """Return a QPushButton stylesheet given the palette and variant."""
    if variant == "accent":
        return f"""
            QPushButton {{
                background-color: {c['accent']};
                color: {c['text_on_accent']};
                border: none;
                border-radius: 6px;
                font-family: "Segoe UI", "SF Pro Display", sans-serif;
                font-size: 14px;
                padding: 6px 14px;
            }}
            QPushButton:hover {{
                background-color: {c['accent_hover']};
            }}
            QPushButton:pressed {{
                background-color: {c['accent_hover']};
                padding: 7px 13px 5px 15px;
            }}
        """
    # ghost / subtle
    return f"""
        QPushButton {{
            background-color: {c['surface_alt']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            font-family: "Segoe UI", "SF Pro Display", sans-serif;
            font-size: 13px;
            padding: 5px 12px;
        }}
        QPushButton:hover {{
            background-color: {c['accent']};
            color: {c['text_on_accent']};
            border-color: {c['accent']};
        }}
        QPushButton:pressed {{
            background-color: {c['accent_hover']};
        }}
        QToolTip {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: 4px;
            font-family: "Segoe UI", sans-serif;
            font-size: 12px;
            padding: 4px 8px;
        }}
    """


def _theme_btn_style(c: dict) -> str:
    return f"""
        QPushButton {{
            background-color: transparent;
            border: 1px solid {c['border']};
            border-radius: 5px;
            font-size: 16px;
        }}
        QPushButton:hover {{
            border-color: {c['accent']};
            background-color: transparent; /* Removes the blue highlight */
        }}
        """


def _icon_btn_style(c: dict) -> str:
    return f"""
        QPushButton {{
            background-color: {c['surface_alt']};
            border: 1px solid {c['border']};
            border-radius: 6px;
        }}
        QPushButton:hover {{
            background-color: {c['accent']};
            border-color: {c['accent']};
        }}
        QToolTip {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: 4px;
            font-family: "Segoe UI", sans-serif;
            font-size: 12px;
            padding: 4px 8px;
        }}
    """


def _label_style(c: dict, size: int = 13, bold: bool = False, secondary: bool = False) -> str:
    color = c['text_secondary'] if secondary else c['text_primary']
    weight = "bold" if bold else "normal"
    return f"""
        color: {color};
        font-family: "Segoe UI", "SF Pro Display", sans-serif;
        font-size: {size}px;
        font-weight: {weight};
        border: none;
        background: transparent;
    """


def _combo_style(c: dict) -> str:
    return f"""
        QComboBox {{
            background-color: {c['surface_alt']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
            padding: 4px 8px;
            outline: none;
        }}
        QComboBox:hover {{ border-color: {c['accent']}; }}
        QComboBox::drop-down {{ border: none; }}
        QComboBox QAbstractItemView {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            selection-background-color: {c['accent']};
            selection-color: {c['text_on_accent']};
            border: 1px solid {c['border']};
        }}
    """


def _spin_style(c: dict) -> str:
    return f"""
        QSpinBox {{
            background-color: {c['surface_alt']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
            padding: 3px 6px;
            outline: none;
        }}
        QSpinBox:hover {{ border-color: {c['accent']}; }}
        QSpinBox::up-button, QSpinBox::down-button {{ width: 18px; }}
    """


def _checkbox_style(c: dict) -> str:
    return f"""
        QCheckBox {{
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
            color: {c['text_primary']};
            border: none;             /* Kills the inherited border from the panel */
            background: transparent;  /* Kills the inherited background */
            outline: none;            /* Kills the focus dotted line */
            padding: 0px;              /* Removes extra padding around the checkbox */
            spacing: 0px;             /* Space between the checkbox and the label */
        }}
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border: 2px solid {c['border']};
            border-radius: 4px;
            background-color: {c['surface_alt']};
        }}
        QCheckBox::indicator:checked {{
            background-color: {c['accent']};
            border-color: {c['accent']};
        }}
    """


def _table_style(c: dict) -> str:
    return f"""
        QTableWidget {{
            background-color: {c['surface']};
            color: {c['text_primary']};
            gridline-color: {c['border']};
            border: 1px solid {c['border']};
            border-radius: 6px;
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
        }}
        QHeaderView::section {{
            background-color: {c['surface_alt']};
            color: {c['text_secondary']};
            font-family: "Segoe UI", sans-serif;
            font-size: 12px;
            font-weight: bold;
            border: none;
            border-bottom: 2px solid {c['border']};
            padding: 6px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        QTableWidget::item {{
            padding: 4px 8px;
        }}
        QTableWidget::item:selected {{
            background-color: {c['accent']};
            color: {c['text_on_accent']};
        }}
        QScrollBar:vertical {{
            background: {c['surface_alt']};
            width: 8px;
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical {{
            background: {c['border']};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::handle:vertical:hover {{ background: {c['accent']}; }}
        QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}
        QScrollBar:horizontal {{
            background: {c['surface_alt']};
            height: 8px;
            border-radius: 4px;
        }}
        QScrollBar::handle:horizontal {{
            background: {c['border']};
            border-radius: 4px;
            min-width: 30px;
        }}
        QScrollBar::handle:horizontal:hover {{ background: {c['accent']}; }}
    """


def _divider(c: dict) -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFixedHeight(1)
    line.setStyleSheet(f"background-color: {c['border']}; border: none;")
    return line


# ─── Main Window ─────────────────────────────────────────────────────────────

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
    date_label: QLabel
    github: QPushButton
    help_button: QPushButton
    theme_button: QPushButton
    hlayout: QHBoxLayout

    def __init__(self):
        super().__init__()
        self._dark_mode = True
        self._palette = DARK

        self.init_window()
        self.create_title_bar()
        self.create_block_select()
        self.create_attendance_list()
        self.create_actions_list()

        # ── Attendance panel wrapper ──────────────────────────────────────────
        self.attendance_wrapper = QWidget()
        dummy_layout = QHBoxLayout(self.attendance_wrapper)
        dummy_layout.setContentsMargins(0, 0, 0, 0)
        dummy_layout.addWidget(self.attendance_panel)
        self.attendance_wrapper.setMaximumWidth(700)

        # ── Central row ───────────────────────────────────────────────────────
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        horizontal_layout.setSpacing(16)
        horizontal_layout.addWidget(self.block_select)
        horizontal_layout.addWidget(self.attendance_wrapper)
        horizontal_layout.addWidget(self.right_panel)
        horizontal_layout.setStretch(1, 1)  # Makes the middle panel (index 1) expand
        self.attendance_wrapper.setMaximumWidth(16777215)  # Remove the 700px limit

        central_widget = QWidget()
        central_widget.setLayout(horizontal_layout)

        # ── Bottom bar ────────────────────────────────────────────────────────
        self.create_help_button()
        self.create_github_link()
        # self.create_theme_toggle()
        self.create_date_display()

        left_layout = QHBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        left_layout.addWidget(self.date_label)

        right_layout = QHBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        right_layout.setSpacing(8)
        # right_layout.addWidget(self.theme_button)
        right_layout.addWidget(self.help_button)
        right_layout.addWidget(self.github)

        bottom_bar = QHBoxLayout()
        bottom_bar.addLayout(left_layout)
        bottom_bar.addLayout(right_layout)

        # ── Root layout ───────────────────────────────────────────────────────
        self.vlayout = QVBoxLayout()
        self.vlayout.setSpacing(12)
        self.vlayout.setContentsMargins(16, 12, 16, 10)
        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addWidget(_divider(self._palette))
        self.vlayout.addWidget(central_widget)
        self.vlayout.addLayout(bottom_bar)

        self.dummy_widget = QWidget()
        self.dummy_widget.setLayout(self.vlayout)
        self.setCentralWidget(self.dummy_widget)

        # ... (near the end of __init__)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)  # MainWindow takes focus on click
        self.dummy_widget.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        # Apply to your three main columns
        self.block_select.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.attendance_wrapper.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.right_panel.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self._apply_theme()

    # ─── Window init ─────────────────────────────────────────────────────────

    def init_window(self):
        self.setWindowTitle("Attendance & Marks Sheet Generator")
        self.setMinimumSize(1240, 640)
        icon = QIcon(resource_path("assets\\icon1.png"))
        self.setWindowIcon(icon)

    # ─── Theme ───────────────────────────────────────────────────────────────

    def _apply_theme(self):
        c = self._palette

        # Root background
        self.dummy_widget.setStyleSheet(f"background-color: {c['bg']};")

        # Title bar
        self._title_label.setStyleSheet(_label_style(c, size=20, bold=True))

        # Block-select panel
        self.block_select.setStyleSheet(
            f"background-color: {c['surface']}; border-radius: 8px; border: 1px solid {c['border']};"
        )
        self._class_label.setStyleSheet(_label_style(c, size=11, secondary=True))
        self.class_dropdown.setStyleSheet(_combo_style(c))
        for btn in (self.temp_attendance_button, self.attendance_button,
                    self.marks_button, self.attendance_marks_button):
            btn.setStyleSheet(_btn_style(c, "ghost"))
        self.attendance_marks_button.setStyleSheet(_btn_style(c, "accent"))

        # Attendance panel
        self.attendance_wrapper.setStyleSheet(
            f"background-color: {c['surface']}; border-radius: 8px; border: 1px solid {c['border']};"
        )
        for btn in (self.load_button, self.save_button, self.add_button, self.remove_button):
            btn.setStyleSheet(_btn_style(c, "ghost"))
        self.table.setStyleSheet(_table_style(c))

        # Right panel
        self.right_panel.setStyleSheet(
            f"background-color: {c['surface']}; border-radius: 8px; border: 1px solid {c['border']};"
        )
        for lbl in (self._att_section_label, self._marks_section_label):
            lbl.setStyleSheet(_label_style(c, size=13, bold=True))
        for lbl in self._field_labels:
            lbl.setStyleSheet(_label_style(c, size=13))
        for cb in (self.midsem_checkbox, self.missed_midsem_checkbox,
                   self.missed_quiz_checkbox, self.endsem_checkbox):
            cb.setStyleSheet(_checkbox_style(c))
        for sb in (self.num_days_spinner, self.quiz_spinbox,
                   self.assignments_spinbox, self.experiments_spinbox):
            sb.setStyleSheet(_spin_style(c))
        self.endsem_dropdown.setStyleSheet(_combo_style(c))

        # Bottom bar
        self.date_label.setStyleSheet(_label_style(c, size=12, secondary=True))
        for btn in (self.help_button, self.github, self.theme_button):
            self.theme_button.setStyleSheet(_theme_btn_style(c))

        # Divider
        # Re-colour existing dividers isn't trivial; simpler to just set bg on root
        self.dummy_widget.update()

    def _show_pdf_success(self, file_name):

        # 1. Dialog Initialization
        dialog = QDialog(self)
        dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Start fully transparent to prevent the "flicker"
        dialog.setWindowOpacity(0.0)

        # 2. Main Container (Visual Rectangle)
        container = QFrame(dialog)
        container.setObjectName("SuccessContainer")
        container.setFixedSize(440, 200)
        # Using #ID selector to ensure internal widgets don't inherit borders
        container.setStyleSheet(f"""
            QFrame#SuccessContainer {{
                background-color: {self._palette['surface']};
                border: 1px solid {self._palette['border']};
                border-radius: 14px;
            }}
            QLabel {{ border: none; background: transparent; }}
        """)

        # 3. Z-Depth Shadow Effect
        shadow = QGraphicsDropShadowEffect(dialog)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 150))
        container.setGraphicsEffect(shadow)

        # 4. Layouts & Content
        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 28, 28, 20)
        layout.setSpacing(10)

        # Success Title
        title = QLabel("PDF generated successfully!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            color: {self._palette['text_primary']}; 
            font-family: 'Segoe UI', 'SF Pro Display', sans-serif; 
            font-size: 19px; 
            font-weight: 600;
        """)

        # File Path (Muted/Grayed)
        path_label = QLabel(file_name)
        path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        path_label.setWordWrap(True)
        path_label.setStyleSheet(f"color: {self._palette['text_secondary']}; font-family: 'Segoe UI'; font-size: 11px;")

        # 5. Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        # OK/Dismiss Button (Discouraged style: underlined, no bg)
        ok_btn = QPushButton("Dismiss")
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        ok_btn.setStyleSheet(f"""
            QPushButton {{ 
                background: transparent; 
                color: {self._palette['text_secondary']}; 
                border: none; 
                border-bottom: 1px solid {self._palette['text_secondary']}; 
                font-size: 13px; 
            }} 
            QPushButton:hover {{ 
                color: {self._palette['text_primary']}; 
                border-bottom: 1px solid {self._palette['text_primary']}; 
            }}
        """)

        # Open PDF Button (Primary action: accent bg)
        open_btn = QPushButton("Open PDF")
        open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        open_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        open_btn.setFixedSize(130, 38)
        open_btn.setStyleSheet(f"""
            QPushButton {{ 
                background-color: {self._palette['accent']}; 
                color: {self._palette['text_on_accent']}; 
                border-radius: 8px; 
                font-weight: bold; 
                font-size: 14px; 
                border: none; 
            }} 
            QPushButton:hover {{ 
                background-color: {self._palette['accent_hover']}; 
            }}
        """)

        btn_layout.addStretch()
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(open_btn)

        layout.addWidget(title)
        layout.addWidget(path_label)
        layout.addStretch()
        layout.addLayout(btn_layout)

        # 6. Assembly
        outer_layout = QVBoxLayout(dialog)
        # The 30px margin provides the "bleed" space for the shadow
        outer_layout.setContentsMargins(30, 30, 30, 30)
        outer_layout.addWidget(container)

        # 7. Animation Logic
        self.fade_anim = QPropertyAnimation(dialog, b"windowOpacity")
        self.fade_anim.setDuration(350)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # CRITICAL FIX: Ensure full opacity on finish
        self.fade_anim.finished.connect(lambda: dialog.setWindowOpacity(1.0))

        self.slide_anim = QPropertyAnimation(container, b"pos")
        self.slide_anim.setDuration(450)
        # Starts 20px lower (at y=50) and slides up to its final y=30 position within the margins
        self.slide_anim.setStartValue(QPoint(30, 50))
        self.slide_anim.setEndValue(QPoint(30, 30))
        self.slide_anim.setEasingCurve(QEasingCurve.Type.OutBack)

        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.fade_anim)
        self.anim_group.addAnimation(self.slide_anim)

        # Interaction Logic
        def handle_open():
            dialog.accept()
            try:
                if sys.platform == "win32":
                    os.startfile(file_name)
                elif sys.platform == "darwin":
                    subprocess.call(["open", file_name])
                else:
                    subprocess.call(["xdg-open", file_name])
            except Exception as e:
                print(f"Error: {e}")

        open_btn.clicked.connect(handle_open)
        ok_btn.clicked.connect(dialog.reject)

        # Start and show
        dialog.show()
        self.anim_group.start()
        dialog.exec()

    def create_theme_toggle(self):

        if not hasattr(self, 'theme_button'):
            self.theme_button = QPushButton()
            self.theme_button.setToolTip("Toggle Light / Dark Mode")
            self.theme_button.setFixedSize(30, 30)
            self.theme_button.clicked.connect(self._toggle_theme)
            self.theme_button.setStyleSheet(_icon_btn_style(self._palette))

        # Update the icon based on current theme
        color = 'light' if self._dark_mode else 'dark'
        try:
            # Use forward slashes for cross-platform compatibility
            icon_path = resource_path(f"assets/theme-{color}.png")
            self.theme_button.setIcon(QIcon(icon_path))
            self.theme_button.setIconSize(QSize(16, 16))
        except Exception:
            self.theme_button.setText("GH")

    def _toggle_theme(self):
        self._dark_mode = not self._dark_mode
        self._palette = DARK if self._dark_mode else LIGHT
        self.create_github_link()
        self.create_help_button()
        self.create_theme_toggle()
        self._apply_theme()

    # ─── Title bar ───────────────────────────────────────────────────────────

    def create_title_bar(self):
        image = QLabel()
        pixmap = QPixmap(resource_path("assets\\icon1.png"))
        if not pixmap.isNull():
            image.setPixmap(pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation))
        image.setFixedSize(40, 40)
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._title_label = QLabel("Attendance / Marks Sheet Generator")
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.hlayout = QHBoxLayout()
        self.hlayout.setSpacing(10)
        self.hlayout.addWidget(image)
        self.hlayout.addWidget(self._title_label)
        self.hlayout.addStretch()
        self.create_theme_toggle()
        self.hlayout.addWidget(self.theme_button)

    # ─── Block-select panel ──────────────────────────────────────────────────

    def create_block_select(self):
        self._class_label = QLabel("CLASS TYPE")
        self._class_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.class_dropdown = QComboBox()
        self.class_dropdown.addItems(["Theory", "Lab"])
        self.class_dropdown.setMinimumHeight(32)
        self.class_dropdown.currentIndexChanged.connect(self.on_class_dropdown_changed)

        top_layout = QVBoxLayout()
        top_layout.setSpacing(6)
        top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        top_layout.addWidget(self._class_label)
        top_layout.addWidget(self.class_dropdown)

        # Action buttons
        self.temp_attendance_button = QPushButton("Temp Attendance")
        self.attendance_button = QPushButton("Attendance")
        self.marks_button = QPushButton("Marks")
        self.attendance_marks_button = QPushButton("Attendance + Marks")

        for btn in (self.temp_attendance_button, self.attendance_button,
                    self.marks_button, self.attendance_marks_button):
            btn.setMinimumHeight(36)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.temp_attendance_button.clicked.connect(self.on_temp_attendance_button_clicked)
        self.attendance_button.clicked.connect(self.on_attendance_button_clicked)
        self.marks_button.clicked.connect(self.on_marks_button_clicked)
        self.attendance_marks_button.clicked.connect(self.on_attendance_marks_button_clicked)

        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(8)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        for btn in (self.temp_attendance_button, self.attendance_button,
                    self.marks_button, self.attendance_marks_button):
            btn_layout.addWidget(btn)

        block_layout = QVBoxLayout()
        block_layout.setContentsMargins(12, 12, 12, 12)
        block_layout.addLayout(top_layout)
        block_layout.addStretch()
        block_layout.addLayout(btn_layout)

        self.block_select = QWidget()
        self.block_select.setFixedWidth(200)
        self.block_select.setLayout(block_layout)

    # ─── Attendance list panel ───────────────────────────────────────────────

    def create_attendance_list(self):
        # Toolbar buttons
        self.load_button = QPushButton("Load CSV")
        self.save_button = QPushButton("Save CSV")
        self.add_button = QPushButton("Add Row")
        self.remove_button = QPushButton("Remove Row")

        self.load_button.setToolTip("Load student list from a CSV file")
        self.save_button.setToolTip("Save current list to a CSV file")
        self.add_button.setToolTip("Insert a new row below selection")
        self.remove_button.setToolTip("Delete selected row")

        for btn in (self.load_button, self.save_button, self.add_button, self.remove_button):
            btn.setMinimumHeight(30)

        self.load_button.clicked.connect(self.on_load_button_pressed)
        self.save_button.clicked.connect(self.on_save_button_pressed)
        self.add_button.clicked.connect(self.on_add_button_pressed)
        self.remove_button.clicked.connect(self.on_remove_button_pressed)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)
        toolbar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        for btn in (self.load_button, self.save_button, self.add_button, self.remove_button):
            toolbar.addWidget(btn)
        toolbar.addStretch()

        # Table
        self.table = QTableWidget()
        self.table.setRowCount(64)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Reg. No.", "Name"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setFixedHeight(36)
        self.table.horizontalHeader().setDefaultSectionSize(160)
        self.table.verticalHeader().setDefaultSectionSize(28)
        self.table.setAlternatingRowColors(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        layout.addLayout(toolbar)
        layout.addWidget(self.table)

        self.attendance_panel = QWidget()
        self.attendance_panel.setLayout(layout)

    # ─── Right panel (settings) ──────────────────────────────────────────────

    def create_actions_list(self):
        self._field_labels = []  # track for theme recolouring

        def field_label(text):
            lbl = QLabel(text)
            lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self._field_labels.append(lbl)
            return lbl

        def row(label_widget, control_widget):
            h = QHBoxLayout()
            h.setContentsMargins(0, 0, 0, 0)
            h.setSpacing(10)
            h.addWidget(label_widget)
            h.addStretch()
            # Pass AlignRight to force the control (checkbox/spinbox) to the edge
            h.addWidget(control_widget, alignment=Qt.AlignmentFlag.AlignRight)
            return h

        # ── Attendance section ────────────────────────────────────────────────
        self._att_section_label = QLabel("ATTENDANCE")

        self.num_days_spinner = QSpinBox()
        self.num_days_spinner.setRange(1, 100)
        self.num_days_spinner.setValue(1)
        self.num_days_spinner.setFixedWidth(70)

        att_row = row(field_label("Number of Classes"), self.num_days_spinner)

        # ── Marks section ─────────────────────────────────────────────────────
        self._marks_section_label = QLabel("MARKS")

        self.midsem_checkbox = QCheckBox()
        self.midsem_checkbox.setChecked(True)
        self.midsem_checkbox.checkStateChanged.connect(self.on_midsem_checkbox_changed)
        midsem_row = row(field_label("Mid Semester"), self.midsem_checkbox)

        self.missed_midsem_label = field_label("Missed Mid Semester")
        self.missed_midsem_checkbox = QCheckBox()
        self.missed_midsem_checkbox.setChecked(True)
        self.missed_midsem_checkbox.setEnabled(False)
        self.hlayout3 = row(self.missed_midsem_label, self.missed_midsem_checkbox)

        self.quiz_label = field_label("Quiz")
        self.quiz_spinbox = QSpinBox()
        self.quiz_spinbox.setRange(0, 5)
        self.quiz_spinbox.setFixedWidth(70)

        self.experiments_spinbox = QSpinBox()
        self.experiments_spinbox.setRange(0, 12)
        self.experiments_spinbox.setFixedWidth(70)
        self.experiments_spinbox.setVisible(False)

        self.hlayout4 = QHBoxLayout()
        self.hlayout4.addWidget(self.quiz_label)
        self.hlayout4.addStretch()
        self.hlayout4.addWidget(self.quiz_spinbox)
        self.hlayout4.addWidget(self.experiments_spinbox)

        self.missed_quiz_label = field_label("Missed Quiz")
        self.missed_quiz_checkbox = QCheckBox()
        self.hlayout5 = row(self.missed_quiz_label, self.missed_quiz_checkbox)

        self.assignments_label = field_label("Assignments")
        self.assignments_spinbox = QSpinBox()
        self.assignments_spinbox.setRange(0, 5)
        self.assignments_spinbox.setFixedWidth(70)
        self.hlayout6 = row(self.assignments_label, self.assignments_spinbox)

        self.endsem_dropdown = QComboBox()
        self.endsem_dropdown.addItems(["Written", "Project"])
        self.endsem_dropdown.setMinimumWidth(110)

        self.endsem_checkbox = QCheckBox()
        self.endsem_checkbox.setVisible(False)

        self.hlayout7 = QHBoxLayout()
        self.hlayout7.addWidget(field_label("End Semester"))
        self.hlayout7.addStretch()
        self.hlayout7.addWidget(self.endsem_dropdown)
        self.hlayout7.addWidget(self.endsem_checkbox)

        # ── Assemble ──────────────────────────────────────────────────────────
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(self._att_section_label)
        layout.addLayout(att_row)
        layout.addSpacing(4)
        layout.addWidget(self._marks_section_label)
        layout.addLayout(midsem_row)
        layout.addLayout(self.hlayout3)
        layout.addLayout(self.hlayout4)
        layout.addLayout(self.hlayout5)
        layout.addLayout(self.hlayout6)
        layout.addLayout(self.hlayout7)

        self.right_panel = QWidget()
        self.right_panel.setMaximumWidth(380)
        self.right_panel.setMinimumWidth(260)
        self.right_panel.setLayout(layout)

    # ─── Bottom-bar widgets ──────────────────────────────────────────────────

    def create_help_button(self):

        if not hasattr(self, 'help_button'):
            self.help_button = QPushButton()
            self.help_button.setToolTip("Help / Getting Started")
            self.help_button.setFixedSize(30, 30)
            self.help_button.clicked.connect(self.on_help_button_clicked)

        # Update the icon based on current theme
        color = 'light' if self._dark_mode else 'dark'
        try:
            # Use forward slashes for cross-platform compatibility
            icon_path = resource_path(f"assets/help-{color}.png")
            self.help_button.setIcon(QIcon(icon_path))
            self.help_button.setIconSize(QSize(16, 16))
        except Exception:
            self.help_button.setText("?")

    def create_github_link(self):
        # Only create the button object if it hasn't been made yet
        if not hasattr(self, 'github'):
            self.github = QPushButton()
            self.github.setToolTip("Open GitHub Repository")
            self.github.setFixedSize(30, 30)
            self.github.clicked.connect(self.on_github_clicked)

        # Update the icon based on current theme
        color = 'light' if self._dark_mode else 'dark'
        try:
            # Use forward slashes for cross-platform compatibility
            icon_path = resource_path(f"assets/github-{color}.png")
            self.github.setIcon(QIcon(icon_path))
            self.github.setIconSize(QSize(16, 16))
        except Exception:
            self.github.setText("GH")

    def create_date_display(self):
        self.date_label = QLabel(QDate.currentDate().toString("dddd, dd MMM yyyy"))

    # ─── Events ──────────────────────────────────────────────────────────────

    def on_class_dropdown_changed(self, index):
        if index == 0:  # Theory
            self.num_days_spinner.setMaximum(100)

            if self.right_panel.layout().indexOf(self.hlayout3) == -1:
                self.right_panel.layout().insertLayout(5, self.hlayout3)
            self.missed_midsem_label.setVisible(True)
            self.missed_midsem_checkbox.setVisible(True)

            if self.experiments_spinbox.isVisible():
                self.quiz_label.setText("Quiz")
                self.quiz_spinbox.setVisible(True)
                self.experiments_spinbox.setVisible(False)

            if self.right_panel.layout().indexOf(self.hlayout5) == -1:
                self.right_panel.layout().insertLayout(7, self.hlayout5)
            self.missed_quiz_label.setVisible(True)
            self.missed_quiz_checkbox.setVisible(True)

            if self.right_panel.layout().indexOf(self.hlayout6) == -1:
                self.right_panel.layout().insertLayout(8, self.hlayout6)
            self.assignments_label.setVisible(True)
            self.assignments_spinbox.setVisible(True)

            self.endsem_dropdown.setVisible(True)
            self.endsem_checkbox.setVisible(False)

            for btn in (self.temp_attendance_button, self.attendance_button, self.marks_button):
                btn.setVisible(True)

        else:  # Lab
            self.num_days_spinner.setMaximum(20)

            self.right_panel.layout().removeItem(self.hlayout3)
            self.missed_midsem_label.setVisible(False)
            self.missed_midsem_checkbox.setVisible(False)

            self.quiz_label.setText("Experiments")
            self.quiz_spinbox.setVisible(False)
            self.experiments_spinbox.setVisible(True)

            self.right_panel.layout().removeItem(self.hlayout5)
            self.missed_quiz_label.setVisible(False)
            self.missed_quiz_checkbox.setVisible(False)

            self.right_panel.layout().removeItem(self.hlayout6)
            self.assignments_label.setVisible(False)
            self.assignments_spinbox.setVisible(False)

            self.endsem_dropdown.setVisible(False)
            self.endsem_checkbox.setVisible(True)

            for btn in (self.temp_attendance_button, self.attendance_button, self.marks_button):
                btn.setVisible(False)

    def on_midsem_checkbox_changed(self, state):
        self.missed_midsem_checkbox.setChecked(state == Qt.CheckState.Checked)

    def on_load_button_pressed(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if not file_name:
            return
        data_frame = pd.read_csv(file_name)
        self.table.setRowCount(len(data_frame))
        for row_index in range(len(data_frame)):
            for col_index in range(data_frame.shape[1]):
                item = QTableWidgetItem(str(data_frame.iloc[row_index, col_index]))
                self.table.setItem(row_index, col_index, item)

    def on_remove_button_pressed(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)

    def on_add_button_pressed(self):
        selected_row = self.table.currentRow()
        self.table.insertRow(selected_row + 1)

    def create_data_frame(self):
        data = []
        for row_index in range(self.table.rowCount()):
            row = []
            for col_index in range(self.table.columnCount()):
                item = self.table.item(row_index, col_index)
                row.append(item.text() if item else "")
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
        self._show_pdf_success(file_name)

    def on_attendance_button_clicked(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)")
        if not file_name:
            return
        pdf_workers.attendance_sheet_pdf.generate_attendance_sheet(
            self.create_data_frame(), self.num_days_spinner.value(), file_name)
        self._show_pdf_success(file_name)

    def on_marks_button_clicked(self):
        requirements_dict = {
            'Roll No.': (1, 10),
            'Reg. No.': (1, 40),
            'Name of Student': (1, 60),
            'M.S.': (self.midsem_checkbox.isChecked(), 10),
            'Missed M.S.': (self.missed_midsem_checkbox.isChecked(), 20),
            'Q': (self.quiz_spinbox.value(), 10),
            'Missed Q': (self.missed_quiz_checkbox.isChecked(), 15),
            'A': (self.assignments_spinbox.value(), 10),
            'Sessional': (1, 15),
            f'E.M. ({self.endsem_dropdown.currentText()})': (1, 20),
            'Total': (1, 15),
            'Grade': (1, 15),
        }
        file_name, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)")
        if not file_name:
            return
        pdf_workers.marks_sheet_pdf.generate_marks_sheet(self.create_data_frame(), requirements_dict, file_name)
        self._show_pdf_success(file_name)

    def on_attendance_marks_button_clicked(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save PDF File", "", "PDF Files (*.pdf)")
        if not file_name:
            return

        if self.class_dropdown.currentIndex() == 0:
            pdf_workers.attendance_sheet_pdf.generate_attendance_sheet(
                self.create_data_frame(), self.num_days_spinner.value(), 'a.pdf')

            requirements_dict = {
                'Roll No.': (1, 10),
                'Reg. No.': (1, 40),
                'Name of Student': (1, 60),
                'M.S.': (self.midsem_checkbox.isChecked(), 10),
                'Missed M.S.': (self.missed_midsem_checkbox.isChecked(), 20),
                'Q': (self.quiz_spinbox.value(), 10),
                'Missed Q': (self.missed_quiz_checkbox.isChecked(), 15),
                'A': (self.assignments_spinbox.value(), 10),
                'Sessional': (1, 15),
                f'E.M. ({self.endsem_dropdown.currentText()})': (1, 20),
                'Total': (1, 15),
                'Grade': (1, 15),
            }
            pdf_workers.marks_sheet_pdf.generate_marks_sheet(self.create_data_frame(), requirements_dict, 'm.pdf')
            pdf_workers.merger.merge_pdfs('a.pdf', 'm.pdf', file_name)
            os.remove('a.pdf')
            os.remove('m.pdf')
            self._show_pdf_success(file_name)

        elif self.class_dropdown.currentIndex() == 1:
            pdf_workers.lab_attendance.generate_attendance_sheet(
                self.create_data_frame(), self.num_days_spinner.value(), 'a.pdf')

            requirements_dict = {
                'Roll No.': (1, 10),
                'Reg. No.': (1, 38),
                'Name of Student': (1, 60),
            }
            for k in range(1, self.experiments_spinbox.value() + 1):
                requirements_dict[str(k)] = (1, 28)
            requirements_dict['Mid Sem'] = (self.midsem_checkbox.isChecked(), 28)
            requirements_dict['End Sem'] = (self.endsem_checkbox.isChecked(), 28)
            requirements_dict['Total'] = (1, 14)
            requirements_dict['Grade'] = (1, 14)

            pdf_workers.marks_sheet_pdf.generate_marks_sheet(self.create_data_frame(), requirements_dict, 'm.pdf')
            pdf_workers.merger.merge_pdfs('a.pdf', 'm.pdf', file_name)
            os.remove('a.pdf')
            os.remove('m.pdf')
            self._show_pdf_success(file_name)

    def on_help_button_clicked(self):
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFrame, QGraphicsDropShadowEffect, QScrollArea
        from PySide6.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QPoint
        from PySide6.QtGui import QColor

        dialog = QDialog(self)
        dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        dialog.setWindowOpacity(0.0)

        # Main Container
        container = QFrame(dialog)
        container.setObjectName("HelpContainer")
        container.setFixedSize(600, 500)
        container.setStyleSheet(f"""
            QFrame#HelpContainer {{
                background-color: {self._palette['surface']};
                border: 1px solid {self._palette['border']};
                border-radius: 16px;
            }}
        """)

        # Shadow
        shadow = QGraphicsDropShadowEffect(dialog)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 180))
        container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 20)

        # Header
        header = QLabel("How to use Register Generator")
        header.setStyleSheet(
            f"color: {self._palette['text_primary']}; font-family: 'Segoe UI', sans-serif; font-size: 22px; font-weight: bold; border: none;")
        layout.addWidget(header)
        layout.addSpacing(15)

        # Scrollable Content Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)
        scroll_layout.setContentsMargins(0, 0, 10, 0)

        # Parse help.txt and create cards
        try:
            with open(resource_path("assets/help.txt"), "r") as f:
                lines = f.readlines()
                for line in lines:
                    if "|" in line:
                        title_text, desc_text = line.split("|")

                        # Card Widget
                        card = QFrame()
                        card.setStyleSheet(
                            f"background-color: {self._palette['surface_alt']}; border-radius: 10px; border: 1px solid {self._palette['border']};")
                        card_layout = QVBoxLayout(card)

                        c_title = QLabel(title_text.strip())
                        c_title.setStyleSheet(f"color: {self._palette['accent']}; font-weight: bold; font-size: 14px; border: none;")

                        c_desc = QLabel(desc_text.strip())
                        c_desc.setWordWrap(True)
                        c_desc.setStyleSheet(f"color: {self._palette['text_secondary']}; font-size: 13px; border: none;")

                        card_layout.addWidget(c_title)
                        card_layout.addWidget(c_desc)
                        scroll_layout.addWidget(card)
        except Exception:
            error_lbl = QLabel("Help file not found in assets/help.txt")
            scroll_layout.addWidget(error_lbl)

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Footer Button
        btn_layout = QHBoxLayout()
        close_btn = QPushButton("Got it")
        close_btn.setFixedSize(100, 36)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._palette['accent']};
                color: {self._palette['text_on_accent']};
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{ background-color: {self._palette['accent_hover']}; }}
        """)
        close_btn.clicked.connect(dialog.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        # Shadow bleed margins
        outer_layout = QVBoxLayout(dialog)
        outer_layout.setContentsMargins(40, 40, 40, 40)
        outer_layout.addWidget(container)

        # Animation
        fade = QPropertyAnimation(dialog, b"windowOpacity")
        fade.setDuration(300)
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)
        fade.setEasingCurve(QEasingCurve.Type.OutCubic)

        slide = QPropertyAnimation(container, b"pos")
        slide.setDuration(400)
        slide.setStartValue(QPoint(40, 70))
        slide.setEndValue(QPoint(40, 40))
        slide.setEasingCurve(QEasingCurve.Type.OutBack)

        anim_group = QParallelAnimationGroup(dialog)
        anim_group.addAnimation(fade)
        anim_group.addAnimation(slide)

        dialog.show()
        anim_group.start()
        dialog.exec()

    @staticmethod
    def on_github_clicked():
        import webbrowser
        webbrowser.open("https://github.com/RuthvikSaiKumar/AmritaAttendanceRegister")
