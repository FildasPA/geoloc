import pandas as pd
import operator

NEAREST_POSITIONS = 2

def get_nearest_positions(df, rssis, k):
    distances = {}
    for i, row in df.iterrows():
        distances[i] = sum([abs(rssis[label] - row[label]) for label in row.drop(labels=['x', 'y']).index])
    # print(distances)

    indexes = sorted(distances, key=distances.get)
    # print(indexes)

    nearest = pd.DataFrame(columns=['x', 'y'])
    for i in range(k):
        nearest = nearest.append(df.loc[indexes[i], ['x', 'y']].to_dict(),
                                 ignore_index=True)
    # print(nearest)
    return nearest


def get_position(df, rssis):
    nearest = get_nearest_positions(df, rssis, NEAREST_POSITIONS)
    x = nearest.loc[:,'x'].mean()
    y = nearest.loc[:,'y'].mean()
    # print(x, y)
    return x, y


df = pd.DataFrame(columns=['x', 'y', 'BALISE_1', 'BALISE_2', 'BALISE_3'])

df = df.append({'x': 1, 'y': 0, 'BALISE_1': 35, 'BALISE_2': 18, 'BALISE_3': 50}, ignore_index=True)
df = df.append({'x': 0, 'y': 0, 'BALISE_1': 50, 'BALISE_2': 25, 'BALISE_3': 100}, ignore_index=True)
df = df.append({'x': 2, 'y': 0, 'BALISE_1': 15, 'BALISE_2': 15, 'BALISE_3': 30}, ignore_index=True)

get_position(df, {'BALISE_1': 50, 'BALISE_2': 25, 'BALISE_3': 100})
