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
## Form generated from reading UI file 'options_window.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)
import resources.resources_rc

class Ui_OptionsWindow(object):
    def setupUi(self, OptionsWindow):
        if not OptionsWindow.objectName():
            OptionsWindow.setObjectName(u"OptionsWindow")
        OptionsWindow.resize(514, 570)
        icon = QIcon()
        icon.addFile(u":/Icons/blob-161097_640.png", QSize(), QIcon.Normal, QIcon.Off)
        OptionsWindow.setWindowIcon(icon)
        self.gridLayout = QGridLayout(OptionsWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.combob_ScalePosition = QComboBox(OptionsWindow)
        self.combob_ScalePosition.addItem("")
        self.combob_ScalePosition.addItem("")
        self.combob_ScalePosition.addItem("")
        self.combob_ScalePosition.addItem("")
        self.combob_ScalePosition.setObjectName(u"combob_ScalePosition")

        self.gridLayout.addWidget(self.combob_ScalePosition, 5, 4, 1, 4)

        self.le_StackInfoIntersliceSpace = QLineEdit(OptionsWindow)
        self.le_StackInfoIntersliceSpace.setObjectName(u"le_StackInfoIntersliceSpace")
        self.le_StackInfoIntersliceSpace.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_StackInfoIntersliceSpace, 23, 4, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_13, 6, 8, 1, 2)

        self.combob_SegmentationColors = QComboBox(OptionsWindow)
        self.combob_SegmentationColors.setObjectName(u"combob_SegmentationColors")

        self.gridLayout.addWidget(self.combob_SegmentationColors, 1, 3, 1, 4)

        self.le_ScaleNumberPixels = QLineEdit(OptionsWindow)
        self.le_ScaleNumberPixels.setObjectName(u"le_ScaleNumberPixels")
        self.le_ScaleNumberPixels.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_ScaleNumberPixels, 3, 4, 1, 2)

        self.le_StackInfoPixelSize = QLineEdit(OptionsWindow)
        self.le_StackInfoPixelSize.setObjectName(u"le_StackInfoPixelSize")
        self.le_StackInfoPixelSize.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_StackInfoPixelSize, 24, 4, 1, 1)

        self.le_SegmentationBlobsMinRadius = QLineEdit(OptionsWindow)
        self.le_SegmentationBlobsMinRadius.setObjectName(u"le_SegmentationBlobsMinRadius")
        self.le_SegmentationBlobsMinRadius.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_SegmentationBlobsMinRadius, 11, 4, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(100, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 4, 6, 1, 4)

        self.lb_IlluminationRollingBallRadius = QLabel(OptionsWindow)
        self.lb_IlluminationRollingBallRadius.setObjectName(u"lb_IlluminationRollingBallRadius")

        self.gridLayout.addWidget(self.lb_IlluminationRollingBallRadius, 9, 2, 1, 2)

        self.verticalSpacer = QSpacerItem(105, 86, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 0, 3, 1)

        self.lb_Profile = QLabel(OptionsWindow)
        self.lb_Profile.setObjectName(u"lb_Profile")

        self.gridLayout.addWidget(self.lb_Profile, 0, 0, 1, 2)

        self.le_DensityKernelSize = QLineEdit(OptionsWindow)
        self.le_DensityKernelSize.setObjectName(u"le_DensityKernelSize")
        self.le_DensityKernelSize.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_DensityKernelSize, 21, 4, 1, 1)

        self.lb_DensityLayers = QLabel(OptionsWindow)
        self.lb_DensityLayers.setObjectName(u"lb_DensityLayers")
        self.lb_DensityLayers.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lb_DensityLayers, 21, 5, 1, 3)

        self.combob_Colormap = QComboBox(OptionsWindow)
        self.combob_Colormap.setObjectName(u"combob_Colormap")

        self.gridLayout.addWidget(self.combob_Colormap, 2, 3, 1, 4)

        self.lb_StackInfoSliceThickness = QLabel(OptionsWindow)
        self.lb_StackInfoSliceThickness.setObjectName(u"lb_StackInfoSliceThickness")

        self.gridLayout.addWidget(self.lb_StackInfoSliceThickness, 22, 2, 1, 2)

        self.le_DensityLayers = QLineEdit(OptionsWindow)
        self.le_DensityLayers.setObjectName(u"le_DensityLayers")
        self.le_DensityLayers.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_DensityLayers, 21, 9, 1, 1)

        self.lb_Colormap = QLabel(OptionsWindow)
        self.lb_Colormap.setObjectName(u"lb_Colormap")
        font = QFont()
        font.setBold(True)
        self.lb_Colormap.setFont(font)

        self.gridLayout.addWidget(self.lb_Colormap, 2, 0, 1, 3)

        self.lb_LabelingSieveSize = QLabel(OptionsWindow)
        self.lb_LabelingSieveSize.setObjectName(u"lb_LabelingSieveSize")
        self.lb_LabelingSieveSize.setLayoutDirection(Qt.LeftToRight)
        self.lb_LabelingSieveSize.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lb_LabelingSieveSize, 16, 5, 1, 2)

        self.combob_SegmentationBlobs = QComboBox(OptionsWindow)
        self.combob_SegmentationBlobs.setObjectName(u"combob_SegmentationBlobs")

        self.gridLayout.addWidget(self.combob_SegmentationBlobs, 11, 2, 1, 2)

        self.horizontalSpacer_4 = QSpacerItem(102, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 3, 6, 1, 4)

        self.lb_Segmentation = QLabel(OptionsWindow)
        self.lb_Segmentation.setObjectName(u"lb_Segmentation")
        self.lb_Segmentation.setFont(font)

        self.gridLayout.addWidget(self.lb_Segmentation, 10, 0, 1, 2)

        self.lb_Scale = QLabel(OptionsWindow)
        self.lb_Scale.setObjectName(u"lb_Scale")
        self.lb_Scale.setFont(font)

        self.gridLayout.addWidget(self.lb_Scale, 3, 0, 1, 2)

        self.combob_ScaleColor = QComboBox(OptionsWindow)
        self.combob_ScaleColor.setObjectName(u"combob_ScaleColor")

        self.gridLayout.addWidget(self.combob_ScaleColor, 6, 4, 1, 4)

        self.le_IlluminationRollingBallRadius = QLineEdit(OptionsWindow)
        self.le_IlluminationRollingBallRadius.setObjectName(u"le_IlluminationRollingBallRadius")
        self.le_IlluminationRollingBallRadius.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_IlluminationRollingBallRadius, 9, 4, 1, 1)

        self.le_SegmentationThresholdTwo = QLineEdit(OptionsWindow)
        self.le_SegmentationThresholdTwo.setObjectName(u"le_SegmentationThresholdTwo")
        self.le_SegmentationThresholdTwo.setEnabled(False)
        self.le_SegmentationThresholdTwo.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_SegmentationThresholdTwo, 10, 6, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(153, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_8, 23, 6, 1, 4)

        self.horizontalSpacer_9 = QSpacerItem(153, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_9, 24, 6, 1, 4)

        self.lb_ScaleUnit = QLabel(OptionsWindow)
        self.lb_ScaleUnit.setObjectName(u"lb_ScaleUnit")

        self.gridLayout.addWidget(self.lb_ScaleUnit, 4, 2, 1, 1)

        self.pb_CreateNewProfile = QPushButton(OptionsWindow)
        self.pb_CreateNewProfile.setObjectName(u"pb_CreateNewProfile")

        self.gridLayout.addWidget(self.pb_CreateNewProfile, 26, 1, 1, 3)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_10, 5, 8, 1, 2)

        self.pb_RemoveProfile = QPushButton(OptionsWindow)
        self.pb_RemoveProfile.setObjectName(u"pb_RemoveProfile")

        self.gridLayout.addWidget(self.pb_RemoveProfile, 26, 4, 1, 3)

        self.lb_ContoursBackground = QLabel(OptionsWindow)
        self.lb_ContoursBackground.setObjectName(u"lb_ContoursBackground")
        self.lb_ContoursBackground.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lb_ContoursBackground, 19, 5, 1, 3)

        self.lb_Density = QLabel(OptionsWindow)
        self.lb_Density.setObjectName(u"lb_Density")
        self.lb_Density.setFont(font)

        self.gridLayout.addWidget(self.lb_Density, 21, 0, 1, 1)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_14, 11, 0, 1, 2)

        self.lb_StackAcquistionParameters = QLabel(OptionsWindow)
        self.lb_StackAcquistionParameters.setObjectName(u"lb_StackAcquistionParameters")
        self.lb_StackAcquistionParameters.setFont(font)

        self.gridLayout.addWidget(self.lb_StackAcquistionParameters, 22, 0, 1, 1)

        self.lb_DensityKernelSize = QLabel(OptionsWindow)
        self.lb_DensityKernelSize.setObjectName(u"lb_DensityKernelSize")

        self.gridLayout.addWidget(self.lb_DensityKernelSize, 21, 2, 1, 1)

        self.lb_StackInfoIntersliceSpace = QLabel(OptionsWindow)
        self.lb_StackInfoIntersliceSpace.setObjectName(u"lb_StackInfoIntersliceSpace")

        self.gridLayout.addWidget(self.lb_StackInfoIntersliceSpace, 23, 2, 1, 1)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_12, 2, 8, 1, 2)

        self.lb_StackInfoPixelSize = QLabel(OptionsWindow)
        self.lb_StackInfoPixelSize.setObjectName(u"lb_StackInfoPixelSize")

        self.gridLayout.addWidget(self.lb_StackInfoPixelSize, 24, 2, 1, 1)

        self.combob_Contours = QComboBox(OptionsWindow)
        self.combob_Contours.setObjectName(u"combob_Contours")

        self.gridLayout.addWidget(self.combob_Contours, 19, 2, 1, 3)

        self.le_ContoursBackground = QLineEdit(OptionsWindow)
        self.le_ContoursBackground.setObjectName(u"le_ContoursBackground")
        self.le_ContoursBackground.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_ContoursBackground, 19, 9, 1, 1)

        self.lb_ScaleNumberPixels = QLabel(OptionsWindow)
        self.lb_ScaleNumberPixels.setObjectName(u"lb_ScaleNumberPixels")

        self.gridLayout.addWidget(self.lb_ScaleNumberPixels, 3, 2, 1, 2)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_11, 1, 8, 1, 2)

        self.horizontalSpacer = QSpacerItem(65, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 10, 8, 1, 2)

        self.combob_Profiles = QComboBox(OptionsWindow)
        self.combob_Profiles.setObjectName(u"combob_Profiles")

        self.gridLayout.addWidget(self.combob_Profiles, 0, 2, 1, 8)

        self.lb_ScaleColor = QLabel(OptionsWindow)
        self.lb_ScaleColor.setObjectName(u"lb_ScaleColor")

        self.gridLayout.addWidget(self.lb_ScaleColor, 6, 2, 1, 1)

        self.le_SegmentationBlobsMaxRadius = QLineEdit(OptionsWindow)
        self.le_SegmentationBlobsMaxRadius.setObjectName(u"le_SegmentationBlobsMaxRadius")
        self.le_SegmentationBlobsMaxRadius.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_SegmentationBlobsMaxRadius, 11, 6, 1, 1)

        self.le_ScaleUnit = QLineEdit(OptionsWindow)
        self.le_ScaleUnit.setObjectName(u"le_ScaleUnit")
        self.le_ScaleUnit.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_ScaleUnit, 4, 4, 1, 2)

        self.pb_UpdateProfile = QPushButton(OptionsWindow)
        self.pb_UpdateProfile.setObjectName(u"pb_UpdateProfile")

        self.gridLayout.addWidget(self.pb_UpdateProfile, 26, 0, 1, 1)

        self.lb_SegmentationColors = QLabel(OptionsWindow)
        self.lb_SegmentationColors.setObjectName(u"lb_SegmentationColors")
        self.lb_SegmentationColors.setMinimumSize(QSize(160, 0))
        self.lb_SegmentationColors.setFont(font)

        self.gridLayout.addWidget(self.lb_SegmentationColors, 1, 0, 1, 3)

        self.lb_Illumination = QLabel(OptionsWindow)
        self.lb_Illumination.setObjectName(u"lb_Illumination")
        self.lb_Illumination.setFont(font)

        self.gridLayout.addWidget(self.lb_Illumination, 9, 0, 1, 2)

        self.lb_Labeling = QLabel(OptionsWindow)
        self.lb_Labeling.setObjectName(u"lb_Labeling")
        self.lb_Labeling.setFont(font)

        self.gridLayout.addWidget(self.lb_Labeling, 16, 0, 1, 2)

        self.horizontalSpacer_7 = QSpacerItem(153, 22, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_7, 22, 6, 1, 4)

        self.horizontalSpacer_2 = QSpacerItem(65, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 11, 8, 1, 2)

        self.lb_Contours = QLabel(OptionsWindow)
        self.lb_Contours.setObjectName(u"lb_Contours")
        self.lb_Contours.setFont(font)

        self.gridLayout.addWidget(self.lb_Contours, 19, 0, 1, 2)

        self.horizontalSpacer_3 = QSpacerItem(146, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 9, 6, 1, 4)

        self.verticalSpacer_3 = QSpacerItem(105, 54, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_3, 23, 0, 2, 1)

        self.le_SegmentationThresholdOne = QLineEdit(OptionsWindow)
        self.le_SegmentationThresholdOne.setObjectName(u"le_SegmentationThresholdOne")
        self.le_SegmentationThresholdOne.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_SegmentationThresholdOne, 10, 4, 1, 1)

        self.le_StackInfoSliceThickness = QLineEdit(OptionsWindow)
        self.le_StackInfoSliceThickness.setObjectName(u"le_StackInfoSliceThickness")
        self.le_StackInfoSliceThickness.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_StackInfoSliceThickness, 22, 4, 1, 1)

        self.combob_Threshold = QComboBox(OptionsWindow)
        self.combob_Threshold.setObjectName(u"combob_Threshold")

        self.gridLayout.addWidget(self.combob_Threshold, 10, 2, 1, 2)

        self.lb_ScalePosition = QLabel(OptionsWindow)
        self.lb_ScalePosition.setObjectName(u"lb_ScalePosition")

        self.gridLayout.addWidget(self.lb_ScalePosition, 5, 2, 1, 1)

        self.combob_Labeling = QComboBox(OptionsWindow)
        self.combob_Labeling.setObjectName(u"combob_Labeling")

        self.gridLayout.addWidget(self.combob_Labeling, 16, 2, 1, 3)

        self.le_LabelingSieveSize = QLineEdit(OptionsWindow)
        self.le_LabelingSieveSize.setObjectName(u"le_LabelingSieveSize")
        self.le_LabelingSieveSize.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.le_LabelingSieveSize, 16, 9, 1, 1)

        self.pb_Quit = QPushButton(OptionsWindow)
        self.pb_Quit.setObjectName(u"pb_Quit")

        self.gridLayout.addWidget(self.pb_Quit, 26, 7, 1, 3)

        self.le_ContoursMinSize = QLineEdit(OptionsWindow)
        self.le_ContoursMinSize.setObjectName(u"le_ContoursMinSize")

        self.gridLayout.addWidget(self.le_ContoursMinSize, 20, 9, 1, 1)

        self.lb_ContoursMinSize = QLabel(OptionsWindow)
        self.lb_ContoursMinSize.setObjectName(u"lb_ContoursMinSize")

        self.gridLayout.addWidget(self.lb_ContoursMinSize, 20, 6, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 20, 0, 1, 5)

        QWidget.setTabOrder(self.combob_Profiles, self.combob_SegmentationColors)
        QWidget.setTabOrder(self.combob_SegmentationColors, self.combob_Colormap)
        QWidget.setTabOrder(self.combob_Colormap, self.le_ScaleNumberPixels)
        QWidget.setTabOrder(self.le_ScaleNumberPixels, self.le_ScaleUnit)
        QWidget.setTabOrder(self.le_ScaleUnit, self.combob_ScalePosition)
        QWidget.setTabOrder(self.combob_ScalePosition, self.combob_ScaleColor)
        QWidget.setTabOrder(self.combob_ScaleColor, self.le_IlluminationRollingBallRadius)
        QWidget.setTabOrder(self.le_IlluminationRollingBallRadius, self.combob_Threshold)
        QWidget.setTabOrder(self.combob_Threshold, self.le_SegmentationThresholdOne)
        QWidget.setTabOrder(self.le_SegmentationThresholdOne, self.le_SegmentationThresholdTwo)
        QWidget.setTabOrder(self.le_SegmentationThresholdTwo, self.combob_SegmentationBlobs)
        QWidget.setTabOrder(self.combob_SegmentationBlobs, self.le_SegmentationBlobsMinRadius)
        QWidget.setTabOrder(self.le_SegmentationBlobsMinRadius, self.le_SegmentationBlobsMaxRadius)
        QWidget.setTabOrder(self.le_SegmentationBlobsMaxRadius, self.combob_Labeling)
        QWidget.setTabOrder(self.combob_Labeling, self.le_LabelingSieveSize)
        QWidget.setTabOrder(self.le_LabelingSieveSize, self.combob_Contours)
        QWidget.setTabOrder(self.combob_Contours, self.le_ContoursBackground)
        QWidget.setTabOrder(self.le_ContoursBackground, self.le_ContoursMinSize)
        QWidget.setTabOrder(self.le_ContoursMinSize, self.le_DensityKernelSize)
        QWidget.setTabOrder(self.le_DensityKernelSize, self.le_DensityLayers)
        QWidget.setTabOrder(self.le_DensityLayers, self.le_StackInfoSliceThickness)
        QWidget.setTabOrder(self.le_StackInfoSliceThickness, self.le_StackInfoIntersliceSpace)
        QWidget.setTabOrder(self.le_StackInfoIntersliceSpace, self.le_StackInfoPixelSize)
        QWidget.setTabOrder(self.le_StackInfoPixelSize, self.pb_UpdateProfile)
        QWidget.setTabOrder(self.pb_UpdateProfile, self.pb_CreateNewProfile)
        QWidget.setTabOrder(self.pb_CreateNewProfile, self.pb_RemoveProfile)
        QWidget.setTabOrder(self.pb_RemoveProfile, self.pb_Quit)

        self.retranslateUi(OptionsWindow)

        QMetaObject.connectSlotsByName(OptionsWindow)
    # setupUi

    def retranslateUi(self, OptionsWindow):
        OptionsWindow.setWindowTitle(QCoreApplication.translate("OptionsWindow", u"Options", None))
        self.combob_ScalePosition.setItemText(0, QCoreApplication.translate("OptionsWindow", u"South-East", None))
        self.combob_ScalePosition.setItemText(1, QCoreApplication.translate("OptionsWindow", u"South-West", None))
        self.combob_ScalePosition.setItemText(2, QCoreApplication.translate("OptionsWindow", u"North-West", None))
        self.combob_ScalePosition.setItemText(3, QCoreApplication.translate("OptionsWindow", u"North-East", None))

