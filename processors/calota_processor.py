from processors.base_processor import ProdutoProcessor
from utils.helpers import formatar_nome_pasta
from config import TEMPLATE_APROVACAO

class CalotaProcessor(ProdutoProcessor):
    def processar(self):
        """Processa os dados específicos para calotas."""
        colunas_necessarias = ["DATA", "FABRICANTE", "MODELO","DIÂMETRO","QTD", "ACABAMENTO", "MATERIAL", "SKU"]
        self.carregar_planilha(colunas_necessarias)

        contador = 1
        for _, row in self.dados.iterrows():
            fabricante = row["FABRICANTE"],
            modelo = row["MODELO"],
            diametro = row["DIÂMETRO"],
            nome_pasta = f"{str(contador).zfill(2)}_{formatar_nome_pasta(row['MODELO'])}"
            pasta = self.criar_pasta(nome_pasta)

            dados_produto = {
                "Marca": row["FABRICANTE"],
                "Modelo": row["MODELO"],
                "Diametro": row["DIÂMETRO"],
                "cor": row["ACABAMENTO"],
                "Material": row["MATERIAL"],
                "sku": row["SKU"]
            }
            self.criar_descricao(pasta, dados_produto)
            contador += 1

        # Criar arquivo de aprovação
        self.criar_aprovacao(TEMPLATE_APROVACAO)