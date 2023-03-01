from UncertaintyQuantification.Similarity import Distance
from UncertaintyQuantification.Classifier import Classifiers
from UncertaintyQuantification.Algorithms import Algos
from UncertaintyQuantification.GraphPlot import Visualize
import configparser
#Loading config
config = configparser.ConfigParser()
config.read("UncertaintyQuantification/config.ini")
OUTPUT_LOCATION = config["location"]["output_location"]
DATASET_LOCATION=config["location"]["dataset_location"]
############Main############


if __name__ == "__main__":

    commentTraining = []  # training set

    commentTest = []  # test set

    actual_labels = []

    lineCounter = 1

    with open(DATASET_LOCATION, "r", encoding='latin-1') as f:

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

    distanceFunction = Distance().text_distance

    Classifier = Classifiers().NN

    # To test the Inductive Conformal Prediction

    proper_set = commentTraining[:70]
    # proper_set = commentTraining[:30]

    calibration_set = commentTraining[70:]
    # calibration_set = commentTraining[30:]

    alphas = []

    n = len(calibration_set)

    output = []

    pvalues = []

    confidence_X=[]
    credibility_Y=[]

    for i in range(n):
        alphas.append(Algos().non_conformity_score(Classifier, proper_set, calibration_set[i]))

    for i in range(10):

        v = commentTest[i]

        v = v[0]

        canAddOne, pOne = Algos().ICP(Classifier, 0.05, proper_set, alphas, [v, 1])

        canAddZero, pZero = Algos().ICP(Classifier, 0.05, proper_set, alphas, [v, 0])

        pvalues.append([pOne, pZero])
        confidence_X.append(1-max(pOne,pZero))
        credibility_Y.append(max(pOne,pZero))

        if pOne > pZero:

            print("%d -> One" % (0 + i + 1) + "...." + str(pOne) + " " + str(pZero))

            output.append(1)

            alphas.append(Algos().non_conformity_score(Classifier, proper_set, [v, 1]))

        else:

            print("%d -> Zero" % (0 + i + 1) + "...." + str(pZero) + " " + str(pOne))

            output.append(0)

            alphas.append(Algos().non_conformity_score(Classifier, proper_set, [v, 0]))

    print(output)

    print(pvalues)
    visualize=Visualize().plot_graph(confidence_X,credibility_Y,"Confidence","Credibility","Confidence vs Credibility")

    with open(OUTPUT_LOCATION, "a") as f1:

        f1.write(str(output))

        f1.write(str(pvalues))
