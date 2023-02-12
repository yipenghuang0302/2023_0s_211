#!/usr/bin/python3

import os
import datetime
import random
import subprocess
import numpy

def cost ( matDims ):
    # matDims are an array of tuples; first element of tuple is row count, second element of tuple is col count
    if len(matDims)==1:
        return 0
    else:
        costs = []
        for split in range( 0, len(matDims)-1 ):
            splitCost = cost( matDims[:split+1] ) + matDims[0][0]*matDims[split][1]*matDims[-1][1] + cost( matDims[split+1:] )
            costs.append ( splitCost )
    return min(costs)

def matChainMul ( matDims, matrices ):

    assert len(matDims) == len(matrices)

    if len(matDims)==1:
        return matrices[0]
    else:
        costs = []
        for split in range( 0, len(matDims)-1 ):
            splitCost = cost( matDims[:split+1] ) + matDims[0][0]*matDims[split][1]*matDims[-1][1] + cost( matDims[split+1:] )
            costs.append ( splitCost )

    bestSplit = costs.index(min(costs))

    lMatMulProduct = matChainMul ( matDims[:bestSplit+1], matrices[:bestSplit+1] )
    rMatMulProduct = matChainMul ( matDims[bestSplit+1:], matrices[bestSplit+1:] )

    matMulProduct = []
    for i in range (matDims[0][0]):
        matMulProduct.append([])
        for k in range (matDims[-1][1]):
            matMulProduct[i].append(0)
            for j in range(matDims[bestSplit][1]):
                matMulProduct[i][k] += lMatMulProduct[i][j] * rMatMulProduct[j][k]

    return matMulProduct

def generate_test ( filenum, matCount=2, maxDim=4, path="./" ):

    matDims = []
    matDims.append( (random.randrange(1,maxDim), random.randrange(1,maxDim)) )
    for matIndex in range(1, matCount):
        matDims.append( (matDims[matIndex-1][1], random.randrange(1,maxDim)) )
    # print("matDims=")
    # print(matDims)

    matrices = []
    for matIndex in range(matCount):
        l = matDims[matIndex][0]
        m = matDims[matIndex][1]
        matrices.append( [[random.randrange(4) for j in range(m)] for i in range(l)] )
    # print("matrices=")
    # print(matrices)

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write("{}\n".format(matCount))
        for matIndex in range(matCount):
            infile.write("{} {}\n".format(matDims[matIndex][0], matDims[matIndex][1]))
            for i in range (matDims[matIndex][0]):
                for j in range (matDims[matIndex][1]):
                    infile.write("{} ".format(matrices[matIndex][i][j]))
                infile.write("\n")
        infile.write("\n")

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:

        outfile.write( "{}\n".format( cost(matDims) ) )

        matChainMulProduct = matChainMul ( matDims, matrices )
        numpyProduct = numpy.linalg.multi_dot(matrices)
        assert numpy.asarray(matChainMulProduct).shape == numpyProduct.shape
        assert (numpy.asarray(matChainMulProduct) == numpyProduct).all()

        for i in range (matDims[0][0]):
            for k in range (matDims[-1][1]):
                outfile.write("{} ".format(matChainMulProduct[i][k]))
            outfile.write("\n")

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, matCount=2, maxDim=2, path="./" )
    generate_test ( 1, matCount=2, maxDim=4, path="./" )
    generate_test ( 2, matCount=3, maxDim=2, path="./" )
    generate_test ( 3, matCount=3, maxDim=4, path="./" )
    generate_test ( 4, matCount=4, maxDim=4, path="./" )
    generate_test ( 5, matCount=4, maxDim=6, path="./" )

def test_matChainMul ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            lines = outfile.read().split('\n')
            answerMulCount = int(lines[0])
            answerMatrix = []
            for line in lines[1:]:
                if line != '':
                    strings = line.split(' ')
                    answerMatrix.append([])
                    for string in strings:
                        if string != '':
                            answerMatrix[-1].append(int(string))
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./matChainMul", "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=2).total_seconds(),
        )

        with open("{}mul_op_count.txt".format(path,filenum), "r") as countfile:
            resultMulCount = int(countfile.read())

        lines = result.stdout.split('\n')
        resultMatrix = []
        for line in lines:
            if line != '':
                resultMatrix.append([])
                for string in line.split():
                    resultMatrix[-1].append(int(string))

        if verbose:
            print (' '.join(result.args))
            # print ("answerMulCount")
            # print (answerMulCount)
            # print ("resultMulCount")
            # print (resultMulCount)
            # print ("answerMatrix")
            # print (answerMatrix)
            # print ("resultMatrix")
            # print (resultMatrix)
        assert resultMulCount == answerMulCount, "The optimal number of multiplications you used doesn't match answers/answer{}.txt.".format(filenum)
        assert resultMatrix == answerMatrix, "The matChainMul matrix result doesn't match answers/answer{}.txt.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./matChainMul returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_matChainMul( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile matChainMul.c.")
        return score

    if test_matChainMul(0,path,verbose):
        score += 2
        if test_matChainMul(1,path,verbose):
            score += 2
            if test_matChainMul(2,path,verbose):
                score += 2
                if test_matChainMul(3,path,verbose):
                    score+= 2
                    if test_matChainMul(4,path,verbose):
                        score+= 2
                        if test_matChainMul(5,path,verbose):
                            score+= 2
                            for filenum in range(6,19):
                                generate_test ( filenum, matCount=6, maxDim=8, path=path )
                                if test_matChainMul(filenum,path,verbose):
                                    score+=1

    print ("Score on matChainMul: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_matChainMul(verbose=True)
    exit()
