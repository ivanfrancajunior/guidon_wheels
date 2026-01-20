import re
from pydantic import BaseModel, Field, computed_field, field_validator


class ProdutoBase(BaseModel):
    """
    Base model for all product types, defining common fields and validators.
    """
    data: str = Field(default="", alias="data")
    fabricante: str = Field(..., alias="fabricante")
    modelo: str = Field(..., alias="modelo")

    sku: str = Field(..., alias="número de peça / sku")

    qtd: int = Field(default=0, alias="qtd")
    acabamento: str = Field(default="", alias="acabamento")
    material: str = Field(default="", alias="material")

    preco_avista: float = Field(default=0.0, alias="olx | face")
    preco_ml: float = Field(default=0.0, alias="ml")
    concorrencia: str = Field(default="", alias="concorrência")

    @field_validator("fabricante", "modelo", "acabamento", "material", mode="before")
    def validate_columns_names(cls, value):
        """Standardizes string fields to Title Case."""
        if isinstance(value, str):
            return value.strip().title()
        return value

    @field_validator("fabricante")
    def convert_lablel_names(cls, value):
        """Normalizes manufacturer names (e.g., VW -> Volkswagen)."""
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
        """Converts price strings to floats, handling currency symbols and formatting."""
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
        """Generates a clean directory name from manufacturer and model."""
        raw_name = f"{self.fabricante}_{self.modelo}"
        nome_limpo = "".join(
            c for c in raw_name if c.isalnum() or c in (" ", "_")
        ).strip()
        return nome_limpo.replace(" ", "_")


class Roda(ProdutoBase):
    """
    Product model specific for Wheels (Roda), treating measures as strings.
    """
    offset: str = Field(default="", alias="et")
    aro: str = Field(default="", alias="aro")
    tala: str = Field(default="", alias="tala")

    @field_validator("offset", "aro", "tala", mode="before")
    def parse_roda_fields(cls, v):
        """Ensures wheel measures are strings, converting numbers if necessary."""
        if v is None:
            return ""
        return str(v).strip()

    @field_validator("modelo", mode="before")
    def extract_model_name(cls, v):
        """Extracts clean model name from pattern 'Roda Guidon [Model] ...'."""
        if not isinstance(v, str):
            return v

        match = re.search(r"Roda\s+Guidon\s+(.+?)\s+(?=\d{2}[xX])", v, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return v

class Calota(ProdutoBase):
    """
    Product model specific for Hubcaps (Calota).
    """
    diametro: str = Field(default="", alias="diâmetro")

    @field_validator("diametro", mode="before")
    def handle_size(cls, v):
        """Standardizes diameter representation."""
        return str(v).strip().upper() if v else ""


class Calotao(ProdutoBase):
    """
    Product model specific for Large Hubcaps (Calotao).
    """
    diametro: str = Field(default="", alias="diâmetro")

    @field_validator("diametro", mode="before")
    def handle_size(cls, value):
        """Standardizes diameter representation, defaulting to 'X' if empty."""
        if value == "" or value is None:
            return "X"
        return str(value).strip().upper()
