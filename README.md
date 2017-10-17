Congressional Scorecards Data
=============================

This repository collects scorecard ratings of Members of the United States Congress published by
advocacy organizations.

Each file in the scorecards directory starts with a metadata block in YAML format:

	name:     Americans for Prosperity
	abbrev:   ~
	homepage: https://americansforprosperity.org/
	link:     http://afpscorecard.org/
	updated:  2017-08-30
	based-on: based on votes in the 115th Congress
	type:     percent
	...

The metadata block is terminated by three periods.

The `abbrev` field holds a common short form of the organization's name. It is optional and you may either leave out the line or set it to null using `~`. `updated` is the publication date of the scorecard or the date it was imported here in YYYY-MM-DD format.

Following the three periods is a CSV table of scores. Each row has
the GovTrack numeric identifier of a Member of Congress and the score (an integer
percentage or a letter grade). The third column holds notes for the data maintainer.

	412601,  5,AL 1 R Byrne
	412394,  5,AL 2 R Roby
	400341, 11,AL 3 R Rogers
	(etcetera..)
