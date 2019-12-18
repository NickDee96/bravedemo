from nltk.stem import WordNetLemmatizer
import pandas as pd
import csv
df=pd.read_csv("tags/Tech practices.csv",header=None,names=["Tech Practice","Category"])

wnl=WordNetLemmatizer()
wnl.lemmatize("best")
with open("lemmatized.csv","w",newline="") as lFile:
    writer=csv.DictWriter(lFile,fieldnames=["Tech process","Category"])
    writer.writeheader()
    skillz=[]
    for i in range(len(df)):
        if i in skillz:
            pass
        else:
            lmtz=wnl.lemmatize(df["Tech Practice"][i].lower())
            skillz.append(skillz)
            writer.writerow({
                "Tech process":lmtz,
                "Category":df["Category"][i],
            })
        print(i)

wnl.lemmatize("accountant")