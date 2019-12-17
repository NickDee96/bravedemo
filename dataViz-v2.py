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




#def getDf():
#    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#    creds = ServiceAccountCredentials.from_json_keyfile_name('indeedscraper-f298f5bd5f02.json', scope)
#    client = gspread.authorize(creds)
#    sheet = client.open('Indeed Jds').sheet1
#    df=pd.DataFrame(sheet.get_all_records())
#    return df
#pRdf=getDf()


mapdata1=pd.read_csv("data/mapdata.csv")##Location data for US job data
mapdata2=pd.read_csv("data/ndLocData.csv")##Location data for African Indeed job data
df1=pd.read_csv("data/VectorizedTags3.csv")## A Vectorized tag dataFrame for US data
df2=pd.read_csv("data/data_net_vectorized.csv")## A Vectorized tag dataFrame for African Indeed job data
prdf2=pd.read_csv("data/pilotRoles.csv") ##Indeed API output with for US data
daDf=pd.read_csv("data/daSample.csv") ## Reduced skill percentages over time for Data Analyst
netDf=pd.read_csv("data/netSample.csv")## Reduced skill percentages over time for Network Engineer
plotdf=pd.read_csv("data/kmeans2.csv")## Loading the KMeans Output data
minDf=plotdf[["Role",'Cluster']]## subsetting the KMeans Data
r=list(df1["Role"].dropna().unique()) ##Getting the roles
df1=df1.fillna(0) #Replacing NaN with 0
df2=df2.fillna(0) #Replacing NaN with 0
r.sort() #Sorting the list from A-Z
r.remove("Amazon") # Removing the role AMAZON


def getRange(start,stop,srs):
    '''
    This function filters the skill count according to a predefined range
    '''
    sr1=srs[srs>=start].sort_values(ascending=False)
    sr1=sr1[sr1<=stop].sort_values(ascending=False)
    return sr1

def get_cluster_dict():
    '''
    This function filters the reduced KMeans dataFrame (minDf)  and returns the roles in according to their respective clusters
    '''
    clustDict=dict()
    for j in range(5):
        roles=list(minDf[minDf["Cluster"]==j]["Role"])
        clustDict.update({
            j:roles
        })
    return clustDict
clustDict=get_cluster_dict()
def get3dplot(plotdf):
    '''
    This function produces an interactive 3d KMeans plot.
    '''
    c0=plotdf[plotdf["Cluster"]==0]
    c1=plotdf[plotdf["Cluster"]==1]
    c2=plotdf[plotdf["Cluster"]==2]
    c3=plotdf[plotdf["Cluster"]==3]
    c4=plotdf[plotdf["Cluster"]==4]
    ## Cluster 1 
    trace1 = go.Scatter3d(
                        x = c1["PCA1_3D"],
                        y = c1["PCA2_3D"],
                        z = c1["PCA3_3D"],
                        mode="markers",
                        #line=dict(
                        #        color='#1f77b4',
                        #        width=4),
                        hovertext=c1.Role,
                        name = "Cluster 1",
                        marker = dict(color = 'rgba(110, 125, 125, 0.8)'),
                        text = None)
    ## Cluster 0
    trace0 = go.Scatter3d(
                        x = c0["PCA1_3D"],
                        y = c0["PCA2_3D"],
                        z = c0["PCA3_3D"],
                        mode = "markers",
                        hovertext=c0.Role,
                        name = "Cluster 0",
                        marker = dict(color = 'rgba(255, 30, 145, 0.8)'),
                        text = None)
    ## Cluster 2
    trace2 = go.Scatter3d(
                        x = c2["PCA1_3D"],
                        y = c2["PCA2_3D"],
                        z = c2["PCA3_3D"],
                        mode = "markers",
                        hovertext=c2.Role,
                        name = "Cluster 2",
                        marker = dict(color = 'rgba(0, 220, 250, 0.8)'),
                        text = None)
    ## Cluster 4
    trace4 = go.Scatter3d(
                        x = c4["PCA1_3D"],
                        y = c4["PCA2_3D"],
                        z = c4["PCA3_3D"],
                        mode = "markers",
                        hovertext=c4.Role,
                        name = "Cluster 4",
                        marker = dict(color = 'rgba(255, 220, 80, 0.8)'),
                        text = None)
    ## Cluster 3
    trace3 = go.Scatter3d(
                        x = c3["PCA1_3D"],
                        y = c3["PCA2_3D"],
                        z = c3["PCA3_3D"],
                        mode = "markers",
                        hovertext=c3.Role,
                        name = "Cluster 3",
                        text = None,
                        marker = dict(color = 'rgba(255, 80, 80, 0.8)'),
                        )
    data=[trace0,trace1,trace2,trace4,trace3]
    # Setting a clear background for the plot
    axis=dict(showbackground=False,
              showline=False,
              zeroline=False,
              showgrid=False,
              showticklabels=False,
              title=''
              )
    # Setting the layout options which includes its size.
    layout = go.Layout(
             plot_bgcolor='#273e49',
             showlegend=False,
             scene=dict(
                 xaxis=dict(axis),
                 yaxis=dict(axis),
                 zaxis=dict(axis),
            ),
            margin=go.layout.Margin(
                    l=0,
                    r=0,
                    b=0,
                    t=5,
                    pad=4
                )        
    )
    ## Combining the trace Data  and layout         
    fig = dict(data = data,layout=layout)
    ## Setting up the figure for rendering
    fig=go.Figure(fig)
    return fig

