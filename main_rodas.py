#%%
import os
import pandas as pd
import re

# Caminho para a planilha
# planilha_path = r"path_planilha"

planilha_path = r"C:\Users\Junior\Desktop\planilha test_script.xlsx"

# Caminho padrão para a criação das pastas
# pasta_raiz = r"seu_path"

pasta_raiz = r"C:\Users\Junior\Desktop\roda_ferro\teste_mar_25"

# Caminhos para os arquivos de texto base
caminho_descricao_base = r"descricao_roda_ferro_calotao.txt"
caminho_cabecalho_aprovacao = r"cabecalho_aprovacao.txt"

raw_marcas_conhecidas = [
    "VW", "GM", "TOYOTA", "HYUNDAI", "VOLKSWAGEN", "CHEVROLET", "MITSUBISHI", "RENAULT", "CITROEN", "JAC", "NOOVA", "FERRARO",
    "FIAT", "KIA", "MANGELS", "ITAL", "TITANIO", "LIMBRA", "BMW", "LAND ROVER","RANGE ROVER", "BYD", "MINI COOPER", "MANGELS",
    "NISSAN", "MERCEDES", "FORD", "GRID", "ZUNKY", "KRMAI", "MAZDA"
]

# Array de marcas conhecidas
marcas_conhecidas = [label.title() for label in raw_marcas_conhecidas ]

# Ler os textos base dos arquivos
with open(caminho_descricao_base, "r", encoding="utf-8") as arquivo:
    descricao_base = arquivo.read()

with open(caminho_cabecalho_aprovacao, "r", encoding="utf-8") as arquivo:
    cabecalho_aprovacao = arquivo.read()

# Texto base para cada entrada na aprovação
template_aprovacao = """------------------------

*{Fabricante_Modelo}*

Quantidade: {QTD}
Acabamento: {ACABAMENTO}
SKU: {SKU}
*Concorrência: {CONCORRÊNCIA}*
*Preço OLX / Facebook: {OLX_FACE}*
*Preço Mercado Livre: {ML}*

---------------"""

# Função para criar pastas e arquivos
def criar_pastas(planilha_path, pasta_raiz):
    try:
        # Verificar se o arquivo existe
        if not os.path.exists(planilha_path):
            raise FileNotFoundError(f"O arquivo '{planilha_path}' não foi encontrado.")

        # Ler a planilha
        df = pd.read_excel(planilha_path)
        df.columns = df.columns.str.strip()

        # Verificar colunas necessárias
        colunas_necessarias = ["DATA", "FABRICANTE" , "MODELO", "QTD","ET", "ACABAMENTO",  "SKU", "CONCORRÊNCIA", "OLX | FACE", "ML"]

        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                raise KeyError(f"A coluna '{coluna}' não foi encontrada na planilha.")

        # Criar diretório raiz
        if not os.path.exists(pasta_raiz):
            os.makedirs(pasta_raiz)
            print(f"Diretório raiz criado: {pasta_raiz}")

        # Inicializar o contador e lista de aprovações
        contador = 1
        conteudo_aprovacao = cabecalho_aprovacao

        # Iterar sobre os dados da planilha
        for _, row in df.iterrows():
            fabricante= row["FABRICANTE"],
            modelo= row["MODELO"]
            acabamento = row["ACABAMENTO"]
            material = row["MATERIAL"]
            sku = row["SKU"]

            # Lógica para entradas que começam com "Calota Aro"

            # Substituir abreviações de marca
            if fabricante == "VW":
                fabricante = "Volkswagen"
            elif fabricante == "GM":
                fabricante = "Chevrolet"
            elif fabricante == "GRID":
                fabricante = "GRID"  # Mantém "GRID" como marca

            # Remover caracteres inválidos do nome da pasta
            nome_formatado = ''.join(c for c in modelo if c.isalnum() or c in (' ', '_')).strip()
            nome_formatado = nome_formatado.replace(' ', '_')
            nome_pasta = f"{str(contador).zfill(2)}_{nome_formatado}"
            nova_pasta = os.path.join(pasta_raiz, nome_pasta)

            # Criar pasta
            if not os.path.exists(nova_pasta):
                os.makedirs(nova_pasta)
                print(f"Pasta criada: {nova_pasta}")

            # Criar descrição
            arquivo_descricao = os.path.join(nova_pasta, "descricao.txt")
            with open(arquivo_descricao, "w", encoding="utf-8") as arquivo:
                descricao = descricao_base.format(
                    Marca=fabricante,
                    Modelo=modelo,
                    Aro='AROXTALA',
                    cor=acabamento,
                    Material=material,
                    sku=sku
                )
                arquivo.write(descricao)
                print(f"Arquivo de descrição criado: {arquivo_descricao}")

            # Adicionar informações ao conteúdo de aprovação
            conteudo_aprovacao += template_aprovacao.format(
                Fabricante_Modelo=f"{modelo}",
                DATA=row["DATA"],
                QTD=row["QTD"],
                ACABAMENTO=["ACABAMENTO"],
                SKU=["SKU"],
                CONCORRÊNCIA=row["CONCORRÊNCIA"],
                OLX_FACE=row["OLX | FACE"],
                ML=row["ML"]
            )

            contador += 1

        # Criar o arquivo de aprovação no diretório raiz
        arquivo_aprovacao = os.path.join(pasta_raiz, "aprovacao.txt")
        with open(arquivo_aprovacao, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo_aprovacao)
            print(f"Arquivo de aprovação criado: {arquivo_aprovacao}")

    except Exception as e:
        print(f"Erro: {e}")

# Executar a função
criar_pastas(planilha_path, pasta_raiz)
# %%
