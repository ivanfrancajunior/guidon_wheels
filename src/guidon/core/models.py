from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Optional

# -------------------------------------------------------------------------
# CLASSE BASE: Regras que valem para Calotas E Rodas
# -------------------------------------------------------------------------
class ProdutoBase(BaseModel):
    # 'alias' serve para ler a coluna do Excel com nome feio e salvar na variável bonita
    fabricante: str = Field(..., alias="FABRICANTE")
    modelo: str = Field(..., alias="MODELO")
    sku: str = Field(..., alias="SKU")

    # Campos com valor padrão (se a célula estiver vazia no Excel)
    qtd: int = Field(default=0, alias="QTD")
    acabamento: str = Field(default="", alias="ACABAMENTO")
    material: str = Field(default="", alias="MATERIAL")

    # Preços
    preco_olx: float = Field(default=0.0, alias="OLX | FACE")
    preco_ml: float = Field(default=0.0, alias="ML")
    concorrencia: str = Field(default="", alias="CONCORRÊNCIA")

    # --- VALIDADOR 1: Limpeza de Texto ---
    # Roda automaticamente antes de salvar os dados.
    # Substitui aquele monte de .strip() e .upper() que tinha no seu código.
    @field_validator('fabricante', 'modelo', 'acabamento', 'material', mode='before')
    def normalizar_texto(cls, v):
        if isinstance(v, str):
            return v.strip().upper()
        return v

    # --- VALIDADOR 2: Correção de Marcas (Regra de Negócio) ---
    @field_validator('fabricante')
    def corrigir_marcas(cls, v):
        if v == "VW":
            return "VOLKSWAGEN"
        elif v == "GM":
            return "CHEVROLET"
        return v

    # --- VALIDADOR 3: Preços Seguros ---
    # Garante que o programa não quebre se tiver texto na coluna de preço
    @field_validator('preco_olx', 'preco_ml', mode='before')
    def tratar_precos(cls, v):
        if v == "" or v is None:
            return 0.0
        try:
            return float(v)
        except ValueError:
            return 0.0

    # --- CAMPO CALCULADO: Nome da Pasta ---
    # Isso substitui a função 'formatar_nome_pasta' do seu antigo helpers.py
    @computed_field
    def nome_pasta_formatado(self) -> str:
        # Junta fabricante e modelo
        raw_name = f"{self.fabricante}_{self.modelo}"

        # Lógica de limpeza: só deixa letras, números e underline
        # (Copiado da lógica do seu legacy/utils/helpers.py)
        nome_limpo = ''.join(c for c in raw_name if c.isalnum() or c in (' ', '_')).strip()

        return nome_limpo.replace(' ', '_')

# -------------------------------------------------------------------------
# MODELOS ESPECÍFICOS
# -------------------------------------------------------------------------

class Calota(ProdutoBase):
    diametro: str = Field(..., alias="DIÂMETRO")

class Roda(ProdutoBase):
    aro: str = Field(..., alias="ARO")
    tala: str = Field(..., alias="TALA")

class RodaLiga(Roda):
    # Futuramente você pode adicionar campos específicos aqui (offset, furação)
    pass