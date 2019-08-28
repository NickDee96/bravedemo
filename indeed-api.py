import requests as req
import csv
import sys
import pandas as pd
def getjds(role,filename,length):
    fieldnames=["Role","Country","Count"]
    url="http://api.indeed.com/ads/apisearch?publisher=9091824477922251&q={}&sort=&radius=&st=&jt=&start={}&limit=25&fromage=&filter=&latlong=1&co=us&chnl=&userip=1.2.3.4&format=json&useragent=Mozilla/%2F4.0(Firefox)&v=2"
    with open(filename,"w",newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0,length,25):
            mUrl=url.format(role,i)
            data=req.get(mUrl).json()
            for j in data["results"]:
                writer.writerow(j)
            print(i) 

if __name__ == "__main__":
    role=str(sys.argv[1])
    filename=str(sys.argv[2])
    length=int(sys.argv[3])
    getjds(role,filename,length)     