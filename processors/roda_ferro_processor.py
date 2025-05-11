from processors.base_processor import ProdutoProcessor
from utils.helpers import formatar_nome_pasta
from config import TEMPLATE_APROVACAO

class RodaFerroProcessor(ProdutoProcessor):
    def processar(self):
        """Processa os dados específicos para rodas de ferro."""
        colunas_necessarias = ["DATA", "FABRICANTE", "MODELO", "QTD", "ACABAMENTO", "MATERIAL", "SKU"]
        self.carregar_planilha(colunas_necessarias)

        contador = 1
        for _, row in self.dados.iterrows():
            fabricante = row["FABRICANTE"]
            modelo = row["MODELO"]

            # Substituir abreviações de marca, se necessário
            if fabricante == "VW":
                fabricante = "Volkswagen"
            elif fabricante == "GM":
                fabricante = "Chevrolet"

            # Formatar nome da pasta
            nome_formatado = f"{fabricante}_{modelo}"
            nome_pasta = f"{str(contador).zfill(2)}_{formatar_nome_pasta(nome_formatado)}"
            pasta = self.criar_pasta(nome_pasta)

            # Dados para a descrição
            dados_produto = {
                "Marca": fabricante,
                "Modelo": modelo,
                "Aro": "AROXTALA",  # Exemplo, ajuste conforme necessário
                "cor": row["ACABAMENTO"],
                "Material": row["MATERIAL"],
                "sku": row["SKU"]
            }
            self.criar_descricao(pasta, dados_produto)
            contador += 1

        # Criar arquivo de aprovação
        self.criar_aprovacao(TEMPLATE_APROVACAO)