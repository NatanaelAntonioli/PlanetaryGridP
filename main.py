import matplotlib.pyplot as plt
import geopy.distance
from geopy import distance
from geopy.distance import geodesic as distance
import math
import random

cortar_lista = False


def bear(latA, lonA, latB, lonB):
    # BEAR Finds the bearing from one lat / lon point to another.
    return math.atan2(
        math.sin(lonB - lonA) * math.cos(latB),
        math.cos(latA) * math.sin(latB) - math.sin(latA) * math.cos(latB) * math.cos(lonB - lonA)
    )


def pointToLineDistance(lon1, lat1, lon2, lat2, lon3, lat3):
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lat3 = math.radians(lat3)
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)
    lon3 = math.radians(lon3)
    R = 6378137

    bear12 = bear(lat1, lon1, lat2, lon2)
    bear13 = bear(lat1, lon1, lat3, lon3)
    dis13 = distance((lat1, lon1), (lat3, lon3)).meters

    # Is relative bearing obtuse?
    if math.fabs(bear13 - bear12) > (math.pi / 2):
        return dis13

    # Find the cross-track distance.
    dxt = math.asin(math.sin(dis13 / R) * math.sin(bear13 - bear12)) * R

    # Is p4 beyond the arc?
    dis12 = distance((lat1, lon1), (lat2, lon2)).meters
    dis14 = math.acos(math.cos(dis13 / R) / math.cos(dxt / R)) * R
    if dis14 > dis12:
        return distance((lat2, lon2), (lat3, lon3)).meters
    return math.fabs(dxt)


def dist_pontos(A, B):
    return geopy.distance.geodesic(A, B).km


def fill_lista(file):
    list = []
    with open(file) as fp:
        for line in fp:
            if "coordinates" in line:
                lon = next(fp)
                lat = next((fp))

                lon = lon.replace(' ', '')
                lon = lon.replace(',', '')
                lon = lon.replace("\n", '')

                lat = lat.replace(' ', '')
                lat = lat.replace("\n", '')

                try:
                    lat = float(lat)
                    lon = float(lon)
                    list.append([lat, lon])
                except:
                    print("Erro em " + str(lat) + " se isso não é coordenada, ignore...")
                    print("Erro em " + str(lon) + " se isso não é coordenada, ignore...")
                    print("------------")

        if cortar_lista:
            while len(list) != 1000:
                list.pop(random.randrange(len(list)))

        return list


def fill_grid():
    list = []
    with open("grid.txt") as fp:
        for line in fp:
            line = line.replace("\n", "")
            line = line.replace(" ", "")
            pos = line.find(",")
            lat = line[:pos]
            lon = line[pos:]
            lon = lon.replace(",", "")
            coord = (float(lat), float(lon))
            list.append(coord)

    return list


def fill_pares():
    list = []
    with open("pares.txt") as fp:
        for line in fp:
            line = line.replace("\n", "")
            line = line.replace(" ", "")
            pos = line.find(",")
            a = line[:pos]
            b = line[pos:]
            b = b.replace(",", "")
            par = (int(a) - 1, int(b) - 1)
            list.append(par)
    return list


def populate_world_with_grid(lista_grid):
    fig, ax = plt.subplots()
    ratio = 1.0
    x_left, x_right = ax.get_xlim()
    y_low, y_high = ax.get_ylim()
    ax.set_aspect(abs((x_right - x_left) / (y_low - y_high)) * ratio)

    for ponto in lista_grid:
        plt.plot(ponto[1], ponto[0], marker=".", color="k", markersize=2)
        ax.annotate(str(lista_grid.index(ponto) + 1), xy=(ponto[1], ponto[0]))


def populate_world_with_lines(lista_pontos, lista_pares):
    for par in lista_pares:
        pontoA = lista_pontos[par[0]]
        pontoB = lista_pontos[par[1]]

        plt.plot([pontoA[1], pontoB[1]], [pontoA[0], pontoB[0]], color='k', linestyle='-', linewidth=0.4)


def populate_world_with_dots(lista_pontos):
    for ponto in lista_pontos:
        plt.plot(ponto[1], ponto[0], marker=".", color="b", markersize=2)


def get_menor_distancia_reta(lista_retas, lista_pontos, ponto):
    menor = 9999999
    for candidato in lista_retas:

        pA = lista_pontos[candidato[0]]
        pB = lista_pontos[candidato[1]]
        distancia = pointToLineDistance(pA[0], pA[1], pB[0], pB[1], ponto[0], ponto[1])
        # print((candidato[0]+1, candidato[1] + 1), distancia)
        if distancia < menor:
            menor = distancia
    return menor/1000


def get_score_grid_pontos(lista_pontos, lista_retas, lista_grid):
    score = 0
    total = len(lista_pontos)
    atual = 0
    for ponto in lista_pontos:
        dist = get_menor_distancia_reta(lista_retas, lista_grid, ponto)
        print("Concluido: " + str(atual / total * 100) + "% - " + str(dist))
        score = score + dist
        atual = atual + 1
    return score


lista_grid = fill_grid()
lista_pares = fill_pares()
lista_mundo = fill_lista("world_sites.txt")


print("0 - Gerar mapa com grade")
print("1 - Gerar mapa com coordenadas e grade")
print("2 - Testar pontuação de conjunto de coordenadas")
acao = int(input("O que deseja fazer? "))


if acao == 0:

    populate_world_with_grid(lista_grid)
    populate_world_with_lines(lista_grid, lista_pares)
    plt.show()

if acao == 1:

    populate_world_with_grid(lista_grid)
    populate_world_with_lines(lista_grid, lista_pares)
    populate_world_with_dots(lista_mundo)
    plt.show()

if acao == 2:
    print(len(lista_mundo))
    print(get_score_grid_pontos(lista_mundo, lista_pares, lista_grid))


print("----------")
#print(len(lista_mundo))
#print(get_score_grid_pontos(lista_mundo, lista_pares, lista_grid))

#plt.show()
