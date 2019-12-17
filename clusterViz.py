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

df=pd.read_csv("data/VectorizedTags3.csv")
n_clust=5
class KMeansModel:
    def __init__(self,df,n_clust):        
        df=df.dropna(axis=0, how='all', thresh=None, subset=None, inplace=False)
        r=list(df.Role.unique())
        ## Initializing an empty dataFrame to update the column sums
        anDf=pd.DataFrame(columns=df.columns)
        for i in r:
            a=(df[df["Role"]==i].drop(["Role","Job Title"],axis=1).sum()/len(df["Role"]==i)).to_dict()
            anDf=anDf.append(a,ignore_index=True)
        anDf=anDf.drop(["Role","Job Title"],axis=1)
        anDf.index=r
        #anDf=anDf.transpose()

        scaler=StandardScaler()
        sDf=pd.DataFrame(scaler.fit_transform(anDf))
        sDf.index=anDf.index
        #30
        kmeans=KMeans(n_clusters=n_clust,init="k-means++",random_state=30)
        kmeans.fit(sDf)
        clusters=kmeans.predict(sDf)
        #Add the cluster vector to our DataFrame, sDf
        sDf["Cluster"] = clusters


        pca_3d = PCA(n_components=3)
        PCs_3d = pd.DataFrame(pca_3d.fit_transform(sDf.drop(["Cluster"], axis=1)))
        PCs_3d.columns=["PCA1_3D","PCA2_3D","PCA3_3D"]
        PCs_3d.index=sDf.index
        plotdf=pd.concat([sDf,PCs_3d], axis=1, join='inner')


        df_row=plotdf[plotdf["Cluster"]==0][["PCA1_3D","PCA2_3D","PCA3_3D"]].mean().to_frame()
        for i in range(n_clust):
            df_row=pd.concat([df_row,plotdf[plotdf["Cluster"]==i][["PCA1_3D","PCA2_3D","PCA3_3D"]].mean().to_frame()],axis=1)

        df_row.columns=[str(x) for x in range(n_clust)]
        df_row=df_row.transpose()
        df_row.to_csv("clusterCenters2.csv")
        plotdf=plotdf.reset_index()
        plotdf.rename(columns={"index":"Role"},inplace=True)
        plotdf.to_csv("data/kmeans2.csv")
        self.plotdf=plotdf
        self.clusterdf=df_row

model=KMeansModel(df,5)



c0=plotdf[plotdf["Cluster"]==0]
c1=plotdf[plotdf["Cluster"]==1]
c2=plotdf[plotdf["Cluster"]==2]
c3=plotdf[plotdf["Cluster"]==3]
c4=plotdf[plotdf["Cluster"]==4]

trace1 = go.Scatter3d(
                    x = c1["PCA1_3D"],
                    y = c1["PCA2_3D"],
                    z = c1["PCA3_3D"],
                    mode="markers",
                    #line=dict(
                    #        color='#1f77b4',
                    #        width=4),
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
trace3 = go.Scatter3d(
                    x = c3["PCA1_3D"],
                    y = c3["PCA2_3D"],
                    z = c3["PCA3_3D"],
                    mode = "markers",
                    text=c3.index,
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
fig.show()




df=pd.read_csv("data/daSample.csv")
df.set_index("Skill",inplace=True)
df=df.drop("Volatility",axis=1)
df.iloc[1]
df.index[1]
import plotly.graph_objects as go

fig =go.Figure()
for i in range(20):
    fig.add_trace(
        go.Scatter(
            x=df.columns,
            y=df.iloc[i],
            mode="lines",
            name=df.index[i]
        )
    )

data=[]
for i in range(len(df.columns)):
    a=go.Scatter(
            x=[x for df.columns[i]],
            y=df.iloc[],
            mode="lines"
    )  


fig.show()
i=df.columns[1]
df["January"].iloc[1]

df.iloc[1]

df[i].head(20).index   