#if QT_CONFIG(tooltip)
        self.combob_ScalePosition.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the position of the scale in the image.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.le_StackInfoIntersliceSpace.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the distance between each slice. Choose the same unit for the 3 parameters in the results section.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.combob_SegmentationColors.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the color to identify the segmented objects (blobs).", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.le_ScaleNumberPixels.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the length of the scale in pixels.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.le_StackInfoPixelSize.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the size of a pixel. Choose the same unit for the 3 parameters in the results section.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.le_SegmentationBlobsMinRadius.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the minimum value of the blobs radius in pixels. Smaller blobs won't be detected.", None))
#endif // QT_CONFIG(tooltip)
        self.le_SegmentationBlobsMinRadius.setText(QCoreApplication.translate("OptionsWindow", u"min", None))
#if QT_CONFIG(tooltip)
        self.lb_IlluminationRollingBallRadius.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the rolling ball radius in pixels", None))
#endif // QT_CONFIG(tooltip)
        self.lb_IlluminationRollingBallRadius.setText(QCoreApplication.translate("OptionsWindow", u"Rolling ball radius", None))
        self.lb_Profile.setText(QCoreApplication.translate("OptionsWindow", u"Default profile", None))
#if QT_CONFIG(tooltip)
        self.le_DensityKernelSize.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the kernel size in pixels. Choose an odd number.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lb_DensityLayers.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the number of concentric regions (layers) around the centroid of the contoured object.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_DensityLayers.setText(QCoreApplication.translate("OptionsWindow", u"Layers", None))
