import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from Utils import returnDadosTeste, returnDadosTreino


def DecisionTreeAlgorithm():
    decisionTree = DecisionTreeClassifier()

    entradaTreino, saidaTreino = returnDadosTreino()
    decisionTree.fit(entradaTreino, saidaTreino)

    entradaTeste, saidaTeste = returnDadosTeste()
    saidaPredita = decisionTree.predict(entradaTeste)

    accuracy = accuracy_score(saidaTeste, saidaPredita)
    return (decisionTree, accuracy)
