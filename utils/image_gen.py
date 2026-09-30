import os
from pathlib import Path
from PIL import Image


# ============================================================
# CONFIGURAÇÕES
# ============================================================

EXTENSOES = (".jpg", ".jpeg", ".png", ".webp")

PREFIXOS_IGNORADOS = (
    "quadrado_",
    "par_",
    "grid4_",
    "colado_",
)


# ============================================================
# SELEÇÃO DE DIRETÓRIO
# ============================================================

def selecionar_diretorio():
    """
    Solicita ao usuário o diretório onde estão as imagens.
    """

    while True:
        diretorio = input(
            "\nDigite o caminho do diretório com as imagens: "
        ).strip().strip('"')

        if not diretorio:
            print("Nenhum diretório informado.")
            continue

        caminho = Path(diretorio)

        if not caminho.exists():
            print("Diretório não encontrado.")
            continue

        if not caminho.is_dir():
            print("O caminho informado não é um diretório.")
            continue

        return caminho


# ============================================================
# ENCONTRAR IMAGENS
# ============================================================

def encontrar_imagens(diretorio):
    """
    Encontra as imagens válidas dentro do diretório.

    Imagens já geradas pelo script são ignoradas.
    """

    diretorio = Path(diretorio)

    imagens = []

    for arquivo in diretorio.iterdir():

        if not arquivo.is_file():
            continue

        if arquivo.suffix.lower() not in EXTENSOES:
            continue

        nome = arquivo.name.lower()

        if nome.startswith(PREFIXOS_IGNORADOS):
            continue

        imagens.append(arquivo.name)

    return sorted(imagens)


# ============================================================
# CRIAR MONTAGEM 2x2
# ============================================================