#if QT_CONFIG(tooltip)
        self.combob_Colormap.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the colormap to display the density results.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lb_StackInfoSliceThickness.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the thickness of each slice. Choose the same unit for the 3 parameters in the results section.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_StackInfoSliceThickness.setText(QCoreApplication.translate("OptionsWindow", u"Slice thickness", None))
#if QT_CONFIG(tooltip)
        self.le_DensityLayers.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the number of concentric regions (layers) around the centroid of the contoured object.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lb_Colormap.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the colormap to display the density results.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_Colormap.setText(QCoreApplication.translate("OptionsWindow", u"Heatmap colormap", None))
#if QT_CONFIG(tooltip)
        self.lb_LabelingSieveSize.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the size of the sieve in pixels. Objects with a size strictly above the sieve size will be kept.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_LabelingSieveSize.setText(QCoreApplication.translate("OptionsWindow", u"Sieve size", None))
#if QT_CONFIG(tooltip)
        self.combob_SegmentationBlobs.setToolTip(QCoreApplication.translate("OptionsWindow", u"Laplacian of Gaussian (LoG), Difference of Gaussian (DoG), Determinant of Hessian (DoH)", None))
#endif // QT_CONFIG(tooltip)
        self.lb_Segmentation.setText(QCoreApplication.translate("OptionsWindow", u"Segmentation", None))
        self.lb_Scale.setText(QCoreApplication.translate("OptionsWindow", u"Scale", None))
