#!/usr/bin/env python

import sys
import os
import time
import urlparse
import sqlite3
import json
import importlib

from sqlite3 import Error

from common import sql_queries


SHARED = 'common'

# these are specific to github


def call_exists(conn, call):
	cur = conn.cursor()
	cur.execute(sql_queries.select_call_id(), (call,))
	rows = cur.fetchall()

	return rows



def add_data(conn, r):
	rec = r.get('data')

	for call in rec:
		tup = (None, call)

		cur = conn.cursor()
		cur.execute(sql_queries.insert_mpicalls(), tup)
		conn.commit()

	return cur.lastrowid

def add_repo(conn, r):
	last_id = -1
	rec = r.get('ghcounts')

	tup = (
		None, r.get('ghuser'), 
		r.get('ghrepo'), 0, None, None, 
		rec.get('OPENMP'),
	rec.get('OPENACC'),rec.get('CUDA'),rec.get('OPENCL'),rec.get('C_LINES'),rec.get('CPP_LINES'),rec.get('C_CPP_H_LINES'),
	rec.get('FORTRAN_LINES'),rec.get('LINES_OF_CODE'))

	cur = conn.cursor()
	cur.execute(sql_queries.insert_repos(), tup)
	conn.commit()

	last_id = cur.lastrowid

	return last_id

def add_owner(conn, r):
	tup = (r.get('ghrepo'), get_owner_name(r.get('data').get(clone_url)))

	cur = conn.cursor()
	cur.execute(sql_queries.insert_owners(), urec)
	conn.commit()

	return cur.lastrowid

def add_usage(conn, urec):
	cur = conn.cursor()
	cur.execute(sql_queries.insert_usage(), urec)
	conn.commit()

	return cur.lastrowid


def mk_clone_cmd(url, source='github'):
	cmd = ''
	if source == 'github':
		cmd = str("git clone " + url + ".git")

	return cmd


def get_repo_clone_url(repouser, reponame, source='github'):
	url = 'https://github.com/'
	if source == 'github':
		url += str(repouser) + '/' + str(reponame) + '.git'
	
	return url


def get_repo_name(url, source='github'):
	path = urlparse.urlparse(url).path
	repo_name = ''
	if source == 'github':
		repo_name = os.path.split(path)[-1]

	return repo_name.split('.')[0]


def get_owner_name(url, source='github'):
	p = urlparse.urlparse(url).path
	owner_name = ''
	if source == 'github':
		owner_name = str(os.path.split(p)[-2])[1:]

	return owner_name


def get_repo_list(lines, source='github'):
	repo_list = []
	if source == 'github':
		repo_list = [get_repo_name(line) for line in lines]

	return repo_list


def util_set_user(usage):
	with open('./corpus/repolist.txt') as f:
		content = f.readlines()
	# strip outer whitespace
	content = [x.strip() for x in content] 

	for line in content:
		# super simple test for url
		if not line.find('http://'):
			#print(get_owner_name(line) +' : '+ get_repo_name(line))
			for r in usage:
				#print (r.get('ghrepo') + '==' + get_repo_name(line))
				if (r.get('ghrepo') == get_repo_name(line)):
					r['ghuser'] = get_owner_name(line)

	print(json.dumps(usage, sort_keys=True, indent=2))

	return 


def main():
	jsonfile = open(sys.argv[2], 'r')
	usage = json.loads(jsonfile.read())

	util_set_user(usage)

	#print(json.dumps(usage, sort_keys=True, indent=2))

	importlib.import_module('sql_queries')

	with sqlite3.connect(sys.argv[1]) as conn:
		for r in usage:
			repo_id = add_repo(conn, r)
			searchtext = 'MPI_ALLGATHER'
			exists = call_exists(conn, searchtext)
			print ('|#')
			print(exists)
			print ('#|')
		


################################ entry point ################################

if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print("usage: $ ./additems.py dbfile jsonfile")


	# may need to search for this file if we move things around
	sys.path.append(
	  os.path.expanduser(
	    os.path.split(os.path.realpath('repolist'))[0] + '/' + SHARED))
		
	#print (sql_queries.insert_repos())

	main()


