document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('livro-form');
    const listaLivros = document.getElementById('lista-livros');

    // Evento de clique para o botão de edição
    listaLivros.addEventListener('click', (event) => {
        if (event.target.classList.contains('edit-button')) {
            const listItem = event.target.parentElement;
            const editForm = listItem.querySelector('.edit-form');
            editForm.style.display = 'block';
        }
    });

    // Evento de envio para o formulário de edição
    listaLivros.addEventListener('submit', async(event) => {
        event.preventDefault();
        if (event.target.classList.contains('edit-form')) {
            const listItem = event.target.parentElement;
            const livroId = listItem.dataset.id;
            const titulo = listItem.querySelector('.edit-titulo').value;
            const autor = listItem.querySelector('.edit-autor').value;
            const editora = listItem.querySelector('.edit-editora').value;

            try {
                const response = await fetch(`http://localhost:3500/livros/${livroId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        titulo,
                        autor,
                        editora
                    })
                });
                const data = await response.json();
                if (response.ok) {
                    alert(data.message);
                    carregarLivros();
                } else {
                    alert('Erro: ' + data.message);
                }
            } catch (error) {
                console.error('Erro ao editar livro:', error);
            }
        }
    });

    form.addEventListener('submit', async(event) => {
        event.preventDefault();

        const titulo = document.getElementById('titulo').value;
        const autor = document.getElementById('autor').value;
        const editora = document.getElementById('editora').value;

        try {
            const response = await fetch('http://localhost:3500/livros', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ titulo, autor, editora })
            });
            const data = await response.json();
            if (response.ok) {
                alert(data.message);
                carregarLivros(); // Atualiza a lista de livros
            } else {
                alert('Erro: ' + data.message);
            }
        } catch (error) {
            console.error('Erro ao adicionar livro:', error);
        }
    });

    async function carregarLivros() {
        try {
            const response = await fetch('http://localhost:3500/livros');
            const data = await response.json();

            // Verifique se 'data' é um array
            if (Array.isArray(data)) {
                listaLivros.innerHTML = '';
                data.forEach(livro => {
                    const li = document.createElement('li');
                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'X';
                    deleteButton.addEventListener('click', async() => {
                        try {
                            const response = await fetch(`http://localhost:3500/livros/${livro.id}`, {
                                method: 'DELETE'
                            });
                            const deleteData = await response.json();
                            if (response.ok) {
                                alert(deleteData.message);
                                carregarLivros(); // Atualiza a lista de livros após excluir
                            } else {
                                alert('Erro ao excluir livro: ' + deleteData.message);
                            }
                        } catch (error) {
                            console.error('Erro ao excluir livro:', error);
                        }
                    });
                    li.textContent = `${livro.titulo} - ${livro.autor} (${livro.editora}) `;
                    li.appendChild(deleteButton);
                    listaLivros.appendChild(li);
                });
            } else {
                console.error('Erro: a resposta não é um array.', data);
            }
        } catch (error) {
            console.error('Erro ao carregar livros:', error);
        }
    }

    // Carrega os livros ao iniciar a página
    carregarLivros();
});