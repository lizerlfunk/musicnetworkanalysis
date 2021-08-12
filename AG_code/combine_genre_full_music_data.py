import csv

# As a csv.reader is usuable once and only once we write the lines of our csv file to a list 
with open("data_by_artist_with_genre.csv", "rt") as infile:
    reader = csv.reader(infile)
    next(reader)
    artist_data = list(reader)

# As a csv.reader is usuable once and only once we write the lines of our csv file to a list 
with open("full_music_data.csv", "rt") as infile:
    reader = csv.reader(infile)
    next(reader)
    full_data = list(reader)

header = ["artist_id", "artist_name", "artist_genre", "danceability", "energy", "valence", "tempo", "loudness", "mode", "key", "acousticness", "instrumentalness", "liveness", "speechiness", "explicit", "duration_ms", "popularity", "year" ,"release_date", "song_title"]


with open("full_music_data_with_genre.csv", mode='w') as artist_file:
	artist_writer = csv.writer(artist_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	header = ["artist_id", "artist_name", "artist_genre", "danceability", "energy", "valence", "tempo", "loudness", "mode", "key", "acousticness", "instrumentalness", "liveness", "speechiness", "explicit", "duration_ms", "popularity", "year" ,"release_date", "song_title"]
	artist_writer.writerow(header)
	for row1 in full_data:
		# Remove the brackets from around the artist id and then split multiple id's seperated by commas into a list of two
		# (or more) artists
		artist_id = row1[1].strip("[]").split(",")
		for row2 in artist_id:
			# When two (or more) artists are separated there is leading whitespace present.
			# Here we remove it.
			artist_id = row2.lstrip(" ")
			for row3 in artist_data:
				if artist_id == row3[0]:
					song_list = [row3[0], row3[1], row3[2], row1[2], row1[3], row1[4], row1[5], row1[6], row1[7], row1[8], row1[9], row1[10], row1[11], row1[12], row1[13], row1[14], row1[15], row1[16], row1[17], row1[18]]
					print(song_list)
					artist_writer.writerow(song_list)
