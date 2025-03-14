import os
import pandas as pd


planilha_path = ""  # C:\Users\Guidom\Desktop\guidom_rodas
coluna_nomes = "Nomes"  # Nome da coluna na planilha 

pasta_raiz = "" # C:\Users\Guido\Desktop\calotas\12_mar_25

# Função para criar pastas com base nos nomes da planilha
def criar_pastas(planilha_path, coluna_nomes, pasta_raiz):
    try:
        # Verificar se o arquivo existe
        if not os.path.exists(planilha_path):
            raise FileNotFoundError(f"Arquivo não encontrado: '{planilha_path}'")

        # Ler a planilha com base na extensão
        if planilha_path.endswith('.csv'):
            df = pd.read_csv(planilha_path)  # Para arquivos CSV
        elif planilha_path.endswith('.xlsx'):
            df = pd.read_excel(planilha_path)  # Para arquivos Excel (.xlsx)
        else:
            raise ValueError("Formato de arquivo não suportado. Use .csv ou .xlsx.")


        if coluna_nomes not in df.columns:
            raise KeyError(f"A coluna '{coluna_nomes}' não foi encontrada na planilha.")


        if not os.path.exists(pasta_raiz):
            os.makedirs(pasta_raiz)
            print(f"Diretório raiz criado: {pasta_raiz}")


        contador = 1


        for nome in df[coluna_nomes]:

            nome_formatado = ''.join(c for c in str(nome) if c.isalnum() or c in (' ', '_')).strip()
            nome_formatado = nome_formatado.replace(' ', '_')


            nome_pasta = f"{str(contador).zfill(2)}_{nome_formatado}"
            nova_pasta = os.path.join(pasta_raiz, nome_pasta)


            if not os.path.exists(nova_pasta):
                os.makedirs(nova_pasta)
                print(f"Pasta criada: {nova_pasta}")
            else:
                print(f"Pasta já existe: {nova_pasta}")


            contador += 1

    except Exception as e:
        print(f"Erro ao criar pastas: {e}")


criar_pastas(planilha_path, coluna_nomes, pasta_raiz)