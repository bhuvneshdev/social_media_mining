from __future__ import unicode_literals
import requests
import json
import time
import codecs
import sys
import pdb
import networkx as nx
import csv
import matplotlib.pyplot as plt
import snap
from snap import *
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)



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

def create_random_graph_snap():
	UGraph = snap.GenRndGnm(snap.PUNGraph, 8986, 1000482)
	return UGraph

def create_small_world_graph_snap():
	Rnd = snap.TRnd(1,0)
	UGraph1 = snap.GenSmallWorld(8986, 222, 0.74, Rnd)
	return UGraph1

def create_pref_attach_model():
	Rnd = snap.TRnd()
	UGraph = snap.GenPrefAttach(8986, 222, Rnd)
	return UGraph


def calculate_average_path_length(graph):
	edges = graph.edges()
	length = 0
	for itr in edges:
		length += nx.shortest_path_length(graph,source=itr[0],target=itr[1])
# average_path_length = (length/len(edges))
	return average_path_length

def draw_degree_distribution_snap(graph):
	snap.PlotInDegDistr(graph, "example", "Preferential Undirected graph - degree Distribution")

# def calculate_preferential_graph():
# 	return nx.barabasi_albert_graph(1000,4)

def calculate_clustering_coeff(graph):
	return nx.average_clustering(graph)

def calculate_local_clustering_coeff(graph):
	hash_clus = nx.clustering(graph)
	clus = 0
	nodes = graph.nodes()
	for itr in graph.nodes():
		clus = clus + hash_clus[itr]
	print(clus/len(nodes))

def calculate_average_path_length(graph):
	diam = snap.GetBfsEffDiam(graph,graph.GetNodes(),'false')
	print diam

def calculate_average_degree_snap(graph):
	nodes = graph.Nodes()
	total_count = 0
	count = 0
	for itr in nodes:
		total_count += itr.GetInDeg()
		count += 1
	print(total_count/count)

def calculate_average_degree_networkx(graph):
	degrees = graph.degree().values()
	total_count = 0
	for itr in degrees:
		total_count +=  itr
	print(total_count/(graph.number_of_nodes()))

def calculate_global_clustering_snap(graph):
	clus = snap.GetClustCf (graph, -1)
	print clus

def calculate_local_clustering_snap(graph):
	NIdCCfH = snap.TIntFltH()
	snap.GetNodeClustCf(graph, NIdCCfH)
	max = 0
	for item in NIdCCfH:
		if(NIdCCfH[item] > max):
			max  = NIdCCfH[item]
	print max


def main():
	networkx_graph = create_graph_networkx()
	snap_graph = create_graph_snap()


	########REAL WORLD GRAPH RESULTS#########
	print("REAL WORLD GRAPH RESULTS")
	print "Average Path Length %s." % calculate_average_path_length(snap_graph)
	# calculate_average_path_length(snap_graph)
	print "Global Clustering %s." % calculate_global_clustering_snap(snap_graph)
	print "Local Clustering %s." % calculate_local_clustering_snap(snap_graph)
	print "Degree Distribution %s." % draw_degree_distribution_snap(snap_graph)



	#######RANDOM WORLD GRAPH RESULTS#########
	print("RANDOM WORLD GRAPH RESULTS")
	random = create_random_graph_snap()
	print "Average Path Length %s." % calculate_average_path_length(random)
	print "Global Clustering %s." % calculate_global_clustering_snap(random)
	print "Local Clustering %s." %calculate_local_clustering_snap(random)
	print "Degree Distribution %s." % draw_degree_distribution_snap(random)


	#######SMALL WORLD GRAPH RESULTS##########
	print("SMALL WORLD GRAPH RESULTS")
	small = create_small_world_graph_snap()
	print "Average Path Length %s." % calculate_average_path_length(small)
	print "Global Clustering %s." % calculate_global_clustering_snap(small)
	print "Local Clustering %s." % calculate_local_clustering_snap(small)
	print "Degree Distribution %s." % draw_degree_distribution_snap(small)



	#######PREF ATTACH GRAPH RESULTS##########
	print("PREF ATTACH GRAPH RESULTS")
	pref = create_pref_attach_model()
	print "Average Path Length %s." % calculate_average_path_length(pref)
	print "Global Clustering %s." % calculate_global_clustering_snap(pref)
	print "Local Clustering %s." % calculate_local_clustering_snap(pref)
	print "Degree Distribution %s." % draw_degree_distribution_snap(pref)
	

if __name__ == '__main__':
	main()


