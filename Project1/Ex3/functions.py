import matplotlib
from scipy.io import wavfile
from PIL import Image as img
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('TkAgg')


# Funcoes calculos
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


def calcular_ocorrencia(fonte, alfabeto):
    ocorrencia = np.zeros(len(alfabeto))
    ocorrencia_dict = dict(zip(alfabeto, ocorrencia))
    for i in range(len(fonte)):
        ocorrencia_dict[fonte[i]] += 1
    return ocorrencia_dict


# Funcoes leituras
def ler_bmp(ficheiro):
    imagem = img.open(ficheiro, 'r')
    # RESTRIÇÃO PARA UMA MATRIZ EM FUNÇÃO DA IMAGEM SER EM GRAYSCALE
    data = list(imagem.getdata(0))
    alfabeto = np.arange(256)
    ocorrencia_img = calcular_ocorrencia(data, alfabeto)
    calcular_entropia(ocorrencia_img)
    return [data, alfabeto, list(ocorrencia_img.values()), calcular_entropia(ocorrencia_img)]


def ler_wav(ficheiro):
    [fs, data] = wavfile.read(ficheiro)
    n_canais = len(data.shape)
    n_bits_quantizar = n_canais * 8
    alfabeto = np.arange(2 ** n_bits_quantizar)
    ocorrencia = calcular_ocorrencia(data, alfabeto)
    return [[fs, data],alfabeto, list(ocorrencia.values()), calcular_entropia(ocorrencia)]


def ler_txt(ficheiro):
    f = open(ficheiro, 'r')
    alfabeto = list()
    for i in range(ord('A'), ord('Z') + 1):
        alfabeto.append(chr(i))
    for i in range(ord('a'), ord('z') + 1):
        alfabeto.append(chr(i))
    texto = f.read(-1)
    f.close()
    ocorrencia = np.zeros(len(alfabeto))
    ocorrencia_dict = dict(zip(alfabeto, ocorrencia))
    for i in range(len(texto)):
        if texto[i] in ocorrencia_dict.keys():
            ocorrencia_dict[texto[i]] += 1
    return [texto, alfabeto, list(ocorrencia_dict.values()), calcular_entropia(ocorrencia_dict)]


# Funcoes graficas

def cria_grafico_barra(x, y, eixo_x='X', eixo_y='Y', titulo='Grafico'):
    plt.bar(x, y, color='skyblue')
    plt.xlabel(eixo_x)
    plt.ylabel(eixo_y)
    plt.title(titulo)
    plt.show()

def cria_grafico(x, y, eixo_x='X', eixo_y='Y', titulo='Grafico'):
    plt.plot(x, y, 'ro')
    plt.xlabel(eixo_x)
    plt.ylabel(eixo_y)
    plt.title(titulo)
    plt.show()
