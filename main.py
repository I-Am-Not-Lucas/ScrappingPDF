

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from make import Driver

from urllib.request import urlopen

import time

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager


driver = webdriver.Chrome()
driver.get("http://diariooficial.imprensaoficial.com.br/nav_v6/index.asp?c=34031&e=20231030&p=1")
time.sleep(5)


driver.switch_to.frame("topFrame")
driver.maximize_window()

while True:
    try:
        driver.find_element('xpath', '//*[@id="pg"]/option[27]').click()
    except Exception as e:
        print(f"Elemento não foi achado {e}")
        time.sleep(2)
    else:
        break

"""## Download do arquivo"""

driver.switch_to.default_content()
time.sleep(2)

elemento_ = driver.find_element('xpath', '//*[@id="frame"]')
link = elemento_.get_attribute('src')
print(link)

driver.get(link)

try:
    response = urlopen(link)

    with open("pagina_scrapping.pdf", "wb") as file:
        file.write(response.read())
except:
    print("Deu errado")
else:
    print("Dowload feito com sucesso")

print(response.read().decode('utf-8'))

"""## Seção 2: uso do regex e varredura de pdf"""

import regex as re
import PyPDF2

def ler_pdf(path):
    with open(path, 'rb') as arquivo_pdf:
        reader = PyPDF2.PdfReader(arquivo_pdf)

        pagina = reader.pages[0]
        texto = pagina.extract_text()
        return texto

path = 'pagina_scrapping.pdf'

conteudo = ler_pdf(path)

padrao = re.compile(r'\bTOMADA\sDE\sPREÇOS\s\b.{18}')

correspondencias = re.findall(padrao, conteudo)

for valor in correspondencias:
    print(valor)