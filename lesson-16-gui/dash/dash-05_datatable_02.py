### https://dash.plot.ly/datatable/callbacks

import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# add index column
df[' index'] = range(1, len(df) + 1)

app = dash.Dash(__name__)

PAGE_SIZE = 10   # rows per page

app.layout = dash_table.DataTable(
    id='datatable-paging',
    columns=[
        {"name": i, "id": i} for i in sorted(df.columns)
    ],
    page_current=0,
    page_size=PAGE_SIZE,
    page_action='custom'
)


@app.callback(
    Output('datatable-paging', 'data'),             # set data key
    [Input('datatable-paging', "page_current"),     # input arg1 
     Input('datatable-paging', "page_size")])       # input arg2
def update_table(page_current,page_size):
    return df.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True, host = "127.0.0.1", port = 8050)