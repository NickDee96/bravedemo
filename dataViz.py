import pandas as pd
import plotly
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from collections import OrderedDict, Counter
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sklearn.feature_extraction.text import TfidfVectorizer 
import re
import nltk
nltk.download('stopwords')
from nltk import PorterStemmer as pstemmer
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
import string
import math
from sklearn.decomposition import PCA #Principal Component Analysis
from sklearn.manifold import TSNE #T-Distributed Stochastic Neighbor Embedding
from sklearn.cluster import KMeans #K-Means Clustering
from sklearn.preprocessing import StandardScaler #used for 'Feature Scaling'
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


ska=pd.read_csv("roles.csv")
techSkills=pd.read_csv("tech_skillz.csv")
skillCount=techSkills['tech_skill'].value_counts()
skillDf=pd.DataFrame(skillCount).reset_index()
skillDf.columns=["tech_skill","count"]
skills=list(skillDf["tech_skill"])

def getDf():
    '''
    This function gets job descriptions from the JDs google sheet  and returns a pandas Dataframe
    '''
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('indeedscraper-f298f5bd5f02.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Indeed Jds').sheet1
    df=pd.DataFrame(sheet.get_all_records())
    return df
pRdf=getDf()
def cleanStrings(text):
	text=str(text)
	text=text.lower()
	text=text.replace("'"," ").replace('"'," ")
	plist=list(string.punctuation)
	plist.remove("+")
	for j in plist:
		if j in plist:
			text=text.replace(j," ")
	stop_words=stopwords.words('english')
	text1=text.split(' ')
	text2=list()
	for i in text1:
	    if i not in stop_words:
	        text2.append(i)
	return ' '.join(text2)
def getFeatureNames(iArray,length,nGramRange):
    tf=TfidfVectorizer(ngram_range=nGramRange,max_df=0.95, min_df=2, max_features=length)
    X=tf.fit_transform(iArray)
    return tf.get_feature_names()
def getCountDict(tfList,rawList):
    countDict=dict()
    for  i in tfList:
        count=0
        try:
            for j in rawList:
                if i in j:
                    count=count+1
            countDict.update({
                i:count
            })
        except ValueError:
            countDict.update({
                i:count
            })
    return countDict
class roleDetails:
    def __init__(self,roleName):
        role_ska=ska[ska["Role"]==roleName]
        self.role_ss=role_ska[role_ska["Content Model"]=="Soft Skills"][['SAK', 'Importance Value','Level Value']].reset_index(drop=True)
        self.role_kdg=role_ska[role_ska["Content Model"]=="Knowledge"][['SAK', 'Importance Value','Level Value']].reset_index(drop=True)
        self.role_skl=role_ska[role_ska["Content Model"]=="Skills"][['SAK', 'Importance Value','Level Value']].reset_index(drop=True)
        role_skills=techSkills[techSkills["role_name"]==roleName]
        self.hot_tech=list(role_skills[role_skills["hot_technology"]=="Y"]["tech_skill"])
        self.outdated_tech=list(role_skills[role_skills["hot_technology"]=="N"]["tech_skill"])

df=pd.read_csv("VectorizedTags.csv")

def getVDf(df):
    df=df.fillna(0)
    df1=df.drop(["Role","Job Title"],axis=1)
    df1.head()
    #Transposing the Data Frame
    df1=df1.transpose()
    #Initializing the sclaer
    scaler=StandardScaler()
    sDf=pd.DataFrame(scaler.fit_transform(df1))
    sDf.index=df1.index
    #Initializing the model
    kmeans=KMeans(n_clusters=5,init="k-means++",random_state=100)
    kmeans.fit(sDf)
    #Find which cluster each data-point belongs to
    clusters=kmeans.predict(sDf)
    #Add the cluster vector to our DataFrame, sDf
    sDf["Cluster"] = clusters
    sDf["Cluster"].value_counts()
    #2d Dataframe
    pca_2d = PCA(n_components=2)
    PCs_2d = pd.DataFrame(pca_2d.fit_transform(sDf.drop(["Cluster"], axis=1)))
    PCs_2d.columns=["PCA1_2D","PCA2_2D"]
    PCs_2d.index=sDf.index
    #3d Dataframe
    pca_3d = PCA(n_components=3)
    PCs_3d = pd.DataFrame(pca_3d.fit_transform(sDf.drop(["Cluster"], axis=1)))
    PCs_3d.columns=["PCA1_3D","PCA2_3D","PCA3_3D"]
    PCs_3d.index=sDf.index

    #Concatenating the Dataframe
    plotdf=pd.concat([sDf,PCs_3d,PCs_2d], axis=1, join='inner')
    return plotdf


