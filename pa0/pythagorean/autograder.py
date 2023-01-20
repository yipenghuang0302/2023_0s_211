#!/usr/bin/python3

import os
import datetime
import random
import subprocess
from math import sqrt

def is_triplet_subset ( x, y ):
    z = int(sqrt(x*x+y*y))
    w = int(sqrt(y*y-x*x))
    if x*x + y*y == z*z:
        return True
    elif w*w + x*x == y*y:
        return True
    else:
        return False

def generate_test ( filenum, is_pyth_triplet, max=3, path="./" ):

    if is_pyth_triplet:
        m = random.randrange(2,max)
        n = random.randrange(1,m)
        a = m*m - n*n
        b = 2*m*n
        c = m*m + n*n
    else:
        accidentally_is_triplet = True
        while accidentally_is_triplet:
            c = random.randrange(3,max)
            b = random.randrange(2,c)
            a = random.randrange(1,b)
            accidentally_is_triplet = is_triplet_subset(a,b) or is_triplet_subset(a,c) or is_triplet_subset(b,c)

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:

        if bool(random.getrandbits(1)): # smaller number first
            ans_index = random.randrange(3)
            if ans_index==0:
                infile.write(str(b))
                infile.write("\n")
                infile.write(str(c))
            elif ans_index==1:
                infile.write(str(a))
                infile.write("\n")
                infile.write(str(c))
            elif ans_index==2:
                infile.write(str(a))
                infile.write("\n")
                infile.write(str(b))
            else:
                raise Exception("Indexing into triplet out of range.")
        else: # bigger number first
            ans_index = random.randrange(3)
            if ans_index==0:
                infile.write(str(c))
                infile.write("\n")
                infile.write(str(b))
            elif ans_index==1:
                infile.write(str(c))
                infile.write("\n")
                infile.write(str(a))
            elif ans_index==2:
                infile.write(str(b))
                infile.write("\n")
                infile.write(str(a))
            else:
                raise Exception("Indexing into triplet out of range.")


    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:

        if is_pyth_triplet:
            outfile.write(str([a,b,c][ans_index]))
        else:
            outfile.write(str(-1))

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, True, max=3, path="./" )
    generate_test ( 1, True, max=6, path="./" )
    generate_test ( 2, True, max=9, path="./" )
    generate_test ( 3, False, max=4, path="./" )
    generate_test ( 4, False, max=8, path="./" )
    generate_test ( 5, False, max=12, path="./" )
    generate_test ( 6, True, max=16, path="./" )
    generate_test ( 7, False, max=16, path="./" )

def test_pythagorean ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerString = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./pythagorean", "tests/test{}.txt".format(filenum)],
            cwd=path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="ASCII",
            timeout=datetime.timedelta(seconds=2).total_seconds(),
        )

        resultString = result.stdout.strip()

        if verbose:
            print (' '.join(result.args))
            # print ("answerString")
            # print (answerString)
            # print ("resultString")
            # print (resultString)
        assert resultString == answerString, "The program output does not complete the Pythagorean triplet, or program failed to return -1 if triplet not possible.".format(filenum)
        return True
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./pythagorean returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_pythagorean( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile pythagorean.c.")
        return score

    if test_pythagorean(0,path,verbose):
        score += 1
        if test_pythagorean(1,path,verbose):
            score += 1
            if test_pythagorean(2,path,verbose):
                score += 1
                if test_pythagorean(3,path,verbose):
                    score += 1
                    if test_pythagorean(4,path,verbose):
                        score += 1
                        if test_pythagorean(5,path,verbose):
                            score += 1
                            if test_pythagorean(6,path,verbose):
                                score += 1
                                if test_pythagorean(7,path,verbose):
                                    score += 1
                                    allPass = True
                                    for filenum in range(8,15):
                                        generate_test (
                                            filenum,
                                            is_pyth_triplet=bool(random.getrandbits(1)),
                                            max=128,
                                            path=path
                                        )
                                        allPass &= test_pythagorean(filenum,path,verbose)
                                        if allPass:
                                            score += 1
                                        else:
                                            break

    print ("Score on pythagorean: {} out of 15.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_pythagorean(verbose=True)
    exit()
