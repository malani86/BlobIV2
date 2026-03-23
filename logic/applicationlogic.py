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

from skimage import draw
import imageio.v3 as iio
import numpy as np
import tifffile
from PySide6.QtWidgets import QFileDialog, QGroupBox, QDialog, QPushButton, QLabel, QVBoxLayout, QCheckBox, QTableWidgetItem, QLineEdit
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QCursor, QIcon
import matplotlib.pyplot as plt
from gui.MplCanvas import MplCanvas
from gui.MplCanvasHistogram import MplCanvasHistogram
from gui.app_ui import Ui_MainWindow
from gui.save_analysis_window import SaveAnalysisWindow
from gui.batch_analysis_window import BatchAnalysisWindow
from gui.options_window import Ui_OptionsWindow
from gui.custom_toolbar import CustomToolbar
from model.app_model import AppModel
from logic.algorithms import *
import random
import re
import csv
import os
from datetime import datetime
from joblib import dump, load
import resources.resources_rc

RUN_LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "run.log"))

def append_run_log(message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(RUN_LOG_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

def export_dl_debug_mask(filename: str, slice_number: int, mask: np.ndarray):
    base_name = os.path.splitext(os.path.basename(filename))[0]
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", base_name)
    output_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "temp",
            f"{safe_name}_slice_{slice_number+1:03d}_dl_gui_mask.png",
        )
    )
    iio.imwrite(output_path, (mask.astype(np.uint8) * 255))
    append_run_log(f"DL GUI mask exported to '{output_path}'")
    return output_path

def get_default_dl_checkpoint_path():
    candidates = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "best_UNetDC_focal_model.pth")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "best_UNetDC_focal_model.pth")),
        os.path.abspath("./best_UNetDC_focal_model.pth"),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return ""

def ensure_deep_learning_defaults(appMod: AppModel):
    if not hasattr(appMod, "original_stacks"):
        appMod.original_stacks = {}
    if not hasattr(appMod, "segmentation_method"):
        appMod.segmentation_method = "Classical"
    if not hasattr(appMod, "dl_checkpoint_path"):
        appMod.dl_checkpoint_path = get_default_dl_checkpoint_path()
    elif not appMod.dl_checkpoint_path:
        appMod.dl_checkpoint_path = get_default_dl_checkpoint_path()
    if not hasattr(appMod, "dl_prob_thresh"):
        appMod.dl_prob_thresh = 0.3
    if not hasattr(appMod, "dl_background_radius"):
        appMod.dl_background_radius = 50
    if not hasattr(appMod, "dl_device"):
        appMod.dl_device = "auto"

def sync_deep_learning_controls(window : Ui_MainWindow):
    appMod = window.appMod
    ensure_deep_learning_defaults(appMod)
    if hasattr(window, "combob_SegmentationMethod"):
        index = window.combob_SegmentationMethod.findText(appMod.segmentation_method)
        window.combob_SegmentationMethod.setCurrentIndex(index if index >= 0 else 0)
    if hasattr(window, "le_DLCheckpointPath"):
        window.le_DLCheckpointPath.setText(appMod.dl_checkpoint_path)
    if hasattr(window, "le_DLProbThresh"):
        window.le_DLProbThresh.setText(str(appMod.dl_prob_thresh))
    if hasattr(window, "le_DLBackgroundRadius"):
        window.le_DLBackgroundRadius.setText(str(appMod.dl_background_radius))


