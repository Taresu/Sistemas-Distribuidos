const url = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('livro-form');
    const listaLivros = document.getElementById('lista-livros');

    form.addEventListener('submit', async(event) => {
        event.preventDefault();

        const titulo = document.getElementById('titulo').value;
        const autor = document.getElementById('autor').value;
        const editora = document.getElementById('editora').value;

        var urlFunction = url + '/livros';
        try {
            const response = await fetch(urlFunction, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ titulo, autor, editora })
            });
            const data = await response.json();
            if (data.mensagem === 'Livro cadastrado com sucesso!') {
                alert(data.mensagem);
                carregarLivros(); // Atualiza a lista de livros
            } else {
                alert('Erro: ' + data.mensagem);
            }
        } catch (error) {
            console.error('Erro Cadastrar Livros:', error);
        }
    });

    async function carregarLivros() {
        var urlFunction = url + '/livros';
        try {
            const response = await fetch(urlFunction);
            const data = await response.json();

            // Verifique se 'data' é um array
            if (Array.isArray(data)) {
                listaLivros.innerHTML = '';
                data.forEach(livro => {
                    const li = document.createElement('li');
                    li.textContent = `${livro.titulo} - ${livro.autor} (${livro.editora})`;
                    listaLivros.appendChild(li);
                });
            } else {
                console.error('Erro: a resposta não é um array.', data);
            }
        } catch (error) {
            console.error('Erro carregar Livros:', error);
        }
    }

    // Carrega os livros ao iniciar a página
    carregarLivros();
});

// --------------- PARTE DA AUTENTICAÇÃO

document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Simular um desafio do servidor
    const challenge = '123456';

    // Função para simular a assinatura do desafio
    function signChallenge(challenge, privateKeyPem) {
        const privateKey = forge.pki.privateKeyFromPem(privateKeyPem);
        const md = forge.md.sha256.create();
        md.update(challenge, 'utf8');
        return forge.util.encode64(privateKey.sign(md));
    }

    // Simular a recuperação da chave privada do usuário (aqui simplificado para demonstração)
    let privateKeyPem;
    if (username === 'bibliotecario') {
        privateKeyPem = `-----BEGIN RSA PRIVATE KEY-----
... // Your librarian private key here
-----END RSA PRIVATE KEY-----`;
    } else if (username === 'cliente') {
        privateKeyPem = `-----BEGIN RSA PRIVATE KEY-----
... // Your client private key here
-----END RSA PRIVATE KEY-----`;
    } else {
        alert('Usuário não encontrado');
        return;
    }

    // Assinar o desafio
    const signature = signChallenge(challenge, privateKeyPem);

    // Enviar a assinatura para o servidor
    fetch('/authenticate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, challenge, signature })
        })
        .then(response => response.json())
        .then(data => {
            if (data.redirectUrl) {
                window.location.href = data.redirectUrl;
            } else {
                alert('Falha na autenticação');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
});