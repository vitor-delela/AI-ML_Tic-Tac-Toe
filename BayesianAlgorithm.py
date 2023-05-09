import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

from Utils import returnDadosTeste, returnDadosTreino


def BayesianAlgorithm():
    bayesian = GaussianNB()

    entradaTreino, saidaTreino = returnDadosTreino()
    bayesian.fit(entradaTreino, saidaTreino)

    entradaTeste, saidaTeste = returnDadosTeste()
    saidaPredita = bayesian.predict(entradaTeste)

    accuracy = accuracy_score(saidaTeste, saidaPredita)
    return (bayesian, accuracy)
