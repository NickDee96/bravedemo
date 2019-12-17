import requests as req
import csv
import sys



def getjds(role,filename):
    fieldnames=[
        "jobtitle",
        "company",
        "city",
        "state",
        "country",
        "language",
        "formattedLocation",
        "source",
        "date",
        "snippet",
        "url",
        "onmousedown",
        "latitude",
        "longitude",
        "jobkey",
        "sponsored",
        "expired",
        "indeedApply",
        "formattedLocationFull",
        "formattedRelativeTime",
        "stations"]
    url="http://api.indeed.com/ads/apisearch?publisher=9091824477922251&q={}&sort=&radius=&sort=date&jt=&start={}&limit=25&fromage=&filter=1&latlong=1&co={}&chnl=&userip=1.2.3.4&format=json&useragent=Mozilla/%2F4.0(Firefox)&v=2"
    with open(filename,"w",newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for k in ["za","ng","ma","eg"]:
            url1="http://api.indeed.com/ads/apisearch?publisher=9091824477922251&q="+role+"&sort=&radius=&st=&jt=&start=0&limit=25&fromage=&filter=&latlong=1&co="+k+"&chnl=&userip=1.2.3.4&format=json&useragent=Mozilla/%2F4.0(Firefox)&v=2"
            length=req.get(url1).json()["totalResults"]
            print("Collecting for {}".format(k))
            for i in range(0,length,25):
                print(i)
                mUrl=url.format(role,i,k)
                data=req.get(mUrl).json()
                for j in data["results"]:
                    writer.writerow(j)

if __name__ == "__main__":
    role=str(sys.argv[1])
    filename=str(sys.argv[2])
    getjds(role,filename)

import json
import csv
with open("role.json","r",newline="") as rFile:
    roles=json.load(rFile)
    roles=list(roles.keys())

with open("roles.txt","w",newline="\r") as rFile:
    for i in roles:
        rFile.write(i+"\n")

roles


url="https://api.indeed.com/ads/apisearch?publisher=9091824477922251&q={}&sort=&radius=&st=&jt=&start=0&limit=25&fromage=60&filter=1&latlong=1&co={}&chnl=&userip=1.2.3.4&format=json&useragent=Mozilla/%2F4.0(Firefox)&v=2"
with open("jdCountSA.csv","w",newline="") as jFile:
    writer=csv.DictWriter(jFile,fieldnames=["Role","JobCount","Country"])
    writer.writeheader()
    for i in roles:
        for j in ["za","ng","eg","ma"]:
            results=req.get(url.format(i,j)).json()["totalResults"]
            writer.writerow({
                "Role":i,
                "JobCount":results,
                "Country":j
            })
            print("{} {} jobs in {}".format(results,i,j))




import pandas as pd
df=pd.read_csv("jdCountSA.csv").set_index("Role")
d=df.to_dict()["Job Count"]


from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

sa_mask = np.array(Image.open("SAshape.png"))
sa_mask

#def transform_format(valList):
#    valList=list(valList)
#    out=[]
#    for i in valList:
#        if i == 0:
#            out.append(255)
#        else:
#            out.append(i)
#    return out
#
#transformed_sa_mask = np.ndarray((sa_mask.shape[0],sa_mask.shape[1]), np.int32)
#sa_mask[i][1].shape
#for i in range(len(sa_mask)):
#    transformed_sa_mask[i] = [transform_format(sa_mask[i][x]) for x in range(len(sa_mask[i]))]


image_colors = ImageColorGenerator(sa_mask)

wordcloud = WordCloud(width=900,height=500,
                        background_color="white",
                        mode="RGBA",
                        relative_scaling=1,
                        normalize_plurals=False,
                        mask=sa_mask,
                        min_font_size=12
                        ).generate_from_frequencies(d)

plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
plt.axis("off")

plt.savefig("sa_wordcloud.png", format="png")
plt.show()


import plotly
import plotly.graph_objects as go
import pandas as pd

df=pd.read_csv("afDataAn.csv")
df=df.set_index("Role")
df.columns
fig=go.Figure()
colours=["#00E676","#09ACF7","#FF1E91","#5B717A"]
countries=['Egypt', 'Morroco', 'Nigeria', 'South Africa']
for i in range(len(countries)):
    fig=fig.add_trace(
        go.Scatter(
            y=df[countries[i]],
            x=df.index,
            mode="markers",
            name=countries[i],
            marker=dict(
                color=colours[i]
            )
        )
    )
fig.add_trace(
    go.Bar(
        y=df["Average"],
        x=df.index,
        name="General Average",
        error_y=dict(
            type="data",
            array=df["ConfInt"])
    )
)
fig.update_layout(
    hovermode="compare"
)
fig.show()


import chart_studio.plotly as py
import chart_studio
chart_studio.tools.set_credentials_file(username='nick-brave', api_key='S2uZaCyuN8maE8Mq5EuJ')

py.plot(fig, filename = 'African Job Data', auto_open=True)





import requests as req
from bs4 import BeautifulSoup as soup
import csv

url="https://www.indeed.co.za/salaries/mechanical-engineer-Salaries"
page=soup(req.get(url).content,"lxml")
with open("roles.txt","r") as rFile:
    roles=rFile.readlines()
    roles=[x.strip() for x in roles]

len(roles)

i=roles[1]
url="https://www.indeed.co.za/salaries/{}-Salaries"
with open("IndeedSalaries.csv","w",newline="") as sFile:
    writer=csv.DictWriter(sFile,fieldnames=["Role","Job Title","Salary"])
    writer.writeheader()
    for i in roles:
        role=i.lower().replace(" ","+")
        page=soup(req.get(url.format(role)).content,"lxml")
        sal=page.find("div",{"class":"cmp-sal-salary"}).strong.text
        period=page.find("div",{"class":"cmp-sal-salary"}).text.strip(sal).strip()
        sal=sal.strip("R ").replace("\xa0","")
        sal=int(sal)    
        if "month" in period:
            sal=sal*12
        writer.writerow({
            "Role":i,
            "Job Title":i,
            "Salary":sal
        })
        print("{} =>>{} =>> {}".format(i,i,sal))
        try:
            rltdRoles=page.find_all("div",{"class":"cmp-related-title-entry"})
            j=rltdRoles[0]
            for j in rltdRoles:
                title=j.find("div",{"class":"cmp-related-title-entry-jobtitle"}).text
                sSal=j.find("div",{"class":"cmp-related-title-entry-salary"}).strong.text
                sPeriod=j.find("div",{"class":"cmp-related-title-entry-salary"}).text.strip(sSal)
                sSal=sSal.strip("R ").replace("\xa0","")
                sSal=int(sSal)
                if "month" in sPeriod:
                    sSal=sSal*12
                writer.writerow({
                    "Role":i,
                    "Job Title":title,
                    "Salary":sSal
                })
                print("{} =>>{} =>> {}".format(i,title,sSal))            
        except IndexError:
            pass
