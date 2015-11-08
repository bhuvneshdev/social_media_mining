from __future__ import unicode_literals
import requests
import json
import time
import codecs
import sys
import pdb
import csv
import networkx as nx
import random
import copy
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)



def get_node_details_new():
	print("started")
	offset = 1
	array_data = []
	check = 1
	member_ids = []###
	topics = []###
	while (check):
		response = get_response(offset)
		# pdb.set_trace()
		offset += 1
		# return_count = response['meta']['count']
		if response['results']:
			# results = response['results']
			for itr in response['results']:
				arr_tops = []
				tops = itr['topics']
				member_id = itr['id']
				name = itr['name']
				for inner_itr in itr['topics']:
					# for tops in inner_itr 
					arr_tops.append(inner_itr['name'])
				# array_data.append({'member_id': itr['id'], 'simlarities': arr_tops, 'name': itr['name']})
				member_ids.append(itr['id'])
				topics.append(arr_tops)
		else:
			check = 0
	return {'member_id': member_ids,'topics': topics}

def running_bfs(details):
	# details = get_node_details
	ids = details['member_id']
	topics = details['topics']
	G = nx.Graph()
	recently_visited = set()
	sample = []
	queue = []
	edge_set = []
	queue.append(0)
	while queue:
		index = queue.pop(0)
		if len(recently_visited) > 1000 :
			break
		if index not in recently_visited:
			recently_visited.add(index)
			child = 0
			for itr in range(len(ids)):
				if child >= 1000:
					sample.add(itr)
					break;
				if itr != index and itr not in recently_visited:
					count = 0
					if(len(list(set(topics[itr]) & set(topics[index]))) >=17):
						queue.append(itr);
						child += 1
						edge_set.append([index,itr])
						break
	return {'edges': edge_set,'visited': recently_visited,'sample': sample}

def create_data_set(data,details):
	edges = data['edges']
	visited = data['visited']
	arr = set()
	for itr in visited:
		arr.add(itr)
	for itr in edges:
		arr.add(itr[0])
		arr.add(itr[1])
	count = 1
	hash_new = {}
	data_arr = []
	for itr in arr:
		data_arr.append([details['member_id'][itr],count])
		hash_new[details['member_id'][itr]] = count
		count += 1
	print(hash_new)
	with open('anonymized.csv', "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=str(u","))
		for line in data_arr:
			writer.writerow(line)
	non_ano_edges_arr = []
	ano_edges_arr = []
	for row in edges:
		non_ano_edges_arr.append([details['member_id'][int(row[0])],details['member_id'][int(row[1])]])
	coi = 0
	for row in edges:
		try:
			a = details['member_id'][row[0]]
			b = details['member_id'][row[1]]
			ano_edges_arr.append([hash_new[a],hash_new[b]])
		except:
			coi += 1
	print(coi)
	with open('edge_list.csv', "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=str(u","))
		for line in non_ano_edges_arr:
			writer.writerow(line)
	with open('anonymized_edge_list.csv', "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=str(u","))
		for line in ano_edges_arr:
			writer.writerow(line)

def get_response(offset):
	key = '3f3711136425202349287410343c2c5e'
	url = "https://api.meetup.com/2/members?offset=%s&group_urlname=coinvent&key=%s" %(offset,key)
	resp = requests.get(url)
	retry_count = 0
	response = resp.json()
	return response

def main():
	details = get_node_details_new()
	data = running_bfs(details)
	create_data_set(data,details)

if __name__ == '__main__':
	main()