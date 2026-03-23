# -*- coding: utf-8 -*-

# This file is part of the Blob Inspector project
# 
# Blob Inspector project is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Blob Inspector project is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Blob Inspector project. If not, see <http://www.gnu.org/licenses/>.
#
# Author: Laurent Busson
# Version: 0.9
# Date: 2024-05-28

################################################################################
## Form generated from reading UI file 'batch_analysis_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)
import resources.resources_rc

class Ui_BatchAnalysisWindow(object):
    def setupUi(self, BatchAnalysisWindow):
        if not BatchAnalysisWindow.objectName():
            BatchAnalysisWindow.setObjectName(u"BatchAnalysisWindow")
        BatchAnalysisWindow.resize(713, 410)
        BatchAnalysisWindow.setFocusPolicy(Qt.NoFocus)
        icon = QIcon()
        icon.addFile(u":/Icons/blob-161097_640.png", QSize(), QIcon.Normal, QIcon.Off)
        BatchAnalysisWindow.setWindowIcon(icon)
        self.gridLayout_6 = QGridLayout(BatchAnalysisWindow)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gb_Segmentation = QGroupBox(BatchAnalysisWindow)
        self.gb_Segmentation.setObjectName(u"gb_Segmentation")
        self.gb_Segmentation.setMinimumSize(QSize(340, 0))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.gb_Segmentation.setFont(font)
        self.gb_Segmentation.setAlignment(Qt.AlignCenter)
        self.gridLayout_2 = QGridLayout(self.gb_Segmentation)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.combob_Threshold = QComboBox(self.gb_Segmentation)
        self.combob_Threshold.addItem("")
        self.combob_Threshold.addItem("")
        self.combob_Threshold.setObjectName(u"combob_Threshold")
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setUnderline(False)
        self.combob_Threshold.setFont(font1)

        self.gridLayout_2.addWidget(self.combob_Threshold, 0, 0, 1, 1)

        self.le_ThresholdOne = QLineEdit(self.gb_Segmentation)
        self.le_ThresholdOne.setObjectName(u"le_ThresholdOne")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_ThresholdOne.sizePolicy().hasHeightForWidth())
        self.le_ThresholdOne.setSizePolicy(sizePolicy)
        self.le_ThresholdOne.setMinimumSize(QSize(40, 0))
        self.le_ThresholdOne.setMaximumSize(QSize(40, 16777215))
        self.le_ThresholdOne.setFont(font1)

        self.gridLayout_2.addWidget(self.le_ThresholdOne, 0, 1, 1, 1)

        self.le_ThresholdTwo = QLineEdit(self.gb_Segmentation)
        self.le_ThresholdTwo.setObjectName(u"le_ThresholdTwo")
        self.le_ThresholdTwo.setEnabled(False)
        sizePolicy.setHeightForWidth(self.le_ThresholdTwo.sizePolicy().hasHeightForWidth())
        self.le_ThresholdTwo.setSizePolicy(sizePolicy)
        self.le_ThresholdTwo.setMinimumSize(QSize(40, 0))
        self.le_ThresholdTwo.setMaximumSize(QSize(40, 16777215))
        self.le_ThresholdTwo.setFont(font1)

        self.gridLayout_2.addWidget(self.le_ThresholdTwo, 0, 2, 1, 1)

        self.combob_BlobsDetection = QComboBox(self.gb_Segmentation)
        self.combob_BlobsDetection.setObjectName(u"combob_BlobsDetection")
        self.combob_BlobsDetection.setFont(font1)

        self.gridLayout_2.addWidget(self.combob_BlobsDetection, 1, 0, 1, 1)

        self.le_BlobsDetectionMinimumRadius = QLineEdit(self.gb_Segmentation)
        self.le_BlobsDetectionMinimumRadius.setObjectName(u"le_BlobsDetectionMinimumRadius")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.le_BlobsDetectionMinimumRadius.sizePolicy().hasHeightForWidth())
        self.le_BlobsDetectionMinimumRadius.setSizePolicy(sizePolicy1)
        self.le_BlobsDetectionMinimumRadius.setMinimumSize(QSize(40, 0))
        self.le_BlobsDetectionMinimumRadius.setMaximumSize(QSize(40, 16777215))
        self.le_BlobsDetectionMinimumRadius.setFont(font1)

        self.gridLayout_2.addWidget(self.le_BlobsDetectionMinimumRadius, 1, 1, 1, 1)

        self.le_BlobsDetectionMaximumRadius = QLineEdit(self.gb_Segmentation)
        self.le_BlobsDetectionMaximumRadius.setObjectName(u"le_BlobsDetectionMaximumRadius")
        sizePolicy.setHeightForWidth(self.le_BlobsDetectionMaximumRadius.sizePolicy().hasHeightForWidth())
        self.le_BlobsDetectionMaximumRadius.setSizePolicy(sizePolicy)
        self.le_BlobsDetectionMaximumRadius.setMinimumSize(QSize(40, 0))
        self.le_BlobsDetectionMaximumRadius.setMaximumSize(QSize(40, 16777215))
        self.le_BlobsDetectionMaximumRadius.setFont(font1)

        self.gridLayout_2.addWidget(self.le_BlobsDetectionMaximumRadius, 1, 2, 1, 1)


        self.gridLayout_6.addWidget(self.gb_Segmentation, 0, 3, 1, 3)

        self.gb_StackInfo = QGroupBox(BatchAnalysisWindow)
        self.gb_StackInfo.setObjectName(u"gb_StackInfo")
        self.gb_StackInfo.setMinimumSize(QSize(340, 0))
        self.gb_StackInfo.setFont(font)
        self.gb_StackInfo.setAlignment(Qt.AlignCenter)
        self.gridLayout_7 = QGridLayout(self.gb_StackInfo)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.horizontalSpacer_12 = QSpacerItem(15, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_12, 1, 5, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(15, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_10, 1, 2, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(15, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_9, 1, 3, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(15, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_11, 1, 6, 1, 1)

        self.le_PixelSize = QLineEdit(self.gb_StackInfo)
        self.le_PixelSize.setObjectName(u"le_PixelSize")
        sizePolicy.setHeightForWidth(self.le_PixelSize.sizePolicy().hasHeightForWidth())
        self.le_PixelSize.setSizePolicy(sizePolicy)
        self.le_PixelSize.setMinimumSize(QSize(40, 26))
        self.le_PixelSize.setMaximumSize(QSize(40, 26))
        self.le_PixelSize.setBaseSize(QSize(40, 26))
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(False)
        self.le_PixelSize.setFont(font2)
        self.le_PixelSize.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.le_PixelSize, 1, 7, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(15, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_8, 1, 0, 1, 1)

        self.le_ZThickness = QLineEdit(self.gb_StackInfo)
        self.le_ZThickness.setObjectName(u"le_ZThickness")
        sizePolicy.setHeightForWidth(self.le_ZThickness.sizePolicy().hasHeightForWidth())
        self.le_ZThickness.setSizePolicy(sizePolicy)
        self.le_ZThickness.setMinimumSize(QSize(40, 26))
        self.le_ZThickness.setMaximumSize(QSize(40, 26))
        self.le_ZThickness.setBaseSize(QSize(40, 26))
        self.le_ZThickness.setFont(font2)
        self.le_ZThickness.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.le_ZThickness, 1, 1, 1, 1)

        self.le_InterZ = QLineEdit(self.gb_StackInfo)
        self.le_InterZ.setObjectName(u"le_InterZ")
        sizePolicy.setHeightForWidth(self.le_InterZ.sizePolicy().hasHeightForWidth())
        self.le_InterZ.setSizePolicy(sizePolicy)
        self.le_InterZ.setMinimumSize(QSize(40, 26))
        self.le_InterZ.setMaximumSize(QSize(40, 26))
        self.le_InterZ.setBaseSize(QSize(40, 26))
        self.le_InterZ.setFont(font2)
        self.le_InterZ.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.le_InterZ, 1, 4, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(15, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_13, 1, 8, 1, 1)

        self.label_3 = QLabel(self.gb_StackInfo)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 0))
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_3, 0, 6, 1, 3)

        self.label_2 = QLabel(self.gb_StackInfo)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 0))
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label_2, 0, 3, 1, 3)

        self.label = QLabel(self.gb_StackInfo)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 0))
        self.label.setFont(font2)
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_7.addWidget(self.label, 0, 0, 1, 3)


        self.gridLayout_6.addWidget(self.gb_StackInfo, 2, 3, 1, 3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 3, 1, 1, 1)

        self.gb_Density = QGroupBox(BatchAnalysisWindow)
        self.gb_Density.setObjectName(u"gb_Density")
        self.gb_Density.setMinimumSize(QSize(340, 0))
        self.gb_Density.setFont(font)
        self.gb_Density.setAlignment(Qt.AlignCenter)
        self.gridLayout_5 = QGridLayout(self.gb_Density)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.lb_ContoursMinSize = QLabel(self.gb_Density)
        self.lb_ContoursMinSize.setObjectName(u"lb_ContoursMinSize")
        self.lb_ContoursMinSize.setFont(font2)

        self.gridLayout_5.addWidget(self.lb_ContoursMinSize, 1, 2, 1, 1)

        self.le_BackgroundThreshold = QLineEdit(self.gb_Density)
        self.le_BackgroundThreshold.setObjectName(u"le_BackgroundThreshold")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.le_BackgroundThreshold.sizePolicy().hasHeightForWidth())
        self.le_BackgroundThreshold.setSizePolicy(sizePolicy2)
        self.le_BackgroundThreshold.setMinimumSize(QSize(40, 0))
        self.le_BackgroundThreshold.setMaximumSize(QSize(40, 16777215))
        self.le_BackgroundThreshold.setFont(font2)

        self.gridLayout_5.addWidget(self.le_BackgroundThreshold, 1, 1, 1, 1)

        self.lb_BackgroundThreshold = QLabel(self.gb_Density)
        self.lb_BackgroundThreshold.setObjectName(u"lb_BackgroundThreshold")
        self.lb_BackgroundThreshold.setFont(font2)
        self.lb_BackgroundThreshold.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_5.addWidget(self.lb_BackgroundThreshold, 1, 0, 1, 1)

        self.le_ContoursMinSize = QLineEdit(self.gb_Density)
        self.le_ContoursMinSize.setObjectName(u"le_ContoursMinSize")
        self.le_ContoursMinSize.setMinimumSize(QSize(40, 0))
        self.le_ContoursMinSize.setMaximumSize(QSize(40, 16777215))
        self.le_ContoursMinSize.setFont(font2)

        self.gridLayout_5.addWidget(self.le_ContoursMinSize, 1, 3, 1, 1)

        self.combob_Contours = QComboBox(self.gb_Density)
        self.combob_Contours.setObjectName(u"combob_Contours")
        self.combob_Contours.setFont(font2)

        self.gridLayout_5.addWidget(self.combob_Contours, 0, 0, 1, 4)


        self.gridLayout_6.addWidget(self.gb_Density, 1, 3, 1, 3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer, 3, 3, 1, 1)

        self.pb_StartAnalysis = QPushButton(BatchAnalysisWindow)
        self.pb_StartAnalysis.setObjectName(u"pb_StartAnalysis")

        self.gridLayout_6.addWidget(self.pb_StartAnalysis, 3, 5, 1, 1)

        self.pb_Cancel = QPushButton(BatchAnalysisWindow)
        self.pb_Cancel.setObjectName(u"pb_Cancel")

        self.gridLayout_6.addWidget(self.pb_Cancel, 3, 0, 1, 1)

        self.gb_Contours = QGroupBox(BatchAnalysisWindow)
        self.gb_Contours.setObjectName(u"gb_Contours")
        self.gb_Contours.setMinimumSize(QSize(340, 0))
        self.gb_Contours.setFont(font)
        self.gb_Contours.setFocusPolicy(Qt.NoFocus)
        self.gb_Contours.setAlignment(Qt.AlignCenter)
        self.gridLayout_4 = QGridLayout(self.gb_Contours)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.le_DensityMapKernelSize = QLineEdit(self.gb_Contours)
        self.le_DensityMapKernelSize.setObjectName(u"le_DensityMapKernelSize")
        sizePolicy2.setHeightForWidth(self.le_DensityMapKernelSize.sizePolicy().hasHeightForWidth())
        self.le_DensityMapKernelSize.setSizePolicy(sizePolicy2)
        self.le_DensityMapKernelSize.setMinimumSize(QSize(40, 0))
        self.le_DensityMapKernelSize.setMaximumSize(QSize(40, 16777215))
        self.le_DensityMapKernelSize.setFont(font2)

        self.gridLayout_4.addWidget(self.le_DensityMapKernelSize, 0, 5, 1, 1)

        self.lb_Layers = QLabel(self.gb_Contours)
        self.lb_Layers.setObjectName(u"lb_Layers")
        self.lb_Layers.setFont(font2)
        self.lb_Layers.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.lb_Layers, 1, 3, 1, 1)

        self.le_DensityTargetLayers = QLineEdit(self.gb_Contours)
        self.le_DensityTargetLayers.setObjectName(u"le_DensityTargetLayers")
        sizePolicy2.setHeightForWidth(self.le_DensityTargetLayers.sizePolicy().hasHeightForWidth())
        self.le_DensityTargetLayers.setSizePolicy(sizePolicy2)
        self.le_DensityTargetLayers.setMinimumSize(QSize(40, 0))
        self.le_DensityTargetLayers.setMaximumSize(QSize(40, 16777215))
        self.le_DensityTargetLayers.setFont(font2)

        self.gridLayout_4.addWidget(self.le_DensityTargetLayers, 1, 5, 1, 1)

        self.lb_Kernel = QLabel(self.gb_Contours)
        self.lb_Kernel.setObjectName(u"lb_Kernel")
        self.lb_Kernel.setFont(font2)
        self.lb_Kernel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.lb_Kernel, 0, 3, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_7, 0, 6, 1, 1)


        self.gridLayout_6.addWidget(self.gb_Contours, 2, 0, 1, 3)

        self.gb_Labeling = QGroupBox(BatchAnalysisWindow)
        self.gb_Labeling.setObjectName(u"gb_Labeling")
        self.gb_Labeling.setMinimumSize(QSize(340, 0))
        self.gb_Labeling.setFont(font)
        self.gb_Labeling.setAlignment(Qt.AlignCenter)
        self.gridLayout_3 = QGridLayout(self.gb_Labeling)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lb_SieveSize = QLabel(self.gb_Labeling)
        self.lb_SieveSize.setObjectName(u"lb_SieveSize")
        self.lb_SieveSize.setFont(font2)
        self.lb_SieveSize.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.lb_SieveSize, 1, 0, 1, 1)

        self.le_SieveSize = QLineEdit(self.gb_Labeling)
        self.le_SieveSize.setObjectName(u"le_SieveSize")
        sizePolicy2.setHeightForWidth(self.le_SieveSize.sizePolicy().hasHeightForWidth())
        self.le_SieveSize.setSizePolicy(sizePolicy2)
        self.le_SieveSize.setMinimumSize(QSize(40, 0))
        self.le_SieveSize.setMaximumSize(QSize(40, 16777215))
        self.le_SieveSize.setFont(font2)

        self.gridLayout_3.addWidget(self.le_SieveSize, 1, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 1, 2, 1, 1)

        self.combob_LabelingOption = QComboBox(self.gb_Labeling)
        self.combob_LabelingOption.setObjectName(u"combob_LabelingOption")
        self.combob_LabelingOption.setFont(font2)

        self.gridLayout_3.addWidget(self.combob_LabelingOption, 0, 0, 1, 3)


        self.gridLayout_6.addWidget(self.gb_Labeling, 1, 0, 1, 3)

        self.gb_Illumination = QGroupBox(BatchAnalysisWindow)
        self.gb_Illumination.setObjectName(u"gb_Illumination")
        self.gb_Illumination.setMinimumSize(QSize(340, 0))
        self.gb_Illumination.setFont(font)
        self.gb_Illumination.setAlignment(Qt.AlignCenter)
        self.gridLayout = QGridLayout(self.gb_Illumination)
        self.gridLayout.setObjectName(u"gridLayout")
        self.le_RollingBallRadius = QLineEdit(self.gb_Illumination)
        self.le_RollingBallRadius.setObjectName(u"le_RollingBallRadius")
        sizePolicy2.setHeightForWidth(self.le_RollingBallRadius.sizePolicy().hasHeightForWidth())
        self.le_RollingBallRadius.setSizePolicy(sizePolicy2)
        self.le_RollingBallRadius.setMinimumSize(QSize(40, 0))
        self.le_RollingBallRadius.setMaximumSize(QSize(40, 16777215))
        self.le_RollingBallRadius.setFont(font2)

        self.gridLayout.addWidget(self.le_RollingBallRadius, 0, 1, 1, 1)

        self.lb_RollingBallRadius = QLabel(self.gb_Illumination)
        self.lb_RollingBallRadius.setObjectName(u"lb_RollingBallRadius")
        self.lb_RollingBallRadius.setFont(font2)
        self.lb_RollingBallRadius.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.lb_RollingBallRadius.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lb_RollingBallRadius, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 0, 2, 1, 1)


        self.gridLayout_6.addWidget(self.gb_Illumination, 0, 0, 1, 3)

        self.pb_DefaultOptions = QPushButton(BatchAnalysisWindow)
        self.pb_DefaultOptions.setObjectName(u"pb_DefaultOptions")

        self.gridLayout_6.addWidget(self.pb_DefaultOptions, 3, 4, 1, 1)

        QWidget.setTabOrder(self.le_RollingBallRadius, self.combob_Threshold)
        QWidget.setTabOrder(self.combob_Threshold, self.le_ThresholdOne)
        QWidget.setTabOrder(self.le_ThresholdOne, self.le_ThresholdTwo)
        QWidget.setTabOrder(self.le_ThresholdTwo, self.combob_BlobsDetection)
        QWidget.setTabOrder(self.combob_BlobsDetection, self.le_BlobsDetectionMinimumRadius)
        QWidget.setTabOrder(self.le_BlobsDetectionMinimumRadius, self.le_BlobsDetectionMaximumRadius)
        QWidget.setTabOrder(self.le_BlobsDetectionMaximumRadius, self.combob_LabelingOption)
        QWidget.setTabOrder(self.combob_LabelingOption, self.le_SieveSize)
        QWidget.setTabOrder(self.le_SieveSize, self.combob_Contours)
        QWidget.setTabOrder(self.combob_Contours, self.le_BackgroundThreshold)
        QWidget.setTabOrder(self.le_BackgroundThreshold, self.le_ContoursMinSize)
        QWidget.setTabOrder(self.le_ContoursMinSize, self.le_DensityMapKernelSize)
        QWidget.setTabOrder(self.le_DensityMapKernelSize, self.le_DensityTargetLayers)
        QWidget.setTabOrder(self.le_DensityTargetLayers, self.le_ZThickness)
        QWidget.setTabOrder(self.le_ZThickness, self.le_InterZ)
        QWidget.setTabOrder(self.le_InterZ, self.le_PixelSize)
        QWidget.setTabOrder(self.le_PixelSize, self.pb_StartAnalysis)
        QWidget.setTabOrder(self.pb_StartAnalysis, self.pb_Cancel)
        QWidget.setTabOrder(self.pb_Cancel, self.pb_DefaultOptions)

        self.retranslateUi(BatchAnalysisWindow)

        QMetaObject.connectSlotsByName(BatchAnalysisWindow)
    # setupUi

    def retranslateUi(self, BatchAnalysisWindow):
        BatchAnalysisWindow.setWindowTitle(QCoreApplication.translate("BatchAnalysisWindow", u"Batch analysis", None))
        self.gb_Segmentation.setTitle(QCoreApplication.translate("BatchAnalysisWindow", u"Segmentation", None))
        self.combob_Threshold.setItemText(0, QCoreApplication.translate("BatchAnalysisWindow", u"One threshold", None))
        self.combob_Threshold.setItemText(1, QCoreApplication.translate("BatchAnalysisWindow", u"Two thresholds", None))

