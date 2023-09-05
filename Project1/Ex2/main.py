import numpy as np


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
    ocorrencia = [0] * len(alfabeto)
    ocorrencia_dict = dict(zip(alfabeto, ocorrencia))
    for i in range(len(fonte)):
        ocorrencia_dict[fonte[i]] += 1
    return ocorrencia_dict


fi = "abadabadoooooooo"
alfabeto_fi = 'abdo'
ocorrencia_fi = calcular_ocorrencia(fi, alfabeto_fi)
entropia_fi = calcular_entropia(ocorrencia_fi)
print(ocorrencia_fi, entropia_fi)
