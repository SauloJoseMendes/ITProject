import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

# funcao para calcular a ocorrencia
def calcular_ocorrencia(fonte, alfabeto):
    ocorrencia = [0] * len(alfabeto)
    ocorrencia_dict = dict(zip(alfabeto, ocorrencia))
    for i in range(len(fonte)):
        ocorrencia_dict[fonte[i]] += 1
    return ocorrencia_dict


def cria_grafico_barra(x, y, eixo_x='X', eixo_y='Y', titulo='Grafico'):
    plt.bar(x, y, color='skyblue')
    plt.xlabel(eixo_x)
    plt.ylabel(eixo_y)
    plt.title(titulo)
    plt.show()


fi = [1, 1, 1, 2, 3]
alfabeto_fi = [1, 2, 3]
cria_grafico_barra(alfabeto_fi, list(calcular_ocorrencia(fi, alfabeto_fi).values()), 'Alfabeto', 'Ocorrencia', 'Histograma')
