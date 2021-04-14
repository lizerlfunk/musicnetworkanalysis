"""
Name
____
build_influence_network.py

Notes
-----
The following .csv files must be in the same directory as influence_network.py :
	(1) influence_data.csv
	(2) data_by_artist.csv
"""

from collections import defaultdict
import collections
import csv
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import powerlaw
import scipy as sci 

def build_graph(inf_data, artist_data):
	"""
	Returns the directed graph of artistic influeence taken from influence_data.csv
	   
	Parameters
	----------
	inf_data : the file influence_data.csv
	arist_data : the file data_by_artist.csv
	
	Returns
	-------
	graph : a NetworkX directed graph

	Notes
	-----
    	"""
	graph = nx.DiGraph()
	for row in inf_data:
		if graph.has_node(row[0]) is False:	
			graph.add_node(row[0], name = row[1], genre = row[2], active_start = row[3] )
		if graph.has_node(row[4]) is False:
			graph.add_node(row[4], name = row[5], genre = row[6], active_start = row[7])
		graph.add_edge(row[4],row[0])
	# Add more attributes to our nodes
	for row in artist_data:
		for node in graph:
			if row[1] == node:
				graph.nodes[node]["danceability"] = row[2]
				graph.nodes[node]["energy"] = row[3]
				graph.nodes[node]["valence"] = row[4]
				graph.nodes[node]["tempo"] = row[5]
				graph.nodes[node]["loudness"] = row[6]
				graph.nodes[node]["key"] = row[8]
				graph.nodes[node]["acousticness"] = row[9]
				graph.nodes[node]["instrumentalness"] = row[10]
				graph.nodes[node]["liveness"] = row[11]
				graph.nodes[node]["speechiness"] = row[12]
				graph.nodes[node]["duration_ms"] = row[13]
				graph.nodes[node]["popularity"] = row[14]
				graph.nodes[node]["count"] = row[15]
	# Is our graph an acyclic directed graph
	print("Our graph is an acyclic directed graph: " + str(nx.is_directed_acyclic_graph(graph)))

	# Check nodes
	num_nodes = graph.number_of_nodes()
	num_edges = graph.number_of_edges()
	# Is this really the number of edges, I know that our graph is not acyclic but if it were there should be
	# n*(n-1)/2 edges, no?
	num_possible_edges = num_nodes*(num_nodes - 1)
	print("Our artistic influence network has " + str(num_nodes)+" artists.")
	print("Our artistic influence network has " + str(num_edges)+" edges out of a possible " + str(num_possible_edges) + " possible edges.")
	print("Our network density is: " + str(nx.density(graph)))

	return graph

def build_genre_graph(genre, inf_data, artist_data):
	"""
	Returns the directed graph of the artistic influeence of a particular genre taken from influence_data.csv 
	   
	Parameters
	----------
	genre : the desired genre
	inf_data : the file influence_data.csv
	arist_data : the file data_by_artist.csv
	
	Returns
	-------
	graph : a NetworkX directed graph

	Notes
	-----
    	The available genres should be listed for ease of use. This will be wored on
	"""
	graph = nx.DiGraph()
	for row in inf_data:
		# Should I use == or is to test for genre?
		if graph.has_node(row[0]) is False and row[2] == genre:	
			graph.add_node(row[0], name = row[1], genre = row[2], active_start = row[3] )
		if graph.has_node(row[4]) is False and row[6] == genre:
			graph.add_node(row[4], name = row[5], genre = row[6], active_start = row[7])
		if row[2] == genre and row[6] == genre:
			graph.add_edge(row[4],row[0])
	# Add more attributes to our nodes
	for row in artist_data:
		for node in graph:
			if row[1] == node:
				graph.nodes[node]["danceability"] = row[2]
				graph.nodes[node]["energy"] = row[3]
				graph.nodes[node]["valence"] = row[4]
				graph.nodes[node]["tempo"] = row[5]
				graph.nodes[node]["loudness"] = row[6]
				graph.nodes[node]["key"] = row[8]
				graph.nodes[node]["acousticness"] = row[9]
				graph.nodes[node]["instrumentalness"] = row[10]
				graph.nodes[node]["liveness"] = row[11]
				graph.nodes[node]["speechiness"] = row[12]
				graph.nodes[node]["duration_ms"] = row[13]
				graph.nodes[node]["popularity"] = row[14]
				graph.nodes[node]["count"] = row[15]
	# Is our graph an acyclic directed graph
	print("Our graph is an acyclic directed graph: " + str(nx.is_directed_acyclic_graph(graph)))

	# Check nodes
	num_nodes = graph.number_of_nodes()
	num_edges = graph.number_of_edges()
	num_possible_edges = num_nodes*(num_nodes - 1)
	print("Our artistic influence network has " + str(num_nodes)+" artists.")
	print("Our artistic influence network has " + str(num_edges)+" edges out of a possible " + str(num_possible_edges) + " possible edges.")
	print("Our network density is: " + str(nx.density(graph)))

	return graph

