from bs4 import BeautifulSoup as soup
import requests as req
import pandas as pd
import csv
import gspread
from gspread.exceptions import APIError
from requests.exceptions.
import time
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('indeedscraper-f298f5bd5f02.json', scope)
client = gspread.authorize(creds)
data=pd.read_csv("pilotRoles.csv")
sheet = client.open('Indeed Jds').sheet1
try:
    df=pd.DataFrame(sheet.get_all_records())
    lastKey=df["jobkey"][len(df)-1]
    a=data[data["jobkey"]==lastKey].index.values
    a=find_nearest(a,len(df))
except IndexError:
    a=0
    header = ["Role","jobtitle","jobkey","jd"]
    sheet.insert_row(header,1)
with open("pilotRolesData.csv","a",newline="") as csvfile:
    writer=csv.DictWriter(csvfile,fieldnames=["Role","jobtitle","jobkey","jd"])
    #writer.writeheader()
    for i in range(a+1,len(data)):
        try:
            page=soup(req.get(data["url"][i]).text,'lxml')
            text=page.find_all('div',{'id':'jobDescriptionText'})[0].text
            text=text.strip().replace("\n"," ").replace("'","").replace('"','').replace(":","")
            writer.writerow({"Role":data["Role"][i],
                            "jobtitle":data["jobtitle"][i],
                            "jobkey":data["jobkey"][i],
                            "jd":text})
            row=[data["Role"][i],data["jobtitle"][i],data["jobkey"][i],text]
            sheet.insert_row(row,i+2)
            time.sleep(1)
            print(i)
        except (IndexError,APIError):
            pass
if __name__ == "__main__":
    scrape()