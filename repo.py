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

# stuff we can do with github repositories

from github import Github
import os
import re
import csv
import datetime

SHA1_LEN = 40
MAX_NCOMMITS = 100000
MAX_NCOMMITSB = 101 # for testing 
EARLIEST = datetime.datetime(2019,1,1) # large repos could have 1000s of commits

TYPES = ["c","cpp","cc","cxx","h","hpp","cu","f","f90","f95","f03"]

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------


def hello():
		print("hello")

def get_recon_file_list(repo, sha, ghel_list):	
	tr = repo.get_git_tree(sha)

	for leaf in tr.tree:
		if leaf.type == "tree":
			return get_recon_file_list(repo, leaf.sha, ghel_list)
		else:
			ext = leaf.path.split(".")[-1]

			if ext.lower() in TYPES:
				ghel_list.append(leaf)
				# if leaf.sha == "0ab9048b4ba9bb3d83514a1a88477e2696ec5757": # MatrixInitOp.hpp
				# 	contents = repo.get_contents(leaf.path)
				# 	print (contents)
	return ghel_list
# --------------------------------------------------------------------------


def get_recon_contents(repo):
	contents = repo.get_contents("")
	while contents:
		file_content = contents.pop(0)
		if file_content.type == "dir":
			contents.extend(repo.get_contents(file_content.path))
		else:
			print(file_content.path)



# --------------------------------------------------------------------------



def get_recon_repo(g, repo_full_name):
	return g.get_repo(repo_full_name)
# --------------------------------------------------------------------------


def get_recon_commits(repo, e=EARLIEST):
	commits = repo.get_commits(since=e)
	commits_extracted = []
	i = 0
	for cmm in commits:
		if cmm.stats.total <= MAX_NCOMMITS:
			xcmm = {
				'author_date': cmm.commit.author.date,
				'nfiles': len(cmm.files),
				'sha': cmm.sha,
				'ninsertions': cmm.stats.additions,
				'ndeletions': cmm.stats.deletions,
				'ntotal_changes': cmm.stats.total
			}

			commits_extracted.append(xcmm)
			i += 1

		if i >= MAX_NCOMMITSB:
			break

	return commits_extracted
# --------------------------------------------------------------------------


def get_recon_stats(repo):
	sizes = {
	        'id': repo.id,
	      'name': repo.name,
	 'full_name': repo.full_name,
	  'language': repo.language,
	    'nstars': repo.stargazers_count,
	    'nforks': repo.forks_count,
	 'nbranches': repo.get_branches().totalCount,
	     'ntags': repo.get_tags().totalCount,
	 'nreleases': repo.get_releases().totalCount,
	  'ncommits': repo.get_commits().totalCount
# these methods require push access
#	    'nviews': repo.get_views_traffic(),
#	 'nviews_wk': repo.get_views_traffic(per="week"),
#	   'nclones': repo.get_clones_traffic(),
#	'nclones_wk': repo.get_clones_traffic(per="week"),

	}
	return sizes
# --------------------------------------------------------------------------


def get_sha_from_branchname(repo, brnm):
	branch = repo.get_branch(brnm)
	return str(branch.commit.sha)
# --------------------------------------------------------------------------
# simple test for valid sha1 string
#   from a tag, we can get the correct hash, but 
#   release.target_commitish may contain a branch name or sha1 hash.
#
#
def valid_sha(strg, search=re.compile(r'[^a-f0-9]').search):
	return bool(len(strg) == SHA1_LEN) and (not bool(search(strg)))
# --------------------------------------------------------------------------


def get_recon_tags(repo):
	tags_extracted = []

	for tag in repo.get_tags():
		cmm = repo.get_commit(tag.commit.sha)
		stats = tag.commit.stats
		xcmm = {
			'name': tag.name,
			'author_date': cmm.commit.author.date,
			'nfiles': len(cmm.files),
			'sha': cmm.sha,
			'ninsertions': cmm.stats.additions,
			'ndeletions': cmm.stats.deletions,
			'ntotal_changes': cmm.stats.total
		}

		tags_extracted.append(xcmm)
	return tags_extracted
# --------------------------------------------------------------------------


def write_tags(tags_extracted, fileoutname="tags.csv"):
	csv_columns = [			
		'name',
		'author_date',
		'nfiles',
		'sha',
		'ninsertions',
		'ndeletions',
		'ntotal_changes'  ]


	try:
		with open(fileoutname, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			for data in tags_extracted:
				writer.writerow(data)
	except IOError:
		print("I/O error")
# --------------------------------------------------------------------------


def write_commits(commits_extracted, fileoutname="commits.csv"):
	csv_columns = [			
		'author_date',
		'nfiles',
		'sha',
		'ninsertions',
		'ndeletions',
		'ntotal_changes'  ]


	try:
		with open(fileoutname, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			for data in commits_extracted:
				writer.writerow(data)
	except IOError:
		print("I/O error")
# --------------------------------------------------------------------------


def write_repos(repos_extracted, fileoutname="commits.csv"):
	csv_columns = [			
		'author_date',
		'nfiles',
		'sha',
		'ninsertions',
		'ndeletions',
		'ntotal_changes'  ]


	try:
		with open(fileoutname, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			for data in commits_extracted:
				writer.writerow(data)
	except IOError:
		print("I/O error")
# --------------------------------------------------------------------------
def handle_commits(repo):

	commits = get_recon_commits(repo)
	write_commits(commits, "commits.csv")
# --------------------------------------------------------------------------


def handle_tags(repo):
	tags = get_recon_tags(repo)
	write_tags(tags, "tags.csv")
# --------------------------------------------------------------------------



# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

if __name__ == "__main__":
	# using an access token
	g = Github(os.environ.get('GITHUB_TOKEN'))

	#repo = g.get_repo("trilinos/Trilinos")
	repo = g.get_repo("Mantevo/miniFE")

	#handle_tags(repo)
	#handle_commits(repo)
	#get_recon_contents(repo)
	#stats = get_recon_stats(repo)
	flatfiles = []
	sha = get_sha_from_branchname(repo, "master")
	flatfiles = get_recon_file_list(repo, sha, flatfiles)

	for f in flatfiles:
		print(f.sha +" | "+ f.path+ " | " +f.url +" | "+ str(f.size))


	# for release in repo.get_releases():
	# 	tc = release.target_commitish
	# 	sha = tc if valid_sha(tc) else get_sha_from_branchname(repo, tc)
		
	# 	print (str(release.created_at) +","+ release.title+","+ sha)

	#get_tags(g)

