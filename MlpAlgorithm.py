import numpy as np
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
            learning_rate='constant',
            learning_rate_init=0.01,
            activation='relu',
            solver = 'adam'
        )

    entradaTreino, saidaTreino = returnDadosTreino()
    mlp.fit(entradaTreino, saidaTreino)

    entradaTeste, saidaTeste = returnDadosTeste()
    saidaPredita = mlp.predict(entradaTeste)

    accuracy = accuracy_score(saidaTeste, saidaPredita)    
    return (mlp, accuracy)