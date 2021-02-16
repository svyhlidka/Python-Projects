# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 18:03:44 2021

@author: stvyh
"""

from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtGui     import QPalette, QFont, QFontMetrics, QStandardItem, QStandardItemModel
from PyQt5.QtCore    import Qt, QRect, QSize, QEvent, QCoreApplication, QMetaObject
from PyQt5.QtCore    import QPointF, QRectF, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtWidgets import QWidget, QDialogButtonBox, QGridLayout, QFormLayout,QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QToolButton, QDoubleSpinBox, QLineEdit
from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate, qApp, QListView
from PyQt5.QtWidgets import QGraphicsScene, QFileDialog, QMessageBox, QDialog
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QGroupBox
from functools import partial
import numpy as np
import cv2
import os

class ColorMaps(object):
    
    def __init__(self):
        self.colorMaps = {'AUTUMN': 0, 'BONE': 1, 'JET': 2, 'WINTER': 3,
             'RAINBOW': 4, 'OCEAN': 5, 'SUMMER': 6, 'SPRING': 7,
             'COOL': 8, 'HSV': 9, 'PINK': 10, 'HOT': 11}

        self.mapsLabel = [*self.colorMaps.keys()]

class CheckableComboBox(QComboBox):

    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        palette = qApp.palette()
        palette.setBrush(QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):

        if object == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None, checked=False):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        if checked: item.setData(Qt.Checked, Qt.CheckStateRole)
        else: item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None, defaults=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data, (text in defaults))

    def currentData(self):
        # Return the list of selected items data
        res = ''
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                res = res +(self.model().item(i).data()) + ' '
        return res


class Ui_INI_Dialog(object):
    def setupUi(self, Dialog):
        self.source_dir = ''
        self.result_dir = ''
        self.color_map = '' 
        self.scale = ''

        self.CM =['AUTUMN','BONE','JET','WINTER','RAINBOW','OCEAN',
        'SUMMER','SPRING','COOL','HSV','PINK','HOT']
        self.dataList = [*range(12)]
        Dialog.setObjectName("Dialog")
        Dialog.resize(446, 316)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(20, 250, 381, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QRect(20, 10, 381, 211))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.sourceDirectoryLineEdit = QLineEdit(self.gridLayoutWidget)
        self.sourceDirectoryLineEdit.setObjectName("sourceDirectoryLineEdit")
        self.gridLayout.addWidget(self.sourceDirectoryLineEdit, 0, 1, 1, 1)
        self.resultDirectoryLineEdit = QLineEdit(self.gridLayoutWidget)
        self.resultDirectoryLineEdit.setObjectName("resultDirectoryLineEdit")
        self.gridLayout.addWidget(self.resultDirectoryLineEdit, 1, 1, 1, 1)
        self.resultsDirectoryLabel = QLabel(self.gridLayoutWidget)
        self.resultsDirectoryLabel.setObjectName("resultsDirectoryLabel")
        self.gridLayout.addWidget(self.resultsDirectoryLabel, 1, 0, 1, 1)
        self.sourceDirectoryToolButton = QToolButton(self.gridLayoutWidget)
        self.sourceDirectoryToolButton.setObjectName("sourceDirectoryToolButton")
        self.gridLayout.addWidget(self.sourceDirectoryToolButton, 0, 2, 1, 1)
        self.resultDirectoryToolButton = QToolButton(self.gridLayoutWidget)
        self.resultDirectoryToolButton.setObjectName("resultDirectoryToolButton")
        self.gridLayout.addWidget(self.resultDirectoryToolButton, 1, 2, 1, 1)
        self.scaleSpinBox = QDoubleSpinBox(self.gridLayoutWidget)
        self.scaleSpinBox.setMaximumSize(QSize(50, 20))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.scaleSpinBox.setFont(font)
        self.scaleSpinBox.setMinimum(0.01)
        self.scaleSpinBox.setMaximum(10.0)
        self.scaleSpinBox.setSingleStep(0.05)
        self.scaleSpinBox.setProperty("value", 1.0)
        self.scaleSpinBox.setObjectName("scaleSpinBox")
        self.gridLayout.addWidget(self.scaleSpinBox, 4, 1, 1, 1)
        self.sourceDirectoryLabel = QLabel(self.gridLayoutWidget)
        self.sourceDirectoryLabel.setObjectName("sourceDirectoryLabel")
        self.gridLayout.addWidget(self.sourceDirectoryLabel, 0, 0, 1, 1)
        self.scaleLabel = QLabel(self.gridLayoutWidget)
        self.scaleLabel.setObjectName("scaleLabel")
        self.gridLayout.addWidget(self.scaleLabel, 4, 0, 1, 1)
        self.colorMapLabel = QLabel(self.gridLayoutWidget)
        self.colorMapLabel.setObjectName("colorMapLabel")
        self.gridLayout.addWidget(self.colorMapLabel, 2, 0, 1, 1)
        self.CMcomboBox = CheckableComboBox(self.gridLayoutWidget)
        self.CMcomboBox.setObjectName("CMcomboBox")
        self.gridLayout.addWidget(self.CMcomboBox, 2, 1, 1, 1)
        
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.acceptAndSave)
        self.buttonBox.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

        self.sourceDirectoryToolButton.clicked.connect(self._source_dir_dialog)
        self.resultDirectoryToolButton.clicked.connect(self._result_dir_dialog)
        
        self.readINI()
       

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Default Values"))
        self.resultsDirectoryLabel.setText(_translate("Dialog", "Results Directory"))
        self.sourceDirectoryToolButton.setText(_translate("Dialog", "..."))
        self.resultDirectoryToolButton.setText(_translate("Dialog", "..."))
        self.sourceDirectoryLabel.setText(_translate("Dialog", "Source Directory"))
        self.scaleLabel.setText(_translate("Dialog", "Scale"))
        self.colorMapLabel.setText(_translate("Dialog", "Default Color Map"))

    def acceptAndSave(self):
        source_dir = self.sourceDirectoryLineEdit.text()
        result_dir = self.resultDirectoryLineEdit.text()
        color_map  = self.CMcomboBox.currentData()
        scale      = str(self.scaleSpinBox.value())
        f = open("elilik.ini", "w")
        f.write(f"source_dir : {source_dir}\n")
        f.write(f"result_dir : {result_dir}\n")
        f.write(f"color_map : {color_map}\n")
        f.write(f"scale : {scale}\n")
        f.close() 
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Default values successfully updated!")
        msg.setWindowTitle("Saved") 
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
    def readINI(self):
        if os.path.exists("elilik.ini"):
            f = open("elilik.ini", "r")
            Lines = f.readlines()
            # Strips the newline character
            for line in Lines:
                l = line.strip()
                if "source_dir : " in l:
                    self.source_dir = l.replace("source_dir : ","").strip()
                elif "result_dir : " in l:
                    self.result_dir = l.replace("result_dir : ","").strip()  
                elif "color_map : " in l:
                    self.color_map = l.replace("color_map : ","").strip()  
                elif "scale : " in l:
                    self.scale = l.replace("scale : ","").strip()
                else:
                    ...
        self.sourceDirectoryLineEdit.setText(self.source_dir)
        self.resultDirectoryLineEdit.setText(self.result_dir)
        self.scaleSpinBox.setValue(float(self.scale))
        self.CMcomboBox.addItems(self.CM,None,self.color_map)

    def _source_dir_dialog(self):
        directory = str(QFileDialog.getExistingDirectory())
        self.sourceDirectoryLineEdit.setText('{}'.format(directory))

    def _result_dir_dialog(self):
        directory = str(QFileDialog.getExistingDirectory())
        self.resultDirectoryLineEdit.setText('{}'.format(directory))

class ColorMapsDialog(object):
    
    def __init__(self,  title, message, items_selected, imageName):
        self.title = title
        self.message = message
        self.items_selected = items_selected #[s for s in items_selected.split(',')]
        self.imageName = imageName
        self.cmObj = ColorMaps()
        self.CM = self.cmObj.colorMaps
        
        form = QFormLayout()
        form.addRow(QLabel(message))
        self.listView = QListView()
        form.addRow(self.listView)
        font = QFont()
        font.setBold(True)
        font.setPointSize(8)
        self.listView.setFont(font)
        model = QStandardItemModel(self.listView)
        size = QSize(60,30)
        for item in self.CM:
            # create an item with a caption
            standardItem = QStandardItem(item)
            standardItem.setCheckable(True)
            if item in self.items_selected: standardItem.setCheckState(True)
            standardItem.setSizeHint(size)
            model.appendRow(standardItem)
        self.listView.setModel(model)
        
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(530, 447)
        Dialog.setWindowTitle(self.title)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QRect(10, 390, 511, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayoutWidget = QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QRect(9, 10, 511, 363))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.addWidget(self.listView)
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setText("")
        self.label.setPixmap(QPixmap(self.imageName))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", self.title))
        
    def itemsSelected(self):
        selected = []
        model = self.listView.model()
        i = 0
        while model.item(i):
            if model.item(i).checkState():
                selected.append(model.item(i).text())
            i += 1
        return selected

class TransformScene(QGraphicsScene):
    
    file_signal  = pyqtSignal(str)
    info_signal  = pyqtSignal(str)
    sliders_reset_signal = pyqtSignal()

    def __init__(self, parent = None):
        QGraphicsScene.__init__(self, parent)
        self.setSceneRect(0,0,3000,2000)
        self.cv2Images = {} # dictionary (filename:image) read by cv2 
        self.default_colorMap = 'JET'
        self.cur_pos = (0,0)
        self.imgScale   = 1.0
        self.currentTransform = 0 
        self.inverted = 0
        self.currentBrightnessValue = 0
        self.currentBlurValue = 0
        self.lastPoint =  None
        self.currentKernelSizeValue = 10
        self.currentSigmaValue = 10
        self.thetaCurrentValue = 1
        self.currentBlockSizeValue = 11
        self.currentCValue = 5
        self.transform5CurrentName = None
        self.currentTransparencyAlpha = 0.4
        self.currentTransparencyBeta  = (1-self.currentTransparencyAlpha)
        self.source_dir = ''
        self.result_dir = ''
        self.color_map = '' 
        self.scale = ''
        self.cmObj =  ColorMaps()
        self.CM = self.cmObj.colorMaps

    def mousePressEvent(self, event):
        self.lastPoint = event.pos()
        if event.button() == Qt.LeftButton:
            QGraphicsScene.mousePressEvent(self,event)
            if type(self.mouseGrabberItem()) is type(None):
                self.file_signal.emit('')
                return
            else:
                self.file_signal.emit(self.mouseGrabberItem().filename)
        elif event.button() == Qt.RightButton:
            for item in self.items():
                item.setZValue(0)
            if len(self.selectedItems()) == 1:
                self.selectedItems()[0].setZValue(1)
        else:
            QGraphicsScene.mousePressEvent(self,event) 
        
    def keyPressEvent(self, event):
        key = event.key()
        if self.selectedItems() == [] or key not in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down]:
            super(TransformScene, self).keyPressEvent(event)
            return
        dx = 0
        dy = 0
        step = 1
        if (event.modifiers() & Qt.ShiftModifier):
            step = 10
        if (event.modifiers() & Qt.ControlModifier):
            step = 100
        if key == Qt.Key_Left:
            dx = -1*step
        if key == Qt.Key_Right:
            dx = 1*step
        if key == Qt.Key_Up:
            dy = -1*step
        if key == Qt.Key_Down:
            dy = 1*step
        for item in self.selectedItems():
            if item.x()+dx < 0: x = 0
            else: x = item.x()+dx
            if item.y()+dx < 0: y = 0
            else: y = item.y()+dy
            item.setPos(x, y)
        else:
            pass
        return


    def addTransform(self, iName, tFormat, pos):
        image = self.cv2Images[iName]
        image = QImage(image, image.shape[1], image.shape[0], image.strides[0], tFormat) 
        im = QPixmap.fromImage(image)
        if self.imgScale != 1: # and self.currentTransform == 0:
            sx = int(self.imgScale*im.width())
            sy = int(self.imgScale*im.height())
            im=im.scaled(sx, sy, Qt.KeepAspectRatio, Qt.FastTransformation)
        im = MovablePixmapItem(im,iName)
        im.setPos(pos)
        self.addItem(im)


    def changeBrightness(self, img):
        
        """
        takes image and brigtness value. Willperform brightness change using OpenCv
        and after split, will merge the img and return it
        """
        value = self.currentBrightnessValue
        
        if value == 0:
            return img
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v>lim] = 255
        v[v<=lim] += value
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    def changeBlur(self, img):
        
        """
        takes image and blur value. Willperform blur change using OpenCv
         return it
        """
        value = self.currentBlurValue
        if value == 0:
            return img
        kernel_size = (value+1, value+1) # +1 to avoid 0
        #img = cv2.blur(img, kernel_size)
        img = cv2.GaussianBlur(img, kernel_size,0)
        return img

    def setSelectedItemByName(self, iName):
        for item in self.items(): 
            if item.filename == iName: item.setSelected(True)
    
    def transform1(self): # Brightnes and Blur
        """
         changes Brightnes and Blur of all selected images
        """
        if len(self.selectedItems()) == 0: return
        for item in self.selectedItems():
            image_src = self.cv2Images[item.filename]
            iName = item.filename
            original_pos = item.pos()
            self.removeItem(item) #remove old item from scene
            image = self.changeBrightness(image_src)
            image = self.changeBlur(image)
            if self.inverted: image = cv2.bitwise_not(image)
            self.cv2Images[iName] = image
            self.addTransform(iName, QImage.Format_RGB888, original_pos)
            # setting back selected status
            self.setSelectedItemByName(iName)
            # moving original image back for next transform
            self.cv2Images[iName] = image_src 

   
    def transform2(self, All, boolTxt):
        """
        Parameters
        ----------
        All : bool
            use all colorMap.
        boolTxt : bool
            show color name in picture

        Returns
        -------
        None.

        """
        if All: colorMapIdxSelected = self.cmObj.mapsLabel
        else:
            Dialog = QDialog()
            dial = ColorMapsDialog("Select method", "List of Color Maps Methods", self.color_map, 'C:/Temp/Data/test/colorMaps.png')
            dial.setupUi(Dialog)
            Dialog.show()
            if Dialog.exec_() == QDialog.Accepted:
                colorMapIdxSelected  = dial.itemsSelected()
            else: return
        
        if len(self.selectedItems()) == 0: return
        pos = QPointF(0,0)
        for item in self.selectedItems():
            image_src = self.cv2Images[item.filename]
            if len(image_src.shape) == 3: image_src = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)
            h, w = image_src.shape[:2]
            h = self.imgScale*h
            w = self.imgScale*w
            i = 0
            x0 = 0
            y0 = h+10
            for idx in colorMapIdxSelected: 
                image = cv2.applyColorMap(image_src, self.cmObj.colorMaps[idx])
                if boolTxt:
                    cv2.putText(image,idx, (10,20),cv2.FONT_HERSHEY_COMPLEX,0.8,(20,20,20),1,cv2.LINE_AA, False)
                iName = item.filename+"-"+idx
                x = int(w*i)+5
                y = y0
                pos = QPointF(x,y)
                i += 1
                if i == 3:
                    i = 0
                    y0 += (h+5)
                if self.inverted: 
                    image = cv2.bitwise_not(image)
                    iName = iName+' inv.'
                self.cv2Images[iName] = image
                self.addTransform(iName, QImage.Format_RGB888, pos)

    def transform4(self):  # SOBEL X and Y
        if len(self.selectedItems()) == 0: return
        for item in self.selectedItems():
            image = self.cv2Images[item.filename]
            if len(image.shape) == 3: image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            h, w = image.shape[:2]
            h = h*self.imgScale
            w = w*self.imgScale
            pos = QPointF(0,h+5)
            sobelX = cv2.Sobel(image, cv2.CV_64F, 0, 1)
            if self.inverted: sobelX = cv2.bitwise_not(sobelX)           
            self.cv2Images['SobelX'] = sobelX
            self.addTransform('SobelX', QImage.Format_Indexed8, pos)
            pos = QPointF(w+10.,h+5)
            sobelY = cv2.Sobel(image, cv2.CV_64F, 1, 0)
            if self.inverted: sobelY = cv2.bitwise_not(sobelY)           
            self.cv2Images['SobelY'] = sobelY
            self.addTransform('SobelY', QImage.Format_Indexed8, pos)
            pos = QPointF(w/2,2*h+10.0)
            sobelXY = cv2.bitwise_or( sobelX, sobelY)
            if self.inverted: sobelXY = cv2.bitwise_not(sobelXY)           
            self.cv2Images['SobelXY'] = sobelXY
            self.addTransform('SobelXY', QImage.Format_Indexed8, pos)
            
    def transform5(self): # Threshold
        if len(self.selectedItems()) == 0: return
        if self.currentBlockSizeValue % 2 != 1: self.currentBlockSizeValue += 1
        pos = QPointF(0,0)
        item = self.selectedItems()[0]
        image_src = self.cv2Images[item.filename]
        iName = item.filename
        self.clear()
        self.cv2Images = {}
        h, w = image_src.shape[:2]
        h = self.imgScale*h
        w = self.imgScale*w
        self.cv2Images[iName] = image_src
        self.addTransform(iName, QImage.Format_RGB888,  pos)
        # new original image needs to selected for next change
        self.setSelectedItemByName(iName)
        if len(image_src.shape) == 3: image = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)
        else: image = image_src.copy()
        image = cv2.adaptiveThreshold(image, 255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 
                self.currentBlockSizeValue,  self.currentCValue) 
        iName = iName+'-Threshold'
        if self.inverted: 
            image = cv2.bitwise_not(image)
            iName = iName+' inv.'
        self.cv2Images[iName] = image
        self.addTransform(iName, QImage.Format_Indexed8, QPointF(w+5,0))
           
    def apply_ColorMap(self, iName, image, color, pos):
        image = cv2.applyColorMap(image, self.CM[color])
        self.cv2Images[iName] = image
        self.addTransform(iName, QImage.Format_RGB888, pos)
        
    def transform6(self): # Laplacian
        if len(self.selectedItems()) == 0: return
        for item in self.selectedItems():
            image = self.cv2Images[item.filename]
            if len(image.shape) == 3: image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            h, w = image.shape[:2]
            h = self.imgScale*h
            w = self.imgScale*w
            image = self.transDFT(image)
            iName = item.filename+ '-DFT'
            if self.inverted: 
                image = cv2.bitwise_not(image)
                iName = iName+' inv.'
            if len(self.CM) > 0:
                i = 1
                x = w+5
                y = 0
                for color in self.color_map:
                    self.apply_ColorMap(iName, image, color, QPointF(x,y))
                    i += 1
                    x = x + w + 5
                    if i == 3:
                        i = 0
                        x = 0
                        y = y + h + 5
            else:
                self.apply_ColorMap(iName, image, cv2.COLORMAP_MAGMA, QPointF(w+5,0))

    def transform7(self): # FFT
        if len(self.selectedItems()) == 0: return
        for item in self.selectedItems():
            image = self.cv2Images[item.filename]
            if len(image.shape) == 3: image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            h, w = image.shape[:2]
            h = self.imgScale*h
            w = self.imgScale*w
            image = self.transFFT(image)
            iName = item.filename+'-FFT'
            if self.inverted: 
                image = cv2.bitwise_not(image)
                iName = iName+' inv.'
            if len(self.CM) > 0:
                i = 1
                x = w+5
                y = 0
                for color in self.color_map:
                    self.apply_ColorMap(iName, image, color, QPointF(x,y))
                    i += 1
                    x = x + w + 5
                    if i == 3:
                        i = 0
                        x = 0
                        y = y + h + 5
            else:
                self.apply_ColorMap(iName, image, cv2.COLORMAP_MAGMA, QPointF(w+5,0))
        
    def transform8(self): #'Gabor'
        for item in self.selectedItems():
            ksize = self.currentKernelSizeValue
            sigma = self.currentSigmaValue
            theta = 1*np.pi/self.thetaCurrentValue #angle /2 horizontal /1 vertical
            lamda = 1*np.pi/4 # waveLength
            gamma = 0.5 #aspect ration 1 - circular ratio, 0.01 diagonal
            phi = 0 # phase offset don't care usually
            
            pos = QPointF(0,0)
            item = self.selectedItems()[0]
            image_src = self.cv2Images[item.filename]
            iName = item.filename
            self.clear()
            self.cv2Images = {}
            h, w = image_src.shape[:2]
            h = self.imgScale*h
            w = self.imgScale*w
            self.cv2Images[iName] = image_src
            self.addTransform(iName, QImage.Format_RGB888,  pos)
            # new original image needs to selected for next change
            self.setSelectedItemByName(iName)
            kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, phi, ktype=cv2.CV_32F)
            #print('=======>', image_src.shape)
            if len(image_src.shape) == 3: image = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)
            else: image = image_src.copy()
            image = cv2.filter2D(image, cv2.CV_8UC3, kernel)
            iName = iName+'-Gabor'
            if self.inverted: 
                image = cv2.bitwise_not(image)
                iName = iName+' inv.'
            self.cv2Images[iName] = image
            self.addTransform(iName, QImage.Format_Indexed8, QPointF(w+5,0))
        
    def transform9(self): # difference
        if len(self.selectedItems()) != 2 : return 
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        fNames = [*self.cv2Images]
        image1 = self.cv2Images[fNames[0]]
        image2 = self.cv2Images[fNames[1]]
        i1, i2, diff = self.transImageDifference(image1, image2)
        self.clear()
        self.cv2Images = {}
        iName = fNames[0]
        h, w = i1.shape[:2]
        h = self.imgScale*h
        w = self.imgScale*w
        self.cv2Images[iName] = i1
        self.addTransform(iName, QImage.Format_RGB888, QPointF(0, 0))
        iName = fNames[1]
        self.cv2Images[iName] = i2
        self.addTransform(iName, QImage.Format_RGB888, QPointF(w+5, 0))
        iName = 'Difference'
        self.cv2Images[iName] = diff
        self.addTransform(iName, QImage.Format_RGB888, QPointF(w//2,h+5))

        
    def transform10(self): # BGR to Gray
        if len(self.selectedItems()) == 0: return
        for item in self.selectedItems():
            image_src = self.cv2Images[item.filename]
            iName = item.filename
            original_pos = item.pos()
            self.removeItem(item) #remove old item from scene
            if len(image_src.shape) == 3: image = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)
            else: image = image_src.copy()
            if self.inverted: image = cv2.bitwise_not(image)
            self.cv2Images[iName] = image
            self.addTransform(iName, QImage.Format_Indexed8, original_pos)
            # setting back selected status
            self.setSelectedItemByName(iName)
            # moving original image back for next transform
            self.cv2Images[iName] = image_src 


    def transform11(self): #transparency 
        if len(self.selectedItems()) != 2: return
        background = cv2.imread('field.jpg')
        overlay = cv2.imread('dice.png')
        alpha = 0.4
        beta = (1.0 - alpha)
        #beta = 0.1
        added_image = cv2.addWeighted(background,alpha,overlay,beta,0)

    def findSceneArea(self):
        """
          returns image scene area

        Returns
        -------
        xMin : float
            left top x
        yMin : float
            left top y
        xMax : float
            right bottom x
        yMax : float
            right bottom x

        """
        xMax = -1000000.
        yMax = -1000000.
        xMin = 1000000.
        yMin = 1000000.
        for item in self.items():
           # print(item.filename, item.pos(), item.pixmap().width(),item.pixmap().height())
            x = item.pos().x()+item.pixmap().width()
            y = item.pos().y()+item.pixmap().height()
            if xMax < x:
                xMax = x
            if xMin > item.pos().x():
                xMin = item.pos().x()
            if yMax < y:
                yMax = y
            if yMin > item.pos().y():
                yMin = item.pos().y()
        return (xMin, yMin, xMax, yMax)
        
    def showSceneSize(self):
        x = self.scene.sceneRect().width()
        y = self.scene.sceneRect().height()      
        self.infoLabel.setText(f'size: {x}x{y}, {self.scene.findSceneArea()}')


    def readCV2(self, filename, gray): 
        """
        reads image from disk

        Parameters
        ----------
        filename : string
            filename path
        gray : int / bool
            if 1 - converts image to gray

        Returns
        -------
        fName : string
            fileme (index in MyScene.cv2Images dictionary)

        """
        fName = os.path.basename(filename)          
        if gray:
            img = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)           
        else:
            img = cv2.imread(filename)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.file_signal.emit(f'File: {fName}')
        
        
        self.cv2Images[fName] = img
        return fName


    def addImg(self):       
        filenames = QFileDialog.getOpenFileNames(None,
                                     "Select one or more Imagess to open",
                                     self.source_dir,
                                     "Images (*.png *.xpm *.jpg *.bmp)")
        if not filenames:
            return 
        self.currentTransform = 0
        xMin, yMin, xMax, yMax = self.findSceneArea()
        prevXmax = 0.; x0 = 0.; y0 = yMax+10.
        for filename in filenames[0]:
            iName = self.readCV2(filename, 0)
            sx = int(self.cv2Images[iName].shape[1]*self.imgScale)
            xMin, yMin, xMax, yMax = self.findSceneArea()
            if not len(self.items()) % 3:
                if len(self.items()) == 0:
                    x0 = 0.
                    y0 = 0.        
                    prevXmax = 0.
                else:
                    x0 = 0.
                    y0 = yMax + 10.
                    prevXmax = 0.
            else:
                x0 = prevXmax+10.
            prevXmax += sx
            iPos = QPointF(float(x0),float(y0))
            self.addTransform(iName, QImage.Format_RGB888, iPos)
            self.info_signal.emit(f'Number of Images: {len(self.items())}')
            
    def saveScene(self): 
        # saves all scene
        fname, filter = QFileDialog.getSaveFileName(None, 'Save File',  self.result_dir, 'images (*.png)')
        if fname:
            xMin, yMin, xMax, yMax = self.findSceneArea()
            # Get region of scene to capture from somewhere.
            ##srect = QRectF(self.sceneRect())
            srect = QRectF(QPointF(xMin, yMin), QPointF(xMax, yMax))
            # Create a QImage to render to and fix up a QPainter for it.
            ##img = QImage(int(srect.width()),int(srect.height()), QImage.Format_RGB32) 
            img = QImage(int(xMax), int(yMax), QImage.Format_RGB32)
            img.fill(Qt.white)
            self.painter = QPainter(img)
            self.render(self.painter, QRectF(img.rect()), srect)
            self.painter.end()
            img.save(fname, "PNG")

    def saveImg(self):
        #saves single image
        if len(self.selectedItems()) != 1: return
        image = self.selectedItems()[0].pixmap()
        fname, filter = QFileDialog.getSaveFileName(None, 'Save File',  self.result_dir, 'images (*.png)') 
        if fname: image.save(fname, "PNG")

    def transDFT(self, I):
        rows, cols = I.shape
        m = cv2.getOptimalDFTSize( rows )
        n = cv2.getOptimalDFTSize( cols )
        padded = cv2.copyMakeBorder(I, 0, m - rows, 0, n - cols, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        
        planes = [np.float32(padded), np.zeros(padded.shape, np.float32)]
        complexI = cv2.merge(planes)         # Add to the expanded another plane with zeros
        
        cv2.dft(complexI, complexI)         # this way the result may fit in the source matrix
        
        cv2.split(complexI, planes)                   # planes[0] = Re(DFT(I), planes[1] = Im(DFT(I))
        cv2.magnitude(planes[0], planes[1], planes[0])# planes[0] = magnitude
        magI = planes[0]
        
        matOfOnes = np.ones(magI.shape, dtype=magI.dtype)
        cv2.add(matOfOnes, magI, magI) #  switch to logarithmic scale
        cv2.log(magI, magI)
        
        magI_rows, magI_cols = magI.shape
        # crop the spectrum, if it has an odd number of rows or columns
        magI = magI[0:(magI_rows & -2), 0:(magI_cols & -2)]
        cx = int(magI_rows/2)
        cy = int(magI_cols/2)
        q0 = magI[0:cx, 0:cy]         # Top-Left - Create a ROI per quadrant
        q1 = magI[cx:cx+cx, 0:cy]     # Top-Right
        q2 = magI[0:cx, cy:cy+cy]     # Bottom-Left
        q3 = magI[cx:cx+cx, cy:cy+cy] # Bottom-Right
        tmp = np.copy(q0)               # swap quadrants (Top-Left with Bottom-Right)
        magI[0:cx, 0:cy] = q3
        magI[cx:cx + cx, cy:cy + cy] = tmp
        tmp = np.copy(q1)               # swap quadrant (Top-Right with Bottom-Left)
        magI[cx:cx + cx, 0:cy] = q2
        magI[0:cx, cy:cy + cy] = tmp
        cv2.normalize(magI, magI, 0, 1, cv2.NORM_MINMAX) # Transform the matrix with float values into a
        return ((magI +1)*255/2.).astype(np.uint8)
    
    def transFFT(self, image):
        f = np.fft.fft2(image)
        fshift = np.fft.fftshift(f)
        image = 20*np.log(np.abs(fshift))            
        return image.astype(np.uint8)
           # image = ((image +1)*255/2.).astype(np.uint8)
           
    def transImageDifference(self, image1, image2):
        # compute difference
        #difference = cv2.subtract(image1, image2)
        difference = cv2.absdiff(image1, image2)

        # color the mask red
        Conv_hsv_Gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(Conv_hsv_Gray, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
        difference[mask != 255] = [0, 0, 255]
        
        # add the red mask to the images to make the differences obvious
        image1[mask != 255] = [0, 0, 255]
        image2[mask != 255] = [0, 0, 255]
        return image1.astype(np.uint8), image2.astype(np.uint8), difference.astype(np.uint8)


    def dialogClearScene(self):
        l = len(self.selectedItems())
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        if l > 0:
            txt = f'Delete {l} selected image(s)??'
        else:
            txt = 'Delete All Images?'
        msgBox.setText(txt)
        msgBox.setWindowTitle("Delete Image(s)")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.currentTransform = 0 
            if l > 0:
                for item in self.selectedItems():
                    del self.cv2Images[item.filename]
                    self.removeItem(item)
                if l == 1:
                    self.sliders_reset_signal.emit()
            else: 
                self.clear()
                self.cv2Images = {}
                self.sliders_reset_signal.emit()
    
#### End class MyScene


class MovablePixmapItem(QGraphicsPixmapItem):
       
    def __init__(self, pixmap, name,  *args, **kwargs):
        self.filename = name
        
       
        QGraphicsPixmapItem.__init__(self, pixmap, *args, **kwargs)
        self.setFlags(QGraphicsItem.ItemIsMovable | 
                      QGraphicsItem.ItemIsSelectable |
                      QGraphicsItem.ItemSendsGeometryChanges |
                      QGraphicsItem.ItemSendsScenePositionChanges)
        self.w = self.pixmap().width()
        self.h = self.pixmap().height()
    
    
    # def contextMenuEvent(self,event):
    #     contextMenu = QMenu(self)
    #     newAction =contextMenu.addAction("New")
    #     openAction =contextMenu.addAction("Nečum")
    #     quitAction =contextMenu.addAction("Quit")
        
    #     action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        
    #     if action == quitAction:
    #         self.close()
        
    def mouseDoubleClickEvent(self, event):
        self.showDialog(event.pos().x(),event.pos().y())
        
    def itemChange(self, change, value):

        if change == QGraphicsItem.ItemPositionHasChanged:
        
            if value.x() < 0 or value.y() < 0:
                if value.x() < 0: x = 0
                else: x = value.x()
                if value.y() < 0: y = 0
                else: y = value.y()
                value = QPointF(x,y)
                self.setPos(value)
                return
            #this works!
            # do other work, or emit signal
          
        return QGraphicsPixmapItem.itemChange(self, change, value)
    
    def showDialog(self, x, y):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(f'{self.filename}  Clicked  at ({x},{y})')
        msgBox.setWindowTitle("Do you want to CROP it?")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        cb = QCheckBox("Keep Image from cursor to Left or Down")
        msgBox.setCheckBox(cb)
        cb.setChecked(True)
        
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
           downRight = False
           downRight = bool(cb.isChecked())
           self.cropMe(x, y, downRight)
          


    def cropMe(self, x, y, downRight):
        """
        
        Parameters
        ----------
        x : int/ float
            x cursor position.
        y : int / float
            y cursor position
        downRight : boolean / int
            direction of crop
            True:  vertically remove from cursor to right edge
                   horizontally remove from top edge to cursor horizontal edge
            False: vertically remove from cursor to left edge
                   horizontally remove from cursor to bottom edge

        Returns
        -------
        None.

        """
        img = self.pixmap()
        w = img.width()
        h = img.height()
        if (abs(y-h) < 5) or abs(y) < 5:
            if downRight: #i.e. vertically remove from cursor to right edge
                x1 = 0
                y1 = 0
                x2 = int(x)
                y2 = int(h)
            else: #i.e. vertically remove from cursor to left edge
                x1 = int(x)
                y1 = 0
                x2 = int(w)
                y2 = int(h)
        elif (abs(x-w) < 5) or (abs(x) < 5):
            if downRight: #i.e. horizontally remove from top edge to cursor horizontal edge
                x1 = 0
                y1 = int(y)
                x2 = int(w)
                y2 = int(h)
            else: #i.e. horizontally remove from cursor to bottom edge
                x1 = 0
                y1 = 0
                x2 = int(w)
                y2 = int(y)
        else:
            x1 = 0
            y1 = 0
            x2 = int(w)
            y2 = int(h)
        rect = QRect(x1, y1, x2, y2)
        self.setPixmap(img.copy(rect))
        self.w = self.pixmap().width()
        self.h = self.pixmap().height()

class showText(QDialog):
    
    def __init__(self, fName):
        
        super(showText,self).__init__()
        self.webView = QWebEngineView(self)
        url = QUrl.fromLocalFile(fName)
        self.webView.load(url)
        self.ok_button = QPushButton('OK')       
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.webView)        
        layout.addWidget(self.ok_button) 
        self.ok_button.clicked.connect(self.end)
        self.setLayout(layout)
        self.show()
            
    def end(self):
        self.close()
