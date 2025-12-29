import sys
from pathlib import Path

# Garante que o Python encontre os módulos na pasta src
sys.path.append(".")

from src.guidon.services.content_builder import ContentBuilder
from src.guidon.services.file_manager import FileManager
from src.guidon.services.image_manager import ImageManager
from src.guidon.services.loader import load_products


def main():
    print("\n" + "=" * 50)
    print("🚀 SISTEMA DE AUTOMAÇÃO GUIDON - ORQUESTRADOR")
    print("=" * 50)

    # --- 1. ENTRADA DE DADOS ---
    while True:
        caminho_input = (
            input("\n📂 Arraste a planilha original aqui: ")
            .strip()
            .replace('"', "")
            .replace("'", "")
        )
        path_planilha = Path(caminho_input)
        if path_planilha.exists():
            break
        print("❌ Arquivo não encontrado. Tente novamente.")

    # --- 2. DEFINIÇÃO DO TIPO (Com Identificação Automática) ---
    tipo_produto = (
        input(
            "\n🛠️  Tipo de produto (roda / calota / calotao) [Deixe vazio para auto-identificar]: "
        )
        .strip()
        .lower()
    )

    if not tipo_produto:
        # Lógica simples de identificação pelo nome do arquivo
        nome_arquivo = path_planilha.name.lower()
        if "roda" in nome_arquivo:
            tipo_produto = "roda"
        elif "calotao" in nome_arquivo or "calotão" in nome_arquivo:
            tipo_produto = "calotao"
        elif "calota" in nome_arquivo:
            tipo_produto = "calota"
        else:
            print("⚠️  Não foi possível identificar o tipo automaticamente.")
            tipo_produto = "roda"  # Fallback

    print(f"✨ Tipo definido como: {tipo_produto.upper()}")

    # --- 3. CAMINHO DE SAÍDA ---
    caminho_saida_input = (
        input("\n📍 Onde deseja criar as pastas? (Enter para pasta atual): ")
        .strip()
        .replace('"', "")
        .replace("'", "")
    )
    path_saida = (
        Path(caminho_saida_input)
        if caminho_saida_input
        else Path.cwd() / "ANUNCIOS_GERADOS"
    )

    # --- 4. ORQUESTRAÇÃO (Delegação para os Services) ---
    try:
        # A. Carregamento dos dados
        print("\n⏳ Lendo dados da planilha...")
        produtos = load_products(path_planilha, tipo_produto)

        if not produtos:
            print("❌ Nenhun produto válido encontrado na planilha.")
            return

        # B. Inicialização dos Serviços
        file_manager = FileManager(path_saida)
        content_builder = ContentBuilder()
        image_manager = ImageManager()

        # C. Criação de Estrutura Inicial (Batch)
        # O FileManager é mais eficiente criando tudo de uma vez
        print("\n🏗️  Verificando estrutura de pastas...")
        file_manager.create_folders(produtos)

        print(f"\n📦 Processando conteúdo para {len(produtos)} itens...")

        sucessos = 0
        erros = 0

        for idx, produto in enumerate(produtos, start=1):
            try:
                # Reconstrói o caminho da pasta (Lógica deve bater com services/models)
                dir_name = f"{idx}_{produto.format_dirname}"
                pasta_produto = path_saida / dir_name

                # Doador de Segurança: Garante que a pasta existe
                if not pasta_produto.exists():
                    pasta_produto.mkdir(parents=True, exist_ok=True)

                # D. Geração da Descrição (ContentBuilder)
                # O service já salva o arquivo internamente
                content_builder.create_content(produto, pasta_produto)

                # E. Gestão de Imagens (ImageManager)
                # O service decide se copia ou não
                image_manager.process_images(produto, pasta_produto)

                sucessos += 1

            except Exception as e_item:
                erros += 1
                print(f"   [❌] Falha no item {idx} ({produto.sku}): {e_item}")

        print("\n" + "=" * 50)
        print(f"✨ FINALIZADO! Sucessos: {sucessos} | Erros: {erros}")
        print(f"📂 Pastas criadas em: {path_saida.absolute()}")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ ERRO DURANTE A ORQUESTRAÇÃO: {e}")

    input("\nPressione ENTER para sair...")


if __name__ == "__main__":
    main()
