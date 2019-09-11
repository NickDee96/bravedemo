#Basic imports
import numpy as np
import pandas as pd

#sklearn imports
from sklearn.decomposition import PCA #Principal Component Analysis
from sklearn.manifold import TSNE #T-Distributed Stochastic Neighbor Embedding
from sklearn.cluster import KMeans #K-Means Clustering
from sklearn.preprocessing import StandardScaler #used for 'Feature Scaling'

#plotly imports
import plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

df=pd.read_csv("VectorizedTags.csv")

def getDf(df):
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


get3Dplot(plotdf)

def get2Dplot():
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


