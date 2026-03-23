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

class AppModel(object):
    def __init__(self):
        self.stacks = {}
        self.original_stacks = {}
        self.stack_names = []
        self.included_images = {}
        self.corrected_images = {}
        self.rolling_ball_param = {}
        self.rolling_ball_background = {}

        self.threshold_algo = {}
        self.first_threshold = {}
        self.second_threshold = {}
        self.thresholded_images = {}
        self.segmentation_method = "Classical"
        self.dl_checkpoint_path = ""
        self.dl_prob_thresh = 0.3
        self.dl_background_radius = 50
        self.dl_device = "auto"

        self.blobs_detection_algo = {}
        self.blobs_radius = {}
        self.blobs_thresholded_images = {}

        self.labeling_option = {}
        self.labeling_sieve_size = {}
        self.labeling_coordinates = {}
        self.labeling_labels = {}
        self.labeling_images_with_labels = {}
        self.labeling_images_conserved_blobs = {}

        self.contours_algo = {}
        self.contours_background = {}
        self.contours_mask = {}
        self.contours_centroids = {}
        self.contours_main_slice = {}

        self.density_target_layers = {}
        self.density_map_kernel_size = {}
        self.density_centroid_size = {}
        self.density_target_heatmap = {}
        self.density_map_heatmap = {}
        self.density_target_centroid_heatmap = {}
        self.density_map_centroid_heatmap = {}
        self.density_target_count_per_10k_pixels_heatmap = {}
        self.density_map_count_per_10k_pixels_heatmap = {}
        self.density_target_size = {}
        self.density_map_size = {}
        

        self.results_count = {}
        self.results_density = {}
        self.results_distance = {}

        self.stack_infos = {}

        
