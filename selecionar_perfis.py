# seleciona o perfil da lista.txt   e organica em uma lista com o nome do perfil 
# seguido do link do perfil.

import pandas as pd
from datetime import date
import numpy as np

today = date.today()
# dd/mm/YY
d1 = today.strftime("%d/%m/%Y")

nw = open('lista.txt', 'r')

data = pd.DataFrame()

for line in nw.readlines():
    data.loc[len(data),['Perfil (@)','URL']] = [line.strip().split('/')[-2] , line.strip()]

# remove duplicadas
ndata = data.drop_duplicates(keep='last').reset_index(drop=True)
# reindex
ndata.index = pd.RangeIndex(start=1, stop=len(ndata)+1, step=1)

# salva lista em csv
ndata.to_csv('lista_atual.csv')

# salva lista em Markdown para visualizar.
ndata.to_markdown('lista_md.md')

with open('lista_atual.md','w') as lista_out, open('lista_md.md') as listamd:

    cab =  f" **Perfis sobre Arquivologia no Instagram** \n\n Lista dos perfis encontratos a partir da pesquisa com os termos 'arquivo', 'arquivologia' e 'arquivística'. \n\n Pesquisa realizada no dia {d1}.\n\n"
    lista_out.write(cab)
    for il in listamd.readlines():
        lista_out.write(f'{il}')
    rpe = "\n\n [Informações sobre o projeto 'Perfis sobre Arquivologia no Instagram'](https://github.com/mmacpaulo/ProfilesArchiveInstagram)"
    lista_out.write(rpe)

    listamd.close()
    lista_out.close()