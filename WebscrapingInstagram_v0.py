#!/usr/bin/env python
# coding: utf-8

# # Web Scraping Instagram with Selenium

#imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


# ## Download ChromeDriver
# Now we need to download latest stable release of ChromeDriver from:
# <br>
# https://chromedriver.chromium.org/

# In[134]:


#specify the path to chromedriver.exe (download and save on your computer)
option = webdriver.ChromeOptions()
# option.add_argument('headless')
driver = webdriver.Chrome('/home/claudio/Downloads/Chrome/chromedriver',options=option)

#open the webpage
driver.get("http://www.instagram.com")

#target username
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

#enter username and password
with open('login_out.txt') as userfile:
    line = userfile.readline() 
    usuario, senha = line.strip().split(' ')


username.clear()
username.send_keys(usuario)
password.clear()
password.send_keys(senha)

#target the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#We are logged in!


# In[135]:


#nadle NOT NOW

not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Agora não")]'))).click()
not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Agora não")]'))).click()


# ## Search keywords

# In[136]:

def buscar_palavras(keywords):
    import time

#target the search input field
    searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Pesquisar']")))
    searchbox.clear()

#search for the hashtag cat
    # keyword = "arquivologia"
    searchbox.send_keys(keywords)
    time.sleep(2)
    divs = driver.find_elements(By.CLASS_NAME, 'fuqBx')

    return divs


# Salva a lista com resultados da busca

with open('lista.txt','w') as filew,  open('keywords.txt','r') as palavras:
    buscapor = palavras.readlines()
    for iw in buscapor:
        divs = buscar_palavras(f'@{iw.split()[0]}')
    
        for div in divs:
            print("___")
            elements = div.find_elements(By.TAG_NAME, 'a')

            for element in elements:
                filew.write(element.get_attribute("href"))
                filew.write('\n')

palavras.close()
filew.close()
# abre a lista e busca as publicaçoes e seguidores em uma nova lista.

def buscar_seguir_perfil(urls):
    import time
    driver.get(urls)
    time.sleep(3)
    h1 = driver.find_elements(By.CSS_SELECTOR,'h1')
    for i in h1:
        print(f'status da página {i.text} \n')
    try:
        posting = driver.find_element(By.XPATH,'/html/body/div[1]/section/main/div/header/section/ul/li[1]/div/span').text
        print('publicaçoes ',posting)
    except:
        posting = "0" 
        print("publicaçoes não foi possivel encontrar")
    
    try:
        followers = driver.find_element(By.XPATH,'/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/div/span').text
        print('seguidores ',followers)
    except:
        followers = "0"
        print("seguidores não foi possivel encontrar")

    try:
        followinger = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Seguir")]'))).click()
        print(' ### ### Seguindo um novo perfil.')
    except:
        print('Já está seguindo este perfil.')

    return posting,followers


# perfil do list file

import pandas as pd
from datetime import date

today = date.today()
# dd/mm/YY
d1 = today.strftime("%d%m%Y")
d1fmt = today.strftime("%d/%m/%Y")

data = pd.read_csv('lista.txt')
fileout = f"lista_{d1}"
ndata = data.drop_duplicates(keep='last')

outdata = pd.DataFrame()

for iw in ndata.values:
    iw=iw[0]
    post,follow = buscar_seguir_perfil(iw.strip())
    outdata.loc[len(outdata),['NumeroSeguidores','NumeroPostagens','@Perfil','url']] = [follow,post,iw.strip().split('/')[-2] , iw.strip()]

# salva lista em csv
outdata.index = pd.RangeIndex(start=1, stop=len(ndata)+1, step=1)
outdata.to_csv(fileout+'.csv')
# salva lista em Markdown para visualizar.
outdata.to_markdown(fileout+'.md')
# criar uma lista temporaria
outdata.to_markdown('lista_md.md')

driver.quit()
# formata o arquivo para apresentar no github
with open('lista_atual.md','w') as lista_out, open('lista_md.md') as listamd:

    cab =  f" **Perfis sobre Arquivologia no Instagram** \n\n Lista dos perfis encontratos a partir da pesquisa com os termos 'arquivo', 'arquivologia' e 'arquivística'. \n\n Pesquisa realizada no dia {d1fmt}.\n\n"
    lista_out.write(cab)
    for il in listamd.readlines():
        lista_out.write(f'{il}')
    rpe = "\n\n [Informações sobre o projeto 'Perfis sobre Arquivologia no Instagram'](https://github.com/mmacpaulo/ProfilesArchiveInstagram)"
    lista_out.write(rpe)

    listamd.close()
    lista_out.close()
