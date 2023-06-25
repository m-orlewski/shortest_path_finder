import matplotlib.pyplot as plt
import networkx as nx
from os.path import join


'''Function that draws the whole graph as well as the calculated path using different colors.

full_graph and positions represent a loaded map graph.
calc_path and positions represent a calculated shortest path.
filename, if set to any value, allows to save graph into filename.png file inside out_graphs catalog.
debug set to True displays nodes names/numbers and edges weights.
'''
def draw_path(full_graph: nx.Graph, calc_path: nx.Graph, positions, filename: str = None, debug: bool = False):
    # Make a subgraph containing only the path nodes
    H = full_graph.subgraph(calc_path)
    
    # Draw whole graph
    nx.draw_networkx_nodes(full_graph, pos=positions, node_color='gray')
    nx.draw_networkx_edges(full_graph, pos=positions, edge_color='black')
    
    # Draw shortest path
    nx.draw_networkx_nodes(H, pos=positions, node_color='orange')
    nx.draw_networkx_edges(H, pos=positions, edge_color='red')
    
    # Testing params
    if debug:
        # Draw edge weights
        edge_labels = nx.get_edge_attributes(full_graph, "weight")
        nx.draw_networkx_edge_labels(full_graph, positions, edge_labels)
        
        # Draw node labels
        nx.draw_networkx_labels(full_graph, positions, font_size=16, font_family="sans-serif")
    
    # Display (and save) the graph
    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    if filename:
        plt.savefig(join('out_graphs', f'{filename}.png'))
    plt.show()

'''Function that calculates shortest path and displays it (and saves to file).

full_graph and positions represent a loaded map graph.
start and end parameters can be either the number or a unique string value describing a node.
filename and debug parameters are passed to draw_path function.
'''
def find_and_draw_path(full_graph: nx.Graph, positions, start, end, filename: str = None, debug: bool = False):
    # Calculate shortest path from point to point
    length, calc_path = nx.bidirectional_dijkstra(full_graph, start, end)
    
    # Print route length
    print(f'Length of calculated route: {length}')
    
    # Draw graph and calculated path
    draw_path(full_graph, calc_path, positions, filename, debug)

# Main with functionality example
def main():
    # Graph from Michał will be here
    G = nx.Graph()
    G.add_edge('a', 'b', weight=0.6)
    G.add_edge('a', 'c', weight=0.2)
    G.add_edge('c', 'd', weight=0.1)
    G.add_edge('c', 'e', weight=0.7)
    G.add_edge('c', 'f', weight=0.9)
    G.add_edge('a', 'd', weight=0.3)
    
    # pos from Michał will be here
    pos = nx.spring_layout(G)
    
    # Magic time!
    find_and_draw_path(G, pos, 'b', 'd', 'test', True)

if __name__ == '__main__':
    main()
