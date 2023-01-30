#!/usr/bin/python3

import os
import datetime
import random
import subprocess

def generate_test ( filenum, max=4, path="./" ):

    randList = [random.randrange(2*max) for i in range(max)]
    randIndex = random.randrange(max)

    with open("{}tests/test{}.txt".format(path,filenum), "w") as infile:
        infile.write(f"{max}\n")
        infile.write(f"{randIndex}\n\n")
        for num in randList:
            infile.write(f"{num}\n")

    with open("{}answers/answer{}.txt".format(path,filenum), "w") as outfile:
        randList.sort()
        outfile.write(f"{randList[randIndex]}")

def generate_test_suite():

    os.makedirs("tests", exist_ok=True)
    os.makedirs("answers", exist_ok=True)

    generate_test ( 0, max=2, path="./" )
    generate_test ( 1, max=4, path="./" )
    generate_test ( 2, max=8, path="./" )
    generate_test ( 3, max=16, path="./" )
    generate_test ( 4, max=32, path="./" )
    generate_test ( 5, max=128, path="./" )
    generate_test ( 6, max=1024, path="./" )
    generate_test ( 7, max=16384, path="./" )

def test_quickselect ( filenum, path="./", verbose=False ):

    try:
        with open("{}answers/answer{}.txt".format(path,filenum), "r") as outfile:
            answerString = outfile.read()
    except EnvironmentError: # parent of IOError, OSError
        print ("answers/answer{}.txt missing".format(filenum))

    try:
        result = subprocess.run(
            ["./quickselect", "tests/test{}.txt".format(filenum)],
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
            # print ("answer")
            # print (answerString)
            # print ("result")
            # print (result.stdout)
        assert resultString == answerString, "The program output does not output the k-th smallest element.".format(filenum)
        return True
    except subprocess.TimeoutExpired as e:
        print (e.output)
        print ("Calling ./quickselect with the previous test case timed out.")
    except subprocess.CalledProcessError as e:
        print (e.output)
        print ("Calling ./quickselect returned an error.")
    except ValueError as e:
        print (' '.join(result.args))
        print (result.stdout)
        print ("Please check your output formatting.")
    except AssertionError as e:
        print (result.stdout)
        print (e.args[0])

    return False

def grade_quickselect( path="./", verbose=False ):

    score = 0

    try:
        subprocess.run( ["make", "clean"], cwd=path, check=True, )
        subprocess.run( ["make", "-B"], cwd=path, check=True, )
    except subprocess.CalledProcessError as e:
        print ("Couldn't compile quickselect.c.")
        return score

    if test_quickselect(0,path,verbose):
        score += 2
        if test_quickselect(1,path,verbose):
            score += 2
            if test_quickselect(2,path,verbose):
                score += 2
                if test_quickselect(3,path,verbose):
                    score += 2
                    if test_quickselect(4,path,verbose):
                        score += 2
                        if test_quickselect(5,path,verbose):
                            score += 2
                            if test_quickselect(6,path,verbose):
                                score += 2
                                if test_quickselect(7,path,verbose):
                                    score += 2
                                    allPass = True
                                    for filenum in range(8,17):
                                        generate_test (
                                            filenum,
                                            max=65536,
                                            path=path
                                        )
                                        allPass &= test_quickselect(filenum,path,verbose)
                                        if allPass:
                                            score += 1
                                        else:
                                            break

    print ("Score on quickselect: {} out of 25.".format(score))
    return score

if __name__ == '__main__':
    # generate_test_suite()
    grade_quickselect(verbose=True)
    exit()
