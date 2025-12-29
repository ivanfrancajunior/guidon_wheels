<h1 align="center">
Guidon Organizer - Versão 2.0
</h1>

<p align="center">
<img src="assets/logo_guidom.png" alt="Guidom Logo" width="200"/>
</p>

<img src="https://i.imgur.com/waxVImv.png" width="100%"/>

## � Sobre o Projeto
O **Guidon Organizer 2.0** é uma solução de engenharia de software para automação de catálogos automotivos. O projeto evoluiu de um script simples para uma arquitetura robusta e escalável, focada em resolver o problema de conversão de dados brutos (planilhas) em estruturas de marketing digital prontas para uso.

Este projeto demonstra competências em:
- **Engenharia de Prompt & Automação**
- **Validação de Dados Rigorosa**
- **Arquitetura Baseada em Serviços**
- **Processamento de Linguagem Natural (via Expressões Regulares)**

---

## �️ Stack Técnica
- **Linguagem:** Python 3.10+
- **Validação:** [Pydantic v2](https://docs.pydantic.dev/) (Data Integrity & Type Safety)
- **Manipulação de Dados:** Pandas
- **Segurança e Caminhos:** Pathlib (Cross-platform compatibility)
- **Interface:** CLI (Command Line Interface) resiliente

---

## 🏗️ Arquitetura e Design Patterns

O projeto segue os princípios de **Clean Code** e **Separation of Concerns (SoC)**, dividindo a lógica em camadas:

### 1. Camada de Domínio (Core Models)
Utilizamos o **Pydantic** para garantir que nenhum dado inválido entre no sistema. Os modelos definem não apenas a estrutura, mas o comportamento dos dados.

```python
# Exemplo de validação funcional no models.py
class ProdutoBase(BaseModel):
    fabricante: str = Field(..., alias="fabricante")
    preco_avista: float = Field(default=0.0, alias="olx | face")

    @field_validator("fabricante", mode="before")
    def validate_brand(cls, value):
        if isinstance(value, str):
            # Normalização automática para consistência no banco de dados
            return value.strip().upper()
        return value
```

### 2. Camada de Serviços (Business Logic)
Os serviços são especialistas em tarefas únicas (Solid SRP):
- **ContentBuilder**: O "cérebro" da aplicação. Extrai medidas complexas e injeta dados em templates.
- **ImageManager**: Gerencia ativos visuais com base em heurísticas de material e tipo de produto.
- **FileManager**: Abstrai a complexidade do sistema de arquivos OS-dependent.

---

## 🧠 Destaque Técnico: Extração Inteligente de Medidas

Um dos maiores desafios técnicos foi extrair informações técnicas (Aro, Tala, Furação) a partir de nomes descritivos variados. Implementamos um buscador baseado em **Regex** (Expressões Regulares) que identifica padrões múltiplos.

```python
# Lógica de extração no content_builder.py
def _extract_measures_from_name(self, texto: str) -> Dict[str, str]:
    # Regex para capturar padrões como "14x5.5x100" ou "15x6"
    match_triplo = re.search(r"(\d{2})[xX](\d+[.,]?\d?)[xX](\d+[.,]?\d?)", texto)

    if match_triplo:
        return {
            "aro": match_triplo.group(1),
            "tala": f"{match_triplo.group(2)} e {match_triplo.group(3)}"
        }
    # ... lógica para furações conhecidas e padrões duplos
```

---

## 🔄 Fluxo de Orquestração Resiliente

O orquestrador em `main.py` foi desenhado para ser "à prova de falhas". Em vez de interromper o processamento total em caso de um erro na planilha, ele isola a falha e reporta o log, garantindo a continuidade do lote.

1. **Ingestão:** Carregamento de CSV/Excel via Pandas.
2. **Normalização:** Conversão de cabeçalhos para lowercase e remoção de ruídos.
3. **Instanciação:** Conversão de linhas em objetos Pydantic validados.
4. **Execução:**
   - Criação de pastas físicas.
   - Aplicação de templates de texto.
   - Gerenciamento de Assets (imagens).
5. **Report:** Resumo final de sucessos e erros.

---

## 📊 Requisitos de Dados

Para portabilidade, o sistema aceita os seguintes cabeçalhos (case-insensitive):

`DATA`, `FABRICANTE`, `MODELO`, `NÚMERO DE PEÇA / SKU`, `QTD`, `ACABAMENTO`, `MATERIAL`, `OLX | FACE`, `ML`, `CONCORRÊNCIA`, `ET`, `ARO`, `TALA`, `DIÂMETRO`.

---

## 🚀 Como Executar

```bash
# 1. Instale as dependências
pip install -r requirements.txt

# 2. Execute o orquestrador
python main.py
```

---

<p align="center">
Desenvolvido com foco em performance e qualidade de código para <b>Guidon - Rodas Antigas</b>.
</p>
