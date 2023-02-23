import math
import csv
import os


############  Similarity Module  ############
# return the distance between 2 texts
def text_distance(string_a, string_b):
    s = os.popen('perl  /Users/rahulvishwakarma/Downloads/Text-Similarity-0.13/bin/text_similarity.pl '
                 '--type=Text::Similarity::Overlaps --verbose '
                 '--stoplist=/Users/rahulvishwakarma/Downloads/Text-Similarity-0.13/samples/stoplist.txt --string "{'
                 '}" "{}"'.format(string_a.replace("`", "").replace("-", "").replace("(", "").replace(")",
                                                                                                      "").replace(
        '"', ''), string_b.replace("`", "").replace("-", "").replace("(", "").replace(")", "").replace('"', ''))).read()

    s = s.split('\n')

    if 'keys: 0' in s:

        return 1

    else:

        distance = 1 - float(s[0])

        return distance


############Classifier############
'''Nearest Neighbors

Z is composed of 'y' label and 'x' vector

noCons: the index to doesn't compute'''


def NN(Z, noCons):
    minEq = float('inf')

    minDis = float('inf')

    for i in range(len(Z)):

        if i == noCons:
            continue

        # same label

        if Z[i][1] == Z[noCons][1]:

            t = distanceFunction(Z[i][0], Z[noCons][0])

            if t < minEq:
                minEq = t

        else:

            t = distanceFunction(Z[i][0], Z[noCons][0])

            if t < minDis:
                minDis = t

    if minDis == 0:

        if minEq == 0:

            return 0

        else:

            return float('inf')

    return float(minEq) / minDis


############Algorithms############


'''Inductive Conformal Prediction

A: nonConformity function

B: training set

alphas: non-conformity scores

z: the test example'''


def ICP(A, error, B, alphas, z):
    az = __non_conformity_score(A, B, z)

    n = len(alphas)

    c = 0

    for i in range(n):

        if alphas[i] >= az:
            c += 1

    pValue = float(c) / n

    if pValue > error:

        return True, pValue

    else:

        return False, pValue


def __non_conformity_score(A, B, z):
    B.append(z)

    n = len(B)

    az = A(B, n - 1)

    B.pop(n - 1)

    return az


############Main############


if __name__ == "__main__":

    commentTraining = []  # training set

    commentTest = []  # test set

    actual_labels = []

    lineCounter = 1

    with open(r"/Users/rahulvishwakarma/PycharmProjects/CECS590/dataset/nlp_100.csv", "r", encoding='latin-1') as f:

        for line in f:

            # t = (line.replace("\n", "").split("\","))

            # t[0]=t[0]+"\""

            line = line.replace("\n", "")

            # if lineCounter == 20001:

            #       break
            if lineCounter > 80:

                t = []

                t.append(line[:-2])

                actual_labels.append(int(line[-1]))

                commentTest.append(t)

            else:

                t1 = []

                t1.append(line[:-2])

                t1.append(int(line[-1]))

                commentTraining.append(t1)

            lineCounter += 1

    # read the file

    distanceFunction = text_distance

    Classifier = NN

    # To test the Inductive Conformal Prediction

    proper_set = commentTraining[:70]
    #proper_set = commentTraining[:30]

    calibration_set = commentTraining[70:]
    #calibration_set = commentTraining[30:]
    #
    alphas = []

    n = len(calibration_set)

    output = []

    pvalues = []

    for i in range(n):
        alphas.append(__non_conformity_score(Classifier, proper_set, calibration_set[i]))

    for i in range(10):

        v = commentTest[i]

        v = v[0]

        canAddOne, pOne = ICP(Classifier, 0.05, proper_set, alphas, [v, 1])

        canAddZero, pZero = ICP(Classifier, 0.05, proper_set, alphas, [v, 0])

        pvalues.append([pOne, pZero])

        if pOne > pZero:

            print("%d -> One" % (0 + i + 1) + "...." + str(pOne) + " " + str(pZero))

            output.append(1)

            alphas.append(__non_conformity_score(Classifier, proper_set, [v, 1]))

        else:

            print("%d -> Zero" % (0 + i + 1) + "...." + str(pZero) + " " + str(pOne))

            output.append(0)

            alphas.append(__non_conformity_score(Classifier, proper_set, [v, 0]))

    print(output)

    print(pvalues)

    with open(r"/Users/rahulvishwakarma/Downloads/final_output_100_with_pvalues_100.txt", "a") as f1:

        f1.write(str(output))

        f1.write(str(pvalues))
