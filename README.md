# Blob Inspector

Blob Inspector is a software designed to analyze blobs in biological images. It provides several common tools
for computing metrics related to the blobs, such as coordinates, size, density, and distances.

![Interface preview](/resources/images/app_image.png)

## Tools

The software offers the following tools:
- Illumination correction
- Segmentation
- Labeling
- Contouring

Results can be saved in CSV files.

## About

Blob Inspector was authored by Laurent Busson as the final project for a Master's degree in Bioinformatics at
the University of Bordeaux in collaboration with BRIC (BoRdeaux Institute of onCology) Team 1, UMR1312, INSERM,
Univ. Bordeaux and LaBRI (Laboratoire Bordelais de Recherche en Informatique).
It was developed in Python with the librairies PySide6, scikit-image, numpy, matplotlib and SciPy.
Blob Inspector is released under GNU GPL license.

## Installation

Before installing Blob Inspector, make sure Python is installed on your operating system. You will need
administrator rights to do so.

### Windows and macOS
1. Download and install the latest version of Python from [Python's official website](https://www.python.org/).
   
### Linux
1. Open a terminal and type the following command:
```bash
sudo apt-get install python
```

2. Once Python is installed on your OS, open a terminal or PowerShell in the root directory of
the program and run the following command to install all the required packages:
```bash
python install_packages.py
```
This command will install all the necessary dependencies for running the program.

## Running the software

To launch the software, open a terminal or PowerShell in the root directory of the program and 
run the following command:
```bash
python appli.py
```

For Windows users, you can also double click on the file "BlobInspectorWindows.bat"

## Instructions
The Blob Inspector interface is designed for ease of use. Tooltips are provided for all interface
elements, offering guidance on their usage and selection.

1. Menu bar
    - Files:
        - Load Image: Loads an image or a stack of images. Upon loading, images are transformed into
        8-bit grayscale and equalized, with the highest pixel value of the original image set to 255.
        Original images are displayed in the left third of the software. Stacks can be navigated using
        the dropdown menu, and images within a stack using the slider. Individual images can be excluded
        from analysis by unchecking the "Include" checkbox above each image. Clicking the "Histogram"
        button provides access to the image's histogram. Scaling can be superimposed on the image if
        necessary information is provided in the user profile (accessible in Options), along with pixel
        size either in the user profile or in the "Results" section. Each image is accompanied by a
        toolbar with tooltips explaining each icon. Hovering over an image displays pixel coordinates
        and values in the toolbar.
        - Remove all stacks: removes all images and stacks
        - Remove current stack: removes the current stack
        - Save analysis: saves the loaded images and current processings into a file (by default in the
        analysis folder of the application)
        - Load analysis: loads a saved analysis
        - Quit: exits the program
    - Process:
        - Batch analysis: opens a window for analyzing all included images across all stacks. Options
        can be automatically filled with current user profile settings.
    - Options:
        - Profiles: allows creation of user profiles with default options.
    - About:
        - Version: provides informations about the software.

2. Tools
    The available tools are located in a ribbon at the top of the screen, intended to be used from left
    to right. Some tools are optional. When options are selected for a tool, you can apply the processing
    to the current image or stack of images. Changing options for a tool afterward may cancel the processing
    of the image with subsequent tools. Tool results are displayed in the right two-thirds of the application.
    You can navigate between tools by clicking the "View" buttons, which displays the processed image if the
    specific tool was used. The tools are as follows:
    - Illumination correction (optional):
    The rolling ball algorithm has been chosen. To use it, choose a rolling ball radius in pixels. The display
    will show the calculated background on the right and the corrected image, resulting from the subtaction of
    the background to the original image, in the center of the screen. This corrected image will be used for
    further processing. You can cancel this tool by clearing the rolling ball radius parameter and applying
    the modification to the image or stack.
    ![Illumination](/resources/images/GUI_illumination.png)
    - Segmentation:
        - Thresholding (mandatory): Choose one or two thresholds (hysteresis thresholding). Input a value
        between 0 and 255. The first threshold must be higher than the second. If you input a value between
        0 and 1, the resulting threshold will be a percentage of the maximum pixel value in the image
        (255 due to equalization). Adjust the threshold by clicking in the desired field and using the up and
        down arrows or scroll wheel while the mouse cursor is above the field. Modifications will be displayed
        in real-time on the image without needing to click the "Apply to image" button.
        - Blob Detection Algorithms (optional): Choose a blob detection algorithm among LoG (Laplacian of
        Gaussian), DoG (Difference of Gaussian), and DoH (Determinant of Hessian). Input minimum and maximum
        radii of the blobs to be detected. Click the "Apply" button to see results. The thresholded image will
        be displayed in the center of the screen. On the right side of the screen, the displayed image shows
        common pixels between the thresholded image and the blob detection algorithm on the thresholded image.
        As blob detection algorithms return a list of centroid coordinates and radii, the resulting image may
        display some cropped objects compared to the thresholded image.
    ![Segmentation](/resources/images/GUI_segmentation.png)
        - Labeling (mandatory): This tool performs semantic segmentation of thresholded objects. If the
        "No separation" option is chosen, each individual object consists of connected pixels in 8 directions.
        If "Watershed" is selected, the watershed algorithm is applied to attempt to separate connected objects.
        The "Sieve size" field requires an integer value; objects with a size in pixels equal to or smaller than
        this value will be discarded. Choosing a value of 0 will retain all objects.
    ![Labeling](/resources/images/GUI_labeling.png)
    - Shape contours (mandatory):
    This tool determines the contours of shapes containing blobs. Several algorithms are available. The maximum
    threshold value must be input (all pixels equal to or less than this value will be considered background,
    depending on the chosen algorithm). The "Min size" field can be left empty or filled with an integer to
    specify the minimum size of the contoured shapes in pixels. Contoured shapes smaller than this value will
    be discarded which is useful for eliminating some aberrant pixels outside the main shape. On the contoured
    shape, the computed centroid is indicated with a red cross. You can manually change its coordinates or reset
    them with the "Auto" button. The slice with the highest pixel count in the contoured shape will be considered
    the main slice of the stack. Distances from the centroids of all blobs to the centroid of the main slice will
    be computed if the required information is input (slice thickness, interslice space, and pixel size). You can
    change the main slice by clicking the "Main Slice" checkbox above the desired image.
    ![Contours](/resources/images/GUI_contours.png)
    - Density (optional):
    This tool computes the density of blobs within the contoured shape. To do so, you must choose a kernel size
    for performing convolution. The kernel must be an odd integer, at least 3, and less than the image dimensions.
    Additionally, you need to select the number of layers to compute density in concentric regions within the
    contoured shape. The layers are established by dividing the distance between the centroid and the furthest
    point within the contoured shape. If there are aberrant pixels outside the main contoured shape, the division
    may be affected.  Density can be displayed in four ways, selectable from a dropdown menu above the center image:
        - Percentage: Number of blob pixels divided by the number of contoured shape pixels per area (kernel for
        the convoluted heatmap and concentric region for the target heatmap)
        - Count: Number of blob centroids per area
        - Count per 10k pixels: Number of blobs centroids per area normalized to 10000 pixels
        - Mean size: Mean size of blobs in pixels per area
    The colormap can be chosen from a dropdown menu above the center image. If the "Shared cb" checkbox (cb for
    colorbar) is selected, the colorbars will have the same scale for all processed images.
    ![Density](/resources/images/GUI_density.png)
    - Results:
    In this section you can input stack informations in order to compute distances between blobs and contoured
    shape centroids. Blob Inspector was designed to detect blobs in confocal microscope images.
    To compute distances between stack slices, input the slice thickness (if left empty, a value of 0 will be
    automatically chosen) and the interslice space. In any case, the pixel size must be input to compute distances.
    All three values must be in the same unit (e.g., µm).
    To view the results, click the "View" button in the "Results" section. All results (sizes, distances) are in
    pixels. You can navigate through the results by clicking on the desired tab. In the lower part of the screen,
    you can check or uncheck the results you want to keep. You can change the folder and the name of the file to
    save. Clicking the "Save results" button generates two CSV files: one with a summary of the results and the
    other with the coordinates, sizes, and distances of the blobs for each slice. Results are saved for the current
    stack. To save results from another stack, click the "Back" button in the lower-left corner of the page and go
    to the desired stack.
    ![Results](/resources/images/GUI_results.png)