def get_color_codes(sdf):
    '''
    This function generates the color codes for Change and volatility in the table.
    '''
    change=[]
    vol=[]
    for i in range(len(sdf)):
        if sdf["% Change from previous month"][i]>0:
            change.append("#00DCFA")
        elif sdf["% Change from previous month"][i]<0:
            change.append("#FF1E91")
        else:
            change.append("#ffffff")
        if sdf.Volatility[i] <2.5:
            vol.append("#ffffff")
        elif (sdf.Volatility[i] >2.5) and (sdf.Volatility[i] <5):
            vol.append("#fc8403")
        else:
            vol.append("#FF1E91")
    mdict={"change":change,"volatility":vol}
    df=pd.DataFrame(mdict)
    df["skill"]="#ffffff"
    df["perc"]="#ffffff"
    return df







#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server
## Setting up the DashBoard layoute
app.layout = html.Div([
    html.Div([
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.H1(children="Brave Venture Labs",style={"color":"white"})
                    ])
                ])
            ]),    
        html.H1(
            children='''Data Exploration''',
            style={
                "font":"Roboto Regular",
                'text-align': 'center',
                "color":"#000000",
                "size":24
            }
        ),
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.H3(
                                    children="Role Category :",
                                    style={
                                        "font":"Roboto",
                                        'text-align': 'center',
                                        "color":"#09ACF7",
                                        "size":20
                                        }
                                    ),
                            ],width=4),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='Role Chooser',
                                    options=[{'label': i, 'value': i} for i in r],
                                    value='Data Analyst'                       
                                )
                                ],width=5)
                            ]),
                    ])
                ],width=7)
            ],justify="between"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Markdown(children='''
                                        **Sample Size**     :   15362 Job Descriptions  
                                        **Time Frame**      :   29/09/2018 ➤➤ 27/09/2019  
                                        **Date Crawled**    :   29/08/2019  
                                                ''')
                    ])
                ])                
            ],className="row mt-4"),
            dbc.Row([
                dbc.Col([
                        html.Div([
                            html.H3(
                                id="role_name",
                                style={
                                    "font":"Roboto",
                                    'text-align': 'left',
                                    "color":"#09ACF7",
                                    "size":20
                                    }
                                ),
                                html.Div([
                                    dcc.Graph(
                                        id="role_graph_table"
                                    )
                                ])

                        ],style={ "backgroundColor": "#ffffff"})
                ],width=9),
                dbc.Col([
                    html.Div([
                        html.H4(
                            children="Job titles Associated with the Role",
                                style={
                                   "font":"Roboto",
                                   'text-align': 'left',
                                   "color":"#09ACF7",
                                   "size":20
                                    }    
                        ),
                        html.Ul(
                            id="jobs_assoc"
                        )
                    ],style={ "backgroundColor": "#ffffff"})                
                ],width=3,align="stretch"),
            ],className="row mt-4"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H3(
                            id="role_name2",
                            style={
                                "font":"Roboto",
                                'text-align': 'left',
                                "color":"#09ACF7",
                                "size":20
                                }
                            ),                        
                        dcc.Graph(id="chloropleth")
                    ],style={ "backgroundColor": "#ffffff"})                
                ],width=6),
                dbc.Col([],width=3),
                dbc.Col([
                    html.Div([
                        html.H3(
                            children="Top Cities",
                                style={
                                   "font":"Roboto",
                                   'text-align': 'left',
                                   "color":"#09ACF7",
                                   "size":20
                                    }    
                            ),
                        html.Ul(
                            id="top_cities"
                        )            
                        ],style={ "backgroundColor": "#ffffff"})
                    ],width=3)
            ],className="row mt-4"),
            dbc.Row([            
                dbc.Col([
                    html.Div([
                        html.H3(
                            children="Roles similarity (3D clusters)",
                            style={
                                "font":"Roboto",
                                'text-align': 'left',
                                "color":"#09ACF7",
                                "size":20
                                }
                            ),
                        dcc.Graph(id="3dplot",
                            hoverData={"points": [{"hovertext": "Software Developer"}]},
                                figure=get3dplot(plotdf)) 
                    ],style={ "backgroundColor": "#ffffff"})            
                ],width=9),
                dbc.Col([
                    html.Div([
                        html.H3(
                            id="role_chosen",
                                style={
                                   "font":"Roboto",
                                   'text-align': 'left',
                                   "color":"#09ACF7",
                                   "size":20
                                    }    
                        ),
                        dcc.Markdown('''**Other Roles in the cluster.**'''),
                        html.Ul(
                            id="filtered_roles"
                        )
                    ])
                ],width=3,style={ "backgroundColor": "#ffffff"})
            ],className="row mt-4")        
        ])
    ],style={ "backgroundColor": "#ffffff"},className="container scalable")#,className="container scalable"
],className="row gs-header")
@app.callback(
    [Output("role_graph_table", 'figure'),
    Output("role_name", 'children'),
    Output("role_name2", 'children')],
    [Input("Role Chooser", 'value')])
