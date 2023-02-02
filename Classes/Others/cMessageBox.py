from re import X
import sys
import os
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QToolBar,
    QVBoxLayout, QWidget,QDialog,QFileDialog,QMessageBox)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtCore import Qt
class cMessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        
    def Notification(text):
        icon_Window = "Icons/warning.png"
        icon_Content = "Icons/input_error.png"
        msg_box = QMessageBox(QMessageBox.Information,'Notification',text,QMessageBox.Ok)
        msg_box.setIconPixmap(QPixmap(icon_Content))
        msg_box.setWindowIcon(QIcon(icon_Window))
        msg_box.exec()
# return in python
class cMessageBoxContent():
     def __init__(self, text):
        self.text = text
     def ErrorInputText():
        return cMessageBoxContent("Error Input. Please Check Again !")

