from Ui_MainWindow import *
import processing
import os.path
import re

class MainWindow(Ui_MainWindow):
    getProgress = pyqtSignal(str,float)
    def __init__(self):
        Ui_MainWindow.__init__(self)
        self.btnFromPDF.clicked.connect(self.tansfer_pdf)
        self.btnFromPics.clicked.connect(self.tansfer_pics)
        self.getProgress.connect(self.updateProgress)

    def updateProgress(self, taskName,progress):
        _dict=self._myTasks.get(taskName,None)
        if _dict:
            _dict["progress"]=progress

    def tansfer_pdf(self):
        filePath,filter = QFileDialog.getOpenFileName(self, filter= r"PDF (*.pdf)")
        if filePath:
            self.addTaskUI(filePath)
            outputDir = filePath[:-4]
            processing.pdfToImageAsync(filePath,outputDir,self.getProgress,self.timer,self)

    def tansfer_pics(self):
        dirPath = QFileDialog.getExistingDirectory(self)
        if dirPath:
            for curDir, subDirs, pics in os.walk(dirPath):
                self.addTaskUI(curDir)
                outputDir = os.path.dirname(dirPath)
                shortName = re.sub(r"[/\\]",".",curDir[len(outputDir) + 1:]) #+1是为了替换路径最前面的/
                processing.imageToPdfAsync(curDir, f"{outputDir}/{shortName}.pdf",self.getProgress, self.timer,self)
                
