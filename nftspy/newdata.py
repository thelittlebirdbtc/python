import json
import csv
import os

def json_to_csv(input_folder="C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\nftspy\\metadata", output_file="C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\nftspy\\newdata.csv"):
    """Converte arquivos JSON em um arquivo CSV, extraindo apenas Rarity, ordenado por tokenId.

    Args:
        input_folder: Caminho para a pasta com os arquivos JSON.
        output_file: Nome do arquivo CSV de saída.
    """

    data_rows = []

    try:
        for filename in os.listdir(input_folder):
            if filename.endswith('.json'):
                file_path = os.path.join(input_folder, filename)

                try:
                    with open(file_path, 'r', encoding='utf-8') as jsonfile:
                        data = json.load(jsonfile)

                        if "tokenId" not in data:
                            print(f"Aviso: 'tokenId' não encontrado no arquivo: {filename}")
                            continue

                        for attribute in data.get("attributes", []):
                            if attribute.get("trait_type") == "Rarity":
                                try:
                                    token_id = int(data["tokenId"])
                                    rarity = attribute["value"]
                                    data_rows.append((token_id, rarity)) # Tupla para ordenação
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

        # Ordena as linhas pelo tokenId (primeiro elemento da tupla)
        data_rows.sort(key=lambda x: x[0])

        # Escreve APENAS a coluna Rarity no arquivo CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Rarity"])  # Cabeçalho: APENAS Rarity
            for _, rarity in data_rows: # Itera pelas tuplas, extraindo apenas a raridade
                writer.writerow([rarity]) # Escreve apenas a raridade

        print(f"Arquivo CSV '{output_file}' criado com sucesso (apenas coluna Rarity, ordenado por tokenId).")

    except OSError as e:
        print(f"Erro de sistema operacional: {e}")
    except Exception as e:
        print(f"Ocorreu um erro geral: {e}")

json_to_csv()