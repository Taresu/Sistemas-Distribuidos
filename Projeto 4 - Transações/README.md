# 1. Arquitetura Monolítica utilizando o protocolo Two-Phase Commit
Na arquitetura monolítica, todas as funcionalidades do sistema estão integradas em uma única aplicação. Utilizaremos o protocolo 2PC para garantir a consistência dos dados.

# 2. Arquitetura de Microsserviços utilizando o padrão SAGA
Na arquitetura de microsserviços, cada serviço é independente e se comunica através de eventos. Utilizaremos o padrão SAGA com coreografia, onde os microsserviços publicam e consomem eventos para garantir a consistência.

Implementação de Microsserviços com SAGA
Vamos implementar cada serviço como um processo independente que se comunica via eventos. Utilizaremos o RabbitMQ como sistema de mensagens.

# Observações
1. Instalação do RabbitMQ:

Instale o RabbitMQ em sua máquina seguindo as instruções disponíveis no site oficial do RabbitMQ.
Certifique-se de que o RabbitMQ esteja em execução.

2. Execução dos serviços:

Execute cada serviço em um terminal separado.
Primeiro, execute o servico_pedidos.py para enviar um pedido inicial e começar a ouvir eventos.
Em seguida, execute os outros serviços (servico_estoque.py, servico_pagamentos.py, servico_envio.py) para que possam ouvir e processar os eventos.

3. Bibliotecas necessárias:

Para conectar ao RabbitMQ, use a biblioteca pika. Instale-a com o comando: 'pip install pika'.

Esses exemplos demonstram a implementação de um sistema de comércio eletrônico em duas arquiteturas diferentes, usando transações tradicionais para a arquitetura monolítica e o padrão SAGA com coreografia para a arquitetura de microsserviços.
