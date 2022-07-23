#!/usr/bin/env python3

# Reading all 250k files into an array takes about 3 minutes.
# Reading them all from a single file takes about 40 seconds
# So if you're doing testing/dev this saves quite a bit of time

import os
import re
import json
import csv
from pathlib import Path
import re
import validators
import  urllib

import tldextract
# pip3 install tldextract
import jsonschema
# pip3 install jsonschema
from ipaddress import ip_address, IPv4Address
# pip3 install ipaddress

#### Options
#
# load-filesystem-path - path to gsd-database
# load-file - file to load
# output-file - file to write to


#
# This script only works when run from the gsd-database directory, you'll want
# to run it there, then copy the GSD-mega-file.json to wherever you're working on things
#
filesystem_path = "./"
gsd_mega_file_name = "GSD-mega-file.json"
CSV_file_path = "GSD-all-links.csv"


def load_gsd_files_into_memory(path):
	#
	# This walks the filesystem and loads all the GSD filesystem
	# TODO: better regex on filenames/etc. GSD-YEAR-INT.json?
	#
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
	#
	# Given a filename to the massive JSON load it into memory
	#
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
	csv_file = open(CSV_file_path, 'w', encoding='UTF8')
	# create the csv writer
	csv_writer = csv.writer(csv_file)
	header = ['gsd_id_value', 'data_type_value', 'namespace_value', 'url_status_message', 'url_value', 'hostname', 'domain_name']
	csv_writer.writerow(header)





# Always pass the key value in, e.g. key: thing, first item, key is null?
# Pass the key e.g. key:value, or key:[value1, [sublist]]
# If key is NULL vs blank?

# To process namespaces we can't make any assumptions about formats.



# Read the CSV file and output a data/ directory with data/org/name/each-unique-hostname.json
# within each directory
# This makes searching for a URL easy, and splits the domains up into sub directories so it's not to crowded

# The JSON data format is:
# {URL1: {gsd_list: {GSD_ID: {OSV/GSD/namespace: {URL_DATA}}}, {meta_data: {GSD COUNT, chances of being a duplicate, etc.}}},
#  URL2: {}...
# }
#


## url uniqueness
## TLD uniqueness
## count of urls in that TLD
## count of times that url is seen, how many GSDs
## who sees that data (which namespace)
## does archive.org have it?



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
#all_gsd_data = load_gsd_megafile_into_memory(gsd_mega_file_name)
#open_csv_output_file()
#process_gsd_data(all_gsd_data)


# What if we make key a list of keys.... how to add, easy, how to remove???? how deep...

def load_json_schema_OSV():
	# Load this into a global so we only do it once
	OSV_schema_file = "OSV-2022-04-schema.json"
	global global_OSV_schema_data
	f = open(OSV_schema_file)
	global_OSV_schema_data = json.load(f)
	f.close
	# https://raw.githubusercontent.com/ossf/osv-schema/main/validation/schema.json


def classify_url_hostname_type(IP: str) -> str:
    try:
        return "ipv4" if type(ip_address(IP)) is IPv4Address else "ipv6"
    except ValueError:
        return "dns"





def make_data_dedupe_file(hostname, data):
	hostname_type=classify_url_hostname_type(hostname)
	if hostname_type == "ipv4":
		pass
		# mkdir a/b/c/d/
		# touch a/b/c/d/a.b.c.d.json
		# Write data to file
	elif hostname_type == "dns":
		pass
		# mkdir tld/domain/whatever/
		# touch whatever.domain.tld.json
		# Write data to file


	# creates a blank file if it doesn't already exist
	# Examples:
	# dns/tld/name/tls.name.json
	# ipv4/a/b/c/d/a.b.c.d.json
	# ipv6/??????/ipv6.json
	# Other address formats? Git? Blockchains?
	# do we need to care about the protocol such as http/https/ftp/??? I don't think so.
	return True


def validate_json_schema_OSV(OSV_data):
	# Validate against the global OSV_schema_data
    try:
        jsonschema.validate(instance=OSV_data, schema=global_OSV_schema_data)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Given OSV JSON data is invalid OSV format"
        return False, err

    message = "Given OSV JSON data is valid"
    return True, message

def process_gsd_megafile(data):
	#
	# Process a single GSD entry (JSON data loaded into memory)
	#
	for key,value in data.items():
		gsd_id = key
		gsd_data = value
		process_gsd_entry(gsd_id, gsd_data)

def process_gsd_entry(gsd_id, gsd_data):
	key_list = []
	#
	# Process a single GSD entry (JSON data loaded into memory)
	#
	for key,value in gsd_data.items():
		if key == "OSV":
			# validate it
			#is_valid, msg = validate_json_schema_OSV(value)
			#print(msg)
			key_list.append("OSV")
			process_json_object(value, gsd_id, key_list)
		elif key == "GSD":
			key_list.append("GSD")
			process_json_object(value, gsd_id, key_list)
		elif key == "namespaces":
			key_list.append("namespaces")
			process_json_object(value, gsd_id, key_list)
		elif key == "overlay":
			key_list.append("overlay")
			process_json_object(value, gsd_id, key_list)
		else:
			print("ERROR, UNKNOWN ROOT LEVEL OBJECT IN JSON")
			print(key)
			quit()
		key_list.pop()

