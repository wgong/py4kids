import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

file_csv = "https://gist.githubusercontent.com/chriddyp/cb5392c35661370d95f300086accea51/raw/8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/indicators.csv"
file_csv = 'indicators.csv'
df = pd.read_csv(file_csv)

countries = sorted(df["Country Name"].unique())

app.layout = html.Div([
    dcc.Dropdown(
        id='country',
        options=[{'label': i, 'value': i} for i in countries],
        value=[i for i in countries if i[:5] == 'China'][0]
    ),
    html.Div(id='my-div')
])


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='country', component_property='value')]
)
def update_output_div(input_value):
    return 'Country: "{}"'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug=True)
