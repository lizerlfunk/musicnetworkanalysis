##Working with artist centrality!
##The file artist_centrality_clean.csv must be loaded

library(dplyr)
centrality1 <- artist_centrality_clean %>%
  arrange(desc(in_degree_centrality)) %>%
  slice(1:10) 
write.csv(centrality1,"centrality1.csv", row.names = FALSE)

centrality2 <- artist_centrality_clean %>%
  arrange(desc(out_degree_centrality)) %>%
  slice(1:10) 
write.csv(centrality2,"centrality2.csv", row.names = FALSE)
##why are in-degree and out-degree the same? 

centrality3 <- artist_centrality_clean %>%
  arrange(desc(betweenness_centrality)) %>%
  slice(1:10) 
write.csv(centrality3,"centrality3.csv", row.names = FALSE)

centrality4 <- artist_centrality_clean %>%
  arrange(desc(katz_centrality)) %>%
  slice(1:10) 
write.csv(centrality4,"centrality4.csv", row.names = FALSE)

centrality5 <- artist_centrality_clean %>%
  arrange(desc(pagerank)) %>%
  slice(1:10) 
write.csv(centrality5,"centrality5.csv", row.names = FALSE)

centrality6 <- artist_centrality_clean %>%
  arrange(desc(eigenvector_centrality)) %>%
  slice(1:10) 
write.csv(centrality6,"centrality6.csv", row.names = FALSE)

centrality7 <- artist_centrality_clean %>%
  arrange(desc(closeness_centrality)) %>%
  slice(1:10) 
write.csv(centrality7,"centrality7.csv", row.names = FALSE)

##We will compare these top 10 lists and investigate characteristics of each of
##the neighbors of the top 10 for each type of centrality. Which should we use?

centralitycombined <- rbind(centrality1, centrality3, centrality4, centrality5, centrality6, centrality7)
centralitycombined <- centralitycombined[!duplicated(centralitycombined$artist_id), ]
write.csv(centralitycombined,"centralitycombined.csv", row.names = FALSE)
