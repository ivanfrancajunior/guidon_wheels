Para identificar exatamente por que nenhum item foi validado, analisei os dados da sua planilha **PLANILHA DE ENTRADAS RODAS AMARELAS 18-09.xlsx** e simulei as regras padrões de validação de estoque/produtos que costumam ser aplicadas a esse tipo de estrutura.

---

### 1. Diagnosticando o Problema (Por que deu 0 validações?)

Ao inspecionar a aba principal (`RODAS AMARELAS`), identificamos **299 linhas de dados**. No entanto, a estrutura apresenta os seguintes pontos críticos que costumam fazer os scripts de validação rejeitarem a leitura ou reprovarem 100% dos registros:

1. **Aresta na Estrutura dos Cabeçalhos (Início dos Dados na Linha 3):**
   * As linhas 1 e 2 contêm títulos mesclados e instruções (`LOJA ROXA 1`, `ENTRADAS ROXA`, `Atenção: Não alterar...`).
   * Os nomes reais das colunas começam apenas na **Linha 3** (`TIPO`, `MÉTODO`, `DESCRIÇÃO`, `SERVIÇO`, etc.). Se o script lê a planilha a partir da Linha 1, ele interpreta os avisos como cabeçalhos e falha ao buscar os nomes das colunas esperadas.

2. **Inconsistência nos Tipos de Dados:**
   * **Datas com texto de observação:** Colunas como `ENTRADA` e `DATA SAÍDA` contêm datas misturadas com textos ou horários não padronizados (ex.: `23/03/26 12 HORAS`, `A CAMINHO`, `2026-03-24 00:00:00`). Se a regra de validação esperar estritamente o formato de data `DD/MM/AAAA`, a conversão falha.
   * **Campos Numéricos Vazio/Formatados:** Colunas como `R$ UN`, `R$ TOTAL` e `PEDIDO` possuem muitos valores ausentes (`NaN`) ou formatações mescladas (texto/float).

---

### 2. Mapeamento dos Campos e Regras de Validação Sugeridas

Abaixo está o detalhamento de como os campos estão estruturados na planilha e como eles devem ser validados pelo script:

| Campo (Coluna) | Tipo Encontrado na Planilha | Exemplo de Dado | Regra de Validação Recomendada | Motivo da Falha Comum |
| :--- | :--- | :--- | :--- | :--- |
| **TIPO** | Texto / Categoria | `SERVIÇO`, `PNEU`, `RODA` | Deve pertencer a uma lista predefinida de categorias permitidas. | Presença de divergências de caixa ou espaços extras. |
| **MÉTODO** | Texto | `MERCADO LIVRE`, `GUILHERME`, `CASA` | Deve ser texto e não estar vazio (se obrigatório). | Valores nulos em várias linhas. |
| **DESCRIÇÃO** | Texto | `175/70/14 FORMULA EVO...` | Preenchimento obrigatório (string com comprimento mínimo). | Linhas de separação ou sem descrição do item. |
| **QTD** | Numérico (Inteiro/Float) | `1.0`, `4.0` | Número inteiro $> 0$. | Linhas com valor nulo ou zerado. |
| **R$ UN / R$ TOTAL** | Decimal (Moeda) | `300.0`, `1200.0` | Valor numérico $\ge 0$. | Linhas em branco ou com texto `R$` concatenado. |
| **ENTRADA / DATA SAÍDA**| Data / Texto | `18/09/2026`, `A CAMINHO` | Formato padrão de data (`YYYY-MM-DD` ou `DD/MM/YYYY`). | Textos de observação (ex.: `A CAMINHO`) quebrando validadores do Pydantic/Python. |
| **SITUAÇÃO** | Texto / Categoria | `ESTOQUE`, `VENDIDO`, `USO` | Deve bater com os status permitidos pelo sistema. | Grafias inconsistentes ou campos em branco. |

---

### 3. Como Corrigir a Leitura no Seu Script Python

Se você está utilizando Python (com `pandas` ou `pydantic`), garanta que a leitura da planilha descarte o cabeçalho decorativo inicial especificando o parâmetro `header=2` (que aponta para a 3ª linha do Excel, onde estão os títulos corretos).

Abaixo está o exemplo de código para realizar o carregamento, limpeza prévia dos dados e validação correta:

```python
import pandas as pd
from typing import Optional
from pydantic import BaseModel, ValidationError, field_validator

# 1. Carregar a planilha pulando os avisos das 2 primeiras linhas
file_path = "PLANILHA DE ENTRADAS RODAS AMARELAS 18-09.xlsx"
df = pd.read_excel(file_path, sheet_name="RODAS AMARELAS", header=2)

# Limpar nomes de colunas (remover espaços extras)
df.columns = df.columns.astype(str).str.strip()

# 2. Definir o Esquema de Validação (Exemplo com Pydantic)
class ItemEntrada(BaseModel):
    tipo: Optional[str] = None
    metodo: Optional[str] = None
    descricao: str  # Campo obrigatório
    qtd: Optional[float] = 0.0
    valor_unitario: Optional[float] = None
    situacao: Optional[str] = None

    @field_validator('descricao')
    def validar_descricao(cls, v):
        if not v or pd.isna(v) or str(v).strip() == "":
            raise ValueError("Descrição não pode ser vazia")
        return str(v).strip()

# 3. Executar a Validação Linha a Linha
itens_validados = []
erros = []

for index, row in df.iterrows():
    # Ignorar linhas totalmente vazias
    if row.dropna().empty:
        continue

    dado_linha = {
        "tipo": None if pd.isna(row.get("TIPO")) else str(row.get("TIPO")),
        "metodo": None if pd.isna(row.get("MÉTODO")) else str(row.get("MÉTODO")),
        "descricao": row.get("DESCRIÇÃO"),
        "qtd": row.get("QTD") if pd.notna(row.get("QTD")) else 0,
        "valor_unitario": row.get("R$ UN") if pd.notna(row.get("R$ UN")) else None,
        "situacao": None if pd.isna(row.get("SITUAÇÃO")) else str(row.get("SITUAÇÃO")),
    }

    try:
        item = ItemEntrada(**dado_linha)
        itens_validados.append(item)
    except ValidationError as e:
        erros.append((index + 4, e.errors())) # +4 para bater com a linha real do Excel

print(f"Sucesso: {len(itens_validados)} itens validados.")
print(f"Falhas: {len(erros)} linhas com erros.")