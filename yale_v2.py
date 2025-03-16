import os
import pandas as pd

# Caminho para a planilha
planilha_path = r"C:\Users\Junior\Downloads\planilha_guidon_ roda_de_ferro_e_calota.xlsx"  # Altere para o caminho da sua planilha

# Caminho padrão para a criação das pastas
pasta_raiz = r"C:\Users\Junior\Desktop\calotas\teste_mar_25"

# Caminhos para os arquivos de texto base
caminho_descricao_base = r"descricao_base.txt"
caminho_cabecalho_aprovacao = r"cabecalho_aprovacao.txt"

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

        # Ler a planilha com base na extensão
        if planilha_path.endswith('.csv'):
            df = pd.read_csv(planilha_path)
        elif planilha_path.endswith('.xlsx'):
            df = pd.read_excel(planilha_path)
        else:
            raise ValueError("Formato de arquivo não suportado. Use .csv ou .xlsx.")

        # Remover espaços extras dos nomes das colunas
        df.columns = df.columns.str.strip()

        # Verificar se as colunas necessárias existem
        colunas_necessarias = [
            "DATA", "FABRICANTE | MODELO", "ANO", "QTD", "ACABAMENTO", "MATERIAL",
            "NÚMERO DE PEÇA / SKU", "CONCORRÊNCIA", "OLX | FACE", "ML", "TOTAL", "POSTADO", "VISITAS", 'USADO'
        ]
        for coluna in colunas_necessarias:
            if coluna not in df.columns:
                raise KeyError(f"A coluna '{coluna}' não foi encontrada na planilha.")

        # Criar o diretório raiz se ele não existir
        if not os.path.exists(pasta_raiz):
            os.makedirs(pasta_raiz)
            print(f"Diretório raiz criado: {pasta_raiz}")

        # Inicializar o contador e lista de aprovações
        contador = 1
        conteudo_aprovacao = cabecalho_aprovacao

        # Iterar sobre os dados da planilha
        for _, row in df.iterrows():
            data = row["DATA"]
            fabricante_modelo = row["FABRICANTE | MODELO"]
            ano = row["ANO"]  # Usado apenas no arquivo individual
            qtd = row["QTD"]
            acabamento = row["ACABAMENTO"]
            material = row["MATERIAL"]
            sku = row["NÚMERO DE PEÇA / SKU"]
            concorrencia = row["CONCORRÊNCIA"]
            olx_face = row["OLX | FACE"]
            ml = row["ML"]
            total = row["TOTAL"]
            postado = row["POSTADO"]
            visitas = row["USADO"]

            # Remover o prefixo "Calota Aro ..." se existir
            if fabricante_modelo.startswith("Calota Aro"):
                fabricante_modelo = fabricante_modelo.replace("Calota Aro ", "", 1)

            # Separar marca e modelo
            partes = fabricante_modelo.split(" ", 1)
            if len(partes) == 2:
                marca, modelo = partes
            else:
                marca, modelo = "Desconhecido", fabricante_modelo

            # Extrair o diâmetro (aro)
            if modelo and modelo[0].isdigit():
                aro = modelo[:2]  # Assume que o diâmetro está nos primeiros 2 caracteres
                modelo = modelo[2:].strip()  # Remove o diâmetro do modelo
            else:
                aro = "Desconhecido"

            # Corrigir o modelo (remover palavras indesejadas como "Grid")
            modelo = modelo.replace("Grid", "").strip()

            cor = acabamento  # Assume que "Acabamento" é a cor

            # Remover caracteres inválidos e substituir espaços por underscores
            nome_formatado = ''.join(c for c in fabricante_modelo if c.isalnum() or c in (' ', '_')).strip()
            nome_formatado = nome_formatado.replace(' ', '_')

            # Adicionar o contador ao nome da pasta
            nome_pasta = f"{str(contador).zfill(2)}_{nome_formatado}"
            nova_pasta = os.path.join(pasta_raiz, nome_pasta)

            # Criar a pasta se ela ainda não existir
            if not os.path.exists(nova_pasta):
                os.makedirs(nova_pasta)
                print(f"Pasta criada: {nova_pasta}")
            else:
                print(f"Pasta já existe: {nova_pasta}")

            # Criar o arquivo de descrição dentro da pasta
            arquivo_descricao = os.path.join(nova_pasta, "descricao.txt")
            with open(arquivo_descricao, "w", encoding="utf-8") as arquivo:
                descricao = descricao_base.format(
                    Marca=marca,
                    Modelo=modelo,
                    Aro=aro,
                    cor=cor,
                    Material=material,
                    sku=sku
                )
                arquivo.write(descricao)
                print(f"Arquivo de descrição criado: {arquivo_descricao}")

            # Adicionar informações ao conteúdo de aprovação
            conteudo_aprovacao += template_aprovacao.format(
                Fabricante_Modelo=fabricante_modelo,
                DATA=data,
                QTD=qtd,
                ACABAMENTO=acabamento,
                SKU=sku,
                CONCORRÊNCIA=concorrencia,
                OLX_FACE=olx_face,
                ML=ml
            )

            contador += 1

        # Criar o arquivo de aprovação no diretório raiz
        arquivo_aprovacao = os.path.join(pasta_raiz, "aprovacao.txt")
        with open(arquivo_aprovacao, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo_aprovacao)
            print(f"Arquivo de aprovação criado: {arquivo_aprovacao}")

    except Exception as e:
        print(f"Erro ao criar pastas: {e}")

# Executar a função
criar_pastas(planilha_path, pasta_raiz)