# starfind_example.py
# minimal example to run StarFinder
import pathlib
import numpy as np
from PIL import Image
from skimage import exposure
from asistarcalibration import starfinder

download_dir = pathlib.Path.cwd() / 'data'
filelist = list(download_dir.glob('*.png'))

imglist = list()
for file in filelist:
    im = Image.open(file)
    imglist.append(im)
img = np.mean(imglist, axis=0)
img_eq = exposure.equalize_hist(img)

time = np.datetime64('2025-01-03T03:27:00')
glat = 65.5
glon = -147.7

sf = starfinder.StarFinder(glat, glon, time)
#sf.load_stars('test_out.txt')
sf.find_stars(img_eq)
sf.save_starcal_file('test_out2.txt')
