Para gerar o par de chaves, podemos usar a ferramenta openssl:

openssl genpkey -algorithm RSA -out bibliotecario_privada.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in bibliotecario_privada.pem -out bibliotecario_publica.pem

openssl genpkey -algorithm RSA -out cliente_privada.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in cliente_privada.pem -out cliente_publica.pem
