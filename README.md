# mpi-recon
Analyze MPI applications in the wild

Workflow. It goes like this :

[gh_search_cli -> repolist] --> [mpiusage.py -> usage.json] --> additems.py -> mpiu.db

folders:
3rd-party is empty now, I am looking into a way to link to MPI-Usage and the cli-based github API search
corpus folder has a list of the repo URLs
data holds mpiu.db and usage.json
docs for documentation and slides, etc.
additems.py populates the db
clonelist.py issues the git clone commands from a list of repos

