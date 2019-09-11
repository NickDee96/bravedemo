import nltk
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
import datetime
import multiprocessing as mp
import pandas as pd
import string
from nltk.corpus import stopwords
from oauth2client.service_account import ServiceAccountCredentials
import gspread


skillz=list(pd.read_csv("hardskills.csv")["Tech_Skill"])

porter=PorterStemmer()
wnl=WordNetLemmatizer()
def getDf():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('indeedscraper-f298f5bd5f02.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Indeed Jds').sheet1
    df=pd.DataFrame(sheet.get_all_records())
    return df


df=getDf()



class splitter:
    def __init__(self,text):
        text=text.strip().lower()
        if len(text)<=3:
            self.text=(" "+text+" ")
            self.search_set={self.text}
        else:
            self.text=text
            self.stemmed=porter.stem(text)
            self.lemma=wnl.lemmatize(text)     
            self.search_set={self.text,self.lemma,self.stemmed}

def cleanStrings(text):
    text=str(text)
    text=text.lower()
    text=text.replace("'"," ").replace('"'," ")
    plist=list(string.punctuation)
    plist.remove("#")
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


def text_searcher(doc,skills):
    t1=datetime.datetime.now()
    skills_present=list()
    doc=doc.lower()
    for i in skills:
        #print("searching for {}".format(skills.index(i)))
        search_terms=splitter(i).search_set
        for j in search_terms:
            if j in doc:
                skills_present.append(i.strip())
                break
    t2=datetime.datetime.now()
    time_taken=(t2-t1).total_seconds()
    print("Process took {} seconds".format(round(time_taken,2)))
    return skills_present




text='''Skills we are looking for 

    Strong Javascript Skills Strong HTML and CSS skills
    Experience with client side frameworks (Angular, Ionic, React, React Native) 
    Proficiency in Nodejs
    Proficiency in ES6
    A Clear understanding of modern Javascript tools like Gulp, NPM, Yarn, Webpack, Modernizr. 
    Understanding of git and continuous integration and deployment practices. 
    Familiarity with good UI/UX practices 
    Strong analytical and problem-solving skills 
    Ability to communicate fluently in English 


Bonus Points: 

    Experience working with Firebase
    Understanding of Progressive Web Apps 
    Experience working with Android / iOS apps 
    Experience using project management tools like Visual Studio Team Services
    Experience working with cloud services like GCP, Azure, AWS 
'''


a=list()
for i in range(len(df)):
    a=a+text_searcher(cleanStrings(df["jd"][i]),skillz)
    a=list(set(a))
    print("Got for {}".format(i))


a=set(a)
with open("tags.txt","w",newline="") as textFile:
    for i in a:
        textFile.write(i+"\n")



a=list()

with open("tags.txt","r",newline="")as tfile:
    a=tfile.readlines()
a=[i.strip() for i in a]


mDf=pd.DataFrame(columns=(list(a)+["Role","Job Title"]))
for i in range(len(df)):
    b=text_searcher(cleanStrings(df["jd"][i]),a)
    upDateDict=dict()
    print("Getting for {}".format(i))
    for j in b:
        upDateDict.update({j:1})
    upDateDict.update({
        "Role":df["Role"][i],
        "Job Title":df['jobtitle'][i]
    })
    mDf=mDf.append(upDateDict,ignore_index=True)

mDf.to_csv("VectorizedTags.csv",index=False)

finalDf=mDf.fillna(0)
finalDf=finalDf.set_index("Role")
finalDf.to_csv("VectorizedTags2.csv",index=False)
