import plotly.graph_objects as go


import numpy as np

# Data
x = np.linspace(0, 10, 1000)
y = np.sin(x)

# Create a trace

trace = go.Scatter(x=x, y=y, mode='lines')

# Create a figure

layout = go.Layout(title='Smooth Sine Wave', xaxis=dict(title='X axis'), yaxis=dict(title='Y axis'))
fig = go.Figure(data=[trace], layout=layout)
 

# Show figure
fig.show()