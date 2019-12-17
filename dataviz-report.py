from plotly import graph_objects as go
import pandas as pd

df=pd.read_csv("monthsdf.csv")

fig=go.Figure()
skills=list(df["Skill"])
df=df.set_index(["Skill"])
df[df["Skill"]==skills[1]].reset_index(drop=True)[:0]

type(df.loc[skills[3]])

for i in skills[:20]:
    fig.add_trace(
        go.Scatter(
            x=df.columns,
            y=df.loc[i],
            mode="lines",
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
    return df      name=i
        )
    )
    
fig.show()





minDf=pd.read_csv("minimizedFlcData.csv")
minDf.columns


def get_color_codes(sdf):
    '''
    This function generates the color codes for Change and volatility in the table.
    '''
    change=[]
    vol=[]
    for i in range(len(sdf)):
        if sdf["%change"][i]>0:
            change.append("#00DCFA")
        elif sdf["%change"][i]<0:
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






get_color_codes(minDf)
sdf=minDf




minDf=df




fig=go.figure()

fig=fig.add_trace(go.Bar(
    x=sr1.index,
    y=list(sr1),
    marker_color="#FF1E91"
),row=1,col=1)


minDf.columns


sdf=minDf[["Skill"'Dec 2019',"Volatility"]]
sdf["% Change from previous month"]=sdf["September"]-sdf[colname]
sdf=sdf.drop([colname],axis=1)
coldf=get_color_codes(sdf)
fig=fig.add_trace(go.Table(minDf.columns
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