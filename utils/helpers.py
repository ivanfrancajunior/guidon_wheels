import os
import re

def formatar_nome_pasta(nome):
    """Remove caracteres inválidos e substitui espaços por underscores."""
    nome_formatado = ''.join(c for c in nome if c.isalnum() or c in (' ', '_')).strip()
    return nome_formatado.replace(' ', '_')

def carregar_template(caminho):
    """Carrega o conteúdo de um arquivo de template."""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return arquivo.read()