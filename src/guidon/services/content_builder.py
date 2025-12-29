import re
from pathlib import Path
from typing import Any, Dict

from src.guidon.core.constants import FURACOES_CONHECIDAS  # <--- Import novo
from src.guidon.core.models import Calota, ProdutoBase, Roda


class ContentBuilder:
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        if not self.templates_dir.exists():
            print(
                f"⚠️  ALERTA: Pasta de templates não encontrada em: {self.templates_dir}"
            )

    def _load_template(self, filename: str) -> str:
        path = self.templates_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Template não encontrado: {filename}")
        return path.read_text(encoding="utf-8")

    def _format_money(self, value: float) -> str:
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _extract_measures_from_name(self, texto: str) -> Dict[str, str]:
        extra = {"aro": "?", "tala": "?", "furacao": "?"}

        texto_upper = texto.upper()

        for furacao in FURACOES_CONHECIDAS:
            # Se a furação da lista estiver dentro do nome do produto
            if furacao.upper() in texto_upper:
                extra["furacao"] = furacao.replace(",", ".")
                break

        match_triplo = re.search(r"(\d{2})[xX](\d+[.,]?\d?)[xX](\d+[.,]?\d?)", texto)

        if match_triplo:
            extra["aro"] = match_triplo.group(1)
            t1 = match_triplo.group(2).replace(".", ",")
            t2 = match_triplo.group(3).replace(".", ",")
            extra["tala"] = f"{t1} e {t2}"
        else:
            # Caso 2: Pares Simples ou Mistos (15x6 ...)
            matches = re.findall(r"(\d{2})[xX](\d{1,2}(?:[.,]\d)?)", texto)
            if matches:
                aros = sorted(list(set(m[0] for m in matches)))
                talas = [m[1].replace(".", ",") for m in matches]
                extra["aro"] = " e ".join(aros)
                extra["tala"] = " e ".join(talas)

        return extra

    def _prepare_context(self, product: ProdutoBase) -> Dict[str, Any]:
        ctx = product.model_dump(exclude_none=True)
        ctx["preco_avista"] = self._format_money(product.preco_avista)
        ctx["preco_ml"] = self._format_money(product.preco_ml)

        if isinstance(product, Roda):
            medidas = self._extract_measures_from_name(product.modelo)

            if (
                product.aro == 0
                or " e " in medidas["aro"]
                or " e " in medidas["tala"]
                or medidas["furacao"] != "?"
            ):
                ctx.update(medidas)
            else:
                # Garante chaves
                if "aro" not in ctx:
                    ctx["aro"] = medidas["aro"]
                if "tala" not in ctx:
                    ctx["tala"] = medidas["tala"]
                if "furacao" not in ctx:
                    ctx["furacao"] = medidas["furacao"]

        ctx["cor"] = ctx.get("acabamento", "")
        return {k: str(v) for k, v in ctx.items()}

    def create_content(self, product: ProdutoBase, product_folder: Path):

        if isinstance(product, Calota):
            templates = ("descricao_calota.txt", "descricao_grupo_calotas.txt")
        elif (
            isinstance(product, Roda)
            and "FERRO" in getattr(product, "material", "").upper()
        ):
            templates = ("descricao_roda_ferro.txt", "descricao_grupo_rodas.txt")
        else:
            return

        tpl_desc_name, tpl_grupo_name = templates

        try:
            context = self._prepare_context(product)

            raw_desc = self._load_template(tpl_desc_name)
            final_desc = raw_desc.format(**context)
            (product_folder / "descricao.txt").write_text(final_desc, encoding="utf-8")

            try:
                raw_grupo = self._load_template(tpl_grupo_name)
                final_grupo = raw_grupo.format(**context)
                (product_folder / "grupo.txt").write_text(final_grupo, encoding="utf-8")
            except FileNotFoundError:
                pass

            print(f"   [📝] Textos gerados em: {product_folder.name}")

        except KeyError as e:
            print(
                f"   [X] Erro de Template: O arquivo .txt pede {{{e}}} mas o código gerou apenas: {list(context.keys())}"
            )
        except Exception as e:
            print(f"   [X] Erro ao gerar texto: {e}")
