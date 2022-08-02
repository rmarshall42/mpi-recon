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
#import search
import os
import json
import sys
#import sys
#import getopt
import argparse
from github import Github

sys.path.append(f"{os.getcwd()}/common")


from recon_config import ReconConfig
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
#----------------------------------------------------------------------------


def recon_cli(ghtok):
	recon = ReconConfig(ghtok)
	parser = argparse.ArgumentParser(prog="mpi-recon")

	parser.add_argument("--info", "-I", 
		action = 'store_true',
		default = None,
		help="""show some info"""
	)

	parser.add_argument('keywords', 
		metavar='KEYWORDS', 
		type=str, 
		nargs='*',
		default = [],
		help='keywords to search or probe'
	)

	parser.add_argument("--probe", "-P", 
		action = 'store_true',
		default = None,
		help = """Probe github for interesting repos, 
					optionally using the keyword(s) in KEYWORDS, and
					optionally using topic(s) in TOPICS, 
					optionally using an input file (repolist.txt).
					Write results to corpus_basic.json"""
	)

	parser.add_argument("--search", "-S", 
		action = 'store_true',
		default = None,
		help = """Perform a live search of github, 
					optionally using the keyword(s) in KEYWORDS, and
					optionally using the topic(s) in TOPICS, 
					optionally using an input file 
					  (repolist.txt, corpus_basic.json or query results).
					Insert results into db (if --dbfile is given) or write 
					  results to corpus.json (if json outfile is given)."""
	)

	parser.add_argument("--usage", "-A", 
		action = 'store_true',
		default = None, 
		help = """Perform usage analysis of a list of repositories 
				   (corpus.json or query results)."""

	)
	#------------------------------------------------------------------------

	parser.add_argument("--topics", "-T", 
		type=str, 
		nargs='+',
		default = None,
		help = """Search by repository topics, using the string in topics"""
	)

	parser.add_argument("--dbfile", "-D", 
		default = None,
		help = """Path to a Sqlite-compatible database file (.db, .sqlite).  
				   If file is valid, recon will enable all db operations."""
	)

	parser.add_argument("--infile", "-i", 
		default = None,
		help = """Path to an input file giving a list of github repository clone urls or corpus_basic.json.  
				   If file is valid, recon will not perform a live search or probe."""
	)

	parser.add_argument("--clone-root", "-c", 
		default = None,
		help = """Path to a directory where cloned repositories reside, save newly cloned repositories here.
				   If directory is valid, recon will not perform a live probe."""
	)

	parser.add_argument("--force-local", "-L", 
		action = 'store_true',
		default = False,
		help = """Force a local search or probe."""
	)

	parser.add_argument("--outfile", "-o", 
		default = None,
		help = """Write results to this output file (json)."""
	)

	args = parser.parse_args()

	if args.keywords is not None:
		recon.keywords = args.keywords
	if args.topics is not None:
		recon.topics = args.topics

	recon.dbfile = args.dbfile
	recon.clone_root = args.clone_root
	recon.force_local = args.force_local


	if args.infile is not None:
		ext = args.infile.split(".")[-1].lower()
		recon.list_infile = args.infile if ext != "json" else None
		recon.json_infile = args.infile if ext == "json" else None

	if args.outfile is not None:
		ext = args.infile.split(".")[-1].lower()
		recon.list_outfile = args.outfile if ext != "json" else None
		recon.json_outfile = args.outfile if ext == "json" else None


		msg = None
	# if we have a search string
	if args.search:
		if len(recon.keywords) > 0 or len(recon.topics) > 0:
			recon.do_search = True


	if args.probe:
		assert recon.do_search is False, \
			"probe + search currently unsupported"

		if len(recon.keywords) > 0 or len(recon.topics) > 0 or args.infile:
			recon.do_probe = True


	if args.usage:
		assert recon.do_search is False and recon.do_probe is False, \
			"search/probe + usage currently unsupported"

		recon.do_usage = True


	if recon.dbfile or recon.list_infile or recon.json_infile:
		recon.force_local = True

	if recon.do_search is False and recon.do_probe is False and recon.do_usage is False:
		recon.do_info = True


	return recon

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
if __name__ == "__main__":

	r = recon_cli(os.environ.get('GITHUB_TOKEN'))









