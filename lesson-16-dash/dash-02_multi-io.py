import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Label("x"),
    dcc.Input(
        id='num_x',
        type='number',
        value=2
    ),
    html.Label("y"),
    dcc.Input(
        id='num_y',
        type='number',
        value=4
    ),
    html.Table([
        html.Tr([html.Td(['x+y']), html.Td(id='x+y')]),
        html.Tr([html.Td(['x-y']), html.Td(id='x-y')]),
        html.Tr([html.Td(['x*y']), html.Td(id='x*y')]),
        html.Tr([html.Td(['x/y']), html.Td(id='x/y')]),
        html.Tr([html.Td(['x', html.Sup('y')]), html.Td(id='x^y')]),
    ]),
])


@app.callback(
    [Output('x+y', 'children'),
     Output('x-y', 'children'),
     Output('x*y', 'children'),
     Output('x/y', 'children'),
     Output('x^y', 'children')],
    [Input('num_x', 'value'),
     Input('num_y', 'value')])
def callback_a(x, y):
    return x+y, x-y, x*y, x/y, x^y


if __name__ == '__main__':
    app.run_server(debug=True, host = "127.0.0.1", port = 8050)