def resize_main_window(window : Ui_MainWindow):
    '''Resizes the images when the main window is resized
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        filename, slice_number = get_filename_slice_number(window)
        display_original_image(window,filename,slice_number,focus=window.focus)

def remove_all_images(window : Ui_MainWindow):
    '''Removes all the loaded images
    Parameters:
    window : an instance of the app'''
    window.combob_FileName.clear()
    window.appMod = AppModel()
    window.wi_OriginalText.hide()
    window.wi_Image1Text.hide()
    window.wi_Image2Text.hide()
    window.tabWidget.hide()
    window.gb_ResultsChoice.hide()
    window.wi_Image1Canvas.hide()
    window.wi_Image2Canvas.hide()
    window.wi_OriginalImage.hide()
    window.frame_4.hide()
    window.histogram_window.close()
    sync_deep_learning_controls(window)

def remove_current_image(window : Ui_MainWindow):
    '''Removes the current image from the comobox
    Parameters:
    window : an instance of the app'''
    appMod=window.appMod
    if len(appMod.stacks.keys()) == 1:
        remove_all_images(window)
    elif len(appMod.stacks.keys()) > 1:
        filename = window.combob_FileName.currentText()
        appMod.stack_names.remove(filename)
        del appMod.stacks[filename]
        del appMod.original_stacks[filename]
        del appMod.included_images[filename]
        del appMod.corrected_images[filename]
        del appMod.rolling_ball_param[filename]
        del appMod.rolling_ball_background[filename]
        del appMod.threshold_algo[filename]
        del appMod.first_threshold[filename]
        del appMod.second_threshold[filename]
        del appMod.thresholded_images[filename]
        del appMod.blobs_detection_algo[filename]
        del appMod.blobs_radius[filename]
        del appMod.blobs_thresholded_images[filename]
        del appMod.labeling_option[filename]
        del appMod.labeling_sieve_size[filename]
        del appMod.labeling_coordinates[filename]
        del appMod.labeling_labels[filename]
        del appMod.labeling_images_with_labels[filename]
        del appMod.labeling_images_conserved_blobs[filename]
        del appMod.contours_algo[filename]
        del appMod.contours_background[filename]
        del appMod.contours_mask[filename]
        del appMod.contours_centroids[filename]
        del appMod.contours_main_slice[filename]
        del appMod.density_target_layers[filename]
        del appMod.density_map_kernel_size[filename]
        del appMod.density_centroid_size[filename]
        del appMod.density_target_heatmap[filename]
        del appMod.density_map_heatmap[filename]
        del appMod.density_target_centroid_heatmap[filename]
        del appMod.density_map_centroid_heatmap[filename]
        del appMod.density_target_count_per_10k_pixels_heatmap[filename]
        del appMod.density_map_count_per_10k_pixels_heatmap[filename]
        del appMod.density_target_size[filename]
        del appMod.density_map_size[filename]
        del appMod.results_count[filename]
        del appMod.results_density[filename]
        del appMod.results_distance[filename]
        del appMod.stack_infos[filename]
        index = window.combob_FileName.findText(filename)
        window.combob_FileName.removeItem(index)
        window.combob_FileName.setCurrentIndex(0)
        combobox_changed(window)

def show_error_message(message):
    '''Displays a QDialog window with a warning message
    Parameters:
    message : the message to display'''
    dialog = QDialog()
    dialog.setWindowTitle("Error")
    icon = QIcon()
    icon.addFile(u":/Icons/blob-161097_640.png", QSize(), QIcon.Normal, QIcon.Off)
    dialog.setWindowIcon(icon)
    dialog.setModal(True)
    label = QLabel(message)
    label.setAlignment(Qt.AlignCenter)    
    button_ok = QPushButton("OK")
    button_ok.clicked.connect(dialog.accept)
    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(button_ok)
    dialog.setLayout(layout)
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)
    dialog.show()
    dialog.exec()

def empty_layout(layout):
    '''Removes all the items in a layout
    Parameters:
    layout: the name of the layout to empty'''
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()
        else:
            layout.removeItem(item)

def hide_text_layout_content(window : Ui_MainWindow, frame):
    '''Hides the chosen content of the QWidgets when displaying secondary images
    Parameters:
    window : an instance of the app
    frame: the number of the frame to hide'''
    if frame == 1:
        window.lb_TargetStats.hide()
        window.lb_MapStats.hide()
        window.combob_DensityDisplay.hide()
        window.combob_cmap.hide()
        window.cb_SharedColorBar.hide()

    else:
        window.lb_CentroidCoordinates.hide()
        window.lb_X.hide()
        window.le_CentroidX.hide()
        window.lb_Y.hide()
        window.le_CentroidY.hide()
        window.pb_CentroidAuto.hide()
        window.cb_MainSlice.hide()

def show_text_layout_content(window : Ui_MainWindow, frame):
    '''Shows the chosen content of the QWidgets whendisplaying secondary images
    Parameters:
    window : an instance of the app
    frame: the number of the frame to show'''
    if frame == 1:
        window.lb_TargetStats.show()
        window.lb_MapStats.show()
        window.combob_DensityDisplay.show()
        window.combob_cmap.show()
        window.cb_SharedColorBar.show()

    else:
        window.lb_CentroidCoordinates.show()
        window.lb_X.show()
        window.le_CentroidX.show()
        window.lb_Y.show()
        window.le_CentroidY.show()
        window.pb_CentroidAuto.show()
        window.cb_MainSlice.show()

def get_filename_slice_number(window : Ui_MainWindow):
    '''Gets the file name and the slice number of the currently displayed image
    Parameters:
    window : an instance of the app
    Returns:
    filename: the absolute path to the name
    slice_number: the index of the slice in the stack'''
    filename = window.combob_FileName.currentText()
    slice_number = int(window.hs_SliceNumber.value())
    return filename, slice_number

def get_histogram(window : Ui_MainWindow, appMod : AppModel,image,title):
    '''Creates an instance of the class MplCanvasHistogram
    Parameters:
    window : an instance of the app
    image: an image whose histogram will be created
    title: a string indicating the title to display on the histogram
    Returns:
    canvas_hist: an instance of the class MplCanvasHistogram'''
    canvas_hist = MplCanvasHistogram(window,8,4,100)
    canvas_hist.axes.hist(image.ravel(),bins=256, range=(0,255), log=True)
    canvas_hist.axes.tick_params(axis='x', labelsize=8)
    ticks = np.arange(0,256,25)
    canvas_hist.axes.set_xticks(ticks)
    canvas_hist.axes.tick_params(axis='y', labelsize=8)
    canvas_hist.axes.set_title(title, fontsize=10)
    return canvas_hist

def draw_histograms(window : Ui_MainWindow):
    '''Places an histogram in the histogram window
    Parameters:
    window : an instance of the app'''
    appMod=window.appMod
    layout = window.histogram_window.layout_Histogram
    empty_layout(layout)
    filename,slice_number = get_filename_slice_number(window)
    image = appMod.stacks[filename][slice_number]
    layout.addWidget(get_histogram(window,appMod,image,"8-bits original histogram"))
    if appMod.corrected_images[filename][slice_number] is not None:
        image = appMod.corrected_images[filename][slice_number]
        layout.addWidget(get_histogram(window,appMod,image,"Corrected 8-bits histogram"))
        window.histogram_window.wi_Histogram.adjustSize()

def display_original_image(window : Ui_MainWindow, filename, slice_number,focus = None):
    ''' Displays the original or the corrected image in the left part of the app
    Parameters:
    window : an instance of the app
    filename : name of the image file
    slice_number : number of the slice in the image file
    focus : string with the name of the presently highlighted tool'''
    window.setCursor(QCursor(Qt.WaitCursor))
    appMod=window.appMod
    window.sw_Data.setCurrentIndex(0)
    existingCanvas = window.wi_OriginalImage.findChildren(MplCanvas)
    if len(existingCanvas)>0:
        current_xlim = existingCanvas[0].axes.get_xlim()
        current_ylim = existingCanvas[0].axes.get_ylim()
    if appMod.corrected_images[filename][slice_number] is not None and window.focus != "illumination":
        image = appMod.corrected_images[filename][slice_number]
        title = f"Corrected image width: {image.shape[1]} height: {image.shape[0]}"
    else:
        image = appMod.stacks[filename][slice_number]
        title = f"Original image width: {image.shape[1]} height: {image.shape[0]}"
    px = 1/plt.rcParams['figure.dpi']
    canvas_original = MplCanvas(window,image.shape[1]*px,image.shape[0]*px,100)
    toolbar = CustomToolbar(canvas_original, window)
    toolbar.font_size = 6
    if not window.cb_IncludeImage.isChecked():
        canvas_original.axes.plot([0,image.shape[1]-1],[0,image.shape[0]-1],color='red',linewidth=2)
        canvas_original.axes.plot([image.shape[0]-1,0],[0,image.shape[1]-1],color='red',linewidth=2)
    if focus == "segmentation" and appMod.thresholded_images[filename][slice_number] is not None:
        if appMod.blobs_thresholded_images[filename][slice_number] is not None:
            mask = appMod.blobs_thresholded_images[filename][slice_number]
        else:
            mask = appMod.thresholded_images[filename][slice_number]
        coordinates = np.where(mask)
        image_rgb = np.empty((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        for i in range (3):
            image_rgb[:,:,i] = image
        if window.appOptions.default_profile is None:
            color = return_colors_dictionnary()[window.options_window.combob_SegmentationColors.currentText()]
        else:
            color = return_colors_dictionnary()[window.appOptions.profiles[window.appOptions.default_profile][0]]
        image_rgb[coordinates[0], coordinates[1]] = color
        image = image_rgb
    if focus == "density":
        heatmap = canvas_original.axes.imshow(image, cmap=window.combob_cmap.currentText(), interpolation='nearest')
        cbar = plt.colorbar(heatmap)
        cbar.ax.set_visible(False)
    if window.cb_Scale.isChecked() and window.cb_IncludeImage.isChecked():
        if len(image.shape) == 2:
            image = np.stack((image,image,image),axis = -1)
        position = window.options_window.combob_ScalePosition.currentText()
        scale_length = int(window.options_window.le_ScaleNumberPixels.text())
        if window.le_PixelSize.text() != "":
            pixel_size = float(window.le_PixelSize.text())
        else:
            pixel_size = float(window.options_window.le_StackInfoPixelSize.text())
        unit = window.options_window.le_ScaleUnit.text()
        scale_color=window.options_window.combob_ScaleColor.currentText()
        if "East" in position:
            x_begin = image.shape[1] - scale_length - 20
        else:
            x_begin = 20
        if "South" in position:
            y_begin = image.shape[0] - 20
        else:
            y_begin = 40
        text = f"{int(scale_length*pixel_size)} {unit}"
        canvas_original.axes.plot([x_begin, x_begin + scale_length], [y_begin,y_begin], linewidth=3, color=scale_color)
        canvas_original.axes.text(int(x_begin+scale_length/2), y_begin-20,text,color=scale_color,va='center', ha='center')
    canvas_original.fig.set_frameon(False)
    canvas_original.axes.set_axis_off()
    label = QLabel()
    label.setText(title)
    label.setMaximumHeight(20)
    label.setAlignment(Qt.AlignCenter)
    # canvas_original.fig.tight_layout()
    canvas_original.axes.imshow(image, cmap='gray')
    empty_layout(window.layout_Original)
    window.layout_Original.addWidget(label)
    window.layout_Original.addWidget(canvas_original)
    window.layout_Original.addWidget(toolbar)
    if focus == "density":
        canvas_original.fig.subplots_adjust(0, 0.01, 1, 0.99, 0, 0)
    else:
        canvas_original.fig.subplots_adjust(0, 0, 1, 1, 0, 0)
    window.wi_OriginalText.setFixedWidth(int(window.size().width()/3))
    window.wi_OriginalText.show()
    window.wi_OriginalImage.setFixedWidth(int(window.size().width()/3))
    window.wi_OriginalImage.show()
    if len(existingCanvas)>0:
        canvas_original.axes.set_xlim(current_xlim)
        canvas_original.axes.set_ylim(current_ylim)
        canvas_original.draw_idle()
    display_secondary_image(1,window,focus = focus)
    display_secondary_image(2,window,focus = focus)
    if window.cb_IncludeImage.isChecked():
        draw_histograms(window)
    else:
        empty_layout(window.histogram_window.layout_Histogram)
    window.setCursor(QCursor(Qt.ArrowCursor))

def update_image_slider_range(window : Ui_MainWindow, filename):
    ''' Update the range of the slider depending on the image file
    Parameters:
    window : an instance of the app
    filename : a string with the name of the file'''
    window.hs_SliceNumber.setValue(0)
    window.hs_SliceNumber.setMinimum(0)
    window.hs_SliceNumber.setMaximum(len(window.appMod.stacks[filename])-1)
    window.lb_SliceNumber.setText(f"{int(window.hs_SliceNumber.value())+1} / {len(window.appMod.stacks[filename])}")

def restore_images_original_size(window : Ui_MainWindow):
    ''' Restores the original size of the images
    Parameters:
    window : an instance of the app'''
    all_canvases = window.findChildren(MplCanvas)
    for canvas in all_canvases:
        canvas.axes.set_xlim(canvas.original_xlim[0]-0.5,canvas.original_xlim[1]-0.5)
        canvas.axes.set_ylim(canvas.original_ylim[1]-0.5,canvas.original_ylim[0]-0.5)
        canvas.draw_idle()
        canvas.previous_xlim = (canvas.original_xlim[0]-0.5,canvas.original_xlim[1]-0.5)
        canvas.previous_ylim = (canvas.original_ylim[1]-0.5,canvas.original_ylim[0]-0.5)

def load_raw_stack_frames(filename):
    '''Loads a file as a list of original frames without BlobInspector preprocessing.'''
    lower_name = filename.lower()
    if lower_name.endswith(".tif") or lower_name.endswith(".tiff"):
        with tifffile.TiffFile(filename) as tif:
            frames = [page.asarray() for page in tif.pages]
        if len(frames) == 0:
            raise ValueError(f"No image frames found in file: {filename}")
        return frames

    image_data = np.asarray(iio.imread(filename))
    if image_data.ndim == 2:
        return [image_data]
    if image_data.ndim == 3:
        if image_data.shape[-1] in (3, 4):
            return [image_data]
        return [frame for frame in image_data]
    if image_data.ndim == 4 and image_data.shape[-1] in (3, 4):
        return [frame for frame in image_data]
    raise ValueError(f"Unsupported image dimensions for file: {filename}")

def load_stack_frames(filename):
    '''Loads a file as a list of 2D 8-bit frames.'''
    return [convert_to_8_bits(frame) for frame in load_raw_stack_frames(filename)]

def get_original_frame_for_dl(appMod: AppModel, filename, slice_number: int):
    '''Returns the original frame for deep-learning inference, reloading from disk if needed.'''
    ensure_deep_learning_defaults(appMod)
    if filename not in appMod.original_stacks or len(appMod.original_stacks[filename]) <= slice_number:
        if os.path.exists(filename):
            appMod.original_stacks[filename] = load_raw_stack_frames(filename)
            append_run_log(f"Reloaded original frames from disk for DL inference: file='{filename}'")
        else:
            raise ValueError(
                "Deep learning segmentation requires the original image data. "
                "Please reload the source image file instead of using only a saved analysis."
            )
    return appMod.original_stacks[filename][slice_number]

def load_files(window : Ui_MainWindow):
    ''' Loads the image files
    Parameters:
    window : an instance of the app'''
    filenames, _ = QFileDialog.getOpenFileNames(window,
        "Choose files",
        "/",
        "Image files (*.*)"
    )
    for filename in filenames:
        try:
            window.appMod.original_stacks[filename] = load_raw_stack_frames(filename)
            window.appMod.stacks[filename] = load_stack_frames(filename)
        except Exception as e:
            show_error_message(f"Unable to load image file:\n{filename}\n\n{e}")
            continue
        length = len(window.appMod.stacks[filename])
        window.appMod.included_images[filename] = [True]*length
        window.appMod.corrected_images[filename] = [None]*length
        window.appMod.rolling_ball_param[filename] = [None]*length
        window.appMod.rolling_ball_background[filename] = [None]*length
        window.appMod.threshold_algo[filename] = [None]*length
        window.appMod.first_threshold[filename] = [None]*length
        window.appMod.second_threshold[filename] = [None]*length
        window.appMod.thresholded_images[filename] = [None]*length
        window.appMod.blobs_detection_algo[filename] = [None]*length
        window.appMod.blobs_radius[filename] = [None]*length
        window.appMod.blobs_thresholded_images[filename] = [None]*length
        window.appMod.labeling_option[filename] = [None]*length
        window.appMod.labeling_sieve_size[filename] = [None]*length
        window.appMod.labeling_coordinates[filename] = [None]*length
        window.appMod.labeling_labels[filename] = [None]*length
        window.appMod.labeling_images_with_labels[filename] = [None]*length
        window.appMod.labeling_images_conserved_blobs[filename] = [None]*length
        window.appMod.contours_algo[filename] = [None]*length
        window.appMod.contours_background[filename] = [None]*length
        window.appMod.contours_mask[filename] = [None]*length
        window.appMod.contours_centroids[filename] = [None]*length
        window.appMod.contours_main_slice[filename] = [False]*length
        window.appMod.density_target_layers[filename] = [None]*length
        window.appMod.density_map_kernel_size[filename] = [None]*length
        window.appMod.density_centroid_size[filename] = [None]*length
        window.appMod.density_target_heatmap[filename] = [None]*length
        window.appMod.density_map_heatmap[filename] = [None]*length
        window.appMod.density_target_centroid_heatmap [filename] = [None]*length
        window.appMod.density_map_centroid_heatmap[filename] = [None]*length
        window.appMod.density_target_count_per_10k_pixels_heatmap[filename] = [None]*length
        window.appMod.density_map_count_per_10k_pixels_heatmap[filename] = [None]*length
        window.appMod.density_target_size[filename] = [None]*length
        window.appMod.density_map_size[filename] = [None]*length
        window.appMod.results_count[filename] = None
        window.appMod.results_density[filename] = None
        window.appMod.results_distance[filename] = None
        window.appMod.stack_infos[filename] = [None, None, None]

    sync_deep_learning_controls(window)
    window.appMod.stack_names = list(window.appMod.stacks.keys())
    if window.appMod.stack_names:
        window.combob_FileName.clear()
        window.combob_FileName.addItems(window.appMod.stack_names)
        highlight_groupbox(window,None)
        window.combob_FileName.setCurrentIndex(0)
        if window.appMod.included_images[window.appMod.stack_names[0]][0]:
            window.cb_IncludeImage.setCheckState(Qt.CheckState.Checked)
        else:
            window.cb_IncludeImage.setCheckState(Qt.CheckState.Unchecked)
        set_current_image_options(window,window.appMod.stack_names[0],0)
        display_original_image(window,window.appMod.stack_names[0],0)
        restore_images_original_size(window)
        update_image_slider_range(window,window.appMod.stack_names[0])

def close_app(window : Ui_MainWindow):
    '''Closes the main window and all the children windows
    Parameters:
    window : an instance of the app'''
    window.histogram_window.close()
    window.save_analysis_window.close()
    window.batch_analysis_window.close()
    window.options_window.close()
    window.close()

def open_batch_analysis_window(window : Ui_MainWindow):
    '''Opens the window to choose the options for a batch analysis
    Parameters:
    window : an instance of the app'''
    window.batch_analysis_window = BatchAnalysisWindow(window)
    bw = window.batch_analysis_window
    bw.le_RollingBallRadius.editingFinished.connect(lambda : input_positive_integer(bw.le_RollingBallRadius))
    bw.le_DensityTargetLayers.editingFinished.connect(lambda : input_positive_integer(bw.le_DensityTargetLayers))
    bw.le_ZThickness.editingFinished.connect(lambda : input_float(bw.le_ZThickness))
    bw.le_InterZ.editingFinished.connect(lambda : input_float(bw.le_InterZ))
    bw.le_PixelSize.editingFinished.connect(lambda : input_float(bw.le_PixelSize))
    bw.le_SieveSize.editingFinished.connect(lambda : input_integer_over_value(bw.le_SieveSize,0,False))
    bw.le_BackgroundThreshold.editingFinished.connect(lambda : input_integer_over_value(bw.le_BackgroundThreshold,0,False))
    bw.le_ContoursMinSize.editingFinished.connect(lambda : input_integer_over_value(bw.le_ContoursMinSize,0,False))
    bw.le_DensityMapKernelSize.editingFinished.connect(lambda : input_integer_over_value(bw.le_DensityMapKernelSize,3,True))
    bw.combob_BlobsDetection.addItems(return_blobs_algorithms())
    bw.combob_LabelingOption.addItems(return_labeling_algorithms())
    bw.combob_Contours.addItems(return_contouring_algorithms())
    bw.le_BlobsDetectionMinimumRadius.editingFinished.connect(lambda : input_blobs_radius(bw.le_BlobsDetectionMinimumRadius,bw.le_BlobsDetectionMaximumRadius,1))
    bw.le_BlobsDetectionMaximumRadius.editingFinished.connect(lambda : input_blobs_radius(bw.le_BlobsDetectionMaximumRadius,bw.le_BlobsDetectionMinimumRadius,1))
    bw.le_ThresholdOne.editingFinished.connect(lambda : input_thresholds(bw,bw.le_ThresholdOne,bw.le_ThresholdTwo,0,255,"I"))
    bw.le_ThresholdTwo.editingFinished.connect(lambda : input_thresholds(bw,bw.le_ThresholdTwo,bw.le_ThresholdOne,0,255,"II"))
    bw.combob_Threshold.currentTextChanged.connect(lambda : change_threshold_combobox(bw.combob_Threshold,bw.le_ThresholdTwo))
    bw.pb_DefaultOptions.clicked.connect(lambda : input_default_options(window))
    bw.pb_StartAnalysis.clicked.connect(lambda : start_batch_analysis(window))
    bw.show()

def input_default_options(window : Ui_MainWindow):
    '''Fills in the form for batch analysis with the default options
    Parameters:
    window : an instance of the app'''
    if window.options_window.combob_Profiles.currentText():
        options = window.appOptions.profiles[window.options_window.combob_Profiles.currentText()]
        bw = window.batch_analysis_window
        bw.le_RollingBallRadius.setText(options[6])
        bw.combob_Threshold.setCurrentIndex(bw.combob_Threshold.findText(options[7]))
        bw.le_ThresholdOne.setText(options[8])
        bw.le_ThresholdTwo.setText(options[9])
        bw.combob_BlobsDetection.setCurrentIndex(bw.combob_BlobsDetection.findText(options[10]))
        bw.le_BlobsDetectionMinimumRadius.setText(options[11])
        bw.le_BlobsDetectionMaximumRadius.setText(options[12])
        bw.combob_LabelingOption.setCurrentIndex(bw.combob_LabelingOption.findText(options[13]))
        bw.le_SieveSize.setText(options[14])
        bw.combob_Contours.setCurrentIndex(bw.combob_Contours.findText(options[15]))
        bw.le_BackgroundThreshold.setText(options[16])
        bw.le_DensityMapKernelSize.setText(options[17])
        bw.le_DensityTargetLayers.setText(options[18])
        bw.le_ZThickness.setText(options[19])
        bw.le_InterZ.setText(options[20])
        bw.le_PixelSize.setText(options[21])
        bw.le_ContoursMinSize.setText(options[22])
    else:
        show_error_message("Please select a profile in the Options.")
    
def start_batch_analysis(window : Ui_MainWindow):
    '''Processes the batch analysis and saves the results in the /temp directory
    Parameters:
    window : an instance of the app'''
    bw = window.batch_analysis_window
    filenames = list(window.appMod.stacks.keys())
    if not len(filenames) == 0:
        bw.setCursor(QCursor(Qt.WaitCursor))
        if bw.le_RollingBallRadius.text() != "":
            for filename in filenames:
                index = window.combob_FileName.findText(filename)
                window.combob_FileName.setCurrentIndex(index)
                window.le_RollingBallRadius.setText(bw.le_RollingBallRadius.text())
                rolling_ball_to_stack(window,False)
        if bw.le_ThresholdOne.text() != "I":
            for filename in filenames:
                index = window.combob_FileName.findText(filename)
                window.combob_FileName.setCurrentIndex(index)
                window.combob_Threshold.setCurrentIndex(bw.combob_Threshold.currentIndex())
                window.combob_BlobsDetection.setCurrentIndex(bw.combob_BlobsDetection.currentIndex())
                window.le_ThresholdOne.setText(bw.le_ThresholdOne.text())
                window.le_ThresholdTwo.setEnabled(bw.le_ThresholdTwo.isEnabled())
                window.le_ThresholdTwo.setText(bw.le_ThresholdTwo.text())
                window.le_BlobsDetectionMinimumRadius.setText(bw.le_BlobsDetectionMinimumRadius.text())
                window.le_BlobsDetectionMaximumRadius.setText(bw.le_BlobsDetectionMaximumRadius.text())
                segmentation_to_stack(window,False)
        if bw.le_SieveSize.text() != "":
            for filename in filenames:
                index = window.combob_FileName.findText(filename)
                window.combob_FileName.setCurrentIndex(index)
                window.combob_LabelingOption.setCurrentIndex(bw.combob_LabelingOption.currentIndex())
                window.le_SieveSize.setText(bw.le_SieveSize.text())
                apply_labeling_to_stack(window,False)
                compute_count_results(window,filename,len(window.appMod.stacks[filename]))
        if bw.le_BackgroundThreshold.text() != "":
            infos_applied = False
            for filename in filenames:
                index = window.combob_FileName.findText(filename)
                window.combob_FileName.setCurrentIndex(index)
                window.combob_Contours.setCurrentIndex(bw.combob_Contours.currentIndex())
                window.le_BackgroundThreshold.setText(bw.le_BackgroundThreshold.text())
                window.le_ContoursMinSize.setText(bw.le_ContoursMinSize.text())
                apply_contours_to_stack(window,False)
                compute_distance = False
                for i in range(len(window.appMod.labeling_labels[filename])):
                    if window.appMod.labeling_labels[filename][i] is not None:
                        compute_distance = True
                        break
                if compute_distance == True:
                    if infos_applied == False:
                        window.le_ZThickness.setText(bw.le_ZThickness.text())
                        window.le_InterZ.setText(bw.le_InterZ.text())
                        window.le_PixelSize.setText(bw.le_PixelSize.text())
                        apply_infos_to_stacks(window)
                        infos_applied = True
                    compute_distance_results(window,filename,len(window.appMod.stacks[filename]))
        if bw.le_DensityMapKernelSize.text() != "" and bw.le_DensityTargetLayers.text() != "":
            for filename in filenames:
                index = window.combob_FileName.findText(filename)
                window.combob_FileName.setCurrentIndex(index)
                window.le_DensityTargetLayers.setText(bw.le_DensityTargetLayers.text())
                window.le_DensityMapKernelSize.setText(bw.le_DensityMapKernelSize.text())
                apply_density_to_stack(window,False)
                compute_density = False
                for i in range(len(window.appMod.contours_mask[filename])):
                    if window.appMod.contours_mask[filename][i] is not None:
                        compute_density = True
                        break
                if compute_density == True:
                    compute_density_results(window,filename,len(window.appMod.stacks[filename]))
        now = datetime.now()
        filename = now.strftime("%Y-%m-%d_%H-%M-%S")
        dump(window.appMod,"./temp/"+filename+"_analysis.joblib",compress= True)
        show_save_message("The batch analysis has been successfully performed.\nThe file has been saved in the /temp repertory with a time stamp and will be kept for 7 days.")
        window.combob_FileName.setCurrentIndex(0)
        window.hs_SliceNumber.setValue(0)
        set_current_image_options(window,filenames[0],0)
        display_original_image(window,filenames[0],0,focus=window.focus)
        bw.close()
    else:
        show_error_message("Please choose some images to process.")

def initialise_options_window(window : Ui_MainWindow):
    '''Connects the widgets from the options window to the required functions
    Parameters:
    window : an instance of the app'''
    ow = window.options_window
    ow.combob_Profiles.currentTextChanged.connect(lambda : profile_changed(window))
    ow.combob_SegmentationColors.currentTextChanged.connect(lambda : segmentation_color_changed(window))
    ow.combob_Colormap.currentTextChanged.connect(lambda : colormap_changed(window))
    ow.le_ScaleNumberPixels.editingFinished.connect(lambda : input_positive_integer(ow.le_ScaleNumberPixels))
    ow.le_ScaleNumberPixels.editingFinished.connect(lambda : scale_checked(window,False))
    ow.le_IlluminationRollingBallRadius.editingFinished.connect(lambda : input_positive_integer(ow.le_IlluminationRollingBallRadius))
    ow.combob_Threshold.currentTextChanged.connect(lambda : change_threshold_combobox(ow.combob_Threshold,ow.le_SegmentationThresholdTwo))
    ow.le_SegmentationThresholdOne.editingFinished.connect(lambda : input_thresholds(ow,ow.le_SegmentationThresholdOne,ow.le_SegmentationThresholdTwo,0,255,"I"))
    ow.le_SegmentationThresholdTwo.editingFinished.connect(lambda : input_thresholds(ow,ow.le_SegmentationThresholdTwo,ow.le_SegmentationThresholdOne,0,255,"II"))
    ow.le_SegmentationBlobsMinRadius.editingFinished.connect(lambda : input_blobs_radius(ow.le_SegmentationBlobsMinRadius,ow.le_SegmentationBlobsMaxRadius,1))
    ow.le_SegmentationBlobsMaxRadius.editingFinished.connect(lambda : input_blobs_radius(ow.le_SegmentationBlobsMaxRadius,ow.le_SegmentationBlobsMinRadius,1))
    ow.le_LabelingSieveSize.editingFinished.connect(lambda : input_integer_over_value(ow.le_LabelingSieveSize,0,False))
    ow.le_ContoursBackground.editingFinished.connect(lambda : input_integer_over_value(ow.le_ContoursBackground,0,False))
    ow.le_ContoursMinSize.editingFinished.connect(lambda : input_integer_over_value(ow.le_ContoursMinSize,0,False))
    ow.le_DensityKernelSize.editingFinished.connect(lambda : input_integer_over_value(ow.le_DensityKernelSize,3,True))
    ow.le_StackInfoSliceThickness.editingFinished.connect(lambda : input_float(ow.le_StackInfoSliceThickness))
    ow.le_StackInfoIntersliceSpace.editingFinished.connect(lambda : input_float(ow.le_StackInfoIntersliceSpace))
    ow.le_StackInfoPixelSize.editingFinished.connect(lambda : input_float(ow.le_StackInfoPixelSize))
    ow.le_StackInfoPixelSize.editingFinished.connect(lambda : scale_checked(window,False))
    ow.pb_UpdateProfile.clicked.connect(lambda : update_profile(window))
    ow.pb_CreateNewProfile.clicked.connect(lambda : create_new_profile(window))
    ow.pb_RemoveProfile.clicked.connect(lambda : remove_profile(window))

def open_options_window(window : Ui_MainWindow):
    '''Shows the option window
    Parameters:
    window : an instance of the app'''
    window.options_window.show()

def segmentation_color_changed(window : Ui_MainWindow):
    '''Update the display of the original image when the segmentation color is changed in the options window
    Parameters:
    window : an instance of the app'''
    if window.focus == "segmentation":
        ow = window.options_window
        filename, slice_number = get_filename_slice_number(window)
        profilename = ow.combob_Profiles.currentText()
        if window.appOptions.default_profile is not None:
            previous_color = window.appOptions.profiles[profilename][0]
            window.appOptions.profiles[profilename][0] = ow.combob_SegmentationColors.currentText()
            display_original_image(window,filename,slice_number,focus="segmentation")
            window.appOptions.profiles[profilename][0] = previous_color
        else:
            display_original_image(window,filename,slice_number,focus="segmentation")

def remove_profile(window : Ui_MainWindow):
    '''Removes the current profile
    Parameters:
    window : an instance of the app'''
    ow = window.options_window
    if ow.combob_Profiles.currentText():
        profilename = ow.combob_Profiles.currentText()
        del window.appOptions.profiles[profilename]
        index = ow.combob_Profiles.findText(profilename)
        ow.combob_Profiles.removeItem(index)
        if ow.combob_Profiles.count() > 0:
            ow.combob_Profiles.setCurrentIndex(0)
        else:
            window.appOptions.default_profile = None
            
        dump(window.appOptions,"./options.joblib",compress= True)

def profile_changed(window : Ui_MainWindow):
    '''Updates the default options on profile change
    Parameters:
    window : an instance of the app'''
    ow = window.options_window
    if ow.combob_Profiles.currentText():
        window.appOptions.default_profile = ow.combob_Profiles.currentText()
        profilename = ow.combob_Profiles.currentText()
        ow.combob_SegmentationColors.setCurrentIndex(ow.combob_SegmentationColors.findText(window.appOptions.profiles[profilename][0]))
        ow.combob_Colormap.setCurrentIndex(ow.combob_Colormap.findText(window.appOptions.profiles[profilename][1]))
        ow.le_ScaleNumberPixels.setText(window.appOptions.profiles[profilename][2])
        ow.le_ScaleUnit.setText(window.appOptions.profiles[profilename][3])
        ow.combob_ScalePosition.setCurrentIndex(ow.combob_ScalePosition.findText(window.appOptions.profiles[profilename][4]))
        ow.combob_ScaleColor.setCurrentIndex(ow.combob_ScaleColor.findText(window.appOptions.profiles[profilename][5]))
        ow.le_IlluminationRollingBallRadius.setText(window.appOptions.profiles[profilename][6])
        ow.combob_Threshold.setCurrentIndex(ow.combob_Threshold.findText(window.appOptions.profiles[profilename][7]))
        ow.le_SegmentationThresholdOne.setText(window.appOptions.profiles[profilename][8])
        ow.le_SegmentationThresholdTwo.setText(window.appOptions.profiles[profilename][9])
        ow.combob_SegmentationBlobs.setCurrentIndex(ow.combob_SegmentationBlobs.findText(window.appOptions.profiles[profilename][10]))
        ow.le_SegmentationBlobsMinRadius.setText(window.appOptions.profiles[profilename][11])
        ow.le_SegmentationBlobsMaxRadius.setText(window.appOptions.profiles[profilename][12])
        ow.combob_Labeling.setCurrentIndex(ow.combob_Labeling.findText(window.appOptions.profiles[profilename][13]))
        ow.le_LabelingSieveSize.setText(window.appOptions.profiles[profilename][14])
        ow.combob_Contours.setCurrentIndex(ow.combob_Contours.findText(window.appOptions.profiles[profilename][15]))
        ow.le_ContoursBackground.setText(window.appOptions.profiles[profilename][16])
        ow.le_DensityKernelSize.setText(window.appOptions.profiles[profilename][17])
        ow.le_DensityLayers.setText(window.appOptions.profiles[profilename][18])
        ow.le_StackInfoSliceThickness.setText(window.appOptions.profiles[profilename][19])
        ow.le_StackInfoIntersliceSpace.setText(window.appOptions.profiles[profilename][20])
        ow.le_StackInfoPixelSize.setText(window.appOptions.profiles[profilename][21])
        ow.le_ContoursMinSize.setText(window.appOptions.profiles[profilename][22])
        dump(window.appOptions,"./options.joblib",compress= True)
        scale_checked(window,False)


def update_profile(window : Ui_MainWindow):
    '''Updates the current profile with the chosen options
    Parameters:
    window : an instance of the app'''
    ow = window.options_window
    if ow.combob_Profiles.currentText():
        profilename = ow.combob_Profiles.currentText()
        save_profile(window,profilename)
    else:
        show_error_message("Please choose a profile to update.")

def save_profile(window : Ui_MainWindow, profilename):
    '''Saves the profile in the options.joblib file
    Parameters:
    window : an instance of the app
    profilename : string with the name of the profile to save'''
    ow = window.options_window
    window.appOptions.profiles[profilename] = [ow.combob_SegmentationColors.currentText(),\
                                            ow.combob_Colormap.currentText(),\
                                            ow.le_ScaleNumberPixels.text(),\
                                            ow.le_ScaleUnit.text(),\
                                            ow.combob_ScalePosition.currentText(),\
                                            ow.combob_ScaleColor.currentText(),\
                                            ow.le_IlluminationRollingBallRadius.text(),\
                                            ow.combob_Threshold.currentText(),\
                                            ow.le_SegmentationThresholdOne.text(),\
                                            ow.le_SegmentationThresholdTwo.text(),\
                                            ow.combob_SegmentationBlobs.currentText(),\
                                            ow.le_SegmentationBlobsMinRadius.text(),\
                                            ow.le_SegmentationBlobsMaxRadius.text(),\
                                            ow.combob_Labeling.currentText(),\
                                            ow.le_LabelingSieveSize.text(),\
                                            ow.combob_Contours.currentText(),\
                                            ow.le_ContoursBackground.text(),\
                                            ow.le_DensityKernelSize.text(),\
                                            ow.le_DensityLayers.text(),\
                                            ow.le_StackInfoSliceThickness.text(),\
                                            ow.le_StackInfoIntersliceSpace.text(),\
                                            ow.le_StackInfoPixelSize.text(),\
                                            ow.le_ContoursMinSize.text()]
    dump(window.appOptions,"./options.joblib",compress= True)

def create_new_profile(window : Ui_MainWindow):
    '''Creates a new profile with the chosen options
    Parameters:
    window : an instance of the app'''
    ow = window.options_window
    profilename = choose_profile_name()
    if profilename != "":
        if profilename in window.appOptions.profiles.keys():
            show_error_message("This profile already exists. Choose the profile and select the update profile option.")
        else:
            save_profile(window,profilename)
            ow.combob_Profiles.addItem(profilename)
            ow.combob_Profiles.setCurrentIndex(ow.combob_Profiles.findText(profilename))
            window.appOptions.default_profile = profilename

def choose_profile_name():
    '''Calls a QDialog to input the profile name
    Returns:
    The input name for the profile'''
    dialog = QDialog()
    dialog.setWindowTitle("Choose profile name")
    icon = QIcon()
    icon.addFile(u":/Icons/blob-161097_640.png", QSize(), QIcon.Normal, QIcon.Off)
    dialog.setWindowIcon(icon)
    layout = QVBoxLayout()
    label = QLabel()
    label.setText("Please choose a profile name")
    line_edit = QLineEdit()
    layout.addWidget(label)
    layout.addWidget(line_edit)
    button_OK = QPushButton("OK")
    button_OK.clicked.connect(dialog.accept)
    layout.addWidget(button_OK)
    button_cancel = QPushButton("Cancel")
    button_cancel.clicked.connect(dialog.reject)
    layout.addWidget(button_cancel)
    dialog.setLayout(layout)
    if dialog.exec() == QDialog.Accepted:
        return line_edit.text()
    else:
        return ""

def colormap_changed(window : Ui_MainWindow):
    '''Changes the colormap in the density tool and updates the display
    Parameters:
    window : an instance of the app'''
    index = window.options_window.combob_Colormap.currentIndex()
    window.combob_cmap.setCurrentIndex(index)
    if window.focus == "density":
        filename,slice_number=get_filename_slice_number(window)
        if window.combob_DensityDisplay.currentText() == "Percentage":
            display_secondary_image(1,window,window.appMod.density_map_heatmap[filename][slice_number],focus="density",title="Convoluted density heatmap (percentage)")
            display_secondary_image(2,window,window.appMod.density_target_heatmap[filename][slice_number],focus = "density", title = "Target density heatmap (percentage)")
        if window.combob_DensityDisplay.currentText() == "Count":
            display_secondary_image(1,window,window.appMod.density_map_centroid_heatmap[filename][slice_number],focus="density",title="Convoluted density heatmap (Count)")
            display_secondary_image(2,window,window.appMod.density_target_centroid_heatmap [filename][slice_number],focus = "density", title = "Target density heatmap (Count)")

def show_version():
    '''Displays a QDialog window with information about the software version'''
    dialog = QDialog()
    dialog.setWindowTitle("Version information")
    icon = QIcon()
    icon.addFile(u":/Icons/blob-161097_640.png", QSize(), QIcon.Normal, QIcon.Off)
    dialog.setWindowIcon(icon)
    dialog.setModal(True)
    label = QLabel("Blob inspector v0.9 (March 2024)\n\
                   Blob Inspector was developped by Laurent Busson as a final project for a Master's degree in Bioinformatics at the University of Bordeaux.\n\
                   This project was made in collaboration with BRIC (BoRdeaux Institute of onCology) Team 1, UMR1312, INSERM, Univ. Bordeaux\n\
                   and LaBRI (Laboratoire Bordelais de Recherche en Informatique) - Universite Bordeaux.\n\
                   Blob Inspector is under GNU GPL license.")
    label.setAlignment(Qt.AlignCenter)
    button_ok = QPushButton("OK")
    button_ok.clicked.connect(dialog.accept)
    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(button_ok)
    dialog.setLayout(layout)
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)
    dialog.show()
    dialog.exec()

def input_positive_integer(widget):
    '''Controls that the input in a widget is a positive integer
    Parameters:
    widget: the widget in which the input is made'''
    if not widget.text().isdigit() or int(widget.text()) <=0:
        if widget.text() != "":
            show_error_message("Please insert a positive integer.")
            widget.clear()

def input_float(widget):
    '''Controls that the input in a widget is a positive float
    Parameters:
    widget: the widget in which the input is made'''
    if not is_float(widget.text()) or float(widget.text())<=0:
        if widget.text() != "":
            show_error_message("Please insert a positive value.")
            widget.clear()

def input_integer_over_value(widget,value,odd):
    '''Controls that the input in a widget is a positive integer equal or greater than a given value
    Parameters:
    widget: the widget in which the input is made
    value: the value to which the input must be at least equal
    odd: if True, the input must be an odd integer'''
    if not widget.text().isdigit() or int(widget.text()) < value:
        if widget.text() != "":
            show_error_message(f"Please insert an integer superior or equal to {value}.")
            widget.clear()
            return False
    else:
        if odd == True and int(widget.text())%2==0:
            show_error_message(f"Please insert an odd integer superior or equal to {value}.")
            widget.clear()
            return False
    return True

def input_blobs_radius(widget1, widget2, value):
    '''Controls the inputs in two widgets
    Parameters:
    widget1: the first widget
    widget2: the second widget
    value: a value above which the inputs must be'''
    if widget1.text() !="min" and widget1.text() !="max":
        if input_integer_over_value(widget1,value,False):
            if widget1.objectName() == "le_BlobsDetectionMinimumRadius" or widget1.objectName() == "le_SegmentationBlobsMinRadius":
                if widget2.text() == "max" or int(widget2.text()) < int(widget1.text()):
                    widget2.setText(widget1.text())
            elif widget1.objectName() == "le_BlobsDetectionMaximumRadius" or widget1.objectName() == "le_SegmentationBlobsMaxRadius":
                if widget2.text() == "min" or int(widget1.text()) < int(widget2.text()):
                    widget2.setText(widget1.text())
        else:
            widget1.editingFinished.disconnect()
            if widget1.objectName() == "le_BlobsDetectionMinimumRadius":
                widget1.setText("min")
            elif widget1.objectName() == "le_BlobsDetectionMaximumRadius":
                widget1.setText("max")
            widget1.clearFocus()
            widget1.editingFinished.connect(lambda : input_blobs_radius(widget1,widget2,value))

def check_value_range(value,min_value,max_value):
    '''Controls that a value is in a given range
    Parameters:
    value: the value to control
    min_value: the minimum range value (included)
    max_value: the maximum range value (included)'''
    if is_float(value) and float(value)>=min_value and float(value)<=max_value:
        return True
    return False

def input_thresholds(window, widget1, widget2, min_value, max_value, original_text):
    '''Controls the input values in two widgets
    Parameters:
    window: an instance of the class BatchAnalysisWindow or OptionsWindow
    widget1: the first widget in which a value is input
    widget2: the second widget in which a value is input
    min_value: the minimum range value (included)
    max_value: the maximum range value (included)
    original_text: a string with the original text of the first widget'''
    if widget1.text() !="I" and widget1.text() !="II":
        if check_value_range(widget1.text(),min_value,max_value):
            if window.combob_Threshold.currentText() == "One threshold":
                if widget1.objectName() == "le_ThresholdOne" or widget1.objectName() == "le_SegmentationThresholdOne":
                    if float(widget1.text()) >=1:
                        widget1.setText(str(int(widget1.text())))
                    else:
                        widget1.setText(str(float(widget1.text())))
            else:
                if widget1.objectName() == "le_ThresholdOne" or widget1.objectName() == "le_SegmentationThresholdOne":
                    if float(widget1.text()) >=1:
                        widget1.setText(str(int(widget1.text())))
                        if widget2.text() != "II" and float(widget2.text()) < 1:
                            widget2.setText(str(int(widget1.text())))
                    else:
                        widget1.setText(str(float(widget1.text())))
                        if widget2.text() != "II" and float(widget2.text())>=1:
                            widget2.setText(str(float(widget1.text())))
                    if widget2.text() == "II" or float(widget2.text())>float(widget1.text()):
                        if float(widget1.text()) >=1:
                            widget2.setText(str(int(widget1.text())))
                        else:
                            widget2.setText(str(float(widget1.text())))
                else:
                    if float(widget1.text()) >=1:
                        widget1.setText(str(int(widget1.text())))
                        if widget2.text() != "I" and float(widget2.text()) < 1:
                            widget2.setText(str(int(widget1.text())))
                    else:
                        widget1.setText(str(float(widget1.text())))
                        if widget2.text() != "I" and float(widget2.text())>=1:
                            widget2.setText(str(float(widget1.text())))
                    if widget2.text() == "I" or float(widget2.text())<float(widget1.text()):
                        if float(widget1.text()) >=1:
                            widget2.setText(str(int(widget1.text())))
                        else:
                            widget2.setText(str(float(widget1.text()))) 
        else:
            show_error_message(f"Please choose a value between {min_value} and {max_value} included.")
            widget1.setText(original_text)
            widget1.clearFocus()                   

def change_threshold_combobox(combobox, lineedit):
    '''Changes the display of a QLineEdit depending on the text in a QCombobox
    Parameters:
    combobox: the QCombobox
    lineedit: the QLineEdit'''
    if combobox.currentText() == "One threshold":
        lineedit.setText("II")
        lineedit.setEnabled(False)
    else:
        lineedit.setEnabled(True)

def slider_value_changed(window : Ui_MainWindow):
    '''Triggers the change of image display when the slider value changes
    Parameters:
    window : an instance of the app'''
    filename, slice_number = get_filename_slice_number(window)
    window.lb_SliceNumber.setText(f"{slice_number+1} / {len(window.appMod.stacks[filename])}")
    if window.appMod.included_images[filename][slice_number]:
        window.cb_IncludeImage.setCheckState(Qt.CheckState.Checked)
    else:
        window.cb_IncludeImage.setCheckState(Qt.CheckState.Unchecked)
    set_current_image_options(window,filename,slice_number)
    display_original_image(window,filename,slice_number,focus=window.focus)

def checkbox_state_changed(window : Ui_MainWindow):
    '''Updates the checkbox determining if the image will be included in the analysis and updates the image display
    Parameters:
    window : an instance of the app'''
    filename, slice_number = get_filename_slice_number(window)
    if window.cb_IncludeImage.isChecked():
        window.appMod.included_images[filename][slice_number] = True
    else:
        window.appMod.included_images[filename][slice_number] = False
        clear_results(window,filename,slice_number,"rtblcd")
    display_original_image(window,filename,slice_number)

def call_histogram_window(window : Ui_MainWindow):
    '''Shows the histogram window
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText() and window.cb_IncludeImage.isChecked():
            draw_histograms(window)
            window.histogram_window.show()
            window.histogram_window.activateWindow()
    else:
        show_error_message("Please choose an image to show its histogram.")