#if QT_CONFIG(tooltip)
        self.combob_ScaleColor.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the color of the scale.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.le_IlluminationRollingBallRadius.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the rolling ball radius in pixels", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.le_SegmentationThresholdTwo.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the value of the threshold from 0 to 255 or from 0 to 1.", None))
#endif // QT_CONFIG(tooltip)
        self.le_SegmentationThresholdTwo.setText(QCoreApplication.translate("OptionsWindow", u"II", None))
#if QT_CONFIG(tooltip)
        self.lb_ScaleUnit.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the unit of the scale.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_ScaleUnit.setText(QCoreApplication.translate("OptionsWindow", u"Unit", None))
        self.pb_CreateNewProfile.setText(QCoreApplication.translate("OptionsWindow", u"Create new profile", None))
        self.pb_RemoveProfile.setText(QCoreApplication.translate("OptionsWindow", u"Remove profile", None))
        self.lb_ContoursBackground.setText(QCoreApplication.translate("OptionsWindow", u"Background", None))
        self.lb_Density.setText(QCoreApplication.translate("OptionsWindow", u"Density", None))
        self.lb_StackAcquistionParameters.setText(QCoreApplication.translate("OptionsWindow", u"Stack info", None))
#if QT_CONFIG(tooltip)
        self.lb_DensityKernelSize.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the kernel size in pixels. Choose an odd number.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_DensityKernelSize.setText(QCoreApplication.translate("OptionsWindow", u"Kernel Size", None))
