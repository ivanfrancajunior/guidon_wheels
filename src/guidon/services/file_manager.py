from pathlib import Path
from typing import List, Tuple
from src.guidon.core.models import ProdutoBase

class FileManager:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """Garante que a pasta raiz de saída existe."""
        if not self.output_dir.exists():
            try:
                self.output_dir.mkdir(parents=True, exist_ok=True)
                print(f"📁 Pasta raiz criada: {self.output_dir}")
            except Exception as e:
                raise PermissionError(f"Não foi possível criar a pasta raiz {self.output_dir}: {e}")

    def create_folders(self, products: List[ProdutoBase]) -> Tuple[int, int]:
        """
        Recebe a lista de produtos processados e cria as pastas físicas.

        Retorna uma tupla: (qtd_criada, qtd_existente)
        """
        created_count = 0
        skipped_count = 0

        print(f"\n📂 Iniciando criação de estruturas em: {self.output_dir.name}")

        for product in products:
            try:
                folder_name = product.format_dirname

                target_path = self.output_dir / folder_name

                if not target_path.exists():
                    target_path.mkdir()
                    print(f"   [+] Pasta Criada: {folder_name}")
                    created_count += 1
                else:
                    # Se já existe, não faz nada (evita sobrescrever dados antigos)
                    # print(f"   [!] Já existe: {folder_name}") # Descomente se quiser ver os logs de pulados
                    skipped_count += 1

            except Exception as e:
                print(f"   [X] Erro crítico ao criar pasta para {product.sku}: {e}")

        print(f"📊 Resumo: {created_count} novas pastas criadas | {skipped_count} já existiam.")
        return created_count, skipped_count