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

def getDf():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('indeedscraper-f298f5bd5f02.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Indeed Jds').sheet1
    df=pd.DataFrame(sheet.get_all_records())
    return df


df=getDf()


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


se=df[df["Role"]=="Software Developer"]

jtitles=se["jobtitle"].apply(cleanStrings)

fJtitles=getFeatureNames(jtitles,20,(2,3))
fJtitles

jDs=se["jd"].apply(cleanStrings)
fjDs=getFeatureNames(jDs,50,(2,3))

fjDs

