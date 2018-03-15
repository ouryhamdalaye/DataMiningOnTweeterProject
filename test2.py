import plotly.plotly as py
from plotly.graph_objs import *

import networkx as nx
import pandas as pd
from test3functions import *

import matplotlib.pyplot as plt

df = pd.read_csv('dfCommunity.csv')

# Convert user ID from float to integer.
df.userFromId=df.userFromId.apply(lambda x: int(x))
df.userToId=df.userToId.apply(lambda x: int(x))

#G = nx.DiGraph()
G = nx.Graph()
G.add_nodes_from(df['userFromId'])
#G.add_edges_from(zip(df['userFromId'],df['userToId']))

# combine userFromId to userToId
temp = zip(df['userFromId'],df['userToId'])
# print(list(temp))
G.add_edges_from(temp)

# Give nodes their Usernames
dfLookup = df[['userFromName','userFromId']].drop_duplicates()

dfLookup.head()
for userId in dfLookup['userFromId']:
    temp = dfLookup['userFromName'][df['userFromId'] == userId]
    G._node[userId]['userName'] = temp.values[0]


# print(dfLookup)


nx.draw(G, pos=nx.spring_layout(G,k=.12), node_color='c', edge_color='k')

# Get a list of all nodeID in ascending order
nodeID = G._node.keys()
sortedNodeID = sorted(nodeID)
print(sortedNodeID)

inScore = G.degree
outScore = G.degree
centralScore = nx.betweenness_centrality(G)

# Node label information available on hover. Note that some html tags such as line break <br> are recognized within a string.
labels = []

for nd in nodeID:
      labels.append(G.node[nd]['userName'] + "<br>" + "Followers: " + str(inScore[nd]) + "<br>" + "Following: " + str(outScore[nd]) + "<br>" + "Centrality: " + str("%0.3f" % centralScore[nd]))

trace1 = scatter_nodes(nx.spring_layout(G,k=.12), None, 'rgb(152, 0, 0)', 8, 1, sortedNodeID, nx.betweenness_centrality(G))
trace2 = scatter_edges(G, nx.spring_layout(G,k=.12), '#a3a3c2', 1, 0.2)

width = 600
height = 600
axis = dict(showline=False,  # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title=''
            )
layout = Layout(title='#EdTechChat Community on Twitter',
                font=Font(),
                showlegend=False,
                autosize=False,
                width=width,
                height=height,
                xaxis=dict(
                    title='Dec 14, 2015 9-10 p.m. EST, #EdTechChat #NETP16   www.techpoweredmath.com',
                    titlefont=dict(
                        size=14,
                        color='#7f7f7f'),
                    showline=False,
                    showticklabels=False,
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

data = Data([trace1, trace2])

fig = Figure(data=data, layout=layout)
fig['layout'].update(annotations=make_annotations(nx.spring_layout(G,k=.12), labels, 14, 'rgb(25,25,25)', sortedNodeID))
plt.show()
py.sign_in('ouryhamdalaye', '4fqmYw6dJn71wiF7U5wY')
py.iplot(fig, filename='test')
