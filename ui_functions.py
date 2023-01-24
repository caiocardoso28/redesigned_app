from main import MainWindow, ICONS, DISABLED
from PyQt5 import QtCore
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import QIcon


class UIFunctions(MainWindow):

    def toggleMenu(self, maxWidth, enable):

        button_text = []
        if enable:

            # GET WIDTH
            width = self.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 100

            # SET MAX WIDTH
            if width == 100:
                widthExtended = maxExtend
                for button in self.buttons:
                    button.setIcon(QIcon())
                self.btn_page_5.setText('Profile Info')
                self.btn_page_1.setText('Load File')
                self.btn_page_2.setText('BI Workspace')
                self.btn_page_3.setText('AE Collaboration')
                self.btn_page_4.setText('Reach Out')
                self.Btn_Toggle.setIcon(QIcon())
                self.Btn_Toggle.setText('Menu')
            else:
                widthExtended = standard
                i = 0
                for button in self.buttons:
                    if len(button.text()) >= 8:
                        if button.isEnabled():
                            button.setText('')
                            button.setIcon(QIcon(ICONS[i]))
                        else:
                            button.setText('')
                            button.setIcon(QIcon(DISABLED[i]))
                    i += 1
                    self.Btn_Toggle.setText('')
                    self.Btn_Toggle.setIcon(QIcon('iconz\\menu_reg.png'))
            # ANIMATION
            self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()