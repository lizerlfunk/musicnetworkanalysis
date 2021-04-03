"""
Name
----
spotify_data_by_year.py
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def make_music_feature_heatmap(correlation_matrix):
	"""
	Parameters
	----------
	correlation_martix : A correlation matrix
	
	Notes
	-----
	Saves the heatmap as the file music_feature_heatmap.pdf
	"""
	# Explore the correlation between music features.
	fig,ax = plt.subplots(figsize = (10,7))
	sns.heatmap(correlation_matrix)
	plt.savefig("music_feature_heatmap.pdf")
	plt.show()

def make_music_feature_lineplots(dataframe):
	"""
	Parameters
	----------
	dataframe : A pandas dataframe
	
	Notes
	-----
	Saves the lineplots as the files music_features_by_year1.pdf and music_features_by_year2.pdf
	I was having issues with matplotlib properly displaying the margins so plt.show() has been 
	commented out for now. 
	"""
	# Explore danceability by year.
	fig,axs = plt.subplots(6, figsize = (10,12))
	sns.lineplot(x="year", y="danceability", data = data_year,ax = axs[0])
	# Explore energy by year.
	sns.lineplot(x="year", y="energy", data = data_year,ax = axs[1])
	# Explore valence by year.
	sns.lineplot(x="year", y="valence", data = data_year,ax = axs[2])
	# Explore tempo by year.
	sns.lineplot(x="year", y="tempo", data = data_year,ax = axs[3])
	# Explore loudness by year.
	sns.lineplot(x="year", y="loudness", data = data_year,ax = axs[4])
	# Explore key by year.
	sns.lineplot(x="year", y="key", data = data_year,ax = axs[5])
	plt.savefig('music_features_by_year_1.pdf', bbox_inches = "tight")	
	fig,axs = plt.subplots(5, figsize = (10,10))
	# Explore acousticness by year.
	sns.lineplot(x="year", y="acousticness", data = data_year,ax = axs[0])
	# Explore instrumentalness by year.
	sns.lineplot(x="year", y="instrumentalness", data = data_year,ax = axs[1])
	# Explore liveness by year.
	sns.lineplot(x="year", y="liveness", data = data_year,ax = axs[2])
	# Explore speechiness by year.
	sns.lineplot(x="year", y="speechiness", data = data_year,ax = axs[3])
	# Explore duration (in milliseconds) by year.
	sns.lineplot(x="year", y="duration_ms", data = data_year,ax = axs[4])
	plt.savefig('music_features_by_year_2.pdf', bbox_inches = "tight")	
	#plt.show()

# Import the dataset data_by_year.csv
data_year = pd.read_csv("data_by_year.csv")
# Construct our correlation matrix
uniform_data = data_year[["danceability","energy","valence","tempo","loudness","key","acousticness","instrumentalness","liveness","speechiness", "duration_ms","popularity"]].corr()

make_music_feature_heatmap(uniform_data)
make_music_feature_lineplots(data_year)

