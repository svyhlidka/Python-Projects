# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 22:38:43 2021

@author: stvyh
this file is used to complete program with Qt Designer output

C:\Users\stvyh\OneDrive\Desktop\ImageProcessing\ImageProcessing

pyuic5 -x m1.ui -o elilik.py

C:/Temp/Data/test/shapes.png


ERROR:    ImportError: QtWebEngineWidgets must be imported before a QCoreApplication instance is created
solved:   runs from console only, not from Spyder!


"""


from PyQt5.QtGui import QImage, QPixmap, QPainter, QBrush, QColor
from PyQt5.QtGui     import QPalette, QFont, QFontMetrics, QStandardItem, QStandardItemModel
from PyQt5.QtCore    import Qt, QRect, QSize, QEvent, QCoreApplication, QMetaObject
from PyQt5.QtCore    import QPointF, QRectF, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtWidgets import QWidget, QDialogButtonBox, QCheckBox, QDial
from PyQt5.QtWidgets import QSizePolicy, QGridLayout, QFormLayout,QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QToolButton, QDoubleSpinBox, QLineEdit
from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate, qApp, QListView
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QFileDialog, QMessageBox, QDialog
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QPushButton, QAbstractScrollArea
from PyQt5.QtWidgets import QAction, QMenu, QMenuBar, QStatusBar
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QGroupBox, QFrame, QSlider
from functools import partial
import numpy as np
import cv2
import os
import sys

from ElilikClasses import Ui_INI_Dialog, ColorMapsDialog, TransformScene, showText


#  replace QtWidgets., QtGui.,  with ''

################ below self.graphicsView.setObjectName("graphicsView")
        self.scene = TransformScene()
        self.graphicsView.setScene(self.scene)
        
        ################## just above retlanslate
        
        self.scene.file_signal.connect(on_file_signal)
        self.scene.info_signal.connect(on_info_signal)
        self.scene.sliders_reset_signal.connect(on_sliders_reset_signal)

#########################################################################
        
        
        self.actionHelp.setShortcut('F1')
        self.actionHelp.setStatusTip('Help')  
        self.actionHelp.triggered.connect(self.showHelp)
        self.actionAbout.setStatusTip('About')  
        self.actionAbout.triggered.connect(self.showAbout)
        self.actionDefault_Values.setStatusTip('Default folders and other values')
        self.actionDefault_Values.triggered.connect(self.updateINI)
   
        self.addImgButton.clicked.connect(partial(self.scene.addImg))
        self.clearImgButton.clicked.connect(self.scene.dialogClearScene)
        self.saveSceneImgButton.clicked.connect(partial(self.scene.saveScene))
        self.saveImgButton.clicked.connect(partial(self.scene.saveImg))
        self.scaleBox.valueChanged.connect(self.onScaleBoxValueChanged)
        self.getSizeButton.clicked.connect(self.showSceneSize)
        self.brightnessButton.clicked.connect(self.startBrightnessAndBlur)
        self.gray2colAllButton.clicked.connect(self.startGray2colAllButton)
        self.gray2colSelButton.clicked.connect(self.startGray2colSelButton)
        self.adaptiveThresholdButton.clicked.connect(self.startAdaptiveThreshold)
        self.edgesButton.clicked.connect(self.startSobelXY)
        self.fftButton.clicked.connect(self.startFFT)
        self.dftButton.clicked.connect(self.startDFT)
        self.gaborButton.clicked.connect(self.startGabor)
        self.differenceButton.clicked.connect(self.startDifference)
        self.RGB2GrayButton.clicked.connect(self.starRGB2Gray)

        
 
        self.leftSlider.valueChanged['int'].connect(self. leftSliderChanged)
        self.rightSlider.valueChanged['int'].connect(self.rightSliderChanged)
        self.angleDial.valueChanged['int'].connect(self.angleDialChanged)
        
    def setStart(self):
        self.graphicsView.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.scene.setSceneRect(0, 0, 0, 0)
        self.scene.imgScale = self.scaleBox.value()
        self.clearSliders()
        self.infoLabel.setText("")
        self.scene.cv2Images = {}
        self.transformsGroupBox.setEnabled(False)
        self.transformsGroupBox.setEnabled(False)
        self.invertedCheckBox.setChecked(False)

        
        
    def clearSliders(self):
        self.infoLabel_2.setText('')
        self.infoLabel_3.setText('')
        self.scene.currentTransform = 0
        self.leftSlider.setEnabled(False)
        self.leftSlider.setToolTip("")
        self.leftSlider.setWhatsThis("")
        self.leftSlider.setMaximum(99)
        self.leftSlider.setMinimum(0)
        self.leftSlider.setTickInterval(10)        
        self.leftSlider.setSingleStep(1)
        self.leftSlider.setTickPosition(11)

        self.rightSlider.setEnabled(False)
        self.rightSlider.setToolTip("")
        self.rightSlider.setWhatsThis("")
        self.rightSlider.setMaximum(99)
        self.rightSlider.setMinimum(0)
        self.rightSlider.setTickInterval(10)        
        self.rightSlider.setSingleStep(1)
        self.rightSlider.setTickPosition(0) 
        self.paramsGroupBox.setFlat(False)
        self.paramsGroupBox.setStyleSheet('QGroupBox * {color: black; font-weight: normal;}') 
        
        self.angleDial.setEnabled(False)
        self.angleDial.setToolTip(" ")
        self.angleDial.setWhatsThis("")



    def invertCheckBoxEvent(self, checked):
        self.scene.inverted = checked
               
    def showSceneSize(self):
        x = self.scene.sceneRect().width()
        y = self.scene.sceneRect().height()      
        self.infoLabel.setText(f'size: {x}x{y}, {self.scene.findSceneArea()}')

    def onScaleBoxValueChanged(self, val):
        self.scene.imgScale = val
          
    def startBrightnessAndBlur(self):
        self.scene.currentTransform = 1
        self.infoLabel_2.setText('Adaptive Threshold')      
        self.scene.currentBrightnessValue = 0
        self.scene.currentBlurValue = 0
        self.scene.transform1()

        self.infoLabel_2.setText('Brightness and Blur')
        self.scene.currentTransform = 1
        self.leftSlider.setEnabled(True)
        self.rightSlider.setEnabled(True)
        self.leftSlider.setToolTip("Change Brightness  -> 0 .. 99")
        self.leftSlider.setWhatsThis("Change Brightness  -> 0 .. 99")
        self.rightSlider.setToolTip("Change Blur  -> 0 .. 99")
        self.rightSlider.setWhatsThis("Change Blur  -> 0 .. 99")
        self.leftSlider.setMaximum(99)
        self.leftSlider.setMinimum(0)
        self.leftSlider.setTickInterval(10)        
        self.leftSlider.setSingleStep(1)
        self.leftSlider.setTickPosition(11)
        self.rightSlider.setMaximum(99)
        self.rightSlider.setMinimum(0)
        self.rightSlider.setTickInterval(10)        
        self.rightSlider.setSingleStep(1)
        self.rightSlider.setTickPosition(0) 
        self.paramsGroupBox.setFlat(True)
        self.paramsGroupBox.setStyleSheet('QGroupBox * {color: red; font-weight: bold;}')
        
    def startGray2colAllButton(self):
        # show all available colorMaps
        self.infoLabel_2.setText('Gray to Color All Methods')
        self.scene.currentTransform = 2
        self.scene.transform2(1, 1)
        
    def startGray2colSelButton(self):
        #colorMaps with selection dialog
        self.scene.currentTransform = 3
        self.infoLabel_2.setText(' Gray to Color')
        self.scene.transform2(0, 1)   
   
    def startSobelXY(self):
        self.scene.currentTransform = 4
        self.infoLabel_2.setText('Edge Detection')
        self.scene.transform4()
 
    def startFFT(self):
        self.scene.currentTransform = 7
        self.infoLabel_2.setText('FFT')
        self.scene.transform7()
    
    def startDFT(self):
        self.scene.currentTransform = 6
        self.infoLabel_2.setText('DFT')
        self.scene.transform6()
        
    def startDenoising(self):
        self.scene.currentTransform = 8
        self.infoLabel_2.setText('Denoising')
        self.scene.transform8()
        
    def startDifference(self):
        self.scene.currentTransform = 9
        self.infoLabel_2.setText('Difference')
        self.scene.transform9()
        
    def starRGB2Gray(self):
        self.scene.currentTransform = 10
        #txt = self.infoLabel_2.text()
        self.infoLabel_2.setText('RGB to Gray')
        self.scene.transform10()
        
    def startAdaptiveThreshold(self):
        self.scene.currentTransform = 5
        self.infoLabel_2.setText('Adaptive Threshold')      
        self.scene.currentBlockSizeValue = 11
        self.scene.currentCValue = 5
        self.scene.transform5()

        self.leftSlider.setEnabled(True)
        self.rightSlider.setEnabled(True)
        self.leftSlider.setToolTip("Adaptive Threshold\n"
"blockSize – Size of a pixel neighborhood that is used to calculate a threshold value for the pixel: 3, 5, 7, and so on.")
        self.leftSlider.setWhatsThis("Adaptive Threshold\n"
"blockSize – Size of a pixel neighborhood that is used to calculate a threshold value for the pixel: 3, 5, 7, and so on.")
        self.rightSlider.setToolTip("Adaptive Threshold\n"
"C – Constant subtracted from the mean or weighted mean (see the details below). Normally, it is positive but may be zero or negative as well.")
        self.rightSlider.setWhatsThis("Adaptive Threshold\n"
"C – Constant subtracted from the mean or weighted mean (see the details below). Normally, it is positive but may be zero or negative as well.")
        self.leftSlider.setMaximum(16)
        self.leftSlider.setMinimum(1)
        self.leftSlider.setTickInterval(1)        
        self.leftSlider.setSingleStep(1)
        self.leftSlider.setTickPosition(11)
        self.rightSlider.setMaximum(20)
        self.rightSlider.setMinimum(-5)
        self.rightSlider.setTickInterval(1)        
        self.rightSlider.setSingleStep(1)
        self.rightSlider.setTickPosition(5)     
        self.paramsGroupBox.setFlat(True)
        self.paramsGroupBox.setStyleSheet('QGroupBox * {color: red; font-weight: bold;}')       

    def startGabor(self):
        self.scene.currentTransform = 8
        self.infoLabel_2.setText('Gabor Filter') 
        self.scene.currentKernelSizeValue = 10
        self.scene.currentSigmaValue = 10
        self.scene.thetaCurrentValue
        self.scene.transform8()
        self.angleDial.setEnabled(True)
        self.leftSlider.setEnabled(True)
        self.rightSlider.setEnabled(True)
        self.leftSlider.setToolTip("Gabor Filter\n"
                                  "kernelSize – Size of a kernel 1..50")
        self.leftSlider.setWhatsThis("Gabor Filter\n"
                                  "kernelSize – Size of a kernel")
        self.rightSlider.setToolTip("Gabor Filter\n"
                                  "Standard Deviation – 1..30")
        self.rightSlider.setWhatsThis("Gabor Filter\n"
                                  "Standard Deviation – 1..30")
        self.angleDial.setToolTip("GABOR Filter - angle 1..4 ~ 1*np.pi/angle")
        self.angleDial.setWhatsThis("GABOR Filter - angle 1..4 ~ 1*np.pi/angle")       
        self.leftSlider.setMaximum(50)
        self.leftSlider.setMinimum(1)
        self.leftSlider.setTickInterval(5)        
        self.leftSlider.setSingleStep(5)
        self.leftSlider.setTickPosition(10)
        self.rightSlider.setMaximum(30)
        self.rightSlider.setMinimum(1)
        self.rightSlider.setTickInterval(5)        
        self.rightSlider.setSingleStep(5)
        self.rightSlider.setTickPosition(10)     
        self.paramsGroupBox.setFlat(True)
        self.paramsGroupBox.setStyleSheet('QGroupBox * {color: red; font-weight: bold;}')       


    def leftSliderChanged(self, value):
        self.leftLabel.setText(str(value))
        if self.scene.currentTransform == 1:
            self.scene.currentBrightnessValue = value
        elif self.scene.currentTransform == 5:
            if value % 2 == 1:return 
            self.scene.currentBlockSizeValue = value
        elif self.scene.currentTransform == 8:
            self.scene.currentKernelSizeValue = value
        else:
            pass
        self.update()
                    
    def rightSliderChanged(self, value):
        self.rightLabel.setText(str(value))
        if self.scene.currentTransform == 1:
            self.scene.currentBlurValue = value
        elif self.scene.currentTransform == 5:
             self.scene.currentCValue = value
        elif self.scene.currentTransform == 8:
            self.scene.currentSigmaValue = value
        else:
            pass
        self.update()  

    def angleDialChanged(self, value): 
        if self.scene.currentTransform == 8:
            self.scene.thetaCurrentValue = value
        self.update()
           
    def update(self):
        if self.scene.currentTransform == 1:
            if len(self.scene.selectedItems()) > 0:
                self.scene.transform1()
        elif self.scene.currentTransform == 5:
            self.infoLabel_2.setText(f'Adaptive Threshold {self.scene.currentBlockSizeValue} {self.scene.currentCValue}')
            if len(self.scene.selectedItems()) > 0:
                self.scene.transform5()
        elif self.scene.currentTransform == 8:
            if len(self.scene.selectedItems()) > 0:
                self.scene.transform8()
        else:
            ...

    def updateINI(self):
        Dialog = QDialog()
        ui = Ui_INI_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        Dialog.exec_()
        self.readINI()
        
    def readINI(self):
        self.scene.source_dir = ''
        self.scene.result_dir = ''
        self.scene.color_map = '' 
        self.scene.scale = ''
        if os.path.exists("elilik.ini"):
            f = open("elilik.ini", "r")
            Lines = f.readlines()
            # Strips the newline character
            for line in Lines:
                l = line.strip()
                if "source_dir : " in l:
                    self.scene.source_dir = l.replace("source_dir : ","").strip()
                elif "result_dir : " in l:
                    self.scene.result_dir = l.replace("result_dir : ","").strip()  
                elif "color_map : " in l:
                     s = l.replace("color_map : ","").strip()
                     self.scene.color_map = s.split()
                elif "scale : " in l:
                    self.scene.scale = l.replace("scale : ","").strip()
                else:
                    ...

    def showHelp(self):
        help = showText(os.getcwd()+"/help.html") 
        help.exec_()
 
    def showAbout(self):
        about = showText(os.getcwd()+"/about.html")
        about.resize(280,250)
        about.exec_()
  

@pyqtSlot(str)
def on_file_signal(value):
    ui.infoLabel_3.setText(value)
    if len(ui.scene.selectedItems()) > 0:
        ui.transformsGroupBox.setEnabled(True)
    else:
        ui.transformsGroupBox.setEnabled(False)
        
@pyqtSlot(str)
def on_info_signal(value):
    ui.infoLabel.setText(value)
    
@pyqtSlot()
def on_sliders_reset_signal():
    ui.clearSliders()
    ui.transformsGroupBox.setEnabled(False)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.setStart()
    ui.readINI()
    MainWindow.show()
    MainWindow.showMaximized()
    sys.exit(app.exec_())

