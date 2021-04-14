"""

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
import pandas as pd
import powerlaw
import plfit_py
import scipy as sci 
import statistics 

def get_genre(inf_data):
	"""
	Puts the genres present in the file influence_data.csv into a list 
	
	Parameters
	----------
	inf_data : the file influence_data.csv

	Returns
	-------
	genre_list : a list of the genres in the file influence_data.csv

	Notes
	-----
	"""
	genre_list = []
	for row in inf_data:
		if row[2] not in genre_list:
			genre_list.append(row[2])
	
	return genre_list
	
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

def build_decade_graph(graph, decade):
	# Must make copy to avoid changing intial graph!
	new_graph = graph.copy()
	# We need to loop through our graph's nodes but within the loop we 
	# are removing edges! Note that self.network.nodes is a dictionary and would be chaning while we iterate.
	# This is not allowed by python. To get around this we predfine nodes as 
	nodes = dict(new_graph.nodes(data = True))
	# And then we loop throught the nodes dictionary
	for node in nodes:
		node_decade = int(nodes[node]["active_start"])
		if node_decade > decade:		
			new_graph.remove_node(node)
	print("The decade that we have selected is: " + str(decade))
	# Is our graph an acyclic directed graph
	print("Our graph is an acyclic directed graph: " + str(nx.is_directed_acyclic_graph(new_graph)))

	# Check nodes
	num_nodes = new_graph.number_of_nodes()
	num_edges = new_graph.number_of_edges()
	num_possible_edges = num_nodes*(num_nodes - 1)
	print("Our artistic influence network has " + str(num_nodes)+" artists.")
	print("Our artistic influence network has " + str(num_edges)+" edges out of a possible " + str(num_possible_edges) + " possible edges.")
	print("Our network density is: " + str(nx.density(new_graph)))

	return new_graph

def build_decade_genre_graph(graph, decade, genre):
	# Must make copy to avoid changing intial graph!
	new_graph = graph.copy()
	# We need to loop through our graph's nodes but within the loop we 
	# are removing edges! Note that self.network.nodes is a dictionary and would be chaning while we iterate.
	# This is not allowed by python. To get around this we predfine nodes as 
	nodes = dict(new_graph.nodes(data = True))
	# And then we loop throught the nodes dictionary
	for node in nodes:
		node_decade = int(nodes[node]["active_start"])
		node_genre = nodes[node]["genre"]
		if node_decade == decade:
			if node_genre != genre:
				new_graph.remove_node(node)
		if node_decade > decade:	
			new_graph.remove_node(node)
	print("The decade that we have selected is: " + str(decade) + " and the genre we have selected is " + str(genre))
	# Is our graph an acyclic directed graph
	print("Our graph is an acyclic directed graph: " + str(nx.is_directed_acyclic_graph(new_graph)))

	# Check nodes
	num_nodes = new_graph.number_of_nodes()
	num_edges = new_graph.number_of_edges()
	num_possible_edges = num_nodes*(num_nodes - 1)
	print("Our artistic influence network has " + str(num_nodes)+" artists.")
	print("Our artistic influence network has " + str(num_edges)+" edges out of a possible " + str(num_possible_edges) + " possible edges.")
	print("Our network density is: " + str(nx.density(new_graph)))

	return new_graph

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
	# Compute the in degree centrality of our graph
	in_deg_cent_dict = nx.in_degree_centrality(graph)
	# Compute the out degree centrality of our graph
	out_deg_cent_dict = nx.out_degree_centrality(graph)
	# Compute the betweenness centrality of our graph
	bet_cent_dict = nx.betweenness_centrality(graph)
	# Compute the Katz centrality of our graph
	katz_cent_dict = nx.katz_centrality(graph)
	# Compute the PageRank of nodes on our graph
	pagerank_dict = nx.pagerank(graph)
	# Compute the eigenvector centrality of our graph
	eigenvector_dict = nx.eigenvector_centrality(graph, max_iter = 500)
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
			row = [node, artist_name[node], in_deg_cent_dict[node], out_deg_cent_dict[node], bet_cent_dict[node], katz_cent_dict[node], pagerank_dict[node], eigenvector_dict[node], closeness_dict[node]]
			filewriter.writerow(row)


# This was lifted from http://github.com/flaviovdf/allmusic-disruption
def compute_disruption(G, min_in=1, min_out=0):

    id_to_node = dict((i, n) for i, n in enumerate(G.nodes))
    in_count = dict(G.in_degree(G.nodes))
    out_count = dict(G.out_degree(G.nodes))

    F = nx.to_scipy_sparse_matrix(G, format='csr')
    T = nx.to_scipy_sparse_matrix(G, format='csc')
    D = np.zeros(shape=(F.shape[0], 6))

    for node_id in range(F.shape[0]):
        if in_count[id_to_node[node_id]] >= min_in and \
                out_count[id_to_node[node_id]] >= min_out:
            ni = 0
            nj = 0
            nk = 0

            outgoing = F[node_id].nonzero()[1]
            incoming = T[:, node_id].nonzero()[0]
            outgoing_set = set(outgoing)

            for other_id in incoming:
                second_level = F[other_id].nonzero()[1]
                if len(outgoing_set.intersection(second_level)) == 0:
                    ni += 1
                else:
                    nj += 1

            # who mentions my influences
            who_mentions_my_influences = np.unique(T[:, outgoing].nonzero()[0])
            for other_id in who_mentions_my_influences:
                # do they mention me?! if no, add nk
                if F[other_id, node_id] == 0 and other_id != node_id:
                    nk += 1

            D[node_id, 0] = ni
            D[node_id, 1] = nj
            D[node_id, 2] = nk
            D[node_id, 3] = (ni - nj) / (ni + nj + nk)
            D[node_id, 4] = in_count[id_to_node[node_id]]
            D[node_id, 5] = out_count[id_to_node[node_id]]
        else:
            D[node_id, 0] = np.nan
            D[node_id, 1] = np.nan
            D[node_id, 2] = np.nan
            D[node_id, 3] = np.nan
            D[node_id, 4] = in_count[id_to_node[node_id]]
            D[node_id, 5] = out_count[id_to_node[node_id]]

    return pd.DataFrame(D, index=G.nodes,
                        columns=['ni', 'nj', 'nk', 'disruption', 'in', 'out'])

def find_in_out_degree_collision(graph):
	node_list = []
	for node in graph:
		if graph.in_degree(node) == graph.out_degree(node):
			node_list.append(node)
	print("We have " + str(len(node_list)) + " instances where a node's in degree is equal to its out degree.")

	return node_list	

def plot_power_law(graph):
	"""
	Compare a power law distribution of node in-degrees to lognormal, exponential, lognormal positive, stretched exponential, and truncated power law	

	Parameters
	----------
	graph : a NetworkX directed graph
	
	Notes
	-----
	See comment by Aaron Clauset in the thread:
	https://stackoverflow.com/questions/49266070/comparing-power-law-with-other-distributions

	"""
	data = [graph.in_degree(n) for n in graph.nodes()]
	fit = powerlaw.Fit(data)
	print("-------------------")
	print("Power law compared with lognormal: " + str(fit.distribution_compare('power_law', 'lognormal')))
	print("Power law compared with exponential: " + str(fit.distribution_compare('power_law', 'exponential')))
	print("Power law compared with lognormal positive: " + str(fit.distribution_compare('power_law', 'lognormal_positive')))
	print("Power law compared with stretched exponential: " + str(fit.distribution_compare('power_law', 'stretched_exponential')))
	print("Power law compard with truncated power law: " + str(fit.distribution_compare('power_law', 'truncated_power_law')))
	print("-------------------")
	'''
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
	'''

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

# As a csv.reader is usuable once and only once we write the lines of our csv file to a list 
with open("influence_data.csv", "rt") as infile:
	reader = csv.reader(infile)
	next(reader)
	influence_data = list(reader) 

# As a csv.reader is usuable once and only once we write the lines of our csv file to a list 
with open("data_by_artist.csv", "rt") as infile:
	reader = csv.reader(infile)
	next(reader)
	artist_data = list(reader) 