def scale_checked(window : Ui_MainWindow,message=True):
    '''Verifies if the required options are met to draw a scale on the images
    Parameters:
    window : an instance of the app
    message: if True, extra error messages will be display (only upon scale QCombobox checking)'''
    if window.cb_Scale.isChecked():
        if (window.le_PixelSize.text() == "" and window.options_window.le_StackInfoPixelSize.text() == "") or window.options_window.le_ScaleNumberPixels.text() == "":
            if message == True:
                show_error_message("Please choose a pixel size and a length in pixels for the scale.")
            window.cb_Scale.setChecked(False)
            window.cb_Scale.setCheckState(Qt.Unchecked)
        else:
            filename, slice_number = get_filename_slice_number(window)
            if int(window.options_window.le_ScaleNumberPixels.text()) > window.appMod.stacks[filename][slice_number].shape[1]:
                if message == True:
                    show_error_message("The length of the scale is greater than the image width. Please choose a smaller pixels number in the options.")
                window.cb_Scale.setChecked(False)
                window.cb_Scale.setCheckState(Qt.Unchecked)
            else:
                display_original_image(window,filename,slice_number,focus=window.focus)
    else:
        if window.combob_FileName.currentText():
            filename, slice_number = get_filename_slice_number(window)
            display_original_image(window,filename,slice_number,focus=window.focus)

def combobox_changed(window : Ui_MainWindow):
    '''Updates the image display on the first image of the new stack when the image file changes
    Parameters:
    window : an instance of the app'''
    filename = window.combob_FileName.currentText()
    update_image_slider_range(window,filename)
    set_current_image_options(window,filename,0)
    if window.appMod.included_images[filename][0]:
        window.cb_IncludeImage.setCheckState(Qt.CheckState.Checked)
    else:
        window.cb_IncludeImage.setCheckState(Qt.CheckState.Unchecked)
    display_original_image(window,filename,0,focus=window.focus)
    restore_images_original_size(window)

def highlight_groupbox(window : Ui_MainWindow, option):
    '''Highlight the tools being used
    Parameters:
    window : an instance of the app
    option: a string with the name of the tool to be highlighted'''
    window.focus = option
    for child in window.frame.findChildren(QGroupBox):
        child.setStyleSheet("")
    if window.focus == "illumination":
        window.gb_Illumination.setStyleSheet("background-color:rgb(85,170,255);")
        hide_text_layout_content(window,1)
        hide_text_layout_content(window,2)
    elif window.focus == "segmentation":
        window.gb_Segmentation.setStyleSheet("background-color:rgb(85,170,255);")
        hide_text_layout_content(window,1)
        hide_text_layout_content(window,2)
    elif window.focus == "labeling":
        window.gb_Labeling.setStyleSheet("background-color:rgb(85,170,255);")
        hide_text_layout_content(window,1)
        hide_text_layout_content(window,2)
    elif window.focus == "contours":
        window.gb_Contours.setStyleSheet("background-color:rgb(85,170,255);")
        hide_text_layout_content(window,1)
    elif window.focus == "density":
        window.gb_Density.setStyleSheet("background-color:rgb(85,170,255);")
        hide_text_layout_content(window,2)
    elif window.focus == "results":
        window.gb_Results.setStyleSheet("background-color:rgb(85,170,255);")
        hide_text_layout_content(window,1)
        hide_text_layout_content(window,2)

def set_current_image_options(window : Ui_MainWindow,filename,slice_number):
    '''Displays the chosen parameters for the processing of the current image
    Parameters:
    window : an instance of the app
    filename: name of the image file
    slice_number : index of the image in the file'''
    appMod = window.appMod
    ensure_deep_learning_defaults(appMod)
    sync_deep_learning_controls(window)
    if appMod.corrected_images[filename][slice_number] is not None:
        window.le_RollingBallRadius.setText(str(appMod.rolling_ball_param[filename][slice_number]))
    else:
        window.le_RollingBallRadius.clear()
    if appMod.first_threshold[filename][slice_number] is not None:
        window.le_ThresholdOne.setText(str(appMod.first_threshold[filename][slice_number]))
    else:
        window.le_ThresholdOne.blockSignals(True)
        window.le_ThresholdOne.setText("I")
        window.le_ThresholdOne.blockSignals(False)
    if appMod.second_threshold[filename][slice_number] is not None:
        window.le_ThresholdTwo.setText(str(appMod.second_threshold[filename][slice_number]))
    else:
        window.le_ThresholdTwo.blockSignals(True)
        window.le_ThresholdTwo.setText("II")
        window.le_ThresholdTwo.blockSignals(False)
    if appMod.threshold_algo[filename][slice_number] is not None and appMod.threshold_algo[filename][slice_number] == "Two thresholds":
        window.combob_Threshold.setCurrentIndex(1)
        window.le_ThresholdTwo.setDisabled(False)
    else:
        window.combob_Threshold.setCurrentIndex(0)
        window.le_ThresholdTwo.setDisabled(True)
    if appMod.blobs_detection_algo[filename][slice_number] is not None:
        blobs_algo = return_blobs_algorithms()
        index = blobs_algo.index(appMod.blobs_detection_algo[filename][slice_number])
        window.combob_BlobsDetection.setCurrentIndex(index)
        window.le_BlobsDetectionMinimumRadius.setText(str(appMod.blobs_radius[filename][slice_number][0]))
        window.le_BlobsDetectionMaximumRadius.setText(str(appMod.blobs_radius[filename][slice_number][1]))
    else:
        window.combob_BlobsDetection.setCurrentIndex(0)
        window.le_BlobsDetectionMinimumRadius.blockSignals(True)
        window.le_BlobsDetectionMinimumRadius.setText("min")
        window.le_BlobsDetectionMinimumRadius.blockSignals(False)
        window.le_BlobsDetectionMaximumRadius.blockSignals(True)
        window.le_BlobsDetectionMaximumRadius.setText("max")
        window.le_BlobsDetectionMaximumRadius.blockSignals(False)
    if appMod.labeling_sieve_size[filename][slice_number] is not None:
        window.le_SieveSize.setText(str(appMod.labeling_sieve_size[filename][slice_number]))
        window.combob_LabelingOption.setCurrentText(appMod.labeling_option[filename][slice_number])
    else:
        window.le_SieveSize.clear()
    if appMod.contours_background[filename][slice_number] is not None:
        window.le_BackgroundThreshold.setText(str(appMod.contours_background[filename][slice_number][0]))
        window.le_ContoursMinSize.setText(appMod.contours_background[filename][slice_number][1])
        contouring_algo = return_contouring_algorithms()
        contouring_algo_index = contouring_algo.index(appMod.contours_algo[filename][slice_number])
        window.combob_Contours.setCurrentIndex(contouring_algo_index)
    else:
        window.combob_Contours.setCurrentIndex(0)
        window.le_BackgroundThreshold.clear()
    if appMod.density_map_kernel_size[filename][slice_number] is not None:
        window.le_DensityMapKernelSize.setText(str(appMod.density_map_kernel_size[filename][slice_number]))
    else:
        window.le_DensityMapKernelSize.clear()
    if appMod.density_target_layers[filename][slice_number] is not None:
        window.le_DensityTargetLayers.setText(str(appMod.density_target_layers[filename][slice_number]))
    else:
        window.le_DensityTargetLayers.clear()
    if appMod.stack_infos[filename][0] is not None:
        window.le_ZThickness.setText(str(appMod.stack_infos[filename][0]))
    else:
        window.le_ZThickness.clear()
    if appMod.stack_infos[filename][1] is not None:
        window.le_InterZ.setText(str(appMod.stack_infos[filename][1]))
    else:
        window.le_InterZ.clear()
    if appMod.stack_infos[filename][2] is not None:
        window.le_PixelSize.setText(str(appMod.stack_infos[filename][2]))
    else:
        window.le_PixelSize.clear()
    segmentation_method_changed(window, False)

def get_colobar_vmin_vmax(window : Ui_MainWindow,frame):
    ''' Determines the minimum and maximum values of density heatmaps when the shared colorbar is checked
    Parameters:
    window : an instance of the app
    frame : the frame in which to display the image (either 1 or 2)
    Returns:
    vmin : minimum value in the heatmap
    vmax : maximum value in the heatmap'''
    vmins = []
    vmaxs = []
    image_type = None
    if window.combob_DensityDisplay.currentText() == "Percentage":
        if frame == 1:
            image_type = window.appMod.density_map_heatmap
        else:
            image_type = window.appMod.density_target_heatmap
    elif window.combob_DensityDisplay.currentText() == "Count":
        if frame == 1:
            image_type = window.appMod.density_map_centroid_heatmap
        else:
            image_type = window.appMod.density_target_centroid_heatmap
    elif window.combob_DensityDisplay.currentText() == "Count per 10k pixels":
        if frame == 1:
            image_type = window.appMod.density_map_count_per_10k_pixels_heatmap
        else:
            image_type = window.appMod.density_target_count_per_10k_pixels_heatmap
    elif window.combob_DensityDisplay.currentText() == "Mean size":
        if frame == 1:
            image_type = window.appMod.density_map_size
        else:
            image_type = window.appMod.density_target_size
    for images in image_type.values():
        for image in images:
            if image is not None:
                vmins.append(np.min(image))
                vmaxs.append(np.max(image))
    return min(vmins),max(vmaxs)
    
