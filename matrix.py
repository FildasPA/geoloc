#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Implémentation d'une matrice."""

class Matrix:
    def __init__(self, columns=[]):
        self.matrix = []
        self.columns = columns


    def __str__(self):
        s = ''
        for i, row in enumerate(self.matrix):
            d = {}
            for j, key in enumerate(self.columns):
                d[key] = row[j]
            s += str(i)+': '+str(d)+'\n'
        return s


    def append(self, row):
        values = []
        for key in self.columns:
            if key in row:
                values.append(row[key])
            else:
                values.append(0)

        self.matrix.append(values)


    def get(self, columns=None, index=None):
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
        if isinstance(o, str):
            return self.get(columns=[o])
        elif isinstance(o, int):
            return self.get(index=[o])
        else:
            return None


    def __iter__(self):
        self.i = -1
        return self


    def next(self):
        self.i += 1
        if self.i >= len(self.matrix):
            raise StopIteration
        return self.i, self[self.i]


    def get_nearest(self, dictionnary, k):
        distances = {i:sum([abs(dictionnary[label]-row[0][label]) for label in list(set(self.columns) & set(dictionnary.keys()))]) for i, row in self}
        nearest_indexes = sorted(distances, key=distances.get)
        return self.get(columns=['x', 'y'], index=nearest_indexes[:k])


def main():
    matrix = Matrix(columns=['x','y'])

    matrix.append({'x': 5, 'y': 3})
    matrix.append({'x': 10, 'y': 8})
    matrix.append({'x': 7, 'y': 1})

    print(matrix)

    print(matrix['x'])

    # for i, row in matrix:
    #     print(str(i)+': '+str(row))

    # print(matrix.get(columns=['y']))

    print(matrix.get_nearest({'x': 7, 'y': 2}, 1))

if __name__ == "__main__":
    main()
