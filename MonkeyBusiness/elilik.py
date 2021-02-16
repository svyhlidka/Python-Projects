# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'm1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

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
import sys
import cv2
import os

from ElilikClasses import Ui_INI_Dialog, ColorMapsDialog, TransformScene, showText


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1871, 1200)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.transformsGroupBox = QGroupBox(self.centralwidget)
        self.transformsGroupBox.setGeometry(QRect(1500, 170, 240, 500))
        self.transformsGroupBox.setMaximumSize(QSize(240, 600))
        font = QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.transformsGroupBox.setFont(font)
        self.transformsGroupBox.setToolTip("")
        self.transformsGroupBox.setWhatsThis("")
        self.transformsGroupBox.setObjectName("transformsGroupBox")
        self.edgesButton = QPushButton(self.transformsGroupBox)
        self.edgesButton.setGeometry(QRect(110, 180, 120, 30))
        self.edgesButton.setObjectName("edgesButton")
        self.brightnessButton = QPushButton(self.transformsGroupBox)
        self.brightnessButton.setGeometry(QRect(110, 20, 120, 30))
        font = QFont()
        font.setPointSize(8)
        self.brightnessButton.setFont(font)
        self.brightnessButton.setObjectName("brightnessButton")
        self.getSizeButton = QPushButton(self.transformsGroupBox)
        self.getSizeButton.setGeometry(QRect(0, 470, 75, 23))
        self.getSizeButton.setObjectName("getSizeButton")
        self.paramsGroupBox = QGroupBox(self.transformsGroupBox)
        self.paramsGroupBox.setGeometry(QRect(10, 29, 91, 321))
        font = QFont()
        font.setPointSize(8)
        self.paramsGroupBox.setFont(font)
        self.paramsGroupBox.setObjectName("paramsGroupBox")
        self.leftSlider = QSlider(self.paramsGroupBox)
        self.leftSlider.setGeometry(QRect(10, 50, 20, 240))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftSlider.sizePolicy().hasHeightForWidth())
        self.leftSlider.setSizePolicy(sizePolicy)
        self.leftSlider.setOrientation(Qt.Vertical)
        self.leftSlider.setTickPosition(QSlider.TicksAbove)
        self.leftSlider.setObjectName("leftSlider")
        self.rightSlider = QSlider(self.paramsGroupBox)
        self.rightSlider.setGeometry(QRect(50, 50, 20, 240))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rightSlider.sizePolicy().hasHeightForWidth())
        self.rightSlider.setSizePolicy(sizePolicy)
        self.rightSlider.setOrientation(Qt.Vertical)
        self.rightSlider.setTickPosition(QSlider.TicksAbove)
        self.rightSlider.setObjectName("rightSlider")
        self.leftLabel = QLabel(self.paramsGroupBox)
        self.leftLabel.setGeometry(QRect(10, 20, 20, 15))
        self.leftLabel.setTextFormat(Qt.PlainText)
        self.leftLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.leftLabel.setObjectName("leftLabel")
        self.rightLabel = QLabel(self.paramsGroupBox)
        self.rightLabel.setGeometry(QRect(50, 20, 20, 15))
        self.rightLabel.setTextFormat(Qt.PlainText)
        self.rightLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.rightLabel.setObjectName("rightLabel")
        self.adaptiveThresholdButton = QPushButton(self.transformsGroupBox)
        self.adaptiveThresholdButton.setGeometry(QRect(110, 140, 120, 30))
        font = QFont()
        font.setPointSize(8)
        self.adaptiveThresholdButton.setFont(font)
        self.adaptiveThresholdButton.setObjectName("adaptiveThresholdButton")
        self.gray2colSelButton = QPushButton(self.transformsGroupBox)
        self.gray2colSelButton.setGeometry(QRect(110, 100, 120, 30))
        font = QFont()
        font.setPointSize(8)
        self.gray2colSelButton.setFont(font)
        self.gray2colSelButton.setObjectName("gray2colSelButton")
        self.gray2colAllButton = QPushButton(self.transformsGroupBox)
        self.gray2colAllButton.setGeometry(QRect(110, 60, 120, 30))
        font = QFont()
        font.setPointSize(8)
        self.gray2colAllButton.setFont(font)
        self.gray2colAllButton.setObjectName("gray2colAllButton")
        self.fftButton = QPushButton(self.transformsGroupBox)
        self.fftButton.setGeometry(QRect(110, 220, 120, 30))
        self.fftButton.setObjectName("fftButton")
        self.dftButton = QPushButton(self.transformsGroupBox)
        self.dftButton.setGeometry(QRect(110, 260, 120, 30))
        self.dftButton.setObjectName("dftButton")
        self.gaborButton = QPushButton(self.transformsGroupBox)
        self.gaborButton.setGeometry(QRect(110, 300, 120, 30))
        self.gaborButton.setObjectName("gaborButton")
        self.differenceButton = QPushButton(self.transformsGroupBox)
        self.differenceButton.setGeometry(QRect(110, 340, 120, 30))
        self.differenceButton.setObjectName("differenceButton")
        self.RGB2GrayButton = QPushButton(self.transformsGroupBox)
        self.RGB2GrayButton.setGeometry(QRect(110, 380, 120, 30))
        self.RGB2GrayButton.setObjectName("RGB2GrayButton")
        self.invertedCheckBox = QCheckBox(self.transformsGroupBox)
        self.invertedCheckBox.setGeometry(QRect(110, 430, 121, 17))
        self.invertedCheckBox.setObjectName("invertedCheckBox")
        self.angleDial = QDial(self.transformsGroupBox)
        self.angleDial.setGeometry(QRect(20, 360, 81, 64))
        self.angleDial.setMinimum(1)
        self.angleDial.setMaximum(4)
        self.angleDial.setPageStep(1)
        self.angleDial.setSliderPosition(1)
        self.angleDial.setWrapping(False)
        self.angleDial.setNotchesVisible(True)
        self.angleDial.setObjectName("angleDial")
        self.groupButtonsBox = QGroupBox(self.centralwidget)
        self.groupButtonsBox.setGeometry(QRect(1500, 730, 241, 141))
        self.groupButtonsBox.setMaximumSize(QSize(250, 600))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupButtonsBox.setFont(font)
        self.groupButtonsBox.setObjectName("groupButtonsBox")
        self.addImgButton = QPushButton(self.groupButtonsBox)
        self.addImgButton.setGeometry(QRect(50, 20, 150, 30))
        palette = QPalette()
        brush = QBrush(QColor(180, 146, 66))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        brush = QBrush(QColor(180, 146, 66))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        brush = QBrush(QColor(180, 146, 66))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        self.addImgButton.setPalette(palette)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.addImgButton.setFont(font)
        self.addImgButton.setObjectName("addImgButton")
        self.saveSceneImgButton = QPushButton(self.groupButtonsBox)
        self.saveSceneImgButton.setGeometry(QRect(50, 60, 150, 30))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.saveSceneImgButton.setFont(font)
        self.saveSceneImgButton.setObjectName("saveSceneImgButton")
        self.saveImgButton = QPushButton(self.groupButtonsBox)
        self.saveImgButton.setGeometry(QRect(50, 100, 150, 30))
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.saveImgButton.setFont(font)
        self.saveImgButton.setObjectName("saveImgButton")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QRect(10, 15, 1471, 900))
        self.graphicsView.setMaximumSize(QSize(4000, 3000))
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.graphicsView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.graphicsView.setObjectName("graphicsView")
        self.scene = TransformScene()
        self.graphicsView.setScene(self.scene)
        self.scaleEditLabel = QLabel(self.centralwidget)
        self.scaleEditLabel.setGeometry(QRect(1500, 100, 47, 13))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.scaleEditLabel.setFont(font)
        self.scaleEditLabel.setObjectName("scaleEditLabel")
        self.scaleBox = QDoubleSpinBox(self.centralwidget)
        self.scaleBox.setGeometry(QRect(1550, 100, 62, 22))
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.scaleBox.setFont(font)
        self.scaleBox.setMinimum(0.1)
        self.scaleBox.setMaximum(10.0)
        self.scaleBox.setSingleStep(0.1)
        self.scaleBox.setProperty("value", 0.5)
        self.scaleBox.setObjectName("scaleBox")
        self.infoLabel = QLabel(self.centralwidget)
        self.infoLabel.setGeometry(QRect(1499, 130, 230, 20))
        self.infoLabel.setFrameShape(QFrame.WinPanel)
        self.infoLabel.setText("")
        self.infoLabel.setAlignment(Qt.AlignCenter)
        self.infoLabel.setObjectName("infoLabel")
        self.infoLabel_2 = QLabel(self.centralwidget)
        self.infoLabel_2.setGeometry(QRect(1500, 20, 230, 20))
        font = QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.infoLabel_2.setFont(font)
        self.infoLabel_2.setFrameShape(QFrame.WinPanel)
        self.infoLabel_2.setText("")
        self.infoLabel_2.setAlignment(Qt.AlignCenter)
        self.infoLabel_2.setObjectName("infoLabel_2")
        self.infoLabel_3 = QLabel(self.centralwidget)
        self.infoLabel_3.setGeometry(QRect(1500, 60, 230, 20))
        font = QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.infoLabel_3.setFont(font)
        self.infoLabel_3.setFrameShape(QFrame.Box)
        self.infoLabel_3.setText("")
        self.infoLabel_3.setAlignment(Qt.AlignCenter)
        self.infoLabel_3.setObjectName("infoLabel_3")
        self.clearImgButton = QPushButton(self.centralwidget)
        self.clearImgButton.setGeometry(QRect(1550, 690, 150, 30))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.clearImgButton.setFont(font)
        self.clearImgButton.setObjectName("clearImgButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1871, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionHelp = QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionDefault_Values = QAction(MainWindow)
        self.actionDefault_Values.setObjectName("actionDefault_Values")
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionDefault_Values)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
        self.scene.file_signal.connect(on_file_signal)
        self.scene.info_signal.connect(on_info_signal)
        self.scene.sliders_reset_signal.connect(on_sliders_reset_signal)
        

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Green Monkey"))
        self.transformsGroupBox.setTitle(_translate("MainWindow", "Transformations"))
        self.edgesButton.setText(_translate("MainWindow", "Edges, Sobel"))
        self.brightnessButton.setToolTip(_translate("MainWindow", "You can change brightness with left slider and blur with rigt one."))
        self.brightnessButton.setWhatsThis(_translate("MainWindow", "You can change brightness with left slider and blur with rigt one."))
        self.brightnessButton.setText(_translate("MainWindow", "Brightness and Blur"))
        self.getSizeButton.setText(_translate("MainWindow", "get Size"))
        self.paramsGroupBox.setTitle(_translate("MainWindow", "Parameters"))
        self.leftSlider.setToolTip(_translate("MainWindow", "Adaptive Threshold\n"
"blockSize – Size of a pixel neighborhood that is used to calculate a threshold value for the pixel: 3, 5, 7, and so on."))
        self.leftSlider.setWhatsThis(_translate("MainWindow", "Adaptive Threshold\n"
"blockSize – Size of a pixel neighborhood that is used to calculate a threshold value for the pixel: 3, 5, 7, and so on."))
        self.rightSlider.setToolTip(_translate("MainWindow", "Adaptive Threshold\n"
"C – Constant subtracted from the mean or weighted mean (see the details below). Normally, it is positive but may be zero or negative as well."))
        self.rightSlider.setWhatsThis(_translate("MainWindow", "Adaptive Threshold\n"
"C – Constant subtracted from the mean or weighted mean (see the details below). Normally, it is positive but may be zero or negative as well."))
        self.leftLabel.setText(_translate("MainWindow", "0"))
        self.rightLabel.setText(_translate("MainWindow", "0"))
        self.adaptiveThresholdButton.setText(_translate("MainWindow", "Adaptive Threshold"))
        self.gray2colSelButton.setToolTip(_translate("MainWindow", "Gray scale 0..255 to color with selected method only.\n"
"Image is converted to gray and finally to color."))
        self.gray2colSelButton.setWhatsThis(_translate("MainWindow", "Gray scale 0..255 to color with selected method only.\n"
"Image is converted to gray and  and finally to color."))
        self.gray2colSelButton.setText(_translate("MainWindow", "Gray2Color Sel."))
        self.gray2colAllButton.setToolTip(_translate("MainWindow", "Gray scale 0..255 to color for all available methods.\n"
"Image resized as per scale window and then  is converted to gray and finally to color."))
        self.gray2colAllButton.setWhatsThis(_translate("MainWindow", "Gray scale 0..255 to color for all available methods.\n"
"Image resized as per scale window and then  is converted to gray and finally to color."))
        self.gray2colAllButton.setText(_translate("MainWindow", "Gray2Color All"))
        self.fftButton.setText(_translate("MainWindow", "FFT"))
        self.dftButton.setText(_translate("MainWindow", "DFT"))
        self.gaborButton.setToolTip(_translate("MainWindow", "Applies Gabor Filter"))
        self.gaborButton.setWhatsThis(_translate("MainWindow", "Applies Gabor Filter"))
        self.gaborButton.setText(_translate("MainWindow", "Gabor Filter"))
        self.differenceButton.setText(_translate("MainWindow", "Difference"))
        self.RGB2GrayButton.setText(_translate("MainWindow", "RGB to Gray"))
        self.invertedCheckBox.setText(_translate("MainWindow", "Inverted Image"))
        self.angleDial.setToolTip(_translate("MainWindow", "GABOR Filter - angle 1..4 ~ 1*np.pi/angle"))
        self.angleDial.setWhatsThis(_translate("MainWindow", "GABOR Filter - angle 1..4 ~ 1*np.pi/angle"))
        self.groupButtonsBox.setTitle(_translate("MainWindow", "Images"))
        self.addImgButton.setText(_translate("MainWindow", "Add Image(s)"))
        self.addImgButton.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.saveSceneImgButton.setText(_translate("MainWindow", "Save Scene as Image"))
        self.saveImgButton.setText(_translate("MainWindow", "Save Selected as Image"))
        self.scaleEditLabel.setText(_translate("MainWindow", "Scale:"))
        self.clearImgButton.setText(_translate("MainWindow", "Clear Image(s)"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionDefault_Values.setText(_translate("MainWindow", "Default Values"))

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
        self.infoLabel_2.setText('Gray to Color All Methods')
        self.scene.currentTransform = 2
        self.scene.transform2(1, 1)
        
    def startGray2colSelButton(self):
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

