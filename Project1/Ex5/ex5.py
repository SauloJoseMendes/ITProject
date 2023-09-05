import functions as f
# Exemplo da aula

# fonte= "abadabadoooooooo"
# alfabeto_fonte= 'abdo'
# alfabeto_contiguo= f.criar_alfabeto_contiguo(alfabeto_fonte,alfabeto_fonte)
# fonte_contigua= f.separar_fonte_em_simbolos_contiguos(fonte)
# ocorrencia_contigua= f.calcular_ocorrencia(fonte_contigua,alfabeto_contiguo)
# print(ocorrencia_contigua, f.calcular_entropia(ocorrencia_contigua))


# Reproduzir o Ex3 como se fossem contíguos

landscape = f.ler_bmp('/Users/saulopiccirilo/Downloads/TP1_v2/DATA/landscape.bmp', contiguo=True)
mri = f.ler_bmp('/Users/saulopiccirilo/Downloads/TP1_v2/DATA/MRI.bmp', contiguo=True)
mri_bin = f.ler_bmp('/Users/saulopiccirilo/Downloads/TP1_v2/DATA/MRIbin.bmp', contiguo=True)
soundMono = f.ler_wav('/Users/saulopiccirilo/Downloads/TP1_v2/DATA/soundMono.wav', contiguo=True)
lyrics = f.ler_txt('/Users/saulopiccirilo/Downloads/TP1_v2/DATA/lyrics.txt', contiguo=True)
print(landscape[2])
print(mri[2])
print(mri_bin[2])
print(soundMono[2])
print(lyrics[2])
