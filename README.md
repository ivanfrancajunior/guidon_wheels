<h1 align="center">
Guidon Organizer - Versão 2.0
</h1>

<p align="center">
<img src="assets/logo_guidom.png" alt="Guidom Logo" width="200"/>
</p>

<img src="https://i.imgur.com/waxVImv.png" width="100%"/>

## 📝 Sobre o Projeto
O **Guidon Organizer 2.0** é uma ferramenta desenvolvida para agilizar o dia a dia da **Guidon - Rodas Antigas**. O objetivo é simples e direto: automatizar a criação de materiais para anúncios.

A partir de uma planilha (CSV ou Excel), o script separa cada item em sua própria pasta e gera automaticamente os textos de venda:
1.  **descricao.txt**: Um texto completo com características técnicas para plataformas de venda.
2.  **grupo.txt**: Uma versão resumida e formatada especificamente para postagens rápidas em grupos de WhatsApp/Facebook.

Nesta versão 2.0, o foco foi transformar um script funcional em um código mais profissional, usando validação de dados e separação de tarefas, o que o torna um ótimo exemplo de **automação para portfólio**.

---

## ⚙️ Como funciona (Destaques Técnicos)

Abaixo, explico como resolvi alguns desafios comuns de automação usando Python:

### 1. Garantia de que os dados estão corretos (Pydantic)
Diferente de scripts simples que podem quebrar com uma célula vazia na planilha, aqui usamos o **Pydantic** para validar se os preços são números, se o fabricante existe e para limpar textos (remover espaços extras e colocar em maiúsculo) antes de criar os arquivos.

```python
# Trecho do models.py que limpa e valida a marca automaticamente
@field_validator("fabricante", mode="before")
def validate_columns_names(cls, value):
    if isinstance(value, str):
        return value.strip().upper() # Padroniza para "VOLKSWAGEN" em vez de "  volks "
    return value
```

### 2. "Lendo" medidas direto do nome (Regex)
Para evitar que o usuário precise preencher cada detalhe (aro, tala, furação) em colunas separadas, implementei um buscador que usa **Expressões Regulares** para identificar esses padrões dentro do nome do produto.

```python
# Lógica em content_builder.py que identifica "15x6" ou "14x5.5" no texto
match = re.search(r"(\d{2})[xX](\d{1,2}(?:[.,]\d)?)", texto)
if match:
    aro = match.group(1)
    tala = match.group(2)
```

### 3. Orquestração sem interrupções
O script foi desenhado para não parar no meio do caminho. Se a linha 10 da planilha estiver com erro, ele avisa no terminal, pula o item e continua processando os próximos até o fim.

---

## 📂 Organização do Código
O projeto é dividido em módulos para facilitar o entendimento:
- **`main.py`**: O "chefe" que pede os dados ao usuário e coordena os serviços.
- **`src/`**: Onde fica toda a inteligência (validação, leitura de planilha e criação de textos).
- **`templates/`**: Modelos de texto que o sistema usa para preencher os arquivos `.txt`.

---

## 📊 O que a planilha deve ter?
O sistema aceita planilhas com os seguintes cabeçalhos (não importa se maiúsculo ou minúsculo):

`DATA`, `FABRICANTE`, `MODELO`, `SKU`, `QTD`, `ACABAMENTO`, `MATERIAL`, `OLX | FACE`, `ML`, `CONCORRÊNCIA`, `ET`, `ARO`, `TALA`, `DIÂMETRO`.

---

## 🚀 Como usar
1. Instale as bibliotecas necessárias: `pip install pandas openpyxl pydantic`.
2. Execute o script: `python main.py`.
3. Arraste sua planilha para o terminal e escolha a pasta de destino.

<p align="center">
Simplificando o estoque e as vendas da <b>Guidon - Rodas Antigas</b>.
</p>
