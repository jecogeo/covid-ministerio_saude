# covid-ministerio_saude
Dados de covid-19 raspados do site do Ministério da Saúde do Brasil

## Motivação

Os dados do Ministério da Saúde (MS) são uma das únicas fontes de dados diários de COVID-19 à nível municipal. Mas esses dados não são acessíveis por máquina (sem API ou URL fixa). Além disso, o arquivo vem compactado e divido em partes, o que dificulta o fácil tratamento e consumo desses dados. 

Além dessa fonte, existem algumas iniciativas importantes de dados de COVID-19 no Brasil disponíveis em formatos abertos. Principalmente os dados do Brasil.io, compilados dos boletins das Secretarias Estaduais de Saúde. No entanto têm havido constantes atrasos na liberação dos dados ao nível municipal, afinal é um projeto que conta com voluntários para essa compilação. Eu mesmo fui voluntário por mêses e conheço as dificuldades e entendo os atrasos. 

Por isso, tendo em vista a obtenção diária de dados atualizados para atualização do dashboard que mantenho em https://mamiraua.org.br/covid-amazonas, fiz esse script em python que "raspa" os dados diretamente de https://covid.saude.gov.br/ e os trata para gerar uma única tabela completa.


## O quê ele faz?

Esse script:
- abre o navegador Firefox;
- clica no botão de download;
- fecha o navegador;
- extrai o arquivo RAR;
- junta os CSVs em um Pandas dataframe;
- filtra apenas os dados do AM em outro dataframe (minha área de interesse aqui);
- cria colunas de letalidade, casos/100k habitantes, uma coluna booleana para marcar os dados mais atuais e uma coluna de nível/escala do dado (estadual ou municipal);
- salva o dataframe resultante em um CSV para o estado de interesse (AM);
- gera um arquivo de logs do processo.

## Agradecimento Especial

Um agradecimento especial ao [@franklintimoteo](https://github.com/franklintimoteo) pela contribuição em lidar com problemas de internet no script, que levantei na [Issue #1](https://github.com/jecogeo/covid-ministerio_saude/issues/1). Tua contribuição foi essencial!! Obrigado!
