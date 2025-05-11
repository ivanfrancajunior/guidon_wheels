import os

# Caminhos padrão
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Arquivos de descrição
DESCRICAO_CALOTA = os.path.join(TEMPLATES_DIR, "descricao_calota.txt")
DESCRICAO_RODA_FERRO = os.path.join(TEMPLATES_DIR, "descricao_roda_ferro.txt")

# Outras configurações
DEFAULT_PASTA_RAIZ = os.path.join(os.path.expanduser("~"), "Desktop", "output")

TEMPLATE_APROVACAO = """------------------------

*{Fabricante_Modelo}*

Data: {DATA}
Quantidade: {QTD}
Acabamento: {ACABAMENTO}
SKU: {SKU}
*Concorrência: {CONCORRÊNCIA}*
*Preço OLX / Facebook: {OLX_FACE}*
*Preço Mercado Livre: {ML}*

---------------"""