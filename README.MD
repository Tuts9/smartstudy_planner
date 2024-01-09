# SmartStudy Planner

O SmartStudy Planner é um aplicativo que permite gerar mapas mentais e planos de estudos com base em entradas de usuário. Ele também oferece a funcionalidade de salvar os resultados em um arquivo PDF e mantém um histórico das pesquisas realizadas.

## Interface Gráfica

A criação da janela e todo layout foram feitos com o uso de uma biblioteca de UI python, a `customtkinter` que serve para ser usada com os mais diversos tipos de programas entregando uma interface limpa, bonita e agradável ao usuário, o qual também poderá escolher entre usar o **tema escuro** ou o **tema claro**.


## Funcionalidades

### Geração de Mapa Mental e Plano de Estudos

O aplicativo oferece duas opções principais para o usuário:

1. **Mapa Mental**: O usuário pode inserir um tópico e o aplicativo gera um mapa mental relacionado a esse tópico, incluindo a ideia central, os ramos principais e os subramos.
2. **Plano de estudos**: O usuário pode inserir um tópico e o aplicativo elabora um plano de estudos para esse tópico.

### Salvar em PDF

O aplicativo permite salvar os resultados das pesquisas em um arquivo PDF.

### Histórico de Pesquisas

O aplicativo mantém um histórico das pesquisas realizadas incluindo o tópico pesquisado e as data da pesquisa. O histórico pode ser visualizado em uma janela separada e oferece a opção de excluir itens do histórico.

### Thread

Foi necessário o uso da biblioteca `threading` para estar usando um processo exclusivo na hora de gerar a resposta para o usuário, antes sem o uso dessa funcionalidade o programa sofria um crash momentâneo e voltava ao normal com a resposta pronta e disponível ao usuário e com isso a adição de uma *progress bar* para indicar que a resposta está sendo gerada.

## Requisitos e Dependências

- Python 3.x
- Bibliotecas: `fpdf`, `tkinter`, `customtkinter`, `json`, `requests`, `sqlite3`. `threading`.

## Configurações e Uso

1. Instale as bibliotecas necessárias: `fpdf`, `customtkinter`, `json`, `requests`, `sqlite3`.
2. Entre no site da OpenAI e coloque a sua chave API na variável `API_KEY`.

3. Execute o arquivo `smartstudy_planenr.py` para iniciar o aplicativo.

## Desenvolvimento e Contribuições

O código fonte está disponível no arquivo `smartstudy_planner.py`. Sinta-se à vontade para contribuir com novos recursos, correções de bugs ou melhorias na interface do usuário.

## Autor

Esta aplicativo foi Desenvolvido por Arthur Rodrigues (Tuts9).

## Licença

Este código é disponibilizado sob a licença [MIT](https://opensource.org/licenses/MIT), o que significa que você é livre para usá-lo, modificá-lo e distribuí-lo da maneira que desejar, desde que mantenha o aviso de direitos autorais original e não responsabilize os autores por qualquer dano ou perda relacionada ao uso deste código.

## Contato

Para relatar problemas, enviar feedback ou obter mais informações, entre em contato com Arthur em (arthurdevti@gmail.com).