### https://dash.plot.ly/datatable/callbacks



import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd



df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

def format_float(a, ndeci=3):
    """print float number to a given decimal place"""
    try:
        a = float(a)
        f_str = 'f"' + "{a:." + str(ndeci) + "f}" + '"'
        # print(f_str)
        return eval(f_str)
    except Exception:
        return a
        
df['gdpPercap'] = df['gdpPercap'].astype(float).fillna(0.0).apply(lambda x: format_float(x,3))
df['lifeExp'] = df['lifeExp'].astype(float).fillna(0.0).apply(lambda x: format_float(x,1))

# add index column
df[' index'] = range(1, len(df) + 1)

app = dash.Dash(__name__)

PAGE_SIZE = 10   # rows per page

app.layout = dash_table.DataTable(
    id='datatable-paging',
    columns=[
        {"name": i, "id": i } for i in sorted(df.columns)
    ],
    page_current=0,
    page_size=PAGE_SIZE,
    page_action='custom',

    sort_action='custom',
    sort_mode='multi',
    sort_by=[]
)


@app.callback(
    Output('datatable-paging', 'data'),             # set data key
    [Input('datatable-paging', "page_current"),     # input arg1 
     Input('datatable-paging', "page_size"),        # input arg2
     Input('datatable-paging', "sort_by")
     ]       
)
def update_table(page_current, page_size, sort_by):
    print(f"sort_by = {sort_by}")   # refresh page in browser will reset sort_by
    if len(sort_by):
        dff = df.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    else:
        # No sort is applied
        dff = df

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True, host = "127.0.0.1", port = 8050)