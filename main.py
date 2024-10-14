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
# todo: add temporary attendance or full attendance button for generating
