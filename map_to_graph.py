import imageio as iio
import matplotlib.pyplot as plt
import cv2
from skimage import morphology
from skan import csr
import numpy as np

path = 'image_database/0.png'

## load and to grayscale
image = cv2.imread(path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# plt.imshow(image)
# plt.show()

## binarize
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# plt.imshow(binary, cmap='gray')
# plt.show()

## skeletonize
skeletonized = morphology.skeletonize(binary)
# plt.imshow(im_skeleton, cmap='gray')
# plt.show()

skeleton = csr.Skeleton(skeletonized)

nodes = {} # key: node number, value: (x_coord, y_coord)
edges = [] # (x, y) - nodes connected
c = 0
for i in range(skeleton.n_paths):
    path_coordinates = skeleton.path_coordinates(i)
    x1, y1 = path_coordinates[0][0], path_coordinates[0][1]
    x2, y2 = path_coordinates[-1][0], path_coordinates[-1][1]

    if (x1, y1) not in nodes.values():
        nodes[c] = (x1, y1)
        c += 1

    if (x2, y2) not in nodes.values():
        nodes[c] = (x2, y2)
        c += 1

    key_list = list(nodes.keys())
    val_list = list(nodes.values())

    pos1 = val_list.index((x1, y1))
    pos2 = val_list.index((x2, y2))

    edges.append((pos1, pos2))

print(nodes)
print()
print(edges)