def display_secondary_image(frame, window : Ui_MainWindow, image = None, focus = None, title = None):
    '''Displays the secondary images resulting from the processing of the original image
    Parameters:
    frame : the frame in which to display the image (either 1 or 2)
    window : an instance of the app
    image : the image to be displayed
    focus : the tool being used
    title : the title of the image'''
    window.setCursor(QCursor(Qt.WaitCursor))
    appMod=window.appMod
    if (image is None and focus is None) or not window.cb_IncludeImage.isChecked():
        if frame == 1:
            window.wi_Image1Text.setFixedWidth(int(window.size().width()/3))
            window.wi_Image1Text.show()
            hide_text_layout_content(window,1)
            empty_layout(window.layout_Image1)
            window.wi_Image1Canvas.setFixedWidth(int(window.size().width()/3))
            window.wi_Image1Canvas.show()
        else:
            window.wi_Image2Text.setFixedWidth(int(window.size().width()/3))
            window.wi_Image2Text.show()
            hide_text_layout_content(window,2)
            empty_layout(window.layout_Image2)
            window.wi_Image2Canvas.setFixedWidth(int(window.size().width()/3))
            window.wi_Image2Canvas.show()
    elif window.cb_IncludeImage.isChecked() and image is not None:
        existingCanvas = window.wi_OriginalImage.findChildren(MplCanvas)
        if len(existingCanvas)>0:
            current_xlim = existingCanvas[0].axes.get_xlim()
            current_ylim = existingCanvas[0].axes.get_ylim()
        px = 1/plt.rcParams['figure.dpi']
        canvas = MplCanvas(window,image.shape[1]*px,image.shape[0]*px,100)
        toolbar = CustomToolbar(canvas, window)
        toolbar.font_size = 6
        canvas.fig.set_frameon(False)
        canvas.axes.set_axis_off()
        if focus == "contours" and frame == 2:
            filename,slice_number = get_filename_slice_number(window)
            centroid_y,centroid_x = appMod.contours_centroids[filename][slice_number]
            centroid_y=int(centroid_y)
            centroid_x=int(centroid_x)
            canvas.axes.plot([centroid_x, centroid_x],[int(max(0,centroid_y-15)), int(min(image.shape[0]-1,centroid_y+15))], color='red', linewidth=2)
            canvas.axes.plot([int(max(0,centroid_x-15)), int(min(image.shape[1]-1,centroid_x+15))],[centroid_y, centroid_y],  color='red', linewidth=2)
            if np.sum(image == 0) == 0:
                image[0,0]=0
            window.le_CentroidX.setText(str(centroid_x))
            window.le_CentroidY.setText(str(centroid_y))
            window.cb_MainSlice.stateChanged.disconnect()
            if appMod.contours_main_slice[filename][slice_number] is True:
                window.cb_MainSlice.setChecked(True)
                window.cb_MainSlice.setEnabled(False)
            else:
                window.cb_MainSlice.setChecked(False)
                window.cb_MainSlice.setEnabled(True)
            window.cb_MainSlice.stateChanged.connect(lambda : change_main_slice(window))
            show_text_layout_content(window,2)
        if focus == "density":
            filename,slice_number = get_filename_slice_number(window)
            if window.cb_SharedColorBar.isChecked():
                vmin,vmax = get_colobar_vmin_vmax(window,frame)
                heatmap = canvas.axes.imshow(image, cmap=window.combob_cmap.currentText(), interpolation='nearest', vmin=vmin, vmax=vmax)
            else:    
                heatmap = canvas.axes.imshow(image, cmap=window.combob_cmap.currentText(), interpolation='nearest')
            plt.colorbar(heatmap)
            contoured_image = appMod.contours_mask[filename][slice_number]
            if frame == 1:
                min_m,max_m,mean_m,median_m = min_max_mean_median_density(image,contoured_image)
                window.lb_MapStats.setText(f"Convoluted\nmean={mean_m:.1f}/median={median_m:.1f}\nmin={min_m:.1f}/max={max_m:.1f}")
                show_text_layout_content(window,1)
            if frame == 2:
                min_t,max_t,mean_t,median_t = min_max_mean_median_density(image,contoured_image)
                window.lb_TargetStats.setText(f"Target\nmean={mean_t:.1f}/median={median_t:.1f}\nmin={min_t:.1f}/max={max_t:.1f}")
        else:
            canvas.axes.imshow(image, cmap='gray')
        label = QLabel()
        if title:
            label.setText(title)
            label.setMaximumHeight(20)
            label.setAlignment(Qt.AlignCenter)
        if window.cb_Scale.isChecked() and window.cb_IncludeImage.isChecked():
            if len(image.shape) == 2:
                image = np.stack((image,image,image),axis = -1)
            position = window.options_window.combob_ScalePosition.currentText()
            if window.le_PixelSize.text() != "":
                pixel_size = float(window.le_PixelSize.text())
            else:
                pixel_size = float(window.options_window.le_StackInfoPixelSize.text())
            scale_length = float(window.options_window.le_ScaleNumberPixels.text())
            unit = window.options_window.le_ScaleUnit.text()
            color=window.options_window.combob_ScaleColor.currentText()
            if "East" in position:
                x_begin = image.shape[1] - scale_length - 20
            else:
                x_begin = 20
            if "South" in position:
                y_begin = image.shape[0] - 20
            else:
                y_begin = 40
            text = f"{int(scale_length*pixel_size)} {unit}"
            canvas.axes.plot([x_begin, x_begin + scale_length], [y_begin,y_begin], linewidth=3, color=color)
            canvas.axes.text(int(x_begin+scale_length/2), y_begin-20,text,color=color,va='center', ha='center')
        # canvas.fig.tight_layout()
        if frame == 1:
            layout = window.layout_Image1
        else:
            layout = window.layout_Image2
        empty_layout(layout)
        layout.addWidget(label)
        layout.addWidget(canvas)
        layout.addWidget(toolbar)
        if focus == "density":
            canvas.fig.subplots_adjust(0, 0.01, 1, 0.99, 0, 0)
        else:
            canvas.fig.subplots_adjust(0, 0, 1, 1, 0, 0)
        if frame == 1:
            window.wi_Image1Canvas.setFixedWidth(int(window.size().width()/3))
            window.wi_Image1Canvas.show()
            window.frame_3.show()
            if len(existingCanvas)>0:
                canvas.axes.set_xlim(current_xlim)
                canvas.axes.set_ylim(current_ylim)
                canvas.draw_idle()        
        else:
            window.wi_Image2Canvas.setFixedWidth(int(window.size().width()/3))
            window.wi_Image2Canvas.show()
            window.frame_3.show()
            if len(existingCanvas)>0:
                canvas.axes.set_xlim(current_xlim)
                canvas.axes.set_ylim(current_ylim)
                canvas.draw_idle()  
    elif window.cb_IncludeImage.isChecked() and focus is not None:
        filename, slice_number = get_filename_slice_number(window)
        if focus == "illumination" and appMod.rolling_ball_param[filename][slice_number] is not None:
            if frame == 1:
                display_secondary_image(1,window,  image = appMod.corrected_images[filename][slice_number], focus = "illumination",title="Corrected image")
            if frame == 2:
                display_secondary_image(2,window,  image = appMod.rolling_ball_background[filename][slice_number], focus = "illumination",title="Background")
        elif focus == "segmentation" and appMod.thresholded_images[filename][slice_number] is not None:
            if frame == 1:
                display_secondary_image(1,window, image = appMod.thresholded_images[filename][slice_number], focus = "segmentation",title="Thresholded image")
            if frame == 2:
                if appMod.blobs_thresholded_images[filename][slice_number] is not None:
                    display_secondary_image(2,window, image = appMod.blobs_thresholded_images[filename][slice_number],title="Blobs thresholded image")
                else:
                    display_secondary_image(2,window)
        elif focus == "labeling" and appMod.labeling_images_with_labels[filename][slice_number] is not None:
            if frame == 1:
                image = appMod.labeling_images_conserved_blobs[filename][slice_number]
                if appMod.blobs_thresholded_images[filename][slice_number] is not None:
                    title = "Blobs thresholded image : conserved blobs"
                else:
                    title = "Thresholded image : conserved blobs"
                display_secondary_image(1,window,image,title = title)
            if frame == 2:
                labels = appMod.labeling_labels[filename][slice_number]
                if labels != []:
                    count = np.max(labels)
                    mean, median = appMod.labeling_images_with_labels[filename][slice_number][1],appMod.labeling_images_with_labels[filename][slice_number][2]
                else:
                    count,mean,median = 0,0,0
                display_secondary_image(2,window,appMod.labeling_images_with_labels[filename][slice_number][0],title = f"Count: {count}, mean size: {mean}, median: {median}")
        elif focus == "contours" and appMod.contours_mask[filename][slice_number] is not None:
            if frame == 1:
                if appMod.labeling_coordinates[filename][slice_number] is not None:
                    image = dots_to_binary(appMod.stacks[filename][slice_number],appMod.labeling_coordinates[filename][slice_number])
                    title = "Conserved blobs after labeling"
                else: 
                    if appMod.blobs_thresholded_images[filename][slice_number] is not None:
                        image = appMod.blobs_thresholded_images[filename][slice_number]
                        title = "Blobs thresholded image"
                    else:
                        image = appMod.thresholded_images[filename][slice_number]
                        title = "Thresholded image"
                display_secondary_image(1,window,image,title = title)
            if frame == 2:
                display_secondary_image(2,window,appMod.contours_mask[filename][slice_number],focus="contours",title = "Contoured image")
        elif focus == "density" and appMod.density_map_heatmap[filename][slice_number] is not None:
            if window.combob_DensityDisplay.currentText() == "Percentage":
                if frame == 1:
                    display_secondary_image(1,window,appMod.density_map_heatmap[filename][slice_number],focus="density",title="Convoluted density heatmap (percentage)")
                if frame == 2:
                    display_secondary_image(2,window,appMod.density_target_heatmap[filename][slice_number],focus = "density", title = "Target density heatmap (percentage)")
            elif window.combob_DensityDisplay.currentText() == "Count":
                if frame == 1:
                    display_secondary_image(1,window,appMod.density_map_centroid_heatmap[filename][slice_number],focus="density",title="Convoluted density heatmap (Count)")
                if frame == 2:
                    display_secondary_image(2,window,appMod.density_target_centroid_heatmap [filename][slice_number],focus = "density", title = "Target density heatmap (Count)")
            elif window.combob_DensityDisplay.currentText() == "Count per 10k pixels":
                if frame == 1:
                    display_secondary_image(1,window,appMod.density_map_count_per_10k_pixels_heatmap[filename][slice_number],focus="density",title="Convoluted density heatmap (Count per 10k pixels)")
                if frame == 2:
                    display_secondary_image(2,window,appMod.density_target_count_per_10k_pixels_heatmap[filename][slice_number],focus = "density", title = "Target density heatmap (Count per 10k pixels)")       
            elif window.combob_DensityDisplay.currentText() == "Mean size":
                if frame == 1:
                    display_secondary_image(1,window,appMod.density_map_size[filename][slice_number],focus="density",title="Convoluted density heatmap (Size)")
                if frame == 2:
                    display_secondary_image(2,window,appMod.density_target_size[filename][slice_number],focus = "density", title = "Target density heatmap (Size)")        
        else:
            if frame == 1:
                window.wi_Image1Text.setFixedWidth(int(window.size().width()/3))
                window.wi_Image1Text.show()
                hide_text_layout_content(window,1)
                empty_layout(window.layout_Image1)
                window.wi_Image1Canvas.setFixedWidth(int(window.size().width()/3))
                window.wi_Image1Canvas.show()
            else:
                window.wi_Image2Text.setFixedWidth(int(window.size().width()/3))
                window.wi_Image2Text.show()
                hide_text_layout_content(window,2)
                empty_layout(window.layout_Image2)
                window.wi_Image2Canvas.setFixedWidth(int(window.size().width()/3))
                window.wi_Image2Canvas.show()
    window.setCursor(QCursor(Qt.ArrowCursor))

def clear_results(window : Ui_MainWindow,filename,slice_number,results):
    '''Clears the chosen parameters and results
    Parameters:
    window : an instance of the app
    filename: name of the image file
    slice_number : index of the image in the file
    results : a string composed of the results to clear (r:rolling-ball,t:threshold,b:blobs,l:labeling,c:contours,d:density)'''
    appMod=window.appMod
    if "r" in results:
        appMod.corrected_images[filename][slice_number] = None
        appMod.rolling_ball_background[filename][slice_number] = None
        appMod.rolling_ball_param[filename][slice_number] = None
        appMod.results_count[filename] = None
        appMod.results_density[filename] = None
        appMod.results_distance[filename] = None
    if "t" in results:
        appMod.threshold_algo[filename][slice_number] = None
        appMod.first_threshold[filename][slice_number] = None
        appMod.second_threshold[filename][slice_number] = None
        appMod.thresholded_images[filename][slice_number] = None
        appMod.results_count[filename] = None
        appMod.results_density[filename] = None
        appMod.results_distance[filename] = None
    if "b" in results:
        appMod.blobs_detection_algo[filename][slice_number] = None
        appMod.blobs_radius[filename][slice_number] = None
        appMod.blobs_thresholded_images[filename][slice_number] = None
        appMod.results_count[filename] = None
        appMod.results_density[filename] = None
        appMod.results_distance[filename] = None
    if "l" in results:
        appMod.labeling_option[filename][slice_number] = None
        appMod.labeling_sieve_size[filename][slice_number] = None
        appMod.labeling_coordinates[filename][slice_number] = None
        appMod.labeling_labels[filename][slice_number] = None
        appMod.labeling_images_with_labels [filename][slice_number] = None
        appMod.labeling_images_conserved_blobs[filename][slice_number] = None
        appMod.results_count[filename] = None
        appMod.results_distance[filename] = None
    if "c" in results:
        appMod.contours_algo[filename][slice_number] = None
        appMod.contours_background[filename][slice_number] = None
        appMod.contours_mask[filename][slice_number] = None
        appMod.contours_centroids[filename][slice_number] = None
        appMod.results_density[filename] = None
        appMod.results_distance[filename] = None
        appMod.contours_main_slice[filename][slice_number] = False
    if "d" in results:
        appMod.density_target_layers[filename][slice_number] = None
        appMod.density_map_kernel_size[filename][slice_number] = None
        appMod.density_centroid_size[filename][slice_number] = None
        appMod.density_target_heatmap[filename][slice_number] = None
        appMod.density_map_heatmap[filename][slice_number] = None
        appMod.density_target_centroid_heatmap [filename][slice_number] = None
        appMod.density_map_centroid_heatmap[filename][slice_number] = None
        appMod.density_target_count_per_10k_pixels_heatmap[filename][slice_number] = None
        appMod.density_map_count_per_10k_pixels_heatmap[filename][slice_number] = None
        appMod.density_target_size[filename][slice_number] = None
        appMod.density_map_size[filename][slice_number] = None
        appMod.results_density[filename] = None

def input_rolling_ball_radius(window :Ui_MainWindow):
    '''Controls the proper input of the rolling ball radius
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"illumination")
        if not window.le_RollingBallRadius.text().isdigit() or int(window.le_RollingBallRadius.text()) <=0:     
            if window.le_RollingBallRadius.text() != "":
                show_error_message("Please insert a positive integer as rolling ball radius.")
                window.le_RollingBallRadius.clear()         
    else:
        show_error_message("Please choose an image to process.")
        window.le_RollingBallRadius.clear() 
 
def rolling_ball_to_image(window : Ui_MainWindow,slice_number = None):
    '''Applies the rolling ball algorithm to the displayed image
    Parameters:
    window : an instance of the app
    slice_number : the number of the slice in the stack'''
    appMod=window.appMod
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"illumination")
        filename = window.combob_FileName.currentText()
        single_image = False
        if slice_number is None:
            slice_number = int(window.hs_SliceNumber.value())
            single_image = True
        if appMod.included_images[filename][slice_number]:
            if window.le_RollingBallRadius.text() == "":
                    clear_results(window,filename,slice_number,"rtblcd")
                    if single_image == True:
                        set_current_image_options(window,filename,slice_number)
                        display_original_image(window,filename,slice_number)
            elif window.le_RollingBallRadius.text().isdigit() and int(window.le_RollingBallRadius.text()) > 0:
                appMod.labeling_sieve_size[filename][slice_number] =  int(window.le_RollingBallRadius.text())
                raw_image = appMod.stacks[filename][slice_number]
                window.setCursor(QCursor(Qt.WaitCursor))
                background, corrected_image = rolling_ball(raw_image,int(window.le_RollingBallRadius.text()))
                window.setCursor(QCursor(Qt.ArrowCursor))
                appMod.corrected_images[filename][slice_number] = corrected_image
                appMod.rolling_ball_background[filename][slice_number] = background
                appMod.rolling_ball_param[filename][slice_number] = int(window.le_RollingBallRadius.text())
                clear_results(window,filename,slice_number,"tblcd")
                if single_image == True:
                    set_current_image_options(window,filename,slice_number)
                    display_original_image(window,filename,slice_number,focus = "illumination")  
            else:
                show_error_message("Please choose a positive integer")
        else:
            if single_image == True:
                show_error_message("Please choose an image to process.")
    else:
        show_error_message("Please choose an image to process.")
     
def rolling_ball_to_stack(window : Ui_MainWindow,display=True):
    '''Applies the rolling ball algorithm to all the checked images in the stack
    Parameters:
    window : an instance of the app
    display: if True, the images will be displayed'''
    if window.combob_FileName.currentText():
        filename, original_slice_number = get_filename_slice_number(window)
        if window.le_RollingBallRadius.text() == "" or (window.le_RollingBallRadius.text().isdigit() and int(window.le_RollingBallRadius.text()) > 0):
            for i in range(len(window.appMod.stacks[filename])):
                if window.appMod.included_images[filename][i]:
                    rolling_ball_to_image(window,i)
            if display == True:
                set_current_image_options(window,filename,original_slice_number)
                display_original_image(window,filename,original_slice_number,focus = "illumination")
        else:
            show_error_message("Please choose a positive integer or 0 as sieve size.")
    else:
        show_error_message("Please choose an image to process.") 
    
def view_illumination(window : Ui_MainWindow):
    '''Highlights the tool 'illumination' and updates the image display
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"illumination")
        filename, slice_number = get_filename_slice_number(window)
        display_original_image(window,filename,slice_number,focus="illumination")
        window.le_RollingBallRadius.setFocus()
    else:
        show_error_message("Please choose an image to process.")
      
def input_threshold_one(window : Ui_MainWindow, slice_number=None):
    '''Triggers several actions when the first threshold is set
    Parameters:
    window : an instance of the app
    appMod : an instance of the class AppModel containing the app variables
    slice_number : the index of the image in the stack'''
    appMod=window.appMod
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"segmentation")
        filename = window.combob_FileName.currentText()
        single_image = False
        if slice_number is None:
            slice_number = int(window.hs_SliceNumber.value())
            single_image = True
        if window.appMod.included_images[filename][slice_number]:
            if window.le_ThresholdOne.text() != "I":
                try:
                    float_var = float(window.le_ThresholdOne.text())
                    if float_var >=0 and float_var <=255:
                        if appMod.corrected_images[filename][slice_number] is not None:
                                image = appMod.corrected_images[filename][slice_number]
                        else:
                            image = appMod.stacks[filename][slice_number]
                        max_im = np.max(image)
                        if float_var < 1:
                            threshold_one = float_var * max_im
                            appMod.first_threshold[filename][slice_number] = float_var
                        else:
                            float_var = int(float_var)
                            threshold_one = float_var
                            appMod.first_threshold[filename][slice_number] = int(float_var)
                        if window.combob_Threshold.currentText() == "Two thresholds":
                            if window.le_ThresholdTwo.text() == "II" or float(window.le_ThresholdTwo.text()) > float_var:
                                window.le_ThresholdTwo.setText(str(float_var))
                                appMod.second_threshold[filename][slice_number] = float_var
                            if float(window.le_ThresholdTwo.text()) < 1:
                                if float_var >=1:
                                    window.le_ThresholdTwo.setText(str(float_var))
                                    threshold_two = threshold_one
                                    appMod.second_threshold[filename][slice_number] = threshold_two
                                else:
                                    threshold_two = float(window.le_ThresholdTwo.text()) * max_im
                                    appMod.second_threshold[filename][slice_number] = float(window.le_ThresholdTwo.text())
                            else:
                                threshold_two = int(window.le_ThresholdTwo.text())
                                appMod.second_threshold[filename][slice_number] = threshold_two
                            window.setCursor(QCursor(Qt.WaitCursor))
                            mask = segmentation_two_thresholds(image,threshold_one,threshold_two)
                            appMod.threshold_algo[filename][slice_number] = "Two thresholds"
                            appMod.thresholded_images[filename][slice_number] = mask
                            window.setCursor(QCursor(Qt.ArrowCursor))
                        else:
                            mask = image >= threshold_one
                            appMod.threshold_algo[filename][slice_number] = "One threshold"
                            appMod.thresholded_images[filename][slice_number] = mask
                            appMod.second_threshold[filename][slice_number] = None
                        clear_results(window,filename,slice_number,"blcd")
                        if single_image == True:
                            set_current_image_options(window,filename,slice_number)
                            display_original_image(window,filename,slice_number,focus = "segmentation")
                        
                    else:
                        raise ValueError("Please choose a number between 0 and 255 included as first threshold.")
                except ValueError as e:
                    show_error_message(f"Please choose a number between 0 and 255 included as first threshold.\n{e}")
                    window.le_ThresholdOne.blockSignals(True)
                    window.le_ThresholdOne.setText("I")
                    window.le_ThresholdOne.blockSignals(False)
    else:
        show_error_message("Please choose an image to process.")

