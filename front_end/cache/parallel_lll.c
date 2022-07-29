#include "parallel_lll.h"

void parallel_LLL(double *B, double *D, double *U, double *M, double w, int m, int n, int id, int np) {
    return;
#ifdef MPI_INCLUDE
    int k = 1;
    int gamma;
    int f = 0;
    MPI_Datatype row_t;
    MPI_Type_vector(n, 1, n, MPI_DOUBLE, &row_t);
    MPI_Type_commit(&row_t);

    while (f == 0) {
        int how_many = (2 + (id + 1) * (n / np) - 1) - (2 + id * (n / np) - 1);
        printf("how_many=%i\n", how_many);
        int *works = (int *)calloc(how_many, sizeof(int));
        int counter = 0;
        f = 1;
        // Even math k (odd in computer terms). Math says start at 2, which is 1 in computer terms
        // Begin Parallel
        for (int k = 2 + id * (n / np) - 1; k < 2  + (id + 1) * (n / np) - 1 && k < n; k += 2) {
            gamma = closest_integer(U[k*n + (k - 1)]);
            int do_work = 0;
            if (D[k] < (w - (U[k*n + (k - 1)] - gamma)*(U[k*n + (k - 1)] - gamma))*D[k - 1]) {
                f = 0;
                works[counter] = 1;
                do_work = 1;
                //reduceSwapRestore(k, gamma, B, D, U, M, m, n);
            }
            counter++;
            //////////////////////////////////////////////////////////////////////
            double u, d_hat_m, epsilon;

            if (do_work == 1) {
                u = U[k*n + (k - 1)];
                d_hat_m = D[k] + (u - gamma)*(u - gamma)*D[k - 1];
                D[k] = (D[k - 1] * D[k]) / d_hat_m;

                epsilon = ((u - gamma)*D[k - 1]) / d_hat_m;
                D[k - 1] = d_hat_m;

                // Do U=X^-1 * U
                u = U[k*n + (k - 1)];
                double u1, u2;
                for (int z = k + 1; z < n; ++z) {
                    u1 = U[z*n + (k - 1)];
                    u2 = U[z*n + k];
                    U[z*n + (k - 1)] = u1*epsilon + (1 - epsilon*u + gamma*epsilon)*u2;
                    U[z*n + k] = u1 + (gamma - u)*u2;
                }
                U[k*n + (k - 1)] = epsilon;
            }

            ////////////////////////////////////////////////////////////////////////
        }
        printf("[%i] Before first allgather\n", id);
        double *Utemp = (double *)calloc(n*n, sizeof(double));
        if (Utemp != NULL) printf("Not null\n");
            MPI_Allgather(&(U[id * (n / np)*n]), how_many, row_t, Utemp, how_many, row_t, MPI_COMM_WORLD);
            memcpy(U, Utemp, n*n*sizeof(double));
            free(Utemp);
        printf("[%i] After first allgather\n", id);
        ////////////////////////////////////////////////////////////////////////////
        counter = 0;
        for (int k = 2 + id * (n / np) - 1; k < 2 + (id + 1) * (n / np) - 1 && k < n; k += 2) {
            gamma = closest_integer(U[k*n + (k - 1)]);
            int do_work = 0;
            if (works[counter]==1) {
                f = 0;
                do_work = 1;
                //reduceSwapRestore(k, gamma, B, D, U, M, m, n);
            }
            counter++;
            //////////////////////////////////////////////////////////////////////
            double u, d_hat_m, epsilon;

            if (do_work == 1) {
                double tempB;
                for (int z = 0; z < m; ++z) {
                    tempB = B[(k - 1)*m + z];
                    B[(k - 1)*m + z] = B[k*m + z] - gamma*tempB;
                    B[k*m + z] = tempB;
                }

                //Update k-1 and k columns of M
                double tempM;
                for (int z = 0; z < n; ++z) {
                    tempM = M[(k - 1)*n + z];
                    M[(k - 1)*n + z] = M[k*m + z] - gamma*tempM;
                    M[k*m + z] = tempM;
                }

                // Update k-1 and k columsn of U
                double tempU;
                for (int z = 0; z <= k - 2; ++z) {
                    tempU = U[(k - 1)*n + z];
                    U[(k - 1)*n + z] = U[k*n + z] - gamma*tempU;
                    U[k*n + z] = tempU;
                }
                
            }
        }
            ////////////////////////////////////////////////////////////////////////////////
        printf("[%i] Before last chunk allgather\n", id);
        if (id == 0) {
            MPI_Allgather(MPI_IN_PLACE, how_many*n, MPI_DOUBLE, U, how_many*n, MPI_DOUBLE, MPI_COMM_WORLD);
            MPI_Allgather(MPI_IN_PLACE, how_many*n, MPI_DOUBLE, M, how_many*n, MPI_DOUBLE, MPI_COMM_WORLD);
            MPI_Allgather(MPI_IN_PLACE, how_many*m, MPI_DOUBLE, B, how_many*m, MPI_DOUBLE, MPI_COMM_WORLD);
            MPI_Allgather(MPI_IN_PLACE, how_many * 1, MPI_DOUBLE, D, how_many * 1, MPI_DOUBLE, MPI_COMM_WORLD);
        }
        else {
            MPI_Allgather(&(U[id * (n / np)*n]), how_many*n, MPI_DOUBLE, U, how_many*n, MPI_DOUBLE, MPI_COMM_WORLD);
            MPI_Allgather(&(M[id * (n / np)*n]), how_many*n, MPI_DOUBLE, M, how_many*n, MPI_DOUBLE, MPI_COMM_WORLD);
            MPI_Allgather(&(B[id * (n / np)*m]), how_many*m, MPI_DOUBLE, B, how_many*m, MPI_DOUBLE, MPI_COMM_WORLD);
            MPI_Allgather(&(D[id*(n / np) * 1]), how_many * 1, MPI_DOUBLE, D, how_many * 1, MPI_DOUBLE, MPI_COMM_WORLD);
        }
        printf("[%i] After last chunk allgather\n", id);
        // End Parallel
#ifdef MPI_INCLUDE
        MPI_Barrier(MPI_COMM_WORLD);
#endif
        // Odd math k (even in computer terms). Math says start at 3, which is 2 in computer terms
        // Begin Parallel
        for (int k = 3 + id * (n / np) - 1; k < 3 + (id + 1) * (n / np) - 1 && k < n; k += 2) {
            gamma = closest_integer(U[k*n + (k - 1)]);
            if (D[k] < (w -
                (U[k*n + (k - 1)] - gamma)
                *(U[k*n + (k - 1)] - gamma)
                )*D[k - 1]) {
                f = 0;
                reduceSwapRestore(k, gamma, B, D, U, M, m, n);
            }
        }
#ifdef MPI_INCLUDE
        MPI_Barrier(MPI_COMM_WORLD);
#endif
    }
    int l_n = n / np;
    int offset = id*l_n;
    // End Parallel
    // NEED TO GET MATRICES ON ALL PARTS NOW
    int i, j, start;
    for (k = 2 * l_n - 3; k >= 1; k--) {
        if (k <= l_n - 1) {
            start = 1;
        }
        else {
            start = k - l_n + 2;
        }
        for (i = start+offset; i < (k + 3) / 2; i++) { // paper code has i+=NUM_THREADS. why?
                                                       // I think because their offset==id. 
                                                       // i.e. they have each thread doing 
                                                       // all columns congruent to 
                                                       // id (mod NUM_THREADS)
            j = k + 2 - i;
#ifdef DEBUG_LLL
            printf("U[%i][%i]=%lf\n", i, j, U[(j - 0)*n + (i - 0)]);
#endif
            if (fabs(U[(j-1)*n+(i-1)]) > 0.5+NUM_ERR) {
                reduce(U, B, M, i-1, j-1, m, n);
            }
        }
    }
#endif
}
