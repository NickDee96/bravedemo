import pandas as pd
import plotly
from plotly.subplots import make_subplots
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




#def getDf():
#    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#    creds = ServiceAccountCredentials.from_json_keyfile_name('indeedscraper-f298f5bd5f02.json', scope)
#    client = gspread.authorize(creds)
#    sheet = client.open('Indeed Jds').sheet1
#    df=pd.DataFrame(sheet.get_all_records())
#    return df
#pRdf=getDf()



df=pd.read_csv("VectorizedTags.csv")
df=df.drop(["Customer","United States"],axis=1)
r=list(df["Role"].unique())

r=list(df["Role"].dropna().unique())
r.sort()
r.remove("Amazon")





r.sort()
desc=df[df["Role"]=="Drafter"].describe()
sr=round((desc.loc["count",]/len(df[df["Role"]=="Drafter"]))*100,ndigits=2)

a=sr[sr>=10]
a[a<=50].sort_values(ascending=False)



def getRange(start,stop,srs):
    sr1=srs[srs>=start].sort_values(ascending=False)
    sr1=sr1[sr1<=stop].sort_values(ascending=False)
    return sr1



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1(
        children="Job description Analysis",
        style={
            "font":"Roboto Regular",
            'text-align': 'center',
            "color":"#09ACF7",
            "size":24
        }
    ),
        html.H2(
        children="Skill in Roles percentages",
        style={
            "font":"Roboto",
            'text-align': 'center',
            "color":"#09ACF7",
            "size":20
        }
    ),
    html.Div([
        dcc.Dropdown(
                        id='Role Chooser',
                        options=[{'label': i, 'value': i} for i in r],
                        value='Software Developer'                       
                    ),
        dcc.Graph(
            id="role_graph_table"
        )
        
    ])
])
@app.callback(
    Output("role_graph_table", 'figure'),
    [Input("Role Chooser", 'value')])
def getFig(role):
    desc=df[df["Role"]==role].describe()
    sr=round((desc.loc["count",]/len(df[df["Role"]==role]))*100,ndigits=2)
    sr1=getRange(10,100,sr)
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

if __name__ == "__main__":
    app.run_server()
