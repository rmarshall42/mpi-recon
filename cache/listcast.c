#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <mpi.h>

int main( int argc, char** argv )
{
	int world_rank;
	int world_size;
	int N, H, k, tmp, min, max, sum;
	int arr[25];
	int secsum[20];
	int secmax[20];
	int secmin[20];
	int megaArr[20][25];

	MPI_Init(NULL, NULL);
	MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
	MPI_Comm_size(MPI_COMM_WORLD, &world_size);

	if ( world_rank == 0 )
	{
		sscanf(argv[1],"%i",&N);
		sscanf(argv[2],"%i",&H);
		MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD);
		MPI_Bcast(&H, 1, MPI_INT, 0, MPI_COMM_WORLD);
		for ( k = 0; k < N; k++ )
		{
			arr[k] = (rand() % H) + 1;
		}

		printf("Proc %d produced: ", world_rank);
		for ( k = 0; k < N; k++ )
			printf("%d ", arr[k]);
		printf("\n");
		usleep(500);

		for ( k = 0; k < N; k++ )
		{
			tmp = arr[k];
			MPI_Gather( &tmp, 1, MPI_INT, megaArr[k], 1, MPI_INT, 0, MPI_COMM_WORLD);
			usleep(500);
		}

		MPI_Bcast(megaArr, 25*20, MPI_INT, 0, MPI_COMM_WORLD);
		usleep(500);

		max = -1;
		min = H + 1;
		sum = 0;
		for ( k = 0; k < N; k++ )
		{
			if ( megaArr[k][world_rank] > max )
				max = megaArr[k][world_rank];
			if ( megaArr[k][world_rank] < min )
				min = megaArr[k][world_rank];
			sum += megaArr[k][world_rank];
		}

		MPI_Gather( &min, 1, MPI_INT, secmin, 1, MPI_INT, 0, MPI_COMM_WORLD);
		MPI_Gather( &max, 1, MPI_INT, secmax, 1, MPI_INT, 0, MPI_COMM_WORLD);
		MPI_Gather( &sum, 1, MPI_INT, secsum, 1, MPI_INT, 0, MPI_COMM_WORLD);
		usleep(500);

		for ( k = 0; k < world_size; k++ )
		{
			printf("Proc %d: min: %2d max: %2d sum: %3d\n",k,secmin[k],secmax[k],secsum[k]);
		}

	}
	else
	{
		MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD);
		MPI_Bcast(&H, 1, MPI_INT, 0, MPI_COMM_WORLD);
		usleep(500);
		srand(world_rank);
		for ( k = 0; k < N; k++ )
		{
			arr[k] = (rand() % H) + 1;
		}

		printf("Proc %d produced: ", world_rank);
		for ( k = 0; k < N; k++ )
			printf("%d ", arr[k]);
		printf("\n");

		for ( k = 0; k < N; k++ )
		{
			tmp = arr[k];
			MPI_Gather( &tmp, 1, MPI_INT, megaArr[k], 1, MPI_INT,0, MPI_COMM_WORLD);
		}
		usleep(500);

		MPI_Bcast(megaArr, 25*20, MPI_INT, 0, MPI_COMM_WORLD);
		usleep(500);
		max = -1;
		min = H + 1;
		sum = 0;
		for ( k = 0; k < N; k++ )
		{
			if ( megaArr[k][world_rank] > max )
				max = megaArr[k][world_rank];
			if ( megaArr[k][world_rank] < min )
				min = megaArr[k][world_rank];
			sum += megaArr[k][world_rank];
		}

		usleep(500);
		MPI_Gather( &min, 1, MPI_INT, secmin, 1, MPI_INT, 0, MPI_COMM_WORLD);
		MPI_Gather( &max, 1, MPI_INT, secmax, 1, MPI_INT, 0, MPI_COMM_WORLD);
		MPI_Gather( &sum, 1, MPI_INT, secsum, 1, MPI_INT, 0, MPI_COMM_WORLD);
	}

	MPI_Finalize();

	return 0;
}


