// Copyright 2020 Sidorova Alexandra

#include <gtest-mpi-listener.hpp>
#include <gtest/gtest.h>
#include <random>
#include <ctime>
#include "./allreduce.h"

#define EPSILON 0.0001

TEST(MPI_AllReduce, IncorrectBuffersPointers) {
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    int* sendbuf = nullptr;
    int* recvbuf = nullptr;
    int count = 1;

    ASSERT_EQ(Allreduce(sendbuf, recvbuf, count, MPI_INT, MPI_SUM, MPI_COMM_WORLD), MPI_ERR_BUFFER);
}

TEST(MPI_AllReduce, IncorrectCount) {
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    int sendbuf = 0;
    int recvbuf = 0;
    int count = -1;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_INT, MPI_SUM, MPI_COMM_WORLD), MPI_ERR_COUNT);
}

TEST(MPI_AllReduce, IncorrectDataType) {
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    int sendbuf = 0;
    int recvbuf = 0;
    int count = 1;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_UNSIGNED_LONG, MPI_SUM, MPI_COMM_WORLD), MPI_ERR_TYPE);
}

TEST(MPI_AllReduce, IncorrectOp) {
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    int sendbuf = 0;
    int recvbuf = 0;
    int count = 1;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_INT, MPI_BXOR, MPI_COMM_WORLD), MPI_ERR_OP);
}

TEST(MPI_AllReduce, IncorrectCommunicator) {
    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    int sendbuf = 0;
    int recvbuf = 0;
    int count = 1;
    MPI_Comm comm = MPI_COMM_NULL;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_INT, MPI_SUM, comm), MPI_ERR_COMM);
}

TEST(MPI_AllReduce, IntMax) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 1;
    int sendbuf = rank * rank;
    int recvbuf = 0;
    const int max = (size - 1) * (size - 1);

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_INT, MPI_MAX, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_EQ(recvbuf, max);
}

TEST(MPI_AllReduce, IntMin) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 1;
    int sendbuf = rank * rank;
    int recvbuf = 0;
    const int min = 0;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_INT, MPI_MIN, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_EQ(recvbuf, min);
}

TEST(MPI_AllReduce, IntSum) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 1;
    int sendbuf  = rank;
    int recvbuf = 0;
    const int sum = size * (size - 1) / 2;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_INT, MPI_SUM, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_EQ(recvbuf, sum);
}

TEST(MPI_AllReduce, IntProd) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 1;
    int sendbuf = rank;
    int recvbuf = 0;
    int prod = 1;
    for (int i = 0; i < size; ++i)
        prod *= i;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_INT, MPI_PROD, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_EQ(recvbuf, prod);
}

TEST(MPI_AllReduce, FloatMax) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 1;
    float sendbuf = rank * rank * 0.1f;
    float recvbuf = 0.0f;
    const float max = (size - 1) * (size - 1) * 0.1f;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_FLOAT, MPI_MAX, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_NEAR(recvbuf, max, EPSILON);
}

TEST(MPI_AllReduce, FloatMin) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 1;
    float sendbuf = rank * rank * 0.1f;
    float recvbuf = 0.0f;
    const float min = 0.0f;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_FLOAT, MPI_MIN, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_NEAR(recvbuf, min, EPSILON);
}

TEST(MPI_AllReduce, FloatSum) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 1;
    float sendbuf = rank * 0.1f;
    float recvbuf = 0.0f;
    float sum = size * (size - 1) / 20.0f;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_FLOAT, MPI_SUM, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_NEAR(recvbuf, sum, EPSILON);
}

TEST(MPI_AllReduce, FloatProd) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 1;
    float sendbuf = rank * 0.1f;
    float recvbuf = 0.0f;
    float prod = 1.0f;
    for (int i = 0; i < size; ++i)
        prod *= i * 0.1f;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_FLOAT, MPI_PROD, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_NEAR(recvbuf, prod, EPSILON);
}


TEST(MPI_AllReduce, DoubleMax) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 1;
    double sendbuf = rank * rank * 0.1;
    double recvbuf = 0.0;
    const double max = (size - 1) * (size - 1) * 0.1;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_DOUBLE, MPI_MAX, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_NEAR(recvbuf, max, EPSILON);
}

TEST(MPI_AllReduce, DoubleMin) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 1;
    double sendbuf = rank * rank * 0.1;
    double recvbuf = 0.0;
    const double min = 0.0;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_DOUBLE, MPI_MIN, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_NEAR(recvbuf, min, EPSILON);
}

TEST(MPI_AllReduce, DoubleSum) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 1;
    double sendbuf = rank * 0.1;
    double recvbuf = 0.0;
    double sum = size * (size - 1) / 20.0;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_NEAR(recvbuf, sum, EPSILON);
}

