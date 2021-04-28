import csv

# As a csv.reader is an expendible resource we write the lines of our csv file to a list
with open("artist_infomap_1000_iter_community.csv", "rt") as infile:
        reader = csv.reader(infile)
        # We discard the column labels as they are unneccesary 
        next(reader)
        community_data = list(reader)

# As a csv.reader is an expendible resource we write the lines of our csv file to a list
with open("artist_centrality_combined.csv", "rt") as infile:
        reader = csv.reader(infile)
        # We discard the column labels as they are unneccesary 
        next(reader)
        centrality_data = list(reader)

for row1 in community_data:
	for row2 in centrality_data:
		if row1[0] == row2[0]:
			print("Artist " + str(row1[1]) + " is in community " + str(row1[4])+".")
			print("-----------------------------------------------------------------")
