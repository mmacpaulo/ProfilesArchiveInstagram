# seleciona o perfil da lista.txt   e organica em uma lista com o nome do perfil 
# seguido do link do perfil.

import pandas as pd

nw = open('lista.txt', 'r')

data = pd.DataFrame()

for line in nw.readlines():
    data.loc[len(data),['Perfil','url']] = [line.strip().split('/')[-2] , line.strip()]

# remove duplicadas
ndata = data.drop_duplicates(keep='last')
# salva lista em csv
ndata.to_csv('lista_organizada.csv',index=False)
# salva lista em Markdown para visualizar.
ndata.to_markdown('lista_organizada.md',index=False)