#if QT_CONFIG(tooltip)
        self.combob_Threshold.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Choose thresholding option.", None))
#endif // QT_CONFIG(tooltip)
        self.combob_Threshold.setCurrentText(QCoreApplication.translate("BatchAnalysisWindow", u"One threshold", None))
#if QT_CONFIG(tooltip)
        self.le_ThresholdOne.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the value of the threshold from 0 to 255 or from 0 to 1.", u"Input the value of the threshold either from 0 to 255 or from 0 to 1."))
#endif // QT_CONFIG(tooltip)
        self.le_ThresholdOne.setText(QCoreApplication.translate("BatchAnalysisWindow", u"I", None))
#if QT_CONFIG(tooltip)
        self.le_ThresholdTwo.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the value of the second threshold from 0 to 255 or from 0 to 1. The value must be less than the one of the first threshold.", None))
#endif // QT_CONFIG(tooltip)
        self.le_ThresholdTwo.setText(QCoreApplication.translate("BatchAnalysisWindow", u"II", None))
#if QT_CONFIG(tooltip)
        self.combob_BlobsDetection.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Laplacian of Gaussian (LoG), Difference of Gaussian (DoG), Determinant of Hessian (DoH)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.le_BlobsDetectionMinimumRadius.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the minimum value of the blobs radius in pixels. Smaller blobs won't be detected.", None))
