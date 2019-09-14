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




#def getDf():
#    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#    creds = ServiceAccountCredentials.from_json_keyfile_name('indeedscraper-f298f5bd5f02.json', scope)
#    client = gspread.authorize(creds)
#    sheet = client.open('Indeed Jds').sheet1
#    df=pd.DataFrame(sheet.get_all_records())
#    return df
#pRdf=getDf()


mapdata=pd.read_csv("mapdata.csv")
df=pd.read_csv("VectorizedTags.csv")
prdf2=pd.read_csv("pilotRoles.csv")
df=df.drop(["Customer","United States","Timiza"],axis=1)
r=list(df["Role"].unique())

r=list(df["Role"].dropna().unique())
r.sort()
r.remove("Amazon")


df=df.fillna(0)


sum(df["Oracle"])



r.sort()
desc=df[df["Role"]=="Drafter"].describe()
sr=round((desc.loc["count",]/len(df[df["Role"]=="Drafter"]))*100,ndigits=2)

a=sr[sr>=10]
a[a<=50].sort_values(ascending=False)



def getRange(start,stop,srs):
    sr1=srs[srs>=start].sort_values(ascending=False)
    sr1=sr1[sr1<=stop].sort_values(ascending=False)
    return sr1

def get3dplot():
    plotdf=pd.read_csv("kmeans.csv")
    c0=plotdf[plotdf["Cluster"]==0]
    c1=plotdf[plotdf["Cluster"]==1]
    c2=plotdf[plotdf["Cluster"]==2]
    c3=plotdf[plotdf["Cluster"]==3]
    c4=plotdf[plotdf["Cluster"]==4]
    def get_label_text(df):
        r=list(df.Role)
        rr=[]    
        for i in r:
            b='''<b>{}</b><br><i>Other roles in the cluster</i><br>\t{}
                '''.format(i," <br>    ".join(r))
            rr.append(b)
        return rr    
    trace1 = go.Scatter3d(
                        x = c1["PCA1_3D"],
                        y = c1["PCA2_3D"],
                        z = c1["PCA3_3D"],
                        mode="markers",
                        #line=dict(
                        #        color='#1f77b4',
                        #        width=4),
                        hovertext=get_label_text(c1),
                        name = "Cluster 1",
                        marker = dict(color = 'rgba(110, 125, 125, 0.8)'),
                        text = None)
    trace0 = go.Scatter3d(
                        x = c0["PCA1_3D"],
                        y = c0["PCA2_3D"],
                        z = c0["PCA3_3D"],
                        mode = "markers",
                        hovertext=get_label_text(c0),
                        name = "Cluster 0",
                        marker = dict(color = 'rgba(255, 30, 145, 0.8)'),
                        text = None)
    trace2 = go.Scatter3d(
                        x = c2["PCA1_3D"],
                        y = c2["PCA2_3D"],
                        z = c2["PCA3_3D"],
                        mode = "markers",
                        hovertext=get_label_text(c2),
                        name = "Cluster 2",
                        marker = dict(color = 'rgba(0, 220, 250, 0.8)'),
                        text = None)

    trace4 = go.Scatter3d(
                        x = c4["PCA1_3D"],
                        y = c4["PCA2_3D"],
                        z = c4["PCA3_3D"],
                        mode = "markers",
                        hovertext=get_label_text(c4),
                        name = "Cluster 4",
                        marker = dict(color = 'rgba(255, 220, 80, 0.8)'),
                        text = None)
    trace3 = go.Scatter3d(
                        x = c3["PCA1_3D"],
                        y = c3["PCA2_3D"],
                        z = c3["PCA3_3D"],
                        mode = "markers",
                        text=get_label_text(c3),
                        name = "Cluster 3",
                        marker = dict(color = 'rgba(255, 80, 80, 0.8)'),
                        )
    data=[trace0,trace1,trace2,trace4,trace3]
    axis=dict(showbackground=False,
              showline=False,
              zeroline=False,
              showgrid=False,
              showticklabels=False,
              title=''
              )
    layout = go.Layout(
             title="Role Similarity (3D visualization)",
             plot_bgcolor='#273e49',
             width=800,
             height=800,
             showlegend=False,
             scene=dict(
                 xaxis=dict(axis),
                 yaxis=dict(axis),
                 zaxis=dict(axis),
            ))        
    fig = dict(data = data,layout=layout)
    fig=go.Figure(fig)
    return fig






