import numpy as np

datasetTreino = "./tic-tac-toe-treino.data"
datasetTeste = "./tic-tac-toe-teste.data"

mapa = {
    "x": 1,
    "o": -1,
    "b": 0,
    "X": 1,
    "O": -1,
    "B": 0,
    " ": 0,
}  # Dicionário de mapeamento

mapaEstados = {1: "positive", 2: "negative", 3: "draw", 4: "continue"}


def returnDadosTreino():
    data = np.genfromtxt(datasetTreino, delimiter="\n", dtype=str, encoding=None)

    posicoesTabuleiro = []
    rotulos = []

    # Divide dataset entre posicoes e rotulos
    for linha in data:
        valores = linha.split(",")
        posicoesTabuleiro.append(",".join(valores[:9]))
        rotulos.append(",".join(valores[9:]))

    # Converte os valores x, o e b para valores numericos de acordo com o dicionario definido
    valores_numeros = []
    for entrada in posicoesTabuleiro:
        valores = entrada.split(",")  # Separa os valores da entrada em uma lista
        valores_numeros.append(
            np.array(
                [mapa[x] for x in valores]
            )  # aplica o mapeamento pra cada valor da lista
        )

    posicoesTabuleiroArr = np.array(valores_numeros)
    rotulosArr = np.array(rotulos)

    return posicoesTabuleiroArr, rotulosArr


def returnDadosTeste():
    data = np.genfromtxt(datasetTeste, delimiter="\n", dtype=str, encoding=None)

    posicoesTabuleiro = []
    rotulos = []

    # Divide dataset entre posicoes e rotulos
    for linha in data:
        valores = linha.split(",")
        posicoesTabuleiro.append(",".join(valores[:9]))
        rotulos.append(",".join(valores[9:]))

    # Converte os valores x, o e b para valores numericos de acordo com o dicionario acima
    valores_numeros = []
    for entrada in posicoesTabuleiro:
        valores = entrada.split(",")  # Separa os valores da entrada em uma lista
        valores_numeros.append(
            np.array([mapa[x] for x in valores])
        )  # aplica o mapeamento pra cada valor da lista

    posicoesTabuleiroArr = np.array(valores_numeros)
    rotulosArr = np.array(rotulos)

    return posicoesTabuleiroArr, rotulosArr


def returnMapa():
    return mapa


def returnMapaEstados():
    return mapaEstados


def returnDataSetTreino():
    return datasetTreino


def returnDataSetTeste():
    return datasetTeste
