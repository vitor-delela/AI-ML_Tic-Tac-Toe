import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from Utils import returnDadosTreino, returnDadosTeste
import matplotlib.pyplot as plt


def KnnAlgorithm():
    # Define o algoritmo knn com o respectivo valor de k
    knn = KNeighborsClassifier(n_neighbors=6)

    # as posicoes a serem treinadas e os rótulos do conjunto de treino
    (
        treinoPosicoes,
        treinoRotulos,
    ) = returnDadosTreino()
    knn.fit(treinoPosicoes, treinoRotulos)  # Treina o algoritmo

    (
        testePosicoes,
        testeRotulos,
    ) = (
        returnDadosTeste()
    )  # as posicoes a serem testadas e os rótulos verdadeiros do conjunto de teste

    teste = knn.predict(testePosicoes)  # previsões do modelo para o conjunto de teste

    accuracy = accuracy_score(testeRotulos, teste)

    return (knn, accuracy)


def KnnCharts():
    num_vizinhos = 100
    scores = []
    (
        testePosicoes,
        testeRotulos,
    ) = (
        returnDadosTeste()
    )  # as posicoes a serem testadas e os rótulos verdadeiros do conjunto de teste
    (
        treinoPosicoes,
        treinoRotulos,
    ) = (
        returnDadosTreino()
    )  # as posicoes a serem treinadas e os rótulos do conjunto de treino
    for k in range(1, num_vizinhos):
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(treinoPosicoes, treinoRotulos)
        accuracy = model.score(testePosicoes, testeRotulos)
        scores.append(accuracy)

    plt.plot(np.arange(1, num_vizinhos), scores)
    plt.title("Acurácias do k-NN por número de vizinhos")
    plt.xlabel("Número de vizinhos")
    plt.ylabel("Acurácia")
    plt.show()
