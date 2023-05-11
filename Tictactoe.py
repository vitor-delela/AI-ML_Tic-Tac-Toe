from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import numpy as np
import matplotlib.pyplot as plt
from BayesianAlgorithm import BayesianAlgorithm
from KnnAlgorithm import KnnAlgorithm
from MlpAlgorithm import MlpAlgorithm
from Utils import returnDadosTeste, returnMapa, returnDataSetTreino, returnMapaEstados
from DecisionTreeAlgorithm import DecisionTreeAlgorithm
from Utils import returnMapa, returnDataSetTreino, returnMapaEstados
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier


root = Tk()
root.title("Jogo da velha")
root.iconbitmap()


datasetTreino = returnDataSetTreino()

mapa = returnMapa()
mapaEstados = returnMapaEstados()
decisionTree, decisionTree_accuracy = DecisionTreeAlgorithm()
knn, knn_accuracy = KnnAlgorithm()
mlp, mlp_accuracy = MlpAlgorithm()

bayesian, bayesian_accuracy = BayesianAlgorithm()


def accuracy():
    messagebox.showinfo(
        "Jogo da velha",
        "Precisão do algoritmo KNN: {:.2f}%\n".format(knn_accuracy * 100)
        + "Precisão do algoritmo MLP: {:.2f}%\n".format(mlp_accuracy * 100)
        + "Precisão do algoritmo Bayesian: {:.2f}%\n".format(bayesian_accuracy * 100)
        + "Precisão do algoritmo Decision Tree: {:.2f}%".format(decisionTree_accuracy * 100),
    )


def desabilitarCampos():
    b1.config(state=DISABLED)
    b2.config(state=DISABLED)
    b3.config(state=DISABLED)

    b4.config(state=DISABLED)
    b5.config(state=DISABLED)
    b6.config(state=DISABLED)

    b7.config(state=DISABLED)
    b8.config(state=DISABLED)
    b9.config(state=DISABLED)


def verficaResposta():
    global answer
    global erros, acertos
    erros = 0
    acertos = 0
    answer = messagebox.askquestion("Jogo da velha", "Resultado correto?")

    if answer == "no":
        erros += 1
        aprendeDataSet()

    if answer == "yes" and winner == True:
        acertos += 1
        desabilitarCampos()


def verificaVencedor():
    global winner
    winner = False

    global tabuleiro
    tabuleiro = [
        b1["text"],
        b2["text"],
        b3["text"],
        b4["text"],
        b5["text"],
        b6["text"],
        b7["text"],
        b8["text"],
        b9["text"],
    ]

    entradaConvertida = [mapa[x] for x in tabuleiro]

    if count == 9:
        desabilitarCampos()
    prediction = algoritmo.predict(np.array(entradaConvertida).reshape(1, -1))

    # print("KNN: ", type(algoritmo) is KNeighborsClassifier)
    # print("MLP: ", type(algoritmo) is MLPClassifier)
    # print("BAYESIANO: ", type(algoritmo) is BernoulliNB)
    # print("Decision Tree: ", type(algoritmo) is DecisionTreeClassifier)


    if prediction == "positive":
        winner = True
        messagebox.showinfo("Jogo da velha", "Vitoria de X!")
        if aprendeDataset is False:
            return
        else:
            verficaResposta()
    elif prediction == "negative":
        winner = True
        messagebox.showinfo("Jogo da velha", "Vitoria de O!")
        if aprendeDataset is False:
            return
        else:
            verficaResposta()
    elif prediction == "draw":
        winner = True
        messagebox.showinfo("Jogo da velha", "Empate!")
        if aprendeDataset is False:
            return
        else:
            verficaResposta()
    elif prediction == "continue":
        winner = False
        messagebox.showinfo("Jogo da velha", "Ainda tem jogo!")
        if aprendeDataset is False:
            return
        else:
            verficaResposta()
    else:
        messagebox.showerror("\nErro na leitura dos resultados!\n")