TEST(MPI_AllReduce, DoubleProd) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 1;
    double sendbuf = rank * 0.1;
    double recvbuf = 0.0;
    double prod = 1.0;

    for (int i = 0; i < size; ++i)
        prod *= i * 0.1;

    ASSERT_EQ(Allreduce(&sendbuf, &recvbuf, count, MPI_DOUBLE, MPI_PROD, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_NEAR(recvbuf, prod, EPSILON);
}

TEST(MPI_AllReduce, IntArrayMax) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 10;
    int* sendbuf = new int[count];
    int* recvbuf = new int[count];
    int* recvbufMPI = new int[count];

    std::mt19937 gen;
    gen.seed(static_cast<unsigned int>(time(0)));
    for (int i = 0; i < count; ++i)
        sendbuf[i] = gen() % 10;

    ASSERT_EQ(Allreduce(sendbuf, recvbuf, count, MPI_INT, MPI_MAX, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_EQ(MPI_Allreduce(sendbuf, recvbufMPI, count, MPI_INT, MPI_MAX, MPI_COMM_WORLD), MPI_SUCCESS);

    for (int i = 0; i < count; ++i) {
        ASSERT_EQ(recvbuf[i], recvbufMPI[i]);
    }

    delete[] sendbuf;
    delete[] recvbuf;
    delete[] recvbufMPI;
}

TEST(MPI_AllReduce, IntArrayMin) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 10;
    int* sendbuf = new int[count];
    int* recvbuf = new int[count];
    int* recvbufMPI = new int[count];

    std::mt19937 gen;
    gen.seed(static_cast<unsigned int>(time(0)));
    for (int i = 0; i < count; ++i)
        sendbuf[i] = gen() % 10;

    ASSERT_EQ(Allreduce(sendbuf, recvbuf, count, MPI_INT, MPI_MIN, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_EQ(MPI_Allreduce(sendbuf, recvbufMPI, count, MPI_INT, MPI_MIN, MPI_COMM_WORLD), MPI_SUCCESS);

    for (int i = 0; i < count; ++i)
        ASSERT_EQ(recvbuf[i], recvbufMPI[i]);

    delete[] sendbuf;
    delete[] recvbuf;
    delete[] recvbufMPI;
}

TEST(MPI_AllReduce, IntArraySum) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 10;
    int* sendbuf = new int[count];
    int* recvbuf = new int[count];
    int* recvbufMPI = new int[count];

    std::mt19937 gen;
    gen.seed(static_cast<unsigned int>(time(0)));
    for (int i = 0; i < count; ++i)
        sendbuf[i] = gen() % 10;

    ASSERT_EQ(Allreduce(sendbuf, recvbuf, count, MPI_INT, MPI_SUM, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_EQ(MPI_Allreduce(sendbuf, recvbufMPI, count, MPI_INT, MPI_SUM, MPI_COMM_WORLD), MPI_SUCCESS);

    for (int i = 0; i < count; ++i)
        ASSERT_EQ(recvbuf[i], recvbufMPI[i]);

    delete[] sendbuf;
    delete[] recvbuf;
    delete[] recvbufMPI;
}

TEST(MPI_AllReduce, IntArrayProd) {
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    const int count = 10;
    int* sendbuf = new int[count];
    int* recvbuf = new int[count];
    int* recvbufMPI = new int[count];

    std::mt19937 gen;
    gen.seed(static_cast<unsigned int>(time(0)));
    for (int i = 0; i < count; ++i)
        sendbuf[i] = gen() % 10;

    ASSERT_EQ(Allreduce(sendbuf, recvbuf, count, MPI_INT, MPI_PROD, MPI_COMM_WORLD), MPI_SUCCESS);
    ASSERT_EQ(MPI_Allreduce(sendbuf, recvbufMPI, count, MPI_INT, MPI_PROD, MPI_COMM_WORLD), MPI_SUCCESS);

    for (int i = 0; i < count; ++i)
        ASSERT_EQ(recvbuf[i], recvbufMPI[i]);

    delete[] sendbuf;
    delete[] recvbuf;
    delete[] recvbufMPI;
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    MPI_Init(&argc, &argv);

    ::testing::AddGlobalTestEnvironment(new GTestMPIListener::MPIEnvironment);
    ::testing::TestEventListeners& listeners =
            ::testing::UnitTest::GetInstance()->listeners();

    listeners.Release(listeners.default_result_printer());
    listeners.Release(listeners.default_xml_generator());

    listeners.Append(new GTestMPIListener::MPIMinimalistPrinter);
    return RUN_ALL_TESTS();
}
