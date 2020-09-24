from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os.path


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self._myTasks = {}
        self.__initializeComponents()

    def __initializeComponents(self):
        self.setObjectName("MainWindow")
        self.setWindowTitle("PDF和图片转换器")
        self.__defaultFont = QFont()
        self.__defaultFont.setFamily("Microsoft YaHei UI")
        self.__defaultFont.setPointSize(18)
        self.setFont(self.__defaultFont)
        # =====centralwidget=====
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        # =====顶层=====
        topLayout = QHBoxLayout()
        topLayout.setObjectName("topLayout")
        # =====按钮框=====
        btnLayout = QVBoxLayout()
        btnLayout.setObjectName("btnLayout")
        btnWidget = QWidget(self.centralwidget)
        # =====按钮=====
        btnSP = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # =====fromPDF=====
        self.btnFromPDF = QPushButton(btnWidget)
        self.btnFromPDF.setSizePolicy(btnSP)
        self.btnFromPDF.setObjectName("btnFromPDF")
        self.btnFromPDF.setText("打开PDF")
        btnLayout.addWidget(self.btnFromPDF)
        # =====fromPics=====
        self.btnFromPics = QPushButton(btnWidget)
        self.btnFromPics.setSizePolicy(btnSP)
        self.btnFromPics.setObjectName("btnFromPics")
        self.btnFromPics.setText("　打开图片文件夹　")
        btnLayout.addWidget(self.btnFromPics)
        # =====按钮框收尾=====
        btnWidget.setLayout(btnLayout)
        topLayout.addWidget(btnWidget, 0, Qt.AlignTop)
        # =====进度条大框=====
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setMinimumSize(QSize(800, 800))
        self.listWidget.setObjectName("listWidget")
        lwSP = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.listWidget.setSizePolicy(lwSP)
        topLayout.addWidget(self.listWidget)  # 注意，这里不能加Qt.AlignTop
        # =====顶层收尾=====
        self.centralwidget.setLayout(topLayout)
        self.setCentralWidget(self.centralwidget)
        self.resize(self.centralwidget.sizeHint())
        # =====计时器=====
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateBar)
        self.timer.start(1000)
        # =====固有，不要修改=====
        QMetaObject.connectSlotsByName(self)

    def addTaskUI(self, taskName):
        shortName = os.path.basename(taskName)
        if taskName.lower().endswith(".pdf"):
            labelText = f"PDF转图片——{shortName[:-4]}"
        else:
            labelText = f"图片转PDF——{shortName}"
        # =====整体=====
        layout = QVBoxLayout()
        layout.setObjectName(f"layout_{taskName}")
        taskWidget = QWidget(self.centralwidget)
        taskWidget.setObjectName(f"widget_{taskName}")
        # =====label=====
        label = QLabel(taskWidget)
        label.setFont(self.__defaultFont)
        label.setText(labelText)
        label.setObjectName(f"label_{taskName}")
        labelSP = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        label.setSizePolicy(labelSP)
        layout.addWidget(label, 0, Qt.AlignTop)
        # =====进度条=====
        bar = QProgressBar(taskWidget)
        bar.setFont(self.__defaultFont)
        bar.setTextVisible(False)
        bar.setValue(0)
        bar.setMinimumSize(QSize(300, 1))
        bar.setMaximum(1024)
        bar.setObjectName(f"bar_{taskName}")
        barSP = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        bar.setSizePolicy(barSP)
        layout.addWidget(bar, 0, Qt.AlignBottom)
        # =====整体收尾=====
        taskWidget.setLayout(layout)
        # =====添加控件=====
        item = QListWidgetItem()
        item.setSizeHint(taskWidget.sizeHint())
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, taskWidget)
        # =====记录=====
        self._myTasks[taskName] = {}
        self._myTasks[taskName]["bar"] = bar
        self._myTasks[taskName]["listWidgetItem"] = item
        self._myTasks[taskName]["progress"] = 0.0

    def updateBar(self):
        taskNames = list(self._myTasks.keys())
        for taskName in taskNames:
            _dict = self._myTasks[taskName]
            bar = _dict["bar"]
            fvalue = _dict["progress"]
            if fvalue >= 1.0:
                item = self._myTasks[taskName]["listWidgetItem"]
                index = self.listWidget.indexFromItem(item).row()
                self.listWidget.takeItem(index)
                self._myTasks.pop(taskName)
            else:
                bar.setValue(int(fvalue * bar.maximum()))