def b_click(b):
    global clicked, count

    if b["text"] == " " and clicked == True:
        b["text"] = "X"
        verificaVencedor()
        clicked = False
        count += 1
    elif b["text"] == " " and clicked == False:
        b["text"] = "O"
        verificaVencedor()
        clicked = True
        count += 1
    else:
        messagebox.showerror("Jogo da velha", "Campo já preenchido, selecione outro.")


def aprendeDataSet():
    correcao = simpledialog.askinteger(
        title="Correção Saída",
        prompt="Saída correta:\n"
        + "1 - vitória de X: \n"
        + "2 - vitória de O\n"
        + "3 - Empate\n"
        + "4 - Segue o Jogo",
    )
    resposta = mapaEstados[int(correcao)]
    gravar = ""
    array = []

    for posicao in tabuleiro:
        posicao
        if posicao == "X" or posicao == "O":
            array.append(posicao.lower())
        else:
            array.append("b")

    gravar = ",".join(array)
    gravar = gravar + "," + resposta

    with open(datasetTreino, "r") as f:
        conteudo = f.readlines()  # armazena todo dataset para evitar jogada repetida
        tabuleiroAtual = ",".join(array)

        # adiciona a combinacao da jogada somente se ela nao existe previamente no dataset
        if (
            tabuleiroAtual + ",positive\n" not in conteudo
            and tabuleiroAtual + ",negative\n" not in conteudo
            and tabuleiroAtual + ",draw\n" not in conteudo
            and tabuleiroAtual + ",continue\n" not in conteudo
        ):
            arquivo = open(datasetTreino, "a")
            arquivo.write("\n")
            arquivo.write(gravar)
            arquivo.close()
            print("tabuleiroAtual:\n {:s}", tabuleiroAtual)


def selecionarAlgoritmo():
    global algoritmo

    alg = simpledialog.askinteger(
        title="Jogo da velha",
        prompt="Selecione o algoritmo:\n"
        + "1 - KNN: \n"
        + "2 - MLP\n"
        + "3 - BAYESIANO\n"
        + "4 - DecisionTree\n",
    )

    if alg == None:
        return
    elif int(alg) == 1:
        algoritmo = knn
    elif int(alg) == 2:
        algoritmo = mlp
    elif int(alg) == 3:
        algoritmo = bayesian
    elif int(alg) == 4:
        algoritmo = decisionTree
    else:
        return


def treinarAlgoritmo():
    global aprendeDataset

    ret = simpledialog.askinteger(
        title="Jogo da velha",
        prompt="Treinar Algoritmo?:\n" + "1 - SIM: \n" + "2 - NÃO",
    )

    if ret == None:
        return
    elif int(ret) == 1:
        aprendeDataset = True
    elif int(ret) == 2:
        aprendeDataset = False
    else:
        return


def reiniciar():
    global b1, b2, b3, b4, b5, b6, b7, b8, b9
    global clicked, count
    clicked = True
    count = 0

    b1 = Button(
        root,
        text=" ",
        font=("Helvetica", 20),
        height=3,
        width=6,
        bg="SystemButtonFace",
        command=lambda: b_click(b1),
    )
    b2 = Button(
        root,
        text=" ",
        font=("Helvetica", 20),
        height=3,
        width=6,
        bg="SystemButtonFace",
        command=lambda: b_click(b2),
    )
    b3 = Button(
        root,
        text=" ",
        font=("Helvetica", 20),
        height=3,
        width=6,
        bg="SystemButtonFace",
        command=lambda: b_click(b3),
    )

    b4 = Button(
        root,
        text=" ",
        font=("Helvetica", 20),
        height=3,
        width=6,
        bg="SystemButtonFace",
        command=lambda: b_click(b4),
    )
    b5 = Button(
        root,
        text=" ",
        font=("Helvetica", 20),
        height=3,
        width=6,
        bg="SystemButtonFace",
        command=lambda: b_click(b5),
    )
    b6 = Button(
        root,
        text=" ",
        font=("Helvetica", 20),
        height=3,
        width=6,
        bg="SystemButtonFace",
        command=lambda: b_click(b6),
    )

    b7 = Button(
        root,
        text=" ",
        font=("Helvetica", 20),
        height=3,
        width=6,
        bg="SystemButtonFace",
        command=lambda: b_click(b7),
    )
    b8 = Button(
        root,
        text=" ",
        font=("Helvetica", 20),
        height=3,
        width=6,
        bg="SystemButtonFace",
        command=lambda: b_click(b8),
    )
    b9 = Button(
        root,
        text=" ",
        font=("Helvetica", 20),
        height=3,
        width=6,
        bg="SystemButtonFace",
        command=lambda: b_click(b9),
    )

    b1.grid(row=0, column=0)
    b2.grid(row=0, column=1)
    b3.grid(row=0, column=2)

    b4.grid(row=1, column=0)
    b5.grid(row=1, column=1)
    b6.grid(row=1, column=2)

    b7.grid(row=2, column=0)
    b8.grid(row=2, column=1)
    b9.grid(row=2, column=2)


