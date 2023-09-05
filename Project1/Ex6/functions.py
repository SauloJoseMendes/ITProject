# import math
from scipy.io import wavfile
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('TkAgg')


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
    # Feito atraves do Python, ao inves do Numpy:
    # entropia_individual = [0] * len(ocorrencia)
    # for i in range(len(probabilidade)):
    #     if probabilidade[i] != 0:
    #         entropia_individual[i] = probabilidade[i] * math.log(1 / probabilidade[i], 2)
    # sum_pyt= sum(entropia_individual)
    sum_numpy = np.sum(entropia_individual1)
    return sum_numpy


def calcular_ocorrencia(fonte, alfabeto):
    ocorrencia = [0] * len(alfabeto)
    ocorrencia_dict = dict(zip(alfabeto, ocorrencia))
    for i in range(len(fonte)):
        ocorrencia_dict[fonte[i]] += 1
    return ocorrencia_dict


def calcular_info_mutua(query, target, alfabeto, passo):
    info_mutua = []
    ocorrencia_query = calcular_ocorrencia(query, alfabeto)
    entropia_query = calcular_entropia(ocorrencia_query)
    alfabeto_condicionado = criar_alfabeto_condicionado(alfabeto, alfabeto)
    for i in range(int(((len(target) - len(query)) / passo) + 1)):
        target_window = target[passo * i:passo * i + len(query)]
        ocorrencia_window = calcular_ocorrencia(target_window, alfabeto)
        entropia_window = calcular_entropia(ocorrencia_window)
        ocorrencia_condicionada = calcular_ocorrencia_condicionada(query, target_window, alfabeto_condicionado)
        entropia_window_e_query = calcular_entropia(ocorrencia_condicionada)
        entropia_condicionada = entropia_query + entropia_window - entropia_window_e_query
        info_mutua.append(entropia_condicionada)
    return info_mutua


def criar_alfabeto_condicionado(alfabeto_x, alfabeto_y):
    alfabeto_condicionado = []
    for i in alfabeto_x:
        for k in alfabeto_y:
            alfabeto_condicionado.append(str(i) + ',' + str(k))
    return alfabeto_condicionado


def calcular_ocorrencia_condicionada(fonte_x, fonte_y, alfabeto_condicionado):
    ocorrencia = np.zeros(len(alfabeto_condicionado))
    ocorrencia_dict = dict(zip(alfabeto_condicionado, ocorrencia))
    for i in range(len(fonte_y)):
        ocorrencia_dict[str(fonte_x[i]) + ',' + str(fonte_y[i])] += 1
    return ocorrencia_dict


def cria_grafico(x, y, eixo_x='X', eixo_y='Y', titulo='Grafico'):
    plt.plot(x, y, 'ro')
    plt.xlabel(eixo_x)
    plt.ylabel(eixo_y)
    plt.title(titulo)
    plt.show()


def cria_grafico_barra(x, y, eixo_x='X', eixo_y='Y', titulo='Grafico'):
    plt.bar(x, y)
    plt.xlabel(eixo_x)
    plt.ylabel(eixo_y)
    plt.title(titulo)
    plt.show()


def calcular_intervalos_tempo(t, query_size, target_size, passo):
    intervalos_tempo = [t * (i * passo) for i in range(int(((target_size - query_size) / passo) + 1))]
    return intervalos_tempo


def identificar_musica(nome, f_s, query, target, passo):
    alfabeto = np.arange(256)
    info_mutua = calcular_info_mutua(query, target, alfabeto, passo)
    tempo = calcular_intervalos_tempo(1 / f_s, len(query), len(target), passo)
    cria_grafico(tempo, info_mutua, 't', 'infomutua', nome)
    info_mutua.sort(reverse=True)
    print("Musica:\t%s\nInfo Mutua:\t" % nome, info_mutua, "\nInfo Mutua Maxima:\t%.4f" % (info_mutua[0]))


# Funcoes de leitura

def ler_wav(ficheiro):
    ficheiro_ler = wavfile.read(ficheiro)
    if len(ficheiro_ler[1].shape) > 1:
        ficheiro_left, ficheiro_right = zip(*ficheiro_ler[1])
        freq_s = ficheiro_ler[0]
        return [freq_s, ficheiro_left]
    else:
        return ficheiro_ler
