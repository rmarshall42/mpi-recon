/*
 * simple lennard-jones potential MD code with velocity verlet.
 * units: Length=Angstrom, Mass=amu; Energy=kcal
 *
 * baseline c version.
 */

#include <assert.h>
#include <ctype.h>
#include <math.h>
#ifdef _MPI
#include <mpi.h>
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "ljmd.h"

/* main */
int main(int argc, char **argv) {
  int nprint, i;
  char restfile[BLEN], trajfile[BLEN], ergfile[BLEN], line[BLEN];
  mdsys_t sys;

#ifdef _MPI
  sys.mcom = MPI_COMM_WORLD;

  MPI_Init(&argc, &argv);
  int mid, msize;
  MPI_Comm_rank(sys.mcom, &mid);
  MPI_Comm_size(sys.mcom, &msize);
#else
  const int mid = 0;
#endif /* _MPI */

  FILE *fp, *traj, *erg;

  traj = NULL; erg = NULL;

  /* read input file */
#ifdef _MPI
  sys.mid = mid;
  sys.msize = msize;
  if (!mid) {
#endif /* _MPI */
    if (get_a_line(stdin, line)) return 1;
    sys.natoms = atoi(line);
    if (get_a_line(stdin, line)) return 1;
    sys.mass = atof(line);
    if (get_a_line(stdin, line)) return 1;
#ifndef WITH_MORSE
    sys.epsilon = atof(line);
#else
    sys.De = atof(line); 
#endif
    if (get_a_line(stdin, line)) return 1;
#ifndef WITH_MORSE
    sys.sigma = atof(line);
#else
    sys.re = pow(2.0, 1/6) * atof(line);
    sys.a  = sqrt(30) / sys.re;
#endif
    if (get_a_line(stdin, line)) return 1;
    sys.rcut = atof(line);
    if (get_a_line(stdin, line)) return 1;
    sys.box = atof(line);
    if (get_a_line(stdin, restfile)) return 1;
    if (get_a_line(stdin, trajfile)) return 1;
    if (get_a_line(stdin, ergfile)) return 1;
    if (get_a_line(stdin, line)) return 1;
    sys.nsteps = atoi(line);
    if (get_a_line(stdin, line)) return 1;
    sys.dt = atof(line);
    if (get_a_line(stdin, line)) return 1;
    nprint = atoi(line);
#ifdef _MPI
  }
  if (msize != 1) {
    MPI_Bcast(&(sys.natoms), 1, MPI_INT, 0, sys.mcom);
    MPI_Bcast(&(sys.mass), 1, MPI_DOUBLE, 0, sys.mcom);
#ifndef WITH_MORSE
    MPI_Bcast(&(sys.epsilon), 1, MPI_DOUBLE, 0, sys.mcom);
    MPI_Bcast(&(sys.sigma), 1, MPI_DOUBLE, 0, sys.mcom);
#else
    MPI_Bcast(&(sys.De), 1, MPI_DOUBLE, 0, sys.mcom);
    MPI_Bcast(&(sys.re), 1, MPI_DOUBLE, 0, sys.mcom);
    MPI_Bcast(&(sys.a), 1, MPI_DOUBLE, 0, sys.mcom);
#endif
    MPI_Bcast(&(sys.rcut), 1, MPI_DOUBLE, 0, sys.mcom);
    MPI_Bcast(&(sys.box), 1, MPI_DOUBLE, 0, sys.mcom);
    MPI_Bcast(restfile, BLEN, MPI_CHAR, 0, sys.mcom);
    MPI_Bcast(trajfile, BLEN, MPI_CHAR, 0, sys.mcom);
    MPI_Bcast(ergfile, BLEN, MPI_CHAR, 0, sys.mcom);
    MPI_Bcast(&(sys.nsteps), 1, MPI_INT, 0, sys.mcom);
    MPI_Bcast(&(sys.dt), 1, MPI_DOUBLE, 0, sys.mcom);
    MPI_Bcast(&nprint, 1, MPI_INT, 0, sys.mcom);
  }
#endif /* _MPI */

  /* allocate memory */
  sys.rx = (double *)malloc(sys.natoms * sizeof(double));
  sys.ry = (double *)malloc(sys.natoms * sizeof(double));
  sys.rz = (double *)malloc(sys.natoms * sizeof(double));
  sys.vx = (double *)malloc(sys.natoms * sizeof(double));
  sys.vy = (double *)malloc(sys.natoms * sizeof(double));
  sys.vz = (double *)malloc(sys.natoms * sizeof(double));
  sys.fx = (double *)malloc(sys.natoms * sizeof(double));
  sys.fy = (double *)malloc(sys.natoms * sizeof(double));
  sys.fz = (double *)malloc(sys.natoms * sizeof(double));

  /* read restart */
  int input_scan;
  fp = fopen(restfile, "r");
  if (fp) {
    for (i = 0; i < sys.natoms; ++i) {
      input_scan = fscanf(fp, "%lf%lf%lf", sys.rx + i, sys.ry + i, sys.rz + i);
      assert(input_scan != 0);
    }
    for (i = 0; i < sys.natoms; ++i) {
      input_scan = fscanf(fp, "%lf%lf%lf", sys.vx + i, sys.vy + i, sys.vz + i);
      assert(input_scan != 0);
    }
    fclose(fp);
    azzero(sys.fx, sys.natoms);
    azzero(sys.fy, sys.natoms);
    azzero(sys.fz, sys.natoms);
  } else {
    perror("cannot read restart file");
    return 3;
  }

  /* initialize forces and energies.*/
  sys.nfi = 0;
  force(&sys);

  if (!mid) {
    ekin(&sys);
    erg = fopen(ergfile, "w");
    traj = fopen(trajfile, "w");

    printf("Starting simulation with %d atoms for %d steps.\n", sys.natoms,
           sys.nsteps);
    output(&sys, erg, traj);
  }
  /**************************************************/
  /* main MD loop */
  for (sys.nfi = 1; sys.nfi <= sys.nsteps; ++sys.nfi) {
    /* write output, if requested */
    if (!mid) {
      /* write output, if requested */
      if ((sys.nfi % nprint) == 0) output(&sys, erg, traj);
      /* propagate system and recompute energies */
      initial_propagation(&sys);
    }

    /* compute forces and potential energy */
    force(&sys);

    if (!mid) {
      final_propagation(&sys);
      ekin(&sys);
    }
  }
  /**************************************************/

  /* clean up: close files, free memory */
  if (!mid) {
    printf("Simulation Done.\n");
    fclose(erg);
    fclose(traj);
  }

  free(sys.rx);
  free(sys.ry);
  free(sys.rz);
  free(sys.vx);
  free(sys.vy);
  free(sys.vz);
  free(sys.fx);
  free(sys.fy);
  free(sys.fz);
#ifdef _MPI
  MPI_Finalize();
#endif /* _MPI */
  return 0;
}
