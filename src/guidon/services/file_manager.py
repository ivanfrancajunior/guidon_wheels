from pathlib import Path
from typing import List, Tuple
from src.guidon.core.models import ProdutoBase

class FileManager:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        if not self.output_dir.exists():
            try:
                self.output_dir.mkdir(parents=True, exist_ok=True)
                print(f"📁 Pasta raiz criada: {self.output_dir}")
            except Exception as e:
                raise PermissionError(f"Não foi possível criar a pasta raiz {self.output_dir}: {e}")

    def create_folders(self, products: List[ProdutoBase]) -> Tuple[int, int]:
        created_count = 0
        skipped_count = 0

        print(f"\n📂 Iniciando criação de estruturas em: {self.output_dir.name}")

        # ALTERAÇÃO AQUI: Adicionamos o index (começando de 1)
        for index, product in enumerate(products, start=1):
            try:
                # Monta o nome: "1_VOLKSWAGEN_FUSCA..."
                folder_name = f"{index}_{product.format_dirname}"

                target_path = self.output_dir / folder_name

                if not target_path.exists():
                    target_path.mkdir()
                    print(f"   [+] Pasta Criada: {folder_name}")
                    created_count += 1
                else:
                    skipped_count += 1

            except Exception as e:
                print(f"   [X] Erro crítico ao criar pasta para {product.sku}: {e}")

        print(f"📊 Resumo: {created_count} novas pastas criadas | {skipped_count} já existiam.")
        return created_count, skipped_count