#import data
full_music_data <- read.csv("~/Downloads/2021_MCM-ICM_Problems/2021_ICM_Problem_D_Data/full_music_data.csv")
View(full_music_data)
influence_data <- read.csv("~/Downloads/2021_MCM-ICM_Problems/2021_ICM_Problem_D_Data/influence_data.csv")
View(influence_data)
data_by_artist <- read.csv("~/Downloads/2021_MCM-ICM_Problems/2021_ICM_Problem_D_Data/data_by_artist.csv")
View(data_by_artist)
data_by_year <- read.csv("~/Downloads/2021_MCM-ICM_Problems/2021_ICM_Problem_D_Data/data_by_year.csv")
View(data_by_year)
#remove unneeded columns from influence data, reorder columns
colnames(influence_data)
influence2 <- influence_data[, c(1, 5, 2, 3, 4, 6, 7, 8)]
View(influence2)



library("igraph")

#reorder artist columns
colnames(data_by_artist)
colnames(data_by_artist_with_genre)
artists2 <- data_by_artist_with_genre

#descriptive statistics: number of influencers/followers in each genre
count(influence_data, vars = "influencer_main_genre", wt_var = NULL)
count(influence_data, vars = "follower_main_genre", wt_var = NULL)

table(unlist(data_by_artist_with_genre$artist_genre))

#Artist The New Pornographers are not included in the artist data, so we omit 
#them from the influence data as well in order to create a network graph
influence3 <- influence2[ -seq( from=22470, length.out=18, by=1), ]

#create network graph
net1 <- graph_from_data_frame(d=influence3, vertices=artists2, directed=T) 
V(net1)$artist_genre <- artists2$artist_genre
V(net1)$active_start <- artists2$active_start
V(net1)$danceability <- artists2$danceability
V(net1)$energy <- artists2$energy
V(net1)$valence <- artists2$valence
V(net1)$tempo <- artists2$tempo
V(net1)$loudness <- artists2$loudness
V(net1)$key <- artists2$key
V(net1)$acousticness <- artists2$acousticness
V(net1)$instrumentalness <- artists2$instrumentalness
V(net1)$liveness <- artists2$liveness
V(net1)$speechiness <- artists2$speechiness
V(net1)$duration_ms <- artists2$duration_ms
V(net1)$popularity <- artists2$popularity
V(net1)$count <- artists2$count

#plot network graph
plot(net1, vertex.shape="none", vertex.label=V(net1)$artist_name, 
     vertex.label.font=2, vertex.label.color="gray40",
     vertex.label.cex=.7, edge.color="gray85", edge.arrow.size=.2)

##Finding characteristics of initial network graph

is_simple(net1)
#YES, the graph is simple--there are no loops and there are no multi-edges, as expected

is_connected(net1)
#NO, the graph is not connected. There are multiple components.

clusters(net1)
##There are 3 connected components--one of size 5598, and two each of size 2. 

diameter(net1)
#The diameter is 29--thus the farthest apart that any two vertices are from each other is 29. 

#We decompose the network graph so that we focus on the largest component and ignore the other disconnected
#components.
net2 <- decompose(net1)
table(sapply(net2, vcount))

#artists3.gc is the new graph of the largest component
artists3.gc <- decompose(net1)[[1]]
component2.gc <- decompose(net1)[[2]]
component3.gc <- decompose(net1)[[3]]

mean_distance(artists3.gc)
#The average path length between artists in giant component is 6.164167
diameter(artists3.gc)
#Diameter is still 29
transitivity(artists3.gc)
#Transitivitiy is 0.08915717, so fairly low level of clustering

is_connected(artists3.gc)
#artists3.gc is connected, so why is the vertex connectivity 0?

is_connected(artists3.gc, mode = c("weak"))
#yes, weakly connected
is_connected(artists3.gc, mode = c("strong"))
#no, not strongly connected
net1components <- components(net1, mode = c("strong"))
table(net1components$csize)
#see Excel spreadsheet for table

artists3components <- components(artists3.gc, mode = c("strong"))
table(artists3components$csize)

reciprocity(artists3.gc)
#The reciprocity, i.e. the proportion of artists who are listed as an influence of an artist they follow, 
#is 0.001824561. Thus only a small number of artists are both influencers and followers of another artists.

table(sapply(cliques(artists3.gc), length))
cliques(artists3.gc)[sapply(cliques(artists3.gc), length) == 9]

#There are two cliques of length 9 (complete subgraphs).
#175286 159699 136640 14651  162487 749476 19241  362437 98189
#Dolly Parton, #Emmylou Harris, Tammy Wynette, Patsy Cline, Dixie Chicks, Trisha Yearwood, Patty Loveless, 
#Kathy Mattea, Kitty Wells

#175286 159699 14651  162487 234325 749476 19241  362437 98189
#Dolly Parton, Emmylou Harris, Patsy Cline, Dixie Chicks, Loretta Lynn, Trisha Yearwood, Patty Loveless, 
#Kathy Mattea, Kitty Wells



vertex_connectivity(net3)

plot(artists3.gc, vertex.shape="none", layout=layout_with_fr, vertex.label=V(net1)$artist_name, 
     vertex.label.font=2, vertex.label.color="gray40",
     vertex.label.cex=.7, edge.color="gray85", edge.arrow.size=.2)
#Fruchterman-Reingold layout

set.seed(42)
drlartists3 <- layout_with_drl(artists3.gc)

plot(artists3.gc, vertex.shape="none", layout=drlartists3, vertex.label=V(net1)$artist_name, 
     vertex.label.font=2, vertex.label.color="gray40",
     vertex.label.cex=.7, edge.color="gray85", edge.arrow.size=.2)
#DrL graph

artists.neighborhoods <- make_ego_graph(artists3.gc, order = 1)
artists.neighborhood.list <- sapply(artists.neighborhoods, vcount)
write.csv(artists.neighborhood.list, file = "artistsneighborhoodlist.csv")
neighborhoodhist <- hist(artists.neighborhood.list, breaks=c(2,10,20,30,40,50,100,700))
text(neighborhoodhist$mids,neighborhoodhist$counts,labels=neighborhoodhist$counts, adj=c(0.5, -0.5))
neighborhoodhist

n15 <- artists.neighborhoods[[15]]
plot(n15, vertex.shape="none", vertex.label=V(net1)$artist_name, 
     vertex.label.font=2, vertex.label.color="gray40",
     vertex.label.cex=.7, edge.color="gray85", edge.arrow.size=.2)


characteristics <- full_music_data[,c(3,4,5,6,7,9,10,11,12,13,15,16)]

head(characteristics)

library(Hmisc)

characteristics_correlations<- cor(characteristics, method = "pearson")
data1corr.df <- as.data.frame(characteristics_correlations)
write.csv(data1corr.df, "datacorr1.csv")


cor.tests <- rcorr(as.matrix(characteristics_correlations))
cortests.df <- as.data.frame(cor.tests$P)
write.csv(cortests.df, "cortests.csv")
