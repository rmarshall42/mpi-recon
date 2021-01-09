#!/usr/bin/env python


import sys
import os
import time
import urlparse
import sqlite3
import json

from sqlite3 import Error




def create_connection(db_file):
    """ create a database connection to a SQLite database """
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
	return str("git clone " + url + ".git")



def get_repo_name(url):
	path = urlparse.urlparse(url).path

	return os.path.split(path)[-1]


def get_repo_list(lines):
	return [get_repo_name(line) for line in lines]



############################################################################

if len(sys.argv) <= 1:
	print("usage: $ ./analyze.py [repolist] DEFAULT:$PWD")

else:
	dbfilename = 'corpus.db' if len(sys.argv) <= 2 else sys.argv[2]
	corpusdir = sys.argv[1]

	lines = [line.rstrip() for line in open(corpusdir)]
	repos = get_repo_list(lines)


