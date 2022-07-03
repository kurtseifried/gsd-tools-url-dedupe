#!/usr/bin/env python3

# Reading all 250k files into an array takes about 3 minutes.
# Reading them all from a single file takes about 40 seconds
# So if you're doing testing/dev this saves quite a bit of time

import os
import re
import json

# This only works when run from the gsd-database directory
filesystem_path = "./"

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

def write_data_to_json_file(json_data):
	# Raw file, the whole thing
	with open('GSD-mega-file.json', 'w', encoding='utf-8') as f:
		json.dump(all_gsd_data, f, ensure_ascii=False, indent=2)

######################

all_gsd_data = load_gsd_files_into_memory(filesystem_path)

write_data_to_json_file(all_gsd_data)

# count should always be 1 but in case it isn't let's explicitly count it

# Just the URLs JSON file:
# {GSD {namespace {references/repo {list of urls: count}}}}

# CSV file (escaped excel format):
# GSD,namespace,reference/repo,url,domain,path,count
