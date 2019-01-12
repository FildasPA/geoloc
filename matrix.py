#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Implémentation d'une matrice. Permet de récupérer les informations par ligne
ou par colonne. Dispose également d'une fonction 'get_nearest' permettant de
récupérer l'entrée la plus similaire à une autre envoyée en paramètres."""

class Matrix:
    def __init__(self, columns=[]):
        """Initialise les entrées et les colonnes de la matrice"""
        self.matrix = []
        self.columns = columns


    def __str__(self):
        """Retourne la matrice au format texte"""
        s = ''
        for i, row in enumerate(self.matrix):
            d = {}
            for j, key in enumerate(self.columns):
                d[key] = row[j]
            s += str(i)+': '+str(d)+'\n'
        return s


    def append(self, row):
        """Insère une nouvelle entrée dans la matrice"""
        values = []
        for key in self.columns:
            if key in row:
                values.append(row[key])
            else:
                values.append(0)

        self.matrix.append(values)


    def get(self, columns=None, index=None):
        """Récupère les informations par colonnes et/ou par lignes.
        Si columns est nulle, renvoie toutes les colonnes.
        Si index est nulle, renvoie toutes les lignes."""
        result = []
        for i, row in enumerate(self.matrix):
            if index is not None and i not in index:
                continue
            rrow = {}
            for j, column in enumerate(self.columns):
                if columns is None or column in columns or j in columns:
                   rrow[column] = row[j]
            result.append(rrow)

        return result


    def __getitem__(self, o):
        """Retourne une entrée de la matrice selon le type de o :
        - si o est un texte, retourne la colonne correspondante
        - si o est un nombre, retourne la ligne correspondante"""
        if isinstance(o, str):
            return self.get(columns=[o])
        elif isinstance(o, int):
            return self.get(index=[o])
        else:
            return None


    def __iter__(self):
        """Initialise l'itération sur la matrice"""
        self.i = -1
        return self


    def next(self):
        """Permet d'itérer sur les entrées de la matrice"""
        self.i += 1
        if self.i >= len(self.matrix):
            raise StopIteration
        return self.i, self[self.i]


    def get_nearest(self, dict, k):
        """Renvoie les k entrées les plus similaires au dictionnaire dict"""
        # Seules les clés/colonnes communes sont utilisées pour la comparaison
        keys = set(dict.keys()) & set(self.columns)
        # Pour chaque entrée de la matrice, calcule la somme des différences
        # avec dict entre chaque clé/colonne
        distances = {i:sum([abs(dic[label]-row[0][label]) for label in list(keys)]) for i, row in self}
        # Trie les entrées de la matrice en fonction des différences calculées
        nearest_indexes = sorted(distances, key=distances.get)
        # Retourne les k entrées les plus similaires
        return self.get(index=nearest_indexes[:k])


def test():
    matrix = Matrix(columns=['BALISE_1','BALISE_2', 'x', 'y'])

    matrix.append({'x': 1, 'y': 1, 'BALISE_1': 40, 'BALISE_2': 30})
    matrix.append({'x': 4, 'y': 4, 'BALISE_1': 50, 'BALISE_2': 20})
    matrix.append({'x': 7, 'y': 7, 'BALISE_1': 60, 'BALISE_2': 10})

    print(matrix)

    print(matrix['x'])

    # for i, row in matrix:
    #     print(str(i)+': '+str(row))

    # print(matrix.get(columns=['y']))

    nearest = matrix.get_nearest({'BALISE_2': 15, 'BALISE_3': 10}, 2)
    # nearest = matrix.get_nearest({'BALISE_1': 55, 'BALISE_2': 15, 'BALISE_3': 10}, 2)

    x = 0
    y = 0
    for row in nearest:
        x += row['x']
        y += row['y']

    x /= float(len(nearest))
    y /= float(len(nearest))

    params = {'x': x, 'y': y}
    print(params)

if __name__ == "__main__":
    test()