def criar_montagem(diretorio, imagens):
    """
    Cria uma montagem 2x2 utilizando as imagens originais.

    IMPORTANTE:
    - Não redimensiona as imagens.
    - Não corta as imagens.
    - Não altera a proporção.
    - Não define resolução máxima.
    - Não estica as imagens.

    A imagem final terá o dobro da largura e o dobro
    da altura das imagens de entrada.

    Espera duas imagens.
    """

    diretorio = Path(diretorio)

    if not imagens:
        print("Nenhuma imagem encontrada.")
        return False

    if len(imagens) > 2:
        print("Foram encontradas mais de duas imagens.")
        print("A montagem utiliza apenas duas imagens.")
        imagens = imagens[:2]

    # --------------------------------------------------------
    # CASO TENHA APENAS UMA IMAGEM
    # --------------------------------------------------------

    if len(imagens) == 1:

        nome_imagem = imagens[0]
        caminho_imagem = diretorio / nome_imagem

        try:
            imagem_1 = Image.open(caminho_imagem).convert("RGB")
        except Exception as erro:
            print(f"Erro ao abrir a imagem: {erro}")
            return False

        largura, altura = imagem_1.size

        # Tela final: 2x2 da própria imagem
        montagem = Image.new(
            "RGB",
            (largura * 2, altura * 2)
        )

        # A mesma imagem nos quatro quadrantes
        montagem.paste(imagem_1, (0, 0))
        montagem.paste(imagem_1, (largura, 0))
        montagem.paste(imagem_1, (0, altura))
        montagem.paste(imagem_1, (largura, altura))

        nome_saida = f"quadrado_{Path(nome_imagem).stem}.jpg"

        caminho_saida = diretorio / nome_saida

        montagem.save(
            caminho_saida,
            format="JPEG",
            quality=95
        )

        print(f"Montagem criada: {caminho_saida}")

        return True

    # --------------------------------------------------------
    # DUAS IMAGENS
    # --------------------------------------------------------

    nome_imagem_1 = imagens[0]
    nome_imagem_2 = imagens[1]

    caminho_imagem_1 = diretorio / nome_imagem_1
    caminho_imagem_2 = diretorio / nome_imagem_2

    try:
        imagem_1 = Image.open(caminho_imagem_1).convert("RGB")
        imagem_2 = Image.open(caminho_imagem_2).convert("RGB")

    except Exception as erro:
        print(f"Erro ao abrir as imagens: {erro}")
        return False

    # --------------------------------------------------------
    # DIMENSÕES ORIGINAIS
    # --------------------------------------------------------
    #
    # Não fazemos nenhum resize.
    #
    # Como você informou que as duas imagens sempre terão
    # as mesmas dimensões, utilizamos diretamente o tamanho
    # da primeira imagem.
    #
    # Exemplo:
    #
    # 1000 x 1000 -> montagem 2000 x 2000
    #
    # 1200 x 900 -> montagem 2400 x 1800
    #
    # --------------------------------------------------------

    largura, altura = imagem_1.size

    # Verificação apenas para evitar uma montagem desalinhada
    # caso futuramente sejam fornecidas imagens diferentes.

    if imagem_2.size != imagem_1.size:

        print(
            "As imagens possuem dimensões diferentes."
        )

        print(
            f"Imagem 1: {imagem_1.size[0]}x{imagem_1.size[1]}"
        )

        print(
            f"Imagem 2: {imagem_2.size[0]}x{imagem_2.size[1]}"
        )

        print(
            "A montagem exige duas imagens com as mesmas dimensões."
        )

        return False

    # --------------------------------------------------------
    # CRIA A TELA FINAL
    # --------------------------------------------------------

    montagem = Image.new(
        "RGB",
        (
            largura * 2,
            altura * 2
        )
    )

    # --------------------------------------------------------
    # POSICIONAMENTO
    # --------------------------------------------------------
    #
    # IMAGEM 1 | IMAGEM 2
    # -------------------
    # IMAGEM 1 | IMAGEM 2
    #
    # --------------------------------------------------------

    montagem.paste(
        imagem_1,
        (0, 0)
    )

    montagem.paste(
        imagem_2,
        (largura, 0)
    )

    montagem.paste(
        imagem_1,
        (0, altura)
    )

    montagem.paste(
        imagem_2,
        (largura, altura)
    )

    # --------------------------------------------------------
    # NOME DO ARQUIVO
    # --------------------------------------------------------

    nome_1 = Path(nome_imagem_1).stem
    nome_2 = Path(nome_imagem_2).stem

    nome_saida = f"quadrado_{nome_1}_{nome_2}.jpg"

    caminho_saida = diretorio / nome_saida

    # --------------------------------------------------------
    # SALVAR
    # --------------------------------------------------------

    montagem.save(
        caminho_saida,
        format="JPEG",
        quality=95
    )

    print()
    print("Montagem criada com sucesso!")
    print(f"Arquivo: {caminho_saida}")
    print(f"Dimensão original: {largura}x{altura}")
    print(
        f"Dimensão final: {largura * 2}x{altura * 2}"
    )

    return True


# ============================================================
# PROCESSAR DIRETÓRIO
# ============================================================

def processar_diretorio_raiz(diretorio_raiz):
    """
    Processa o diretório informado e suas subpastas.

    Cada pasta que possuir imagens terá uma montagem criada.
    """

    diretorio_raiz = Path(diretorio_raiz)

    if not diretorio_raiz.exists():
        print("Diretório não encontrado.")
        return

    if not diretorio_raiz.is_dir():
        print("O caminho informado não é um diretório.")
        return

    print()
    print("=" * 60)
    print("PROCESSANDO IMAGENS")
    print("=" * 60)

    total_processadas = 0

    # Inclui o próprio diretório e todas as subpastas
    diretorios = [diretorio_raiz]

    diretorios.extend(
        pasta
        for pasta in diretorio_raiz.rglob("*")
        if pasta.is_dir()
    )

    for diretorio in diretorios:

        imagens = encontrar_imagens(diretorio)

        if not imagens:
            continue

        print()
        print(f"Diretório: {diretorio}")
        print(f"Imagens encontradas: {len(imagens)}")

        if criar_montagem(diretorio, imagens):
            total_processadas += 1

    print()
    print("=" * 60)
    print("PROCESSAMENTO FINALIZADO")
    print(f"Montagens criadas: {total_processadas}")
    print("=" * 60)


# ============================================================
# EXECUÇÃO DIRETA
# ============================================================

if __name__ == "__main__":

    diretorio = selecionar_diretorio()

    processar_diretorio_raiz(diretorio)