external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div([
    html.H1(
        children="Data Exploration",
        style={
            "font":"Roboto Regular",
            'text-align': 'center',
            "color":"#09ACF7",
            "size":24
        }
    ),
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H3(
                            children="Role Chooser :",
                            style={
                                "font":"Roboto",
                                'text-align': 'center',
                                "color":"#09ACF7",
                                "size":17
                                }
                            )
            ],width=3),
            dbc.Col([
                    dcc.Dropdown(
                        id='Role Chooser',
                        options=[{'label': i, 'value': i} for i in r],
                        value='Software Developer'                       
                    )
            ],width=3),
            dbc.Col([
                dcc.Markdown(children='''
                                **Sample Size**     :   13169 Job Descriptions  
                                **Time Frame**      :   29/09/2018 ➤➤ 27/08/2019  
                                **Date Crawled**    :   28/08/2019  
                                        ''')
                
            ],width=6)
        ]),
        dbc.Row([
            dbc.Col([
                    html.Div([
                        html.H3(
                            children="Skill in Roles percentages",
                            style={
                                "font":"Roboto",
                                'text-align': 'center',
                                "color":"#09ACF7",
                                "size":17
                                }
                            ),
                        dcc.Graph(
                            id="role_graph_table"
                        )
                    ])
            ],width=9),
            dbc.Col([
                html.Div([
                    html.H4(
                        children="Job titles Associated with the Role",
                            style={
                               "font":"Roboto",
                               'text-align': 'center',
                               "color":"#09ACF7",
                               "size":20
                                }    
                    ),
                    html.Ul(
                        id="jobs_assoc"
                    )
                ])                
            ])

        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id="chloropleth")
                ])                
            ],width=4.5),
            dbc.Col([
                html.Div([
                    html.H4(
                        children="Top Cities",
                            style={
                               "font":"Roboto",
                               'text-align': 'center',
                               "color":"#09ACF7",
                               "size":20
                                }    
                        ),
                    html.Ul(
                        id="top_cities"
                    )            
                    ])
                ],width=3),
            dbc.Col([
                dcc.Graph(id="3dplot",
                    figure=get3dplot())              
            ])
        ])        
    ])
])
@app.callback(
    Output("role_graph_table", 'figure'),
    [Input("Role Chooser", 'value')])
def getFig(role):
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
    fig.add_trace(go.Bar(
        x=sr1.index,
        y=list(sr1)
    ),row=1,col=1)
    fig.add_trace(go.Table(
        header=dict(
            values=["Skill","Percentage"],
            font=dict(size=14),
            align="left"
        ),
        cells=dict(
            values=[list(sr1.index),list(sr1)],
            align="left"
        )
    ),row=1,col=2)

    return fig

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
def get_chloropleth(role):
    mapdf=mapdata[mapdata["Role"]==role]
    mapdf.columns
    fig=go.Figure()
    fig.add_trace(go.Scattergeo(    
            locationmode = 'USA-states',
            lon = mapdf['longitude'],
            lat = mapdf['latitude'],
            text = mapdf['City'],
            marker = dict(
                size = mapdf['Count']*15,
                color = "blue"
            )
    )
    )
    fig.update_layout(
            title_text = 'Geographical Demand for {} in the US'.format(role),
            showlegend = False,
            geo = dict(
                scope = 'usa',
                landcolor = 'rgb(217, 217, 217)',
            )
        )
    return fig



@app.callback(
    Output("top_cities", 'children'),
    [Input("Role Chooser", 'value')])
def get_top_cities(role):
    jts=list(mapdata[mapdata["Role"]==role]["City"][0:10])
    htm=[html.Li(x) for x in jts]
    return htm




if __name__ == "__main__":
    app.run_server(host="0.0.0.0")


