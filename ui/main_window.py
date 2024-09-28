from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_window()

    def on_close(self, event):
        ...

    def on_resize(self, event):
        ...

    def init_window(self):
        self.setWindowTitle("Attendance/Marks Register Generator")
        self.setMinimumSize(900, 600)
        self.setWindowIcon(QIcon("assets/icon_with_background.png"))
        self.setStyleSheet("""
            background-color: #DDFFC7;
        """)
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

    # def create_toolbar(self):
    #     self.toolbar = self.addToolBar("Toolbar")
    #     self.toolbar.setStyleSheet("""
    #         background-color: #66B032;
    #         height: 30px;
    #         font-family: Century Gothic;
    #         font-weight: bold;
    #         color: #DDFFC7;
    #         font-size: 16px;
    #     """)
    #     self.toolbar.setMovable(False)
    #     self.toolbar.setFloatable(False)
    #     self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
    #     self.toolbar.setIconSize(QSize(25, 25))
    #
    #     back_button = self.toolbar.addAction(QIcon("assets/back.png"), "Back")
    #     back_button.setToolTip("Back to Profile Selection")
    #     back_button.triggered.connect(self.switch_to_scene1)
    #
    #     add_button = self.toolbar.addAction(QIcon("assets/add.png"), "Add")
    #     add_button.setToolTip("Add Password (Ctrl+N)")
    #     add_button.triggered.connect(self.add_password)
    #
    #     remove_button = self.toolbar.addAction(QIcon("assets/remove.png"), "Remove")
    #     remove_button.setToolTip("Remove Password (Ctrl+R)")
    #     remove_button.triggered.connect(self.remove_password)
    #
    #     edit_button = self.toolbar.addAction(QIcon("assets/edit.png"), "Edit")
    #     edit_button.setToolTip("Edit Password (Ctrl+E)")
    #     edit_button.triggered.connect(self.edit_password)
    #
    #     save_button = self.toolbar.addAction(QIcon("assets/save.png"), "Save")
    #     save_button.setToolTip("Save Passwords (Ctrl+S)")
    #     save_button.triggered.connect(self.on_save_button_clicked)
    #
    #     search_button = self.toolbar.addAction(QIcon("assets/search.png"), "Search")
    #     search_button.setToolTip("Search Password (Ctrl+F)")
    #     search_button.triggered.connect(self.search_password)
    #
    #     copy_button = self.toolbar.addAction(QIcon("assets/copy.png"), "Search")
    #     copy_button.setToolTip("Copy Password (Ctrl+C)")
    #     copy_button.triggered.connect(self.copy_password)
    #
    #     edit_master_password = self.toolbar.addAction(QIcon("assets/edit_master.png"), "Edit Master Password")
    #     edit_master_password.setToolTip("Edit Master Password")
    #     edit_master_password.triggered.connect(self.edit_master_password)
    #
    #     reload_passwords = self.toolbar.addAction(QIcon("assets/refresh.png"), "Reload Passwords")
    #     reload_passwords.setToolTip("Reload Passwords")
    #     reload_passwords.triggered.connect(self.refresh_passwords)
    #
    #     add_button.setShortcut("Ctrl+N")
    #     remove_button.setShortcut("Ctrl+R")
    #     edit_button.setShortcut("Ctrl+E")
    #     save_button.setShortcut("Ctrl+S")
    #     search_button.setShortcut("Ctrl+F")
    #     copy_button.setShortcut("Ctrl+C")

    # def create_title_bar(self):
    #     image = QLabel()
    #     image.setPixmap(QPixmap("assets/icon.png"))
    #     image.setAlignment(Qt.AlignmentFlag.AlignCenter)
    #     image.setScaledContents(True)
    #     image.setMinimumSize(50, 50)
    #     image.setMaximumSize(50, 50)
    #
    #     title = QLabel("Password Manager")
    #     title.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    #     title.setStyleSheet("""
    #         font-family: Monospace;
    #         font-size: 24px;
    #         color: #375F1B;
    #         font-weight: bold;
    #     """)
    #
    #     self.title_hlayout = QHBoxLayout()
    #     self.title_hlayout.addWidget(image)
    #     self.title_hlayout.addSpacing(25)
    #     self.title_hlayout.addWidget(title)

    # def create_bottom_bar(self):
    #     self.create_help_button()
    #     self.create_switch_theme_button()
    #     self.create_github_link()
    #
    #     self.bottom_bar = QHBoxLayout()
    #     self.bottom_bar.setAlignment(Qt.AlignmentFlag.AlignRight)
    #     self.bottom_bar.addWidget(self.switch_theme_button)
    #     self.bottom_bar.addWidget(self.help_button)
    #     self.bottom_bar.addWidget(self.github)
