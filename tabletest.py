import pandas as pd
import numpy as np
import plotly
from plotly.subplots import make_subplots
import dash
import dash_table
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
                                    id='mRoleChooser',
                                    options=[{'label': i, 'value': i} for i in ["Data Analyst","Network Engineer"]],
                                    value="Data Analyst"
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
                html.Div(
                    id="dtbl"
                )
            ])
        ])
    ])
])

@app.callback(
    Output("dtbl","children"),
    [Input("mRoleChooser","value"),
    Input("month_end","value")]
)
def get_table(role,end):
    if role =="Data Analyst":
        mdf=daDf
    else:
        mdf=netDf
    pos=list(mdf.columns).index(end)
    if pos>1:
        colname=list(mdf.columns)[pos-1]
    df=mdf[["Skill",colname,end]]
    df["% Change from previous month"]=df[end]-df[colname]
    df=df.drop([colname],axis=1)
    df=df.head(10)
    df=df.sort_values(end,ascending=False)
    tbl=dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
            style_data_conditional=[
                {
                    'if': {
                        'column_id': '% Change from previous month',
                        'filter_query': '{% Change from previous month} < 0'
                    },
                    'backgroundColor': '#f2b3ae',
                    'color': '#ff1300',
                    'font-weight': 'bold',
                    'font-family':'Roboto'
                },
                {
                    'if': {
                        'column_id': '% Change from previous month',
                        'filter_query': '{% Change from previous month} > 0'
                    },
                    'backgroundColor': '#97f098',
                    'color': '#008001',
                    'font-weight': 'bold',
                    'font-family':'Roboto'
                }                    
            ],
            style_data={ 'border': '0px solid blue',
                        'font-family':"Roboto",
                        'align':"left" },
            style_header={ 'border': '0px solid pink',
                            'font-weight': 'bold',
                            'font-family':"Roboto",
                            'align':"left" }
        )
    return tbl



if __name__ == "__main__":
    app.run_server(host="0.0.0.0")


