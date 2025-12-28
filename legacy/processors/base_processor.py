import os
import pandas as pd


class ProdutoProcessor:
    def __init__(self, planilha_path, pasta_raiz, descricao_base):
        self.planilha_path = planilha_path
        self.pasta_raiz = pasta_raiz
        self.descricao_base = descricao_base
        self.dados = None

    def carregar_planilha(self, colunas_necessarias):
        """Carrega a planilha e valida as colunas necessárias."""
        try:
            if not os.path.exists(self.planilha_path):
                raise FileNotFoundError(f"O arquivo '{self.planilha_path}' não foi encontrado.")

            self.dados = pd.read_excel(self.planilha_path)
            self.dados.columns = self.dados.columns.str.strip()

            for coluna in colunas_necessarias:
                if coluna not in self.dados.columns:
                    raise KeyError(f"A coluna '{coluna}' não foi encontrada na planilha.")

        except Exception as e:
            raise ValueError(f"Erro ao carregar a planilha: {e}")

    def criar_pasta(self, nome_pasta):
        """Cria uma pasta dentro da pasta raiz."""
        caminho_completo = os.path.join(self.pasta_raiz, nome_pasta)
        if not os.path.exists(caminho_completo):
            os.makedirs(caminho_completo)
        return caminho_completo

    def criar_descricao(self, pasta, dados_produto):
        """Cria um arquivo de descrição dentro da pasta."""
        descricao = self.descricao_base.format(**dados_produto)
        caminho_arquivo = os.path.join(pasta, "descricao.txt")
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(descricao)

    def criar_aprovacao(self, template_aprovacao):
        """Cria o arquivo consolidado de aprovação no diretório raiz."""
        conteudo_aprovacao = "=== Aprovação ===\n"
        for _, row in self.dados.iterrows():

            try:
                olx_face = round(float(row.get("OLX | FACE", 0)), 2)
                ml = round(float(row.get("ML", "")), 2)

            except ValueError:
                olx_face = 0.00
                ml = 0.00

            conteudo_aprovacao += template_aprovacao.format(
                 DATA=row.get("DATA", ""),
                Fabricante_Modelo=row.get("MODELO", row.get("MODELO", "")),
                QTD=row.get("QTD", ""),
                ACABAMENTO=row.get("ACABAMENTO", ""),
                SKU=row.get("SKU", ""),
                CONCORRÊNCIA=row.get("CONCORRÊNCIA", ""),
                OLX_FACE=olx_face,
                ML=ml
            )
            conteudo_aprovacao += "\n"

        caminho_arquivo = os.path.join(self.pasta_raiz, "aprovacao.txt")
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo_aprovacao)
        print(f"Arquivo de aprovação criado: {caminho_arquivo}")