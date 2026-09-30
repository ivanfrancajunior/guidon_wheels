import shutil
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from src.guidon.services.content_builder import ContentBuilder

# PIL apenas para visualização das miniaturas
# Importa o loader atualizado e o gerador de conteúdo
from src.guidon.services.loader import load_products

# Importa o gerador de montagem
from utils.image_gen import criar_montagem

# ============================================================
# FUNÇÕES DO GERADOR DE ARQUIVOS
# ============================================================


def formatar_nome_pasta(index: int, produto) -> str:
    """Gera o nome da pasta numerado sequencialmente."""

    base_nome = getattr(
        produto, "format_dirname", f"{produto.fabricante}_{produto.modelo}"
    )

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
    Cria a estrutura de pastas e aciona o ContentBuilder
    para gerar descricao.txt e grupo.txt.
    """

    builder = ContentBuilder()

    for index, p in enumerate(produtos, start=1):
        nome_pasta = formatar_nome_pasta(index, p)

        dir_produto = pasta_destino / nome_pasta

        dir_produto.mkdir(parents=True, exist_ok=True)

        # 1. Gera descricao.txt e grupo.txt
        builder.create_content(p, dir_produto)

        # 2. Gera dados.txt
        arquivo_resumo = dir_produto / "dados.txt"

        with open(arquivo_resumo, "w", encoding="utf-8") as f:
            f.write(f"Item: #{index}\n")
            f.write(f"Fabricante: {p.fabricante}\n")
            f.write(f"Modelo: {p.modelo}\n")
            f.write(f"SKU: {p.sku}\n")
            f.write(f"Quantidade: {p.qtd}\n")
            f.write(f"Preço ML: R$ {p.preco_ml:.2f}\n")
            f.write(f"Preço À Vista: R$ {p.preco_avista:.2f}\n")


# ============================================================
# CONFIGURAÇÃO DO STREAMLIT
# ============================================================

st.set_page_config(page_title="Gerador Guidon", page_icon="📦", layout="wide")

st.title("📦 Gerador Guidon Rodas")

st.markdown("Ferramentas para geração de arquivos e montagem de imagens.")

st.divider()


# ============================================================
# ABAS
# ============================================================

aba_arquivos, aba_imagens = st.tabs(["📦 Gerador de Arquivos", "🖼️ Montagem de Imagens"])


# ============================================================
# ABA 1 — GERADOR DE ARQUIVOS
# ============================================================

with aba_arquivos:
    st.subheader("Gerador de Arquivos")

    st.markdown(
        "Faça o upload da planilha para validar os dados "
        "e baixar as pastas geradas em formato ZIP."
    )

    st.divider()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Configurações")

        tipo_produto = st.selectbox("Tipo de Produto:", ["Roda", "Calota", "Calotao"])

        arquivo_upload = st.file_uploader(
            "Selecione a planilha (.xlsx)",
            type=["xlsx", "xls", "csv"],
            key="planilha_upload",
        )

    with col2:
        st.subheader("Painel de Execução")

        if arquivo_upload:
            if st.button(
                "Processar e Gerar Arquivos", type="primary", use_container_width=True
            ):
                with tempfile.TemporaryDirectory() as temp_dir_str:
                    temp_dir = Path(temp_dir_str)

                    # ------------------------------------------------
                    # Salva a planilha temporariamente
                    # ------------------------------------------------

                    extensao = f".{arquivo_upload.name.split('.')[-1]}"

                    tmp_excel_path = temp_dir / f"upload{extensao}"

                    with open(tmp_excel_path, "wb") as f:
                        f.write(arquivo_upload.getvalue())

                    # ------------------------------------------------
                    # Processamento
                    # ------------------------------------------------

                    with st.spinner("Lendo, validando dados e criando descrições..."):
                        try:
                            produtos_validados = load_products(
                                tmp_excel_path, tipo_produto
                            )

                            if not produtos_validados:
                                st.warning("Nenhum produto foi validado.")

                            else:
                                st.success(
                                    f"✅ {len(produtos_validados)} produtos validados!"
                                )

                                # ------------------------------------------------
                                # Cria estrutura de saída
                                # ------------------------------------------------

                                pasta_saida = temp_dir / "arquivos_saida"

                                pasta_saida.mkdir(exist_ok=True)

                                criar_pastas_e_arquivos(produtos_validados, pasta_saida)

                                # ------------------------------------------------
                                # Compactação
                                # ------------------------------------------------

                                st.info("📦 Compactando pastas com descrições...")

                                caminho_zip = temp_dir / "arquivos_guidon"

                                shutil.make_archive(
                                    base_name=str(caminho_zip),
                                    format="zip",
                                    root_dir=str(pasta_saida),
                                )

                                # ------------------------------------------------
                                # DataFrame
                                # ------------------------------------------------

                                df_resultado = pd.DataFrame(
                                    [p.model_dump() for p in produtos_validados]
                                )

                                st.markdown("### Pré-visualização dos Dados")

                                st.dataframe(
                                    df_resultado,
                                    use_container_width=True,
                                    hide_index=True,
                                    column_config={
                                        "preco_ml": st.column_config.NumberColumn(
                                            "Preço ML", format="R$ %.2f"
                                        ),
                                        "preco_avista": st.column_config.NumberColumn(
                                            "Preço À Vista", format="R$ %.2f"
                                        ),
                                    },
                                )

                                # ------------------------------------------------
                                # Download
                                # ------------------------------------------------

                                with open(f"{caminho_zip}.zip", "rb") as zip_file:
                                    st.download_button(
                                        label=(
                                            "📥 Baixar Pastas com Descrições (.ZIP)"
                                        ),
                                        data=zip_file,
                                        file_name=("Arquivos_Guidon_Rodas.zip"),
                                        mime="application/zip",
                                        type="primary",
                                    )

                        except Exception as e:
                            st.error(f"Erro ao processar: {e}")


# ============================================================
# ABA 2 — MONTAGEM DE IMAGENS
# ============================================================

with aba_imagens:
    st.subheader("🖼️ Montagem de Imagens")

    st.markdown("Envie até duas imagens para criar uma montagem 2×2.")

    st.divider()

    arquivos_imagens = st.file_uploader(
        "Selecione as imagens",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True,
        key="imagens_upload",
    )

    if arquivos_imagens:
        # ------------------------------------------------------------
        # Limite de duas imagens
        # ------------------------------------------------------------

        if len(arquivos_imagens) > 2:
            st.warning("Selecione no máximo 2 imagens.")

        else:
            st.markdown("### Imagens selecionadas")

            # --------------------------------------------------------
            # MINIATURAS
            # --------------------------------------------------------

            if len(arquivos_imagens) == 1:
                col_img1, col_vazia = st.columns(2)

                with col_img1:
                    st.image(
                        arquivos_imagens[0], caption=arquivos_imagens[0].name, width=200
                    )

            else:
                col_img1, col_img2 = st.columns(2)

                with col_img1:
                    st.image(
                        arquivos_imagens[0], caption=arquivos_imagens[0].name, width=200
                    )

                with col_img2:
                    st.image(
                        arquivos_imagens[1], caption=arquivos_imagens[1].name, width=200
                    )

            st.divider()

            # --------------------------------------------------------
            # BOTÃO DE GERAÇÃO
            # --------------------------------------------------------

            if st.button(
                "🖼️ Gerar Montagem 2×2", type="primary", use_container_width=True
            ):
                with st.spinner("Gerando montagem..."):
                    try:
                        # ------------------------------------------------
                        # Cria diretório temporário
                        # ------------------------------------------------

                        with tempfile.TemporaryDirectory() as temp_dir_str:
                            pasta_imagens = Path(temp_dir_str)

                            # ------------------------------------------------
                            # Salva os arquivos enviados
                            # ------------------------------------------------

                            nomes_imagens = []

                            for arquivo in arquivos_imagens:
                                caminho_imagem = pasta_imagens / arquivo.name

                                with open(caminho_imagem, "wb") as f:
                                    f.write(arquivo.getvalue())

                                nomes_imagens.append(arquivo.name)

                            # ------------------------------------------------
                            # Executa a montagem
                            # ------------------------------------------------
                            #
                            # A função recebe:
                            #
                            # criar_montagem(
                            #     diretorio,
                            #     imagens
                            # )
                            #
                            # ------------------------------------------------

                            sucesso = criar_montagem(str(pasta_imagens), nomes_imagens)

                            if not sucesso:
                                st.error("Não foi possível gerar a montagem.")

                            else:
                                # ------------------------------------------------
                                # Descobre o nome do arquivo gerado
                                # ------------------------------------------------

                                if len(nomes_imagens) == 1:
                                    nome_saida = (
                                        f"quadrado_{Path(nomes_imagens[0]).stem}.jpg"
                                    )

                                else:
                                    nome_saida = (
                                        f"quadrado_"
                                        f"{Path(nomes_imagens[0]).stem}"
                                        f"_"
                                        f"{Path(nomes_imagens[1]).stem}"
                                        f".jpg"
                                    )

                                caminho_resultado = pasta_imagens / nome_saida

                                if caminho_resultado.exists():
                                    dados_imagem = caminho_resultado.read_bytes()

                                    st.success("✅ Montagem criada com sucesso!")

                                    # ------------------------------------------------
                                    # Pré-visualização da montagem
                                    # ------------------------------------------------

                                    st.markdown("### Montagem gerada")

                                    st.image(
                                        dados_imagem, caption=nome_saida, width=400
                                    )

                                    # ------------------------------------------------
                                    # Download
                                    # ------------------------------------------------

                                    st.download_button(
                                        label=("📥 Baixar Montagem"),
                                        data=dados_imagem,
                                        file_name=nome_saida,
                                        mime="image/jpeg",
                                        type="primary",
                                        use_container_width=True,
                                    )

                                else:
                                    st.error(
                                        "A montagem foi executada, "
                                        "mas o arquivo de saída não foi encontrado."
                                    )

                    except Exception as e:
                        st.error(f"Não foi possível gerar a montagem: {e}")
