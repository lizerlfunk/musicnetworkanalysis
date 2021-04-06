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
artists2 <- data_by_artist[, c(2,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16)]
View(artists2)

#descriptive statistics: number of influencers/followers in each genre
count(influence_data, vars = "influencer_main_genre", wt_var = NULL)
count(influence_data, vars = "follower_main_genre", wt_var = NULL)

#Artist The New Pornographers are not included in the artist data, so we omit 
#them from the influence data as well in order to create a network graph
influence3 <- influence2[ -seq( from=22470, length.out=18, by=1), ]

#create network graph
net1 <- graph_from_data_frame(d=influence3, vertices=artists2, directed=T) 

#plot network graph
plot(net1, vertex.shape="none", vertex.label=V(net1)$artist_name, 
     vertex.label.font=2, vertex.label.color="gray40",
     vertex.label.cex=.7, edge.color="gray85", edge.arrow.size=.2)

#We subset the artists that are listed in the influence data--we are only
#interested in artists that are listed as an influencer of at least one other
#artist or a follower of at least one other artist.
artists3 <- artists2[artists2$artist_id %in% influence3$influencer_id,]
artists4 <- artists2[artists2$artist_id %in% influence3$follower_id,]
artists5 <- rbind(artists3, artists4)
artists5 <- artists5[!duplicated(artists5$artist_id), ]

#Create network graph with the disconnected nodes removed
net1 <- graph_from_data_frame(d=influence3, vertices=artists5, directed=T) 

V(net1)$color <- graphcolors(V(net1)$influencer_main_genre)

plot(net1, vertex.shape="none", vertex.label=V(net1)$artist_name, 
     vertex.label.font=2, vertex.label.color="gray40",
     vertex.label.cex=.7, edge.color="gray85", edge.arrow.size=.2)

graphcolors <- pal_d3(palette = c("category20"), alpha = 1)



characteristics <- full_music_data[,c(3,4,5,6,7,9,10,11,12,13,15,16)]

head(characteristics)

library(Hmisc)

characteristics_correlations<- cor(characteristics, method = "pearson")
data1corr.df <- as.data.frame(characteristics_correlations)
write.csv(data1corr.df, "datacorr1.csv")


cor.tests <- rcorr(as.matrix(characteristics_correlations))
cortests.df <- as.data.frame(cor.tests$P)
write.csv(cortests.df, "cortests.csv")
