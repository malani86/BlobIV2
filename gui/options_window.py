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

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import sys
from gui.options_window_ui import Ui_OptionsWindow
from logic.algorithms import return_colors_dictionnary, return_colormaps, return_blobs_algorithms, return_contouring_algorithms, return_labeling_algorithms

class OptionsWindow(QtWidgets.QWidget, Ui_OptionsWindow):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)

        self.main_window = main_window
        self.pb_Quit.clicked.connect(self.close)
        colors_dictionnary = return_colors_dictionnary()
        colors_list = list(colors_dictionnary.keys())
        for i in range(len(colors_list)):
            if colors_list[i] not in ["white"]:
                self.combob_SegmentationColors.addItem(colors_list[i])
                self.combob_SegmentationColors.setItemData(i,QColor(colors_list[i]),Qt.BackgroundRole)
            self.combob_ScaleColor.addItem(colors_list[i])
            self.combob_ScaleColor.setItemData(i,QColor(colors_list[i]),Qt.BackgroundRole)
        self.combob_Colormap.addItems(return_colormaps())
        self.combob_Threshold.addItems(["One threshold","Two thresholds"])
        self.combob_SegmentationBlobs.addItems(return_blobs_algorithms())
        self.combob_Labeling.addItems(return_labeling_algorithms())
        self.combob_Contours.addItems(return_contouring_algorithms())
        
if __name__ == "__main":
    app = QtWidgets.QApplication(sys.argv)
    batch_analysis_window = OptionsWindow()
    batch_analysis_window.show()
    sys.exit(app.exec())