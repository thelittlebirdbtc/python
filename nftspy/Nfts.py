import csv
import os
import shutil

def processar_csv(
    caminho_csv = "C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\nftspy\\metadata.csv", 
    pasta_balls = "C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\nftspy\\webp", 
    pasta_nfts = "C:\\Users\\jhosephethierry\\Documents\\Bird\\python\\nftspy\\nfts"
    ):
    """
    Processa um arquivo CSV, copiando arquivos de vídeo com base na raridade.

    Args:
        caminho_csv: Caminho para o arquivo CSV.
        pasta_balls: Caminho para a pasta contendo os vídeos originais.
        pasta_nfts: Caminho para a pasta onde os vídeos serão copiados.
    """

    try:
        with open(caminho_csv, 'r', encoding='utf-8') as arquivo_csv:  # encoding utf-8 para lidar com caracteres especiais
            leitor_csv = csv.DictReader(arquivo_csv)

            if not os.path.exists(pasta_nfts):
                os.makedirs(pasta_nfts) # Cria a pasta NFTs caso não exista

            for linha in leitor_csv:
                token_id = linha.get('tokenId')
                raridade = linha.get('Rarity')

                if not token_id or not raridade:
                    print(f"Aviso: Linha com tokenId ou Rarity faltando: {linha}")
                    continue # Pula para a proxima iteração

                nome_arquivo_origem = f"{raridade}.webp"
                caminho_origem = os.path.join(pasta_balls, nome_arquivo_origem)

                if not os.path.exists(caminho_origem):
                    print(f"Aviso: Arquivo não encontrado: {caminho_origem}")
                    continue # Pula para a proxima iteração

                nome_arquivo_destino = f"Stone {token_id.zfill(4)} {raridade}.webp"
                caminho_destino = os.path.join(pasta_nfts, nome_arquivo_destino)

                try:
                    shutil.copy2(caminho_origem, caminho_destino) # Usando copy2 para preservar metadados
                    print(f"Arquivo copiado: {nome_arquivo_origem} para {nome_arquivo_destino}")
                except Exception as e:
                    print(f"Erro ao copiar arquivo: {e}")

    except FileNotFoundError:
        print(f"Erro: Arquivo CSV não encontrado: {caminho_csv}")
    except csv.Error as e:
        print(f"Erro ao ler CSV: {e}")
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}")


processar_csv()