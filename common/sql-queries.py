#!/usr/bin/env python


def insert_repos():
	q = ''' INSERT INTO Repos (
		repo_id,owner,reponame,revision_id,clone_url,
		retrieval_date,omp_occs,acc_occs,cuda_occs,ocl_occs,
		c_lines,cpp_lines,c_cpp_h_lines,fortran_lines,total_lines)
		VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?); ''' 

	return q

def insert_usage():
	q = ''' INSERT INTO projects(name,begin_date,end_date) VALUES(?,?,?) '''

	return q

