from Ui_MainWindow import *
from processing import *
from os.path import dirname, join
from pathlib import Path
import re


class MainWindow(Ui_MainWindow):
    getProgress = pyqtSignal(str, float)

    def __init__(self):
        Ui_MainWindow.__init__(self)
        self.btnFromPDF.clicked.connect(self.tansfer_pdf)
        self.btnFromPics.clicked.connect(self.tansfer_pics)
        self.getProgress.connect(self.updateProgress)

    def updateProgress(self, taskName, progress):
        _dict = self._myTasks.get(taskName, None)
        if _dict:
            _dict["progress"] = progress

    def tansfer_pdf(self):
        filePath, filter = QFileDialog.getOpenFileName(self, filter=r"PDF (*.pdf)")
        if filePath:
            self.addTaskUI(filePath)
            outputDir = filePath[:-4]
            pdfToImageAsync(filePath, outputDir, self.getProgress, self.timer, self)

    def tansfer_pics(self):
        dirPath = QFileDialog.getExistingDirectory(self)
        outputDir = dirname(dirPath).replace("/", "\\")
        if dirPath:
            for curDir in (str(i) for i in Path.rglob(dirPath, "*") if i.is_dir()):
                self.addTaskUI(curDir)
                shortName = curDir[len(outputDir) + 1 :].replace(
                    "\\", "."
                )  # +1是为了替换路径最前面的/
                imageToPdfAsync(
                    curDir,
                    join(outputDir, f"{shortName}.pdf"),
                    self.getProgress,
                    self.timer,
                    self,
                )
