import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QVBoxLayout
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from qfluentwidgets import CheckBox, MessageBox
from .qiandao import Ui_MainWindow
from PyQt5 import QtCore  # 添加这一行

from .ClassWidgets.base import PluginBase, SettingsBase, PluginConfig  # 导入CW的基类

class Plugin(PluginBase):  # 插件类
    def __init__(self, cw_contexts, method):  # 初始化
        super().__init__(cw_contexts, method)  # 调用父类初始化方法
        """
        插件初始化，插件被执行时将会执行此部分的代码
        """


    def execute(self):  # 自启动执行部分
        """
        当 Class Widgets启动时，将会执行此部分的代码
        """
        self.main_window = MyMainForm()
        self.main_window.show()
        pass

    def update(self, cw_contexts):  # 自动更新部分（每秒更新）
        super().update(cw_contexts)  # 获取最新接口
        """
        Class Widgets 本体会每1秒更新一次状态，同时也会调用此部分的代码。
        可在此部分插入动态更新的内容
        """
        pass


class Settings(SettingsBase):  # 设置类
    def __init__(self, plugin_path, parent=None):  # 初始化
        super().__init__(plugin_path, parent)
        """
        在这里写设置页面
        """
        # 其他代码……

class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.students = []
        self.signed_students = []

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)


        self.pushButton_4.clicked.connect(self.import_students)
        self.pushButton_3.clicked.connect(self.open_signin_dialog)
        self.pushButton.clicked.connect(self.closewidget)
        self.pushButton_2.clicked.connect(self.closewidget)

        self.widget_4_layout = QVBoxLayout(self.widget_4)

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

    def import_students(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择学生名单文件", "", "文本文件 (*.txt)")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.students = [line.strip().split(".", 1)[-1] for line in f.readlines() if "." in line]

                self.signed_students.clear()
                self.update_checkboxes()
                self.peoplenum.setText(str(len(self.students)))
                self.textEdit_2.setText("\n".join(self.students))

                MessageBox("导入成功", f"成功导入 {len(self.students)} 名学生。", self.centralwidget).exec()

            except Exception as e:
                QMessageBox.critical(self, "错误", str(e))

    def update_checkboxes(self):
        try:
            for i in reversed(range(self.grid_layout.count())):
                widget = self.grid_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            self.checkboxes = []
            self.cols = 4  # 每行最多 4 个
            for index, student in enumerate(self.students):
                cb = CheckBox(student)
                cb.setChecked(student in self.signed_students)

                # 先清除旧信号再连接新信号
                cb.clicked.connect(lambda checked, s=student: self.toggle_signin(s, checked))

                row, col = divmod(index, self.cols)
                self.grid_layout.addWidget(cb, row, col)
                self.checkboxes.append(cb)

        except Exception as e:
            QMessageBox.critical(self, "错误", str(e))

    def toggle_signin(self, student, checked):
        if checked:
            if student not in self.signed_students:
                self.signed_students.append(student)
        else:
            if student in self.signed_students:
                self.signed_students.remove(student)

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
        self.animation.setEndValue(QRect(0, -620, 1341, 631))
        self.animation.setEasingCurve(QEasingCurve.OutExpo)
        self.animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())