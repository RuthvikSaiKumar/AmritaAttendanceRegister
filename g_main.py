from PySide6.QtWidgets import QApplication
import ui
import sys
import qdarktheme

qdarktheme.enable_hi_dpi()
app = QApplication(sys.argv)
qdarktheme.setup_theme('auto')
window = ui.MainWindow()

window.show()
app.exec()


# todo: give meaningful names to the classes, functions, and variables