def build_decade_graph(decade, inf_data, artist_data):
	"""
	Returns the directed graph of the artistic influeence during a specified decade taken from influence_data.csv 
	   
	Parameters
	----------
	decade : the desired decade 
	inf_data : the file influence_data.csv
	arist_data : the file data_by_artist.csv
	
	Returns
	-------
	graph : a NetworkX directed graph

	Notes
	-----
	"""
	graph = nx.DiGraph()
	for row in inf_data:
		if int(row[7]) == decade:
			if graph.has_node(row[0]) is False:	
				graph.add_node(row[0], name = row[1], genre = row[2], active_start = row[3] )
			if graph.has_node(row[4]) is False:
				graph.add_node(row[4], name = row[5], genre = row[6], active_start = row[7])
			graph.add_edge(row[4],row[0])
		# Add more attributes to our nodes
		for row in artist_data:
			for node in graph:
				if row[1] == node:
					graph.nodes[node]["danceability"] = row[2]
					graph.nodes[node]["energy"] = row[3]
					graph.nodes[node]["valence"] = row[4]
					graph.nodes[node]["tempo"] = row[5]
					graph.nodes[node]["loudness"] = row[6]
					graph.nodes[node]["key"] = row[8]
					graph.nodes[node]["acousticness"] = row[9]
					graph.nodes[node]["instrumentalness"] = row[10]
					graph.nodes[node]["liveness"] = row[11]
					graph.nodes[node]["speechiness"] = row[12]
					graph.nodes[node]["duration_ms"] = row[13]
					graph.nodes[node]["popularity"] = row[14]
					graph.nodes[node]["count"] = row[15]
	# Is our graph an acyclic directed graph
	print("Our graph is an acyclic directed graph: " + str(nx.is_directed_acyclic_graph(graph)))

	# Check nodes
	num_nodes = graph.number_of_nodes()
	num_edges = graph.number_of_edges()
	num_possible_edges = num_nodes*(num_nodes - 1)
	print("Our artistic influence network has " + str(num_nodes)+" artists.")
	print("Our artistic influence network has " + str(num_edges)+" edges out of a possible " + str(num_possible_edges) + " possible edges.")
	print("Our network density is: " + str(nx.density(graph)))

	return graph

def build_out_of_genre_graph(inf_data, artist_data):
	"""
	Returns a directed graph of artists whose influencers lie outside of their genre so we'll be able to more easily
	see if, for example, an R&B group is influenced by a Jazz musician.  
	Parameters
	----------
	decade : the desired decade 
	inf_data : the file influence_data.csv
	arist_data : the file data_by_artist.csv
	
	Returns
	-------
	graph : a NetworkX directed graph

	Notes
	-----
	This is more a lark but useful things sometimes come out of larks. Though, on examination of the raw data this may
	not be too terribly useful as Pop/Rock is such a large umbrella.
	"""
	graph = nx.DiGraph()
	for row in inf_data:
		if row[2] != row[6]:
			# Should I use == or is to test for genre?
			if graph.has_node(row[0]) is False:	
				graph.add_node(row[0], name = row[1], genre = row[2], active_start = row[3] )
			if graph.has_node(row[4]) is False:
				graph.add_node(row[4], name = row[5], genre = row[6], active_start = row[7])
			graph.add_edge(row[4],row[0])
		# Add more attributes to our nodes
		for row in artist_data:
			for node in graph:
				if row[1] == node:
					graph.nodes[node]["danceability"] = row[2]
					graph.nodes[node]["energy"] = row[3]
					graph.nodes[node]["valence"] = row[4]
					graph.nodes[node]["tempo"] = row[5]
					graph.nodes[node]["loudness"] = row[6]
					graph.nodes[node]["key"] = row[8]
					graph.nodes[node]["acousticness"] = row[9]
					graph.nodes[node]["instrumentalness"] = row[10]
					graph.nodes[node]["liveness"] = row[11]
					graph.nodes[node]["speechiness"] = row[12]
					graph.nodes[node]["duration_ms"] = row[13]
					graph.nodes[node]["popularity"] = row[14]
					graph.nodes[node]["count"] = row[15]
	# Is our graph an acyclic directed graph
	print("Our graph is an acyclic directed graph: " + str(nx.is_directed_acyclic_graph(graph)))

	# Check nodes
	num_nodes = graph.number_of_nodes()
	num_edges = graph.number_of_edges()
	num_possible_edges = num_nodes*(num_nodes - 1)
	print("Our artistic influence network has " + str(num_nodes)+" artists.")
	print("Our artistic influence network has " + str(num_edges)+" edges out of a possible " + str(num_possible_edges) + " possible edges.")
	print("Our network density is: " + str(nx.density(graph)))

	return graph

