import sys
from pathlib import Path
import re
sys.path.append(str(Path(__file__).parent))

from src.guidon.core.models import ProdutoBase, Roda, Calota

def test_fixes():
    print("=== Iniciando Verificação ===")

    # 1. Teste de Caixa Alta e Marcas
    print("\n[Teste 1] Caixa Alta e Substituição de Marcas")
    p1 = ProdutoBase(
        fabricante="volks",
        modelo="Gol g5",
        sku="123",
        acabamento="Preto Fosco",
        material="Liga Leve"
    )

    print(f"Input: fabricante='volks', modelo='Gol g5'")
    print(f"Output: fabricante='{p1.fabricante}', modelo='{p1.modelo}'")

    assert p1.fabricante == "Volkswagen", f"Erro: fabricante esperava 'Volkswagen', veio '{p1.fabricante}'"
    assert p1.modelo == "Gol g5", f"Erro: modelo esperava 'Gol g5', veio '{p1.modelo}'"

    p2 = ProdutoBase(
        fabricante="GM",
        modelo="Corsa",
        sku="999"
    )
    assert p2.fabricante == "Chevrolet"

    # 2. Teste de Rodas (Strings e Multiplos Valores)
    print("\n[Teste 2] Rodas com Múltiplos Valores")
    r1 = Roda(
        fabricante="Ramlow",
        modelo="P90",
        sku="R1",
        aro="17 e 18",
        tala="7 e 8",
        et="40 e 42"
    )
    assert r1.aro == "17 e 18"
    assert r1.tala == "7 e 8"
    assert r1.offset == "40 e 42"

    # 3. Teste de Rodas (Conversão de Números)
    print("\n[Teste 3] Rodas com Valores Numéricos")
    r2 = Roda(
        fabricante="Krmai",
        modelo="K1",
        sku="K2",
        aro=15,
        tala=6.0,
        et=40
    )
    assert r2.aro == "15"
    assert r2.tala == "6.0"
    assert r2.offset == "40"

    # 4. Teste de Regex do Modelo
    print("\n[Teste 4] Regex de Extração de Modelo")
    r3 = Roda(
        fabricante="BBS",
        modelo="Roda Guidon BBS RS 17x7", # Deve virar "BBS RS"
        sku="SKU-REGEX",
        aro="17",
        tala="7"
    )
    print(f"Input: modelo='Roda Guidon BBS RS 17x7'")
    print(f"Output: modelo='{r3.modelo}'")

    assert r3.modelo == "BBS RS", f"Erro: Esperado 'BBS RS', recebido '{r3.modelo}'"

    print("\n=== Verificação Concluída com SUCESSO! ===")

if __name__ == "__main__":
    try:
        test_fixes()
    except AssertionError as e:
        print(f"\n❌ FALHA: {e}")
    except Exception as e:
        print(f"\n❌ ERRO DE EXECUÇÃO: {e}")
