#!/usr/bin/env python
# coding: utf-8

# # Script para raspar os dados de COVID-19 do site do Ministério da Saúde (MS) e fazer um dataframe para o Painel Covid-Amazonas - https://mamiraua.org.br/covid-amazonas



# In[2]:
# ## Importando bibliotecas necessárias

from glob import glob
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
import time
import os
import patoolib
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# In[2]:
OS_SYSTEM = os.name # nt == windows posix == linux, unix
# caso seja um sistema diferente de windows, obtem um diretório apropriado
BASE_FOLDER = "C:\\covid-amazonas\\" if 'nt' in OS_SYSTEM else '/tmp/'
## Define a pasta onde será baixado o arquivo e deleta arquivos (`RAR` e `CSV`s extraídos) antes


for item in os.listdir(BASE_FOLDER):
    if item.endswith(tuple([".rar", ".csv"])):
        os.remove(os.path.join(BASE_FOLDER, item))

# In[3]:


# Para que não abra a caixa de diálogo de download do firefox e para que o arquivo seja salvo no local persolnalizado
options = Options()
options.set_preference("browser.download.folderList", 2) # diretorio de download personalizado
options.set_preference("browser.download.manager.showWhenStarting", False) # nao abrir caixa de dialogo
options.set_preference("browser.download.dir", BASE_FOLDER) # baixar na pasta personalizada
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-rar-compressed, application/octet-stream, application/zip, application/octet-stream, application/x-zip-compressed, multipart/x-zip") # nao perguntar sobre arquivos compactados
browser = webdriver.Firefox(options=options) # abre firefox

while True:
    try:   
        # entra no site
        browser.get("https://covid.saude.gov.br/")
        # espera 15 segundos para carregar todo site
        time.sleep(15)
    except WebDriverException as error:
        # Caso esteja sem internet, ou website indisponível ocorrera um erro com NotFound em error.msg
        # Ingnora silenciosamente e tenta uma nova requisição
        time.sleep(25) # faz uma nova tentativa após 25 segundos
        pass
    else:
        # Se tudo ocorreu bem no browser.get, sai do while
        break

filename = glob(BASE_FOLDER+'*.rar')

# clica em baixar arquivo
browser.find_element_by_xpath("//ion-button[contains(text(),'Arquivo')]").click()

# assim que baixar o arquivo .rar, fecha o browser
while not filename:
    time.sleep(1)
    filename = glob(BASE_FOLDER+'*.rar')

browser.quit()
# In[7]:

# extraindo o arquivo RAR
program = '/usr/bin/7z' if 'posix' in OS_SYSTEM else ''
patoolib.extract_archive(filename, outdir=BASE_FOLDER, program=program)
                         

# In[8]:

# juntando os 3 CSVs que vem dentro do rar em um único dataframe, filtrando em seguida apenas dados do AM
csvs = []

for table in os.listdir(BASE_FOLDER):
    if table.endswith(".csv"):
        df = pd.read_csv(BASE_FOLDER + table, index_col=None, header=0, sep=';')
        csvs.append(df)

df_all = pd.concat(csvs, axis=0, ignore_index=True)


# In[11]:


df_am = df_all[df_all['estado'] == 'AM'].copy()
df_am['data'] = pd.to_datetime(df_am['data'], format='%Y-%m-%d')
df_am.sort_values(by=['municipio', 'data'], axis=0,
                  ascending=[True, False], inplace=True)
# df_am.head()
# print(df_am.dtypes)


# In[51]:

# ## Adiciona colunas de letalidade, de casos/100k habitantes, uma booleana para marcar os daddos mais atuais e uma de nível/escala do dado (estadual ou municipal)
df_am['ultimo_dado'] = df_am['data'] == df_am.data.max()
df_am['nivel_dado'] = df_am['municipio'].apply(
    lambda x: 'estadual' if pd.isnull(x) else 'municipal')

df_am['letalidade'] = (df_am['obitosAcumulado'] / df_am['casosAcumulado']) * 100
df_am['casos_100k'] = (df_am['casosAcumulado'] / df_am['populacaoTCU2019']) * 100000
# df_am.head()


# is_last
# confirmed_per_100k_inhabitants
# death_rate




# In[54]:

# salva csv final
df_am.to_csv(BASE_FOLDER + 'casos_am_MS.csv', sep=',', encoding='utf-8', index=False)
# df_all.to_csv(folder + 'casos_brasil_MS.csv', sep=',', encoding='utf-8', index=False)