plotdf=getVDf(df)

def get3Dplot(plotdf):    
    c0=plotdf[plotdf["Cluster"]==0]
    c1=plotdf[plotdf["Cluster"]==1]
    c2=plotdf[plotdf["Cluster"]==2]
    c3=plotdf[plotdf["Cluster"]==3]
    c4=plotdf[plotdf["Cluster"]==4]
    trace1 = go.Scatter3d(
                        x = c1["PCA1_3D"],
                        y = c1["PCA2_3D"],
                        z = c1["PCA3_3D"],
                        mode = "markers",
                        hovertext=c1.index,
                        name = "Cluster 1",
                        marker = dict(color = 'rgba(110, 125, 125, 0.8)'),
                        text = None)
    trace0 = go.Scatter3d(
                        x = c0["PCA1_3D"],
                        y = c0["PCA2_3D"],
                        z = c0["PCA3_3D"],
                        mode = "markers",
                        hovertext=c0.index,
                        name = "Cluster 0",
                        marker = dict(color = 'rgba(255, 30, 145, 0.8)'),
                        text = None)

    trace2 = go.Scatter3d(
                        x = c2["PCA1_3D"],
                        y = c2["PCA2_3D"],
                        z = c2["PCA3_3D"],
                        mode = "markers",
                        hovertext=c2.index,
                        name = "Cluster 2",
                        marker = dict(color = 'rgba(0, 220, 250, 0.8)'),
                        text = None)

    trace4 = go.Scatter3d(
                        x = c4["PCA1_3D"],
                        y = c4["PCA2_3D"],
                        z = c4["PCA3_3D"],
                        mode = "markers",
                        hovertext=c4.index,
                        name = "Cluster 4",
                        marker = dict(color = 'rgba(255, 220, 80, 0.8)'),
                        text = None)
    data=[trace0,trace1,trace2,trace4]
    fig = dict(data = data)
    fig=go.Figure(fig)
    return fig



def get2Dplot(plotDf):
    c0=plotdf[plotdf["Cluster"]==0]
    c1=plotdf[plotdf["Cluster"]==1]
    c2=plotdf[plotdf["Cluster"]==2]
    c3=plotdf[plotdf["Cluster"]==3]
    c4=plotdf[plotdf["Cluster"]==4]  

    trace1 = go.Scatter(
                        x = c1["PCA1_2D"],
                        y = c1["PCA2_2D"],
                        mode = "markers",
                        hovertext=c1.index,
                        name = "Cluster 1",
                        marker = dict(color = 'rgba(125, 125, 0.8)'),
                        text = None)
    trace0 = go.Scatter(
                        x = c0["PCA1_2D"],
                        y = c0["PCA2_2D"],
                        mode = "markers",
                        hovertext=c0.index,
                        name = "Cluster 0",
                        marker = dict(color = 'rgba(30, 145, 0.8)'),
                        text = None)
    trace2 = go.Scatter(
                        x = c2["PCA1_2D"],
                        y = c2["PCA2_2D"],
                        mode = "markers",
                        hovertext=c2.index,
                        name = "Cluster 2",
                        marker = dict(color = 'rgba( 220, 250, 0.8)'),
                        text = None)
    trace4 = go.Scatter(
                        x = c4["PCA1_2D"],
                        y = c4["PCA2_2D"],
                        mode = "markers",
                        hovertext=c4.index,
                        name = "Cluster 4",
                        marker = dict(color = 'rgba(220, 80, 0.8)'),
                        text = None)
    data=[trace0,trace1,trace2,trace4]
    fig = dict(data = data)

    iplot(fig)
    fig=go.Figure(fig)
    return fig


def get2dcluster3(plotdf):
    c3=plotdf[plotdf["Cluster"]==3]
    trace3 = go.Scatter(
                    x = c3["PCA1_2D"],
                    y = c3["PCA2_2D"],
                    mode = "markers",
                    text=c3.index,
                    hovertext=c3.index,
                    name = "Cluster 3",
                    marker = dict(color = 'rgba(220, 80, 0.8)'))
    data=[trace3]
    fig = dict(data = data)
    fig=go.Figure(fig)
    return fig

