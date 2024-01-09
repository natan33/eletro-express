from random import randint


def gerar_cod_barra():
    numeros = []
    for c in range(12):
        i = randint(0, 9)
        numeros.append(i)

    cod_barra = str(numeros).replace(",", "")

    return cod_barra.replace("[","").replace("]", "")