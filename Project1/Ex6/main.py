from scipy.io import wavfile
import functions as f

# Alínea A
#
# query1 = [2, 6, 4, 10, 5, 9, 5, 8, 0, 8]
# target1 = [6, 8, 9, 7, 2, 4, 9, 9, 4, 9, 1, 4, 8, 0, 1, 2, 2, 6, 3, 2, 0, 7, 4, 9, 5, 4, 8, 5, 2, 7, 8, 0, 7, 4, 8, 5,
#            7, 4, 3, 2, 2, 7, 3, 5, 2, 7, 4, 9, 9, 6]
# #não fiz import do numpy para o main.py, somente para o functions.py
# alfabeto1 = range(11)
# print(f.calcular_info_mutua(query1, target1, alfabeto1,1))



# Alínea B

# Variaveis
# query_saxriff= f.ler_wav('/Users/saulopiccirilo/Downloads/TP1_v2/DATA/MI/saxriff.wav')
# target01_repeat=f.ler_wav('/Users/saulopiccirilo/Downloads/TP1_v2/DATA/MI/target01 - repeat.wav')
# target02_repeat_noise= f.ler_wav('/Users/saulopiccirilo/Downloads/TP1_v2/DATA/MI/target02 - repeatNoise.wav')
# alfabeto_wavfile1= range(256)
# passo_saxriff= (int)(len(query_saxriff[1])/4)
# intervalos_tempo_target_01= f.calcular_intervalos_tempo(1/target01_repeat[0],len(query_saxriff[1]),len(target01_repeat[1]),passo_saxriff)
#
#
# "Info mutua query/target01"
# intervalos_tempo_target_01= f.calcular_intervalos_tempo(1/target01_repeat[0],len(query_saxriff[1]),len(target01_repeat[1]),passo_saxriff)
# info_mutua=f.calcular_info_mutua(query_saxriff[1],target01_repeat[1],alfabeto_wavfile1,passo_saxriff)
# f.cria_grafico_barra(intervalos_tempo_target_01,info_mutua,'t','info_mutua',"Info mutua query/target01")
#
# "Info mutua query/target02"
# intervalos_tempo_target_02= f.calcular_intervalos_tempo(1/target02_repeat_noise[0],len(query_saxriff[1]),len(target02_repeat_noise[1]),passo_saxriff)
# info_mutua=f.calcular_info_mutua(query_saxriff[1],target02_repeat_noise[1],alfabeto_wavfile1,passo_saxriff)
# f.cria_grafico_barra(intervalos_tempo_target_02,info_mutua,'t','info_mutua',"Info mutua query/target01")

# Alinea C

# query_saxriff= f.ler_wav('/Users/saulopiccirilo/Downloads/TP1_v2/DATA/MI/saxriff.wav')
# passo_saxriff= (int)(len(query_saxriff[1])/4)
# for i in range(1,8):
#     i=7
#     musica= f.ler_wav("/Users/saulopiccirilo/Downloads/TP1_v2/DATA/MI/Song0%d.wav"%i)
#     f.identificar_musica("Song%d"%i,musica[0],query_saxriff[1],musica[1],passo_saxriff)
