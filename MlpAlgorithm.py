import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
from Utils import returnDadosTreino, returnDadosTeste


def MlpAlgorithm():
    mlp = MLPClassifier(
        hidden_layer_sizes=(1000,),
        max_iter=600,
        verbose=False,
        learning_rate="constant",
        learning_rate_init=0.01,
        activation="relu",
        solver="adam",
    )

    entradaTreino, saidaTreino = returnDadosTreino()
    mlp.fit(entradaTreino, saidaTreino)

    entradaTeste, saidaTeste = returnDadosTeste()
    saidaPredita = mlp.predict(entradaTeste)

    accuracy = accuracy_score(saidaTeste, saidaPredita)
    return (mlp, accuracy)


def MlpCharts():
    repeticoes = 1000
    scores = []
    (
        entradaTeste,
        saidaTeste,
    ) = (
        returnDadosTeste()
    )  # as posicoes a serem testadas e os rótulos verdadeiros do conjunto de teste
    (
        entradaTreino,
        saidaTreino,
    ) = (
        returnDadosTreino()
    )  # as posicoes a serem treinadas e os rótulos do conjunto de treino

    for k in range(100, 1000, 100):
        model = MLPClassifier(
            hidden_layer_sizes=(k,),
            max_iter=2000,
            verbose=False,
            learning_rate="constant",
            learning_rate_init=0.01,
            activation="identity",
            solver="sgd",
        )
        model.fit(entradaTreino, saidaTreino)
        saidaPredita = model.predict(entradaTeste)
        accuracy = accuracy_score(saidaTeste, saidaPredita)
        print(accuracy)
    # accuracy = model.score(entradaTeste, saidaTeste)

    # scores.append("{:.2f}".format(accuracy * 100))


# MlpCharts()

# plt.plot(np.arange(100, repeticoes, 10), scores)
# plt.title(
#     "Acurácias MLP de 100 a 1000 neurônios em 1 camada e de 200 a 1200 interações"
# )
# plt.xlabel("Número de neurônios")
# plt.ylabel("Acurácia")
# plt.show()
