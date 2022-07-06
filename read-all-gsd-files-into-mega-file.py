#!/usr/bin/env python3

# Reading all 250k files into an array takes about 3 minutes.
# Reading them all from a single file takes about 40 seconds
# So if you're doing testing/dev this saves quite a bit of time

import os
import re
import json
import csv

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

def open_csv_output_file():
	#
	# open file and leave open
	#
	global csv_writer
	CSV_file_path = "GSD-all-links.csv"
	csv_file = open(CSV_file_path, 'w', encoding='UTF8')
	# create the csv writer
	csv_writer = csv.writer(csv_file)
	header = ['gsd_id_value', 'data_type_value', 'namespace_value', 'status_message', 'url_value', 'domain_name']
	csv_writer.writerow(header)
	#



def handle_gsd_output(gsd_id_value, data_type_value, namespace_value, url_value):
	# Get TLD (domain + suffix), if it's not valid suffix will be a null str
	# (domain_info.subdomain, domain_info.domain, domain_info.suffix)
	if type(url_value) == str:
		domain_info = tldextract.extract(url_value)
	else:
		domain_info = tldextract.extract("")
		print("ERROR: " + gsd_id_value + " " + str(url_value))
	# Error out if the TLD is malformed
	if domain_info.suffix == "":
		status_message = "ERROR: bad tld"
	# TLD is ok, check url
	else:
		# Check if url is correctly formatted
		if validators.url(url_value) == True:
			status_message = "Good link"
		else:
			status_message = "ERROR: possible bad url format"
	#
	# CSV output
	#
	domain_name = domain_info.domain  + "." + domain_info.suffix
	data_entry = [gsd_id_value, data_type_value, namespace_value, status_message, url_value, domain_name]
	csv_writer.writerow(data_entry)
	#
	# We can print the output
	#
#	print(str(status_message)+ " " + str(gsd_id_value) + " " + str(data_type_value) + " " + str(namespace_value) + " " + str(url_value) + " " + domain_info.domain  + "." + domain_info.suffix)




def write_data_to_json_file(json_data, filename):
	# Raw file, the whole thing
	with open(filename, 'w', encoding='utf-8') as f:
		json.dump(all_gsd_data, f, ensure_ascii=False, indent=2)

# TODO: what happens if it's not a dict/list/str? what about a boolean? or INT
def walk_dict(data, gsdkey, namespace):
	for key,value in data.items():
		if isinstance(value, str):
			if str(key) == "url":
				handle_gsd_output(gsdkey, "url", namespace, value)
			if str(key) == "repo":
				handle_gsd_output(gsdkey, "repo", namespace, value)
		if isinstance(value, dict):
			walk_dict(value, gsdkey, namespace)
		elif isinstance(value, list):
			for val in value:
				if isinstance(val, str):
					if key == "references":
						# It's a list so we need to walk it
						# the list might be a dict and not just entries. ### TODO
						for url_entry in value:
							if type(url_entry) == str:
								handle_gsd_output(gsdkey, "references", namespace, url_entry)
							else:
								walk_dict(url_entry, gsdkey, namespace)
				elif isinstance(val, list):
					pass
				else:
					walk_dict(val, gsdkey, namespace)



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
				walk_dict(rootvalue, gsdkey, "GSD")
			elif rootkey == "OSV":
				walk_dict(rootvalue, gsdkey, "OSV")
			elif rootkey == "namespaces":
				for namespacekey,namespacevalue in rootvalue.items():
					walk_dict(namespacevalue, gsdkey, namespacekey)
			elif rootkey == "overlay":
				# ignore for now
				continue
			else:
				# print an error
				handle_gsd_output(gsdkey, "ERROR: unknown format", namespace, value)
				#print("ERROR, UNKNOWN DATA FOUND: " + gsdkey + " " + rootkey )

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
#all_gsd_data = load_gsd_files_into_memory(filesystem_path)

# Write the GSD file data dict into a single huge file
#write_data_to_json_file(all_gsd_data, gsd_mega_file_name)

# Load the mega GSD file into a large dict in memory
#
all_gsd_data = load_gsd_megafile_into_memory(gsd_mega_file_name)
open_csv_output_file()
process_gsd_data(all_gsd_data)

#
# count should always be 1 but in case it isn't let's explicitly count it

# Just the URLs JSON file:
# {GSD {namespace {references/repo {list of urls: count}}}}

# CSV file (escaped excel format):
# GSD,namespace,reference/repo,url,domain,path,count
