import shutil
from pathlib import Path

from src.guidon.core.models import Calota, ProdutoBase, Roda


class ImageManager:
    def __init__(self, assets_dir: Path = None):
        """
        :param assets_dir: Caminho completo para a imagem 'valor_ref_und.jpg'
        """
        if assets_dir is None:
            self.default_image = Path(
                r"C:\Users\Junior\Desktop\guidon_wheels\assets\valor_ref_und.jpg"
            )
        else:
            self.default_image = Path(assets_dir)

        # Verifica se o arquivo existe
        if not self.default_image.exists():
            print(f"⚠️  ALERTA: Imagem padrão não encontrada em: {self.default_image}")

    def process_images(self, product: ProdutoBase, product_folder: Path):
        """
        Se for Calota ou Roda de Ferro, copia a imagem de aviso para a pasta.
        """
        should_copy = False

        # Regra Simplificada:
        # 1. É Calota? SIM.
        # 2. É Roda e o material é Ferro? SIM.
        if isinstance(product, Calota):
            should_copy = True
        elif (
            isinstance(product, Roda)
            and "FERRO" in getattr(product, "material", "").upper()
        ):
            should_copy = True

        # Executa a cópia se necessário
        if should_copy:
            if self.default_image.exists():
                try:
                    # Copia o arquivo para dentro da pasta do produto mantendo o nome
                    dest_file = product_folder / self.default_image.name
                    shutil.copy2(self.default_image, dest_file)
                    print(f"   [🖼️] Imagem copiada: {self.default_image.name}")
                except Exception as e:
                    print(f"   [X] Erro ao copiar imagem: {e}")
            else:
                print(
                    f"   [!] ALERTA: Imagem '{self.default_image.name}' não encontrada na pasta assets."
                )