#if QT_CONFIG(tooltip)
        self.lb_StackInfoIntersliceSpace.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the distance between each slice. Choose the same unit for the 3 parameters in the results section.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_StackInfoIntersliceSpace.setText(QCoreApplication.translate("OptionsWindow", u"Interslice space", None))
#if QT_CONFIG(tooltip)
        self.lb_StackInfoPixelSize.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the size of a pixel. Choose the same unit for the 3 parameters in the results section.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_StackInfoPixelSize.setText(QCoreApplication.translate("OptionsWindow", u"Pixel size", None))
#if QT_CONFIG(tooltip)
        self.combob_Contours.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the algorithm to contour the object containing the blobs.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.le_ContoursBackground.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the minimum value of the background. Pixels with a value strictly over the threshold will be considered part of the object depending on the algorithm.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lb_ScaleNumberPixels.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the length of the scale in pixels.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_ScaleNumberPixels.setText(QCoreApplication.translate("OptionsWindow", u"Number of pixels", None))
#if QT_CONFIG(tooltip)
        self.lb_ScaleColor.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the color of the scale.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_ScaleColor.setText(QCoreApplication.translate("OptionsWindow", u"Color", None))
#if QT_CONFIG(tooltip)
        self.le_SegmentationBlobsMaxRadius.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the maximum value of the blobs radius in pixels. Bigger blobs won't be detected.", None))
