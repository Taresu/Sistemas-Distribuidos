import pandas as pd

tabela = pd.read_csv('Projeto 3 - Serviços Web (REST ou gRPC)/Train/advertising.csv')

total_vendas = tabela['Vendas'].sum()

print(total_vendas)