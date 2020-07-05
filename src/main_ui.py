import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QApplication, QDesktopWidget,
                             QCalendarWidget, QLabel, QWidget,
                             QMessageBox)
from PyQt5.QtGui import QIcon

from calculator_ui import Calculator

class Example(QMainWindow):

    updateUI = False
    number = 1

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.resize(1200, 800)
        self.center()

        self.setWindowTitle('人民日报——今日新闻分析')

        exitAction = QAction(QIcon('../img/tuichu.png'), '退出', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('退出')
        exitAction.triggered.connect(self.close)

        calculatorAction = QAction(QIcon('../img/rili.png'), '日历', self)
        calculatorAction.setShortcut('Ctrl+C')
        calculatorAction.setStatusTip('日历')
        calculatorAction.triggered.connect(self.calculator)

        getAction = QAction(QIcon('../img/huoqu.png'), '获取今日数据', self)
        getAction.setShortcut('Ctrl+G')
        getAction.setStatusTip('获取今日数据')
        getAction.triggered.connect(self.getdata)

        analyAction = QAction(QIcon('../img/analysis.png'), '文本预处理', self)
        analyAction.setShortcut('Ctrl+A')
        analyAction.setStatusTip('文本预处理')
        analyAction.triggered.connect(self.close)

        titleAction = QAction(QIcon('../img/title.png'), '列出今日标题', self)
        titleAction.setShortcut('Ctrl+T')
        titleAction.setStatusTip('列出今日标题')
        titleAction.triggered.connect(self.close)

        wordsAction = QAction(QIcon('../img/words.png'), '词频统计', self)
        wordsAction.setShortcut('Ctrl+W')
        wordsAction.setStatusTip('词频统计')
        wordsAction.triggered.connect(self.close)

        menubar = self.menuBar()
        ToolMenu = menubar.addMenu('&Tools')
        ToolMenu.addAction(exitAction)

        toolbar = self.addToolBar('')
        toolbar.addAction(exitAction)
        toolbar.addAction(calculatorAction)
        toolbar.addAction(getAction)
        toolbar.addAction(analyAction)
        toolbar.addAction(titleAction)
        toolbar.addAction(wordsAction)

        self.statusBar()
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        # 获取窗口
        qr = self.frameGeometry()
        # 获取屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def calculator(self):
        number = 2
        print(number)

    def getdata(self):
        number = 3
        print(number)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    mainui = Example()

    cal = Calculator()

    sys.exit(app.exec_())