#endif // QT_CONFIG(tooltip)
        self.le_BlobsDetectionMinimumRadius.setText(QCoreApplication.translate("BatchAnalysisWindow", u"min", None))
#if QT_CONFIG(tooltip)
        self.le_BlobsDetectionMaximumRadius.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the maximum value of the blobs radius in pixels. Bigger blobs won't be detected.", None))
#endif // QT_CONFIG(tooltip)
        self.le_BlobsDetectionMaximumRadius.setText(QCoreApplication.translate("BatchAnalysisWindow", u"max", None))
        self.gb_StackInfo.setTitle(QCoreApplication.translate("BatchAnalysisWindow", u"Stack informations", None))
#if QT_CONFIG(tooltip)
        self.le_PixelSize.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the size of a pixel. Choose the same unit for the 3 parameters in the results section.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.le_ZThickness.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the thickness of each slice. Choose the same unit for the 3 parameters in the results section.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.le_InterZ.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the distance between each slice. Choose the same unit for the 3 parameters in the results section.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_3.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the size of a pixel. Choose the same unit for the 3 parameters in the results section.", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("BatchAnalysisWindow", u"Pixel\n"
"size", None))
#if QT_CONFIG(tooltip)
        self.label_2.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the distance between each slice. Choose the same unit for the 3 parameters in the results section.", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("BatchAnalysisWindow", u"Interslice\n"
