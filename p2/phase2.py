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
import numpy as np
from snap import *
import matplotlib.pyplot as plt


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


def calculate_degree_distribution(graph):
	in_degrees = nx.degree(graph) # dictionary node:degree
	in_values = sorted(set(in_degrees.values()))
	in_hist = [in_degrees.values().count(x) for x in in_values]
	plt.plot(in_values,in_hist,'ro-')
	plt.title("Degree distribution")
	plt.xlabel("Degree Count")
	plt.ylabel("Count")
	plt.show(block=False)

def power_law_exponent(graph):
	in_degrees = nx.degree(graph) # dictionary node:degree
	in_values = sorted(set(in_degrees.values()))
	in_hist = [in_degrees.values().count(x) for x in in_values]
	plt.loglog(in_values,in_hist, basex=np.e, basey=np.e(-2))
	plt.show(block=False)

def calulate_diameter_graph(graph):
	diameter = nx.diameter(graph)
	return diameter

# def calculate_bridges(graph):
# 	n = nx.number_connected_components(graph)
# 	bridge_count = 0
# 	for edge in graph.edges():
# 		if (len(set(graph.neighbors(edge[0])) and set(graph.neighbors(edge[1])))==0):
# 			graph.remove_edge(edge[0], edge[1])
# 			if nx.number_connected_components(graph) > n:
# 				print edge, 'is a bridge'
# 				bridge_count += 1
# 			graph.add_edge(edge[0], edge[1])
# 	print bridge_count


def calculate_bridges(G):
	EdgeV = snap.TIntPrV()
	snap.GetEdgeBridges(G, EdgeV)
	count = 0
	for edge in EdgeV:
		count += 1
	print count

def calculate_num_triangles(graph):
	########## need to see this ###########
	count = 0
	triang = nx.triangles(graph)
	for itr in graph.nodes():
		count += triang[itr]
	return count

def calculate_number_of_connected_components(graph):
	########
	array = []
	test = range(1,101)
	for x in test:
		G = graph.copy()
		count_edges = G.number_of_edges()
		number_edges_removed = int((x*count_edges)/100)
		for itr in G.edges() :
			if number_edges_removed == 0 :
				break
			G.remove_edge(itr[0],itr[1])
			number_edges_removed -= 1
		cal = sorted(nx.connected_components(G))
		largest = len(cal[0])
		cont = cal[0]
		for i in cal:
			if(len(i) > largest):
				largest = len(i)
				cont = i

		if largest > 1 :
			array.append(largest)
		else:
			array.append(0)
	plt.plot(test,array)
	plt.title("Largest Connected Components after removing X% of nodes")
	plt.xlabel("X% Nodes Removed")
	plt.ylabel("Size of the Largest Component")
	plt.show(block=False)


def main():
	graph = create_graph_networkx()
	snapg = create_graph_snap()

	print("Number of Bridges")
	calculate_bridges(snapg)
	print("=====================================================")
	print("=====================================================")
	print("Number of 3 Cycles")
	calculate_num_triangles(graph)
	print("=====================================================")
	print("=====================================================")
	print("Calculate diameter")
	calulate_diameter_graph(graph)
	print("=====================================================")
	print("=====================================================")
	calculate_degree_distribution(graph)
	print("=====================================================")
	print("=====================================================")


if __name__ == '__main__':
	main()
