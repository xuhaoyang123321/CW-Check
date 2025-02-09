import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QVBoxLayout
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from qfluentwidgets import MessageBox, PushButton, Dialog
from .qiandao import Ui_MainWindow
from PyQt5 import QtCore
from .ClassWidgets.base import PluginBase, SettingsBase, PluginConfig

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QVBoxLayout,QPushButton

from qfluentwidgets import CaptionLabel, CardWidget, PushButton, SmoothScrollArea, SubtitleLabel, SwitchButton, \
    TitleLabel
class Plugin(PluginBase):
    def __init__(self, cw_contexts, method):
        super().__init__(cw_contexts, method)
        self.app = QApplication(sys.argv)
        self.myWin = MyMainForm()
        self.myWin.show()

    def execute(self):
        sys.exit(self.app.exec_())

    def update(self, cw_contexts):
        super().update(cw_contexts)
        # 可以在这里添加动态更新的内容

class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.students = []
        self.signed_students = []


        self.setAttribute(Qt.WA_TranslucentBackground)
        self.animation = QPropertyAnimation(self.widget, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(QRect(20,20,0,651))
        self.animation.setEndValue(QRect(20,20,1341,651))
        self.animation.setEasingCurve(QEasingCurve.OutExpo)
        self.animation.start()
        self.move(300, 200)
        self.pushButton_5.clicked.connect(self.closewindows)
        self.pushButton_4.clicked.connect(self.import_students)
        self.pushButton_3.clicked.connect(self.open_signin_dialog)
        self.pushButton.clicked.connect(self.closewidget)
        self.pushButton_2.clicked.connect(self.closewidget)

        self.widget_4_layout = QVBoxLayout(self.widget_4)

    def closewindows(self):
        self.closeevent = Dialog("警告", "是否关闭签到系统？", self.centralwidget)
        self.closeevent.yesButton.setText("是的")
        self.closeevent.cancelButton.setText("取消哦宝宝~")

        if self.closeevent.exec():
            print('确认')
            self.close()
        else:
            print('取消')

    def import_students(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择学生名单文件", "", "文本文件 (*.txt)")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.students = [line.strip() for line in f.readlines() if line.strip()]

                self.signed_students.clear()
                self.update_buttons()
                self.peoplenum.setText(str(len(self.students)))
                self.textEdit_2.setText("\n".join(self.students))

                MessageBox("导入成功", f"成功导入 {len(self.students)} 名学生。", self.centralwidget).exec()

            except Exception as e:
                QMessageBox.critical(self, "错误", str(e))

    def update_buttons(self):
        try:
            for i in reversed(range(self.grid_layout.count())):
                widget = self.grid_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            self.buttons = []
            self.cols = 4  # 每行最多 4 个
            for index, student in enumerate(self.students):
                btn = PushButton(student)
                btn.setFixedSize(120, 36)
                self.update_button_style(btn, student in self.signed_students)
                btn.clicked.connect(lambda checked, s=student, b=btn: self.toggle_signin(s, b))

                row, col = divmod(index, self.cols)
                self.grid_layout.addWidget(btn, row, col)
                self.buttons.append(btn)
        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def update_button_style(self, btn, signed):
        if signed:
            btn.setText(f"{btn.text()}(已签到)")
            btn.setStyleSheet("background-color: #0078d7; color: white;border-radius:5px;")
        else:
            btn.setText(btn.text().replace("(已签到)", ""))
            btn.setStyleSheet("background-color: #f0f0f0; color: black;border-radius:5px;")

    def toggle_signin(self, student, btn):
        if student in self.signed_students:
            self.signed_students.remove(student)
            self.update_button_style(btn, False)
        else:
            self.signed_students.append(student)
            self.update_button_style(btn, True)

        self.update_signin_status()

    def confirm_signin(self):
        print("已签到:", self.signed_students)
        print("未签到:", [s for s in self.students if s not in self.signed_students])
        self.update_signin_status()

    def update_signin_status(self):
        self.textEdit.setText("\n".join(self.signed_students))
        self.textEdit_2.setText("\n".join([s for s in self.students if s not in self.signed_students]))
        self.qiandaonum.setText(str(len(self.signed_students)))

    def open_signin_dialog(self):
        if not self.students:
            MessageBox("警告", "请导入学生名单！", self.centralwidget).exec()
            return

        if self.widget_2.y() == 40:  # 确保不会重复动画
            return

        self.animation = QPropertyAnimation(self.widget_2, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(QRect(0, -620, 1341, 631))
        self.animation.setEndValue(QRect(0, 40, 1341, 631))
        self.animation.setEasingCurve(QEasingCurve.OutExpo)
        self.animation.start()

    def closewidget(self):
        self.animation = QPropertyAnimation(self.widget_2, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(QRect(0, 40, 1341, 631))
        self.animation.setEndValue(QRect(0, -650, 1341, 631))
        self.animation.setEasingCurve(QEasingCurve.OutExpo)
        self.animation.start()

    def mouseReleaseEvent(self, event):
        self.start_x = None
        self.start_y = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            super(MyMainForm, self).mousePressEvent(event)
            self.start_x = event.x()
            self.start_y = event.y()

    def mouseMoveEvent(self, event):
        try:
            super(MyMainForm, self).mouseMoveEvent(event)
            dis_x = event.x() - self.start_x
            dis_y = event.y() - self.start_y
            self.move(self.x() + dis_x, self.y() + dis_y)
        except:
            pass

class Settings(SettingsBase):
    def __init__(self, plugin_path, parent=None):
        super().__init__(plugin_path, parent)
        # 在这里写设置页面
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(688, 571)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(24, 24, 24, 0)
        self.verticalLayout_2.setSpacing(18)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.TitleLabel = TitleLabel(Form)
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout_2.addWidget(self.TitleLabel)
        self.SmoothScrollArea = SmoothScrollArea(Form)
        self.SmoothScrollArea.setStyleSheet("background: transparent; border: none")
        self.SmoothScrollArea.setWidgetResizable(True)
        self.SmoothScrollArea.setObjectName("SmoothScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 640, 514))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setSpacing(12)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setSpacing(3)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.SubtitleLabel_2 = SubtitleLabel(self.scrollAreaWidgetContents)
        self.SubtitleLabel_2.setText("")
        self.SubtitleLabel_2.setObjectName("SubtitleLabel_2")
        self.verticalLayout_7.addWidget(self.SubtitleLabel_2)
        self.CaptionLabel_10 = CaptionLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CaptionLabel_10.sizePolicy().hasHeightForWidth())
        self.CaptionLabel_10.setSizePolicy(sizePolicy)
        self.CaptionLabel_10.setText("")
        self.CaptionLabel_10.setWordWrap(True)
        self.CaptionLabel_10.setProperty("lightColor", QtGui.QColor(0, 0, 0, 150))
        self.CaptionLabel_10.setProperty("darkColor", QtGui.QColor(255, 255, 255, 200))
        self.CaptionLabel_10.setObjectName("CaptionLabel_10")
        self.verticalLayout_7.addWidget(self.CaptionLabel_10)
        self.CardWidget_4 = CardWidget(self.scrollAreaWidgetContents)
        self.CardWidget_4.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_4.setObjectName("CardWidget_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.CardWidget_4)
        self.horizontalLayout_6.setContentsMargins(16, 16, 16, 16)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton = PushButton(self.CardWidget_4)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_6.addWidget(self.pushButton)
        self.verticalLayout_7.addWidget(self.CardWidget_4)
        self.CardWidget_5 = CardWidget(self.scrollAreaWidgetContents)
        self.CardWidget_5.setMinimumSize(QtCore.QSize(0, 70))
        self.CardWidget_5.setObjectName("CardWidget_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.CardWidget_5)
        self.horizontalLayout_7.setContentsMargins(16, 16, 16, 16)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")

        self.verticalLayout_7.addWidget(self.CardWidget_5)
        self.verticalLayout_9.addLayout(self.verticalLayout_7)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setSpacing(3)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_9.addLayout(self.verticalLayout_12)
        self.blank = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.blank.setMinimumSize(QtCore.QSize(0, 25))
        self.blank.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.blank.setLineWidth(5)
        self.blank.setObjectName("blank")
        self.verticalLayout_9.addWidget(self.blank)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                           QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem)
        self.SmoothScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.SmoothScrollArea)
        self.pushButton.clicked.connect(self.start)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.TitleLabel.setText(_translate("Form", "Class Widgets签到设置"))
        self.pushButton.setText(_translate("Form", "打开签到程序"))


    def start(self):
        self.app = QApplication(sys.argv)
        self.myWin = MyMainForm()
        self.myWin.show()
