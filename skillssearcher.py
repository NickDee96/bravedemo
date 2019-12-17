import nltk
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
import datetime
import pandas as pd
import string
from nltk.corpus import stopwords
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import csv

##Loading the rawtags
#with open("tags/stackOtags.txt","r") as tFile:
#    tags=tFile.readlines()
#    skillz=[x.strip() for x in tags]
#
skillz=list(pd.read_csv("tags/hs-new-list.csv")["name"])


##Initializing the port stemmer and lemmatizer classes
porter=PorterStemmer()
wnl=WordNetLemmatizer()

def getDf():
    '''
    This function gets job descriptions from the JDs google sheet  and returns a pandas Dataframe
    '''
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('indeedscraper-f298f5bd5f02.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Indeed Jds').sheet1
    df=pd.DataFrame(sheet.get_all_records())
    return df


df=getDf()



class splitter:
    '''
    This class produces the text entered in three types; stemmed, lemmatized and lowercase text for searching. It returns as set of the three
    '''
    def __init__(self,text):
        text=text.strip().lower()
        ##text is separated based on it's lenght so as to take into consideration tags such as C and R from appearing in any text.
        if len(text)<=3:
            self.text=(" "+text+" ")
            self.search_set={self.text}
        else:
            self.text=" {} ".format(text)
            self.stemmed=porter.stem(text)
            self.lemma=wnl.lemmatize(text)     
            self.search_set={self.text,
                                #self.lemma,
                                #self.stemmed
                                }

def cleanStrings(text):
    '''
    This function cleans up text
    '''
    ##setting the text to an absolute string datatype
    text=str(text)
    ## Sets the text to lowercase
    text=text.lower()
    ## loading the punctuation list
    plist=list(string.punctuation)
    ## removing  # and + due to some skill having those characters
    plist.remove("#")
    plist.remove("+")
    ## removing punctuation from the text
    for j in plist:
        if j in plist:
            text=text.replace(j," ")
    ##removing the stopwords
    stop_words=stopwords.words('english')
    ## splitting the text to a list for stopword removal
    text1=text.split(' ')
    text2=list()
    for i in text1:
        if i not in stop_words:
            text2.append(i)
    ## rejoining the text
    return ' '.join(text2)


def text_searcher(doc,skills):
    ''' This function searches for skills in text. The input is a string to be searched in and a list of skills.
        It returns a list of skills present in the text
    '''
    ##Introduced time to track how long the function runs due to the change of tags list that normally occurs
    tStart=datetime.datetime.now()
    #Initialized an empty list for the skill to append to
    skills_present=list()
    doc=doc.lower()
    for i in skills:
        #print("searching for {}".format(skills.index(i)))
        i=i.replace("-"," ")
        #initilizing the splitter class
        search_terms=splitter(i).search_set
        for j in search_terms:
            if j in doc:
                skills_present.append(i.strip())
                break
    tEnd=datetime.datetime.now()
    ##Calcuting the duration
    duration=(tEnd-tStart).total_seconds()
    ##Printing the time taken for the function to run
    print("Process took {} seconds".format(round(duration,2)))
    return skills_present


def filter_tags(output_filename,taglist,text_array):
    '''
    This function searches for the raw skills in all of the jd's and returns only the skills present in the jds.
    It's a filtering mechanism so as to reduce the time it takes to vectorize the text.
    '''
    rTags=list()
    j=0
    for i in text_array:
        ##merge the text
        rTags=rTags+text_searcher(cleanStrings(i),taglist)
        rTags=list(set(rTags))
        print("Got for {}".format(j))
        j=j+1
    rTags=list(set(rTags))
    #sorting the list from A-Z
    rTags.sort()
    ##Writing the tags into a text file
    with open(output_filename,"w",newline="") as textFile:
        for i in rTags:
            textFile.write(i+"\n")






filter_tags("tags/stags2.txt",skillz,df.jd)

def get_filtered_tags(filename):
    a=list()
    with open(filename,"r",newline="")as tfile:
        a=tfile.readlines()
    a=[i.strip() for i in a]
    return a

fTags=get_filtered_tags("tags/stags2.txt")

def get_Vectorized_df(filename,tags):
    #Initializing the writer
    with open(filename,"w",newline="") as vFile:
        writer=csv.DictWriter(vFile,fieldnames=["Role","Job Title"]+list(tags))
        #writing the header row
        writer.writeheader()
        for i in range(len(df)):
            tStart=datetime.datetime.now()
            ##searching for the tags in text
            taglist=text_searcher(cleanStrings(df["jd"][i]),tags)
            ## Initializing an empty dictionary to update the tags
            upDateDict=dict()
            print("Getting for {}".format(i))
            ##Creating a dictionary to update the csv where 1 means a skill was found in the text
            for j in taglist:
                upDateDict.update({j:1})
            ## Merging the Role name and job title into the dictionary
            upDateDict.update({
                "Role":df["Role"][i],
                "Job Title":df['jobtitle'][i]
            })
            writer.writerow(upDateDict)
            tEnd=datetime.datetime.now()
            time_taken=(tEnd-tStart).total_seconds()
            print("Main Process took {} seconds".format(round(time_taken,2)))

get_Vectorized_df("data/VectorizedTags3.csv",fTags)

a="test-setting"
aS=splitter(a).search_set

text= " ".join(df.jd)
ct=cleanStrings(text)
len(ct)

ct

fTags[24].lower() in ct

countList=[]
for i in fTags:
    count=ct.count(" {} ".format(i.lower()))
    countList.append(count)
    print("{} ==> {}".format(i,count))

countDf=pd.DataFrame(data={
    "Skill":fTags,
    "Count":countList
})
countDf.to_csv("data/SkillCount-flatlist.csv",index=False)

countDf

import pandas as pd
df1=pd.read_csv("data/VectorizedTags3.csv").dropna(how="all",axis=1)## A Vectorized tag dataFrame for US data
df1.sum()s
