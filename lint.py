#!/usr/bin/python3

# To use this script, first:
#
# pip3 install rtyaml

import csv
import glob
import io
import re
from datetime import date

import rtyaml

for fn in sorted(glob.glob("scorecards/*.yaml")):
	with open(fn, "r+") as f:
		# Split on "...".
		scorecard = f.read()
		metadata, scores = scorecard.split("\n...\n")

		# Parse the YAML for the top half.
		metadata = rtyaml.load(metadata)

		# Validate metadata. Required fields...
		for key, datatype in (("name", str), ("homepage", str), ("link", str), ("updated", date), ("based-on", str), ("type", str)):
			if (metadata.get(key, "") or "") == "":
				raise ValueError("Missing required field {} in {}.".format(key, fn))
			if not isinstance(metadata[key], datatype):
				raise ValueError("Invalid data type {} for field {} in {}, should be {}.".format(type(metadata.get(key)).__name__, key, fn, datatype.__name__))
		
		# Optional fields..
		for key, datatype in (("abbrev", str),):
			if not isinstance(metadata.get(key), (str, type(None))):
				raise ValueError("Invalid data type {} for field {} in {}, should be {}.".format(type(metadata.get(key)).__name__, key, fn, datatype))
		
		# Field values.
		if metadata["type"] not in ("percent", "grade"):
				raise ValueError("Invalid value for field {} in {}, should be 'percent' or 'grade'.".format(key, fn))

		# Load the remaining data as a TSV.
		scores = list(csv.reader(io.StringIO(scores), delimiter=","))

		# Write it out again.
		f.seek(0)
		f.truncate()
		f.write(rtyaml.dump(metadata))
		f.write("...\n")
		w = csv.writer(f, delimiter=",", lineterminator="\n")
		for row in scores:
			# Validate data.
			if len(row) != 3: raise ValueError("Not three columns: " + row)
			if row[1].strip() == "": raise ValueError("Empty score in " + row)

			# Left-pad the score column to make it easier to scan visually.
			row[1] = " "*(3-len(row[1])) + row[1]

			w.writerow(row)

		print(metadata['name'])
