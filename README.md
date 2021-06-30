# covid-ministerio_saude
Dados de covid-19 raspados do site do Ministério da Saúde do Brasil

## Motivação

Existem alguns dados de COVID-19 no Brasil disponpíveis em formatos abertos. Mas nem sempre é muito fácil fazer o download ou muitas vezes sem a frequência de atualização desejada. Por isso, fiz esse script em python que faz o download dos dados diretamente de https://covid.saude.gov.br/.

## O quê ele faz?

Esse script:
- abre o navegador Firefox
- clica no botão de download
- fecha o navegador
- extrai o arquivo RAR
- junta os CSVs em um Pandas dataframe
- filtra apenas os dados do AM em outro dataframe (minha área de interesse aqui)
- cria colunas de letalidade, casos/100k habitantes, uma coluna booleana para marcar os daddos mais atuais e uma coluna de nível/escala do dado (estadual ou municipal)
- salva o dataframe resultante em um CSV para o estado de interesse (AM).
