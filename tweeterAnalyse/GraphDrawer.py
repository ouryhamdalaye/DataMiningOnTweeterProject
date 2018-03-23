from plotly.graph_objs import *

import plotly.plotly as py
import networkx as nx
import matplotlib.pyplot as plt


class GraphDrawer(object):

    def __init__(self, type_graph):
        if type_graph == "digraph" :
            self.G = nx.DiGraph()
        else:
            self.G = nx.Graph()

    def add_nodes(self, df):
        self.G.add_nodes_from(df['userFromId'])

    def add_edged(self, df):
        temp = zip(df['userFromId'], df['userToId'])
        self.G.add_edges_from(temp)

    def draw_graph(self):
        nx.draw(self.G, pos=nx.spring_layout(G, k=.12), node_color='c', edge_color='k')

    def display_graph(self):
        plt.show()