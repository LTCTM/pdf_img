import os
import re
import fitz
from PyQt5.QtCore import QThread,QTimer

class _TaskImageToPdf(QThread):
    def __init__(self, inputDir,outputName,signal,timer,parent):
        QThread.__init__(self,parent)
        self._inputDir = inputDir
        self._outputName = outputName
        self._signal=signal

        self._progress=0
        self._picCount=None
        timer.timeout.connect(self._updateBar)

    def run(self):
        pics = os.listdir(self._inputDir)
        #筛选并排序pics
        pics = [p for p in pics if re.search(r"\.png$|\.jpe?g$|\.bmp$",p,re.I)]
        pics = sorted(pics)
        self._picCount = len(pics)
        if self._picCount>0:
            #核心
            doc = fitz.Document()         
            for index, picName in enumerate(pics, start=1):
                self._progress=index+1
                picFullPath = f"{self._inputDir}/{picName}"
                imgDoc = fitz.Document(picFullPath)  # 获得图片对象
                pdfBytes = imgDoc.convertToPDF()  # 获得图片流对象
                imgPdf = fitz.Document("pdf", pdfBytes)  # 将图片流创建单个的PDF文件
                doc.insertPDF(imgPdf)  # 将单个文件插入到文档
                imgDoc.close()
                imgPdf.close()
            #路径与保存
            doc.save(self._outputName)
            doc.close()

    def _updateBar(self):
        if self._picCount is not None:
            if self._picCount>0:
                self._signal.emit(self._inputDir,self._progress / self._picCount)
            else:
                self._signal.emit(self._inputDir,1.0)

def imageToPdfAsync(inputDir,outputName,signal,timer,widget):
    _TaskImageToPdf(inputDir,outputName,signal,timer,widget).start()


class _TaskPdfToImage(QThread):
    def __init__(self, inputName,outputDir,signal,timer,parent):
        QThread.__init__(self,parent)
        self._inputName = inputName
        self._outputDir = outputDir
        self._signal=signal

        self._progress=0
        self._pageCount=None
        timer.timeout.connect(self._updateBar)

    def run(self):
        newDirName = self._inputName[:-4]
        if not os.path.exists(newDirName):
            os.mkdir(newDirName)
        # 正式开始
        pdf = fitz.Document(self._inputName)
        self._pageCount = pdf.pageCount
        for index in range(0, self._pageCount):
            self._progress=index+1
            page = pdf[index]  # 获得每一页的对象
            trans = fitz.Matrix(1.0, 1.0).preRotate(0)
            pm = page.getPixmap(matrix=trans, alpha=False)  # 获得每一页的流对象
            imgName = newDirName + '/{:0>5d}.png'.format(index + 1)
            pm.writePNG(imgName)
        #路径与保存
        pdf.close()

    def _updateBar(self):
        if self._pageCount is not None:
            if self._pageCount>0:
                self._signal.emit(self._inputName,self._progress / self._pageCount)
            else:
                self._signal.emit(self._inputName,1.0)

def pdfToImageAsync(inputName,outputDir,signal,timer,widget):
    _TaskPdfToImage(inputName,outputDir,signal,timer,widget).start()