#!/usr/bin/env python3

#############################################################################
# mpi-recon                                                                 #
#                                 _                                         #
#                ____ ___  ____  (_)     ________  _________  ____          #
#               / __ `__ \/ __ \/ /_____/ ___/ _ \/ ___/ __ \/ __ \         #
#              / / / / / / /_/ / /_____/ /  /  __/ /__/ /_/ / / / /         #
#             /_/ /_/ /_/ .___/_/     /_/   \___/\___/\____/_/ /_/          #
#                      /_/                                                  #
#                                                                           #
#############################################################################


#import repo

import os
import re
import time

#import sys
#import getopt
#import argparse
#----------------------------------------------------------------------------

LINES_BEHIND = 1
LINES_AHEAD = 1
GAP_THRESHOLD = 10 # merge 2 code snippets A, B if they are less than this many lines apart.

def get_codestring(filebuffer, idx_first, idx_last):

	return "".join([filebuffer[idx] for idx in range(idx_first, idx_last+1)])
#----------------------------------------------------------------------------


def grep_file_for(filename, pattern):
	buffered_result = {}
	filebuffer = {}
	foundbuffer = {}


	if os.path.exists(filename):
		regex = re.compile(pattern)
		with open(filename,'r') as inputFile:
			for line_i, line in enumerate(inputFile, 1):
				# check if we have a regex match
				filebuffer[line_i] = line
				if regex.search( line ):
					foundbuffer[line_i] = line

		for line_i,line in filebuffer.items():
			if line_i in foundbuffer:
				# replace this with get_codestring if it works ok
				prevln = str(filebuffer.get(line_i - 1))
				currln = str(filebuffer.get(line_i))
				nextln = str(filebuffer.get(line_i + 1))
				
				buffered_result[line_i] = prevln + currln + nextln    

	return buffered_result
#----------------------------------------------------------------------------

# see if we have the file locally
def has_local(fn):
	try:
		x = open(fn, "r")
		return True
	except IOError:
		return False
#----------------------------------------------------------------------------


# this is where we can search local cache first before github
def get_file(file, cachedir='./cache'):
	if not os.path.exists(cachedir):
		os.makedirs(cachedir)

	filepath = str(cachedir + "/" + file.name)
	local = has_local(filepath)

	if not local:
		import requests

		its_local_now = requests.get(f'{file.download_url}')
		try: 
			local = open(filepath, "w").write(its_local_now.text)
		except IOError:
			return False

	return local
#----------------------------------------------------------------------------

#manage rate limit before calling Github.search_code
def call_search(g, query, minval = 1):
	result = None
	rate_limit = g.get_rate_limit()
	srate = rate_limit.search
	crate = rate_limit.core

	sleep_limit = 0.5
	time_limit = 15.0

	while srate.remaining < minval or crate.remaining < minval:
		time.sleep(sleep_limit)
		time_limit -= sleep_limit
		print(f'rates(search, core): ({srate.remaining},{crate.remaining})')

	result = g.search_code(query, order='desc')

	return result[:20]
#----------------------------------------------------------------------------


def github_search(g, keyword, cachedir="./cache"):
	query = f'"{keyword} " language:cpp language:c'
	result = call_search(g, query)
	resultset = {}

	flood_ctrl = 4 # stop after retrieving this many files

	if result:
		rate_limit = g.get_rate_limit()
		srate = rate_limit.search
		crate = rate_limit.core
		i = 0
		
		for file in result:
			print (f'rates({srate},{crate})')
			if i < flood_ctrl:
				res = get_file(file)
				if res:
					resultset[file.name] = \
						grep_file_for(cachedir + "/" + file.name, keyword)			
			else:
				print("flood_ctrl")
				print(f'{file.download_url}')
			i += 1

	return resultset
#----------------------------------------------------------------------------


def do_search(g, q, max_results=0):
	i = 1

	for rp in g.search_repositories(q, sort="stars", order="desc"):
		row = {
			'name' : rp.name,
			'language' : rp.language,
			'stars' : rp.stargazers_count,
			'forks' : rp.forks_count,
			'updated_at' : rp.updated_at,
			'created_at' : rp.created_at
		}
		i=i+1
		print(row)
		if i == max_results:
			break

