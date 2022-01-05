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

#specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome()

#open the webpage
driver.get("http://www.instagram.com")

#target username
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

#enter username and password
try:
    with open('login.txt', 'r') as usere:
        datauser = usere.read()
        usuario, senha = datauser.split(" ")
except: 
    print('arquivo não existe.\n')
    print('crie o arquivo login.txt com o usuario e senha na mesma linha separados por espaço.')
usere.close()

# perfilarquivologia 
username.clear()
username.send_keys(usuario)
password.clear()
password.send_keys(senha)

#target the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

#We are logged in!
#nadle NOT NOW

not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Agora não")]'))).click()
not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Agora não")]'))).click()

# ## Search keywords

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
driver.quit()