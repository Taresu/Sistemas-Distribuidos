# Sistemas Distribuídos

#### `Bacharelado` Sistemas de Informação (BSI)
#### `Universidade` UTFPR - Universidade Tecnológica Federal do Paraná
#### `Docente`  Ana Cristina Kochem

_______________________________________________________________________________________________________________________________________________________________________

## 📖 Ementa

Caracterização de sistemas distribuídos. Arquiteturas de sistemas distribuídos. Modelo de falhas. Modelo de segurança. Comunicação e sincronização em sistemas distribuídos. Coordenação e acordo. Eventos e notificações. Serviços web. Middlewares. Transações. Controle de concorrência.


## 💭 Contextualização

A disciplina de Sistemas Distribuídos explora os princípios e técnicas para projetar, implementar e gerenciar sistemas que operam em redes distribuídas. Ela abrange desde fundamentos como arquiteturas e comunicação, até tópicos avançados como segurança e tolerância a falhas. Essa compreensão é essencial para lidar com os desafios da crescente dependência de sistemas distribuídos em aplicações modernas.

<details>
  <summary>SAIBA MAIS! ;)</summary>

  Nos últimos anos, vimos um aumento no uso de sistemas distribuídos em diferentes áreas da indústria e da tecnologia. Eles são importantes para lidar com grandes quantidades de dados, garantir que os serviços estejam sempre disponíveis e possam crescer conforme necessário, como acontece na Internet.

O objetivo principal da disciplina é ajudar os estudantes a entender os princípios e desafios por trás da criação, implementação e operação desses sistemas. Começamos com conceitos básicos, como como esses sistemas são construídos e como eles se comunicam, e depois avançamos para coisas mais complexas, como manter esses sistemas seguros e garantir que eles funcionem sem problemas.

Durante o curso, os alunos aprendem sobre problemas práticos que surgem ao lidar com sistemas distribuídos, como lidar com muitas pessoas tentando acessar os mesmos dados ao mesmo tempo, garantir que os dados estejam sempre corretos e lidar com falhas que possam acontecer sem prejudicar o sistema como um todo. Eles também têm a chance de explorar tecnologias modernas usadas para construir esses sistemas, como serviços web e ferramentas de comunicação.

Entender como os sistemas distribuídos funcionam é importante para profissionais de tecnologia da informação e desenvolvedores de software, já que muitos dos aplicativos e serviços que usamos todos os dias dependem deles para funcionar corretamente. Por isso, essa disciplina é crucial para preparar os alunos para os desafios que enfrentarão no mundo real da computação distribuída.

  ### Um pouco de Python
  ```py
  def sistemas_distribuidos():
    print('algum trecho de código representativo')
  ```
</details>

<<<<<<< Updated upstream
=======
## 💯 Projeto 1 - Contextualização e Desenvolvimento

`Discentes` - Luis Carlos e Thales Salata 

A ideia foi criar uma aplicação de mensageria no contexto de um restaurante e/ou mercado.

Serviço: RabbitMQ (Message Broker)
Protocolo: AQMP (Advanced Message Queuing Protocol)
Linguagem: Python

A aplicação se concentra em enviar e receber mensagens entre diferentes partes do sistema, como criadores de mensagens (publishers) e consumidores de mensagens (consumers).

No contexto da Arquitetura Orientada a Eventos, os eventos são gerados e consumidos de forma assíncrona por diferentes partes do sistema. O restaurante atua como produtor de eventos (producers), enviando promoções (publish) de produtos para um sistema de mensageria (RabbitMQ), e os consumidores assinam (subscribe) essas promoções para processamento. 

Os eventos são trocados de forma assíncrona, proporcionando desacoplamento entre produtores e consumidores, permitindo escalabilidade e resiliência no sistema. O RabbitMQ é utilizado como o serviço de mensageria, roteando as mensagens para as filas correspondentes (queues), onde os consumidores (consumers) as processam conforme necessário.

Checklist:
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

Progresso:
![](https://geps.dev/progress/85) 

>>>>>>> Stashed changes
## 🌐 Links interessantes 

- [Rabbit MQ](https://www.rabbitmq.com/)
- [Rabbit MQ, Python Tutorial 1](https://www.rabbitmq.com/tutorials/tutorial-one-python)