def plotGrafic():
    (testePosicoes, testeRotulos) = returnDadosTeste()
    retKnn = []
    retMlp = []
    retBay = []
    retDT = []
    real = []

    for p in testePosicoes:
        aux1 = knn.predict(np.array(p).reshape(1, -1))
        retKnn.append(aux1[0])
        aux2 = mlp.predict(np.array(p).reshape(1, -1))
        retMlp.append(aux2[0])
        aux3 = bayesian.predict(np.array(p).reshape(1, -1))
        retBay.append(aux3[0])
        aux4 = decisionTree.predict(np.array(p).reshape(1, -1))
        retDT.append(aux3[0])

    for r in testeRotulos:
        real.append(r)

    BayAccuracy = bayesian.score(testePosicoes, testeRotulos)
    knnAccuracy = knn.score(testePosicoes, testeRotulos)
    MlpAccuracy = mlp.score(testePosicoes, testeRotulos)
    DTreeAccuracy = decisionTree.score(testePosicoes, testeRotulos)

    jogadas = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "40",
        "41",
        "42",
        "43",
        "4",
        "45",
        "46",
        "47",
        "48",
        "49",
        "50",
        "51",
        "52",
    ]

    print("arr", len(jogadas))
    print("arr", jogadas)
    print("knn", len(retKnn))
    print("knn", retKnn)
    print("mlp", len(retMlp))
    print("mlp", retMlp)
    print("bayesian", len(retBay))
    print("bayesian", retBay)
    print("real", len(real))
    print("real", real)

    plt.plot(jogadas, real, alpha=0.5, label="REAIS")
    plt.plot(jogadas, retKnn, alpha=0.5, label="KNN")
    plt.plot(jogadas, retMlp, alpha=0.5, label="MLP")
    plt.plot(jogadas, retBay, alpha=0.5, label="BAY")
    plt.plot(jogadas, retDT, alpha=0.5, label="DET")
    plt.xlabel("Jogada")
    plt.ylabel("Resultado")
    plt.title("Comparação dos algoritmos com o resultado real")
    plt.legend(loc=1)
    plt.show()


menu = Menu(root)
root.config(menu=menu)

options = Menu(menu, tearoff=False)
algorithm = Menu(menu, tearoff=False)
menu.add_cascade(label="Opções", menu=options)
menu.add_cascade(label="Algoritmos", menu=algorithm)
options.add_command(label="Reiniciar", command=reiniciar)
options.add_command(label="Treinar Algoritmo", command=treinarAlgoritmo)
algorithm.add_command(label="Precisão do algoritmo", command=accuracy)
algorithm.add_command(label="Selecionar Algoritmo", command=selecionarAlgoritmo)
algorithm.add_command(label="Plot", command=plotGrafic)

selecionarAlgoritmo()
treinarAlgoritmo()
reiniciar()

root.mainloop()
