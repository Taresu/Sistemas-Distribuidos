from flask import Flask, jsonify, request
from models import Livro, db
from flask_cors import CORS

app = Flask(__name__)


# Configurando o banco de dados para a aplicação
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:utfpr@localhost:5432/biblioteca'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para desabilitar um aviso desnecessário
db.init_app(app)
CORS(app)

# Rota para cadastrar um novo livro
@app.route('/livros', methods=['POST'])
def cadastrar_livro():
    # Recebendo os dados do JSON na requisição
    dados = request.get_json()
    titulo = dados['titulo']
    autor = dados['autor']
    editora = dados['editora']

    # Criando um novo objeto 'Livro'
    novo_livro = Livro(titulo=titulo, autor=autor, editora=editora)

    # Tentando salvar o novo livro no banco de dados
    try:
        db.session.add(novo_livro)
        db.session.commit()
        return jsonify({'mensagem': 'Livro cadastrado com sucesso!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'mensagem': 'Erro ao cadastrar livro.'}), 500

@app.route('/livros', methods=['GET'])
def obter_livros():
    try:
        # Consulta todos os livros no banco de dados
        livros = Livro.query.all()
        # Converte os objetos Livro em um formato serializável (lista de dicionários)
        livros_json = [{'id': livro.id, 'titulo': livro.titulo, 'autor': livro.autor, 'editora': livro.editora} for livro in livros]
        return jsonify(livros_json), 200
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao obter livros: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
