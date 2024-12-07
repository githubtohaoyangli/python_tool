import sys
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QVBoxLayout

class MyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("点击确定后执行函数")

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)  # 点击“确定”按钮触发accept信号
        button_box.rejected.connect(self.reject)  # 点击“取消”按钮触发reject信号

        layout = QVBoxLayout()
        layout.addWidget(button_box)
        self.setLayout(layout)

    def accept(self):
        print("点击了确定按钮，执行相应的函数")
        # 在这里编写执行函数的代码

app = QApplication(sys.argv)
dialog = MyDialog()
dialog.show()
sys.exit(app.exec())