def input_threshold_two(window : Ui_MainWindow):
    '''Triggers several actions when the second threshold is set
     Parameters:
    window : an instance of the app'''
    appMod=window.appMod
    if window.combob_FileName.currentText() and window.cb_IncludeImage.isChecked():
        highlight_groupbox(window,"segmentation")
        filename, slice_number = get_filename_slice_number(window)
        display_original_image(window,filename,slice_number)
        if window.le_ThresholdTwo.text() != "II":
            try:
                float_var = float(window.le_ThresholdTwo.text())
                if float_var >=0 and float_var <=255:
                    filename = window.combob_FileName.currentText()
                    slice_number = int(window.hs_SliceNumber.value())
                    if appMod.corrected_images[filename][slice_number] is not None:
                            image = appMod.corrected_images[filename][slice_number]
                    else:
                        image = appMod.stacks[filename][slice_number]
                    max_im = np.max(image)
                    if window.le_ThresholdOne.text() == "I" or float(window.le_ThresholdOne.text()) < float_var:
                        if float_var >= 1:
                            float_var = int(float_var)
                        window.le_ThresholdOne.setText(str(float_var))
                    if float_var < 1:
                        threshold_two = float_var * max_im
                        appMod.second_threshold[filename][slice_number] = float_var
                        if float(window.le_ThresholdOne.text()) >= 1:
                            window.le_ThresholdOne.setText(str(float_var))
                    else:
                        threshold_two = float_var
                        appMod.second_threshold[filename][slice_number] = int(float_var)
                    if float(window.le_ThresholdOne.text()) < 1:
                        threshold_one = float(window.le_ThresholdTwo.text()) * max_im
                        appMod.first_threshold[filename][slice_number] = float(window.le_ThresholdTwo.text())
                    else:
                        threshold_one = int(window.le_ThresholdOne.text())
                        appMod.first_threshold[filename][slice_number] = threshold_one
                    window.setCursor(QCursor(Qt.WaitCursor))
                    mask = segmentation_two_thresholds(image,threshold_one,threshold_two)
                    window.setCursor(QCursor(Qt.ArrowCursor))
                    appMod.thresholded_images[filename][slice_number] = mask
                    appMod.blobs_detection_algo[filename][slice_number] = None
                    appMod.blobs_radius[filename][slice_number] = None
                    appMod.blobs_thresholded_images[filename][slice_number] = None
                    display_original_image(window,filename,slice_number,focus = "segmentation")
                    window.combob_BlobsDetection.setCurrentIndex(0)
                    window.le_BlobsDetectionMinimumRadius.setText("min")
                    window.le_BlobsDetectionMaximumRadius.setText("max")
                else:
                    raise ValueError("Please choose a number between 0 and 255 included as second threshold.")
            except ValueError as e:
                show_error_message(f"Please choose a number between 0 and 255 included as second threshold.\n{e}")
                window.le_ThresholdTwo.blockSignals(True)
                window.le_ThresholdTwo.setText("II")
                window.le_ThresholdTwo.blockSignals(False) 
    else:
        show_error_message("Please choose an image to process.")
        window.le_ThresholdTwo.blockSignals(True)
        window.le_ThresholdTwo.setText("II")
        window.le_ThresholdTwo.blockSignals(False)

def threshold_option_changed(window : Ui_MainWindow):
    '''Triggers several action when the combobox for threshold option is activated
    Parameters:
    window : an instance of the app'''
    highlight_groupbox(window,"segmentation")
    if window.combob_Threshold.currentText() == "One threshold":
        window.le_ThresholdTwo.blockSignals(True)
        window.le_ThresholdTwo.setText("II")
        window.le_ThresholdTwo.blockSignals(False)
        window.le_ThresholdTwo.setDisabled(True)
        if window.le_ThresholdOne.text() != "I":
            input_threshold_one(window)
    else:
        window.le_ThresholdTwo.setDisabled(False)
        if window.le_ThresholdOne.text() != "I" and window.le_ThresholdTwo.text() != "II":
            input_threshold_two(window)

def segmentation_method_changed(window : Ui_MainWindow, do_highlight=True):
    '''Triggers actions when segmentation method changes'''
    if not hasattr(window, "combob_SegmentationMethod"):
        return
    ensure_deep_learning_defaults(window.appMod)
    if do_highlight:
        highlight_groupbox(window,"segmentation")
    method = window.combob_SegmentationMethod.currentText()
    window.appMod.segmentation_method = method
    classical = method == "Classical"
    classical_widgets = [
        window.combob_Threshold,
        window.le_ThresholdOne,
        window.le_ThresholdTwo,
        window.combob_BlobsDetection,
        window.le_BlobsDetectionMinimumRadius,
        window.le_BlobsDetectionMaximumRadius,
    ]
    dl_widgets = [
        window.le_DLCheckpointPath,
        window.le_DLProbThresh,
        window.le_DLBackgroundRadius,
    ]
    for widget in classical_widgets:
        widget.setVisible(classical)
        widget.setEnabled(classical)
    for widget in dl_widgets:
        widget.setVisible(not classical)
        widget.setEnabled(not classical)

def input_dl_checkpoint_path(window : Ui_MainWindow):
    '''Stores checkpoint path for deep learning segmentation'''
    window.appMod.dl_checkpoint_path = window.le_DLCheckpointPath.text().strip()

def input_dl_prob_thresh(window : Ui_MainWindow):
    '''Validates deep learning probability threshold'''
    if window.le_DLProbThresh.text() == "":
        return
    try:
        threshold = float(window.le_DLProbThresh.text())
        if threshold < 0 or threshold > 1:
            raise ValueError
        window.appMod.dl_prob_thresh = threshold
    except ValueError:
        show_error_message("Please insert a number between 0 and 1 for deep learning probability threshold.")
        window.le_DLProbThresh.setText(str(window.appMod.dl_prob_thresh))

def input_dl_background_radius(window : Ui_MainWindow):
    '''Validates deep learning rolling ball radius'''
    if window.le_DLBackgroundRadius.text() == "":
        return
    try:
        radius = int(window.le_DLBackgroundRadius.text())
        if radius <= 0:
            raise ValueError
        window.appMod.dl_background_radius = radius
    except ValueError:
        show_error_message("Please insert a positive integer for deep learning rolling ball radius.")
        window.le_DLBackgroundRadius.setText(str(window.appMod.dl_background_radius))

def dl_device_changed(window : Ui_MainWindow):
    '''Stores selected deep learning device'''
    window.appMod.dl_device = window.combob_DLDevice.currentData()

def combobox_blobs_changed(window : Ui_MainWindow):
    '''Highlights the box 'segmentation' when the combobox for blobs detection is activated
    Parameters:
    window : an instance of the app'''
    highlight_groupbox(window,"segmentation")
     
def set_blobs_minimum_radius(window : Ui_MainWindow):
    '''Triggers several actions when a value for minimum radius of blob detection is set
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText() and window.cb_IncludeImage.isChecked():
        highlight_groupbox(window,"segmentation")
        try:
            if window.le_BlobsDetectionMinimumRadius.text() != "min":
                if not window.le_BlobsDetectionMinimumRadius.text().isdigit() or int(window.le_BlobsDetectionMinimumRadius.text()) <0:
                    raise ValueError("The value must be a positive integer")
                if window.le_BlobsDetectionMaximumRadius.text() != "max" and int(window.le_BlobsDetectionMaximumRadius.text()) < int(window.le_BlobsDetectionMinimumRadius.text()):
                    raise ValueError("Minimum radius value must be less than the maximum radius value.")
        except ValueError as e:
            show_error_message(str(e))
            window.le_BlobsDetectionMinimumRadius.blockSignals(True)
            window.le_BlobsDetectionMinimumRadius.setText("min")
            window.le_BlobsDetectionMinimumRadius.blockSignals(False)
    else:
        show_error_message("Please choose an image to process")
        window.le_BlobsDetectionMinimumRadius.blockSignals(True)
        window.le_BlobsDetectionMinimumRadius.setText("min")
        window.le_BlobsDetectionMinimumRadius.blockSignals(False)

def set_blobs_maximum_radius(window : Ui_MainWindow):
    '''Triggers several actions when a value for maximum radius of blob detection is set
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText() and window.cb_IncludeImage.isChecked():
        highlight_groupbox(window,"segmentation")
        try:
            if window.le_BlobsDetectionMaximumRadius.text() != "max":
                if not window.le_BlobsDetectionMaximumRadius.text().isdigit() or int(window.le_BlobsDetectionMaximumRadius.text()) < 0:
                    raise ValueError("The value must be a positive integer")
                if window.le_BlobsDetectionMinimumRadius.text() != "min" and int(window.le_BlobsDetectionMaximumRadius.text()) < int(window.le_BlobsDetectionMinimumRadius.text()):
                    raise ValueError("Maximum radius value must be greater than the minimum radius value.")
        except ValueError as e:
            show_error_message(str(e))
            window.le_BlobsDetectionMaximumRadius.blockSignals(True)
            window.le_BlobsDetectionMaximumRadius.setText("max")
            window.le_BlobsDetectionMaximumRadius.blockSignals(False)
    else:
        show_error_message("Please choose an image to process")
        window.le_BlobsDetectionMaximumRadius.blockSignals(True)
        window.le_BlobsDetectionMaximumRadius.setText("max")
        window.le_BlobsDetectionMaximumRadius.blockSignals(False)

def segmentation_to_image(window : Ui_MainWindow, slice_number=None):
    '''Applies the segmentation with the chosen options to an image
    Parameters:
    window: an instance of the app
    slice_number: the index of the image in the stack'''
    appMod=window.appMod
    ensure_deep_learning_defaults(appMod)
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"segmentation")
        filename = window.combob_FileName.currentText()
        single_image = False
        if slice_number is None:
            slice_number = int(window.hs_SliceNumber.value())
            single_image = True
        if appMod.included_images[filename][slice_number]:
            if appMod.segmentation_method == "Deep learning (UNet-DC)":
                window.setCursor(QCursor(Qt.WaitCursor))
                try:
                    image = get_original_frame_for_dl(appMod, filename, slice_number)
                    append_run_log(
                        "DL inference start "
                        f"file='{filename}' slice={slice_number} "
                        f"shape={np.asarray(image).shape} "
                        f"checkpoint='{appMod.dl_checkpoint_path}' "
                        f"prob_thresh={appMod.dl_prob_thresh} "
                        f"background_radius={appMod.dl_background_radius} "
                        f"device='{appMod.dl_device}'"
                    )
                    mask = segmentation_deep_learning(
                        image=image,
                        checkpoint_path=appMod.dl_checkpoint_path,
                        prob_thresh=appMod.dl_prob_thresh,
                        background_radius=appMod.dl_background_radius,
                        device=appMod.dl_device,
                    )
                    appMod.threshold_algo[filename][slice_number] = "Deep learning (UNet-DC)"
                    appMod.first_threshold[filename][slice_number] = None
                    appMod.second_threshold[filename][slice_number] = None
                    appMod.thresholded_images[filename][slice_number] = mask
                    appMod.blobs_detection_algo[filename][slice_number] = None
                    appMod.blobs_radius[filename][slice_number] = None
                    appMod.blobs_thresholded_images[filename][slice_number] = None
                    export_dl_debug_mask(filename, slice_number, mask)
                    append_run_log(
                        f"DL inference done file='{filename}' slice={slice_number} "
                        f"mask_true_pixels={int(np.count_nonzero(mask))}"
                    )
                    clear_results(window,filename,slice_number,"lcd")
                    if single_image == True:
                        set_current_image_options(window,filename,slice_number)
                        display_original_image(window,filename,slice_number,focus = "segmentation")
                except ValueError as e:
                    append_run_log(
                        f"DL inference error file='{filename}' slice={slice_number} error='{e}'"
                    )
                    show_error_message(str(e))
                finally:
                    window.setCursor(QCursor(Qt.ArrowCursor))
                return
            if window.le_ThresholdOne.text() != "I":
                if window.combob_BlobsDetection.currentIndex() == 0:
                    input_threshold_one(window,slice_number)
                elif window.le_BlobsDetectionMinimumRadius.text() != "min" and window.le_BlobsDetectionMaximumRadius.text() != "max":
                    algo_index = int(window.combob_BlobsDetection.currentIndex())
                    min_radius = int(window.le_BlobsDetectionMinimumRadius.text())
                    max_radius = int(window.le_BlobsDetectionMaximumRadius.text())
                    input_threshold_one(window,slice_number)
                    image = appMod.thresholded_images[filename][slice_number]
                    window.setCursor(QCursor(Qt.WaitCursor))
                    blobs_list = blobs_detection(image,algo_index,min_radius,max_radius)
                    bl_mask = blobs_mask(image,blobs_list)
                    window.setCursor(QCursor(Qt.ArrowCursor))
                    appMod.blobs_detection_algo[filename][slice_number] = window.combob_BlobsDetection.itemText(algo_index)
                    appMod.blobs_radius[filename][slice_number] = (min_radius,max_radius)
                    blobs_thres_im = image & bl_mask
                    appMod.blobs_thresholded_images[filename][slice_number] = blobs_thres_im
                    if single_image == True:
                        set_current_image_options(window,filename,slice_number)
                        display_original_image(window,filename,slice_number,focus = "segmentation")                        
                else:
                    show_error_message("Please choose a minimum and maximum radius for blobs detection.")
            else:
                if single_image == True:
                    show_error_message("Please segment image with a thresholding option first.")
                else:
                    show_error_message(f"Please segment image {filename} slice {slice_number+1} with a thresholding option first.")
        else:
            if single_image == True:
                show_error_message("Please choose an image to process.")
    else:
        show_error_message("Please choose an image to process.")

def segmentation_to_stack(window : Ui_MainWindow, display=True):
    '''Applies the segmentation with the chosen options to all the images in the stack
     Parameters:
    window : an instance of the app
    display: if True, the images will be displayed'''
    if window.combob_FileName.currentText():
        filename, original_slice_number = get_filename_slice_number(window)
        for i in range(len(window.appMod.stacks[filename])):
            if window.appMod.included_images[filename][i]:
                segmentation_to_image(window,i)
        if display == True:
            set_current_image_options(window,filename,original_slice_number)
            display_original_image(window,filename,original_slice_number,focus = "segmentation")
    else:
        show_error_message("Please choose an image to process.")

def view_segmentation(window : Ui_MainWindow):
    '''Highlights the tool 'segmentation' and updates the image display
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"segmentation")
        filename, slice_number = get_filename_slice_number(window)
        display_original_image(window,filename,slice_number,focus="segmentation")
        window.combob_Threshold.setFocus()
    else:
        show_error_message("Please choose an image to process.")

def input_sieve_size(window :Ui_MainWindow):
    '''Controls the input of the sieve size which must be a positive integer or zero
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"labeling")
        if not window.le_SieveSize.text().isdigit() or  int(window.le_SieveSize.text()) < 0:
                if window.le_SieveSize.text() != "":
                    show_error_message("Please insert a positive integer or zero.")
                    window.le_SieveSize.clear()         
    else:
        show_error_message("Please choose an image to process.")
        window.le_SieveSize.clear()

def apply_labeling_to_image(window :Ui_MainWindow, slice_number = None):
    '''Applies the labeling options to the current image
    Parameters:
    window : an instance of the app
    slice_number: the number of the slice in the stack'''
    appMod=window.appMod
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"labeling")
        filename = window.combob_FileName.currentText()
        single_image = False
        if slice_number is None:
            slice_number = int(window.hs_SliceNumber.value())
            single_image = True
        if appMod.included_images[filename][slice_number] == True:
            clear_results(window,filename,slice_number,"ld")
            if window.le_SieveSize.text() == "":
                if single_image == True:
                    set_current_image_options(window,filename,slice_number) 
            elif window.le_SieveSize.text().isdigit() and int(window.le_SieveSize.text()) >= 0:
                if appMod.included_images[filename][slice_number]:
                    if appMod.thresholded_images[filename][slice_number] is not None:
                        if appMod.blobs_thresholded_images[filename][slice_number] is not None:
                            image = appMod.blobs_thresholded_images[filename][slice_number]
                        else:
                            image = appMod.thresholded_images[filename][slice_number]
                        if int(window.le_SieveSize.text()) != appMod.labeling_sieve_size[filename][slice_number] or appMod.labeling_option[filename][slice_number] != window.combob_LabelingOption.currentText():
                            appMod.labeling_option[filename][slice_number] = window.combob_LabelingOption.currentText()
                            window.setCursor(QCursor(Qt.WaitCursor))
                            appMod.labeling_sieve_size[filename][slice_number] = int(window.le_SieveSize.text())
                            dots = binary_to_dots(image)
                            if dots != []:
                                if appMod.labeling_option[filename][slice_number] == window.combob_LabelingOption.itemText(1):
                                    dots, labels = watershed_custom(image,dots)
                                else:
                                    labels = labeling_custom(image,dots)
                                if window.le_SieveSize.text() != "0":
                                    dots,labels = sieve_labels(dots,labels,int(window.le_SieveSize.text()))  
                            else:
                                labels = []
                            appMod.labeling_sieve_size[filename][slice_number] = int(window.le_SieveSize.text())
                            appMod.labeling_coordinates[filename][slice_number] = dots if dots != [] else []
                            appMod.labeling_labels[filename][slice_number] = labels if labels != [] else []
                            image_8_bits = image.astype(np.uint8) * 255
                            image_with_conserved_blobs = np.stack((image_8_bits,image_8_bits,image_8_bits),axis = -1)
                            image_with_labels = np.stack((image_8_bits,image_8_bits,image_8_bits),axis = -1)
                            sizes=[]
                            if labels != []:
                                unique_labels = set(labels)
                                for label in unique_labels:
                                    random_color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
                                    cluster_points = np.array([point for point, l in zip(dots, labels) if l == label])
                                    sizes.append(labels.count(label))
                                    for y,x in cluster_points:
                                        image_with_conserved_blobs[y,x] = [0,255,0]
                                        image_with_labels[y,x] = random_color
                                mean_s, median_s, min_s, max_s = round(np.mean(sizes),2),round(np.median(sizes),2),round(np.min(sizes),2),round(np.max(sizes),2)
                            else:
                                mean_s, median_s, min_s, max_s= 0,0,0,0
                            # mean_s, median_s, min_s, max_s, sizes = mean_median_min_max_size(labels)
                            appMod.labeling_images_with_labels[filename][slice_number] = [image_with_labels,mean_s, median_s, min_s, max_s, sizes]
                            appMod.labeling_images_conserved_blobs[filename][slice_number] = image_with_conserved_blobs
                            if single_image == True:
                                set_current_image_options(window,filename,slice_number)
                                display_original_image(window,filename,slice_number,focus = "labeling")
                            window.setCursor(QCursor(Qt.ArrowCursor))    
                        else:
                            if single_image == True:
                                set_current_image_options(window,filename,slice_number)
                                display_original_image(window,filename,slice_number,focus = "labeling")
                    else:
                        if single_image == True:
                            show_error_message("Please segment image first.")
                        else:
                            show_error_message(f"Please segment image {filename} slice {slice_number+1} first.")
            else:
                show_error_message("Please choose a positive integer or 0.")
        else:
            if single_image == True:
                show_error_message("Please choose an image to process.")
    else:
        show_error_message("Please choose an image to process.")

def apply_labeling_to_stack(window :Ui_MainWindow, display=True):
    '''Applies the labeling with the chosen options to all the images in the stack
     Parameters:
    window : an instance of the app
    display: if True, the images will be displayed'''
    if window.combob_FileName.currentText():
        filename, original_slice_number = get_filename_slice_number(window)
        if window.le_SieveSize.text() == "" or (window.le_SieveSize.text().isdigit() and int(window.le_SieveSize.text()) >= 0):
            for i in range(len(window.appMod.stacks[filename])):
                if window.appMod.included_images[filename][i]:
                    apply_labeling_to_image(window,i)
            if display == True:
                set_current_image_options(window,filename,original_slice_number)
                display_original_image(window,filename,original_slice_number,focus = "labeling")
        else:
            show_error_message("Please choose a positive interger or 0 as sieve size.")
    else:
        show_error_message("Please choose an image to process.")

