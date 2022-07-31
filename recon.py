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
import json
import sys
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
#----------------------------------------------------------------------------


def recon_probe(g, str_query):
	print ("** mpi-recon: live probe **")
	print ("query: " + str_query)
	#search.do_search(g, str_query)
	resultset = search.github_search(g, str_query, flood_ctrl=-1)
	get_interesting(resultset)

#----------------------------------------------------------------------------


def recon_search(g, str_query):
	print ("** mpi-recon: live search **", file = sys.stderr)
	print ("query: " + str_query, file = sys.stderr)
	#resultset = search.do_search(g, str_query,20)
	resultset = search.github_search(g, str_query)
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

def recon_repo_search(g, querykw=None, withtopic="mpi", jsonfile=None, dbfile=None):
	results = {
		'nfound' = 0,
		'ninserted' = 0;
	}
	repolist = []

	if jsonfile is None:
		flood_ctrl = 200
		repolist = search.github_repo_search(g, querykw, withtopic, flood_ctrl)

	else:
		try:
			jsonfile = open(jsonfile, 'r')
			repolist = json.loads(jsonfile.read())
		except OSError as exception:
			print (exception)

	results['nfound'] = 1

	for repo in repolist:
		#print (str(results['nfound']) + "\t" + str(repo['size']) +"\t"+ repo['clone_url'])
		results['nfound'] += 1

	print (f"results found from github: {results['nfound']}")
	#print (f"results inserted into db: {results['ninserted']}")


#----------------------------------------------------------------------------


def recon_cli(g):


	list_infile = None
	json_infile = None
	dbfile = None

	json_outfile = None
	list_outfile = None

	dbexts = ["db", "sqlite"]


	parser = argparse.ArgumentParser(prog="mpi-recon")
	parser.add_argument("--info", "-I", help="show some info")
	parser.add_argument("--probe", "-P", 
		default=None, # "MPI_Allgather", 
		help="probe for interesting repos, using the string in SEARCH")
	parser.add_argument("--search", "-s", 
		default=None, #"MPI_Allgather", 
		help="do a live search of github, using the string in SEARCH")
	parser.add_argument("--repos-by-topic", "-r", 
		default=None, 
		help="add a list of repositories into a dbms, example: data/topics-mpi.json")
	parser.add_argument("--infile", "-i", 
		default=None, 
		help="input file, text or JSON, depending on other options")
	parser.add_argument("--outfile", "-o", 
		default=None, 
		help="output file, text, JSON or db file, depending on other options")
#	parser.add_argument("--local", "-L", 
#		action='store_true', 
#		help="tell mpi-recon to do a local search")


	args = parser.parse_args()


	if args.infile:
		ext = args.infile.split(".")[-1].lower()

		if ext == "json":
			json_infile = args.infile
		else:
			list_infile = args.infile

	if args.outfile:
		ext = args.outfile.split(".")[-1].lower()
		if ext in dbexts:
			dbfile = args.outfile
		elif ext == "json":
			json_outfile = args.outfile
		else:
			list_outfile = args.outfile



	if args.probe:
		q = args.probe
		recon_probe(g, q)
	elif args.search:
		#q = args.search + " language:cpp language:c language:fortran"
		q = args.search
		recon_search(g, q)
	elif args.repos_by_topic:
		q = args.repos_by_topic
		print (f"json file: {json_infile}")
		recon_repo_search(g, q, jsonfile=json_infile)


		#if json_outfile is not None:



	else:
		recon_info(args.info)

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
if __name__ == "__main__":
	
	#search.grep_file_for('allred.c', '[0-9]')
	#search.grep_file_for('allred.c', 'MPI_Allreduce')
	# Alltoall, Alltoallv, Gather, Gatherv, Scatter, Scatterv, Reduce, Bcast, Allgather
	#repo.hello()

	g = Github(os.environ.get('GITHUB_TOKEN'))

	recon_cli(g)






