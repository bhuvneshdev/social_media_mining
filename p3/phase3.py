from __future__ import unicode_literals
import requests
import json
import time
import codecs
import sys
import pdb
import networkx as nx
import csv
import operator
import snap
from snap import *
import matplotlib.pyplot as plt

######
import random
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# def import_csv():
# 	f=open('ano_edges.csv','rb')
# 	G=nx.Graph()
# 	reader=csv.reader(f)
# 	for row in reader:
# 		# G.add_edge(row[0],row[1].lstrip(' '))
# 		G.add_edge(row[0],row[1])
# 	return G
def create_graph_networkx():
	G = nx.Graph()
	f=open('anonymized_edge_list.csv','rb')
	reader = csv.reader(f)
	for row in reader:
		G.add_edge(row[0],row[1])
	return G

def create_graph_snap():
	G = TUNGraph.New()
	f=open('anonymized.csv','rb')
	reader = csv.reader(f)
	for row in reader:
		G.AddNode(int(row[1]))
	f1=open('anonymized_edge_list.csv','rb')
	reader = csv.reader(f1)
	for row in reader:
		G.AddEdge(int(row[0]),int(row[1]))
	return G

def calculate_clustering_coeff(graph):
	return nx.average_clustering(graph)

def calculate_local_clustering_coeff(graph):
	hash_clus = nx.clustering(graph)
	clus = 0
	nodes = graph.nodes()
	max = 0
	for item in nodes:
		if(hash_clus[item] > max):
			max  = hash_clus[item]
	print max

	# for itr in graph.nodes():
	# 	clus = clus + hash_clus[itr]
	# print(clus/len(nodes))

#################USING NETWORK X #################
def calculate_degree_centrality(graph):
	# Using Networkx
	hash_new= {}
	degree_centrality = nx.degree_centrality(graph)
	for l in graph.nodes():
		hash_new[l] = degree_centrality[l]
	arr = sorted(hash_new, key=hash_new.get, reverse=True)[:10]
	for itr in arr:
		print(itr)
		print("=====")
		print(degree_centrality[itr])

def calculate_eigen_vector_centrality(graph):
	eigen_vector_centrality = nx.eigenvector_centrality(graph)
		# print(eigen_vector_centrality)
	hash_new ={}
	for l in graph.nodes():
		hash_new[l] = eigen_vector_centrality[l]
	arr = sorted(hash_new, key=hash_new.get, reverse=True)[:10]
	for itr in arr:
		print(itr)
		print("=====")
		print(eigen_vector_centrality[itr])

def calculate_page_rank(graph):
	page_rank = nx.pagerank(graph,alpha=0.9)
	hash_new ={}
	for l in graph.nodes():
		hash_new[l] = page_rank[l]
	arr = sorted(hash_new, key=hash_new.get, reverse=True)[:10]
	for itr in arr:
		print(itr)
		print("=====")
		print(page_rank[itr])
		####TO DO arrange in order#######

def calculate_jaccard_similarity(graph):
	preds = nx.jaccard_coefficient(graph,graph.edges())
	hash_new = {}
	for u, v, p in preds:
		hash_new[str(u) + ',' + str(v)] = p
	arr_nodes = (max(hash_new.iteritems(), key=operator.itemgetter(1))[0])
	arr_value = (max(hash_new.iteritems(), key=operator.itemgetter(1))[1])
	print("nodes")
	print(arr_nodes)
	print("Jaccard Coefficient")
	print(arr_value)



def main():
	graph = create_graph_networkx()
	print("Average Local Clustering Coefficient")
	calculate_local_clustering_coeff(graph)
	print("=========================================================")
	calculate_clustering_coeff(graph)
	print("Top 10 Degree Centrality")
	calculate_degree_centrality(graph)
	print("=========================================================")
	print("Top 10 Eigen Vector Centrality")
	calculate_eigen_vector_centrality(graph)
	print("=========================================================")
	print("Top 10 Page Rank Values")
	calculate_page_rank(graph)
	print("=========================================================")
	print("Jaccard Centrality")
	calculate_jaccard_similarity(graph)
	print("=========================================================")


if __name__ == '__main__':
	main()

