const url = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('livro-form');
    const listaLivros = document.getElementById('lista-livros');

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const titulo = document.getElementById('titulo').value;
        const autor = document.getElementById('autor').value;
        const editora = document.getElementById('editora').value;

        var urlFunction = url + '/livros';

        fetch(urlFunction, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ titulo, autor, editora })
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensagem === 'Livro cadastrado com sucesso!') {
                alert(data.mensagem);
                carregarLivros(); // Atualiza a lista de livros
            } else {
                alert('Erro: ' + data.mensagem);
            }
        })
        .catch(error => console.error('Erro:', error));
    });

    async function carregarLivros() {

        var urlFunction = url + '/livros';
        fetch(urlFunction)
            .then(response => response.json())
            .then(data => {
                listaLivros.innerHTML = '';
                data.forEach(livro => {
                    const li = document.createElement('li');
                    li.textContent = `${livro.titulo} - ${livro.autor} (${livro.editora})`;
                    listaLivros.appendChild(li);
                });
            })
            .catch(error => console.error('Erro carregar Livros:', error));
    }

    // Carrega os livros ao iniciar a página
    carregarLivros();
});