#!/usr/bin/env python


import sys
import os
import time
#import urlparse
import urllib.parse
import sqlite3
import json

from sqlite3 import Error




def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def mk_clone_cmd(url):
	#return str("git clone " + url + ".git")
	return str("git clone " + url)


def get_repo_name(url):
	# path = urlparse.urlparse(url).path
	path = urllib.parse.urlparse(url).path

	return os.path.split(path)[-1]


def get_repo_list(lines):
	return [get_repo_name(line) for line in lines]


def get_cmds(lines):

	return map(mk_clone_cmd, lines)



############################################################################

if len(sys.argv) <= 1:
	print("usage: $ ./clonelist.py repolist [dbfile]")

else:
	dbfilename = 'corpus.db' if len(sys.argv) <= 2 else sys.argv[2]
	infile = sys.argv[1]

	lines = [line.rstrip() for line in open(infile)]
	repos = get_repo_list(lines)

	cmds = get_cmds(lines)


	print(cmds)
	for cmd in cmds:
		print (cmd)
		os.system(cmd)
#jdata = os.popen('../mpiusage.py ./sfxc')
#rec = json.loads(jdata.read())

#print(rec['CPP_LINES'])

