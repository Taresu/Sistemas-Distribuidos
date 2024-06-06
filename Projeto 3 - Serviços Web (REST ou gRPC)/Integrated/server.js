const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { Pool } = require('pg');
const forge = require('node-forge');
const fs = require('fs');
const morgan = require('morgan');
const WebSocket = require('ws');

const app = express();
const PORT = 3500;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'frontend')));

const bibliotecarioPublicKey = fs.readFileSync('./keys/bibliotecario_publica.pem', 'utf8');
const clientePublicKey = fs.readFileSync('./keys/cliente_publica.pem', 'utf8');

// Configuração do pool de banco de dados
const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'Biblioteca',
    password: 'postgres',
    port: 5432,
});

// Configuração do servidor WebSocket
const wss = new WebSocket.Server({ port: 8080 });

// Middleware para capturar mensagens HTTP e enviá-las por WebSocket
app.use((req, res, next) => {
    res.on('finish', () => {
        const message = `${req.method} ${req.originalUrl} ${res.statusCode} ${res.statusMessage}`;
        wss.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify({ type: 'http', message: message }));
            }
        });
    });
    next();
});

// Rota para eventos SSE
app.get('/stream', (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    // Função para enviar eventos SSE periodicamente
    const sendSSE = () => {
        res.write('data: {"message": "Evento do servidor"}\n\n');
    };

    // Envie um evento SSE a cada 3 segundos
    const intervalId = setInterval(sendSSE, 3000);

    // Encerre a conexão ao cliente quando ele fechar
    req.on('close', () => {
        clearInterval(intervalId);
        console.log('Conexão SSE encerrada');
    });
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/login.html'));
});

app.post('/authenticate', async(req, res) => {
    const { username, challenge, signature } = req.body;

    let publicKeyPem;
    if (username === 'bibliotecario') {
        publicKeyPem = bibliotecarioPublicKey;
    } else if (username === 'cliente') {
        publicKeyPem = clientePublicKey;
    } else {
        return res.status(401).json({ message: 'Usuário não encontrado' });
    }

    const publicKey = forge.pki.publicKeyFromPem(publicKeyPem);
    const md = forge.md.sha256.create();
    md.update(challenge, 'utf8');

    const isVerified = publicKey.verify(md.digest().bytes(), forge.util.decode64(signature));

    if (isVerified) {
        if (username === 'bibliotecario') {
            res.json({ redirectUrl: 'edicao_banco.html' });
        } else {
            res.json({ redirectUrl: 'lista_livros.html' });
        }
    } else {
        res.status(401).json({ message: 'Autenticação falhou' });
    }
});

app.get('/livros', async(req, res) => {
    try {
        const { rows } = await pool.query('SELECT * FROM livros');
        res.json(rows);
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Erro ao buscar livros' });
    }
});

app.post('/livros', async(req, res) => {
    try {
        const { titulo, autor, editora } = req.body;
        await pool.query('INSERT INTO livros (titulo, autor, editora) VALUES ($1, $2, $3)', [titulo, autor, editora]);
        res.status(201).json({ message: 'Livro cadastrado com sucesso!' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Erro ao cadastrar livro' });
    }
});

app.put('/livros/:id', async(req, res) => {
    try {
        const { id } = req.params;
        const { titulo, autor, editora } = req.body;
        await pool.query('UPDATE livros SET titulo = $1, autor = $2, editora = $3 WHERE id = $4', [titulo, autor, editora, id]);
        res.json({ message: 'Livro atualizado com sucesso' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Erro ao atualizar livro' });
    }
});

app.delete('/livros/:id', async(req, res) => {
    try {
        const { id } = req.params;
        await pool.query('DELETE FROM livros WHERE id = $1', [id]);
        res.json({ message: 'Livro deletado com sucesso' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ message: 'Erro ao deletar livro' });
    }
});

app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});