import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QDesktopWidget
from PyQt5.QtGui import QIcon


class Example(QMainWindow):

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

        getAction = QAction(QIcon('../img/huoqu.png'), '获取今日数据', self)
        getAction.setShortcut('Ctrl+G')
        getAction.setStatusTip('获取今日数据')
        getAction.triggered.connect(self.close)

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
        toolbar.addAction(getAction)
        toolbar.addAction(analyAction)
        toolbar.addAction(titleAction)
        toolbar.addAction(wordsAction)

        self.statusBar()
        self.show()

    def center(self):
        # 获取窗口
        qr = self.frameGeometry()
        # 获取屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
