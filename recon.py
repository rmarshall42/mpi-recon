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


import repo
import recon_search as search
import recon_probe as probe
import recon_cli as rc
from recon_cli import ReconConfig
import os
import json
import sys
#import sys
#import getopt
import argparse
from github import Github
#----------------------------------------------------------------------------

USE_CACHE=True


def recon_info(rc):
	print (rc.to_string())
#----------------------------------------------------------------------------







#def recon_search(rc):
#	print (rc.to_string())
#----------------------------------------------------------------------------



def do_search(rcli):
	print ("** mpi-recon: live search **", file = sys.stderr)
	print ("query: " + str_query, file = sys.stderr)
	#resultset = search.do_search(g, str_query,20)
	#resultset = search.github_search(rcli.github_obj, rcli.keywords)
	resultset = search.github_search(rcli)
	if resultset:
		for i,snip in resultset.items():
			print(str(i), file = sys.stderr)
			if snip:
				for k,line in snip.items():
					#print(str(k)+"\n"+line)
					print(k, file = sys.stderr)

					json_object = json.dumps(line, indent = 4) 
					print(json_object, file = sys.stderr)
			print("--------", file = sys.stderr)
#----------------------------------------------------------------------------






def recon_usage(rc):
	print (rc.to_string())
#----------------------------------------------------------------------------


def print_resultset(resultset):
	for i,snip in resultset.items():
		print(str(i))
		for k,line in snip.items():
			print(str(k)+"\n"+line)
		print("--------")
#----------------------------------------------------------------------------


def get_interesting(resultset):
	print (resultset)
#----------------------------------------------------------------------------



def do_recon(recon, sort_by_size=True):


	if recon.do_probe:
		corpus_basic = probe.do_probe(\
			recon.github_obj, recon.keywords, recon.topics, recon.json_infile, recon.dbfile)


		if sort_by_size:
			corpus_basic.sort(key=lambda x: x['size'])
		
		#print(json.dumps(corpus_basic, indent=4))
		return corpus_basic
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
if __name__ == "__main__":
	

	# ./recon.py --probe --infile data/topics-mpi.json

	recon = rc.recon_cli(os.environ.get('GITHUB_TOKEN'))

	print (recon.to_string())

	results = do_recon(recon)

	print(json.dumps(results, indent=4))















