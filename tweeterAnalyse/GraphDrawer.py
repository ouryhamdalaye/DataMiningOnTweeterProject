from plotly.graph_objs import *

import plotly.plotly as py
import networkx as nx
import matplotlib.pyplot as plt
from config.private_config_data import *


class GraphDrawer(object):

    def __init__(self, type_graph):
        if type_graph == "digraph" :
            self.G = nx.DiGraph()
        else:
            self.G = nx.Graph()
        self.sortedNodeID = []
        self.inScore = []
        self.outScore = []
        self.centralScore = []
        self.labels = []
        self.pos = []
        self.node_color = 'b'
        self.edge_color = 'k'

    def add_nodes(self, df):
        self.G.add_nodes_from(df['userFromId'])
        self.sortedNodeID = sorted(self.G.node.keys())

    def define_pos(self):
        self.pos = nx.spring_layout(self.G, k=.12)

    def add_edges(self, df):
        temp = zip(df['userFromId'], df['userToId'])
        self.G.add_edges_from(temp)

        self.inScore = self.G.in_degree()
        self.outScore = self.G.out_degree()
        self.centralScore = nx.betweenness_centrality(self.G)
        self.define_pos()

    def draw_graph(self):
        nx.draw(self.G, pos=self.pos, node_color=self.node_color, edge_color=self.edge_color)

    def display_graph(self):
        plt.show()

    """
    Node label information available on hover.
    Note that some html tags such as line break <br> are recognized within a string.
    """
    def get_node_labels(self):
        labels = []

        for nd in self.sortedNodeID:
            labels.append(
                self.G.node[nd]['userName'] + "<br>" + "Followers: " + str(self.inScore[nd]) + "<br>" + "Following: " + str(
                    self.outScore[nd]) + "<br>" + "Centrality: " + str("%0.3f" % self.centralScore[nd]))

        return labels

    """
    # pos is the dict of node positions
    # labels is a list  of labels of len(pos), to be displayed when hovering the mouse over the nodes
    # color is the color for nodes. When it is set as None the Plotly default color is used
    # size is the size of the dots representing the nodes
    # opacity is a value between [0,1] defining the node color opacity
    """
    def scatter_nodes(self, color='rgb(152, 0, 0)', size=8, opacity=1):

        trace = Scatter(x=[],
                        y=[],
                        mode='markers',
                        marker=Marker(
                            showscale=True,
                            # colorscale options
                            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
                            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
                            colorscale='Hot',
                            reversescale=True,
                            color=[],
                            size=10,
                            colorbar=dict(
                                thickness=15,
                                title='Betweeenness Centrality',
                                xanchor='left',
                                titleside='right'
                            ),
                            line=dict(width=2)))
        for nd in self.sortedNodeID:
            trace['x'].append(self.pos[nd][0])
            trace['y'].append(self.pos[nd][1])
            trace['marker']['color'].append(self.centralScore[nd])

        # a dict of Plotly node attributes
        attrib = dict(name='', text=self.labels, hoverinfo='text', opacity=opacity)

        # concatenate the dict trace and attrib
        trace = dict(trace, **attrib)

        trace['marker']['size'] = size

        return trace

    def scatter_edges(self, line_color='#a3a3c2', line_width=1, opacity=.2):
        trace = Scatter(x=[],
                        y=[],
                        mode='lines',
                        )
        for edge in self.G.edges():
            trace['x'] += [self.pos[edge[0]][0], self.pos[edge[1]][0], None]
            trace['y'] += [self.pos[edge[0]][1], self.pos[edge[1]][1], None]
            trace['hoverinfo'] = 'none'
            trace['line']['width'] = line_width
            if line_color is not None:  # when it is None a default Plotly color is used
                trace['line']['color'] = line_color
        return trace

    def make_annotations(self, text, font_size=14, font_color='rgb(25,25,25)'):
        L = len(self.pos)
        if len(text) != L:
            raise ValueError('The lists pos and text must have the same len')
        annotations = Annotations()
        for nd in self.sortedNodeID:
            annotations.append(
                Annotation(
                    text="",
                    x=self.pos[nd][0], y=self.pos[nd][1],
                    xref='x1', yref='y1',
                    font=dict(color=font_color, size=font_size),
                    showarrow=False)
            )
        return annotations

    @staticmethod
    def config_plotly(width=600, height=600):
        axis = dict(showline=True,  # hide axis line, grid, ticklabels and  title
                    zeroline=True,
                    showgrid=True,
                    showticklabels=True,
                    title='test'
                    )
        layout = Layout(title='Community on Twitter',
                        font=Font(),
                        showlegend=True,
                        autosize=False,
                        width=width,
                        height=height,
                        xaxis=dict(
                            title='Communities',
                            titlefont=dict(
                                size=14,
                                color='#7f7f7f'),
                            showline=False,
                            showticklabels=True,
                            zeroline=False
                        ),
                        yaxis=YAxis(axis),
                        margin=Margin(
                            l=40,
                            r=40,
                            b=85,
                            t=100,
                            pad=0,

                        ),
                        hovermode='closest',
                        plot_bgcolor='#EFECEA',  # set background color
                        )
        return layout

    def create_iplot(self, trace1, trace2):
        data = Data([trace1, trace2])
        fig = Figure(data=data, layout=GraphDrawer.config_plotly())
        # fig['layout'].update(
          #  annotations=self.make_annotations(text=self.labels))
        py.sign_in(username=username, api_key=api_key)
        py.plot(fig, filename='test')
