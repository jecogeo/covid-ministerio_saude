# covid-ministerio_saude
Dados de covid-19 raspados do site do Ministério da Saúde do Brasil

## Motivação

Existem alguns dados de COVID-19 no Brasil disponíveis em formatos abertos. Principalmente os dados do Brasil.io, compilados dos boletins estaduais. No entanto têm havido constantes atrasos na liberação dos dados ao nível municipal, afinal é um projeto que conta com voluntários para essa compilação. Eu mesmo fui voluntário por mêses e conheço as dificuldades e entendo os atrasos. Para mim, o ideal é ter os dados atualizados diariamente para atualização do dashboard que mantenho em https://mamiraua.org.br/covid-amazonas.

Os dados do Ministério da saúde restam sendo a única fonte de dados diários à nível municipal. Mas esses dados não são acessíveis por máquina (sem API ou URL fixa). Por isso, fiz esse script em python que "raspa" os dados diretamente de https://covid.saude.gov.br/.

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
- gera um arquivo de logs.

## Agradecimento Especial

Um agradecimento especial ao [@franklintimoteo](https://github.com/franklintimoteo) pela contribuição em lidar com problemas de internet no script, que levantei na [Issue #1](https://github.com/jecogeo/covid-ministerio_saude/issues/1). Tua contribuição foi essencial!! Valeu demais!
