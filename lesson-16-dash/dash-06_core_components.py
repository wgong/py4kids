# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go

from datetime import datetime as dt
import pandas as pd


df_solar = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

header_txt = """
Dash ships with supercharged components for interactive user interfaces. 
A core set of components, written and maintained by the Dash team, is available 
in the dash-core-components library.

The source on GitHub [plotly/dash-core-components](https://github.com/plotly/dash-core-components).

[Dash Sample Apps](https://github.com/plotly/dash-sample-apps)

"""



app.layout = html.Div([
    html.H4('Dash Core Components'),
    dcc.Markdown(children=header_txt),
    html.Div(className='container', children=[

        html.Div(className='container', children=[
            html.Label('URL', style={'color': 'red', 'fontSize': 18}),
            dcc.Link('Dash Core Components User Guide', href='https://dash.plot.ly/dash-core-components')
        ]),

        html.Label('Dropdown', style={'color': 'red', 'fontSize': 18}),
        dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': u'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SFO'}
            ],
            value='SFO'   # default
        ),

        html.Label('Multi-Select Dropdown', style={'color': 'red', 'fontSize': 18}),
        dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': u'Montréal', 'value': 'MTL'},
                {'label': u'上海', 'value': 'PVG'},
                {'label': 'San Francisco', 'value': 'SFO'}
            ],
            value=['PVG', 'SFO'],
            multi=True
        ),

        html.Label('Radio Items', style={'color': 'red', 'fontSize': 18}),
        dcc.RadioItems(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': u'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SFO'}
            ],
            value='SFO'
        ),

        html.Label('Checkboxes', style={'color': 'red', 'fontSize': 18}),
        dcc.Checklist(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': u'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SFO'}
            ],
            value=['MTL', 'SFO']
        ),

        html.Label('Text Input', style={'color': 'red', 'fontSize': 18}),
        dcc.Input(value='Dash is cool', type='text'),
        html.Br(),
        dcc.Link('More examples on Text Input types', href='https://dash.plot.ly/dash-core-components/input'),

        html.Label('Textarea', style={'color': 'red', 'fontSize': 18}),
        dcc.Textarea(
            placeholder='Enter a value...',
            value='This is a TextArea component',
            style={'width': '100%'}
        ),

        html.Label('DatePicker-Single', style={'color': 'red', 'fontSize': 18}),
        html.Div(
            dcc.DatePickerSingle(
            id='date-picker-single',
            date=dt(1997, 10, 1))
        ),

        html.Label('DatePicker-Range', style={'color': 'red', 'fontSize': 18}),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=dt(1997, 5, 3),
            end_date_placeholder_text='Select a date!'
        ),       

        html.Label("Markdown", style={'color': 'red', 'fontSize': 18}),
        dcc.Markdown('''
        #### Dash and Markdown

        Dash supports [Markdown](http://commonmark.org/help).

        Markdown is a simple way to write and format text.
        It includes a syntax for things like **bold text** and *italics*,
        [links](http://commonmark.org/help), inline `code` snippets, lists,
        quotes, and more.
        '''),

        html.Label('Button', style={'color': 'red', 'fontSize': 18}),
        dcc.Input(id='input-box', type='text'),
        html.Button('Submit', id='button'),
        html.Div(id='output-container-button',
                children='Enter a value and press submit'),

        html.Label('Dash Table', style={'color': 'red', 'fontSize': 18}),
        dash_table.DataTable(
            id='dash_table_1',
            columns=[{"name": i, "id": i} for i in df_solar.columns],
            data=df_solar.to_dict("rows"),
        ),


        html.Label('Graph', style={'color': 'red', 'fontSize': 18}),
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                        2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                        y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                        350, 430, 474, 526, 488, 537, 500, 439],
                        name='Rest of world',
                        marker=go.bar.Marker(
                            color='rgb(55, 83, 109)'
                        )
                    ),
                    go.Bar(
                        x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                        2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                        y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                        299, 340, 403, 549, 499],
                        name='China',
                        marker=go.bar.Marker(
                            color='rgb(26, 118, 255)'
                        )
                    )
                ],
                layout=go.Layout(
                    title='US Export of Plastic Scrap',
                    showlegend=True,
                    legend=go.layout.Legend(
                        x=0,
                        y=1.0
                    ),
                    margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                )
            ),
            style={'height': 300},
            id='my-graph'
        ),

        html.Label('Slider', style={'color': 'red', 'fontSize': 18}),
        dcc.Slider(
            min=0,
            max=9,
            marks={i: 'Label {}'.format(i) if i < 1 else str(i) for i in range(0, 6)},
            value=5,
        ),


     ], style={'columnCount': 1})   
])

@app.callback(
    dash.dependencies.Output('output-container-button', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def button_cb(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        (value or ""),
        n_clicks
    )


if __name__ == '__main__':
    app.run_server(debug=True, host = "127.0.0.1", port = 8050)