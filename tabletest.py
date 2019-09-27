import pandas as pd
import numpy as np
import plotly
from plotly.subplots import make_subplots
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import dash_bootstrap_components as dbc


daDf=pd.read_csv("daSample.csv")
netDf=pd.read_csv("netSample.csv")

daDf.columns

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout=html.Div([
    html.Div([
        html.H1(
            children="Table test"
        )
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            dcc.Dropdown(                                
                                    id='month_start',
                                    options=[{'label': i, 'value': i} for i in daDf.columns ],
                                    value='January'
                            )
                        ])
                    ]),
                    dbc.Col([
                        html.Div([
                            dcc.Dropdown(                              
                                    id='month_end',
                                    options=[{'label': i, 'value': i} for i in daDf.columns ],
                                    value='September'                                
                            )
                        ])
                    ])
                ]),
                html.Div([
                    [html.P(children=x)for x in daDf.Skill]
                ])
            ])
        ])
    ])
])

if __name__ == "__main__":
    app.run_server(host="0.0.0.0")