def getFig(role):
    if (role=="Data Analyst") or (role=="Network Engineer"):
        df=df2
        a=df[df["Role"]==role].sum()
        a=a.drop("Role")
        a=a.drop("month")  
    else:
        df=df1
        a=df[df["Role"]==role].sum()
        a=a.drop("Role")
        a=a.drop("Job Title")    
    a=a.divide(len(df[df["Role"]==role]))*100
    a=getRange(10,100,a)
    sr1=a.apply(np.round)
    fig=make_subplots(    
        rows=1, cols=2,
        shared_xaxes=False,
        vertical_spacing=0.03,
        specs=[[{"type": "scatter"},{"type": "table"}]]
    )
    fig=fig.add_trace(go.Bar(
        x=sr1.index,
        y=list(sr1),
        marker_color="#FF1E91"
    ),row=1,col=1)
    if (role=="Data Analyst") or (role=="Network Engineer"):
        if role =="Data Analyst":
            mdf=daDf
        else:
            mdf=netDf
        pos=list(mdf.columns).index("September")
        if pos>1:
            colname=list(mdf.columns)[pos-1]
        sdf=mdf[["Skill",colname,"September","Volatility"]]
        sdf["% Change from previous month"]=sdf["September"]-sdf[colname]
        sdf=sdf.drop([colname],axis=1)
        coldf=get_color_codes(sdf)
        fig=fig.add_trace(go.Table(
            header=dict(
                values=["<b>Skills in demand this month <b>","<b>% of DB<b>","<b>% Change since last month<b>","<b>Change this year<b>"],
                font=dict(color="#ffffff",size=12),
                align="left",
                fill_color="slategray"
            ),
            cells=dict(
                values=[sdf.Skill.head(20),sdf.September.head(20),sdf["% Change from previous month"].head(20),sdf.Volatility.head(20)],
                align="left",
                fill_color=[coldf.skill.head(20),coldf.perc.head(20),list(coldf.change.head(20)),list(coldf.volatility.head(20))],#"#ffffff",
                font=dict(
                    size=12,
                    color="black")
            )
        ),row=1,col=2)        
    else:
        fig=fig.add_trace(go.Table(
            header=dict(
                values=["<b>Skill<b>","<b>Percentage<b>"],
                font=dict(color="#ffffff",size=14),
                align="left",
                fill_color="slategray"
            ),
            cells=dict(
                values=[list(sr1.index),list(sr1)],
                align="left",
                fill_color="#ffffff",
            )
        ),row=1,col=2)
    fig=fig.update_layout(
                margin=go.layout.Margin(
                    l=0,
                    r=0,
                    b=0,
                    t=35,
                    pad=4
                ),
                plot_bgcolor="#ffffff" ,
                paper_bgcolor="#ffffff"        
    )

    mainText1="Skills most in demand for {}".format(role)
    mainText2="Where is {} more in demand".format(role)
    return (fig,mainText1,mainText2)

