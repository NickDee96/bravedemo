import requests as req
from bs4 import BeautifulSoup as soup

url=""

with open("roles.txt","r") as rFile:
    roles=rFile.readlines()
    roles=[x.strip() for x in roles]

roles
codes={
    "South Africa":211,
    "Nigeria":177,
    "Morocco":162,
    "Egypt":69
}

from bs4 import BeautifulSoup as soup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv
driver=webdriver.Firefox()
driver.get("https://www.glassdoor.com/profile/login_input.htm")

cookie="0000016ef48d2236a05cb71aef975917"
driver.add_cookie({
        "name": "_uac",
        "value": cookie,
        "domain":".www.glassdoor.com"
    })


driver.get("https://www.glassdoor.com/Salaries/south-africa-analyst-salary-SRCH_IL.0,12_IN211_KO13,20.htm")

with open("salaryData.csv","a",newline="") as sFile:
    writer=csv.DictWriter(sFile,fieldnames=["Role","Country","Salary","Per"])
    #writer.writeheader()
    for k in range(57,len(roles)):
        for j in ["South Africa","Nigeria","Morocco","Egypt"]:
            driver.find_element_by_css_selector("#sc\.keyword").clear()
            driver.find_element_by_css_selector("#sc\.keyword").send_keys(roles[k])

            driver.find_element_by_css_selector("#sc\.location").clear()

            driver.find_element_by_css_selector("#sc\.location").send_keys(j)
            driver.find_element_by_css_selector("#HeroSearchButton > span:nth-child(1)").click()

            page=soup(driver.execute_script("return document.body.innerHTML"),"lxml")
            try:
                salary=page.find("span",{"data-test":"AveragePay"}).text.replace(",","")
                per=page.find("span",{"class":"occMedianModule__OccMedianBasePayStyle__yearLabel"}).text
            except AttributeError:
                salary="NA"
                per="NA"
            writer.writerow({
                "Role":roles[k],
                "Country":j,
                "Salary":salary,
                "Per":per
            })
            print("{} in {} =>> {} {}".format(roles[k],j,salary,per))


## Data Nomarlization
import pandas as pd
import numpy as np
df=pd.read_csv("sDataUpdated.csv")

df.columns
rates={
    "South Africa":0.068,
    "Nigeria":0.0028,
    "Morocco":0.10,
    "Egypt":0.062
}

yEarnings=[]
for i in range(len(df)):
    sal=df["Salary"][i]
    if df["Per"][i] is not np.nan:
        country=df["Country"][i]
        if "K" in str(sal):
            sal=int(sal.strip("K"))*1000
        eSal=int(sal)*rates[country]
        if df["Per"][i]=="mo":
            eSal=eSal*12
        yEarnings.append(eSal)
    else:
        yEarnings.append(sal)
    print(sal)

df["Yearly Earnings"]=yEarnings

df.to_csv("sdataUPdated2.csv",index=False)