def calculate_centrality(graph):
	"""
	Writes the in degree centrality, out degree centrality, betweenness centrality, Katz centrality, PageRank,
	eigenvector centrality, closeness centrality, and global reaching centrality of a NetworkX graph's nodes
	to the file artist_centrality.csv

	Parameters
	----------
	graph : a NetworkX graph 
	
	Notes
	-----
	"""
	# Compute the degree centrality of our graph
	in_deg_cent_dict = nx.in_degree_centrality(graph)
	# Compute the degree centrality of our graph
	out_deg_cent_dict = nx.in_degree_centrality(graph)
	# Compute the betweenness centrality of our graph
	bet_cent_dict = nx.betweenness_centrality(graph)
	# Compute the Katz centrality of our graph
	katz_cent_dict = nx.katz_centrality(graph)
	# Compute the PageRank of nodes on our graph
	pagerank_dict = nx.pagerank(graph)
	# Compute the eigenvector centrality of our graph
	eigenvector_dict = nx.eigenvector_centrality(graph)
	# Computer the closeness centrality of our graph
	closeness_dict = nx.closeness_centrality(graph)
	# Compute the global reaching centrality of our graph
	global_reach_cent = nx.global_reaching_centrality(graph)
	print("The global reaching centrality is " + str(global_reach_cent))
	# Write centrality measures to file
	with open("artist_centrality.csv", "w") as csvfile:
		filewriter = csv.writer(csvfile, delimiter = ",", quotechar = "|", quoting = csv.QUOTE_MINIMAL)
		filewriter.writerow(["artist_id","artist_name", "in_degree_centrality", "out_degree_centrality", "betweenness_centrality", "katz_centrality", "pagerank", "eigenvector_centrality","closeness_centrality"])
		for node in graph.nodes:
			artist_name = nx.get_node_attributes(inf_graph, "name")
			row = [node, artist_name[node], int_deg_cent_dict[node], out_deg_cent_dict[node], bet_cent_dict[node], katz_cent_dict[node], pagerank_dict[node], eigenvector_dict[node], closeness_dict[node]]
			filewriter.writerow(row)

def plot_power_law(graph):
	data = [graph.in_degree(n) for n in graph.nodes()]
	results = powerlaw.Fit(data)
	print(results.power_law.alpha)
	print(results.power_law.xmin)
	print(np.isfinite(data).all())
	#figPDF = powerlaw.plot_pdf(np.array(data), color='b')
	#powerlaw.plot_pdf(np.array(data), linear_bins=True, color='r', ax=figPDF)
	#np.seterr(divide='ignore', invalid='ignore')
	fit=powerlaw.Fit(np.array(data), discrete=True)
	#print(fit.power_law.alpha)
	print(fit.distribution_compare('power_law', 'truncated_power_law'))
	fit.power_law.plot_pdf( color= 'b',linestyle='--',label='fit ccdf')
	# Linear bins?
	fit.plot_pdf(color= 'r', linear_bins=True)
	# Logarithmic bins?
	fit.plot_pdf(color = 'g')
	plt.show()

def plot_degree_dist(graph):
	"""
	Plots a histograph of the in degree distribution of the nodes of a directed graph.
	
	Parameters
	----------
	graph : a NetworkX directed graph 
	
	Notes
	-----
	"""
	degrees = [graph.in_degree(n) for n in graph.nodes()]
	plt.hist(degrees,100)
	plt.title("Degree Histogram")
	plt.ylabel("Count")
	plt.xlabel("Degree")
	plt.xticks(rotation = 90)
	plt.show()

