import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output

import random
from collections import deque

app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H4('NYC Taxi & Limousine Commission data'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


X = deque(maxlen=20)
Y = deque(maxlen=20)
Z = deque(maxlen=20)
X.append(1)
Y.append(1)
Z.append(1)


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    global X
    global Y
    global Z

    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    
    X.append(X[-1]+1)
    Y.append(Y[-1]+(Y[-1]*random.uniform(-0.1,0.1)))
    Z.append(Z[-1]+(Z[-1]*random.uniform(-0.5,5)))

    fig.append_trace({
        'x': list(X),
        'y': list(Y),
        'name': 'X and Y',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)


    fig.append_trace({
        'x': list(X),
        'y': list(Z),
        'name': 'X and Z',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)