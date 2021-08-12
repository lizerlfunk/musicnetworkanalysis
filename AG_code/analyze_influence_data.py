from collections import Counter
import csv
import matplotlib.pyplot as plt
import numpy as np
import statistics 

# Read in the file influence_data.csv
with open("influence_data.csv", "rt") as infile:
	reader = csv.reader(infile)
	# Disgard the first row of influence_data.csv as the 
	# column names are unneeded. 
	next(reader)
	influence_data = list(reader)

# Read in the file artist_data_with_genre.csv
with open("data_by_artist_with_genre.csv", "rt") as infile:
	reader = csv.reader(infile)
	# Disgard the first row of artist_data_with_genre.csv as the 
	# column names are unneeded. 
	next(reader)
	artist_data = list(reader)

# Read in the file data_by_year.csv
with open("data_by_year.csv", "rt") as infile:
	reader = csv.reader(infile)
	# Disregard the first row of the data_by_year.csv file as the
	# column names are uneeded
	next(reader)
	data_by_year = list(reader)

# Read in the distruption centrality file distruption disruption_centrality.csv
with open("disruption_centrality.csv", "rt") as infile:
	reader = csv.reader(infile)
	# Disgard the first row of disruption_centrality.csv as the 
	# column names are unneeded. 
	next(reader)
	disruption_data = list(reader)

# Read in the distruption centrality file distruption disruption_centrality.csv
with open("artist_centrality.csv", "rt") as infile:
	reader = csv.reader(infile)
	# Disgard the first row of artist_centrality.csv as the 
	# column names are unneeded. 
	next(reader)
	artist_centrality_data = list(reader)

def append_disruption_to_artist_centrality(artist_centrality, distruption_centrality):
	with open("new_artist_centrality.csv", "w") as csvfile:
		filewriter = csv.writer(csvfile, delimiter = ",", quotechar = "|", quoting = csv.QUOTE_MINIMAL)
		filewriter.writerow(["artist_id","artist_name", "in_degree_centrality", "out_degree_centrality", "betweenness_centrality", "katz_centrality", "pagerank"
    , "eigenvector_centrality","closeness_centrality", "ni", "nj", "nk", "disruption", "in", "out"]) 
		for row1 in artist_centrality:
			for row2 in distruption_centrality:
				if row1[0] == row2[0]:
					cent_row = [row1[0], row1[1], row1[2], row1[3], row1[4], row1[5], row1[6], row1[7], row1[8], row2[1], row2[2], row2[3], row2[4], row2[5], row2[6]]
					filewriter.writerow(cent_row)

def top_10_deg_cent_std_dv(artist_data, data_by_year):
	# The node ids of the top ten artists scored by degree centrality.
	# Note that 9 out of ten are from the 1960s, Hank Willaims being the notable exception with a start decade of 1930.  
	artist_list = [754032, 66915, 894465, 531986, 139026, 354105, 100160, 41874, 549797, 840402] 
	with open("top_10_artist_by_degree_standard_deviation_of_music_attributes.csv", "w") as csvfile:
		filewriter = csv.writer(csvfile, delimiter = ",", quotechar = "|", quoting = csv.QUOTE_MINIMAL)
		# Note that popularity is left out as I don't quite know what to make of that characteristic.
		filewriter.writerow(["artist_id", "artist_name", "danceability_std_dev", "energy_std_dev", "valence_std_dev", "tempo_std_dev", "loudness_std_dev", "key_std_dev", "acousticness_std_dev", "instrumentalness_std_dev", "liveness_std_dev", "speechiness_std_dev", "duration_std_dev"])
		for row_artist in artist_data:
			if int(row_artist[0]) in artist_list:
				for row_year in data_by_year:
					if int(row_artist[3]) == int(row_year[0]):
						danceability_std_dev = statistics.stdev([float(row_artist[4]), float(row_year[1])]) 
						energy_std_dev = statistics.stdev([float(row_artist[5]), float(row_year[2])]) 
						valence_std_dev = statistics.stdev([float(row_artist[6]), float(row_year[3])]) 
						tempo_std_dev = statistics.stdev([float(row_artist[7]), float(row_year[4])]) 
						loudness_std_dev = statistics.stdev([float(row_artist[8]), float(row_year[5])]) 
						key_std_dev = statistics.stdev([float(row_artist[9]), float(row_year[7])]) 
						acousticness_std_dev = statistics.stdev([float(row_artist[10]), float(row_year[8])]) 
						instrumentalness_std_dev = statistics.stdev([float(row_artist[11]), float(row_year[9])]) 
						liveness_std_dev = statistics.stdev([float(row_artist[12]), float(row_year[10])]) 
						speechiness_std_dev = statistics.stdev([float(row_artist[13]), float(row_year[11])]) 
						duration_std_dev = statistics.stdev([float(row_artist[14]), float(row_year[12])])
						filewriter.writerow([row_artist[0], row_artist[1], danceability_std_dev, energy_std_dev, valence_std_dev, tempo_std_dev, loudness_std_dev, key_std_dev, acousticness_std_dev, instrumentalness_std_dev, liveness_std_dev, speechiness_std_dev, duration_std_dev])

