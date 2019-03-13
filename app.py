import dash
#from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import pandas as pd
import flask
from flask_cors import CORS
import os


'''
By Vivien Lee
iota Chapter Potential Alpha Delta Class
'''

df = pd.read_csv('chapters.csv',sep='|')
df.head()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                        "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                        "//fonts.googleapis.com/css?family=Dosis:Medium",
                        "https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css"]

app = dash.Dash(external_stylesheets=external_stylesheets)

for css in external_stylesheets:
    app.css.append_css({"external_url": css})

server = app.server

df['text'] = '<br>' + df['Chapter'] + '<br>' + df['Status'] + '<br><br><b>' + df['Campus'] + '</b><br>' + df['Location'] + '<br>Region: ' + df['Region']

data = [ dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df['long'],
        lat = df['lat'],
        hoverinfo = 'text',
        text = df['text'],
        customdata = df['Campus'],
        mode = 'markers',
        marker = dict(
            size = 6,
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
        height=550,
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showland = True,
            landcolor = "rgb(250, 250, 250)",
            subunitcolor = 'rgb(215, 0, 0)',
            countrycolor = "rgb(255, 255, 255)",
            countrywidth = 0.5,
            subunitwidth = 0.1
        ),
    )

fig = dict( data=data, layout=layout)
STARTING_SCHOOL = 'Cornell University'
CHAPTER = df.loc[df['Campus'] == STARTING_SCHOOL]['Chapter'].iloc[0]
STARTING_IMG = df.loc[df['Chapter'] == CHAPTER]['Image'].iloc[0]
STARTING_DATE = "Founded: " + df.loc[df['Chapter'] == CHAPTER]['Founding Date'].iloc[0]
STARTING_FACT = df.loc[df['Chapter'] == CHAPTER]['Fun Fact'].iloc[0]


app.layout  = html.Div(children=[

    html.Div(children=[
    html.Div('Kappa Phi Lambda', style={'color': 'white', 'fontSize': 30, 'font-family':'Helvetica', 'text-align':'center', "text-shadow":"rgba(0, 0, 0, 0.298039) 3px 3px 0px"}),
    html.Div('Chapters & Colonies', style={'color': 'white', 'fontSize': 20, 'font-family':'Helvetica', 'text-align':'center',"text-shadow":"rgba(0, 0, 0, 0.298039) 2px 2px 0px"})
    #html.Div('Chapters & Colonies', style={'width': '300px', 'float':'left', 'color': 'rgb(215, 0, 0)', 'fontSize': 24, 'font-family':'Lucida Console', 'text-align':'center'}),
    ], style={'padding':'110px 0','margin-left':'37.5%','backgroundImage':'url(https://www.onlygfx.com/wp-content/uploads/2017/07/watercolor-texture-red-5.jpg)','width':'340px','height':'77px','backgroundSize':'contain'}),

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
        style_cell={'fontWeight': 'lighter','textAlign': 'left', 'font-family':'Helvetica', 'fontSize':'16px','padding':'5px', 'width':'50px'},
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
        'backgroundColor': 'rgba(175, 37, 27, 0.93)',
        'color':'white',
        'fontWeight': 'normal'
        },
        n_fixed_rows=1,
        style_as_list_view=True,
        css=[{
        'selector': '.dash-cell div.dash-cell-value',
        'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        style_table={
        'maxHeight': '240',
        'overflowY': 'scroll'
        },
    )
    ], style={'width':'100%'}),

            html.Div(children=
            [
                dcc.Graph(id='graph', figure=fig),
            ],style={'float':'right',  'display': 'inline'}),

            html.Div([

                html.Br(),

                html.H4(STARTING_SCHOOL,
                id='chapter_name', style=dict(marginBottom='5px')),

                html.P(CHAPTER,
                id='chapter_letters',
                style=dict(fontSize='18px', marginBottom='2px', fontWeight='lighter')),

                html.P(STARTING_DATE,
                id='chapter_date',
                style=dict(fontSize='18px', marginBottom='15px',fontWeight='lighter')),

                html.P("Fun Fact!",
                style=dict(fontSize='15px', marginBottom='2px', color='rgba(175, 37, 27, 0.93)',fontWeight='lighter')),

                html.P(STARTING_FACT,
                id='chapter_fact',
                style=dict(fontSize='15px', marginBottom='15px',fontWeight='lighter' )),

                html.Img(id='chem_img', src=STARTING_IMG, style={'width':'500px', 'height':'auto', 'position': 'absolute', 'clip':'rect(0px,500px,350px,0px)'}),


            ], style={'max-width':'calc(100% - 900px)',  'display': 'inline', 'overflow-wrap': 'break-word', 'float':'left', 'left':'100px', 'font-family':'Helvetica'}),





], style={'backgroundColor':'white'})

def dfRowFromHover( hoverData ):
    ''' Returns row for hover point as a Pandas Series '''
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'pointNumber' in firstPoint:
                point_number = firstPoint['pointNumber']
                school_name = str(fig['data'][0]['text'][point_number]).strip()
                return df.loc[df['Campus'] == school_name]
    return pd.Series()

@app.callback(
    dash.dependencies.Output('chapter_name', 'children'),
    [dash.dependencies.Input('graph', 'hoverData')])
def return_chapter_name(hoverData):
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'customdata' in firstPoint:
                chapter = firstPoint['customdata']
                return chapter
    return STARTING_SCHOOL

@app.callback(
    dash.dependencies.Output('chapter_letters', 'children'),
    [dash.dependencies.Input('graph', 'hoverData')])
def return_chapter_name(hoverData):
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'customdata' in firstPoint:
                chapter = firstPoint['customdata']
                return df.loc[df['Campus'] == chapter]['Chapter'].iloc[0]
    return CHAPTER

@app.callback(
    dash.dependencies.Output('chapter_date', 'children'),
    [dash.dependencies.Input('graph', 'hoverData')])
def display_chapter(hoverData):
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'customdata' in firstPoint:
                chapter = firstPoint['customdata']
                return "Founded: " + df.loc[df['Campus'] == chapter]['Founding Date'].iloc[0]
    return STARTING_DATE

@app.callback(
    dash.dependencies.Output('chapter_fact', 'children'),
    [dash.dependencies.Input('graph', 'hoverData')])
def display_chapter(hoverData):
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'customdata' in firstPoint:
                chapter = firstPoint['customdata']
                return df.loc[df['Campus'] == chapter]['Fun Fact'].iloc[0]
    return STARTING_FACT

@app.callback(
    dash.dependencies.Output('chem_img', 'src'),
    [dash.dependencies.Input('graph', 'hoverData')])
def display_image(hoverData):
    if hoverData is not None:
        if 'points' in hoverData:
            firstPoint = hoverData['points'][0]
            if 'customdata' in firstPoint:
                chapter = firstPoint['customdata']
                return df.loc[df['Campus'] == chapter]['Image'].iloc[0]
    return STARTING_IMG


#server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
