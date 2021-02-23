import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
df = pd.read_excel('./yale/Summer_2019_Intern.xlsx'
    ,index_col=0
)

def generate_table(dataframe, max_rows=10):
    return html.Table(className='searchable sortable', children=
        [html.Tr([html.Th(col) for col in dataframe.columns])]
        +
        [html.Tr([
            html.Td(dataframe.iloc[ir][col]) for col in dataframe.columns
        ]) for ir in range(len(dataframe))]
)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    html.H4(children='Yale Interns'),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True, host = "127.0.0.1", port = 8050)