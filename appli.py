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
import os
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QEvent
from joblib import load

from gui.app_ui import Ui_MainWindow
from gui.histogram_window import HistogramWindow
from gui.save_analysis_window import SaveAnalysisWindow
from gui.batch_analysis_window import BatchAnalysisWindow
from gui.options_window import OptionsWindow

from logic.applicationlogic import *

from resources import resources_rc


from model.app_options import AppOptions
from model.app_model import AppModel

from datetime import datetime, timedelta


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)      
        self._setup_segmentation_dl_controls()
        # Attributes
        self.focus = None
        self.batchAnalysis = {}
        self.appMod = AppModel()
        profiles_list = []
        if os.path.exists("./options.joblib"):
            self.appOptions = load("./options.joblib")
            profiles_list = list(self.appOptions.profiles.keys())
        else:
            self.appOptions = AppOptions()
        self.histogram_window = HistogramWindow()
        self.save_analysis_window = SaveAnalysisWindow(self)
        self.batch_analysis_window = BatchAnalysisWindow(self)
        self.options_window = OptionsWindow(self)
        initialise_options_window(self)
        # Display at setup
        self.histogram_window.setVisible(False)
        self.save_analysis_window.setVisible(False)
        self.batch_analysis_window.setVisible(False)
        self.options_window.setVisible(False)
        self.wi_OriginalText.hide()
        self.wi_Image1Text.hide()
        self.wi_Image2Text.hide()
        self.tabWidget.hide()
        self.gb_ResultsChoice.hide()
        self.frame_4.hide()
        self.cb_Scale.setChecked(False)
        # Comboboxes initialisation
        self.combob_BlobsDetection.addItems(return_blobs_algorithms())
        self.combob_LabelingOption.addItems(return_labeling_algorithms())
        self.combob_Contours.addItems(return_contouring_algorithms())
        self.combob_cmap.addItems(return_colormaps())
        if len(profiles_list) > 0:
            self.options_window.combob_Profiles.addItems(profiles_list)
        if self.appOptions.default_profile is not None:
            index = self.options_window.combob_SegmentationColors.findText(self.appOptions.profiles[self.appOptions.default_profile][0])
            self.options_window.combob_SegmentationColors.setCurrentIndex(index)
            index2 = self.options_window.combob_Colormap.findText(self.appOptions.profiles[self.appOptions.default_profile][1])
            self.options_window.combob_Colormap.setCurrentIndex(index2)
            self.options_window.combob_Profiles.setCurrentIndex(self.options_window.combob_Profiles.findText(self.appOptions.default_profile))
        else:
            index = self.options_window.combob_SegmentationColors.findText("yellow")
            self.options_window.combob_SegmentationColors.setCurrentIndex(index)
        # Methods
        self.installEventFilter(self)
        self.resizeEvent = lambda event : resize_main_window(self)
        directories = ["./temp/","./analysis/","./results/"]
        for dir in directories:
            if not os.path.exists(dir):
                os.makedirs(dir)
        self.clear_temp_repertory("./temp/")
        # Menu bar
        self.action_Load.triggered.connect(lambda : load_files(self))
        self.action_RemoveAllImages.triggered.connect(lambda : remove_all_images(self))
        self.action_RemoveCurrentImage.triggered.connect(lambda : remove_current_image(self))
        self.action_SaveAnalysis.triggered.connect(lambda : open_save_analysis_window(self))
        self.action_LoadAnalysis.triggered.connect(lambda : load_analysis(self))
        self.action_Quit_2.triggered.connect(lambda : close_app(self))
        self.action_BatchAnalysis.triggered.connect(lambda : open_batch_analysis_window(self))
        self.action_SeeOptions.triggered.connect(lambda : open_options_window(self))
        self.action_Version.triggered.connect(lambda : show_version())
        # Original image options
        self.hs_SliceNumber.valueChanged.connect(lambda : slider_value_changed(self))
        self.cb_IncludeImage.stateChanged.connect(lambda : checkbox_state_changed(self))
        self.pb_Histogram.clicked.connect(lambda : call_histogram_window(self))
        self.cb_Scale.stateChanged.connect(lambda : scale_checked(self))
        self.combob_FileName.activated.connect(lambda : combobox_changed(self))
        # Illumination
        self.le_RollingBallRadius.editingFinished.connect(lambda : input_rolling_ball_radius(self))
        self.pb_RollingBallRadiusToImage.clicked.connect(lambda : rolling_ball_to_image(self))
        self.pb_RollingBallRadiusToStack.clicked.connect(lambda : rolling_ball_to_stack(self))
        self.pb_RollingBallRadiusView.clicked.connect(lambda : view_illumination(self))
        # Segmentation
        self.le_ThresholdOne.editingFinished.connect(lambda : input_threshold_one(self))
        self.le_ThresholdTwo.editingFinished.connect(lambda : input_threshold_two(self))
        self.le_ThresholdOne.installEventFilter(self)
        self.le_ThresholdTwo.installEventFilter(self)
        self.combob_Threshold.activated.connect(lambda : threshold_option_changed(self))
        self.combob_SegmentationMethod.activated.connect(lambda : segmentation_method_changed(self))
        self.le_DLCheckpointPath.editingFinished.connect(lambda : input_dl_checkpoint_path(self))
        self.le_DLProbThresh.editingFinished.connect(lambda : input_dl_prob_thresh(self))
        self.le_DLBackgroundRadius.editingFinished.connect(lambda : input_dl_background_radius(self))
        self.le_BlobsDetectionMinimumRadius.editingFinished.connect(lambda : set_blobs_minimum_radius(self))
        self.le_BlobsDetectionMaximumRadius.editingFinished.connect(lambda : set_blobs_maximum_radius(self))
        self.combob_BlobsDetection.activated.connect(lambda : combobox_blobs_changed(self))
        self.pb_SegmentationToImage.clicked.connect(lambda : segmentation_to_image(self))
        self.pb_SegmentationToStack.clicked.connect(lambda : segmentation_to_stack(self))
        self.pb_SegmentationView.clicked.connect(lambda : view_segmentation(self))
        # Labeling
        self.le_SieveSize.editingFinished.connect(lambda : input_sieve_size(self))
        self.pb_LabelingToImage.clicked.connect(lambda : apply_labeling_to_image(self))
        self.pb_LabelingToStack.clicked.connect(lambda : apply_labeling_to_stack(self))
        self.pb_LabelingView.clicked.connect(lambda : view_labeling(self))
        # Contours
        self.combob_Contours.activated.connect(lambda : combobox_contours_changed(self))
        self.le_BackgroundThreshold.editingFinished.connect(lambda : input_background_threshold(self))
        self.pb_ContoursToImage.clicked.connect(lambda : apply_contours_to_image(self))
        self.pb_ContoursToStack.clicked.connect(lambda : apply_contours_to_stack(self))
        self.pb_ContoursView.clicked.connect(lambda : view_contours(self))
        self.le_CentroidX.editingFinished.connect(lambda : edit_centroid_x(self))
        self.le_CentroidY.editingFinished.connect(lambda : edit_centroid_y(self))
        self.pb_CentroidAuto.clicked.connect(lambda : set_centroid_auto(self))
        self.cb_MainSlice.stateChanged.connect(lambda : change_main_slice(self))
        self.le_ContoursMinSize.editingFinished.connect(lambda: input_integer_over_value(self.le_ContoursMinSize,0,False))
        # Density
        self.le_DensityTargetLayers.editingFinished.connect(lambda : input_target_layers(self))
        self.le_DensityMapKernelSize.editingFinished.connect(lambda : input_kernel_size(self))
        self.pb_DensityToImage.clicked.connect(lambda : apply_density_to_image(self))
        self.pb_DensityToStack.clicked.connect(lambda : apply_density_to_stack(self))
        self.pb_DensityView.clicked.connect(lambda : view_density(self))
        self.combob_DensityDisplay.activated.connect(lambda : combobox_density_changed(self))
        self.combob_cmap.activated.connect(lambda : combobox_density_changed(self))
        self.cb_SharedColorBar.stateChanged.connect(lambda : shared_colorbar_state_changed(self))
        # Results
        self.le_ZThickness.editingFinished.connect(lambda : input_z_thickness(self))
        self.le_InterZ.editingFinished.connect(lambda : input_inter_z(self))
        self.le_PixelSize.editingFinished.connect(lambda : input_pixel_size(self))
        self.le_PixelSize.editingFinished.connect(lambda : scale_checked(self,False))
        self.pb_ResultsApplyToStacks.clicked.connect(lambda : apply_infos_to_stacks(self))
        self.pb_ResultsView.clicked.connect(lambda : view_results_page(self))
        self.pb_ResultsAll.clicked.connect(lambda : select_all(self))
        self.pb_ResultsNone.clicked.connect(lambda : select_none(self))
        self.pb_ResultsDestinationFolder.clicked.connect(lambda : select_folder(self,self.lb_ResultsDestinationFolder))
        self.pb_ResultsBack.clicked.connect(lambda : return_to_images_screen(self))
        self.le_ResultsCSVFileName.editingFinished.connect(lambda: check_file_name(self,self.le_ResultsCSVFileName))
        self.pb_ResultsSave.clicked.connect(lambda : save_results(self))
        sync_deep_learning_controls(self)
        segmentation_method_changed(self, False)

    def _setup_segmentation_dl_controls(self):
        self.frame.setMinimumHeight(152)
        
        self.frame.setMaximumHeight(152)
        self.gb_Segmentation.setMinimumHeight(132)
        self.gb_Segmentation.setMaximumHeight(132)
        label_font = self.le_ThresholdOne.font()

        self.combob_SegmentationMethod = QtWidgets.QComboBox(self.gb_Segmentation)
        self.combob_SegmentationMethod.setObjectName("combob_SegmentationMethod")
        self.combob_SegmentationMethod.setFont(label_font)
        self.combob_SegmentationMethod.addItems(["Classical", "Deep learning (UNet-DC)"])
        self.gridLayout.removeWidget(self.combob_Threshold)
        self.gridLayout.addWidget(self.combob_SegmentationMethod, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.combob_Threshold, 0, 1, 1, 1)

        self.le_DLCheckpointPath = QtWidgets.QLineEdit(self.gb_Segmentation)
        self.le_DLCheckpointPath.setObjectName("le_DLCheckpointPath")
        self.le_DLCheckpointPath.setFont(label_font)
        self.le_DLCheckpointPath.setPlaceholderText("checkpoint")
        self.gridLayout.addWidget(self.le_DLCheckpointPath, 1, 0, 1, 2)

        self.le_DLProbThresh = QtWidgets.QLineEdit(self.gb_Segmentation)
        self.le_DLProbThresh.setObjectName("le_DLProbThresh")
        self.le_DLProbThresh.setFont(label_font)
        self.le_DLProbThresh.setText("0.3")
        self.le_DLProbThresh.setPlaceholderText("prob")
        self.gridLayout.addWidget(self.le_DLProbThresh, 1, 2, 1, 1)

        self.le_DLBackgroundRadius = QtWidgets.QLineEdit(self.gb_Segmentation)
        self.le_DLBackgroundRadius.setObjectName("le_DLBackgroundRadius")
        self.le_DLBackgroundRadius.setFont(label_font)
        self.le_DLBackgroundRadius.setText("50")
        self.le_DLBackgroundRadius.setPlaceholderText("radius")
        self.gridLayout.addWidget(self.le_DLBackgroundRadius, 1, 3, 1, 1)

    def eventFilter(self, obj, event):
        if (obj == self.le_ThresholdOne or obj == self.le_ThresholdTwo)  and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Up:
                if obj.text() != "I" and obj.text() != "II":
                    self.increment_value(obj)
                    return True
            elif event.key() == Qt.Key_Down:
                if obj.text() != "I" and obj.text() != "II":
                    self.decrement_value(obj)
                    return True
        if event.type() == QEvent.Wheel and (obj == self.le_ThresholdOne or obj == self.le_ThresholdTwo):
            if obj.text() != "I" and obj.text() != "II":
                value = float(obj.text())
                new_value = None
                if value >=1 and value <255 and event.angleDelta().y() > 0:
                    new_value = int(value+1)
                elif value >1 and value <=255 and event.angleDelta().y() <0:
                    new_value = int(value-1)
                elif value <1 and value >=0 and event.angleDelta().y() > 0:
                    new_value = round(float(value + 0.01),2)
                elif value <=1 and value >0 and event.angleDelta().y() <0:
                    new_value = round(float(value - 0.01),2)
                if new_value is not None:
                    obj.setText(str(new_value))
                    obj.editingFinished.emit()
                    return True
        return super().eventFilter(obj, event)
    
    def increment_value(self,obj):
        current_value = float(obj.text())
        if current_value >= 1 and current_value <255: 
            obj.setText(str(int(current_value + 1)))
            obj.editingFinished.emit()
        elif current_value <1:
            obj.setText(str(round(current_value + 0.01,2)))
            obj.editingFinished.emit()
        
    def decrement_value(self,obj):
        current_value = float(obj.text())
        if current_value <= 1 and current_value > 0:
            obj.setText(str(round(current_value - 0.01,2)))
            obj.editingFinished.emit()
        elif current_value > 1:
            obj.setText(str(int(current_value - 1)))
            obj.editingFinished.emit()
  
    def closeEvent(self,event):
        self.histogram_window.close()
        self.save_analysis_window.close()
        self.batch_analysis_window.close()
        self.options_window.close()
        super().closeEvent(event)

    def clear_temp_repertory(self,temp_path):
        now=datetime.now()
        retention_period=timedelta(days=7)
        for file in os.listdir(temp_path):
            if file.endswith(".joblib"):
                absolute_path=os.path.join(temp_path,file)
                if os.path.isdir(absolute_path):
                    continue
                modification_time=os.path.getmtime(absolute_path)
                modification_date=datetime.fromtimestamp(modification_time)
                if now - modification_date > retention_period:
                    os.remove(absolute_path)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
