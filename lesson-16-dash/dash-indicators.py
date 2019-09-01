import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

file_csv = "https://gist.githubusercontent.com/chriddyp/cb5392c35661370d95f300086accea51/raw/8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/indicators.csv"
file_csv = 'indicators.csv'
df = pd.read_csv(file_csv)

_indicators = sorted(df['Indicator Name'].unique())
_years = sorted(df["Year"].unique())
_countries = sorted(df["Country Name"].unique())

app.layout = html.Div([
    html.Div([
        html.Label('Year',
            style={
                'textAlign': 'left',
                'color': 'red'
            }
        ),
        html.Div(
            dcc.Slider(
                id='year--slider',
                min=_years[0],
                max=_years[-1],
                value=_years[-1],
                marks={str(y): str(y) for y in _years},
                step=None
            )
        ),

        html.P("."),
        html.Label('Country',
            style={
                'textAlign': 'left',
                'color': 'red'
            }
        ),
        html.Div([
                dcc.Dropdown(
                    id='country-column',
                    options=[{'label': i, 'value': i} for i in _countries],
                    value=[i for i in _countries if i[:5] == 'China'][0]
                )
            ],
            style={'width': '100%', 'display': 'inline-block'}
        ),

        html.Label('Indicator',
            style={
                'textAlign': 'left',
                'color': 'red'
            }
        ),
        html.Div([
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in _indicators],
                    value=[i for i in _indicators if i[0] == 'F'][0]
                ),
                dcc.RadioItems(
                    id='xaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],
            style={'width': '45%', 'display': 'inline-block'}
        ),

        html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in _indicators],
                    value=[i for i in _indicators if i[:4] == 'Life'][0]
                ),
                dcc.RadioItems(
                    id='yaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ]
            ,style={'width': '40%', 'float': 'right', 'display': 'inline-block'}
        )


    ]),

    html.Label('Indicator-Correlation',
        style={
            'textAlign': 'left',
            'color': 'red'
        }
    ),
    html.Div(
        dcc.Graph(id='indicator-graphic'),
        style={'width': 1000}
    )
    




])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),  
     Input('country-column', 'value'),
     Input('year--slider', 'value')])
def update_graph(xaxis_column_name, 
                 yaxis_column_name,
                 xaxis_type, 
                 yaxis_type,
                 country_name,
                 year_value):
    dff = df[(df['Year'] == year_value) & (df['Country Name'] == country_name)]

    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type.lower() == 'linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type.lower() == 'linear' else 'log'
            },
            margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
