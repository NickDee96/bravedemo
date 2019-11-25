import requests as req
from bs4 import BeautifulSoup as soup
import pandas as pd
import random
from datetime import datetime, timedelta
import csv
ska=pd.read_csv("roles.csv")
techSkills=pd.read_csv("tech_skillz.csv")
skillCount=techSkills['tech_skill'].value_counts()
skillDf=pd.DataFrame(skillCount).reset_index()
skillDf.columns=["tech_skill","count"]
skills=list(skillDf["tech_skill"])

r=list(ska["Role"].value_counts().index)
countrycodes=pd.read_csv("country_codes_indeed.csv")


def getHeaders():
    headers=(
        {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'},
        {'user-agent':'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'},
        {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'},
        {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'},
        {'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'},
        {'user-agent':'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot; http://www.jobboerse.com/bot.htm) Gecko/20100101 Firefox/38.0'},
        {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'},
        {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'},
        {'user-agent':'Mozilla/5.0 (X11; od-database-crawler) Gecko/20100101 Firefox/52.0'},
        {'user-agent':'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.16) Gecko/20110323 Ubuntu/10.04 (lucid) Firefox/3.6.16'},
    )
    return random.choice(headers)

with open("GeoJobs.csv","w",newline="") as geoFile:
    writer=csv.DictWriter(geoFile,fieldnames=["Role","Country","Count"])
    for i in r:
        rolename=i.split(",")[0].replace(" ","+")
        for j in range(len(countrycodes)):
            try:
                print("Getting for {} in {}".format(i,countrycodes["Country"][j]))
                url="https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={}&sc.keyword={}&locT=N&locId={}&jobType=".format(rolename,rolename,countrycodes["Code"][j])
                page=soup(req.get(url,headers=getHeaders()).text,"lxml")
                jCount=int(page.find_all("p",{"class":"jobsCount"})[0].text.split("\xa0")[0].replace(",",""))
                writer.writerow(
                    {
                        "Role":i,
                        "Country":countrycodes["Country"][j],
                        "Count":jCount
                    }
                )
            except IndexError:
                pass
        


