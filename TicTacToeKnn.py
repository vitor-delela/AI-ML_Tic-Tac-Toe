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
mapa = {'x': 1, 'o': -1, 'b': 0, 'X': 1, 'O': -1, 'B': 0}

valores_numeros = []
for entrada in dadosTabuleiro:
    # Separa os valores da entrada em uma lista e aplica o mapeamento pra cada valor da lista
    valores = entrada.split(',')
    valores_numeros.append(np.array([mapa[x] for x in valores]))

dadosTabuleiroArr = np.array(valores_numeros)
dadosClassificacoArr = np.array(dadosClassificaco)

# Define o algoritmo k-NN com k=4
knn = KNeighborsClassifier(n_neighbors=4, metric='euclidean')

# Treina o algoritmo com as instâncias de treinamento e as classes correspondentes
knn.fit(dadosTabuleiroArr, dadosClassificacoArr)

def verifica_acabou(tabuleiroAtual):

    # Define a instância a ser testada
    #X_test = ['x,x,x,x,o,o,x,o,o'] #[-1, 0, 0, -1, 1, 1, -1, 1, 1]

    entradaConvertida = [mapa[x] for x in tabuleiroAtual.replace(',', '')]

    # Classifica a instância de teste com base nas instâncias de treinamento
    prediction = knn.predict(np.array(entradaConvertida).reshape(1,-1))
    print("prediction: ")
    print(prediction)

    # Imprime a classe prevista para a instância de teste
    #print("\nAinda tem jogo!\n" if prediction == "negative" else "\nJogo acabou!\n")
    #return (True if prediction == "negative" else False)
    return False



# Definindo o tabuleiro
tabuleiro = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

# Função para imprimir o tabuleiro
def imprime_tabuleiro():
    print(tabuleiro[0] + '|' + tabuleiro[1] + '|' + tabuleiro[2])
    print('-+-+-')
    print(tabuleiro[3] + '|' + tabuleiro[4] + '|' + tabuleiro[5])
    print('-+-+-')
    print(tabuleiro[6] + '|' + tabuleiro[7] + '|' + tabuleiro[8])

# Função principal do jogo
def jogo_da_velha():
    jogando = True
    jogador_atual = 'x'

    while jogando:
        imprime_tabuleiro()
        jogada = input("Entre a posição desejada: ")
        
        # Verifica se a jogada é válida
        while jogada not in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] or tabuleiro[int(jogada)-1] != ' ':
            jogada = input("Entre a posição desejada: ")

        # Atualiza o tabuleiro com a jogada do jogador atual
        tabuleiro[int(jogada)-1] = jogador_atual

        #num_nao_vazios = len([elem for elem in tabuleiro if elem.strip() != ''])

        # Verifica se houve vencedor, se nao passa a vez para o próximo jogador
        if verifica_acabou((",".join([elem.strip() if elem.strip() != '' else 'b' for elem in tabuleiro]))):
            imprime_tabuleiro()
            jogando = False
        else:
            if jogador_atual == 'x':
                jogador_atual = 'o'
            else:
                jogador_atual = 'x'

# Inicia o jogo
jogo_da_velha()
