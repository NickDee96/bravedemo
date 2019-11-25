import pandas as pd
import numpy as np


df=pd.read_csv("VectorizedTags.csv")

df=df.fillna(0)


def getDf():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('indeedscraper-f298f5bd5f02.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Indeed Jds').sheet1
    df=pd.DataFrame(sheet.get_all_records())
    return df
pRdf=getDf()

len(pRdf)

pRdf[pRdf["Role"]==nan]

pRdf["skills"]=np.nan

for i in range(len(pRdf)-1):
    skills=list((df.loc[i,:][df.loc[i,:]==1]).index)
    skills="|".join(skills)
    pRdf["skills"][i]=skills

pRdf.to_csv("jds&skills.csv")

skills=list((df.loc[24,:][df.loc[24,:]==1]).index)



pRdf.loc[24,:]
a.index



#skills merger

df2=pd.read_csv("jds&skills.csv")
df3=pd.read_csv("pilotRoles.csv")

df3.columns

new=["date",'latitude', 'longitude','company', 'city', 'state', 'country']
for i in new:
    df2[i]=np.nan





for i in range(593,len(df2)):
    key=df2["jobkey"][i]
    print(str(i))
    if type(key)==float:
        pass
    else:
        try:
            b=df3[df3["jobkey"]==key].reset_index().loc[0,:].to_dict()        
            df2["date"][i]=b["date"]
            df2['latitude'][i]=b['latitude']
            df2['longitude'][i]=b['longitude']
            df2['company'][i]=b['company']
            df2['city'][i]=b['city']
            df2['state'][i]=b['state']
            df2['country'][i]=b['country']
        except KeyError:
            pass

df2.to_csv("jds&skillsV2.csv")

##jobTitles df


df3=pd.read_csv("pilotRoles.csv")


r=list(df3["Role"].unique())

b=list(df3[df3["Role"]==r[1]]["jobtitle"].unique())
",".join(b)

import csv
with open("jtitles.csv","w",newline="") as jfile:
    writer=csv.DictWriter(jfile,fieldnames=["Role","Jobtitles"])
    writer.writeheader()
    for i in r:
        uRow=list(df3[df3["Role"]==i]["jobtitle"].unique())
        writer.writerow({
            "Role":i,
            "Jobtitles":",".join(uRow)            
        })


###cities values
df3[df3["Role"]==r[1]]["city"].value_counts().to_dict()

with open("StateCount.csv","w",newline="") as cFile:
    writer=csv.DictWriter(cFile,fieldnames=["Role","State","Count"])
    writer.writeheader()
    for i in r:
        udict=df3[df3["Role"]==i]["state"].value_counts().to_dict()
        for j in udict.keys():
            writer.writerow({
                "Role":i,
                "State":j,
                "Count":udict[j]
            })


#####SKILLS COUNT
df=pd.read_csv("VectorizedTags.csv")
df=df.drop(["Customer","United States","Timiza"],axis=1)
r=list(df["Role"].unique())

r=list(df["Role"].dropna().unique())
r.sort()
r.remove("Amazon")


df=df.fillna(0)


skls=list(df.columns)
skls.remove('Job Title')
skls.remove('Role')
with open("skillCount.csv","w",newline="") as sFile:
    writer=csv.DictWriter(sFile,fieldnames=["Skill","Count"])
    writer.writeheader()
    for i in skls :
        s=sum(df[i])
        writer.writerow({
            "Skill":i,
            "Count":s
        })
    
####skills similarity



a=df[df["Role"]=="Software Developer"].describe().loc["mean",:]
a=list(a[a>0].index)


roleDict=dict()
for i in r:
    a=df[df["Role"]==i].describe().loc["mean",:]
    a=list(a[a>0].index)
    roleDict.update({
        i:a
    })