#
# get a json object, dict/list, values
#
def process_json_object(input_json_item, key_name, key_list):
	if type(key_list) is not list:
		print(key_name)
		quit()
	# Take an item and a key, on passing the root object pass a null key ""
	# A series of isinstances and then call the processor
	if type(input_json_item) is dict:
		if input_json_item:
			for key, value in input_json_item.items():
				#
				# first set the key_list
				#
				key_list.append(key)
				process_json_object(value, key_name, key_list)
				# Set a new key_name since it's a dict and we have a key:value
				key_list.pop()
		else:
			pass
	elif type(input_json_item) is list:
		if input_json_item:
			# If empty just ignore I guess
			if input_json_item:
				for value in input_json_item:
					process_json_object(value, key_name, key_list)
	elif type(input_json_item) is str:
		last_key = key_list[-1]
		search_words = ["defect", "references", "repo", "url", "urls"]
		# defect is 282 out of 13592 entries are URLs so worth grabbing
		# advisory should never be a URL but there is one in CVE-2017-14798
		# refsource should never be a URL but there is one in CVE-2018-15177 in the NVD data)
		if last_key in search_words:
			#
			# Check for basic url format first, lower case it, and simply match.
			#
			if re.match("^(ftp|http|https)://", input_json_item.lower()):
				if key_list[0] == "GSD" or "OSV":
					handle_gsd_output(key_name, key_list[0], str(key_list), input_json_item)
#					print(key_name + " " + input_json_item + " " + str(key_list))
				elif key_list[0] == "namespaces":
					# strip the first list item
					null_item = key_list.pop(0)
					handle_gsd_output(key_name, key_list[0], str(key_list), input_json_item)
				elif key_list[0] == "overlay":
					# remove the first two elements, POP POP!
					null_item = key_list.pop(0)
					null_item = key_list.pop(0)
					handle_gsd_output(key_name, "overlay", str(key_list), input_json_item)
				else:
					print("UNKNOWN DATA ERROR!!!!!")
			else:
				#
				# there are advisory ID's and whatnot en masse, so just ignore them
				#
				pass
	else:
		#
		# Ignore ints/floats/bools for now, hopefully no error slip through.
		#
		pass


def handle_gsd_output(gsd_id_value, data_type_value, namespace_value, url_value):
	url_status_message = "OK"
	# Get TLD (domain + suffix), if it's not valid suffix will be a null str
	# (domain_info.subdomain, domain_info.domain, domain_info.suffix)
	parsed_url = urllib.parse.urlparse(url_value)

	domain_info = tldextract.extract(parsed_url.netloc)

	# Error out if the TLD is malformed
	if domain_info.suffix == "":
		# CVE and others have links with bad TLD's e.g. "https://www.flightradar24.com.aa"
		url_status_message = "URL_ERROR: bad TLD"
		# Weed out IP addresses here? there are 13 links that are IP based in the dataset
		if re.match("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+", parsed_url.netloc):
			url_status_message = "URL_ERROR: IP Address"

	# TLD is ok, check url
	if validators.url(url_value) is True:
		pass
	else:
		url_status_message = "URL_ERROR: bad URL"
	#
	# CSV output
	#

	hostname = parsed_url.netloc
	domain_name = domain_info.domain  + "." + domain_info.suffix

	if write_output_to_csv == True:
		data_entry = [gsd_id_value, data_type_value, namespace_value, url_status_message, url_value, hostname, domain_name]
		csv_writer.writerow(data_entry)


def write_data_to_json_file(json_data, filename):
	# indent = 2, it saves a lot of space as per Josh
	# Raw file, the whole thing
	with open(filename, 'w', encoding='utf-8') as f:
		json.dump(all_gsd_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":

	#
	# Check if the mega data file exists, if not create it and save it locally
	#
	if Path(gsd_mega_file_name).is_file() is False:
		all_gsd_data = load_gsd_files_into_memory(filesystem_path)
		write_data_to_json_file(all_gsd_data, gsd_mega_file_name)

	#
	# Kurt likes CSV files. This takes along time to generate though
	#
	if Path(CSV_file_path).is_file() is False:
		all_gsd_data = load_gsd_megafile_into_memory(gsd_mega_file_name)
		open_csv_output_file()
		write_output_to_csv = True
		process_gsd_megafile(all_gsd_data)


	#all_gsd_data = load_gsd_megafile_into_memory(gsd_mega_file_name)




	#
	# count should always be 1 but in case it isn't let's explicitly count it

	# Just the URLs JSON file:
	# {GSD {namespace {references/repo {list of urls: count}}}}

	# CSV file (escaped excel format):
	# GSD,namespace,reference/repo,url,domain,path,count