@app.callback(
    Output("jobs_assoc", 'children'),
    [Input("Role Chooser", 'value')])
def get_assocJt(role):
    jts=list(prdf2[prdf2["Role"]==role]["jobtitle"].value_counts().index)[0:10]
    htm=[html.Li(x) for x in jts]
    return htm



@app.callback(
    Output("chloropleth", 'figure'),
    [Input("Role Chooser", 'value')])
def get_BubbleMap(role):
    '''
    This function produces a Bubble map  of job Occurence by city
    '''
    ##Separating African Data from US data
    if (role=="Data Analyst") or (role=="Network Engineer"):
        mapdata=mapdata2
        scp="africa" ## setting the plot scope
        fct=1 ## setting the magnification factor
    else:
        mapdata=mapdata1
        scp="usa" ## setting the plot scope
        fct=15 ## setting the magnification factor
    mapdf=mapdata[mapdata["Role"]==role] ## Filtering location Data
    fig=go.Figure() ##Initializing the figure
    fig=fig.add_trace(go.Scattergeo(    
            locationmode = 'USA-states',
            lon = mapdf['longitude'],
            lat = mapdf['latitude'],
            text = mapdf['City'],
            marker = dict(
                size = mapdf['Count']*fct,
                color ="#FF1E91"
            )
    )
    )
    fig=fig.update_layout(
            showlegend = False,
            geo = dict(
                scope = scp,
                landcolor = 'rgb(217, 217, 217)',
            ),
            margin=go.layout.Margin(
                    l=0,
                    r=0,
                    b=0,
                    t=0,
                    pad=4
                ),
            plot_bgcolor="#ffffff" ,
            paper_bgcolor="#ffffff"  
        )
    return fig



@app.callback(
    Output("top_cities", 'children'),
    [Input("Role Chooser", 'value')])
def get_top_cities(role):
    '''
    This function gets the top Cities for a given Role and returns a html ordered list
    '''
    if (role=="Data Analyst") or (role=="Network Engineer"):
        mapdata=mapdata2
    else:
        mapdata=mapdata1
    jts=list(mapdata[mapdata["Role"]==role].sort_values("Count",ascending=False).head(10)["City"])
    htm=[html.Li(x) for x in jts]
    return htm

@app.callback(
    [Output("role_chosen", 'children'),
    Output("filtered_roles", 'children')],
    [Input("3dplot", 'hoverData')])
def hoverDataShow(hoverData):
    point = hoverData["points"][0]
    clstr=int(minDf[minDf["Role"]==point["hovertext"]]["Cluster"])
    rls=clustDict[clstr]
    a=rls.remove(point["hovertext"])
    a=set(rls)
    rls.append(point["hovertext"])
    return (
        point["hovertext"],
        [html.Li(x) for x in a],
    )
if __name__ == "__main__":
    app.run_server(host="0.0.0.0",port=8080)