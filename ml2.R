library(factoextra)
library(NbClust)
library(janitor)

vectDf<-read.csv("VectorizedTags.csv")
#vectDf<-within(vectDf,rm(Role))
vectDf<-within(vectDf,rm(`Job.Title`))
#vectDf<-as.data.frame(t(vectDf))

vectDf<-remove_empty_cols(vectDf)
#vectDf <- as.data.frame(scale(vectDf))
vectDf[is.na.data.frame(vectDf)]<-0

# Compute dissimilarity matrix
#res.dist <- dist(vectDf, method = "euclidean")

# Compute hierarchical clustering
#res.hc <- hclust(res.dist, method = "ward.D2")


summary(vectDf)

res.km<-kmeans(vectDf,4,25)

fviz_cluster(res.km,vectDf)

kdf<-cbind(vectDf,res.km$cluster)



cKdf<-kdf[kdf$"res.km$cluster"==4,]
cKdf<-within(cKdf,rm("res.km$cluster"))
cKdf<-remove_empty(cKdf,"rows")


cKdf<-cKdf[ , apply(cKdf, 2, var) != 0]





res1.km<-kmeans(cKdf,10,25)

####Kmeans with means


unique(vectDf$Role)[1]
a<-vectDf[vectDf$Role==unique(vectDf$Role)[1],]
a<-within(a,rm(Role))
b<-as.data.frame(colMeans(a))
colnames(b)<-unique(vectDf$Role)[1]
d<-vectDf[vectDf$Role==unique(vectDf$Role)[2],]
d<-within(d,rm(Role))
e<-as.data.frame(colMeans(d))
colnames(e)<-unique(vectDf$Role)[2]
f<-cbind.data.frame(b,e)

for (i in 3:length(unique(vectDf$Role))) {
  d<-vectDf[vectDf$Role==unique(vectDf$Role)[i],]
  d<-within(d,rm(Role))
  e<-as.data.frame(colMeans(d))
  colnames(e)<-unique(vectDf$Role)[i]
  f<-cbind.data.frame(f,e)
  
}

write.csv(f,"kmeansVECTHS.csv")

f<-f[ apply(f, 2, var) != 0,]
f<-f[ ,apply(f, 2, var) != 0]
res.km<-kmeans(f,4,25)


fviz_cluster(res.km,f)

f<-cbind(f,res.km$cluster)
g<-f[f$`res.km$cluster`==3,]
g<-within(g,rm("res.km$cluster"))



g<-as.data.frame(t(g))
res.km<-kmeans(g,3,25)

library(corrplot)
library(tidyverse)
corrplot(cor(g))
ggpairs(data)

fviz_cluster(res.km,g)

res.dist <- dist(g, method = "euclidean")

# Compute hierarchical clustering
res.hc <- hclust(res.dist, method = "ward.D2")

# Visualize
fviz_dend(res.hc,rect = TRUE)
plot(res.hc, cex = 0.8,main = "Cluster Dendrogram",xlab = "Role",leaflab = "none")






#####Naive Bayes Classifier

vectDf<-read.csv("VectorizedTags.csv")
#vectDf<-within(vectDf,rm(Role))
vectDf<-within(vectDf,rm(`Job.Title`))
#vectDf<-as.data.frame(t(vectDf))

vectDf<-remove_empty_cols(vectDf)
#vectDf <- as.data.frame(scale(vectDf))
vectDf[is.na.data.frame(vectDf)]<-0


library(e1071)
index<-sample(1:nrow(vectDf),.75*nrow(vectDf))
train<-vectDf[index,]
test<-vectDf[-index,]
nbFit<-naiveBayes(Role~.,data=train)

default_pred <- predict(nbFit, newdata = test)


table(default_pred)







