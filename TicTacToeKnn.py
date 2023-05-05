#pip install -U scikit-learn

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

atualizaDataset = False
caminhoDataset = './tic-tac-toe.data'


# -- CARREGAMENTO E MODIFICACOES DO DATASET ----------------------------------------------------------------------
data = np.genfromtxt(caminhoDataset, delimiter='\n', dtype=str, encoding=None)

dadosTabuleiro = []
dadosClassificaco = []

for linha in data:
    valores = linha.split(',')
    dadosTabuleiro.append(','.join(valores[:9]))
    dadosClassificaco.append(','.join(valores[9:]))

mapa = {'x': 1, 'o': -1, 'b': 0, 'X': 1, 'O': -1, 'B': 0} # Dicionário de mapeamento

valores_numeros = []
for entrada in dadosTabuleiro:
    valores = entrada.split(',') # Separa os valores da entrada em uma lista
    valores_numeros.append(np.array([mapa[x] for x in valores])) # aplica o mapeamento pra cada valor da lista

dadosTabuleiroArr = np.array(valores_numeros)
dadosClassificacoArr = np.array(dadosClassificaco)

# - KNN --------------------------------------------------------------------------------------------
knn = KNeighborsClassifier(n_neighbors=3, metric='euclidean') # Define o algoritmo knn usando k=3
knn.fit(dadosTabuleiroArr, dadosClassificacoArr) # Treina o algoritmo
# --------------------------------------------------------------------------------------------------

def verifica_acabou(tabuleiroAtual):

    print("tabuleiroAtual: ")
    print(tabuleiroAtual)
    imprime_tabuleiro()

    entradaConvertida = [mapa[x] for x in tabuleiroAtual.replace(',', '')] #traduz X para 1, O para -1 e b para 0
    prediction = knn.predict(np.array(entradaConvertida).reshape(1,-1)) # Classifica o teste com base no treinamento

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

    #recebe feedback a cada jogada para verificar se o resultado foi correto
    if atualizaDataset:
        resposta = 'a'
        while resposta != 'y' and resposta != 'n':
            resposta = input("Foi o resultado correto? (y/n): ")
            if (resposta == 'N' or resposta == 'n'): 
                gravar = input ("Digite o resultado esperado para ser gravado: ")
                gravar = tabuleiroAtual + ',' + gravar
                
                with open(caminhoDataset, 'r') as f:
                    conteudo = f.readlines() #armazena todo dataset para evitar jogada repetida
                
                #adiciona a combinacao da jogada somente se ela nao existe previamente no dataset
                if tabuleiroAtual+",positive\n" not in conteudo and \
                    tabuleiroAtual+",negative\n" not in conteudo and \
                    tabuleiroAtual+",draw\n" not in conteudo and \
                    tabuleiroAtual+",continue\n" not in conteudo :
                    arquivo = open(caminhoDataset, "a")
                    arquivo.write("\n")
                    arquivo.write(gravar)
                    arquivo.close()
                print("tabuleiroAtual: ")
                print(tabuleiroAtual)

    #print("\nVitoria de X!\n" if prediction == "positive" else "\nJogo acabou!\n")
    #return (True if prediction == "negative" else False)
    return False if 0 in entradaConvertida else True

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

        # Verifica se houve vencedor, se nao passa a vez para o próximo jogador
        if verifica_acabou((",".join([elem.strip() if elem.strip() != '' else 'b' for elem in tabuleiro]))):
            imprime_tabuleiro()
            jogando = False
        else: 
            if jogador_atual == 'x':
                jogador_atual = 'o'
            else:
                jogador_atual = 'x'


# Definindo o tabuleiro
tabuleiro = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
# Inicia o jogo
jogo_da_velha()
