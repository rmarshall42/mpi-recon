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
import search
import os
#import sys
#import getopt
import argparse
from github import Github
#----------------------------------------------------------------------------

USE_CACHE=True


def recon_info(options = None):
	print ("** mpi-recon: info **")
	print (options)
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

def recon_probe(g, str_query):
	print ("** mpi-recon: live probe **")
	print ("query: " + str_query)
	#search.do_search(g, str_query)
	resultset = search.github_search(g, str_query)
	get_interesting(resultset)

#----------------------------------------------------------------------------


def recon_search(g, str_query):
	print ("** mpi-recon: live search **")
	print ("query: " + str_query)
	#search.do_search(g, str_query)
	resultset = search.github_search(g, str_query)

	for i,snip in resultset.items():
		print(str(i))
		for k,line in snip.items():
			print(str(k)+"\n"+line)
		print("--------")
#----------------------------------------------------------------------------


def recon_cli(g):
	parser = argparse.ArgumentParser(prog="mpi-recon")
	parser.add_argument("--info", "-i", help="show some info")
	parser.add_argument("--probe", "-P", 
		default="MPI_Allgather", 
		help="probe for interesting repos, using the string in SEARCH")
	parser.add_argument("--search", "-s", 
		default="MPI_Allgather", 
		help="do a live search of github, using the string in SEARCH")
	args = parser.parse_args()

	if args.probe:
		q = args.probe
		recon_probe(g, q)
	elif args.search:
		#q = args.search + " language:cpp language:c language:fortran"
		q = args.search
		recon_search(g, q)
	else:
		recon_info(args.info)

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
if __name__ == "__main__":
	
	#search.grep_file_for('allred.c', '[0-9]')
	#search.grep_file_for('allred.c', 'MPI_Allreduce')

	#repo.hello()

	g = Github(os.environ.get('GITHUB_TOKEN'))

	recon_cli(g)






