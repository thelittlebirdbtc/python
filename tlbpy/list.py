import csv

def extrair_enderecos_unicos(arquivo_entrada, arquivo_saida):
  """
  Extrai endereços únicos de um arquivo CSV e salva em um novo arquivo.

  Args:
    arquivo_entrada: Caminho para o arquivo CSV de entrada.
    arquivo_saida: Caminho para o arquivo CSV de saída.
  """

  enderecos = set()  # Um conjunto para armazenar endereços únicos
  with open(arquivo_entrada, 'r') as entrada:
    leitor = csv.reader(entrada)
    # Assumindo que a coluna de endereços é a primeira, ajuste o índice se necessário
    for linha in leitor:
      endereco = linha[0]
      enderecos.add(endereco)

  with open(arquivo_saida, 'w', newline='') as saida:
    escritor = csv.writer(saida)
    for endereco in enderecos:
      escritor.writerow([endereco])

# Exemplo de uso
arquivo_entrada = 'C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\tlbpy\\tlbmints.csv'
arquivo_saida = 'C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\tlbpy\\tlbhlist.csv'
extrair_enderecos_unicos(arquivo_entrada, arquivo_saida)