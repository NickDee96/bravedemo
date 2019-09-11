library(factoextra)
library(NbClust)
library(janitor)
mdf<-read.csv("indeedjds.csv")

df<-read.csv("unigram.csv")

unique(mdf$Role)

rownames(df)<-df$Role
df<-within(df,rm(Role))
df<-remove_empty_cols(df)

df<-as.data.frame(t(df))
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
nodePar <- list(lab.cex = 0.6, pch = c(NA, 19), 
                cex = 0.7, col = "blue")
plot(res.hc, cex = 0.8,main = "Bigram Cluster Dendrogram",xlab = "Role",
     nodePar=nodePar,leaflab = "none")




library(ape)

plot(as.phylo(res.hc), type = "fan")


nodePar <- list(lab.cex = 0.6, pch = c(NA, 19), 
                cex = 0.7, col = "blue")
# Customized plot; remove labels
plot(res.hc, ylab = "Height", nodePar = nodePar, leaflab = "none")



df[is.na.data.frame(df)]<-0
#res.km <- eclust(df, "kmeans", nstart = 25)

res.km<-kmeans(df,4,25)

df<-cbind(df,res.km$cluster)

res.km$cluster

write.csv(df,"kmeansUnigram.csv")

a<-fviz_cluster(res.km,df,main = "Unigram tags kmeans cluster")
a
ggsave(a,filename = "uni.png",device = "png",dpi = 1000,width = 10,height = 6)


res.hc <- eclust(df, "hclust") # compute hclust

fviz_dend(res.hc)






