from UncertaintyQuantification.Similarity import Distance

############Classifier############
'''Nearest Neighbors

Z is composed of 'y' label and 'x' vector

noCons: the index to doesn't compute'''

class Classifiers:
    def __init__(self):
        pass

    def NN(self,Z, noCons):
        minEq = float('inf')

        minDis = float('inf')

        for i in range(len(Z)):

            if i == noCons:
                continue

            # same label
            distanceFunction = Distance().text_distance
            if Z[i][1] == Z[noCons][1]:
                # read the file

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
