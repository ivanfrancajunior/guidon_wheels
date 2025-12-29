import shutil
from pathlib import Path

from src.guidon.core.models import Calota, ProdutoBase, Roda


class ImageManager:
    def __init__(self, assets_dir: Path):
        """
        :param assets_dir: Pasta onde fica a imagem 'valor_ref_und.jpg'
        """
        self.assets_dir = assets_dir
        # O arquivo único que será usado
        self.default_image = self.assets_dir / "valor_ref_und.jpg"

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
