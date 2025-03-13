import random

chutar = []

chutes = []
respostas = []
words = None

def pensar():
    """
    Essa função é chamada antes de chutar_palavra
    pode utiliza-la para computar uma estratégia de chute
    """
    global chutar, words
    if words is None:
        with open("palavras.txt", "r", encoding="utf-8") as file:
            words = [line.strip().upper() for line in file.readlines() if len(line.strip()) == 5]
            #words = ["abaco"]

    # Escolher uma palavra aleatória
    chutar.append(random.choice(words))
    print(chutar)
    


def chutar_palavra():
    """
    Essa função é chamada para chutar uma palavra.
    Se retornado None, nenhum chute é executado.
    Retorne uma string para chutar uma palavra.
    """
    global chutar, chutes
    
    if len(chutar) > 0:
        chute = chutar.pop(0)
        chutes.append(chute)
        return chute
    else:
        return None
    
def retorno(resposta):
    """
    
    """
    global respostas
    print(resposta)
    respostas.append(resposta)