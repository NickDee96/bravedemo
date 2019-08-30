import nltk
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
import datetime
import multiprocessing as mp
with open("LinkedInskills.txt") as skillsfile:
    skills=skillsfile.readlines()

porter=PorterStemmer()
wnl=WordNetLemmatizer()



class splitter:
    def __init__(self,text):
        text=text.strip().lower()
        self.stemmed=porter.stem(text)
        self.lemma=wnl.lemmatize(text)
        self.text=text        
        self.search_set={self.stemmed,self.text,self.lemma}

def text_searcher(doc):
    t1=datetime.datetime.now()
    skills_present=list()
    for i in skills:
        print("searching for {}".format(skills.index(i)))
        search_terms=splitter(i).search_set
        for j in search_terms:
            j=(" "+j+" ") 
            if j in doc:
                skills_present.append(i.strip())
                break
    t2=datetime.datetime.now()
    time_taken=(t2-t1).total_seconds()
    print("Process took {} seconds".format(round(time_taken,2)))
    return skills_present




text='''
    numpy.nancumprod() in Python
    Machine Learning in C++
    Top Career Paths in Machine Learning
    Top 10 Algorithms every Machine Learning Engineer should know
    Python | Speech recognition on large audio files
    Handwritten Equation Solver in Python
    ML | Training Image Classifier using Tensorflow Object Detection API
    How to approach a Machine Learning project : A step-wise guidance
    How to use Google Colab
    5 Machine Learning Projects to Implement as a Beginner
    ML | Implement Face recognition using k-NN with scikit-learn
    30 minutes to machine learning
    The true story about Facebook's closed AI Wing
    DBSCAN Clustering in ML | Density based clustering
    ML | Semi-Supervised Learning
    Python | Linear Regression using sklearn
    ML | Reinforcement Learning Algorithm : Python Implementation using Q-learning
    ML | Rainfall prediction using Linear regression
    The Hathaway Effect : Does The Anne Hathaway effect really true?
    ML | Logistic Regression using Python
    ML | K-Medoids clustering with example
    Bag of words (BoW) model in NLP
    Regularization in Machine Learning
    Random Forest Regression in Python
    Processing text using NLP | Basics
    Implementing Apriori algorithm in Python
    ML | One Hot Encoding of datasets in Python
    ML | Dummy variable trap in Regression Models
    Image compression using K-means clustering
    Combining IoT and Machine Learning makes our future smarter




Article Tags : Machine Learning
Python
Practice Tags : Machine Learning'''

search_terms=splitter(skills[100]).search_set



pool=mp.Pool(mp.cpu_count())

search_terms=[pool.apply(text_searcher(text))]



def text_searcher1(skill,doc):
    print("searching for {}".format(skills.index(skill)))
    search_terms=splitter(skill).search_set
    for j in search_terms:
        j=(" "+j+" ") 
        if j in doc:
            return skill
            break

pool=mp.Pool(mp.cpu_count())
t1=datetime.datetime.now()
d=[pool.apply(text_searcher1,args=(i,text))for i in skills]
t2=datetime.datetime.now()
time_taken=(t2-t1).total_seconds()
pool.close()
print("Process took {} seconds".format(round(time_taken,2)))

for i in skills:
    print(text_searcher1(i,text))