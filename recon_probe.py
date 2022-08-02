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

import os
import re
import time
import json
from datetime import datetime

from github import GithubException
#import sys
#import getopt
#import argparse
#----------------------------------------------------------------------------

def github_repo_probe(g, querykws=[], withtopic=[], flood_ctrl=200):
	repolist = []
	kw       = " ".join(querykws)
	query    = f'"{kw}"'
	i        = 0

	try:
		for repo in g.search_repositories(\
			query, topic=withtopic, sort="stars", order="desc"):
			i += 1
			#print(repo)
			repolist.append(repo)
			if i >= flood_ctrl:
				time.sleep(15)
				i = 0
	except GithubException:
		print (f"got {str(len(repolist))} repos before rate limit exeeded")

	print (f"got {str(len(repolist))} repos before rate limit exeeded")

	return repolist
#----------------------------------------------------------------------------


def do_probe(g, querykws=[], withtopic=["mpi"], jsonfile=None, dbfile=None):

	repolist = []

	if jsonfile is None:
		flood_ctrl = 200
		repolist = github_repo_probe(g, querykw, withtopic, flood_ctrl)

	else:
		try:
			jsonfile = open(jsonfile, 'r')
			repolist = json.loads(jsonfile.read())
		except OSError as exception:
			print (exception)

	return repolist

#----------------------------------------------------------------------------








