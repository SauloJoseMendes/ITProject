import numpy as np
from PIL import Image as img
from scipy.io import wavfile


# Calcular
def calcular_ocorrencia(fonte, alfabeto):
    ocorrencia = np.zeros(len(alfabeto))
    ocorrencia_dict = dict(zip(alfabeto, ocorrencia))
    for i in range(len(fonte)):
        ocorrencia_dict[fonte[i]] += 1
    return ocorrencia_dict


def calcular_entropia(ocorrencia1):
    ocorrencia = np.array(list(ocorrencia1.values()))
    tamanho_da_fonte = np.sum(ocorrencia)
    probabilidade = np.zeros(len(ocorrencia))
    np.divide(ocorrencia, tamanho_da_fonte, probabilidade, where=ocorrencia != 0)
    entropia_individual1 = np.zeros(len(ocorrencia))
    prob_inverso = np.zeros(len(ocorrencia))
    prob_log = np.zeros(len(ocorrencia))
    np.divide(1, probabilidade, prob_inverso, where=probabilidade != 0)
    np.log2(prob_inverso, prob_log, where=prob_inverso != 0)
    np.multiply(probabilidade, prob_log, entropia_individual1, where=probabilidade != 0)
    sum_numpy = np.sum(entropia_individual1)
    return sum_numpy
    # Feito atraves do Python, ao inves do Numpy:
    # entropia_individual = [0] * len(ocorrencia)
    # for i in range(len(probabilidade)):
    #     if probabilidade[i] != 0:
    #         entropia_individual[i] = probabilidade[i] * math.log(1 / probabilidade[i], 2)
    # sum_pyt= sum(entropia_individual)



def separar_fonte_em_simbolos_contiguos(fonte):
    fonte_nova = []
    for i in range(int(len(fonte) / 2)):
        fonte_nova.append(str(fonte[i * 2]) + ',' + str(fonte[(i * 2) + 1]))
    return fonte_nova


def criar_alfabeto_contiguo(alfabeto_x, alfabeto_y):
    alfabeto_condicionado = []
    for i in alfabeto_x:
        for k in alfabeto_y:
            alfabeto_condicionado.append(str(i) + "," + str(k))
    return alfabeto_condicionado


# Funcoes leituras
def ler_bmp(ficheiro, contiguo=False):
    imagem = img.open(ficheiro, 'r')
    # RESTRIÇÃO PARA UMA MATRIZ EM FUNÇÃO DA IMAGEM SER EM GRAYSCALE
    data = list(imagem.getdata(0))
    alfabeto = np.arange(256)
    if contiguo:
        data = separar_fonte_em_simbolos_contiguos(data)
        alfabeto = criar_alfabeto_contiguo(alfabeto, alfabeto)
    ocorrencia_img = calcular_ocorrencia(data, alfabeto)
    calcular_entropia(ocorrencia_img)
    return [data, list(ocorrencia_img.values()), calcular_entropia(ocorrencia_img)/2]


def ler_wav(ficheiro, contiguo=False):
    [fs, data] = wavfile.read(ficheiro)
    n_canais = len(data.shape)
    n_bits_quantizar = n_canais * 8
    alfabeto = [str(i) for i in range(2 ** n_bits_quantizar)]
    if contiguo:
        data = separar_fonte_em_simbolos_contiguos(data)
        alfabeto = criar_alfabeto_contiguo(alfabeto, alfabeto)
    ocorrencia = calcular_ocorrencia(data, alfabeto)
    return [[fs, data], list(ocorrencia.values()), calcular_entropia(ocorrencia)/2]


def ler_txt(ficheiro, contiguo=False):
    f = open(ficheiro, 'r')
    alfabeto = list()
    for i in range(ord('A'), ord('Z') + 1):
        alfabeto.append(chr(i))
    for i in range(ord('a'), ord('z') + 1):
        alfabeto.append(chr(i))
    texto = f.read(-1)
    f.close()
    if contiguo:
        texto = separar_fonte_em_simbolos_contiguos(texto)
        alfabeto = criar_alfabeto_contiguo(alfabeto, alfabeto)
    ocorrencia = np.arange(len(alfabeto))
    ocorrencia_dict = dict(zip(alfabeto, ocorrencia))
    for i in range(len(texto)):
        if texto[i] in ocorrencia_dict.keys():
            ocorrencia_dict[texto[i]] += 1
    return [texto, list(ocorrencia_dict.values()), calcular_entropia(ocorrencia_dict)/2]
