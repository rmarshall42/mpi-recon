#!/usr/bin/env python

import sys
import os
import time
import urlparse
import sqlite3
import json

from sqlite3 import Error

# this is specific to github
def add_repo(conn, r):
	rec = r.get('data')
	tup = (
		None, 'shengg', r.get('ghrepo'), 0, 'https://github.com/shengg/stochastic_pt.git', None, rec.get('OPENMP'),
	rec.get('OPENACC'),rec.get('CUDA'),rec.get('OPENCL'),rec.get('C_LINES'),rec.get('CPP_LINES'),rec.get('C_CPP_H_LINES'),
	rec.get('FORTRAN_LINES'),rec.get('LINES_OF_CODE'))

	#print (tup)

	sql = ''' INSERT INTO Repos (
		repo_id,owner,reponame,revision_id,clone_url,
		retrieval_date,omp_occs,acc_occs,cuda_occs,ocl_occs,
		c_lines,cpp_lines,c_cpp_h_lines,fortran_lines,total_lines
	)
	VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); '''

	cur = conn.cursor()
	cur.execute(sql, tup)
	conn.commit()

	return cur.lastrowid

def add_usage(conn, urec):
	sql = ''' INSERT INTO projects(name,begin_date,end_date)
						VALUES(?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, urec)
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

	return repo_name


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



def main():
	jsonfile = open(sys.argv[2], 'r')
	usage = json.loads(jsonfile.read())

	with sqlite3.connect(sys.argv[1]) as conn:
		for r in usage:
			repo_id = 1#add_repo(conn, r)
			print('inserted repo_id: ' + str(repo_id) + ', name:' + r.get('ghrepo'))
		


################################## entry ##################################

if __name__ == '__main__':
	if len(sys.argv) <= 2:
		print("usage: $ ./additems.py dbfile jsonfile")

	main()


