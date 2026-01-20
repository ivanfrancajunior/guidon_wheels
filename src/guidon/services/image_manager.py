import shutil
from pathlib import Path

from src.guidon.core.models import Calota, ProdutoBase, Roda


class ImageManager:
    def __init__(self, assets_dir: Path = None):
        """
        :param assets_dir: Caminho completo para a pasta de assets.
                           Se não fornecido, tenta resolver dinamicamente.
        """
        if assets_dir:
            self.assets_dir = assets_dir
        else:
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent.parent
            self.assets_dir = project_root / "assets"

        self.default_image = self.assets_dir / "valor_ref_und.jpg"

        if not self.default_image.exists():
            print(f"⚠️  ALERTA: Imagem padrão não encontrada em: {self.default_image}")

    def process_images(self, product: ProdutoBase, product_folder: Path):
        """
        Se for Calota ou Roda de Ferro, copia a imagem de aviso para a pasta.
        """
        should_copy = False

        if isinstance(product, Calota):
            should_copy = True
        elif (
            isinstance(product, Roda)
            and "FERRO" in getattr(product, "material", "").upper()
        ):
            should_copy = True

        if should_copy:
            if self.default_image.exists():
                try:
                    dest_file = product_folder / self.default_image.name
                    shutil.copy2(self.default_image, dest_file)
                    print(f"   [🖼️] Imagem copiada: {self.default_image.name}")
                except Exception as e:
                    print(f"   [X] Erro ao copiar imagem: {e}")
            else:
                print(
                    f"   [!] ALERTA: Imagem '{self.default_image.name}' não encontrada na pasta assets."
                )
