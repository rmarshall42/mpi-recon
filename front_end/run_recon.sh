#!/bin/bash -l

#$ -l h_rt=12:00:00   # Specify the hard time limit for the job
#$ -N mpi-recon           # Give job a name
#$ -j y               # Merge the error and output streams into a single file

module load python3/3.8.3
export GITHUB_TOKEN=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

python3 recon.py --search "MPI_Allreduce" > search_Allreduce.txt 
python3 recon.py --search "MPI_Alltoall" > search_Alltoall.txt 
python3 recon.py --search "MPI_Gather" > search_Gather.txt 
python3 recon.py --search "MPI_Gatherv" > search_Gatherv.txt 
python3 recon.py --search "MPI_Scatter" > search_Scatter.txt 
python3 recon.py --search "MPI_Scatterv" > search_Scatterv.txt 
python3 recon.py --search "MPI_Reduce" > search_Reduce.txt 
python3 recon.py --search "MPI_Bcast" > search_Bcast.txt 
python3 recon.py --search "MPI_Allgather" > search_Allgather.txt 


