import cv2
import numpy as np
import random
import math

SEED = "ABC"

# Number of lines per single image
NO_OF_LINES = (6, 10)

# Width (and height) of generated image
WIDTH = 1000

BACKGROUND_COLORS = [
    (34, 139, 34),
    (53, 94, 59),
    (79, 121, 66),
    (103, 146, 103),
    (0, 168, 107),
    (0, 0, 0)
]

BACKGROUND_CIRCLE_MAX_SIZE = 150
BACKGROUND_CIRCLE_COUNT = 50

ROAD_COLORS = [
    (255, 255, 255),
    (237, 234, 222),
    (249, 246, 238),
    (255, 255, 240),
    (255, 245, 238),
    (252, 245, 229),
    (224, 224, 224),
    (192, 192, 192),
]

# Path where to save generated images
# Must be created before running the script
IMAGE_PATH = 'image_database/'

# Number of images in total
IMAGE_COUNT = 1

random.seed(SEED)

def calculate_angle(point1, common_point, point2):
    vector1 = (point1[0] - common_point[0], point1[1] - common_point[1])
    vector2 = (point2[0] - common_point[0], point2[1] - common_point[1])

    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    norm1 = math.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
    norm2 = math.sqrt(vector2[0] ** 2 + vector2[1] ** 2)

    cosine_angle = dot_product / (norm1 * norm2)
    intersection_angle = math.acos(cosine_angle)
    return math.degrees(intersection_angle)

# Create a set of lines connected lines that are used as roads
def create_road_set():
    data = []
    prev_x = random.randint(0, WIDTH)
    prev_y = random.randint(0, WIDTH)

    current_x = random.randint(0, WIDTH)
    current_y = random.randint(0, WIDTH)

    line_number = random.randint(NO_OF_LINES[0], NO_OF_LINES[1])
    for _ in range(line_number):
        next_x = random.randint(0, WIDTH)
        next_y = random.randint(0, WIDTH)
        thicc = random.randint(2, 10)
        angle = calculate_angle((prev_x, prev_y), (current_x, current_y), (next_x, next_y))
        while math.fabs(angle) < 80:
            #print(f"Bad angle {angle}")
            next_x = random.randint(0, WIDTH)
            next_y = random.randint(0, WIDTH)
            angle = calculate_angle((prev_x, prev_y), (current_x, current_y), (next_x, next_y))

        #print(angle)
        line = [current_x, current_y, next_x, next_y, thicc]
        data.append(line)
        prev_x, prev_y = current_x, current_y
        current_x, current_y = next_x, next_y
    return data


# Create background based on seed
def create_background(img):
    img[:] = BACKGROUND_COLORS[0]
    for i in range(BACKGROUND_CIRCLE_COUNT):
        x = random.randint(0, WIDTH)
        y = random.randint(0, WIDTH)
        size = random.randint(50, BACKGROUND_CIRCLE_MAX_SIZE)
        color = random.choice(BACKGROUND_COLORS)
        img = cv2.circle(img, (x,y), size, color, cv2.FILLED)
        img = cv2.blur(img, (70, 70))
    return img


# Draw line (road) based on given input data
def draw_line(img, line):
    x1, y1, x2, y2, thickness = line
    color = random.choice(ROAD_COLORS)
    img = cv2.line(img, (x1, y1), (x2, y2), color, thickness)
    return img


# Creates and saves a complete image
def create_single_image(name=""):
    # Initialize empty image
    image = np.zeros((WIDTH, WIDTH, 3), np.uint8)

    # Create sample background for the image
    image = create_background(image)

    # Create a set of roads
    # Paint the roads onto the image
    for _ in range(2):
        lines = create_road_set()
        for line in lines:
            image = draw_line(image, line)

    if name == "":
        return image 
    # Posprocess and save
    # image = cv2.blur(image, (2, 2))
    else:
        print(f'{IMAGE_PATH}{name}.png')
        cv2.imwrite(f'{IMAGE_PATH}{name}.png', image)


if __name__ == "__main__":
    for i in range(IMAGE_COUNT):
        create_single_image(i)
