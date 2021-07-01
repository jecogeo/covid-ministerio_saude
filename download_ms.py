#!/usr/bin/env python
# coding: utf-8

# # Script para raspar os dados de COVID-19 do site do Ministério da Saúde (MS) e fazer um dataframe para o Painel Covid-Amazonas



# In[2]:
# ## Importando bibliotecas necessárias

from glob import glob
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os
import patoolib
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


# ## Define a pasta onde será baixado o arquivo e deleta arquivos (`RAR` e `CSV`s extraídos) anteriores

# In[2]:


folder = "/home/jeco/Mamirauá/COVID/painel-covid/"

for item in os.listdir(folder):
    if item.endswith(tuple([".rar", ".csv"])):
        os.remove(os.path.join(folder, item))


# ## Definindo algumas opções do firefox, abrindo o firefox e baixando o arquivo RAR

# In[3]:


# Para que não abra a caixa de diálogo de download do firefox e para que o arquivo seja salvo no local persolnalizado
options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.download.dir", folder)
options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                       "application/x-rar-compressed, application/octet-stream, application/zip, application/octet-stream, application/x-zip-compressed, multipart/x-zip")
browser = webdriver.Firefox(options=options)

# Abre o firefox, entra no site, espera carregar tudo, clica em download, espera um pouco e fecha o browser
browser.get("https://covid.saude.gov.br/")
time.sleep(15)  # espera 15 segundos para carregar todo site
browser.find_element_by_xpath("//ion-button[contains(text(),'Arquivo')]").click()
time.sleep(15)  # espera 15 segundos para terminar o download
browser.quit()


# ## extraindo o arquivo RAR e juntando os 3 CSVs que vem dentro dele em um único dataframe, filtrando em seguida apenas dados do AM

# In[7]:


filename = glob('/home/jeco/Mamirauá/COVID/painel-covid/*.rar')[0]
patoolib.extract_archive(filename, outdir=folder, program='/usr/bin/7z')


# In[8]:


csvs = []

for table in os.listdir(folder):
    if table.endswith(".csv"):
        df = pd.read_csv(folder + table, index_col=None, header=0, sep=';')
        csvs.append(df)

df_all = pd.concat(csvs, axis=0, ignore_index=True)


# In[11]:


df_am = df_all[df_all['estado'] == 'AM'].copy()
df_am['data'] = pd.to_datetime(df_am['data'], format='%Y-%m-%d')
df_am.sort_values(by=['municipio', 'data'], axis=0,
                  ascending=[True, False], inplace=True)
df_am.head()
# print(df_am.dtypes)


# In[51]:

# ## Adiciona colunas de letalidade, de casos/100k habitantes, uma booleana para marcar os daddos mais atuais e uma de nível/escala do dado (estadual ou municipal)
df_am['ultimo_dado'] = df_am['data'] == df_am.data.max()
df_am['nivel_dado'] = df_am['municipio'].apply(
    lambda x: 'estadual' if pd.isnull(x) else 'municipal')
df_am['letalidade'] = (df_am['obitosAcumulado'] / df_am['casosAcumulado']) * 100
df_am['casos_100k'] = (df_am['casosAcumulado'] / df_am['populacaoTCU2019']) * 100000
df_am.head()


# is_last
# confirmed_per_100k_inhabitants
# death_rate


# In[54]:


df_am.to_csv(folder + 'casos_am_MS.csv', sep=',', encoding='utf-8', index=False)
df_all.to_csv(folder + 'casos_brasil_MS.csv', sep=',', encoding='utf-8', index=False)
