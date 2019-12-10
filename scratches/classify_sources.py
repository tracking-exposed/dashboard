import os

import matplotlib.pyplot as plt
import pandas as pd

df_list = []


def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


files = absoluteFilePaths('/home/ubuntu/PycharmProjects/dashboard/outputs/fb/summary')

print(files)
for f in files:
    df = pd.read_csv(f)
    df_list.append(df)
    print(len(df.index))

pages = {

    'Italia Viva': 'centro',
    'La Nazione': 'centro-destra',
    'La7': 'centro-sinistra',
    'Rainews.it': 'centro-sinistra',
    'Open': 'centro-sinistra',
    'Adnkronos': 'neutrale',
    'Partito Democratico': 'centro-sinistra',
    'Lega - Salvini Premier': 'destra',
    'Corriere della Sera': 'centro',
    'Il Foglio': 'destra',
    'Tgcom24': 'centro-destra',
    'Il Messaggero.it': 'centro',
    'Il Fatto Quotidiano': 'centro-sinistra',
    "Fratelli d'Italia": 'destra',
    'la Repubblica': 'sinistra',
    'il manifesto': 'sinistra',
    'La Stampa': 'centro',
    'il Post': 'centro',
    'Matteo Salvini': 'destra',
    'Il Giornale': 'destra',
    'Il Sole 24 ORE': 'centro-destra',
    'HuffPost Italia': 'centro-sinistra',
    'Sky TG24': 'centro',
    'Libero': 'destra',
    'MoVimento 5 Stelle': 'centro',
    'Giorgia Meloni': 'destra',
    'ANSA.it': 'neutrale',
    'Giuseppe Conte': 'centro',
    'Luigi Di Maio': 'centro',
    'Silvio Berlusconi': 'destra',
    'Matteo Renzi': 'centro'
}

polarized = {
    'Lega - Salvini Premier': 'destra',
    "Fratelli d'Italia": 'destra',
    'Matteo Salvini': 'destra',
    'Giorgia Meloni': 'destra'
}

orientamento = ['destra', 'centro-destra', 'centro', 'centro-sinistra', 'sinistra', 'neutrale']

t = 0
for o in orientamento:
    i = 0
    for key, value in pages.items():
        if value == o:
            i = i + 1
    print(o + ' :' + str(i))
    t += i
print('tot: ' + str(t))

for df in df_list:
    df = df[['source', 'user']]
    df = df.groupby('source').count().reset_index()
    df = df.replace({"source": pages})
    df = df.groupby('source').sum().reset_index()
    df = df[df['user'] > 9].sort_values('user',
                                        ascending=False)
    df.plot()
    plt.show()
    print(df)
