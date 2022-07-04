#!/usr/bin/env python3

# Reading all 250k files into an array takes about 3 minutes.
# Reading them all from a single file takes about 40 seconds
# So if you're doing testing/dev this saves quite a bit of time

import os
import re
import json
import validators
# pip3 install validators
import tldextract
# pip3 install tldextract

#### Options
#
# load-filesystem-path - path to gsd-database
# load-file - file to load

# output-file - file to write to
#


# This only works when run from the gsd-database directory
filesystem_path = "./"
gsd_mega_file_name = "GSD-mega-file.json"

def load_gsd_files_into_memory(path):
	gsd_data = {}
	for root, dirs, files in os.walk(path):
		for file in files:
			# Make sure we only load GSD files so check if starts with year
			# TODO: better check, maybe GSD-INT-INT?
			if re.match("\./[0-9][0-9][0-9][0-9]/.*", root):
				gsd = file.replace(".json", "")
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

# TODO: what happens if it's not a dict/list/str? what about a boolean? or INT
def walk_dict(data, gsdkey):
	for key,value in data.items():
		if isinstance(value, str):
			if str(key) == "url":
				print (gsdkey + " " + value)
			if str(key) == "repo":
				print (gsdkey + " " + value)
		if isinstance(value, dict):
			walk_dict(value, gsdkey)
		elif isinstance(value, list):
			for val in value:
				if isinstance(val, str):
					if key == "references":
						print(gsdkey + " " + val)
				elif isinstance(val, list):
					pass
				else:
					walk_dict(val, gsdkey)



# walk gsd mega files
# 1) dict, first keys are GSD ids
# 2) GSD ID dict keys: GSD, OSV, namespaces
# 3) namespaces dict
# 4) walk each namespace with the walk_dict
def process_gsd_data(data):
	# Layer one: GSD entries
	for gsdkey,gsdvalue in data.items():
		# Layer two: GSD/OSV/namespaces
		for rootkey,rootvalue in gsdvalue.items():
			if rootkey == "GSD":
				walk_dict(rootvalue, gsdkey)
			elif rootkey == "OSV":
				walk_dict(rootvalue, gsdkey)
			elif rootkey == "namespaces":
				for namespacekey,namespacevalue in rootvalue.items():
					walk_dict(namespacevalue, gsdkey)
			elif rootkey == "overlay":
				# ignore for now
				continue
			else:
				# print an error
				print("ERROR, UNKNOWN DATA FOUND: " + gsdkey + " " + rootkey )

# Data structure:
#{TLD:
#	SUBDOMAIN:
#			URLPATH:
#					PROTOCOL
#							valid url: yes/no?
#							totalcount:INT
#							GSD-ID:
#									count:INT
#									namespace:
#											name:count:INT

## url uniqueness
## TLD uniqueness
## count of urls in that TLD
## count of times that url is seen, how many GSDs
## who sees that data (which namespace)
## does archive.org have it?




## Validate URL - basic correctness (mistyped entries/etc)
# To check for urls lets use the validators
# pip3 install validators


## Validate DNS is live
# FUTURE FEATURE: do dns lookups, have a cache

## MIRROR URL
# FUTURE FEATURE: mirror URL and headers



# "url": str
# "references": list


######################

# Load all GSD files into a large dict in memory
##all_gsd_data = load_gsd_files_into_memory(filesystem_path)

# Write the GSD file data dict into a single huge file
##write_data_to_json_file(all_gsd_data, gsd_mega_file_name)

# Load the mega GSD file into a large dict in memory
all_gsd_data = load_gsd_megafile_into_memory(gsd_mega_file_name)

process_gsd_data(all_gsd_data)

#
# count should always be 1 but in case it isn't let's explicitly count it

# Just the URLs JSON file:
# {GSD {namespace {references/repo {list of urls: count}}}}

# CSV file (escaped excel format):
# GSD,namespace,reference/repo,url,domain,path,count
