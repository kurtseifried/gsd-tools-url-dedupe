#!/usr/bin/env python3

# Reading all 250k files into an array takes about 3 minutes.
# Reading them all from a single file takes about 40 seconds
# So if you're doing testing/dev this saves quite a bit of time

import os
import re
import json

# This only works when run from the gsd-database directory
filesystem_path = "./"
gsd_mega_file_name = "GSD-mega-file.json"

def load_gsd_files_into_memory(path):
	gsd_data = {}
	for root, dirs, files in os.walk(path):
		for file in files:
			# Make sure we only load GSD files so check if starts with year
			if re.match("\./[0-9][0-9][0-9][0-9]/.*", root):
				gsd = file.replace(".json", "")
				#print(gsd)
				f = open(os.path.join(root,file))
				gsd_data[gsd] = json.load(f)
				f.close()
	return gsd_data

def load_gsd_megafile_into_memory(filename):
	gsd_data = {}
	f = open(filename)
	gsd_data = json.load(f)
	f.close()
	return gsd_data


def write_data_to_json_file(json_data, filename):
	# Raw file, the whole thing
	with open(filename, 'w', encoding='utf-8') as f:
		json.dump(all_gsd_data, f, ensure_ascii=False, indent=2)

def walk_dict(data):
	for key,value in data.items():
		if isinstance(value, str):
			print ("DICT VALUE: " + str(key) + " -> " + value)
		if isinstance(value, dict):
			walk_dict(value)
		elif isinstance(value, list):
			for val in value:
				if isinstance(val, str):
					print("LIST VALUE: " + val)
				elif isinstance(val, list):
					pass
				else:
					walk_dict(val)

# walk gsd mega files
# 1) dict, first keys are GSD ids
# 2) GSD ID dict keys: GSD, OSV, namespaces
# 3) namespaces dict


######################

# Load all GSD files into a large dict in memory
#all_gsd_data = load_gsd_files_into_memory(filesystem_path)

# Write the GSD file data dict into a single huge file
#write_data_to_json_file(all_gsd_data, gsd_mega_file_name)

# Load the mega GSD file into a large dict in memory
all_gsd_data = load_gsd_megafile_into_memory(gsd_mega_file_name)

walk_dict(all_gsd_data)

#
# count should always be 1 but in case it isn't let's explicitly count it

# Just the URLs JSON file:
# {GSD {namespace {references/repo {list of urls: count}}}}

# CSV file (escaped excel format):
# GSD,namespace,reference/repo,url,domain,path,count
