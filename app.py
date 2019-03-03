import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

'''
By Vivien Lee
iota Chapter Potential Alpha Delta Class
'''

df = pd.read_csv('chapters.csv')
df.head()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(external_stylesheets=external_stylesheets)

server = app.server

df['text'] = '<br>' + df['Chapter'] + '<br>' + df['Status'] + '<br><br><b>' + df['Campus'] + '</b><br>' + df['Location'] + '<br><br>Founded: ' + df['Founding Date'] + '<br>Region: ' + df['Region']

data = [ dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df['long'],
        lat = df['lat'],
        hoverinfo = 'text',
        text = df['text'],
        mode = 'markers',
        marker = dict(
            size = 10,
            opacity = 0.8,
            reversescale = True,
            symbol = df['symbol'],
            line = dict(
                width=1,
                color='rgba(102, 102, 102)'
            ),
            color = 'rgb(215, 0, 0)',

        ))]

layout = dict(
        #title = 'Kappa Phi Lambda<br>Chapters and Colonies',
        colorbar = True,
        autosize=False,
        width=900,
        height=600,
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = 'rgb(215, 0, 0)',
            countrycolor = "rgb(217, 217, 217)",
            countrywidth = 0.5,
            subunitwidth = 0.1
        ),
    )

fig = dict( data=data, layout=layout )

app.layout  = html.Div(children=[

    html.Div('Kappa Phi Lambda', style={'color': 'rgb(215, 0, 0)', 'fontSize': 36, 'font-family':'Lucida Console', 'text-align':'center'}),
    html.Div('Chapters & Colonies', style={'color': 'rgb(215, 0, 0)', 'fontSize': 24, 'font-family':'Lucida Console', 'text-align':'center'}),
    #html.Div('Chapters & Colonies', style={'width': '300px', 'float':'left', 'color': 'rgb(215, 0, 0)', 'fontSize': 24, 'font-family':'Lucida Console', 'text-align':'center'}),

    html.Div(children=[
    dash_table.DataTable(
        id='table',
        columns=[{'name': 'Chapter', 'id': 'Chapter'},
                 {'name': 'Status', 'id': 'Status'},
                 {'name': 'Campus', 'id': 'Campus'},
                 {'name': 'Founding Date', 'id': 'Founding Date'},
                 {'name': 'Region', 'id': 'Region'},
             #{'name': 'Status', 'id': 'Status', 'hidden': True}
             ],
        data=df.to_dict("rows"),
        style_cell={'textAlign': 'left', 'font-family':'Lucida Console', 'padding':'5px', 'width':'50px'},
        style_cell_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
                }
        ] + [
            {
                'if': {'column_id': c},
                'textAlign': 'left'
                } for c in ['Date', 'Region']
        ],
        style_data={'whiteSpace': 'normal'},
        style_header={
        'backgroundColor': 'rgb(145, 0, 0)',
        'color':'white',
        #'fontWeight': 'bold'
        },
        n_fixed_rows=1,
        style_as_list_view=True,
        css=[{
        'selector': '.dash-cell div.dash-cell-value',
        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        style_table={
        'maxHeight': '600',
        'overflowY': 'scroll'
        },
    )
    ], style={'width':'calc(100% - 900px)', 'float':'left', 'left':'100px', 'font-family':'Lucida Console'}),
    html.Div(children=
        [
        dcc.Graph(id='graph', figure=fig),
    ],style={'width':'900px','float':'right'})
])

#server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
