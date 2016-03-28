"""
这是qt_main下面的子窗口，addgame
用来添加游戏的。

作者：向航
2015-12-15
"""
from PyQt5.QtWidgets import *

from qt_support import *


class AddGame(QWidget):

    def __init__(self, father, parent=None):
        self.father = father
        super(QWidget, self).__init__(parent)
        directory_label = QLabel('请选择文件：')
        directory_btn = QPushButton('...')
        name_label = QLabel('游戏名称：')
        self.name_edit = QLineEdit()
        confirm_btn = QPushButton('确认添加')
        self.dir = QLabel('.')

        layout = QGridLayout()
        layout.addWidget(name_label, 0, 0, 1, 4)
        layout.addWidget(self.name_edit, 1, 0, 1, 4)
        layout.addWidget(directory_label, 2, 0, 1, 1)
        layout.addWidget(directory_btn, 2, 3, 1, 1)
        layout.addWidget(self.dir, 3, 0, 1, 3)
        layout.addWidget(confirm_btn, 4, 3)

        directory_btn.clicked.connect(self.select_directory)
        confirm_btn.clicked.connect(self.confirm)

        self.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)
        self.setWindowTitle('添加游戏')

    def select_directory(self):
        _dir = QFileDialog.getOpenFileName(self, '选取文件')
        self.dir.setText(_dir[0])
        self.update()

    def confirm(self):
        game_name = self.name_edit.text()
        if game_name in self.father.games:
            QMessageBox.warning(self, '提示', '游戏已经添加！')
            return

        print('添加游戏 :', game_name, self.dir.text())
        # self.father.games.append([self.name_edit.text(), self.dir.text()])
        another_name = add_game_to_server(self.father.id, game_name)
        print(another_name)
        if another_name != "Error":
            self.father.games[game_name] = {'dir': self.dir.text(),
                                                        'time': 0,
                                                        'another_name': another_name}
            self.father.refresh()
            QMessageBox.information(self, '提示', '游戏添加成功！')
        else:
            QMessageBox.information(self, '注意', '游戏添加失败，游戏名称无法识别！')

        # 清除痕迹
        self.name_edit.clear()
        self.dir.setText('.')

