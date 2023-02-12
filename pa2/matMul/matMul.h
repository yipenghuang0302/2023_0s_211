#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>

size_t mulOpCount = 0;
bool set = false;

void printLog ( void ) {
    FILE *fp = fopen("mul_op_count.txt", "w");
    fprintf(fp, "%ld", mulOpCount);
    fclose(fp);
}

unsigned int mul (
    unsigned int multiplier,
    unsigned int multiplicand
) {
    if (!set) {
        atexit(printLog);
        set = true;
    }
    mulOpCount++;
    return multiplier * multiplicand;
}

void matMul (
    unsigned int l,
    unsigned int m,
    unsigned int n,
    int** matrix_a,
    int** matrix_b,
    int** matMulProduct
) {

    // printf("l=%d\n", l);
    // printf("m=%d\n", m);
    // printf("n=%d\n", n);

    for ( unsigned int i=0; i<l; i++ ) {
        // printf("i=%d\n", i);
        for ( unsigned int k=0; k<n; k++ ) {
            // printf("k=%d\n", k);
            matMulProduct[i][k] = 0;
            for ( unsigned int j=0; j<m; j++ ) {
                matMulProduct[i][k] += mul ( matrix_a[i][j], matrix_b[j][k] );
            }
        }
    }

}