def top_10_pagerank_std_dv(artist_data, data_by_year):
	# The node ids of the top ten artists scored by PageRank.
	# Note that 9 out of 10 artists are from the 1930s with The Beatles being a noteable exception. Also note that Hank Williams, the lone artist from the 1930s
	# in our top ten by degree centrality is absent here!
	artist_list = [532957, 79016, 259529, 287604, 3829, 13511, 754032, 403120, 848784, 805930]
	with open("top_10_artist_by_pagerank_standard_deviation_of_music_attributes.csv", "w") as csvfile:
		filewriter = csv.writer(csvfile, delimiter = ",", quotechar = "|", quoting = csv.QUOTE_MINIMAL)
		# Note that popularity is left out as I don't quite know what to make of that characteristic.
		filewriter.writerow(["artist_id", "artist_name", "danceability_std_dev", "energy_std_dev", "valence_std_dev", "tempo_std_dev", "loudness_std_dev", "key_std_dev", "acousticness_std_dev", "instrumentalness_std_dev", "liveness_std_dev", "speechiness_std_dev", "duration_std_dev"])
		for row_artist in artist_data:
			if int(row_artist[0]) in artist_list:
				for row_year in data_by_year:
					if int(row_artist[3]) == int(row_year[0]):
						print(row_year[0])
						danceability_std_dev = statistics.stdev([float(row_artist[4]), float(row_year[1])]) 
						energy_std_dev = statistics.stdev([float(row_artist[5]), float(row_year[2])]) 
						valence_std_dev = statistics.stdev([float(row_artist[6]), float(row_year[3])]) 
						tempo_std_dev = statistics.stdev([float(row_artist[7]), float(row_year[4])]) 
						loudness_std_dev = statistics.stdev([float(row_artist[8]), float(row_year[5])]) 
						key_std_dev = statistics.stdev([float(row_artist[9]), float(row_year[7])]) 
						acousticness_std_dev = statistics.stdev([float(row_artist[10]), float(row_year[8])]) 
						instrumentalness_std_dev = statistics.stdev([float(row_artist[11]), float(row_year[9])]) 
						liveness_std_dev = statistics.stdev([float(row_artist[12]), float(row_year[10])]) 
						speechiness_std_dev = statistics.stdev([float(row_artist[13]), float(row_year[11])]) 
						duration_std_dev = statistics.stdev([float(row_artist[14]), float(row_year[12])]) 
						filewriter.writerow([row_artist[0], row_artist[1], danceability_std_dev, energy_std_dev, valence_std_dev, tempo_std_dev, loudness_std_dev, key_std_dev, acousticness_std_dev, instrumentalness_std_dev, liveness_std_dev, speechiness_std_dev, duration_std_dev])

