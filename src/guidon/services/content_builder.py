import re
from pathlib import Path
from typing import Any, Dict

from src.guidon.core.constants import FURACOES_CONHECIDAS
from src.guidon.core.models import Calota, ProdutoBase, Roda


class ContentBuilder:
    """
    Handles the generation of content (descriptions and group texts) for products based on templates.
    """
    def __init__(self, templates_dir: Path = None):
        if templates_dir:
            self.templates_dir = templates_dir
        else:
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent.parent
            self.templates_dir = project_root / "templates"

        if not self.templates_dir.exists():
            print(f"⚠️  ALERTA: Pasta de templates não encontrada em: {self.templates_dir}")

    def _load_template(self, filename: str) -> str:
        path = self.templates_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Template não encontrado: {filename}")
        return path.read_text(encoding="utf-8")

    def _format_money(self, value: float) -> str:
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _extract_measures(self, texto: str) -> Dict[str, str]:
        extra = {"aro": "?", "tala": "?", "furacao": "?"}
        if not texto:
            return extra

        # 1. Regex Furação (ex: 5X100, 4X108, 5X114,3, 5x114.3)
        match_furacao = re.search(r"(\d)\s*[xX]\s*(\d{2,3}(?:[.,]\d)?)", texto)
        if match_furacao:
            qtd_furos = match_furacao.group(1)
            distancia = match_furacao.group(2).replace(",", ".")
            extra["furacao"] = f"{qtd_furos}x{distancia}"
        else:
            texto_upper = texto.upper()
            for furacao in FURACOES_CONHECIDAS:
                if furacao.upper() in texto_upper:
                    extra["furacao"] = furacao.replace(",", ".")
                    break

        # 2. Regex Aro e Tala (ex: 16X6,5)
        match_medidas = re.search(r"(\d{2})\s*[xX]\s*(\d+(?:[.,]\d)?)", texto)
        if match_medidas:
            extra["aro"] = match_medidas.group(1)
            extra["tala"] = match_medidas.group(2).replace(".", ",")

        return extra

    def _prepare_context(self, product: ProdutoBase) -> Dict[str, Any]:
        ctx = product.model_dump(exclude_none=True)

        ctx["preco_avista"] = self._format_money(product.preco_avista)
        ctx["preco_ml"] = self._format_money(product.preco_ml)

        if isinstance(product, Roda):
            # Lê do bruto_modelo para recuperar furação e medidas limpas pelo Pydantic
            texto_completo = getattr(product, "bruto_modelo", product.modelo)
            medidas = self._extract_measures(texto_completo)

            ctx["aro"] = product.aro if (product.aro and product.aro != "?") else medidas["aro"]
            ctx["tala"] = product.tala if (product.tala and product.tala != "?") else medidas["tala"]
            ctx["furacao"] = medidas["furacao"]
            ctx["et"] = product.offset if product.offset else "?"

        ctx["cor"] = ctx.get("acabamento", "")
        ctx["numero_peça"] = ctx.get("sku", "")
        ctx["Modelo"] = product.modelo
        ctx["Material"] = product.material
        if "diametro" in ctx:
            ctx["Diametro"] = ctx["diametro"]

        return {k: str(v) for k, v in ctx.items()}

    def create_content(self, product: ProdutoBase, product_folder: Path):
        if isinstance(product, Calota):
            templates = ("descricao_calota.txt", "descricao_grupo_calotas.txt")
        elif isinstance(product, Roda):
            templates = ("descricao_roda_ferro.txt", "descricao_grupo_rodas.txt")
        else:
            return

        tpl_desc_name, tpl_grupo_name = templates

        try:
            context = self._prepare_context(product)

            # Gera Descrição
            raw_desc = self._load_template(tpl_desc_name)
            final_desc = raw_desc.format(**context)
            (product_folder / "descricao.txt").write_text(final_desc, encoding="utf-8")

            # Gera Grupo
            try:
                raw_grupo = self._load_template(tpl_grupo_name)
                final_grupo = raw_grupo.format(**context)
                (product_folder / "grupo.txt").write_text(final_grupo, encoding="utf-8")
            except FileNotFoundError:
                pass

            print(f"   [📝] Textos gerados em: {product_folder.name}")

        except KeyError as e:
            chaves_disponiveis = ", ".join(sorted(context.keys()))
            print(
                f"   [X] Erro de Template: O arquivo pede {{{e}}} mas temos apenas: [{chaves_disponiveis}]"
            )
        except Exception as e:
            print(f"   [X] Erro ao gerar texto: {e}")