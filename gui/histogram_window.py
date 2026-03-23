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

import sys
from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from gui.histogram_window_ui import Ui_wi_HistogramWindow

class HistogramWindow(QtWidgets.QWidget, Ui_wi_HistogramWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        
        self.pb_Quit.clicked.connect(self.close)

if __name__ == "__main":
    app = QtWidgets.QApplication(sys.argv)
    histogram_window = HistogramWindow()
    histogram_window.show()
    sys.exit(app.exec())