"space", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the thickness of each slice. Choose the same unit for the 3 parameters in the results section.", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("BatchAnalysisWindow", u"Slice\n"
"thickness", None))
        self.gb_Density.setTitle(QCoreApplication.translate("BatchAnalysisWindow", u"Contours", None))
#if QT_CONFIG(tooltip)
        self.lb_ContoursMinSize.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Choose the minimum size in pixels of the contoured objects.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_ContoursMinSize.setText(QCoreApplication.translate("BatchAnalysisWindow", u"Min size", None))
#if QT_CONFIG(tooltip)
        self.le_BackgroundThreshold.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the minimum value of the background. Pixels with a value strictly over the threshold will be considered part of the object depending on the algorithm.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lb_BackgroundThreshold.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the minimum value of the background. Pixels with a value strictly over the threshold will be considered part of the object depending on the algorithm.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_BackgroundThreshold.setText(QCoreApplication.translate("BatchAnalysisWindow", u"Background threshold", None))
#if QT_CONFIG(tooltip)
        self.le_ContoursMinSize.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Choose the minimum size in pixels of the contoured objects.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_StartAnalysis.setText(QCoreApplication.translate("BatchAnalysisWindow", u"Start analysis", None))
        self.pb_Cancel.setText(QCoreApplication.translate("BatchAnalysisWindow", u"Cancel", None))
        self.gb_Contours.setTitle(QCoreApplication.translate("BatchAnalysisWindow", u"Density", None))
