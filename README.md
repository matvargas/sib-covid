# sib-covid
## Sistema de visualização de dados de COVID-19 no estado de Minas Gerais

O sistema foi desenvolvido utilizando as linguagens python e javascript. No lado do python utilizamos o framework Django para o desenvolvimento da aplicação web e no javascript utilizandos a biblioteca chart.js para a renderização dos gráficos.


### Arquivos importantes:
- etl/etl.py: onde executamos todo o processo de limpeza, normalização e carregamento dos dados.
- scripts/functions.py: arquivo utilizado como scratchpad para a confecção dos dados, possui outras bibliotecas python para renderização de gráficos (como por exemplo: matplotlib, folium, circlify, etc) que utilizamos para testar os gráficos.
- covid_data_viewer/views.py: arquivo onde efetivamente calculamos os dados para serem renderizados nos gráficos, aqui realizamos conexões com o banco e buscamos os dados que serão repassados ao javascript contido nos arquivos .html
- covid_data_viewer/templates/covid_data_viewer/: praticamente todos os arquivos .html contidos nesse diretório contém trechos de código em javascript utilizado para de fato renderizar os gráficos que foram propostos.

### Outros arquivos
- Em geral os outros arquivos contidos nesse projeto são requeridos pelo framework Django para que a aplicação web possa funcionar da maneira correta. Arquivos para configuração de urls, css, etc...

### Observações
- O Python env necessário para a execução desse código deve incluir os seguintes pacotes: django, pandas, sqlalchemy, folium, circlify e seaborn.
- Os arquivos .csv utilizados podem ser baixados no link a seguir: https://opendatasus.saude.gov.br/dataset/casos-nacionais
