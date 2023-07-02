import matplotlib.pyplot as plt
import cv2
from skimage import morphology
from skan import csr
from pathfinder import find_and_draw_path
from width_finder import get_path_width

path = 'image_database/0.png'

## load and to grayscale
image = cv2.imread(path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.imshow(gray, cmap='gray')
plt.show()

# ## binarize
_, binary = cv2.threshold(image, 175, 255, cv2.THRESH_BINARY)
# # _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 0)
plt.imshow(binary, cmap='gray')
plt.show()

# ## skeletonize
skeletonized = morphology.skeletonize(binary)
plt.imshow(skeletonized, cmap='gray')
plt.show()

skeleton = csr.Skeleton(skeletonized)

nodes = {} # key: node number, value: (x_coord, y_coord)
edges = [] # (x, y, w) - nodes connected + weight
c = 0
for i in range(skeleton.n_paths):
    path_coordinates = skeleton.path_coordinates(i)
    x1, y1 = path_coordinates[0][1], path_coordinates[0][0]
    x2, y2 = path_coordinates[-1][1], path_coordinates[-1][0]

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
    
    edge_weight = len(path_coordinates) / get_path_width(binary, path_coordinates)
    edges.append((pos1, pos2, edge_weight))

print(nodes)
print()
print(edges)

# Make ax with plot
_, ax = plt.subplots()
ax.imshow(skeletonized, cmap='gray')
# Get shortest path
find_and_draw_path(nodes, edges, skeleton, ax, 0, 37, 'test')
# Show the plot
plt.show()
