# pip install -U scikit-learn

import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

aprendeDataset = False
datasetTreino = './tic-tac-toe-treino.data'
datasetTeste = './tic-tac-toe-teste.data'

mapa = {'x': 1, 'o': -1, 'b': 0, 'X': 1, 'O': -1, 'B': 0}  # Dicionário de mapeamento

""" -------------------------------------------------------------------------------------------------------

MODIFICACOES NO DATASET

------------------------------------------------------------------------------------------------------- """


def converteDatasetParaDoisArrays(dataset):
    data = np.genfromtxt(dataset, delimiter='\n', dtype=str, encoding=None)

    posicoesTabuleiro = []
    rotulos = []

    # Divide dataset entre posicoes e rotulos
    for linha in data:
        valores = linha.split(',')
        posicoesTabuleiro.append(','.join(valores[:9]))
        rotulos.append(','.join(valores[9:]))

    # Converte os valores x, o e b para valores numericos de acordo com o dicionario acima
    valores_numeros = []
    for entrada in posicoesTabuleiro:
        valores = entrada.split(',')  # Separa os valores da entrada em uma lista
        valores_numeros.append(np.array([mapa[x] for x in valores]))  # aplica o mapeamento pra cada valor da lista

    posicoesTabuleiroArr = np.array(valores_numeros)
    rotulosArr = np.array(rotulos)

    return posicoesTabuleiroArr, rotulosArr


""" -------------------------------------------------------------------------------------------------------

Bayesiano - Treino e Testes

------------------------------------------------------------------------------------------------------- """
# Cria o modelo Bayesiano
model = DecisionTreeClassifier()


treinoPosicoes, treinoRotulos = converteDatasetParaDoisArrays(
    datasetTreino)
model.fit(treinoPosicoes, treinoRotulos)  # Treina o algoritmo

testePosicoes, testeRotulos = converteDatasetParaDoisArrays(
    datasetTeste)  # as posicoes a serem testadas e os rótulos verdadeiros do conjunto de teste

teste = model.predict(testePosicoes)  # previsões do modelo para o conjunto de teste

accuracy = accuracy_score(testeRotulos, teste)
print("Eficiente dos testes: {:.2f}%".format(accuracy * 100))

""" -------------------------------------------------------------------------------------------------------

Bayesiano - jogadas

------------------------------------------------------------------------------------------------------- """


def atualiza_status_partida(tabuleiroAtual):
    # print("tabuleiroAtual: ")
    # print(tabuleiroAtual)
    imprime_tabuleiro()

    entradaConvertida = [mapa[x] for x in tabuleiroAtual.replace(',', '')]  # traduz X para 1, O para -1 e b para 0
    prediction = model.predict(np.array(entradaConvertida).reshape(1, -1))  # Classifica o teste com base no treinamento

    # Imprime o resultado esperado com base na predição
    if prediction == "positive":
        print("\nVitoria de X!\n")
    elif prediction == "negative":
        print("\nVitoria de O!\n")
    elif prediction == "draw":
        print("\nEmpate!\n")
    elif prediction == "continue":
        print("\nAinda tem jogo!\n")
    else:
        print("\nErro na leitura dos resultados!\n")

    # recebe feedback a cada jogada para verificar se o resultado foi correto
    if aprendeDataset:
        resposta = 'a'
        while resposta != 'y' and resposta != 'n':
            resposta = input("Foi o resultado correto? (y/n): ")
            if (resposta == 'N' or resposta == 'n'):
                gravar = input("Digite o resultado esperado para ser gravado: ")
                gravar = tabuleiroAtual + ',' + gravar

                with open(datasetTreino, 'r') as f:
                    conteudo = f.readlines()  # armazena todo dataset para evitar jogada repetida

                # adiciona a combinacao da jogada somente se ela nao existe previamente no dataset
                if tabuleiroAtual + ",positive\n" not in conteudo and \
                        tabuleiroAtual + ",negative\n" not in conteudo and \
                        tabuleiroAtual + ",draw\n" not in conteudo and \
                        tabuleiroAtual + ",continue\n" not in conteudo:
                    arquivo = open(datasetTreino, "a")
                    arquivo.write("\n")
                    arquivo.write(gravar)
                    arquivo.close()
                print("tabuleiroAtual: ")
                print(tabuleiroAtual)

    return False if 0 in entradaConvertida else True


""" -------------------------------------------------------------------------------------------------------

FRONT END

------------------------------------------------------------------------------------------------------- """


# Função para imprimir o tabuleiro
def imprime_tabuleiro():
    print(tabuleiro[0] + '|' + tabuleiro[1] + '|' + tabuleiro[2])
    print('-+-+-')
    print(tabuleiro[3] + '|' + tabuleiro[4] + '|' + tabuleiro[5])
    print('-+-+-')
    print(tabuleiro[6] + '|' + tabuleiro[7] + '|' + tabuleiro[8])


# Função principal do jogo
def jogo():
    temJogo = True
    player = 'x'

    imprime_tabuleiro()

    while temJogo:
        jogada = input("Entre a posição desejada: ")

        # Verifica se a jogada é válida
        while jogada not in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] or tabuleiro[int(jogada) - 1] != ' ':
            jogada = input("Entre a posição desejada: ")

        # Atualiza o tabuleiro com a jogada do jogador atual
        tabuleiro[int(jogada) - 1] = player

        # Atualiza o status com base no Bayesiano e passa a vez para o próximo jogador se houver
        if atualiza_status_partida((",".join([elem.strip() if elem.strip() != '' else 'b' for elem in tabuleiro]))):
            imprime_tabuleiro()
            temJogo = False
        else:
            if player == 'x':
                player = 'o'
            else:
                player = 'x'


# Definindo o tabuleiro
tabuleiro = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
# Inicia o jogo
jogo()
