import math

def points_on_circle(x, y, radius):
    points = []
    for angle in range(0, 37):
        radian = math.radians(angle*10)
        
        point_x = int(x + radius * math.cos(radian))
        point_y = int(y + radius * math.sin(radian))

        points.append((point_x, point_y))
    return list(set(points))

def get_path_width(binary_image, points_on_path) -> int:
    path_length = len(points_on_path)
    mid_index = math.floor(path_length/2)
    midpoint = points_on_path[mid_index]
    x, y = midpoint[0], midpoint[1]
    
    for radius in range(1, 100): #soft cap on radius 100
        circle_points = points_on_circle(x, y, radius)
        for point in circle_points:
            if binary_image[point[0]][point[1]][0] == 0:
                return radius*2
    
    print("RADIUS NOT FOUND")
    return 1