#endif // QT_CONFIG(tooltip)
        self.le_SegmentationBlobsMaxRadius.setText(QCoreApplication.translate("OptionsWindow", u"max", None))
#if QT_CONFIG(tooltip)
        self.le_ScaleUnit.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the unit of the scale.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_UpdateProfile.setText(QCoreApplication.translate("OptionsWindow", u"Update profile", None))
#if QT_CONFIG(tooltip)
        self.lb_SegmentationColors.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the color to identify the segmented objects (blobs).", None))
#endif // QT_CONFIG(tooltip)
        self.lb_SegmentationColors.setText(QCoreApplication.translate("OptionsWindow", u"Segmentation color", None))
        self.lb_Illumination.setText(QCoreApplication.translate("OptionsWindow", u"Illumination", None))
        self.lb_Labeling.setText(QCoreApplication.translate("OptionsWindow", u"Labeling", None))
        self.lb_Contours.setText(QCoreApplication.translate("OptionsWindow", u"Shape contours", None))
#if QT_CONFIG(tooltip)
        self.le_SegmentationThresholdOne.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the value of the threshold from 0 to 255 or from 0 to 1.", None))
#endif // QT_CONFIG(tooltip)
        self.le_SegmentationThresholdOne.setText(QCoreApplication.translate("OptionsWindow", u"I", None))
#if QT_CONFIG(tooltip)
        self.le_StackInfoSliceThickness.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the thickness of each slice. Choose the same unit for the 3 parameters in the results section.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.combob_Threshold.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose thresholding option.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lb_ScalePosition.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the position of the scale in the image.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_ScalePosition.setText(QCoreApplication.translate("OptionsWindow", u"Position", None))
#if QT_CONFIG(tooltip)
        self.combob_Labeling.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the labeling option.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.le_LabelingSieveSize.setToolTip(QCoreApplication.translate("OptionsWindow", u"Input the size of the sieve in pixels. Objects with a size strictly above the sieve size will be kept.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_Quit.setText(QCoreApplication.translate("OptionsWindow", u"Quit", None))
#if QT_CONFIG(tooltip)
        self.le_ContoursMinSize.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the minimum size in pixels of the contoured objects.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lb_ContoursMinSize.setToolTip(QCoreApplication.translate("OptionsWindow", u"Choose the minimum size in pixels of the contoured objects.", None))
#endif // QT_CONFIG(tooltip)
        self.lb_ContoursMinSize.setText(QCoreApplication.translate("OptionsWindow", u"Min size", None))
    # retranslateUi

