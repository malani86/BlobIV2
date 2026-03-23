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

from PySide6.QtWidgets import QFileDialog, QMessageBox, QDialog, QVBoxLayout, QGroupBox, QFormLayout, QDoubleSpinBox, QPushButton, QHBoxLayout, QPlainTextEdit
from PySide6.QtGui import QIcon, QFontMetrics
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure, cbook
import matplotlib as plt
import os

class SubplotToolQt(QDialog):
    def __init__(self, targetfig, parent):
        super().__init__()
        self.setWindowIcon(QIcon(
            str(cbook._get_data_path("images/matplotlib.png"))))
        self.setObjectName("SubplotTool")
        self._spinboxes = {}
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        for group, spinboxes, buttons in [
                ("Borders",
                 ["top", "bottom", "left", "right"],
                 [("Export values", self._export_values)]),
                ("Spacings",
                 ["hspace", "wspace"],
                 [("Tight layout", self._tight_layout),
                  ("Reset", self._reset),
                  ("Close", self.close)])]:
            layout = QVBoxLayout()
            main_layout.addLayout(layout)
            box = QGroupBox(group)
            layout.addWidget(box)
            inner = QFormLayout(box)
            for name in spinboxes:
                self._spinboxes[name] = spinbox = QDoubleSpinBox()
                spinbox.setRange(0, 1)
                spinbox.setDecimals(3)
                spinbox.setSingleStep(0.005)
                spinbox.setKeyboardTracking(False)
                spinbox.valueChanged.connect(self._on_value_changed)
                inner.addRow(name, spinbox)
            layout.addStretch(1)
            for name, method in buttons:
                button = QPushButton(name)
                # Don't trigger on <enter>, which is used to input values.
                button.setAutoDefault(False)
                button.clicked.connect(method)
                layout.addWidget(button)
                if name == "Close":
                    button.setFocus()
        self._figure = targetfig
        self._defaults = {}
        self._export_values_dialog = None
        self.update_from_current_subplotpars()

    def _export_values(self):
        # Explicitly round to 3 decimals (which is also the spinbox precision)
        # to avoid numbers of the form 0.100...001.
        self._export_values_dialog = QDialog()
        layout = QVBoxLayout()
        self._export_values_dialog.setLayout(layout)
        text = QPlainTextEdit()
        text.setReadOnly(True)
        layout.addWidget(text)
        text.setPlainText(
            ",\n".join(f"{attr}={spinbox.value():.3}"
                       for attr, spinbox in self._spinboxes.items()))
        # Adjust the height of the text widget to fit the whole text, plus
        # some padding.
        size = text.maximumSize()
        size.setHeight(
            QFontMetrics(text.document().defaultFont())
            .size(0, text.toPlainText()).height() + 20)
        text.setMaximumSize(size)
        self._export_values_dialog.show()

    def _tight_layout(self):
        self._figure.tight_layout()
        for attr, spinbox in self._spinboxes.items():
            spinbox.blockSignals(True)
            spinbox.setValue(getattr(self._figure.subplotpars, attr))
            spinbox.blockSignals(False)
        self._figure.canvas.draw_idle()
    
    def update_from_current_subplotpars(self):
        self._defaults = {spinbox: getattr(self._figure.subplotpars, name)
                          for name, spinbox in self._spinboxes.items()}
        self._reset()  # Set spinbox current values without triggering signals.

    def _reset(self):
        for spinbox, value in self._defaults.items():
            spinbox.setRange(0, 1)
            spinbox.blockSignals(True)
            spinbox.setValue(value)
            spinbox.blockSignals(False)
        self._on_value_changed()

    def _on_value_changed(self):
        spinboxes = self._spinboxes
        # Set all mins and maxes, so that this can also be used in _reset().
        for lower, higher in [("bottom", "top"), ("left", "right")]:
            spinboxes[higher].setMinimum(spinboxes[lower].value() + .001)
            spinboxes[lower].setMaximum(spinboxes[higher].value() - .001)
        self._figure.subplots_adjust(
            **{attr: spinbox.value() for attr, spinbox in spinboxes.items()})
        self._figure.canvas.draw_idle()

class CustomToolbar(NavigationToolbar):
    def __init__(self, canvas, parent, coordinates=True):
        super().__init__(canvas, parent, coordinates)
        self.canvas = canvas
        self.canvas.custom_home_function = self.custom_home_function
        self.parent = parent
        
    def home(self, *args, **kwargs):
        self.custom_home_function()

    def custom_home_function(self):
        self.canvas.axes.set_xlim(self.canvas.original_xlim[0]-0.5,self.canvas.original_xlim[1]-0.5)
        self.canvas.axes.set_ylim(self.canvas.original_ylim[1]-0.5,self.canvas.original_ylim[0]-0.5)
        self.canvas.draw_idle()

    def save_figure(self, *args):
        filetypes = self.canvas.get_supported_filetypes_grouped()
        sorted_filetypes = sorted(filetypes.items())
        default_filetype = self.canvas.get_default_filetype()

        startpath = os.path.expanduser(plt.rcParams['savefig.directory'])
        start = os.path.join(startpath, self.canvas.get_default_filename())
        filters = []
        selectedFilter = None
        for name, exts in sorted_filetypes:
            exts_list = " ".join(['*.%s' % ext for ext in exts])
            filter = f'{name} ({exts_list})'
            if default_filetype in exts:
                selectedFilter = filter
            filters.append(filter)
        filters = ';;'.join(filters)

        fname, filter = QFileDialog.getSaveFileName(
            self.parent, "Choose a filename to save to", start,
            filters, selectedFilter)
        if fname:
            if startpath != "":
                plt.rcParams['savefig.directory'] = os.path.dirname(fname)
            try:
                self.canvas.figure.savefig(fname)
            except Exception as e:
                QMessageBox.critical(
                    self.parent, "Error saving file", str(e),
                    QMessageBox.StandardButton.Ok,
                    QMessageBox.StandardButton.NoButton)
        
    def configure_subplots(self):
        if self._subplot_dialog is None:
            self._subplot_dialog = SubplotToolQt(
                self.canvas.figure, self.canvas.parent)
            self.canvas.mpl_connect(
                "close_event", lambda e: self._subplot_dialog.reject())
        self._subplot_dialog.update_from_current_subplotpars()
        self._subplot_dialog.show()
        return self._subplot_dialog
    
    
    