def view_labeling(window :Ui_MainWindow):
    '''Highlights the tool 'labeling' and updates the image display
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"labeling")
        filename, slice_number = get_filename_slice_number(window)
        display_original_image(window,filename,slice_number,focus="labeling")
        window.le_SieveSize.setFocus()
    else:
        show_error_message("Please choose an image to process.")

def input_background_threshold(window :Ui_MainWindow):
    '''Controls that the value of the threshold is correct
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"contours")
        if not window.le_BackgroundThreshold.text().isdigit() or int(window.le_BackgroundThreshold.text()) < 0:
            if window.le_BackgroundThreshold.text() != "":
                show_error_message("Please choose an integer between 0 and 255 included.")
                window.le_BackgroundThreshold.clear()
    else:
        show_error_message("Please choose an image to process.")
        window.le_BackgroundThreshold.clear()

def combobox_contours_changed(window :Ui_MainWindow):
    '''Triggers several actrions when the combox with the contouring option is activated
    Parameters:
    window : an instance of the app'''
    highlight_groupbox(window,"contours")
    if window.combob_FileName.currentText():
        filename, slice_number = get_filename_slice_number(window)
        if window.appMod.contours_algo[filename][slice_number] is not None:
            clear_results(window,filename,slice_number,"cd")
            display_original_image(window,filename,slice_number,focus="contours")
    else:
        show_error_message("Please choose an image to process.")

def determine_main_slice(appMod : AppModel, filename):
    '''Determines the slice with the largest contour in a stack
    Parameters:
    appMod: an instance of the class AppModel
    filename: the name of the file with the stack of images'''
    max_contours = 0
    main_slice_index = 0
    for i in range(len(appMod.stacks[filename])):
        if appMod.included_images[filename][i] and appMod.contours_mask[filename][i] is not None:
            sum_contours = np.sum(appMod.contours_mask[filename][i])
            if  sum_contours >= max_contours:
                appMod.contours_main_slice[filename][main_slice_index] = False
                appMod.contours_main_slice[filename][i] = True
                main_slice_index = i
                max_contours = sum_contours

def apply_contours_to_image(window :Ui_MainWindow, slice_number=None):
    '''Applies the chosen contouring algorithm to the image
    Parameters:
    window : an instance of the app
    slice_number: the index of the image in the stack'''
    appMod=window.appMod
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"contours")
        filename = window.combob_FileName.currentText()
        single_image = False
        if slice_number is None:
            slice_number = int(window.hs_SliceNumber.value())
            single_image = True
        if appMod.included_images[filename][slice_number]:
            if appMod.thresholded_images[filename][slice_number] is not None:
                if window.le_BackgroundThreshold.text() != "":
                    clear_results(window,filename,slice_number,"d")
                    appMod.results_density[filename] = None
                    algo_index = window.combob_Contours.currentIndex()
                    threshold_value = int(window.le_BackgroundThreshold.text())
                    if appMod.corrected_images[filename][slice_number] is not None:
                        image_to_contour = appMod.corrected_images[filename][slice_number]
                    else:
                        image_to_contour = appMod.stacks[filename][slice_number]
                    window.setCursor(QCursor(Qt.WaitCursor))
                    if algo_index == 0:
                        contour_mask = contour_scan(image_to_contour,threshold_value)
                    elif algo_index == 1:
                        contour_mask = contour_spreading_4(image_to_contour,threshold_value)
                    elif algo_index == 2:
                        contour_mask = contour_spreading_8(image_to_contour,threshold_value)
                    elif algo_index == 3:
                        contour_mask = contour_shrinking_box(image_to_contour,threshold_value)
                    else:
                        contour_mask = image_to_contour > threshold_value
                    if window.le_ContoursMinSize.text() not in ["","0"]:
                        contour_mask = remove_objects(contour_mask,int(window.le_ContoursMinSize.text()))
                    window.setCursor(QCursor(Qt.ArrowCursor))
                    contour_centroid_y_x = calculate_contours_centroid(contour_mask)
                    appMod.contours_centroids[filename][slice_number] = contour_centroid_y_x
                    appMod.contours_algo[filename][slice_number] = window.combob_Contours.currentText()
                    appMod.contours_background[filename][slice_number] = [threshold_value,window.le_ContoursMinSize.text()]
                    appMod.contours_mask[filename][slice_number] = contour_mask
                    if single_image == True:
                        determine_main_slice(appMod,filename)
                        set_current_image_options(window,filename,slice_number)
                        display_original_image(window,filename,slice_number,focus = "contours")                        
                else:
                    show_error_message("Please choose a background value.")
            else:
                if single_image == True:
                    show_error_message("Please segment image first.")
                else:
                    show_error_message(f"Please segment image {filename} slice {slice_number+1} first.")
    else:
        show_error_message("Please choose an image to process.")

def apply_contours_to_stack(window :Ui_MainWindow, display = True):
    '''Applies the chosen contouring algorithm to the current stack of images
    Parameters:
    window : an instance of the app
    display: if True, the images will be displayed'''
    if window.combob_FileName.currentText():
        filename, original_slice_number = get_filename_slice_number(window)
        if window.le_BackgroundThreshold.text() != "":
            for i in range(len(window.appMod.stacks[filename])):
                if window.appMod.included_images[filename][i]:
                    apply_contours_to_image(window,i)
            determine_main_slice(window.appMod,filename)
            if display == True:
                set_current_image_options(window,filename,original_slice_number)
                display_original_image(window,filename,original_slice_number,focus = "contours")
        else:
            show_error_message("Please choose a background threshold value.")
    else:
        show_error_message("Please choose an image to process.")

def view_contours(window :Ui_MainWindow):
    '''Highlights the tool 'contours' and updates the image display
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"contours")
        filename, slice_number = get_filename_slice_number(window)
        display_original_image(window,filename,slice_number,focus="contours")
        window.combob_Contours.setFocus()
    else:
        show_error_message("Please choose an image to process.")

def edit_centroid_x(window :Ui_MainWindow):
    '''Controls the input of the x coordinate for the centroid and draws the new location on the image
    Parameters:
    window : an instance of the app'''
    if window.focus == "contours":
        appMod=window.appMod
        filename,slice_number = get_filename_slice_number(window)
        image = appMod.contours_mask[filename][slice_number]
        if window.le_CentroidX.text().isdigit() and int(window.le_CentroidX.text()) >= 0 \
        and int(window.le_CentroidX.text()) < image.shape[1]:
            appMod.contours_centroids[filename][slice_number][1] = int(window.le_CentroidX.text())
            appMod.density_target_heatmap[filename][slice_number] = None
            appMod.density_target_layers[filename][slice_number] = None
            set_current_image_options(window,filename,slice_number)
            display_secondary_image(2,window,image,focus="contours",title="Contoured image")    
        else:
            show_error_message("Please enter an pixel value in the range of the x image shape")
            window.le_CentroidX.setText(str(appMod.contours_centroids[filename][slice_number][1]))

def edit_centroid_y(window :Ui_MainWindow):
    '''Controls the input of the y coordinate for the centroid and draws the new location on the image
    Parameters:
    window : an instance of the app'''
    if window.focus == "contours":
        appMod=window.appMod
        filename,slice_number = get_filename_slice_number(window)
        image = appMod.contours_mask[filename][slice_number]
        if window.le_CentroidY.text().isdigit() and int(window.le_CentroidY.text()) >= 0 \
        and int(window.le_CentroidY.text()) < image.shape[0]:
            appMod.contours_centroids[filename][slice_number][0] = int(window.le_CentroidY.text())
            appMod.density_target_heatmap[filename][slice_number] = None
            appMod.density_target_layers[filename][slice_number] = None
            set_current_image_options(window,filename,slice_number)
            display_secondary_image(2,window,image,focus="contours",title="Contoured image")    
        else:
            show_error_message("Please enter an pixel value in the range of the x image shape")
            window.le_CentroidY.setText(str(appMod.contours_centroids[filename][slice_number][0]))

def set_centroid_auto(window :Ui_MainWindow):
    '''Automatically computes the coordinates of the centroid of a contoured image and places it on the image
    Parameters:
    window : an instance of the app'''
    if window.focus == "contours":
        appMod=window.appMod
        filename,slice_number = get_filename_slice_number(window)
        image = appMod.contours_mask[filename][slice_number]
        centroid_y_x = calculate_contours_centroid(image)
        appMod.contours_centroids[filename][slice_number] = centroid_y_x
        appMod.density_target_heatmap[filename][slice_number] = None
        appMod.density_target_layers[filename][slice_number] = None
        set_current_image_options(window,filename,slice_number)
        display_secondary_image(2,window,image,focus="contours",title="Contoured image")

def change_main_slice(window :Ui_MainWindow):
    '''Changes the check in the combobox when manually selecting a main slice
    Parameters:
    window : an instance of the app'''
    appMod=window.appMod
    filename,slice_number = get_filename_slice_number(window)
    length = len(appMod.stacks[filename])
    appMod.contours_main_slice[filename] = [False]*length
    appMod.contours_main_slice[filename][slice_number] = True
    appMod.results_distance[filename] = None
    display_secondary_image(2,window,focus = "contours")


def input_target_layers(window :Ui_MainWindow):
    '''Controls the input of the number of layers
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"density")
        if not window.le_DensityTargetLayers.text().isdigit() or int(window.le_DensityTargetLayers.text()) <=0:
            if window.le_DensityTargetLayers.text() != "":
                show_error_message("Please insert a positive integer.")
                window.le_DensityTargetLayers.clear()
    else:
        show_error_message("Please choose an image to process.")
        window.le_DensityTargetLayers.clear()

def input_kernel_size(window :Ui_MainWindow):
    '''Controls the input for the kernel size
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        filename,slice_number = get_filename_slice_number(window)
        if window.appMod.included_images[filename][slice_number] == True:
            image = window.appMod.stacks[filename][slice_number]
            highlight_groupbox(window,"density")
            if not window.le_DensityMapKernelSize.text().isdigit() or int(window.le_DensityMapKernelSize.text()) <3 \
            or int(window.le_DensityMapKernelSize.text()) %2 ==0 or int(window.le_DensityMapKernelSize.text()) >= min(image.shape[0],image.shape[1]):
                    if window.le_DensityMapKernelSize.text() != "":
                        show_error_message("Please insert a positive integer at least equal to 3 and smaller than the image shape.")
                        window.le_DensityMapKernelSize.clear()
        else:
            show_error_message("Please choose an image to process.")
            window.le_DensityMapKernelSize.clear()
    else:
        show_error_message("Please choose an image to process.")
        window.le_DensityMapKernelSize.clear()

def apply_density_to_image(window :Ui_MainWindow, slice_number=None):
    '''Applies the density algorithms to the image
    Parameters:
    window : an instance of the app
    slice_number: the index of the image in the stack'''
    if window.combob_FileName.currentText():
        appMod=window.appMod
        highlight_groupbox(window,"density")
        filename = window.combob_FileName.currentText()
        single_image = False
        if slice_number is None:
            slice_number = int(window.hs_SliceNumber.value())
            single_image = True
        if appMod.included_images[filename][slice_number]:
            if appMod.thresholded_images[filename][slice_number] is not None:
                if appMod.labeling_labels[filename][slice_number] is not None:
                    if appMod.contours_mask[filename][slice_number] is not None:
                        if window.le_DensityTargetLayers.text() != "" and window.le_DensityMapKernelSize.text() != "":
                            window.setCursor(QCursor(Qt.WaitCursor))
                            thresholded_image = dots_to_binary(appMod.stacks[filename][slice_number],appMod.labeling_coordinates[filename][slice_number])
                            contoured_image = appMod.contours_mask[filename][slice_number]
                            # centroids_image = dots_to_binary(appMod.stacks[filename][slice_number],calculate_centroids(appMod.labeling_coordinates[filename][slice_number],appMod.labeling_labels[filename][slice_number]))
                            if appMod.density_centroid_size[filename][slice_number] is None:
                                centroid_size_image = calculate_centroids_sizes_image(appMod.labeling_coordinates[filename][slice_number],appMod.labeling_labels[filename][slice_number],contoured_image)
                                appMod.density_centroid_size[filename][slice_number] = centroid_size_image
                            else:
                                centroid_size_image = appMod.density_centroid_size[filename][slice_number]
                            if appMod.density_target_layers[filename][slice_number] != int(window.le_DensityTargetLayers.text()) or appMod.density_target_heatmap[filename][slice_number] is None:
                                appMod.density_target_layers[filename][slice_number] = int(window.le_DensityTargetLayers.text())
                                layers = appMod.density_target_layers[filename][slice_number]
                                centroid_y = appMod.contours_centroids[filename][slice_number][0]
                                centroid_x = appMod.contours_centroids[filename][slice_number][1]
                                target_map, target_count, target_count_per_10k_pixels, target_size = get_targets(thresholded_image,contoured_image,centroid_size_image,layers,centroid_y,centroid_x)
                                appMod.density_target_heatmap[filename][slice_number] = target_map
                                appMod.density_target_centroid_heatmap[filename][slice_number] = target_count
                                appMod.density_target_count_per_10k_pixels_heatmap[filename][slice_number] = target_count_per_10k_pixels
                                appMod.density_target_size[filename][slice_number] = target_size
                                appMod.results_density[filename] = None  
                            if appMod.density_map_kernel_size[filename][slice_number] != int(window.le_DensityMapKernelSize.text()) or appMod.density_map_heatmap[filename][slice_number] is None:
                                appMod.density_map_kernel_size[filename][slice_number] = int(window.le_DensityMapKernelSize.text())
                                d_map_percentage, d_map_count, d_map_count_per_10k_pixels, d_map_size = density_maps(thresholded_image,contoured_image,centroid_size_image,appMod.density_map_kernel_size[filename][slice_number])
                                appMod.density_map_heatmap[filename][slice_number] = d_map_percentage
                                appMod.density_map_centroid_heatmap[filename][slice_number] = d_map_count
                                appMod.density_map_count_per_10k_pixels_heatmap[filename][slice_number] = d_map_count_per_10k_pixels
                                appMod.density_map_size[filename][slice_number] = d_map_size
                                appMod.results_density[filename] = None
                            if single_image == True:
                                display_original_image(window,filename,slice_number,focus = "density")
                            window.setCursor(QCursor(Qt.ArrowCursor))
                        else:
                            show_error_message("Please choose target layers and a kernel size.")                    
                    else:
                        if single_image == True:
                            show_error_message("Please choose contouring option first.")
                        else:
                            show_error_message(f"Please process image {filename} slice {slice_number+1} with a contouring option first.")
                else:
                    if single_image == True:
                        show_error_message("Please label the image first.")
                    else:
                        show_error_message(f"Please label image {filename} slice {slice_number+1} first.")
            else:
                if single_image == True:
                    show_error_message("Please segment image first.")
                else:
                    show_error_message(f"Please segment image {filename} slice {slice_number+1} first.")
        else:
            if single_image == True:
                show_error_message("Please choose an image to process.")
    else:
        show_error_message("Please choose an image to process.")

def apply_density_to_stack(window :Ui_MainWindow, display = True):
    '''Applies the density algorithms to the current stack of images
    Parameters:
    window : an instance of the app
    display: if True, the images will be displayed'''
    if window.combob_FileName.currentText():
        filename, original_slice_number = get_filename_slice_number(window)
        if window.le_DensityTargetLayers.text() != "" and window.le_DensityMapKernelSize.text() !="":
            for i in range(len(window.appMod.stacks[filename])):
                if window.appMod.included_images[filename][i]:
                    apply_density_to_image(window,i)
            if display == True:
                set_current_image_options(window,filename,original_slice_number)
                display_original_image(window,filename,original_slice_number,focus = "density")
        else:
            show_error_message("Please choose target layers and a kernel size.")
    else:
        show_error_message("Please choose an image to process.")

def view_density(window :Ui_MainWindow):
    '''Highlights the tool 'density' and updates the image display
    Parameters:
    window : an instance of the app
    appMod : an instance of the class AppModel containing the app variables'''
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"density")
        filename, slice_number = get_filename_slice_number(window)
        display_original_image(window,filename,slice_number,focus="density")
    else:
        show_error_message("Please choose an image to process.")

def combobox_density_changed(window :Ui_MainWindow):
    '''Changes the diplay of the images when the combobox for the density is changed
    Parameters:
    window : an instance of the app'''
    filename,slice_number=get_filename_slice_number(window)
    if window.combob_DensityDisplay.currentText() == "Percentage":
        display_secondary_image(1,window,window.appMod.density_map_heatmap[filename][slice_number],focus="density",title="Convoluted density heatmap (percentage)")
        display_secondary_image(2,window,window.appMod.density_target_heatmap[filename][slice_number],focus = "density", title = "Target density heatmap (percentage)")
    elif window.combob_DensityDisplay.currentText() == "Count":
        display_secondary_image(1,window,window.appMod.density_map_centroid_heatmap[filename][slice_number],focus="density",title="Convoluted density heatmap (Count)")
        display_secondary_image(2,window,window.appMod.density_target_centroid_heatmap [filename][slice_number],focus = "density", title = "Target density heatmap (Count)")
    elif window.combob_DensityDisplay.currentText() == "Count per 10k pixels":  
        display_secondary_image(1,window,window.appMod.density_map_count_per_10k_pixels_heatmap[filename][slice_number],focus="density",title="Convoluted density heatmap (Count per 10k pixels)")
        display_secondary_image(2,window,window.appMod.density_target_count_per_10k_pixels_heatmap[filename][slice_number],focus = "density", title = "Target density heatmap (Count per 10k pixels)")
    elif window.combob_DensityDisplay.currentText() == "Mean size":
        display_secondary_image(1,window,window.appMod.density_map_size[filename][slice_number],focus="density",title="Convoluted density heatmap (Mean size)")
        display_secondary_image(2,window,window.appMod.density_target_size[filename][slice_number],focus = "density", title = "Target density heatmap (Mean size)")

def shared_colorbar_state_changed(window :Ui_MainWindow):
    ''' Changes the display of the density colobars when the checkbox is checked/unchecked
    Parameters:
    window : an instance of the app'''
    display_secondary_image(1,window,focus="density")
    display_secondary_image(2,window,focus="density")

def input_z_thickness(window :Ui_MainWindow):
    '''Controls the input of the thickness of the slices
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"results")
        if window.le_ZThickness.text() == "" or is_float(window.le_ZThickness.text()):
            filename = window.combob_FileName.currentText()
            if window.le_ZThickness.text() == "":
                window.appMod.stack_infos[filename][0] = None
            else:
                window.appMod.stack_infos[filename][0] = float(window.le_ZThickness.text())
            window.appMod.results_distance[filename] = None
        else:
            show_error_message("Please input a floating number.")
            window.le_ZThickness.clear()
    else:
        show_error_message("Please choose a stack of images to process.")
        window.le_ZThickness.clear()

def input_inter_z(window :Ui_MainWindow):
    '''Controls the input of the space between slices
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"results")
        if window.le_InterZ.text() == "" or is_float(window.le_InterZ.text()):
            filename = window.combob_FileName.currentText()
            if window.le_InterZ.text() == "":
                window.appMod.stack_infos[filename][1] = None
            else:
                window.appMod.stack_infos[filename][1] = float(window.le_InterZ.text())
            window.appMod.results_distance[filename] = None
        else:
            show_error_message("Please input a floating number.")
            window.le_InterZ.clear()
    else:
        show_error_message("Please choose a stack of images to process.")
        window.le_InterZ.clear()

def input_pixel_size(window :Ui_MainWindow):
    '''Controls the input of the pixel size
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        highlight_groupbox(window,"results")
        if window.le_PixelSize.text() == "" or is_float(window.le_PixelSize.text()):
            filename = window.combob_FileName.currentText()
            if window.le_PixelSize.text() == "":
                window.appMod.stack_infos[filename][2] = None
            else:
                window.appMod.stack_infos[filename][2] = float(window.le_PixelSize.text())
            window.appMod.results_distance[filename] = None
        else:
            show_error_message("Please input a floating number.")
            window.le_PixelSize.clear()
    else:
        show_error_message("Please choose a stack of images to process.")
        window.le_PixelSize.clear()

