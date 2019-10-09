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

df=pd.read_csv("VectorizedTags3.csv")
df=df.dropna(axis=0, how='all', thresh=None, subset=None, inplace=False)
r=list(df.Role.unique())
df.columns
a=(df[df["Role"]=="Software Developer"].drop(["Role","Job Title"],axis=1).sum()/len(df["Role"])).to_dict()

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
kmeans=KMeans(n_clusters=5,init="k-means++",random_state=30)
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
for i in range(1,5):
    df_row=pd.concat([df_row,plotdf[plotdf["Cluster"]==i][["PCA1_3D","PCA2_3D","PCA3_3D"]].mean().to_frame()],axis=1)


plotdf["Cluster"].value_counts()

df_row
df_row.columns=["0","1","2","3","4"]
df_row=df_row.transpose()
df_row.to_csv("clusterCenters2.csv")
df_row.columns



plotdf.to_csv("kmeans2.csv")
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
#df_row["PCA1_3D"][3]
#xe=[]
#ye=[]
#ze=[]
#for i in range(len(c3)):
#    xe += [c3["PCA1_3D"][i],df_row["PCA1_3D"][3]],
#    ye += c3["PCA2_3D"][i],df_row["PCA2_3D"][3],
#    ze += c3["PCA3_3D"][i],df_row["PCA3_3D"][3],
#
#
#ltrace3 = go.Scatter3d(
#                    x = xe,
#                    y = ye,
#                    z = ze,
#                    mode = "lines",
#                    text=c3.index,
#                    line=dict(
#                            color='#1f77b4',
#                            width=6),
#                    )
#
#cTrace=go.Scatter3d(
#                    x = df_row["PCA1_3D"],
#                    y = df_row["PCA2_3D"],
#                    z = df_row["PCA3_3D"],
#                    mode="markers",
#                    marker=dict(
#                        color='rgb(24, 53, 82)',
#                        size=10,
#                        line=dict(
#                            color='yellow',
#                            width=8
#                        )
#                    ),
#                    line=dict(color='rgb(125,125,125)', width=1),
#                    hovertext=list(df_row.index)
#               )

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
            b='''<b>{}</b><br>
            <i>Other roles in the cluster</i><br>
                {}
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
    axis=dict(#showbackground=False,
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


a=get3dplot()

a["data"]

def get_label_text(df):
    r=list(df.Role)
    rr=[]    
    for i in r:
        b='''<b>{}</b><br>
        <i>Other roles in the cluster</i><br>
            {}
            '''.format(i," <br>    ".join(r))
        rr.append(b)
    return rr
get_label_text(c1)


plotdf=pd.read_csv("kmeans.csv")
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
                    hovertext=rr,
                    name = "Cluster 1",
                    marker = dict(color = 'rgba(110, 125, 125, 0.8)'),
                    text =None )
data=[trace1]
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




@app.callback(
    [Output("role_chosen", 'children'),
    Output("filtered_roles", 'children'),
    Output("test", 'children')],
    [Input("3dplot", 'hoverData')])
def hoverDataShow(hoverData):
    point = hoverData["points"]
    clstr=int(minDf[minDf["Role"]==point["text"]]["Cluster"])
    rls=clustDict[clstr]
    rls.remove(point["text"])
    return (
        point["text"],
        [html.Li(x) for x in rls],
        point
    )








import plotly.plotly as py
a=plot(fig, filename='RoleSimilarity.html')
print(a)
fig.show()
import chart_studio
import chart_studio.plotly as py
chart_studio.tools.set_credentials_file(username='unleash', api_key='8ffgofURfM5YYfUzlYdG')
py.plot(fig, filename = 'RoleSimilarity', auto_open=True)




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


plotdf=getDf(df)

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


get3dcluster3(plotdf)


####Viz tests

def getRange(start,stop,srs):
    sr1=srs[srs>=start].sort_values(ascending=False)
    sr1=sr1[sr1<=stop].sort_values(ascending=False)
    return sr1



role="Software Engineer"
desc=df[df["Role"]==role].describe()
sr=round((desc.loc["count",]/len(df[df["Role"]==role]))*100,ndigits=2)
sr1=getRange(10,100,sr)


a=df[df["Role"]==role].sum()
a=a.drop("Role")
a=a.drop("Job Title")

a=a.divide(len(df[df["Role"]==role]))*100

a=getRange(10,100,a)
a=a.apply(np.round)




role="Software Engineer"
a=df[df["Role"]==role].sum()
a=a.drop("Role")
a=a.drop("Job Title")    
a=a.divide(len(df[df["Role"]==role]))*100
a=getRange(10,100,a)
sr1=a.apply(np.round)
fig=go.Figure()
fig=fig.add_trace(go.Table(
    header=dict(
        values=["Skill","Percentage"],
        font=dict(size=14),
        align="left"
    ),
    cells=dict(
        values=[list(sr1.index),list(sr1)],
        align="left"
    )
))

fig.show()



prdf2=pd.read_csv("pilotRoles.csv")



def get_assocJt(role):
    jts=list(prdf2[prdf2["Role"]==role]["jobtitle"].value_counts().index)[1:10]
    return jts

get_assocJt(role)


b=prdf2[prdf2["Role"]==role]["city"].value_counts()

fig=go.Figure()
fig.add_trace(go.Scattergeo(

))

b["San Francisco"]

c=b.index[1]
cities=list(prdf2["city"].value_counts().index)

c=cities[1]
d=prdf2[prdf2["city"]==c]["latitude"].mean()

prdf=prdf2

len(cities)

ndloc=pd.read_csv("sampleData.csv")[['Role','latitude', 'longitude','city']]
afCities=list(ndloc.city.unique())
afCities.remove(np.nan)
ndloc.columns
ndloc2=ndloc

locD=ndloc.city.value_counts().to_frame().reset_index()
locD.columns=["City","Count"]


for i in afCities:
    lat=ndloc[ndloc["city"]==i]["latitude"].mean()
    lng=ndloc[ndloc["city"]==i]["longitude"].mean()
    ndloc2[ndloc2["city"]==i]["latitude"]=lat

ndloc2.to_csv("ndLocData",index=False)

i="Data Analyst"
j="Lagos"
fdf=pd.DataFrame(columns=["Role","latitude","longitude","City"])    
for i in ndloc2.Role.unique():
    for j in afCities:
        try:
            sdf=ndloc2[(ndloc2["Role"]==i)&(ndloc2["city"]==j)].reset_index(drop=True)
            cnt=len(sdf)
            fdf=fdf.append({
                "Role":i,
                "latitude":sdf["latitude"][0],
                "longitude":sdf["longitude"][0],
                "City":j,
                "Count":cnt
            },ignore_index=True)
        except IndexError:
            pass

fdf.to_csv("ndLocData.csv",index=False)




prdf[prdf["city"]=="New York"].assign(latitude,lat)

lat

locations=pd.read_csv("locations.csv")
b=ndloc2[ndloc2["Role"]==role]["city"].value_counts()

len(b.index)


b=b.to_frame()
b.columns=["count"]
float(locations[locations["city"]==b.index[1]]["latitude"])
b["latitude"]=np.nan
b["longitude"]=np.nan
for i in b.index:
    lat=float(locations[locations["city"]==i]["latitude"])
    lng=float(locations[locations["city"]==i]["longitude"])
    b["latitude"][i]=lat
    b["longitude"][i]=lng


locations.to_dict()["city"]



mapdata=pd.read_csv("ndLocData.csv")


def get_chloropleth(role):
    mapdf=mapdata[mapdata["Role"]==role]
    mapdf.columns
    fig=go.Figure()
    fig.add_trace(go.Scattergeo(
            lon = mapdf['longitude'],
            lat = mapdf['latitude'],
            text = mapdf['City'],
            marker = dict(
                size = mapdf['Count']*.8,
                color = "blue"
            )
    )
    )
    fig.update_layout(
            title_text = 'Geographical Demand for {} in the US'.format(role),
            showlegend = True,
            geo = dict(
                scope = 'africa',
                landcolor = 'rgb(217, 217, 217)',
            )
        )
    return fig



def get_top_cities(role):
    jts=list(mapdata[mapdata["Role"]==role]["City"][0:10])
    return jts



get_chloropleth("Data Analyst").show()


role="Data Analyst"
mapdata[mapdata["Role"]==role].sort_values("Count",ascending=False).head(10)["City"]
df2.columns

if (role=="data") or (role=="daata2"):
    print("yes")
else:
    print("no")



daDf=pd.read_csv("daSample.csv")
netDf=pd.read_csv("netSample.csv")

sdf.columns
def get_color_codes(sdf):
    change=[]
    vol=[]
    for i in range(20):
        if sdf["% Change from previous month"][15]>0:
            change.append("#00DCFA")
        elif sdf["% Change from previous month"][i]<0:
            change.append("#FF1E91")
        else:
            change.append("#252630")        
        if sdf.Volatility[i] <2.5:
            vol.append("#252630")
        elif (sdf.Volatility[i] >2.5) and (sdf.Volatility[i] <5):
            vol.append("#FFDC50")
        else:
            vol.append("#FF1E91")
    df=pd.DataFrame()
    df["change"]=change
    df["volatility"]=vol
    df["skill"]="#252630"
    df["perc"]="#252630"
    return df

df["change"]=np.nan
df["change"][0]=10


sdf[sdf.Skill=="modelling"]["% Change from previous month"]
import json
with open("skill_distribution.json","r") as jFile:
    tCount=json.load(jFile)

tCount

df=df.drop(['Role', 'Job Title'],axis=1)

jCount=df.sum().to_dict()

tCount["customer"]
cDf=pd.DataFrame(columns=["skill","supply","demand"])
for i in jCount.keys():
    try:
        src=i.lower()
        t=tCount[src]
        cDf=cDf.append({
            "skill":i,
            "supply":round((t/4708)*100,ndigits=2),
            "demand":round((jCount[i]/13169)*100,ndigits=2)
        },ignore_index=True)
    except KeyError:
        pass
cDf.to_csv("Count.csv",index=False)



type(tCount["customer"])


cdf=pd.read_csv("Count.csv")
cdf=cdf.sort_values("Supply Difference",ascending=True).reset_index(drop=True)

fig=go.Figure()

fig=fig.add_trace(
    go.Bar(
        y=cdf.skill.head(30),x=cdf.sup.head(30),
        name='Supply',
        orientation='h',
        marker=dict(
        color='rgba(246, 78, 139, 0.6)',
        line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    )
    )
)
fig=fig.add_trace(
    go.Bar(
        y=cdf.skill.head(30),x=cdf.dem.head(30),
        name='Demand',
        orientation='h',
        marker=dict(
        color='rgba(58, 71, 80, 0.6)',
        line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
    )
    )
)
fig=fig.update_layout(barmode='stack')
fig.show()


daDf=pd.read_csv("daSample.csv")
daDf.head(10)
sdf=daDf.drop("Volatility",axis=1)
sdf.ix[2].drop("Skill")
a=list(sdf.columns)
a.remove("Skill")
fig=go.Figure()
for i in range(10):
    row=sdf.ix[i]
    fig=fig.add_trace(
        go.Scatter(
            x=a,
            y=row.drop("Skill"),
            mode="lines",
            name=row["Skill"].capitalize()
        )
    )
fig=fig.update_layout(
    go.Layout(
        title="Start Title",
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None])])]
    )
)
fig.update_frame()

fig.show()

row["Skill"].capitalize()

help(fig)
