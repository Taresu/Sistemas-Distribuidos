import psycopg2

# Parâmetros de conexão ao PostgreSQL
DB_NAME = "biblioteca"
DB_USER = "postgres"
DB_PASSWORD = "utfpr"
DB_HOST = "localhost"
DB_PORT = 5432

# Criando a conexão com o banco de dados
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

# Criando um cursor para executar consultas
cursor = conn.cursor()