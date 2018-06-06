import json
import cv2
import glob
import os
import numpy as np

cv2.setUseOptimized(True)

class Stitcher():

    def __init__(self, position_list_filename):

        # Change directory to directory of position_list_filename
        abs_path = os.path.abspath(position_list_filename)
        dir_name = os.path.dirname(abs_path)
        os.chdir(dir_name)

        # Find all filenames of .tif files in directory
        self.filenames = []
        for filename in glob.glob("*.tif"):
            self.filenames.append(filename)

        # Load data in position_list_filename as JSON object
        with open(position_list_filename) as f:
            self.position_list = json.load(f)

        # Load image details into Tile objects
        self.tiles = []

        ## Loop through all files specified in position_list
        for position in self.position_list['POSITIONS']:
            name = None

            ### Check if files are in directory
            for filename in self.filenames:
                if position['LABEL'] in filename:
                    name = filename
                    break

            ### Report missing file
            if name is None:
                raise ValueError('Missing image file', position['LABEL'])

            ### Create and append Tile object
            tile = Tile((position['GRID_COL'], position['GRID_ROW']), name)
            tile.rotate(180)
            self.tiles.append(tile)

        # Attribute for final stitched image
        self.stitched_img = np.array([])

    def stitch(self):
        '''Stitch the images specified in the PositionList file'''

        self.stitched_img = np.array([])


        # Ensure tiles are sorted
        self.tiles.sort(key = lambda x: x.col)
        self.tiles.sort(key = lambda  x: x.row)

        # Find number of rows and columns
        num_col = max(tile.col for tile in self.tiles) + 1
        num_row = max(tile.row for tile in self.tiles) + 1

        # Iteratively stitch images together into final image
        i = 0
        for row in range(num_row):
            row_img = np.array([])
            for col in range(num_col):
                assert self.tiles[i].col == col
                assert self.tiles[i].row == row
                row_img = np.hstack((row_img, self.tiles[i].img)) if row_img.size else self.tiles[i].img
                i = i + 1
            self.stitched_img = np.vstack((self.stitched_img, row_img)) if self.stitched_img.size else row_img

    def save(self, filename):
        cv2.imwrite(filename, self.stitched_img)


    def downsample(self, img):
        # Todo: implement

        return img



import imutils
class Tile():
    def __init__(self, pos, filename):
        self.col = pos[0]
        self.row = pos[1]
        self.name = filename

        self.img = self.load(self.name)

    def load(self, filename):
        return cv2.imread(filename, 0)

    def rotate(self, angle):
        self.img = imutils.rotate_bound(self.img, angle)