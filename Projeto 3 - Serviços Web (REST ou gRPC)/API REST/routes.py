from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Livro, db

app = Flask(__name__)

# Banco de dados para a aplicação
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/Biblioteca'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Para desabilitar um aviso desnecessário
db.init_app(app)
CORS(app)

# Gerando o par de chaves para a criptografia assimétrica
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

def sign_message(message):
    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature.hex()

# Rota para cadastrar um novo livro
@app.route('/livros', methods=['POST'])
def cadastrar_livro():
    dados = request.get_json()
    titulo = dados['titulo']
    autor = dados['autor']
    editora = dados['editora']

    novo_livro = Livro(titulo=titulo, autor=autor, editora=editora)

    # Salvar o novo livro no banco de dados
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
        livros = Livro.query.all()
        # Converte os objetos Livro em lista de dicionários
        livros_json = [{'id': livro.id, 'titulo': livro.titulo, 'autor': livro.autor, 'editora': livro.editora} for livro in livros]
        livros_str = str(livros_json)
        signature = sign_message(livros_str)
        print("Mensagem:", livros_str)
        print("Assinatura:", signature)        
        return jsonify({'livros': livros_json, 'signature': signature}), 200
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao obter livros: {str(e)}'}), 500


@app.route('/public_key', methods=['GET'])
def get_public_key():
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return jsonify({'public_key': public_pem.decode()}), 200

if __name__ == '__main__':
    app.run(debug=True)
