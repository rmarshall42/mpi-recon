#!/usr/bin/env python


def insert_repos():
	q = ''' INSERT INTO Repos (
		repo_id,owner,repo_name,revision_id,clone_url,
		retrieval_date,omp_occs,acc_occs,cuda_occs,ocl_occs,
		c_lines,cpp_lines,c_cpp_h_lines,fortran_lines,total_lines)
		VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); ''' 

	return q

def insert_usage():
	q = ''' INSERT INTO Usage(call_id,repo_id,num_calls) VALUES(?,?,?) '''

	return q


def insert_owners():
	q = ''' INSERT INTO Owners(repo_id,user_id) VALUES(?,?) '''

	return q

def insert_mpicalls():
	q = ''' INSERT INTO MPICalls(call_id,call_name) VALUES(?,?) '''

	return q


def select_call_id():
	q = ''' SELECT * FROM MPICalls WHERE call_name LIKE ? '''

	return q



def get_repo_id():
	q = ''' SELECT repo_id FROM Repos WHERE repo_name LIKE ? '''

	return q
