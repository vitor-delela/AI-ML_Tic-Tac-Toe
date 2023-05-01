#pip install -U scikit-learn

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer

# Carrega o dataset atraves da Leitura do arquivo CSV
data = np.genfromtxt('/Users/vitordelela/Downloads/tic-tac-toe.data', delimiter='\n', dtype=str, encoding=None)

dadosTabuleiro = []
dadosClassificaco = []

for linha in data:
    valores = linha.split(',')
    dadosTabuleiro.append(','.join(valores[:9]))
    dadosClassificaco.append(','.join(valores[9:]))

# Define o dicionário de mapeamento
mapa = {'x': 1, 'o': -1, 'b': 0}

valores_numeros = []
for entrada in dadosTabuleiro:
    # Separa os valores da entrada em uma lista
    valores = entrada.split(',')
    # Aplica o mapeamento a cada valor da lista
    valores_numeros.append(np.array([mapa[x] for x in valores]))

dadosTabuleiroArr = np.array(valores_numeros)
dadosClassificacoArr = np.array(dadosClassificaco)

# Define o algoritmo k-NN com k=3
knn = KNeighborsClassifier(n_neighbors=3, metric='euclidean')

# Treina o algoritmo com as instâncias de treinamento e as classes correspondentes
knn.fit(dadosTabuleiroArr, dadosClassificacoArr)

# Define a instância a ser testada
X_test = ['x,x,x,x,o,o,x,o,o'] #[-1, 0, 0, -1, 1, 1, -1, 1, 1]

entradaConvertida = [mapa[x] for x in X_test[0].replace(',', '')]

# Classifica a instância de teste com base nas instâncias de treinamento
prediction = knn.predict(np.array(entradaConvertida).reshape(1,-1))

# Imprime a classe prevista para a instância de teste
print("Ainda tem jogo!" if prediction == "negative" else "Jogo acabou!")

