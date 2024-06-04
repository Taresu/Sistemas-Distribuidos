const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = 5100;

app.use(bodyParser.json());
app.use(cors());

// Endpoint para adicionar um livro
app.post('/livros', (req, res) => {
    const { titulo, autor, editora } = req.body;
    const novoLivro = { titulo, autor, editora };
    livros.push(novoLivro);
    res.json({ mensagem: 'Livro cadastrado com sucesso!' });
});

// Endpoint para listar todos os livros
app.get('/livros', (req, res) => {
    res.json(livros);
});

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});