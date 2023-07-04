from glob import glob
import imageio as iio

files = glob('image_database/*.png')
image0 = iio.v2.imread(files[0], format='png')

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.imshow(image0, cmap='gray');