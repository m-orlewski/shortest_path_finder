import matplotlib.pyplot as plt
import networkx as nx
from os.path import join
from skan import csr

'''Function that calculates shortest path (and saves to file).

nodes - dictionary of nodes - key: node number, value: (x_coord, y_coord).
edges - list of edges with weights - (x, y, w) - nodes connected + weight.
skeleton - skeleton of path to be used for drawing.
axis - axis used to draw a path on.
start - node number for a path's start node.
end - node number for a path's end node.
filename - if given, saves image to a file in out_graphs.
'''
def find_and_draw_path(nodes: dict, edges: list, skeleton: csr.Skeleton, axis: plt.Axes, start: int, end: int, filename: str = None):
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    length, calc_path = nx.bidirectional_dijkstra(G, start, end)
    print(f'--- Shortest path ({length}): {calc_path}')

    val_list = list(nodes.values())
    for j in range(len(calc_path)-1):
        for i in range(skeleton.n_paths):
            path_coordinates = skeleton.path_coordinates(i)
            x1, y1 = path_coordinates[0][1], path_coordinates[0][0]
            x2, y2 = path_coordinates[-1][1], path_coordinates[-1][0]

            pos1 = val_list.index((x1, y1))
            pos2 = val_list.index((x2, y2))
            if pos1 == calc_path[j] and pos2 == calc_path[j+1]:
                axis.plot(path_coordinates[:,1], path_coordinates[:,0], color='red')
    if filename:
        plt.savefig(join('out_graphs', f'{filename}.png'))
