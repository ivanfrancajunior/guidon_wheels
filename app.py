import shutil
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

# Importa o loader atualizado e o gerador de conteúdo
from src.guidon.services.loader import load_products
from src.guidon.services.content_builder import ContentBuilder


def formatar_nome_pasta(index: int, produto) -> str:
    """Gera o nome da pasta numerado sequencialmente."""
    base_nome = getattr(produto, "format_dirname", f"{produto.fabricante}_{produto.modelo}")

    furacao = getattr(produto, "furacao", "")
    aro = getattr(produto, "aro", "")

    detalhes = []
    if aro:
        detalhes.append(f"Aro_{aro}")
    if furacao:
        detalhes.append(str(furacao))

    sufixo = f"_{'_'.join(detalhes)}" if detalhes else ""
    nome_cru = f"{index}_{base_nome}{sufixo}"

    return "".join(c for c in nome_cru if c.isalnum() or c in ("_", "-")).strip("_")


def criar_pastas_e_arquivos(produtos, pasta_destino: Path):
    """
    Cria a estrutura de pastas e aciona o ContentBuilder para gerar descricao.txt e grupo.txt
    """
    # Inicializa o ContentBuilder
    builder = ContentBuilder()

    for index, p in enumerate(produtos, start=1):
        nome_pasta = formatar_nome_pasta(index, p)
        dir_produto = pasta_destino / nome_pasta
        dir_produto.mkdir(parents=True, exist_ok=True)

        # 1. Gera descricao.txt e grupo.txt usando os templates físicos (.txt)
        builder.create_content(p, dir_produto)

        # 2. Gera um resumo padrão em dados.txt (fallback para dados numéricos brutos)
        arquivo_resumo = dir_produto / "dados.txt"
        with open(arquivo_resumo, "w", encoding="utf-8") as f:
            f.write(f"Item: #{index}\n")
            f.write(f"Fabricante: {p.fabricante}\n")
            f.write(f"Modelo: {p.modelo}\n")
            f.write(f"SKU: {p.sku}\n")
            f.write(f"Quantidade: {p.qtd}\n")
            f.write(f"Preço ML: R$ {p.preco_ml:.2f}\n")
            f.write(f"Preço À Vista: R$ {p.preco_avista:.2f}\n")


st.set_page_config(page_title="Gerador Guidon", page_icon="📦", layout="wide")

st.title("📦 Gerador de Arquivos - Guidon Rodas")
st.markdown("Faça o upload da planilha para validar os dados e baixar as pastas geradas em formato ZIP.")
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Configurações")
    tipo_produto = st.selectbox("Tipo de Produto:", ["Roda", "Calota", "Calotao"])
    arquivo_upload = st.file_uploader("Selecione a planilha (.xlsx)", type=["xlsx", "xls", "csv"])

with col2:
    st.subheader("Painel de Execução")

    if arquivo_upload:
        if st.button("Processar e Gerar Arquivos", type="primary", use_container_width=True):

            with tempfile.TemporaryDirectory() as temp_dir_str:
                temp_dir = Path(temp_dir_str)

                # Salva a planilha temporariamente
                extensao = f".{arquivo_upload.name.split('.')[-1]}"
                tmp_excel_path = temp_dir / f"upload{extensao}"
                with open(tmp_excel_path, "wb") as f:
                    f.write(arquivo_upload.getvalue())

                with st.spinner("Lendo, validando dados e criando descrições..."):
                    try:
                        produtos_validados = load_products(tmp_excel_path, tipo_produto)

                        if not produtos_validados:
                            st.warning("Nenhum produto foi validado.")
                        else:
                            st.success(f"✅ {len(produtos_validados)} produtos validados!")

                            pasta_saida = temp_dir / "arquivos_saida"
                            pasta_saida.mkdir(exist_ok=True)

                            # Cria pastas + executa ContentBuilder
                            criar_pastas_e_arquivos(produtos_validados, pasta_saida)

                            st.info("📦 Compactando pastas com descrições...")

                            caminho_zip = temp_dir / "arquivos_guidon"
                            shutil.make_archive(
                                base_name=str(caminho_zip),
                                format="zip",
                                root_dir=str(pasta_saida)
                            )

                            df_resultado = pd.DataFrame([p.model_dump() for p in produtos_validados])

                            st.markdown("### Pré-visualização dos Dados")
                            st.dataframe(
                                df_resultado,
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "preco_ml": st.column_config.NumberColumn("Preço ML", format="R$ %.2f"),
                                    "preco_avista": st.column_config.NumberColumn("Preço À Vista", format="R$ %.2f")
                                }
                            )

                            with open(f"{caminho_zip}.zip", "rb") as zip_file:
                                st.download_button(
                                    label="📥 Baixar Pastas com Descrições (.ZIP)",
                                    data=zip_file,
                                    file_name="Arquivos_Guidon_Rodas.zip",
                                    mime="application/zip",
                                    type="primary"
                                )

                    except Exception as e:
                        st.error(f"Erro ao processar: {e}")