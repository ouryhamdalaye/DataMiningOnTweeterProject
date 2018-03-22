import plotly.plotly as py
from plotly.graph_objs import *

import networkx as nx
import pandas as pd
from test3functions import *

import matplotlib.pyplot as plt

df = pd.read_csv('dfCommunity_backup.csv')

# Convert user ID from float to integer.
df.userFromId=df.userFromId.apply(lambda x: int(x))
df.userToId=df.userToId.apply(lambda x: int(x))

# how to make links
# print(list(zip(df['userFromId'],df['userToId'])))

G = nx.DiGraph()
#G = nx.Graph()
G.add_nodes_from(df['userFromId'])
# G.add_edges_from(zip(df['userFromId'],df['userToId']))

# print(dfLookup)

# combine userFromId to userToId
temp = zip(df['userFromId'],df['userToId'])
# print(list(temp))
G.add_edges_from(temp)
# print(G.edges())

# Give nodes their Usernames
dfLookup = df[['userFromName','userFromId']].drop_duplicates()

# print(dfLookup)

dfLookup.head()
for userId in dfLookup['userFromId']:
    temp = dfLookup['userFromName'][df['userFromId'] == userId]
    # print(str(userId) + " " + str(temp))
    G._node[userId]['userName'] = temp.values[0]
    print(G._node)

# print(G.nodes())

# print(G.edges())

nx.draw(G, pos=nx.spring_layout(G,k=.12), node_color='c', edge_color='k')


# Get a list of all nodeID in ascending order
nodeID = G.node.keys()
sortedNodeID = sorted(nodeID)
print(sortedNodeID)

inScore = G.in_degree()
outScore = G.out_degree()
centralScore = nx.betweenness_centrality(G)
print(G.degree)

# Node label information available on hover. Note that some html tags such as line break <br> are recognized within a string.
labels = []

# plt.show()
for nd in nodeID:
      labels.append(G.node[nd]['userName'] + "<br>" + "Followers: " + str(inScore[nd]) + "<br>" + "Following: " + str(outScore[nd]) + "<br>" + "Centrality: " + str("%0.3f" % centralScore[nd]))

print(labels)

trace1 = scatter_nodes(pos=nx.spring_layout(G,k=.12), nodeID=sortedNodeID,centralScore=nx.betweenness_centrality(G))
trace2 = scatter_edges(G=G, pos=nx.spring_layout(G,k=.12))


width = 600
height = 600
axis = dict(showline=True,  # hide axis line, grid, ticklabels and  title
            zeroline=True,
            showgrid=True,
            showticklabels=True,
            title='test'
            )
layout = Layout(title='#EdTechChat Community on Twitter',
                font=Font(),
                showlegend=True,
                autosize=False,
                width=width,
                height=height,
                xaxis=dict(
                    title='Dec 14, 2015 9-10 p.m. EST, #EdTechChat #NETP16   www.techpoweredmath.com',
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

data = Data([trace1, trace2])

fig = Figure(data=data, layout=layout)
fig['layout'].update(annotations=make_annotations(nx.spring_layout(G,k=.12), labels, 14, 'rgb(25,25,25)', sortedNodeID))
#plt.show()
py.sign_in('ouryhamdalaye', '4fqmYw6dJn71wiF7U5wY')
py.plot(fig, filename='test')
"""
"""