############Algorithms############

'''Inductive Conformal Prediction

A: nonConformity function

B: training set

alphas: non-conformity scores

z: the test example'''


class Algos:
    def __init__(self):
        pass

    def ICP(self, A, error, B, alphas, z):
        az = self.non_conformity_score(A, B, z)

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

    def non_conformity_score(self, A, B, z):
        B.append(z)

        n = len(B)

        az = A(B, n - 1)

        B.pop(n - 1)

        return az