#if QT_CONFIG(tooltip)
        self.le_DensityMapKernelSize.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the kernel size in pixels. Choose an odd number.", None))
#endif // QT_CONFIG(tooltip)
        self.le_DensityMapKernelSize.setText("")
#if QT_CONFIG(tooltip)
        self.lb_Layers.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the number of concentric regions (layers) around the centroid of the contoured object.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_Layers.setText(QCoreApplication.translate("BatchAnalysisWindow", u"Target layers", None))
#if QT_CONFIG(tooltip)
        self.le_DensityTargetLayers.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the number of concentric regions (layers) around the centroid of the contoured object.", None))
#endif // QT_CONFIG(tooltip)
        self.le_DensityTargetLayers.setText("")
#if QT_CONFIG(tooltip)
        self.lb_Kernel.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the kernel size in pixels. Choose an odd number.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_Kernel.setText(QCoreApplication.translate("BatchAnalysisWindow", u"Map kernel size", None))
        self.gb_Labeling.setTitle(QCoreApplication.translate("BatchAnalysisWindow", u"Labeling", None))
#if QT_CONFIG(tooltip)
        self.lb_SieveSize.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the size of the sieve in pixels. Objects with a size strictly above the sieve size will be kept.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_SieveSize.setText(QCoreApplication.translate("BatchAnalysisWindow", u"Sieve size", None))
#if QT_CONFIG(tooltip)
        self.le_SieveSize.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the size of the sieve in pixels. Objects with a size strictly above the sieve size will be kept.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.combob_LabelingOption.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Choose the labeling option.", None))
#endif // QT_CONFIG(tooltip)
        self.gb_Illumination.setTitle(QCoreApplication.translate("BatchAnalysisWindow", u"Illumination", None))
#if QT_CONFIG(tooltip)
        self.le_RollingBallRadius.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the rolling ball radius in pixels", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lb_RollingBallRadius.setToolTip(QCoreApplication.translate("BatchAnalysisWindow", u"Input the rolling ball radius in pixels", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.lb_RollingBallRadius.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.lb_RollingBallRadius.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.lb_RollingBallRadius.setText(QCoreApplication.translate("BatchAnalysisWindow", u"Rolling ball radius", None))
        self.pb_DefaultOptions.setText(QCoreApplication.translate("BatchAnalysisWindow", u"Default options", None))
    # retranslateUi

