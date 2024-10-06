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
# todo: add missed midsem check box / make it compulsory
# todo: add a row for max marks in marks sheet pdf
# todo: add temporary attendance or full attendance button for generating