# Taken from:
# https://stackoverflow.com/questions/53958700/plotting-the-degree-distribution-of-a-graph-using-nx-degree-histogram
def degree_histogram_directed(G, in_degree=False, out_degree=False):
    """
    Return a list of the frequency of each degree value.

    Parameters
    ----------
    G : Networkx graph
       A graph
    in_degree : bool
    out_degree : bool

    Returns
    -------
    hist : list
       A list of frequencies of degrees.
       The degree values are the index in the list.

    Notes
    -----
    Note: the bins are width one, hence len(list) can be large
    (Order(number_of_edges))
    """
    nodes = G.nodes()
    if in_degree:
        in_degree = dict(G.in_degree())
        degseq=[in_degree.get(k,0) for k in nodes]
    elif out_degree:
        out_degree = dict(G.out_degree())
        degseq=[out_degree.get(k,0) for k in nodes]
    else:
        degseq=[v for k, v in G.degree()]
    dmax=max(degseq)+1
    freq= [ 0 for d in range(dmax) ]
    for d in degseq:
        freq[d] += 1
    return freq

def create_artist_attributes_file(graph):
	"""
	One of the rather annoying things about
	(1) data_by_artist.csv
	(2) data_by_year.csv
	(3) full_music_data.csv
	is that they lack information about artistic genre. 
	
	Parameters
	----------
	graph : A NetworkX graph

	Notes
	-----
	The artist The New Pornographers was found to be in the file influence_data.csv 
	but not in the file data_by_artist.csv
	"""
	with open("data_by_artists_with_genre.csv", "w", newline="") as csvfile:

		filewriter = csv.writer(csvfile, delimiter = ",")#, quotechar = "|", quoting = csv.QUOTE_MINIMAL)
		filewriter.writerow(["artist_id", "artist_name", "artist_genre", "active_start", "danceability", "energy", "valence", "tempo", "loudness", "key", "acousticness", "instrumentalness", "liveness", "speechiness", "duration_ms", "popularity", "count"])
		for node in graph.nodes:
			artist_name = nx.get_node_attributes(graph, "name")	
			genre = nx.get_node_attributes(graph, "genre")
			active_start = nx.get_node_attributes(graph, "active_start")
			danceability = nx.get_node_attributes(graph, "danceability")
			energy = nx.get_node_attributes(graph, "energy")
			valence = nx.get_node_attributes(graph, "valence")
			tempo = nx.get_node_attributes(graph, "tempo")
			loudness = nx.get_node_attributes(graph, "loudness")
			key = nx.get_node_attributes(graph, "key")
			acousticness = nx.get_node_attributes(graph, "acousticness")
			instrumentalness = nx.get_node_attributes(graph, "instrumentalness")
			liveness = nx.get_node_attributes(graph, "liveness")
			speechiness = nx.get_node_attributes(graph, "speechiness")
			duration_ms = nx.get_node_attributes(graph, "duration_ms")
			popularity = nx.get_node_attributes(graph, "popularity")
			count = nx.get_node_attributes(graph, "count")
			# The artist The New Pornographers is in influence_data.csv but not data_by_artist.csv
			if artist_name[node] != "The New Pornographers":
				row = [node, artist_name[node], genre[node], active_start[node], danceability[node], energy[node], valence[node], tempo[node], loudness[node], key[node], acousticness[node], instrumentalness[node], liveness[node], speechiness[node], duration_ms[node], popularity[node], count[node]]
				filewriter.writerow(row)

# Open influence_data.csv and data_by_artists.csv
influence_csv_reader = csv.reader(open("influence_data.csv"), delimiter=",")
artist_csv_reader = csv.reader(open("data_by_artist.csv"),delimiter=",")
# Disgard the first row of influence_data.csv and data_by_artsit.csv as the column labels are unneeded.
next(influence_csv_reader)
next(artist_csv_reader)

# Construct our graph
inf_graph = build_graph(influence_csv_reader, artist_csv_reader)
create_artist_attributes_file(inf_graph)
#plot_degree_dist(inf_graph)
plot_power_law(inf_graph)

#pos = nx.spring_layout(inf_graph)
#nx.draw(inf_graph, pos, node_size = 10) 
#nx.draw_networkx_labels(inf_graph, pos)
#plt.savefig("graph.pdf")
#plt.show()

