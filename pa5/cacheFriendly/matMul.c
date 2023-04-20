#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>
#define M 600


void matMulIJK (
    int a[M][M],
    int b[M][M],
    int c[M][M]
) {
    for ( int i=0; i<M; i++ )
        for ( int j=0; j<M; j++ ) {
            int sum = 0;
            for ( int k=0; k<M; k++ )
                sum += a[i][k] * b[k][j];
            c[i][j] += sum;
        }

    return;
}
// JIK

void matMulKIJ (
  int a[M][M],
  int b[M][M],
  int c[M][M]
) {
    for ( int k=0; k<M; k++ )
        for ( int i=0; i<M; i++ ) {
            int r = a[i][k];
            for ( int j=0; j<M; j++ )
                c[i][j] += r * b[k][j];
        }

    return;
}
// IKJ

void matMulJKI (
  int a[M][M],
  int b[M][M],
  int c[M][M]
) {
    for ( int j=0; j<M; j++ )
        for ( int k=0; k<M; k++ ) {
            int r = b[k][j];
            for ( int i=0; i<M; i++ )
                c[i][j] += a[i][k] * r;
        }

    return;
}
// KJI

int main() {

    time_t t;
    srand((unsigned) time(&t));

    // ALLOCATE AND INITIALIZE ARRAYS WITH RANDOM NUMBERS
    int a[M][M];
    for ( int i=0; i<M; i++ ) {
        for ( int k=0; k<M; k++ )
            a[i][k] = rand() % 256;
    }

    int b[M][M];
    for ( int k=0; k<M; k++ ) {
        for ( int j=0; j<M; j++ )
            b[k][j] = rand() % 256;
    }

    clock_t start, end;
    double cpu_time_used;

    // TIME matMulIJK
    int ijkResult[M][M];
    for ( int i=0; i<M; i++ )
        for ( int j=0; j<M; j++ )
            ijkResult[i][j] = 0;

    start = clock();
    matMulIJK( a, b, ijkResult );
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("matMulIJK took %lf seconds.\n", cpu_time_used);

    // TIME matMulKIJ
    int kijResult[M][M];
    for ( int i=0; i<M; i++ )
        for ( int j=0; j<M; j++ )
            kijResult[i][j] = 0;

    start = clock();
    matMulKIJ( a, b, kijResult );
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("matMulKIJ took %lf seconds.\n", cpu_time_used);

    // TIME matMulJKI
    int jkiResult[M][M];
    for ( int i=0; i<M; i++ )
        for ( int j=0; j<M; j++ )
            jkiResult[i][j] = 0;

    start = clock();
    matMulJKI( a, b, jkiResult );
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("matMulJKI took %lf seconds.\n", cpu_time_used);

    // // TIME matMulRcrs
    // int** rcrResult = calloc( M, sizeof(int*) );
    // for ( int i=0; i<M; i++ )
    //     rcrResult[i] = calloc( M, sizeof(int) );
    //
    // start = clock();
    // matMulRCR( m, 0, n, 0, p, 0, a, b, rcrResult );
    // end = clock();
    // cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    // printf("matMulRCR took %lf seconds.\n", cpu_time_used);

    for ( int i=0; i<M; i++ )
        for ( int j=0; j<M; j++ ) {
            assert ( ijkResult[i][j] == kijResult[i][j] );
            assert ( kijResult[i][j] == jkiResult[i][j] );
        }

    return EXIT_SUCCESS;
}