def get3dcluster3(plotdf):
    c0=plotdf[plotdf["Cluster"]==0]
    c1=plotdf[plotdf["Cluster"]==1]
    c2=plotdf[plotdf["Cluster"]==2]
    c3=plotdf[plotdf["Cluster"]==3]
    c4=plotdf[plotdf["Cluster"]==4]
    trace3 = go.Scatter3d(
                    x = c3["PCA1_3D"],
                    y = c3["PCA2_3D"],
                    z=c3["PCA3_3D"],
                    mode = "markers",
                    text=c3.index,
                    hovertext=c3.index,
                    name = "Cluster 3",
                    marker = dict(color = 'rgba(220, 80, 0.8)'))
    data=[trace3]
    fig = dict(data = data)
    fig=go.Figure(fig)
    return fig





r=list(ska["Role"].value_counts().index)
r.sort()

pilotRoles=list(pRdf["Role"].value_counts().index)

s=list()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1(
        children='O*net Analysis',
        style={'text-align': 'center',
                "font":"Roboto",
                "color":"#09ACF7",
                "size":"24"}
    ),
        html.H2(
        children='Brave Venture Labs',
        style={'text-align': 'center',
                "font":"Lustria",
                "color":"#09ACF7",
                "size":"20"}
    ),
        html.H3(
        children='Search by Role',
        style={'text-align': 'center',
                "font":"Lustria",
                "color":"#5B717A",
                "size":"17"}
    ),
    html.Div([
        html.Div([
            html.Div([
                    dcc.Dropdown(
                        id='Role Chooser',
                        options=[{'label': i, 'value': i} for i in r],
                        value='Statisticians'
                    ),
                    dcc.Graph(id="role_det")
                    ]
                )
                ],style= {'width': '49%', 'display': 'inline-block'}),
            html.Div([
                        html.H3([
                                "Technologies used",
                            ],style={'text-align': 'center',
                                        "font":"Roboto",
                                        "color":"#09ACF7",
                                        "size":"20"}),
                        dcc.Markdown(id="hot_tech",style={'color': "#5B717A",
                                                             'fontSize': 16,
                                                             "font":"Roboto"})
            ],style= {'width': '49%',
                     'display': 'inline-block',
                     'vertical-align': 'top',
                     'horizontal-align':"right"})
    ]),
    html.Div([
        html.Div([
            html.H3(
                children='Search by Skill',
                style={'text-align': 'center',
                        "font":"Lustria",
                        "color":"#5B717A",
                        "size":"17"}
                    ),
            dcc.Dropdown(
                        id='Skill Chooser',
                        options=[{'label': i, 'value': i} for i in skills],
                        multi=True,
                        value='Python',
                    ),
            html.H4(id="skill chooser" ,
                    style={'text-align': 'center',
                                        "font":"Roboto",
                                        "color":"#09ACF7",
                                        "size":"16"}),
            dcc.Graph(id="roles-appearing")
            
        ],style= {'width': '49%', 'display': 'inline-block'})
    ,html.Div([
            html.H3(
                children='Pilot Roles Search',
                style={'text-align': 'center',
                        "font":"Lustria",
                        "color":"#5B717A",
                        "size":"17"}
                    ),
            dcc.Dropdown(
                        id='plRole Chooser',
                        options=[{'label': i, 'value': i} for i in pilotRoles],
                        value='Software Engineer',
                    ),
            dcc.Graph(id="jobTitleGraph")
    ],style= {'width': '49%', 'display': 'inline-block'})
    ]),
    html.Div([
                html.H2(
                    children='KMeans Cluster analysis',
                    style={'text-align': 'center',
                            "font":"Lustria",
                            "color":"#5B717A",
                            "size":"17"}
                        ),
        html.Div([
                html.H3(
                    children='Cluster 0,1,2 and 4 in 2 dimensional space',
                    style={'text-align': 'center',
                            "font":"Lustria",
                            "color":"#5B717A",
                            "size":"15"}
                        ),
                dcc.Graph(id="graph2d",
                            figure=get2Dplot(plotdf))

        ]),
        html.Div([
                html.H3(
                    children='Cluster 0,1,2 and 4 in 3 dimensional space',
                    style={'text-align': 'center',
                            "font":"Lustria",
                            "color":"#5B717A",
                            "size":"15"}
                        ),
                dcc.Graph(id="graph3d",
                            figure=get3Dplot(plotdf))

        ])

    ],style= {'width': '49%', 'display': 'inline-block'}),
    html.Div([
        html.Div([
                html.H3(
                    children='Cluster 3 in 2 dimensional space',
                    style={'text-align': 'center',
                            "font":"Lustria",
                            "color":"#5B717A",
                            "size":"15"}
                        ),
                dcc.Graph(id="graph2dc3",
                            figure=get2dcluster3(plotdf))

        ]),
        html.Div([
                html.H3(
                    children='Cluster 3 in 3 dimensional space',
                    style={'text-align': 'center',
                            "font":"Lustria",
                            "color":"#5B717A",
                            "size":"15"}
                        ),
                dcc.Graph(id="graph3dc3",
                            figure=get3dcluster3(plotdf))

        ])

    ],style= {'width': '49%', 'display': 'inline-block'})

])







