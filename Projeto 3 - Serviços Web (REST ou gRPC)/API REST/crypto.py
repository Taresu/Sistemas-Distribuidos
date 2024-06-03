from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# Gerar chave privada
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Gerar chave pública
public_key = private_key.public_key()

# # Converte a chaves para bytes.
# private_pem = private_key.private_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PrivateFormat.PKCS8,
#     encryption_algorithm=serialization.NoEncryption()
# )

# public_pem = public_key.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
# )

# # Salvar as chaves em arquivos (opcional)
# with open("private_key.pem", "wb") as private_file:
#     private_file.write(private_pem)

# with open("public_key.pem", "wb") as public_file:
#     public_file.write(public_pem)
