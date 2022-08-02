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

from github import Github



class ReconConfig:

	do_search = False
	do_probe = False
	do_info = False
	do_usage = False
	force_local = False

	list_infile = None
	json_infile = None

	json_outfile = None
	list_outfile = None

	dbfile = None
	clone_root = None

	keywords = []
	topics = []

	dbexts = ["db", "sqlite"]

	github_obj = None
	#------------------------------------------------------------------------


	def __init__(self, ghtok=None):
		if ghtok:
			self.github_obj = Github(ghtok)
	#------------------------------------------------------------------------


	def to_string(self):
		return (f"""Recon Info_________
			keywords:      {self.keywords}
			topics:        {self.topics}
			list_infile:   {self.list_infile}
			json_infile:   {self.json_infile}
			dbfile:        {self.dbfile}
			list_outfile:  {self.list_outfile}
			json_outfile:  {self.json_infile}
			clone_root:    {self.clone_root}

			do_search:     {self.do_search}
			do_probe:      {self.do_probe}
			do_info:       {self.do_info}
			do_usage:      {self.do_usage}
			force_local:   {self.force_local}
			"""
		)
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------