def apply_infos_to_stacks(window :Ui_MainWindow):
    '''Applies the input data to all the stacks
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        appMod=window.appMod
        highlight_groupbox(window,"results")
        stack_names = list(appMod.stacks.keys())
        for filename in stack_names:
            if window.le_ZThickness.text() == "":
                appMod.stack_infos[filename][0] = None
            else:
                appMod.stack_infos[filename][0] = float(window.le_ZThickness.text())
            if window.le_InterZ.text() == "":
                appMod.stack_infos[filename][1] = None
            else:
                appMod.stack_infos[filename][1] = float(window.le_InterZ.text())
            if window.le_PixelSize.text() == "":
                appMod.stack_infos[filename][2] = None
            else:
                appMod.stack_infos[filename][2] = float(window.le_PixelSize.text())
            appMod.results_distance[filename] = None
    else:
        show_error_message("Please choose a stack of images to process.")

def disable_results_checkboxes(window :Ui_MainWindow):
    '''Disables checkboxes in the result section
    Parameters:
    window : an instance of the app'''
    for widget in window.gb_ResultsChoice.findChildren(QCheckBox):
        widget.setChecked(False)
        widget.setEnabled(False)

def enable_count_results(window :Ui_MainWindow):
    '''Enables the checkboxes for count results
    Parameters:
    window : an instance of the app'''
    window.cb_ResultsCount.setEnabled(True)
    window.cb_ResultsCount.setChecked(True)

def enable_density_results(window :Ui_MainWindow):
    '''Enables the checkboxes for density results
    Parameters:
    window : an instance of the app'''
    window.cb_ResultsDensityCount.setEnabled(True)
    window.cb_ResultsDensityPercentage.setEnabled(True)
    window.cb_ResultsDensitySize.setEnabled(True)
    window.cb_ResultsDensityCount.setChecked(True)
    window.cb_ResultsDensityPercentage.setChecked(True)
    window.cb_ResultsDensitySize.setChecked(True)

def enable_distance_results(window :Ui_MainWindow,filename):
    '''Enables the checkboxes for distance results
    Parameters:
    window : an instance of the app
    filename: the name of the file'''
    window.cb_ResultsDistanceOwnCentroid.setEnabled(True)
    window.cb_ResultsDistanceOwnCentroid.setChecked(True)
    if window.appMod.stack_infos[filename][1] is not None and window.appMod.stack_infos[filename][2] is not None:
        window.cb_ResultsDistanceSpecificCentroid.setEnabled(True)
        window.cb_ResultsDistanceSpecificCentroid.setChecked(True)

def compute_count_results(window : Ui_MainWindow,filename,nb_slices):
    '''Computes the count results
    Parameters:
    window : an instance of the app
    filename: the name of the file
    nb_slices: the number of slices in the stack'''
    relative_path = get_filename(filename)
    count_results = [[relative_path,"Blobs count","Mean size"," Median size","Min size","Max size","Segmentation threshold(s)",\
                      "Blobs detection","Blobs min/max radius","Rolling ball radius","Watershed","Sieve size"]]
    total = 0
    all_sizes= []
    appMod=window.appMod
    for i in range(nb_slices):
        if appMod.included_images[filename][i]:
            slice = f"slice_{i+1:02d}/{nb_slices}"
            if appMod.labeling_coordinates[filename][i] is not None:
                if appMod.labeling_labels[filename][i] == []:
                    count = 0
                else:
                    count = np.max(appMod.labeling_labels[filename][i])
                if all_sizes== []:
                    all_sizes = appMod.labeling_images_with_labels[filename][i][5].copy()
                else:
                    all_sizes.extend(appMod.labeling_images_with_labels[filename][i][5].copy())
                total += count
                if count == 0:
                    mean_s, median_s, min_size, max_size = 0,0,0,0
                else:
                    mean_s, median_s, min_size, max_size = appMod.labeling_images_with_labels[filename][i][1],appMod.labeling_images_with_labels[filename][i][2],\
                                                            appMod.labeling_images_with_labels[filename][i][3],appMod.labeling_images_with_labels[filename][i][4]
                if appMod.threshold_algo[filename][i] == "Deep learning (UNet-DC)":
                    thresholds = "Deep learning (UNet-DC)"
                elif appMod.threshold_algo[filename][i] == window.combob_Threshold.itemText(0):
                    thresholds = str(appMod.first_threshold[filename][i])
                else:
                    thresholds = f"{appMod.first_threshold[filename][i]}_{appMod.second_threshold[filename][i]}"
                if appMod.blobs_detection_algo[filename][i] is not None:
                    blobs_algo = appMod.blobs_detection_algo[filename][i]
                    blobs_radius = f"{appMod.blobs_radius[filename][i][0]}_{appMod.blobs_radius[filename][i][1]}"
                else:
                    blobs_algo = "-"
                    blobs_radius = "-"
                if appMod.rolling_ball_param[filename][i] is not None:
                    rbr = appMod.rolling_ball_param[filename][i]
                else:
                    rbr = "-"
                if appMod.labeling_option[filename][i] == window.combob_LabelingOption.itemText(1):
                    ws = "yes"
                else:
                    ws = "no"
                sieve_size = appMod.labeling_sieve_size[filename][i]
            else:
                count,mean_s,median_s,min_size,max_size,thresholds,blobs_algo,blobs_radius,rbr,ws,sieve_size = "-","-","-","-","-","-","-","-","-","-","-"
            count_results.append([slice,count,mean_s,median_s,min_size,max_size,thresholds,blobs_algo,blobs_radius,rbr,ws,sieve_size])
    if len(all_sizes) == 0:
        tot_median, tot_SD, tot_min, tot_max = 0,0,0,0
    else:
        tot_median, tot_SD, tot_min, tot_max = round(np.mean(all_sizes),2),round(np.median(all_sizes),2),round(np.min(all_sizes),2),round(np.max(all_sizes),2)
    count_results.append(["Total",total,tot_median,tot_SD,tot_min,tot_max,"-","-","-","-","-","-"])    
    appMod.results_count[filename] = count_results

def input_count_results(window : Ui_MainWindow, filename):
    '''Input the count results in the QTableWidget
    Parameters:
    window : an instance of the app
    filename: the name of the file'''
    count_results = window.appMod.results_count[filename]
    window.tw_Count.clear()
    window.tw_Count.setRowCount(len(count_results))
    window.tw_Count.setColumnCount(len(count_results[0]))
    for i in range(len(count_results)):
        for j in range(len(count_results[0])):
            item = QTableWidgetItem(str(count_results[i][j]))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            window.tw_Count.setItem(i,j,item)
    window.tw_Count.resizeColumnsToContents()

def compute_density_results(window : Ui_MainWindow,filename,nb_slices):
    '''Computes the density results
    Parameters:
    window : an instance of the app
    filename: the name of the file
    nb_slices: the number of slices in the stack'''
    appMod=window.appMod
    relative_path = get_filename(filename)
    density_results = [[relative_path,"Mean density %","Blobs area","Contours area","Target % median","Target % min","Target % max",\
                        "Heatmap % median","Heatmap % min","Heatmap % max",\
                        "Target count mean","Target count median","Target count min","Target count max",\
                        "Heatmap count mean","Heatmap count median","Heatmap count min","Heatmap count max",\
                        "Target count per 10k pixels mean","Target count per 10k pixels median","Target count per 10k pixels min","Target count per 10k pixels max",\
                        "Heatmap count per 10k pixels mean","Heatmap count per 10k pixels median","Heatmap count per 10k pixels min","Heatmap count per 10k pixels max",\
                        "Target size mean","Target size median","Target size min","Target size max",\
                        "Heatmap size mean","Heatmap size median","Heatmap size min","Heatmap size max",\
                            "Contours algorithm","Contours threshold","Contours min size","Target layers","Kernel size"]]
    all_densities_targets_percentage = []
    all_densities_maps_percentage = []
    all_densities_targets_count = []
    all_densities_maps_count = []
    all_densities_targets_count_per_10k = []
    all_densities_maps_count_per_10k = []
    all_densities_targets_size = []
    all_densities_maps_size = []
    total_blobs_area = 0
    total_area = 0
    for i in range(nb_slices):
        if appMod.included_images[filename][i]:
            slice = f"slice_{i+1:02d}/{nb_slices}"
            if appMod.density_target_heatmap[filename][i] is not None:
                d_target = appMod.density_target_heatmap[filename][i]
                d_map = appMod.density_map_heatmap[filename][i]
                d_target_count = appMod.density_target_centroid_heatmap[filename][i]
                d_map_count = appMod.density_map_centroid_heatmap[filename][i]
                d_target_count_per_10k = appMod.density_target_count_per_10k_pixels_heatmap[filename][i]
                d_map_count_per_10k = appMod.density_map_count_per_10k_pixels_heatmap[filename][i]
                d_target_size = appMod.density_target_size[filename][i]
                d_map_size = appMod.density_map_size[filename][i]
                mask_contour = appMod.contours_mask[filename][i]
                if all_densities_targets_percentage == []:
                    all_densities_targets_percentage = d_target[mask_contour].tolist()
                    all_densities_maps_percentage = d_map[mask_contour].tolist()
                    all_densities_targets_count = d_target_count[mask_contour].tolist()
                    all_densities_maps_count = d_map_count[mask_contour].tolist()
                    all_densities_targets_count_per_10k = d_target_count_per_10k[mask_contour].tolist()
                    all_densities_maps_count_per_10k = d_map_count_per_10k[mask_contour].tolist()
                    all_densities_targets_size = d_target_size[mask_contour].tolist()
                    all_densities_maps_size = d_map_size[mask_contour].tolist()
                else:
                    all_densities_targets_percentage.extend(d_target[mask_contour].tolist())
                    all_densities_maps_percentage.extend(d_map[mask_contour].tolist())
                    all_densities_targets_count.extend(d_target_count[mask_contour].tolist())
                    all_densities_maps_count.extend(d_map_count[mask_contour].tolist())
                    all_densities_targets_count_per_10k.extend(d_target_count_per_10k[mask_contour].tolist())
                    all_densities_maps_count_per_10k.extend(d_map_count_per_10k[mask_contour].tolist())
                    all_densities_targets_size.extend(d_target_size[mask_contour].tolist())
                    all_densities_maps_size.extend(d_map_size[mask_contour].tolist())
                area = np.sum(mask_contour)
                blobs_area = len(appMod.labeling_coordinates[filename][i])
                total_area +=area
                total_blobs_area += blobs_area
                min_t,max_t,mean_t,median_t = min_max_mean_median_density(d_target,mask_contour)
                min_m,max_m,_,median_m = min_max_mean_median_density(d_map,mask_contour)
                min_t_count,max_t_count,mean_t_count,median_t_count= min_max_mean_median_density(d_target_count,mask_contour)
                min_m_count,max_m_count,mean_m_count,median_m_count = min_max_mean_median_density(d_map_count,mask_contour)
                min_t_count_per_10k,max_t_count_per_10k,mean_t_count_per_10k,median_t_count_per_10k= min_max_mean_median_density(d_target_count_per_10k,mask_contour)
                min_m_count_per_10k,max_m_count_per_10k,mean_m_count_per_10k,median_m_count_per_10k = min_max_mean_median_density(d_map_count_per_10k,mask_contour)
                min_t_size,max_t_size,mean_t_size,median_t_size= min_max_mean_median_density(d_target_size,mask_contour)
                min_m_size,max_m_size,mean_m_size,median_m_size = min_max_mean_median_density(d_map_size,mask_contour)
                contours_algo = appMod.contours_algo[filename][i]
                contours_threshold = appMod.contours_background[filename][i][0]
                if appMod.contours_background[filename][i][1] != "":
                    contours_min_size =int(appMod.contours_background[filename][i][1])
                else:
                    contours_min_size = 0
                layers = appMod.density_target_layers[filename][i]
                kernel_size = appMod.density_map_kernel_size[filename][i]
                density_results.append([slice,mean_t,blobs_area,area,median_t,min_t,max_t,median_m,min_m,max_m,\
                                        mean_t_count,round(median_t_count),round(min_t_count),round(max_t_count),\
                                        mean_m_count,round(median_m_count),round(min_m_count),round(max_m_count),\
                                        mean_t_count_per_10k,round(median_t_count_per_10k,3),round(min_t_count_per_10k,3),round(max_t_count_per_10k,3),\
                                        mean_m_count_per_10k,round(median_m_count_per_10k,3),round(min_m_count_per_10k,3),round(max_m_count_per_10k,3),\
                                        mean_t_size,round(median_t_size),round(min_t_size),round(max_t_size),\
                                        mean_m_size,round(median_m_size),round(min_m_size),round(max_m_size),\
                                        contours_algo,contours_threshold,contours_min_size,layers,kernel_size])
            else:
                density_results.append([slice,"-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-",\
                                        "-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-"])
    if len(all_densities_targets_percentage) >0:
        min_tot_t,max_tot_t,mean_tot_t,median_tot_t = round(min(all_densities_targets_percentage),3),round(max(all_densities_targets_percentage),3),\
            round(np.mean(all_densities_targets_percentage),3),round(np.median(all_densities_targets_percentage),3)
    else:
        min_tot_t,max_tot_t,mean_tot_t,median_tot_t = "-","-","-","-"
    if len(all_densities_maps_percentage) >0:
        min_tot_m,max_tot_m,median_tot_m = round(min(all_densities_maps_percentage),3),round(max(all_densities_maps_percentage),3),round(np.median(all_densities_maps_percentage),3)
    else:
        min_tot_m,max_tot_m,median_tot_m = "-","-","-"
    if len(all_densities_targets_count) >0:
        min_tot_t_count,max_tot_t_count,mean_tot_t_count,median_tot_t_count = round(min(all_densities_targets_count)),round(max(all_densities_targets_count)),\
            round(np.mean(all_densities_targets_count),3),round(np.median(all_densities_targets_count))
    else:
        min_tot_t_count,max_tot_t_count,mean_tot_t_count,median_tot_t_count = "-","-","-","-"
    if len(all_densities_maps_count) >0:
        min_tot_m_count,max_tot_m_count,mean_tot_m_count,median_tot_m_count = round(min(all_densities_maps_count)),round(max(all_densities_maps_count)),\
            round(np.mean(all_densities_maps_count),3),round(np.median(all_densities_maps_count))
    else:
        min_tot_m_count,max_tot_m_count,mean_tot_m_count,median_tot_m_count = "-","-","-","-"
    if len(all_densities_targets_count_per_10k) >0:
        min_tot_t_count_per_10k,max_tot_t_count_per_10k,mean_tot_t_count_per_10k,median_tot_t_count_per_10k = round(min(all_densities_targets_count_per_10k)),round(max(all_densities_targets_count_per_10k)),\
            round(np.mean(all_densities_targets_count_per_10k),3),round(np.median(all_densities_targets_count_per_10k))
    else:
        min_tot_t_count_per_10k,max_tot_t_count_per_10k,mean_tot_t_count_per_10k,median_tot_t_count_per_10k = "-","-","-","-"
    if len(all_densities_maps_count_per_10k) >0:
        min_tot_m_count_per_10k,max_tot_m_count_per_10k,mean_tot_m_count_per_10k,median_tot_m_count_per_10k = round(min(all_densities_maps_count_per_10k)),round(max(all_densities_maps_count_per_10k)),\
            round(np.mean(all_densities_maps_count_per_10k),3),round(np.median(all_densities_maps_count_per_10k))
    else:
        min_tot_m_count_per_10k,max_tot_m_count_per_10k,mean_tot_m_count_per_10k,median_tot_m_count_per_10k = "-","-","-","-"
    if len(all_densities_targets_size) >0:
        min_tot_t_size,max_tot_t_size,mean_tot_t_size,median_tot_t_size = round(min(all_densities_targets_size)),round(max(all_densities_targets_size)),\
            round(np.mean(all_densities_targets_size),3),round(np.median(all_densities_targets_size))
    else:
        min_tot_t_size,max_tot_t_size,mean_tot_t_size,median_tot_t_size = "-","-","-","-"
    if len(all_densities_maps_size) >0:
        min_tot_m_size,max_tot_m_size,mean_tot_m_size,median_tot_m_size = round(min(all_densities_maps_size)),round(max(all_densities_maps_size)),\
            round(np.mean(all_densities_maps_size),3),round(np.median(all_densities_maps_size))
    else:
        min_tot_m_size,max_tot_m_size,mean_tot_m_size,median_tot_m_size = "-","-","-","-"

    density_results.append(["Total",mean_tot_t,total_blobs_area,total_area,median_tot_t,min_tot_t,max_tot_t,median_tot_m,min_tot_m,max_tot_m,\
                            mean_tot_t_count,median_tot_t_count,min_tot_t_count,max_tot_t_count,mean_tot_m_count,median_tot_m_count,min_tot_m_count,max_tot_m_count,\
                            mean_tot_t_count_per_10k,median_tot_t_count_per_10k,min_tot_t_count_per_10k,max_tot_t_count_per_10k,mean_tot_m_count_per_10k,median_tot_m_count_per_10k,min_tot_m_count_per_10k,max_tot_m_count_per_10k,\
                            mean_tot_t_size,median_tot_t_size,min_tot_t_size,max_tot_t_size,mean_tot_m_size,median_tot_m_size,min_tot_m_size,max_tot_m_size,"-","-","-","-","-"])    
    appMod.results_density[filename] = density_results

def input_density_results(window : Ui_MainWindow, filename):
    '''Input the density results in the QTableWidget
    Parameters:
    window : an instance of the app
    filename: the name of the file'''
    density_results = window.appMod.results_density[filename]
    window.tw_Density.clear()
    window.tw_Density.setRowCount(len(density_results))
    window.tw_Density.setColumnCount(len(density_results[0]))
    for i in range(len(density_results)):
        for j in range(len(density_results[0])):
            item = QTableWidgetItem(str(density_results[i][j]))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            window.tw_Density.setItem(i,j,item)
    window.tw_Density.resizeColumnsToContents()

def compute_distance_results(window : Ui_MainWindow,filename,nb_slices):
    '''Computes the distance results
    Parameters:
    window : an instance of the app
    filename: the name of the file
    nb_slices: the number of slices in the stack'''
    appMod=window.appMod
    relative_path = get_filename(filename)
    if not any(appMod.contours_main_slice[filename]):
        determine_main_slice(appMod,filename)
    for i, value in enumerate(appMod.contours_main_slice[filename]):
        if value:
            main_slice = i
            break
    distance_results = [[relative_path,"Centroid X","Centroid Y","Centroid Z","Mean distance to own centroid","median DTOC","min DTOC","max DTOC",\
                         f"Mean distance to centroid of slice {main_slice+1}",f"median DTCOS{main_slice+1}",f"min DTCOS{main_slice+1}",f"max DTCOS{main_slice+1}",\
                            "Slice thickness","Interslice space","Pixel size"]]
    all_DTOC = []
    all_DTCOS = []
    if appMod.stack_infos[filename][1] is not None and appMod.stack_infos[filename][2] is not None:
        if appMod.stack_infos[filename][0] is None:
            slice_thickness = 0
        else:
            slice_thickness = appMod.stack_infos[filename][0]
        interslice_space = appMod.stack_infos[filename][1]
        pixel_size = appMod.stack_infos[filename][2]
        main_slice_y_coordinate, main_slice_x_coordinate = appMod.contours_centroids[filename][main_slice]
        main_slice_z_coordinate = round((main_slice * ((slice_thickness+interslice_space) / pixel_size)),1)
    else:
        slice_thickness = "-"
        interslice_space = "-"
        pixel_size = "-"
    for i in range(nb_slices):
        if appMod.included_images[filename][i]:
            slice = f"slice_{i+1:02d}/{nb_slices}"
            if appMod.labeling_labels[filename][i] is not None and appMod.contours_centroids[filename][i] is not None:
                labels = appMod.labeling_labels[filename][i]
                dots = appMod.labeling_coordinates[filename][i]
                centroid_y,centroid_x = appMod.contours_centroids[filename][i]
                centroid_y=round(centroid_y,1)
                centroid_x=round(centroid_x,1)
                blobs_centroids_list, DTOC = calculate_blobs_centroids_and_DTOC(dots,labels,centroid_x,centroid_y)
                if DTOC != []:
                    if all_DTOC == []:
                        all_DTOC = DTOC
                    else:
                        all_DTOC.extend(DTOC)
                    DTOC_mean,DTOC_median,DTOC_min,DTOC_max = round(np.mean(DTOC),1),round(np.median(DTOC),1),round(min(DTOC),1),round(max(DTOC),1)
                else:
                    DTOC_mean,DTOC_median,DTOC_min,DTOC_max = "-","-","-","-"
                if appMod.stack_infos[filename][1] is not None and appMod.stack_infos[filename][2] is not None:
                    z_coordinate = round((i * ((slice_thickness+interslice_space) / pixel_size)),1)
                    if len(blobs_centroids_list) != 0:
                        if i != main_slice:
                            z_difference_square = (z_coordinate - main_slice_z_coordinate)**2
                            DTCOS = np.sqrt((blobs_centroids_list[:,0]-main_slice_y_coordinate)**2 + (blobs_centroids_list[:,1]-main_slice_x_coordinate)**2 + z_difference_square)
                            DTCOS = DTCOS.tolist()
                            DTCOS_mean,DTCOS_median,DTCOS_min,DTCOS_max = round(np.mean(DTCOS),1),round(np.median(DTCOS),1),round(min(DTCOS),1),round(max(DTCOS),1)
                        else:
                            DTCOS = DTOC
                            DTCOS_mean,DTCOS_median,DTCOS_min,DTCOS_max = DTOC_mean,DTOC_median,DTOC_min,DTOC_max
                        if all_DTCOS == []:
                            all_DTCOS = DTCOS
                        else:
                            all_DTCOS.extend(DTCOS)
                    else:
                        DTCOS_mean,DTCOS_median,DTCOS_min,DTCOS_max = "-","-","-","-"
                else:
                    z_coordinate = f"z{i+1}"
                    DTCOS_mean,DTCOS_median,DTCOS_min,DTCOS_max = "-","-","-","-"
                distance_results.append([slice,centroid_x,centroid_y,z_coordinate,DTOC_mean,DTOC_median,DTOC_min,DTOC_max,DTCOS_mean,DTCOS_median,DTCOS_min,DTCOS_max,slice_thickness,interslice_space,pixel_size])
            else:
                distance_results.append([slice,"-","-","-","-","-","-","-","-","-","-","-",slice_thickness,interslice_space,pixel_size])
    if len(all_DTOC) != 0:
        min_tot_DTOC,max_tot_DTOC,mean_tot_DTOC,median_tot_DTOC = round(min(all_DTOC),1),round(max(all_DTOC),1), round(np.mean(all_DTOC),1),round(np.median(all_DTOC),1)
    else:
        min_tot_DTOC,max_tot_DTOC,mean_tot_DTOC,median_tot_DTOC = "-","-","-","-"
    if DTCOS_mean != "-":
        min_tot_DTCOS,max_tot_DTCOS,mean_tot_DTCOS,median_tot_DTCOS = round(min(all_DTCOS),1),round(max(all_DTCOS),1), round(np.mean(all_DTCOS),1),round(np.median(all_DTCOS),1)
    else:
        min_tot_DTCOS,max_tot_DTCOS,mean_tot_DTCOS,median_tot_DTCOS = "-","-","-","-"
    distance_results.append(["Total","-","-","-",mean_tot_DTOC,median_tot_DTOC,min_tot_DTOC,max_tot_DTOC,mean_tot_DTCOS,median_tot_DTCOS,min_tot_DTCOS,max_tot_DTCOS,slice_thickness,interslice_space,pixel_size])    
    appMod.results_distance[filename] = distance_results

def input_distance_results(window : Ui_MainWindow, filename):
    '''Input the distance results in the QTableWidget
    Parameters:
    window : an instance of the app
    filename: the name of the file'''
    distance_results = window.appMod.results_distance[filename]
    window.tw_Distance.clear()
    window.tw_Distance.setRowCount(len(distance_results))
    window.tw_Distance.setColumnCount(len(distance_results[0]))
    for i in range(len(distance_results)):
        for j in range(len(distance_results[0])):
            item = QTableWidgetItem(str(distance_results[i][j]))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            window.tw_Distance.setItem(i,j,item)
    window.tw_Distance.resizeColumnsToContents()
    
def view_results_page(window :Ui_MainWindow):
    '''Displays the result page
    Parameters:
    window : an instance of the app'''
    if window.combob_FileName.currentText():
        appMod=window.appMod
        window.setCursor(QCursor(Qt.WaitCursor))
        highlight_groupbox(window,"results")
        filename = window.combob_FileName.currentText()
        nb_slices = len(appMod.stacks[filename])
        count = False
        density = False
        distance = False
        at_least_one_slice = False
        window.tw_Count.setEnabled(False)
        window.tw_Density.setEnabled(False)
        window.tw_Distance.setEnabled(False)
        disable_results_checkboxes(window)
        for i in range(nb_slices):
            if appMod.included_images[filename][i]:
                at_least_one_slice = True
                if appMod.labeling_labels[filename][i] is not None:
                    count = True
                    window.tw_Count.setEnabled(True)
                if appMod.density_target_heatmap[filename][i] is not None:
                    density = True
                    window.tw_Density.setEnabled(True)
                if appMod.contours_mask[filename][i] is not None and appMod.labeling_labels[filename][i] is not None:
                    distance = True
                    window.tw_Distance.setEnabled(True)
        if at_least_one_slice == False:
            show_error_message("Please select at least one slice to get some results.")
        if count == False and density == False and distance == False:
            show_error_message("Please process the images to get results.")
        else:
            if count == True:
                if appMod.results_count[filename] is None:
                    compute_count_results(window,filename,nb_slices)
                input_count_results(window,filename)
            if density == True:
                if appMod.results_density[filename] is None:
                    compute_density_results(window,filename,nb_slices)
                input_density_results(window,filename)
            if distance == True:
                if appMod.results_distance[filename] is None:
                    compute_distance_results(window,filename,nb_slices)
                input_distance_results(window,filename)
            if appMod.results_count[filename] is not None:
                enable_count_results(window)
            if appMod.results_density[filename] is not None:
                enable_density_results(window)
            if appMod.results_distance[filename] is not None:
                enable_distance_results(window,filename)
            if window.lb_ResultsDestinationFolder.text() == "":
                window.lb_ResultsDestinationFolder.setText("./results/")
            window.le_ResultsCSVFileName.setText(get_filename_without_extension(filename)+"_results")
            window.sw_Data.setCurrentIndex(1)
            window.tabWidget.show()
            window.gb_ResultsChoice.show()
            window.frame_4.show()
        window.setCursor(QCursor(Qt.ArrowCursor))
    else:
        show_error_message("Please choose a stack of images to process.")

def select_all(window :Ui_MainWindow):
    '''Checks the checkboxes for all results
    Parameters:
    window : an instance of the app'''
    widget = window.gb_ResultsChoice
    for checkbox in widget.findChildren(QCheckBox):
        if checkbox.isEnabled():
            checkbox.setChecked(True)

def select_none(window :Ui_MainWindow):
    '''Unchecks the checkboxes for all results
    Parameters:
    window : an instance of the app'''
    widget = window.gb_ResultsChoice
    for checkbox in widget.findChildren(QCheckBox):
        if checkbox.isEnabled():
            checkbox.setChecked(False)

def select_folder(window :Ui_MainWindow,widget):
    '''Selects a folder and displays it in a widget
    Parameters:
    window : an instance of the app
    widget: the widget in which to display the chosen folder name'''
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    dialog = QFileDialog(window, "Select Folder", options=options)
    dialog.setFileMode(QFileDialog.FileMode.Directory)
    folder_path = QFileDialog.getExistingDirectory()
    widget.setText(folder_path)

def return_to_images_screen(window :Ui_MainWindow):
    '''Goes back from the result display to the image display
    Parameters:
    window : an instance of the app'''
    highlight_groupbox(window,None)
    filename, slice_number = get_filename_slice_number(window)
    display_original_image(window,filename,slice_number,focus=None)

def check_file_name(window : Ui_MainWindow, widget):
    '''Checks that an input file name only contains allowed characters and displays the name in a widget
    Parameters:
    window : an instance of the app
    widget: the widget in which to display the chosen folder name'''
    filename = widget.text()
    allowed_characters = re.compile(r'^[a-zA-Z0-9_\- µ]*$')
    if not allowed_characters.match(filename):
        show_error_message("Invalid file name. Please use only letters, numbers, underscore, hyphen, space and µ.")
        filename = window.combob_FileName.currentText()
        if widget.objectName() == "le_ResultsCSVFileName":
            widget.setText(get_filename_without_extension(filename)+"_results")
        else:
            now = datetime.now()
            now_string = now.strftime("%Y-%m-%d_%H-%M-%S")
            widget.setText(now_string+"_analysis")

def check_checkboxes(groupbox):
    '''Checks if an any checkbox is checked in a widget
    Parameters:
    groupbox: the widget in which checking all the checkboxes
    Return:
    True if any checkbox is checked'''
    for widget in groupbox.findChildren(QCheckBox):
        if widget.isChecked():
            return True
    return False

def show_save_message(message):
    '''Displays a QDialog window with a warning message
    Parameters:
    message : the message to display'''
    dialog = QDialog()
    dialog.setWindowTitle("Save successful")
    icon = QIcon()
    icon.addFile(u":/Icons/blob-161097_640.png", QSize(), QIcon.Normal, QIcon.Off)
    dialog.setWindowIcon(icon)
    dialog.setModal(True)
    label = QLabel(message)
    label.setAlignment(Qt.AlignCenter)
    button_ok = QPushButton("OK")
    button_ok.clicked.connect(dialog.accept)
    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(button_ok)
    dialog.setLayout(layout)
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)
    dialog.show()
    dialog.exec()

def save_results(window :Ui_MainWindow):
    '''Save the results in two csv files; a summary and a file with the details of each blob per slice
    Parameters:
    window : an instance of the app'''
    if check_checkboxes(window.gb_ResultsChoice):
        window.setCursor(QCursor(Qt.WaitCursor))
        try:
            appMod=window.appMod
            filename = window.combob_FileName.currentText()
            folder = window.lb_ResultsDestinationFolder.text()
            if not folder.endswith("/") and not folder.endswith("\\"):
                folder+="/"
            csv_filename = folder+window.le_ResultsCSVFileName.text()+"_summary.csv"
            csv_filename_per_slice = folder+window.le_ResultsCSVFileName.text()+"_per_slice.csv"
            table_first_row = False
            results = []
            if window.cb_ResultsCount.isChecked():
                results = np.array(appMod.results_count[filename],dtype=str)
                table_first_row = True
            if window.cb_ResultsDensityPercentage.isChecked() or window.cb_ResultsDensityCount.isChecked() or window.cb_ResultsDensitySize.isChecked():
                density_results = np.array(appMod.results_density[filename], dtype=str)
                columns_to_add = set()
                if window.cb_ResultsDensityPercentage.isChecked():
                    columns_to_add.update([1,2,3,4,5,6,7,8,9,26,27,28,29,30])
                if window.cb_ResultsDensityCount.isChecked():
                    columns_to_add.update([1,2,3,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,34,35,36,37,38])
                if window.cb_ResultsDensitySize.isChecked():
                    columns_to_add.update([1,2,3,26,27,28,29,30,31,32,33,34,35,36,37,38])
                columns_to_add = list(columns_to_add)
                if table_first_row == True:
                    results = np.concatenate((results,density_results[:,columns_to_add]),axis=1)
                else:
                    results = density_results[:,0][:, np.newaxis]
                    results = np.concatenate((results,density_results[:,columns_to_add]),axis=1)
                    table_first_row = True
            if window.cb_ResultsDistanceOwnCentroid.isChecked() or window.cb_ResultsDistanceOwnCentroid.isChecked():
                distance_results = np.array(appMod.results_distance[filename],dtype=str)
                columns_to_add = set()
                if window.cb_ResultsDistanceOwnCentroid.isChecked():
                    columns_to_add.update([1,2,3,4,5,6,7,12,13,14])
                if window.cb_ResultsDistanceSpecificCentroid.isChecked():
                    columns_to_add.update([1,2,3,8,9,10,11,12,13,14])
                columns_to_add = list(columns_to_add)
                if table_first_row == True:
                    results = np.concatenate((results,distance_results[:,columns_to_add]),axis=1)
                else:
                    results = distance_results[:,0][:, np.newaxis]
                    results = np.concatenate((results,distance_results[:,columns_to_add]),axis=1)
            np.savetxt(csv_filename,results,delimiter=";",fmt='%s')
            results = []
            if appMod.results_count[filename] is not None: 
                for i, value in enumerate(appMod.contours_main_slice[filename]):
                    if value:
                        main_slice = i
                        break
                for i in range(len(appMod.stacks[filename])):
                    if appMod.included_images[filename][i] and appMod.labeling_coordinates[filename][i] is not None:
                        dots = appMod.labeling_coordinates[filename][i]
                        labels = appMod.labeling_labels[filename][i]
                        centroidsAndSizes = calculate_centroids_sizes(dots,labels)
                        length = len(centroidsAndSizes)
                        if appMod.results_density[filename] is not None or appMod.results_distance[filename] is not None:
                            centroid_y , centroid_x = appMod.contours_centroids[filename][i]
                            if length > 0:
                                DTOC = np.sqrt((centroidsAndSizes[:, 0] - centroid_y) ** 2 + (centroidsAndSizes[:, 1] - centroid_x) ** 2)
                            else:
                                DTOC = None
                            if appMod.stack_infos[filename][1] is not None and appMod.stack_infos[filename][2] is not None:
                                if appMod.stack_infos[filename][0] is None:
                                    slice_thickness = 0
                                else:
                                    slice_thickness = appMod.stack_infos[filename][0]
                                interslice_space = appMod.stack_infos[filename][1]
                                pixel_size = appMod.stack_infos[filename][2]
                                main_slice_y_coordinate, main_slice_x_coordinate = appMod.contours_centroids[filename][main_slice]
                                main_slice_z_coordinate = round((main_slice * ((slice_thickness+interslice_space) / pixel_size)),1)
                                z_coordinate = round((i * ((slice_thickness+interslice_space) / pixel_size)),1)
                                z_difference_square = (z_coordinate - main_slice_z_coordinate)**2
                                if length > 0:
                                    DTCOS = np.sqrt((centroidsAndSizes[:,0]-main_slice_y_coordinate)**2 + (centroidsAndSizes[:,1]-main_slice_x_coordinate)**2 + z_difference_square)
                                else:
                                    DTCOS = None
                            else:
                                z_coordinate = f"z{i+1}"
                                DTCOS = None
                        else:
                            DTOC = None
                            DTCOS = None
                        if length >0:
                            centroidsAndSizes[:,[0,1]]=centroidsAndSizes[:,[1,0]]
                        else:
                            centroidsAndSizes = np.array(["-","-","-"])
                        header = [f"x slice {i+1}",f"y slice {i+1}",f"size slice {i+1}"]
                        if DTOC is not None:
                            DTOC = np.array(DTOC)[:, np.newaxis]
                            centroidsAndSizes = np.concatenate((centroidsAndSizes,DTOC),axis=1)
                            header.append(f"DTOC slice {i+1}")
                        if DTCOS is not None:
                            DTCOS = np.array(DTCOS)[:, np.newaxis]
                            centroidsAndSizes = np.concatenate((centroidsAndSizes,DTCOS),axis=1)
                            z_coordinate_list = [z_coordinate]*length
                            z_coordinate_array = np.array([z_coordinate_list])
                            centroidsAndSizes = np.insert(centroidsAndSizes,2,z_coordinate_array,axis=1)
                            header.insert(2,f"z slice {i+1}")
                            header.append(f"DTCOS{main_slice+1} slice {i+1}")
                        if length > 0:
                            centroidsAndSizes = np.round(centroidsAndSizes,decimals=1)
                        header = np.array([header])
                        centroidsAndSizes = np.vstack((header,centroidsAndSizes))
                        if len(results) == 0:
                            results = centroidsAndSizes
                        else:
                            results = np.array(results)
                            centroidsAndSizes = np.array(centroidsAndSizes)
                            max_rows = max(results.shape[0], centroidsAndSizes.shape[0])
                            results_padded = np.pad(results, ((0, max_rows - results.shape[0]), (0, 0)), mode='constant', constant_values='')
                            centroidsAndSizes_padded = np.pad(centroidsAndSizes, ((0, max_rows - centroidsAndSizes.shape[0]), (0, 0)), mode='constant', constant_values='')
                            results = np.concatenate((results_padded,centroidsAndSizes_padded),axis=1)
                first_column = np.empty(results.shape[0], dtype="str")
                first_column[:] = ""
                title = get_filename(filename)
                results = np.insert(results,0,first_column,axis=1)
                results[0,0] = title
                with open(csv_filename_per_slice, "w", newline='',) as file:
                    writer = csv.writer(file,delimiter=";")
                    for line in results:
                        writer.writerow(line)
                show_save_message(f"The file has been successfully saved in {folder}")                  
        except (ValueError, TypeError, PermissionError, IndexError) as e:
            show_error_message(f"An error occured while saving the results:\n{e}")
        window.setCursor(QCursor(Qt.ArrowCursor))
    else:
        show_error_message("Please choose at least one result or image to save.")
    
def open_save_analysis_window(window : Ui_MainWindow):
    '''Opens a window to choose the folder and the file name to save an analysis
    Parameters:
    window : an instance of the app'''
    window.save_analysis_window = SaveAnalysisWindow(window)
    window.save_analysis_window.pb_ChooseDestinationFolder.clicked.connect(lambda : select_folder(window.save_analysis_window,window.save_analysis_window.lb_DestinationFolder))
    window.save_analysis_window.lb_DestinationFolder.setText("./analysis/")
    window.save_analysis_window.le_FileName.editingFinished.connect(lambda : check_file_name(window.save_analysis_window,window.save_analysis_window.le_FileName))
    window.save_analysis_window.pb_SaveAnalysis.clicked.connect(lambda : save_analysis(window.save_analysis_window))
    window.save_analysis_window.show()

def save_analysis(window : SaveAnalysisWindow):
    '''Saves the analysis in a file as a joblib object
    Parameters:
    window: an instance of the class SaveAnalysisWindow'''
    window.setCursor(QCursor(Qt.WaitCursor))
    try:
        filename = window.le_FileName.text()
        if filename == "":
            now = datetime.now()
            filename = now.strftime("%Y-%m-%d_%H-%M-%S")
        folder = window.lb_DestinationFolder.text()
        if folder == "":
            folder = "./"
        if not folder.endswith("/") and not folder.endswith("\\"):
            folder+="/"
        appMod = window.main_window.appMod
        dump(appMod,folder+filename+"_analysis.joblib",compress= True)
        show_save_message(f"The analysis has been successfully saved in {folder}")
        window.close()
    except (AttributeError, FileNotFoundError, PermissionError, TypeError, IOError, KeyError) as e:
        show_error_message(f"An error occured during while saving the analysis:\n{e}")
    window.setCursor(QCursor(Qt.ArrowCursor))

def load_analysis(window : Ui_MainWindow):
    '''Load an analysis from a joblib file
    Parameters:
    window : an instance of the app'''
    filename, _ = QFileDialog.getOpenFileName(window,
        "Choose files",
        "./analysis/",
        "Analysis files (*.joblib)"
    )
    window.setCursor(QCursor(Qt.WaitCursor))
    if filename:
        remove_all_images(window)
        window.appMod = load(filename)
        ensure_deep_learning_defaults(window.appMod)
        if hasattr(window.appMod, "stacks"):
            for stack_filename in list(window.appMod.stacks.keys()):
                if os.path.exists(stack_filename):
                    try:
                        window.appMod.original_stacks[stack_filename] = load_raw_stack_frames(stack_filename)
                    except Exception:
                        pass
        sync_deep_learning_controls(window)
        if hasattr(window.appMod, "stacks"):
            if len(window.appMod.stacks) > 0:
                window.appMod.stack_names = list(window.appMod.stacks.keys())
                if window.appMod.stack_names:
                    window.combob_FileName.clear()
                    window.combob_FileName.addItems(window.appMod.stack_names)
                    highlight_groupbox(window,None)
                    window.combob_FileName.setCurrentIndex(0)
                    if window.appMod.included_images[window.appMod.stack_names[0]][0]:
                        window.cb_IncludeImage.setCheckState(Qt.CheckState.Checked)
                    else:
                        window.cb_IncludeImage.setCheckState(Qt.CheckState.Unchecked)
                    window.cb_Scale.setCheckState(Qt.CheckState.Unchecked)
                    set_current_image_options(window,window.appMod.stack_names[0],0)
                    display_original_image(window,window.appMod.stack_names[0],0)
                    update_image_slider_range(window,window.appMod.stack_names[0])
            else:
                window.wi_OriginalText.hide()
                window.wi_Image1Text.hide()
                window.wi_Image2Text.hide()
                window.tabWidget.hide()
                window.gb_ResultsChoice.hide()
                window.wi_Image1Canvas.hide()
                window.wi_Image2Canvas.hide()
                window.wi_OriginalImage.hide()
                window.frame_4.hide()
                window.cb_Scale.setCheckState(Qt.CheckState.Unchecked)
        else:
            show_error_message("Incorrect file format.")
            window.appMod = AppModel()
            window.wi_OriginalText.hide()
            window.wi_Image1Text.hide()
            window.wi_Image2Text.hide()
            window.tabWidget.hide()
            window.gb_ResultsChoice.hide()
            window.wi_Image1Canvas.hide()
            window.wi_Image2Canvas.hide()
            window.wi_OriginalImage.hide()
            window.frame_4.hide()
            window.cb_Scale.setCheckState(Qt.CheckState.Unchecked)
        window.setCursor(QCursor(Qt.ArrowCursor))
