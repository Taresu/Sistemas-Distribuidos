Dependências:
- npm install express body-parser node-forge fs path pg morgan ws

Para testar o SSE:
  - sudo service redis-server start
  - redis-cli
  - ping
  - curl http://localhost:5000/stream (novo terminal)