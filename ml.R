library(factoextra)
library(NbClust)
library(janitor)
df<-read.csv("unigram.csv")

rownames(df)<-df$Role
df<-within(df,rm(Role))
df<-remove_empty_cols(df)

#df<-as.data.frame(t(df))
df[is.na.data.frame(df)]<-0


#estimating optimum number of clusters
df <- as.data.frame(scale(df))
df[is.na.data.frame(df)]<-0

# Compute dissimilarity matrix
res.dist <- dist(df, method = "euclidean")

# Compute hierarchical clustering
res.hc <- hclust(res.dist, method = "ward.D2")

# Visualize
fviz_dend(res.hc,rect = TRUE)
plot(res.hc, cex = 0.7)


df[is.na.data.frame(df)]<-0
res.km <- eclust(df, "kmeans", nstart = 25)

res.km<-kmeans(df,6,25)

fviz_cluster(res.km,df,ellipse.type = "t")


res.hc <- eclust(df, "hclust") # compute hclust

fviz_dend(res.hc)






