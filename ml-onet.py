import pandas as pd
import gspread
import plotly
from matplotlib import pyplot as plt
from oauth2client.service_account import ServiceAccountCredentials
from sklearn.feature_extraction.text import TfidfVectorizer 
import re
import nltk
from nltk import PorterStemmer as pstemmer
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
import string
import math

def getDf():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('indeedscraper-f298f5bd5f02.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Indeed Jds').sheet1
    df=pd.DataFrame(sheet.get_all_records())
    return df


df=getDf()


a=plt.plot(df["Role"].value_counts())





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

df["Role"].value_counts()
rName="Software Engineer"
se=df[df["Role"]==rName]

jtitles=se["jobtitle"].apply(cleanStrings)
fJtitles=getFeatureNames(jtitles,20,(2,3))


def getTitleMetrics(rName):
    se=df[df["Role"]==rName]
    jtitles=se["jobtitle"].apply(cleanStrings)
    fJtitles=getFeatureNames(jtitles,20,(2,3))
    counts=getCountDict(fJtitles,jtitles)
    return counts

def get_title_plot(counts):
    fig = go.Figure(data=[go.Pie(labels=list(counts.keys()), values=list(counts.values()))])
    fig.update_traces(hole=.5)
    fig.update_layout(
        title_text="Job titles associated with {}".format(rName),
        # Add annotations in the center of the donut pies.
        annotations=[dict(text=rName, x=0.5, y=0.5, font_size=20, showarrow=False)])
    return fig




jds=se["jd"].apply(cleanStrings)
fJds1=getFeatureNames(jds,50,(1,1))
fJds2=getFeatureNames(jds,50,(2,2))
fJds3=getFeatureNames(jds,50,(3,3))




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

counts=getCountDict(fJtitles,jtitles)

#counts=getCountDict(fJds3,jds)



import plotly.graph_objects as go


fig = go.Figure(data=[go.Pie(labels=list(counts.keys()), values=list(counts.values()))])
fig.update_traces(hole=.5)
fig.update_layout(
    title_text="Job titles associated with {}".format(rName),
    # Add annotations in the center of the donut pies.
    annotations=[dict(text=rName, x=0.5, y=0.5, font_size=20, showarrow=False)])

fig.show()

fig.write_html("test.html")


roles=list(df["Role"].value_counts().index)


tagDict=dict()
unigram=set()
bigram=set()
trigram=set()
for i in roles:
    if i=="":
        pass
    else:
        se=df[df["Role"]==i]
        jds=se["jd"].apply(cleanStrings)
        fJds1=getFeatureNames(jds,100,(1,1))
        fJds2=getFeatureNames(jds,100,(2,2))
        fJds3=getFeatureNames(jds,100,(3,3))
        tagDict.update({
            i:{
                "unigram":fJds1,
                "bigram":fJds2,
                "trigram":fJds3
            }}
        )
        unigram=unigram.union(fJds1)
        bigram=bigram.union(fJds2)
        trigram=trigram.union(fJds3)
        print(i)


len(trigram)

unidf=pd.DataFrame(columns=list(unigram))
bidf=pd.DataFrame(columns=list(bigram))
tridf=pd.DataFrame(columns=list(trigram))

for i in roles:
    if i =="":
        pass
    else:
        se=df[df["Role"]==i]
        jds=se["jd"].apply(cleanStrings)
        fJds1=getFeatureNames(jds,50,(1,1))
        fJds2=getFeatureNames(jds,50,(2,2))
        fJds3=getFeatureNames(jds,50,(3,3))
        counts1=getCountDict(fJds1,jds)
        counts1.update({"Role":i})
        counts2=getCountDict(fJds2,jds)
        counts2.update({"Role":i})
        counts3=getCountDict(fJds3,jds)
        counts3.update({"Role":i})
        unidf=unidf.append(counts1,ignore_index=True)
        bidf=bidf.append(counts2,ignore_index=True)
        tridf=tridf.append(counts3,ignore_index=True)
        print(i)

unidf.to_csv("unigram.csv",index=False)
bidf.to_csv("bigram.csv",index=False)
tridf.to_csv("trigram.csv",index=False)


#Feature Analysis

#unidf=pd.read_csv("unigram.csv")
#bidf=pd.read_csv("bigram.csv")
#tridf=pd.read_csv("trigram.csv")

unidf=unidf.fillna(0)
unidf.set_index("Role",inplace=True)
unidf=unidf.transpose()

cor = unidf.corr() #Calculate the correlation of the above variables
import seaborn as sns
sns.heatmap(cor, square = True)

from sklearn.cluster import KMeans


kmeans = KMeans(n_clusters=4)
kmeans.fit(unidf)
y_kmeans = kmeans.predict(unidf)


plt.scatter(unidf[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='white', s=200, alpha=0.5)


sum(unidf.iloc[0])







x=unidf[unidf["Software Engineer"]>=1]["Software Engineer"]
fig = go.Figure()
fig.add_trace(go.Scatter(x=x.index,y=x,mode='markers'))
fig.write_html("test.html")

import json
f=open("roles&tags.json","w")
f.write(json.dumps(tagDict,indent=2))
f.close()








