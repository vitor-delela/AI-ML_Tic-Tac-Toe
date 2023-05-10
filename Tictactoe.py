from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import numpy as np
from BayesianAlgorithm import BayesianAlgorithm
from KnnAlgorithm import KnnAlgorithm
from MlpAlgorithm import MlpAlgorithm
from Utils import returnMapa, returnDataSetTreino, returnMapaEstados

root = Tk()
root.title("Jogo da velha")
root.iconbitmap()


datasetTreino = returnDataSetTreino()

mapa = returnMapa()
mapaEstados = returnMapaEstados()

knn, knn_accuracy = KnnAlgorithm()
mlp, mlp_accuracy = MlpAlgorithm()
bayesian, bayesian_accuracy = BayesianAlgorithm()


def accuracy():
    messagebox.showinfo(
        "Jogo da velha",
        "Precisão do algoritmo KNN: {:.2f}%\n".format(knn_accuracy * 100)
        + "Precisão do algoritmo MLP: {:.2f}%\n".format(mlp_accuracy * 100)
        + "Precisão do algoritmo Bayesian: {:.2f}%".format(bayesian_accuracy * 100),
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
    # print("BAYESIANO: ", type(algoritmo) is GaussianNB)

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
        + "3 - BAYESIANO\n",
    )

    if alg == None:
        return
    elif int(alg) == 1:
        algoritmo = knn
    elif int(alg) == 2:
        algoritmo = mlp
    elif int(alg) == 3:
        algoritmo = bayesian
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

selecionarAlgoritmo()
treinarAlgoritmo()
reiniciar()

root.mainloop()
