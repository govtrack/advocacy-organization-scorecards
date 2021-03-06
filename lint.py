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
				raise ValueError("Invalid value for type in {}, should be 'percent' or 'grade'.".format(fn))

		# Load the remaining data as a TSV.
		scores = list(csv.reader(io.StringIO(scores), delimiter=","))

		def is_int(v):
			try:
				int(v)
			except ValueError:
				return False
			return True

		# Validate data.
		for row in scores:
			if len(row) != 3: raise ValueError("Not three columns: " + repr(row) + " (" + fn + ")")
			if row[1].strip() == "": raise ValueError("Empty score in " + repr(row) + " (" + fn + ")")
			if metadata["type"] == "percent" and not is_int(row[1]): raise ValueError("Invalid score (must be an integer for percent scores) in " + repr(row) + " (" + fn + ")")

		# Write it out again.
		f.seek(0)
		f.truncate()
		f.write(rtyaml.dump(metadata))
		f.write("...\n")
		w = csv.writer(f, delimiter=",", lineterminator="\n")
		for row in scores:
			# Left-pad the score column to make it easier to scan visually.
			row[1] = " "*(3-len(row[1])) + row[1]
			w.writerow(row)

		print(metadata['name'])
