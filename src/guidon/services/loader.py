from pathlib import Path
from typing import List
import pandas as pd

# Certifique-se de que o caminho dos imports está correto no seu projeto
from src.guidon.core.models import Calota, Calotao, ProdutoBase, Roda

def get_file_ext_helper(file_path: Path) -> pd.DataFrame:
    file_ext = file_path.suffix.lower()

    if file_ext == ".csv":
        try:
            return pd.read_csv(file_path, sep=None, engine="python", dtype=str)
        except Exception:
            try:
                return pd.read_csv(file_path, sep=";", dtype=str)
            except Exception:
                return pd.read_csv(file_path, sep=",", dtype=str, on_bad_lines="skip")
    elif file_ext in [".xlsx", ".xls"]:
        return pd.read_excel(file_path, dtype=str)
    else:
        raise ValueError(f"Formato '{file_ext}' não suportado. Use .csv ou .xlsx")

def load_products(file_path: Path, type_product: str) -> List[ProdutoBase]:
    # Ajuste esse offset conforme seu Excel real (se tem linhas em branco antes do cabeçalho)
    OFFSET_CABECALHO_EXCEL = 2

    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    class_map = {
        "roda": Roda,
        "calota": Calota,
        "calotao": Calotao,
    }

    product_inputed = type_product.lower().strip()
    class_model = class_map.get(product_inputed)

    if not class_model:
        raise ValueError(f"Tipo '{type_product}' inválido. Opções: {list(class_map.keys())}")

    print(f"📂 Lendo arquivo ({product_inputed}): {file_path}...")

    try:
        df = get_file_ext_helper(file_path)

        # --- AQUI ESTÁ A MUDANÇA ---
        # Padronizamos para minúsculo (.lower) para facilitar o match com os Models
        df.columns = df.columns.str.strip().str.lower()

        df = df.fillna("")
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo: {e}")

    products_list = []

    for line_number, (_, row) in enumerate(df.iterrows(), start=OFFSET_CABECALHO_EXCEL):
        try:
            # O **row.to_dict() pega as colunas (ex: "diametro", "modelo")
            # e tenta encaixar na classe Roda(diametro=..., modelo=...)
            product = class_model(**row.to_dict())
            products_list.append(product)
        except Exception as e:
            # Mostra qual campo deu erro (ex: validação do Pydantic falhou)
            print(f"⚠️  Linha {line_number} ignorada: {e}")
            continue

    print(f"✅ Sucesso! {len(products_list)} itens carregados.")
    return products_list