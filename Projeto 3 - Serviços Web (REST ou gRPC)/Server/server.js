const express = require('express');
const bodyParser = require('body-parser');
const forge = require('node-forge');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3500;

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, '../frontend')));

const bibliotecarioPublicKey = fs.readFileSync('./keys/bibliotecario_publica.pem', 'utf8');
const clientePublicKey = fs.readFileSync('./keys/cliente_publica.pem', 'utf8');

app.post('/authenticate', (req, res) => {
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

app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});