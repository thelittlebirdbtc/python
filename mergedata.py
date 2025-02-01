import json
import csv
import os

def json_to_csv(input_folder="C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\nftspy\\metadata", output_file="C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\nftspy\\metadata.csv"):
    """Converte arquivos JSON em um arquivo CSV, extraindo tokenId e Rarity, e ordenando por tokenId.

    Args:
        input_folder: Caminho para a pasta com os arquivos JSON.
        output_file: Nome do arquivo CSV de saída.
    """

    data_rows = []  # Lista para armazenar as linhas de dados antes de escrever no CSV

    try:
        for filename in os.listdir(input_folder):
            if filename.endswith('.json'):
                file_path = os.path.join(input_folder, filename)

                try:
                    with open(file_path, 'r', encoding='utf-8') as jsonfile:  # Adicionado encoding UTF-8
                        data = json.load(jsonfile)

                        # Verifica se "tokenId" existe no JSON
                        if "tokenId" not in data:
                            print(f"Aviso: 'tokenId' não encontrado no arquivo: {filename}")
                            continue

                        for attribute in data.get("attributes", []): # Usando .get para evitar KeyError se "attributes" não existir
                            if attribute.get("trait_type") == "Rarity": # Usando .get para evitar KeyError se "trait_type" não existir
                                try:
                                    token_id = int(data["tokenId"]) # Converte para inteiro para ordenação numérica
                                    row = [token_id, attribute["value"]] # Inclui o tokenId na linha
                                    data_rows.append(row)
                                except ValueError:
                                    print(f"Aviso: 'tokenId' com valor não numérico no arquivo: {filename}. Valor: {data['tokenId']}")
                                except KeyError as e:
                                    print(f"Erro: Chave '{e}' não encontrada em {filename}")

                except json.JSONDecodeError:
                    print(f"Erro: Arquivo JSON inválido: {filename}")
                except FileNotFoundError:
                    print(f"Erro: Arquivo não encontrado: {filename}")
                except Exception as e:
                    print(f"Erro ao processar o arquivo {filename}: {e}")

        # Ordena as linhas pelo tokenId (primeiro elemento de cada linha)
        data_rows.sort(key=lambda x: x[0])

        # Escreve os dados ordenados no arquivo CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile: # Adicionado encoding UTF-8
            writer = csv.writer(csvfile)
            writer.writerow(["tokenId", "Rarity"])  # Escreve o cabeçalho CORRETO
            writer.writerows(data_rows)

        print(f"Arquivo CSV '{output_file}' criado com sucesso e ordenado por tokenId.")

    except OSError as e:
        print(f"Erro de sistema operacional: {e}")
    except Exception as e:
        print(f"Ocorreu um erro geral: {e}")

json_to_csv()