## 💯 Projeto 1 - Contextualização e Desenvolvimento

________________________________________________________________
`Discentes`: 

Luis Carlos, [luisj.1994@alunos.utfpr.edu.br](mailto:luisj.1994@alunos.utfpr.edu.br), 2073099

Thales Salata, [tsalata@alunos.utfpr.edu.br](mailto:tsalata@alunos.utfpr.edu.br), 2324911

_________________________________________________________________

A ideia implementada é uma aplicação de mensageria no contexto de um restaurante e/ou mercado.


**Serviço**: RabbitMQ (Message Broker)

**Protocolo**: AQMP (Advanced Message Queuing Protocol)

**Linguagem**: Python

_________________________________________________________________

A aplicação se concentra em enviar e receber mensagens entre diferentes partes do sistema, como criadores de mensagens (publishers) e consumidores de mensagens (consumers).

No contexto da Arquitetura Orientada a Eventos, os eventos são gerados e consumidos de forma assíncrona por diferentes partes do sistema. O restaurante atua como produtor de eventos (producers), enviando promoções (publish) de produtos para um sistema de mensageria (RabbitMQ), e os consumidores assinam (subscribe) essas promoções para processamento. 

Os eventos são trocados de forma assíncrona, proporcionando desacoplamento entre produtores e consumidores, permitindo escalabilidade e resiliência no sistema. O RabbitMQ é utilizado como o serviço de mensageria, roteando as mensagens para as filas correspondentes (queues), onde os consumidores (consumers) as processam conforme necessário.

`Checklist`:
- [X] Criar arquivo em Python para o Projeto 1 - Arquitetura Orientada a Eventos
- [X] Fazer README.md básico do repositório
- [ ] Fazer um trecho de código representativo para a contextualização da disciplina, no README
- [X] Fazer o tutorial do RabbitMQ e entender como o protocolo AMQP funciona na prática
- [X] Desenvolver uma aplicação envolvendo o contexto de um mercado
- [X] Desenvolver uma aplicação envolvendo o contexto de um restaurante
- [X] Conversar sobre as soluções, como cada uma delas funciona e o que pode ser melhorado
- [X] Adicionar uma contextualização ao tópico para explicar melhor o que foi feito
- [X] Aprimorar README
- [ ] Aprimorar lógica dos códigos

`Progresso`: 

![](https://geps.dev/progress/85) 
