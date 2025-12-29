from pydantic import BaseModel, Field, computed_field, field_validator

class ProdutoBase(BaseModel):
    # Nomes padronizados (snake_case) para uso interno no Python
    data: str = Field(default="", alias="DATA")
    fabricante: str = Field(..., alias="FABRICANTE")
    modelo: str = Field(..., alias="MODELO")
    sku: str = Field(..., alias="NÚMERO DE PEÇA / SKU") # Mudamos de numero_peça para sku
    qtd: int = Field(default=0, alias="QTD")
    acabamento: str = Field(default="", alias="ACABAMENTO")
    material: str = Field(default="", alias="MATERIAL")
    preco_avista: float = Field(default=0.0, alias="OLX | FACE")
    preco_ml: float = Field(default=0.0, alias="ML")
    concorrencia: str = Field(default="", alias="CONCORRÊNCIA")

    # --- VALIDADORES (Mantive os seus, apenas ocultando para economizar espaço) ---
    @field_validator("fabricante", "modelo", "acabamento", "material", mode="before")
    def validate_columns_names(cls, value):
        if isinstance(value, str):
            return value.strip().upper()
        return value

    @field_validator("fabricante")
    def convert_lablel_names(cls, value):
        if value == "VW" or value == "Volks":
            return "Volkswagen"
        elif value == "GM":
            return "Chevrolet"
        return value

    @field_validator("preco_avista", "preco_ml", mode="before")
    def price_handler(cls, value):
        if value is None or str(value).strip() == "":
            return 0.0
        if isinstance(value, (float, int)):
            return float(value)
        texto = str(value).replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            return 0.0

    @computed_field
    def format_dirname(self) -> str:
        raw_name = f"{self.fabricante}_{self.modelo}"
        nome_limpo = "".join(c for c in raw_name if c.isalnum() or c in (" ", "_")).strip()
        return nome_limpo.replace(" ", "_")

class Roda(ProdutoBase):
    offset: int = Field(default=0, alias="ET") # Variável interna é 'offset'
    aro: int = Field(default=0, alias="ARO")
    tala: float = Field(default=0, alias="TALA")

class Calota(ProdutoBase):
    diametro: str = Field(default="", alias="DIÂMETRO")

    @field_validator("diametro", mode="before")
    def handle_size(cls, v):
        return str(v).strip().upper() if v else ""


class Calotao(ProdutoBase):
    diametro: str = Field(default="", alias="DIÂMETRO")

    @field_validator("diametro", mode="before")
    def handle_size(cls, value):
        if value == "" or value is None:
            return "X"
