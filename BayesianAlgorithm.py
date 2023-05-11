import numpy as np
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


from Utils import returnDadosTeste, returnDadosTreino


def BayesianAlgorithm():
    # Pré-processamento dos dados de entrada
    scaler = StandardScaler()

    entradaTreino, saidaTreino = returnDadosTreino()
    entradaTreino = scaler.fit_transform(entradaTreino)
    entradaTeste, saidaTeste = returnDadosTeste()
    entradaTeste = scaler.transform(entradaTeste)

    bayesian = BernoulliNB()

    # entradaTreino, saidaTreino = returnDadosTreino() - Anterior a melhoria
    bayesian.fit(entradaTreino, saidaTreino)

    entradaTeste, saidaTeste = returnDadosTeste()
    saidaPredita = bayesian.predict(entradaTeste)

    accuracy = accuracy_score(saidaTeste, saidaPredita)
    return (bayesian, accuracy)
