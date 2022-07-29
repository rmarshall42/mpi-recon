#!/usr/bin/env python3

import os
import time    
import json

outputs_location = r'/home/rmarshall/git/mpi-recon/data/usage-outputs'
owner_file = r'/home/rmarshall/git/mpi-recon/data/owner_reponame.txt'

reponames = []

owner_reponame = {}



def get_owner_from_reponame(reponame):
	with open(owner_file) as file_in:
		for line in file_in:
			rname = line[line.find('/')+1:].strip()
			if rname == reponame:
				#print (rname +' : '+ reponame)
				return line[0:line.find('/')]

	return ''

#get the reponames and look up the owners
for entry in os.scandir(outputs_location):
	if (entry.path.endswith(".json")) and entry.is_file():
		reponame = entry.name.replace('.json', '');
		reponames.append(reponame)
		owner = get_owner_from_reponame(reponame)

		# owner may own multiple repos
		if len(owner) > 0:
			if owner in owner_reponame:
				owner_reponame[owner].append(reponame)
			else:
				owner_reponame[owner] = [reponame]


			with open(entry.path) as f:
				data = json.load(f)

				revision_id = ''
				clone_url = 'https://github.com/' + owner + '/' + reponame + '.git'
				retrieval_date = time.strftime('%Y-%m-%d %H:%M:%S')
				omp_occs = data['OPENMP']
				cuda_occs = data['CUDA']
				acc_occs = data['OPENACC']
				ocl_occs = data['OPENCL']
				c_lines = data['C_LINES']
				cpp_lines = data['CPP_LINES']
				c_cpp_h_lines = data['C_CPP_H_LINES']
				fortran_lines = data['FORTRAN_LINES']
				total_lines = data['LINES_OF_CODE']

				# first field is sql autonumber type
				# print ('None,' + 
			  #   owner + ',' + reponame + ',' + revision_id + ',' + clone_url +','+ 
				# 	retrieval_date + ',' + str(ocl_occs) +','+ str(acc_occs) +
				# 	',' + str(cuda_occs) + ',' + str(omp_occs) + ',' + str(c_lines) + ',' + 
				# 	str(cpp_lines) + ',' + str(c_cpp_h_lines) + ',' + str(fortran_lines) + ',' + 
				# 	str(total_lines) )

				exclude = ['OPENMP','CUDA','OPENACC','OPENCL','C_LINES','CPP_LINES','C_CPP_H_LINES','FORTRAN_LINES','LINES_OF_CODE']

				# now get the mpi calls
				#for callname in data.keys():
				#	if callname not in exclude:
				#		print (owner + ',' + reponame + ',' + callname + ',' + str(data[callname]))




#print (owner_reponame)