len(set(roleDict["Software Developer"]).intersection(set(roleDict["QA Manager"])))
rd=list(roleDict.keys())
ommit50=["Skill","Excel","Data","Test","Programming","Scripting","Security","Analysis","Rest","Restful","Analytics","Strategy","Computer Science","Research","Automation","Automate","Mining","Redis","Concept","Relationships","Relationship","Media","Apis","Customer Service","Databases","Word","Marketing","Risk","Project Management","Architect","Deployment","Growth","Road","Scala","Modeling","Modelling","Finance","Microsoft Office","Flow","Architecture","Consulting","Optimization","Senior","Emails","Creative","Sql","Mobile","Components","Budgeting","Budget","Reliability",]
ommit100=["Excel","Data","Test","Programming","Scripting","Security","Analysis","Rest","Restful","Analytics","Strategy","Computer Science","Research","Automation","Automate","Mining","Redis","Concept","Relationships","Relationship","Media","Apis","Customer Service","Databases","Word","Marketing","Risk","Project Management","Architect","Deployment","Growth","Road","Scala","Modeling","Modelling","Finance","Microsoft Office","Flow","Architecture","Consulting","Optimization","Senior","Emails","Creative","Sql","Mobile","Components","Budgeting","Budget","Reliability","Sass","Credit","Construction","Engagement","Java","Agile","Sales","Machining","Recruitment","Ticketing","Iteration","Emerging","Quality Assurance","Visualization","Mentor","Electronics","Digital","Legal","Diploma","Rust","Scaling","Python","Math","Statistics","Linux","Scale","Javascript","Html","Energy","Country","Assemblies","C","Transport","Transformer","Pressure","Portfolio","Powerpoint","Autocad","Regional","Region","Brand","Workflows","Suppliers","Perl","Mathematics","Influencer","Test Planning","Test Plans","Readiness","Software Engineering","Human Resource","Target","Targets","R","AWS","Web App","Video","Go","Test Cases","Css","Containers"]
def get_df(roleDict,rd,role):
    sdf=pd.DataFrame(columns=["MainRole","Roles","Similarity Count","skills"])
    mskills=list(roleDict[role])
    for i in mskills:
        if i in ommit100:
            mskills.remove(i)
        else:
            pass
    mskills=set(mskills)
    rd.remove(role)
    for j in rd:
        sks=mskills.intersection(set(roleDict[j]))
        count=len(sks)
        sdf=sdf.append({
            "MainRole":role,
            "Roles":j,
            "Similarity Count":count,
            "skills":",".join(sks)
        },ignore_index=True)
    sdf=sdf.sort_values("Similarity Count",ascending=False)
    sdf.reset_index(inplace=True)
    sdf=sdf.drop("index",axis=1)
    mc=sdf['Similarity Count']
    ss=list()
    for i in mc:
        if i<=stat.median(mc):
            n=abs(stat.median(mc)-i)
            n=i-n**1.5
            ss.append(n)
        else:
            n=abs(stat.median(mc)-i)
            n=i+n**.08
            ss.append(n)
    sdf['Weighted']=ss    
    rd.append(role)
    return sdf

a=get_df(roleDict,rd,"Software Engineer")
b=get_df(roleDict,rd,"Drafter")

type(a)
mdf=pd.concat([a,b],ignore_index=True)
dfs=list()
for i in rd:
    a=get_df(roleDict,rd,i)
    dfs.append(a)
    print(rd.index(i))

mdf=pd.concat(dfs,ignore_index=True)
mdf.to_csv("h2.csv",index=False)



import statistics as stat
stat.median(dfs[1]['Similarity Count'])

from matplotlib import pyplot as plt

fig=plt.plot(a['Similarity Count'])
plt.show(fig)

import math
ex=math.exp(dfs[1]['Similarity Count'])
mc=dfs[1]['Similarity Count']

ss=list()
for i in mc:
    if i<=stat.median(mc):
        n=abs(stat.median(mc)-i)
        n=i-n**1.2
        ss.append(n)
    else:
        n=abs(stat.median(mc)-i)
        n=i+n**1.5
        ss.append(n)
fig=plt.plot(ss)
plt.show(fig)

import numpy as np
np.exp()


mdf.to_csv("h50.csv",index=False)





