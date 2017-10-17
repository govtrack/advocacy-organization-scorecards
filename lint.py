#!/usr/bin/python3

# To use this script, first:
#
# pip3 install rtyaml

import csv
import glob
import io
import re

import rtyaml

for fn in sorted(glob.glob("scorecards/*.yaml")):
	with open(fn, "r+") as f:
		# Split on "...".
		scorecard = f.read()
		metadata, scores = scorecard.split("\n...\n")

		## Parse the YAML for the top half.
		metadata = rtyaml.load(metadata)

		# Load the remaining data as a TSV.
		scores = list(csv.reader(io.StringIO(scores), delimiter=","))
		
		# Write it out again.
		f.seek(0)
		f.truncate()
		f.write(rtyaml.dump(metadata))
		f.write("...\n")
		w = csv.writer(f, delimiter=",", lineterminator="\n")
		for row in scores:
			row[1] = " "*(3-len(row[1])) + row[1]
			w.writerow(row)

		print(metadata['name'])