@app.callback(
    Output("role_det", 'figure'),
    [Input("Role Chooser", 'value')])

def getRoleplot(role):
    a=roleDetails(role)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=a.role_kdg["Importance Value"],
                                y=a.role_kdg["Level Value"],
                                mode="markers",name="Knowledge",
                                hovertext=a.role_kdg["SAK"],
                                marker=dict(
                                    color='#09ACF7',
                                    size=10,
                                )
                ))
    fig.add_trace(go.Scatter(x=a.role_skl["Importance Value"],
                                y=a.role_skl["Level Value"],
                                mode="markers",
                                name="Skills",
                                hovertext=a.role_skl["SAK"],
                                marker=dict(
                                    color='#FF1E91',
                                    size=10,
                                    )))
    fig.add_trace(go.Scatter(x=a.role_ss["Importance Value"],
                                y=a.role_ss["Level Value"],
                                mode="markers",
                                name="Soft Skills",
                                hovertext=a.role_ss["SAK"],
                                marker=dict(
                                    color='#00E676',
                                    size=10,
                                    )))
    fig.update_layout(
        title=go.layout.Title(
            text=("<b>{} <b> <br>Plot of Skills, Knowledge and Soft Skills".format(role)),
            xref="paper",
            x=0,
            font=dict(
                    family="Roboto",
                    size=24,
                    color="#09ACF7"
                )
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text="Importance Value",
                font=dict(
                    family="Roboto Regular",
                    size=18,
                    color="#5B717A"
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text="Level Value",
                font=dict(
                    family="Roboto Regular",
                    size=18,
                    color="#5B717A"
                )
            )
        )
    )
    return fig


@app.callback(
    Output("hot_tech","children"),
    [Input("Role Chooser", 'value')])
def getTech(role):
    a=roleDetails(role)   
    return ", ".join(a.hot_tech)

@app.callback(
    Output("skill chooser","children"),
    [Input('Skill Chooser','value')]
)

def getPercentage(skill):
    if type(skill)=="str":
        perc=round(float(skillDf[skillDf["tech_skill"]==skill]["count"]/1100)*100,2)
        out=(skill+" occurs in "+str(perc)+"% of O*Net's roles. The roles are listed below.")
    else:
        perc=round(float(skillDf[skillDf["tech_skill"]==skill[0]]["count"]/1100)*100,2)
        out=(skill[0]+" occurs in "+str(perc)+"% of O*Net's roles. The roles are listed below.")
    return out

@app.callback(
    Output("roles-appearing","figure"),
    [Input('Skill Chooser','value')]
)
def getroles(skill_list):
    s=list()
    for i in skill_list:
        skills=list(techSkills[techSkills["tech_skill"]==i]["role_name"])
        s=s+skills
        class OrderedCounter(Counter, OrderedDict): 
            pass
    mskills = [k for k, v in OrderedCounter(s).items() if v > len(skill_list)-1]
    fig2 = go.Figure(data=[go.Table(header=dict(values=['Roles']),
                 cells=dict(values=[mskills]))
                     ])
    return fig2

@app.callback(
    Output("jobTitleGraph","figure"),
    [Input('plRole Chooser','value')])

def get_title_plot(rName):
    se=pRdf[pRdf["Role"]==rName]
    jtitles=se["jobtitle"].apply(cleanStrings)
    fJtitles=getFeatureNames(jtitles,20,(2,3))
    counts=getCountDict(fJtitles,jtitles)
    fig = go.Figure(data=[go.Pie(labels=list(counts.keys()), values=list(counts.values()))])
    fig.update_traces(hole=.5)
    fig.update_layout(
        title_text="Job titles associated with {}".format(rName),
        # Add annotations in the center of the donut pies.
        annotations=[dict(text=rName, x=0.5, y=0.5, font_size=20, showarrow=False)])
    return fig


if __name__ == "__main__":
    app.run_server(host="0.0.0.0")
