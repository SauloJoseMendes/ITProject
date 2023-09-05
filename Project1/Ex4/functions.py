from scipy.io import wavfile
from PIL import Image as img
from huffmancodec import HuffmanCodec
import numpy as np


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


def calcular_variancia(comprimentos, ocorrencia1):
    comprimentos_ar = np.array(comprimentos).astype('float64')
    ocorrencia = np.array(list(ocorrencia1.values())).astype('float64')
    somatorio = np.zeros(len(ocorrencia))
    soma_ocorrencia= np.sum(ocorrencia)
    media_aritmetica_ponderada_soma = np.sum(np.multiply(comprimentos_ar, ocorrencia) / soma_ocorrencia)
    subtracao = np.subtract(comprimentos_ar, media_aritmetica_ponderada_soma)
    np.power(subtracao, 2, subtracao)
    np.multiply(subtracao, ocorrencia, somatorio)
    somatorio_final = np.sum(somatorio) / soma_ocorrencia
    return somatorio_final
    # Feito em Python, ao inves de NumPy
    # media_aritmetica_ponderada1=0
    # for i in range(len(comprimentos)):
    #     media_aritmetica_ponderada1+=(comprimentos[i]*ocorrencia[i])
    # media_aritmetica_ponderada1/=sum(ocorrencia)
    # somatorio = 0
    # for i in range(len(comprimentos)):
    #     somatorio += ocorrencia[i] * ((comprimentos[i] - media_aritmetica_ponderada1) ** 2)
    # somatorio/=sum(ocorrencia)
    # return somatorio



def calcular_n_bits_por_simbolo(alfabeto, li, tamanho_fonte, ocorrencia):
    n_bits_simb = 0
    for i in range(len(alfabeto)):
        n_bits_simb += ocorrencia[alfabeto[i]] * li[i] / tamanho_fonte
    return n_bits_simb


# Funcoes leituras
def ler_bmp(ficheiro):
    imagem = img.open(ficheiro, 'r')
    # RESTRIÇÃO PARA UMA MATRIZ EM FUNÇÃO DA IMAGEM SER EM GRAYSCALE
    data = list(imagem.getdata(0))
    codec = HuffmanCodec.from_data(data)
    alfabeto, li = codec.get_code_len()
    tamanho_fonte = len(data)
    ocorrencia_dict = calcular_ocorrencia(data, alfabeto)
    n_bits = calcular_n_bits_por_simbolo(alfabeto, li, tamanho_fonte, ocorrencia_dict)
    entropia = calcular_entropia(ocorrencia_dict)
    variancia= calcular_variancia(li, ocorrencia_dict)
    return [entropia, n_bits, variancia]


def ler_wav(ficheiro):
    ficheiro_ler = wavfile.read(ficheiro)
    if len(ficheiro_ler[1].shape) > 1:
        ficheiro_left, ficheiro_right = zip(*ficheiro_ler[1])
        freq_s = ficheiro_ler[0]
        ficheiro = [freq_s, ficheiro_left]
    else:
        ficheiro = ficheiro_ler
    codec = HuffmanCodec.from_data(ficheiro[1])
    alfabeto, li = codec.get_code_len()
    tamanho_fonte = len(ficheiro[1])
    ocorrencia_dict = calcular_ocorrencia(ficheiro[1], alfabeto)
    n_bits = calcular_n_bits_por_simbolo(alfabeto, li, tamanho_fonte, ocorrencia_dict)
    entropia = calcular_entropia(ocorrencia_dict)
    variancia= calcular_variancia(li, ocorrencia_dict)
    return [entropia, n_bits, variancia]


def ler_txt(ficheiro):
    f = open(ficheiro, 'r')
    texto = f.read(-1)
    f.close()
    codec = HuffmanCodec.from_data(texto)
    alfabeto, li = codec.get_code_len()
    tamanho_fonte = len(texto)
    ocorrencia = np.zeros(len(alfabeto))
    ocorrencia_dict = dict(zip(alfabeto, ocorrencia))
    for i in range(len(texto)):
        if texto[i] in ocorrencia_dict.keys():
            ocorrencia_dict[texto[i]] += 1
    n_bits = calcular_n_bits_por_simbolo(alfabeto, li, tamanho_fonte, ocorrencia_dict)
    entropia = calcular_entropia(ocorrencia_dict)
    variancia= calcular_variancia(li, ocorrencia_dict)
    return [entropia, n_bits, variancia]
