from Stitcher import Stitcher

# .pos file specifying the names of the tile images
position_list_filename = '/home/sihao/SchultzBox/Sihao/Imaging/050618Grid_stack/050618aaPositionList.pos'

# Create Stitcher object
s = Stitcher(position_list_filename)

# Stitch and save
s.stitch()
s.save('stitched.png')
