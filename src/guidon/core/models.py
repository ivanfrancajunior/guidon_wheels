from pydantic import BaseModel, Field, computed_field, field_validator


class ProdutoBase(BaseModel):
    # --- MUDANÇA: Todos os aliases agora estão em minúsculo para bater com o loader ---
    data: str = Field(default="", alias="data")
    fabricante: str = Field(..., alias="fabricante")
    modelo: str = Field(..., alias="modelo")

    # Atenção aqui: o loader vai transformar "NÚMERO..." em "número..."
    sku: str = Field(..., alias="número de peça / sku")

    qtd: int = Field(default=0, alias="qtd")
    acabamento: str = Field(default="", alias="acabamento")
    material: str = Field(default="", alias="material")

    # Se no Excel estiver "OLX | FACE", o loader entrega "olx | face"
    preco_avista: float = Field(default=0.0, alias="olx | face")
    preco_ml: float = Field(default=0.0, alias="ml")
    concorrencia: str = Field(default="", alias="concorrência")

    # --- VALIDADORES (Lógica Mantida) ---
    @field_validator("fabricante", "modelo", "acabamento", "material", mode="before")
    def validate_columns_names(cls, value):
        if isinstance(value, str):
            return value.strip().upper()
        return value

    @field_validator("fabricante")
    def convert_lablel_names(cls, value):
        # Ajustei para verificar maiúsculo, já que o validator de cima (validate_columns_names) roda antes
        if value == "VW" or value == "VOLKS":
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
        texto = (
            str(value)
            .replace("R$", "")
            .replace(" ", "")
            .replace(".", "")
            .replace(",", ".")
        )
        try:
            return float(texto)
        except ValueError:
            return 0.0

    @computed_field
    def format_dirname(self) -> str:
        raw_name = f"{self.fabricante}_{self.modelo}"
        nome_limpo = "".join(
            c for c in raw_name if c.isalnum() or c in (" ", "_")
        ).strip()
        return nome_limpo.replace(" ", "_")


class Roda(ProdutoBase):
    offset: int = Field(default=0, alias="et")  # "ET" vira "et"
    aro: int = Field(default=0, alias="aro")
    tala: float = Field(default=0, alias="tala")


class Calota(ProdutoBase):
    diametro: str = Field(default="", alias="diâmetro")

    @field_validator("diametro", mode="before")
    def handle_size(cls, v):
        return str(v).strip().upper() if v else ""


class Calotao(ProdutoBase):
    diametro: str = Field(default="", alias="diâmetro")

    @field_validator("diametro", mode="before")
    def handle_size(cls, value):
        if value == "" or value is None:
            return "X"
        return str(value).strip().upper()
