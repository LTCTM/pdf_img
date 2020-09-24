from os.path import exists, join
from os import listdir, mkdir
from re import search as re_search, I as re_I
import fitz
import math
from PyQt5.QtCore import QThread

get_digits = lambda num: 1 if num <= 1 else math.floor(math.log10(num)) + 1


class _TaskImageToPdf(QThread):
    def __init__(self, inputDir, outputName, signal, timer, parent):
        QThread.__init__(self, parent)
        self._inputDir = inputDir
        self._outputName = outputName
        self._signal = signal

        self._progress = 0
        self._picCount = None
        timer.timeout.connect(self._updateBar)

    def run(self):
        pics = sorted(
            f"{self._inputDir}/{p}"
            for p in listdir(self._inputDir)
            if re_search(r"\.png$|\.jpe?g$|\.bmp$", p, re_I)
        )
        self._picCount = len(pics)
        if self._picCount == 0:
            return
        with fitz.Document() as doc:
            for index, picName in enumerate(pics, start=1):
                self._progress = index
                try:
                    with fitz.open(picName) as img:
                        rect = img[0].rect
                        pdfbytes = img.convertToPDF()
                    with fitz.open("pdf", pdfbytes) as imgPDF:
                        page = doc.newPage(width=rect.width, height=rect.height)
                        page.showPDFpage(rect, imgPDF, 0)
                except:
                    continue
            doc.save(self._outputName)

    def _updateBar(self):
        if self._picCount is not None:
            if self._picCount > 0:
                self._signal.emit(self._inputDir, self._progress / self._picCount)
            else:
                self._signal.emit(self._inputDir, 1.0)


def imageToPdfAsync(inputDir, outputName, signal, timer, widget):
    _TaskImageToPdf(inputDir, outputName, signal, timer, widget).start()


class _TaskPdfToImage(QThread):
    def __init__(self, inputName, outputDir, signal, timer, parent, zoom=(1.0, 1.0)):
        QThread.__init__(self, parent)
        self._inputName = inputName
        self._outputDir = outputDir
        self._signal = signal
        self._zoom = zoom

        self._progress = 0
        self._pageCount = None
        timer.timeout.connect(self._updateBar)

    def run(self):
        newDirName = self._inputName[:-4]
        if not exists(newDirName):
            mkdir(newDirName)
        # 正式开始
        with fitz.Document(self._inputName) as doc:
            self._pageCount = doc.pageCount
            digits = get_digits(doc.pageCount)
            for index, page in enumerate(doc, 1):
                self._progress = index
                page.getPixmap(matrix=fitz.Matrix(*self._zoom)).writePNG(
                    join(newDirName, f"P{str(index).zfill(digits)}.png")
                )

    def _updateBar(self):
        if self._pageCount is not None:
            if self._pageCount > 0:
                self._signal.emit(self._inputName, self._progress / self._pageCount)
            else:
                self._signal.emit(self._inputName, 1.0)


def pdfToImageAsync(inputName, outputDir, signal, timer, widget, zoom=(1.0, 1.0)):
    _TaskPdfToImage(inputName, outputDir, signal, timer, widget, zoom).start()

