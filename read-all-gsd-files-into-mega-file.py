#!/usr/bin/env python3

# Reading all 250k files into an array takes about 3 minutes.
# Reading them all from a single file takes about 40 seconds
# So if you're doing testing/dev this saves quite a bit of time

import os
import re
import json

# This only works when run from the gsd-database directory
path ="./"

gsdfilelist = []
gsd_data={}

for root, dirs, files in os.walk(path):
	for file in files:
                # Make sure we only load GSD files so check if starts with year
                if re.match("\./[0-9][0-9][0-9][0-9]/.*", root):
                        gsd=file.replace(".json", "")
                        print(gsd)
                        f = open(os.path.join(root,file))
                        gsd_data[gsd]=json.load(f)
                        f.close()

with open('GSD-mega-file.json', 'w', encoding='utf-8') as f:
    json.dump(gsd_data, f, ensure_ascii=False, indent=2)
