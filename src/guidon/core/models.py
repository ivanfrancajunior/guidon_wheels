import re
from typing import Union
import pandas as pd
from pydantic import BaseModel, Field, computed_field, field_validator


class ProdutoBase(BaseModel):
    data: str = Field(default="", alias="dt")
    fabricante: str = Field(..., alias="fabricante")
    modelo: str = Field(..., alias="modelo")
    bruto_modelo: str = Field(default="")

    sku: str = Field(default="-", alias="sku")

    qtd: Union[int, str] = Field(default=0, alias="qtd")
    acabamento: str = Field(default="", alias="acabamento")
    material: str = Field(default="", alias="material")

    preco_avista: float = Field(default=0.0, alias="olx | face")
    preco_ml: float = Field(default=0.0, alias="ml")
    concorrencia: str = Field(default="", alias="concorrência")

    @field_validator("sku", "data", mode="before")
    def parse_string_fields(cls, value):
        if value is None or pd.isna(value):
            return "-"
        if isinstance(value, float):
            return str(int(value)) if value.is_integer() else str(value)
        return str(value).strip()

    @field_validator("concorrencia", "acabamento", "material", mode="before")
    def handle_nan_strings(cls, value):
        if value is None or pd.isna(value):
            return ""
        return str(value).strip().title() if isinstance(value, str) else str(value)

    @field_validator("qtd", mode="before")
    def parse_qtd(cls, v):
        if v is None or pd.isna(v) or str(v).strip() == "":
            return 0
        try:
            return int(float(v))
        except ValueError:
            return 0

    @field_validator("fabricante")
    def convert_lablel_names(cls, value):
        if not isinstance(value, str):
            return value

        val_upper = value.upper().strip()
        if val_upper in ("VW", "VOLKS"):
            return "Volkswagen"
        elif val_upper == "GM":
            return "Chevrolet"
        return value

    @field_validator("preco_avista", "preco_ml", mode="before")
    def price_handler(cls, value):
        if value is None or pd.isna(value) or str(value).strip() == "":
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
    offset: str = Field(default="", alias="et")
    aro: str = Field(default="", alias="aro")
    tala: str = Field(default="", alias="tala")

    @field_validator("offset", "aro", "tala", mode="before")
    def parse_roda_fields(cls, v):
        if v is None or pd.isna(v):
            return ""
        if isinstance(v, float):
            return str(int(v)) if v.is_integer() else str(v)
        return str(v).strip()

    @field_validator("modelo", mode="before")
    def extract_model_name(cls, v):
        if not isinstance(v, str):
            return str(v) if v is not None else ""

        match = re.search(r"Roda\s+Guidon\s+(.+?)\s+(?=\d{2}[xX])", v, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return v

    def __init__(self, **data):
        if "bruto_modelo" not in data and "modelo" in data:
            data["bruto_modelo"] = str(data["modelo"])
        super().__init__(**data)


class Calota(ProdutoBase):
    diametro: str = Field(default="", alias="diâmetro")

    @field_validator("diametro", mode="before")
    def handle_size(cls, v):
        if v is None or pd.isna(v):
            return ""
        if isinstance(v, float):
            return str(int(v)) if v.is_integer() else str(v)
        return str(v).strip().upper()


class Calotao(ProdutoBase):
    diametro: str = Field(default="", alias="diâmetro")

    @field_validator("diametro", mode="before")
    def handle_size(cls, value):
        if value == "" or value is None or pd.isna(value):
            return "X"
        if isinstance(value, float):
            return str(int(value)) if value.is_integer() else str(value)
        return str(value).strip().upper()