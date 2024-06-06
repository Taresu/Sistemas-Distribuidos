document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio padrão do formulário

    const userType = document.querySelector('input[name="userType"]:checked').value;
    const privateKeyFile = document.getElementById('privateKeyFile').files[0];

    if (!privateKeyFile) {
        alert('Por favor, carregue sua chave privada.');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(event) {
        const privateKeyPem = event.target.result;

        try {
            const privateKey = forge.pki.privateKeyFromPem(privateKeyPem);

            // Gera um desafio (aqui estamos usando o tipo de usuário + timestamp)
            const challenge = userType + new Date().getTime();
            const md = forge.md.sha256.create();
            md.update(challenge);
            const hashedChallenge = md.digest().bytes();

            const signature = forge.util.encode64(privateKey.sign(md));

            fetch('/authenticate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: userType,
                        challenge: challenge,
                        signature: signature
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.redirectUrl) {
                        window.location.href = data.redirectUrl; // Redireciona para a URL recebida
                    } else {
                        alert('Autenticação falhou');
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    alert('Ocorreu um erro durante a autenticação');
                });
        } catch (error) {
            console.error('Erro ao processar a chave privada:', error);
            alert('Chave privada inválida.');
        }
    };

    reader.readAsText(privateKeyFile);
});