def top_10_katz_std_dv(artist_data, data_by_year):
	# The node ids of the top ten artists scored by Katz centrality.
	# No artist after 1960 is present in the top ten list of artists sorted by highest Katz Centrality 
	artist_list = [120521, 754032, 608701, 287604, 66915, 549797, 824022, 180228, 343396, 276085]
	with open("top_10_artist_by_katz_standard_deviation_of_music_attributes.csv", "w") as csvfile:
		filewriter = csv.writer(csvfile, delimiter = ",", quotechar = "|", quoting = csv.QUOTE_MINIMAL)
		# Note that popularity is left out as I don't quite know what to make of that characteristic.
		filewriter.writerow(["artist_id", "artist_name", "danceability_std_dev", "energy_std_dev", "valence_std_dev", "tempo_std_dev", "loudness_std_dev", "key_std_dev", "acousticness_std_dev", "instrumentalness_std_dev", "liveness_std_dev", "speechiness_std_dev", "duration_std_dev"])
		for row_artist in artist_data:
			if int(row_artist[0]) in artist_list:
				for row_year in data_by_year:
					if int(row_artist[3]) == int(row_year[0]):
						print(row_year[0])
						danceability_std_dev = statistics.stdev([float(row_artist[4]), float(row_year[1])]) 
						energy_std_dev = statistics.stdev([float(row_artist[5]), float(row_year[2])]) 
						valence_std_dev = statistics.stdev([float(row_artist[6]), float(row_year[3])]) 
						tempo_std_dev = statistics.stdev([float(row_artist[7]), float(row_year[4])]) 
						loudness_std_dev = statistics.stdev([float(row_artist[8]), float(row_year[5])]) 
						key_std_dev = statistics.stdev([float(row_artist[9]), float(row_year[7])]) 
						acousticness_std_dev = statistics.stdev([float(row_artist[10]), float(row_year[8])]) 
						instrumentalness_std_dev = statistics.stdev([float(row_artist[11]), float(row_year[9])]) 
						liveness_std_dev = statistics.stdev([float(row_artist[12]), float(row_year[10])]) 
						speechiness_std_dev = statistics.stdev([float(row_artist[13]), float(row_year[11])]) 
						duration_std_dev = statistics.stdev([float(row_artist[14]), float(row_year[12])]) 
						filewriter.writerow([row_artist[0], row_artist[1], danceability_std_dev, energy_std_dev, valence_std_dev, tempo_std_dev, loudness_std_dev, key_std_dev, acousticness_std_dev, instrumentalness_std_dev, liveness_std_dev, speechiness_std_dev, duration_std_dev])

def top_10_betweenness_std_dv(artist_data, data_by_year):
	# The node ids of the top ten artists scored by betweenness centrality.
	artist_list = [583959, 222927, 846092, 278575, 102050, 423829, 33161, 754032, 840102, 418740]
	with open("top_10_artist_by_betweenness_standard_deviation_of_music_attributes.csv", "w") as csvfile:
		filewriter = csv.writer(csvfile, delimiter = ",", quotechar = "|", quoting = csv.QUOTE_MINIMAL)
		# Note that popularity is left out as I don't quite know what to make of that characteristic.
		filewriter.writerow(["artist_id", "artist_name", "danceability_std_dev", "energy_std_dev", "valence_std_dev", "tempo_std_dev", "loudness_std_dev", "key_std_dev", "acousticness_std_dev", "instrumentalness_std_dev", "liveness_std_dev", "speechiness_std_dev", "duration_std_dev"])
		for row_artist in artist_data:
			if int(row_artist[0]) in artist_list:
				for row_year in data_by_year:
					if int(row_artist[3]) == int(row_year[0]):
						print(row_year[0])
						danceability_std_dev = statistics.stdev([float(row_artist[4]), float(row_year[1])]) 
						energy_std_dev = statistics.stdev([float(row_artist[5]), float(row_year[2])]) 
						valence_std_dev = statistics.stdev([float(row_artist[6]), float(row_year[3])]) 
						tempo_std_dev = statistics.stdev([float(row_artist[7]), float(row_year[4])]) 
						loudness_std_dev = statistics.stdev([float(row_artist[8]), float(row_year[5])]) 
						key_std_dev = statistics.stdev([float(row_artist[9]), float(row_year[7])]) 
						acousticness_std_dev = statistics.stdev([float(row_artist[10]), float(row_year[8])]) 
						instrumentalness_std_dev = statistics.stdev([float(row_artist[11]), float(row_year[9])]) 
						liveness_std_dev = statistics.stdev([float(row_artist[12]), float(row_year[10])]) 
						speechiness_std_dev = statistics.stdev([float(row_artist[13]), float(row_year[11])]) 
						duration_std_dev = statistics.stdev([float(row_artist[14]), float(row_year[12])]) 
						filewriter.writerow([row_artist[0], row_artist[1], danceability_std_dev, energy_std_dev, valence_std_dev, tempo_std_dev, loudness_std_dev, key_std_dev, acousticness_std_dev, instrumentalness_std_dev, liveness_std_dev, speechiness_std_dev, duration_std_dev])

