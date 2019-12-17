import pandas as pd
from datetime import datetime

from skillssearcher import filter_tags
from skillssearcher import *

sdData=pd.read_csv("soft-dev.csv")
jds=pd.read_csv("softdevjds.csv")


def cleanDate(text):
    date=text.split(", ")[1].strip(" GMT")
    date=" ".join(date.split(" ")[:3])
    date=datetime.datetime.strptime(date,"%d %b %Y")
    return date.strftime("%b %Y")


sdData["date"]=sdData["date"].apply(cleanDate)
sdData.drop_duplicates(subset ="jobkey", 
                     keep = False, inplace = True) 
jds.drop_duplicates(subset ="jobkey", 
                     keep = False, inplace = True) 



mgd=pd.merge(left=sdData,right=jds,how="left",left_on="jobkey",right_on="jobkey")
mgd.dropna(subset=['jobkey'], inplace=True)

mgd.to_csv("Software Developer data.csv",index=False)

df=mgd

##Loading the rawtags
with open("tags/tags.txt","r") as tFile:
    tags=tFile.readlines()
    skillz=[x.strip() for x in tags]

len(tags)

filter_tags("sdevtags2.txt",skillz,jds["jds"])
tags=get_filtered_tags("sdevtags2.txt")

#Initializing the writer
with open("sdVectorized.csv","w",newline="") as vFile:
    writer=csv.DictWriter(vFile,fieldnames=["Job Title","jobkey"]+list(tags))
    #writing the header row
    writer.writeheader()
    for i in range(len(df)):
        tStart=datetime.datetime.now()
        ##searching for the tags in text
        taglist=text_searcher(cleanStrings(df["jds"][i]),tags)
        ## Initializing an empty dictionary to update the tags
        upDateDict=dict()
        print("Getting for {}".format(i))
        ##Creating a dictionary to update the csv where 1 means a skill was found in the text
        for j in taglist:
            upDateDict.update({j:1})
        ## Merging the Role name and job title into the dictionary
        upDateDict.update({
            "jobkey":df["jobkey"][i],
            "Job Title":df['jobtitle'][i]
        })
        writer.writerow(upDateDict)
        tEnd=datetime.datetime.now()
        time_taken=(tEnd-tStart).total_seconds()
        print("Main Process took {} seconds".format(round(time_taken,2)))


vectDf=pd.read_csv("sdVectorized.csv")

sumDf=(vectDf.drop(["jobkey","Job Title"],axis=1).sum()/len(vectDf)).to_frame()
sumDf.reset_index(inplace=True)
sumDf.columns=["skill","ratio"]
sumDf=sumDf.sort_values("ratio",ascending=False)
sumDf=sumDf.reset_index(drop=True)


sumDf.to_csv("sumdf2.csv",index=False)


fDf=pd.merge(vectDf,mgd[["jobkey","date"]],how="inner",left_on="jobkey",right_on="jobkey")

fDf["date"].sort_values(ascending=False)
i=fDf["date"].unique()[1]

monthsdf=pd.DataFrame()
months=pd.Index(['Jun 2019','Jul 2019','Aug 2019','Sep 2019','Oct 2019','Nov 2019','Dec 2019'],"index")
for i in months:
    mData=fDf.drop(["Job Title","jobkey"],axis=1)
    mseries=(mData[mData["date"]==i].drop(["date"],axis=1).sum()/len(mData[mData["date"]==i]))*100
    monthsdf=monthsdf.append(mseries,ignore_index=True)
monthsdf=(monthsdf.set_index(months)).transpose().sort_values("Dec 2019",ascending=False)
monthsdf.reset_index()
monthsdf.to_csv("monthsdf.csv")




## LOCATION ANALYSYIS
import csv

with open("sdevLocData.csv","w",newline="") as lfile:
    writer=csv.DictWriter(lfile,fieldnames=["City","Latitude","Longitude","Job Count"])
    writer.writeheader()
    for i in sdData["city"].unique():
        lat=sdData[sdData["city"]==i]["latitude"].mean()
        lon=sdData[sdData["city"]==i]["longitude"].mean()
        count=len(sdData[sdData["city"]==i])
        writer.writerow({
            "City":i,
            "Latitude":lat,
            "Longitude":lon,
            "Job Count":count

        })

###Skills vs location

sDf=pd.merge(vectDf,mgd[["jobkey","date"]],how="inner",left_on="jobkey",right_on="jobkey")

mgd.country