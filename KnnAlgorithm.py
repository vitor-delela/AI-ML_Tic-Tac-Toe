import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from Utils import returnDadosTreino, returnDadosTeste

def KnnAlgorithm():
    knn = KNeighborsClassifier(n_neighbors=3, metric='euclidean') # Define o algoritmo knn com o respectivo valor de k
    treinoPosicoes, treinoRotulos = returnDadosTreino() # as posicoes a serem treinadas e os rótulos do conjunto de treino
    knn.fit(treinoPosicoes, treinoRotulos) # Treina o algoritmo

    testePosicoes, testeRotulos = returnDadosTeste() # as posicoes a serem testadas e os rótulos verdadeiros do conjunto de teste

    teste = knn.predict(testePosicoes) # previsões do modelo para o conjunto de teste

    accuracy = accuracy_score(testeRotulos, teste)

    return (knn, accuracy)