def top_10_closeness_std_dv(artist_data, data_by_year):
	# The node ids of the top ten artists scored by closeness centrality.
	# No artist after 1960 is present in the top ten artists sorted by highest closeness centrality
	artist_list = [66915, 754032, 120521, 128099, 824022, 180228, 79016, 608701, 46861, 287604]
	with open("top_10_artist_by_closeness_standard_deviation_of_music_attributes.csv", "w") as csvfile:
		filewriter = csv.writer(csvfile, delimiter = ",", quotechar = "|", quoting = csv.QUOTE_MINIMAL)
		# Note that popularity is left out as I don't quite know what to make of that characteristic.
		filewriter.writerow(["artist_id", "artist_name", "danceability_std_dev", "energy_std_dev", "valence_std_dev", "tempo_std_dev", "loudness_std_dev", "key_std_dev", "acousticness_std_dev", "instrumentalness_std_dev", "liveness_std_dev", "speechiness_std_dev", "duration_std_dev"])
		for row_artist in artist_data:
			if int(row_artist[0]) in artist_list:
				for row_year in data_by_year:
					if int(row_artist[3]) == int(row_year[0]):
						print(row_year[0])
						danceability_std_dev = statistics.stdev([float(row_artist[4]), float(row_year[1])]) 
						energy_std_dev = statistics.stdev([float(row_artist[5]), float(row_year[2])]) 
						valence_std_dev = statistics.stdev([float(row_artist[6]), float(row_year[3])]) 
						tempo_std_dev = statistics.stdev([float(row_artist[7]), float(row_year[4])]) 
						loudness_std_dev = statistics.stdev([float(row_artist[8]), float(row_year[5])]) 
						key_std_dev = statistics.stdev([float(row_artist[9]), float(row_year[7])]) 
						acousticness_std_dev = statistics.stdev([float(row_artist[10]), float(row_year[8])]) 
						instrumentalness_std_dev = statistics.stdev([float(row_artist[11]), float(row_year[9])]) 
						liveness_std_dev = statistics.stdev([float(row_artist[12]), float(row_year[10])]) 
						speechiness_std_dev = statistics.stdev([float(row_artist[13]), float(row_year[11])]) 
						duration_std_dev = statistics.stdev([float(row_artist[14]), float(row_year[12])]) 
						filewriter.writerow([row_artist[0], row_artist[1], danceability_std_dev, energy_std_dev, valence_std_dev, tempo_std_dev, loudness_std_dev, key_std_dev, acousticness_std_dev, instrumentalness_std_dev, liveness_std_dev, speechiness_std_dev, duration_std_dev])

def get_influence_time_difference(inf_data):
	inf_difference_list = []
	long_career_inf_list = []
	for row in inf_data:
		# Subtract the influenced's active start date from
		# the influencer's active start date
		inf_difference = int(row[7]) - int(row[3])
		if inf_difference < 0:
			long_career_inf_list.append(inf_difference)
		inf_difference_list.append(inf_difference)
	print("The median difference between active start dates is " + str(statistics.median(inf_difference_list)))
	print("the mode of the difference between active start dates is " + str(statistics.mode(inf_difference_list)))
	plt.hist(inf_difference_list)
	plt.ylabel("Number of Edges")
	# RELABEL THIS!
	plt.xlabel("Start Date Difference")
	plt.savefig("hist.png")	
	
	return inf_difference_list

def out_of_genre_influence(inf_data):
	out_of_genre_counter = 0
	total_row_counter = 0
	for row in inf_data:
		if row[2] != row[6]:
			out_of_genre_counter += 1	
		total_row_counter += 1
	percent_diff_genre = (out_of_genre_counter/total_row_counter) * 100
	print("We have a total of " + str(total_row_counter) + " edges.")
	print("Of these edges " + str(out_of_genre_counter) + " between artists of different genres.")
	print("Thus " + str(percent_diff_genre) + " percent of our edges occur between artists of different genres.")

def get_artist_data(artist_data):
	artist_number = 0
	genre_list = []
	for row in artist_data:
		artist_number += 1
		genre_list.append(row[2])
	print("There are " + str(artist_number) + " artists in our data set.")
	genre_dict = Counter(genre_list)
	for genre in genre_dict:
		print("There are " + str(genre_dict[genre]) + " artists in the following genre: " + str(genre))	
		print("The genre " + str(genre) + " makes up " + str((genre_dict[genre]/artist_number)*100) + " percent of the artists in our data set.")	

def get_genre(inf_data): 
	genres = [] 
	for row in inf_data:
		if row[2] not in genres:
			genres.append(row[2])
		if row[6] not in genres:
			genres.append(row[6])
	print("We have " + str(len(genres)) + " genres.")
	print("They are  " + str(genres))

