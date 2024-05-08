## 💯 Projeto 2 - Middleware Pyro e Algoritmo de Consenso
________________________________________________________________
`Discentes`: 

Luis Carlos, [luisj.1994@alunos.utfpr.edu.br](mailto:luisj.1994@alunos.utfpr.edu.br), 2073099

Thales Salata, [tsalata@alunos.utfpr.edu.br](mailto:tsalata@alunos.utfpr.edu.br), 2324911

_________________________________________________________________

O projeto implementa um sistema distribuído utilizando o algoritmo de consenso Raft para replicação de log entre quatro processos. 

**Biblioteca**: Pyro5 (Python Remote Objects)

**Algoritmo**: Raft (Algoritmo de Consenso)

**Linguagem**: Python3

_________________________________________________________________

Os processos se comunicam através do middleware Pyro e são compostos por quatro servidores e um cliente. 

O sistema consiste em três principais componentes: eleição de líder, replicação de log e comunicação cliente-servidor.

**Eleição de Líder**:

- Os processos iniciam como seguidores e podem se tornar candidatos para liderar.
- Temporizadores de eleição aleatórios são utilizados para evitar a eleição simultânea de múltiplos líderes.
- Quando um líder falha, outro processo é eleito para liderar.

**Replicação de Log**:

- O cliente busca o URI do líder no servidor de nomes Pyro.
- O cliente envia comandos ao líder, que os anexa ao seu log e replica aos seguidores.
- Uma entrada no log só é efetivada se a maioria dos seguidores a confirmar em seus logs.
- O líder transmite mensagens periódicas aos seguidores para manter sua autoridade e prevenir novas eleições.

**Comunicação Cliente-Servidor**:

- O cliente se conecta aos servidores Pyro disponíveis.
- O cliente envia comandos ao líder para serem registrados no log e replicados.

Este projeto demonstra como implementar um sistema distribuído utilizando o Algoritmo de Consenso Raft, para garantir consistência e tolerância a falhas.

`Checklist - Repositório`:
- [X] Criar arquivo em Python para o Projeto 2 - Middleware Pyro e Algoritmo de Consenso
- [X] Fazer README.md básico do repositório

`Checklist - Inicialização dos Processos`: 
- [X] Inicialização do servidor de nomes do Pyro;
- [X] Inicialização dos 4 processos que implementam o Raft como seguidores;
- [X] Informar uma porta ao criar o Daemon e um objectId no registro do objeto com o Daemon. Com essas duas informações, teremos o URI "PYRO:objectId@localhost:porta" de cada objeto Pyro e poderemos deixá-los hard coded;
- [X] Inicialização do processo cliente responsável por encaminhar comandos ao líder.

`Checklist - Eleição`: 
- [X] Um dos processos será eleito líder;
- [X] Utilizem temporizadores de eleição aleatórios para evitar que os nós se tornem candidatos ao mesmo tempo;
- [X] Quando um líder falhar, um outro processo será eleito como líder.

`Checklist - Replicação`:
- [X] O cliente pesquisará o URI do líder no servidor de nomes;
- [X] O cliente enviará comandos ao líder;
- [X] O líder será responsável por receber receber comandos dos clientes, anexá-los ao seu log e replicá-los aos seguidores;
- [ ] Uma entrada no log apenas será efetivada (committed) se a maioria dos seguidores confirmarem ela no seu log;
- [ ] O líder transmitirá mensagens periódicas para todos os seguidores para manter sua autoridade e prevenir novas eleições.

`Progresso`: 
![](https://geps.dev/progress/75) 
