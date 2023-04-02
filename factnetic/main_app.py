#Import system libraries
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash
from dash import Dash, dcc, html, Input, Output, State, callback_context, callback, dash_table
import random
import string
import base64
import os
import pandas as pd
import plotly.express as px
'''
Building application high-level layout
High-level layout of the program includes the page header, tab menu, and a place holder for the tab specific layout

'''

# variable initialization

# df = pd.DataFrame()
df = px.data.election()
geojson = px.data.election_geojson()

def home_tab_layout():
    image_path = 'assets/icon_background.png'

    layout =[
                 dbc.Row(
                        html.Img(src=image_path)
                 )
    ]

    return layout

def first_tab_layout():
    layout = [
        #grid layout using row and col to place div accordingly
        dbc.Row([ #first row
                dbc.Col(
                            html.Div([
                                    dbc.Label('Location'),
                                    dcc.Dropdown(id='first_tab-location',
                                        options=[
                                                    {'label': 'India', 'value': 'india'},
                                                    {'label': 'Uniteed States of America', 'value': 'usa'},
                                                    {'label': 'Canada', 'value': 'canada'},
                                                    {'label': 'China', 'value': 'china'},
                                                    {'label': 'Russia', 'value': 'russia'},
                                                ],
                                        value=None,
                                        clearable=False
                                    ),
                                ]),width=2
                        ),

                dbc.Col(
                            html.Div([
                                    dbc.Label('Sentiment'),
                                    dcc.Dropdown(id='first_tab-sentiment',
                                        options= [
                                                    {'label': 'Positive', 'value': 'pos'},
                                                    {'label': 'Neutral', 'value': 'neu'},
                                                    {'label': 'Negative', 'value': 'neg'},
                                                ],
                                        value=None,
                                        clearable=False
                                    ),
                                ]),width=1
                        ), 

                dbc.Col(
                            html.Div([
                                    dcc.RadioItems(
                                                    id='candidate', 
                                                    options=["Joly", "Coderre", "Bergeron"],
                                                    value="Coderre",
                                                    inline=True
                                                ),
                                ]),width=2
                        ), 
                dbc.Col(
                            html.Div([
                                    dbc.Label('Graph switch'),
                                    daq.BooleanSwitch(
                                                        id = 'first_tab-graph_switch',
                                                        on=True,
                                                        className='dark-theme-control'
                                                    ),
                                ]),width=2
                        ),    
        
        ]),
        
        dbc.Row([ # 2nd row
                    # dbc.Col(
                    #             html.Div([
        
                                        
                    #                     dbc.Label('Data Report in table format'),

                    #                     html.Div([
                    #                                 dash_table.DataTable(
                    #                                     id='first_tab-reporting_datatable',
                    #                                     columns=[
                    #                                         {"name": i, "id": i} for i in df.columns
                    #                                     ],
                    #                                     data=df.to_dict('records'),
                    #                                     # filter_action="native",
                    #                                     sort_action="native",
                    #                                     sort_mode="multi",
                    #                                     column_selectable="single",
                    #                                     selected_columns=[],
                    #                                     selected_rows=[],
                    #                                     page_action="native",
                    #                                     page_current= 0,
                    #                                     page_size= 15,
                    #                                 ),
                    #                                 html.Div(id='datatable-interactivity-container')
                    #                             ])
                                        
                    #                 ]), width = 12
                    # ),
                    dbc.Col(
                                html.Div([

                                        dcc.Graph(id="first_tab-location_graph"),
                                    
                                    ]), width = 12
                    ),
                    dbc.Col(html.Div([]))
                    

        ]),
        
        dbc.Row([ # 3rd row - quality graph plot
        

        ]),

        dbc.Row([ # 4th row - quality dataframes
        

        ]),

        

    ]

    return layout
     
encoded_image2 = base64.b64encode(open('assets/icon_png_2.png', 'rb').read())

app = Dash(    __name__, 
                external_scripts     = ["https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"],
                external_stylesheets = [dbc.themes.BOOTSTRAP]
                #,prevent_initial_callbacks=True

        )

app.title = "factnetic"
app.layout = html.Div([
    
    dbc.Row(
        dbc.Col(
            dbc.NavbarSimple(
                children=[
                        dbc.NavItem(dbc.NavLink("Help", href= "https://www.google.com/"
                                            )   
                                ),
                        dbc.NavItem(dbc.NavLink("Feedback", href= ""
                                            )   
                                ),        
                        dbc.NavItem(dbc.NavLink("Email Us", href= "mailto: "
                                                ),
                        ),
                        html.Img(title = "factnetic",height="30px", width = "136px", src='data:image/png;base64,{}'.format(encoded_image2.decode())),

                
                ],
                brand='factnetic',
                
                fluid = True, #makes the heading and the elements of the navigatio bar to stick to the extreme sides respectively
                brand_href='#',
                color='grey',
                dark = True,
            ),align="right", width=12
        )
    ),

    dbc.Row(html.P()),
    dbc.Row(
        dbc.Tabs(
            [   
                dbc.Tab(label='Home', tab_id='home_tab'),
                dbc.Tab(label='Data reporting', tab_id='first_tab'),
                # dbc.Tab(label='EPS', tab_id='eps-tab'),
            ],
            id='tab-menu', 
            active_tab='first_tab', 
        ),
    ),
    dbc.Row(html.P()),
    html.Div(id='tab-content')
])

@app.callback(
    
    Output('tab-content','children'),
    Input('tab-menu','active_tab'),
)

def display_tab(active_tab): 
    '''
    Function changes the page content based on the tab selected.
    Input: 
        active_tab: the tab_id of the selected tab
    
    Output:
        layout: the layout of the selected tab, will be injected into the tab-content Div.
    '''
    
    #Get the layout for the selected tab
    if active_tab == 'home_tab':
        layout = home_tab_layout()
    
    elif active_tab == 'first_tab':
        layout = first_tab_layout()

    return layout


@app.callback(
    Output("first_tab-location_graph", "figure"), 
    Input("candidate", "value"))
def display_choropleth(candidate):
    df = px.data.election() # replace with your own data source
    geojson = px.data.election_geojson()
    fig = px.choropleth(
        df, geojson=geojson, color=candidate,
        locations="district", featureidkey="properties.district",
        projection="mercator", range_color=[0, 6500])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

if __name__ == '__main__':
            
    app.run_server(debug=True, host='0.0.0.0', port=1001) #, use_reloader=False, dev_tools_ui=True)
        
        
