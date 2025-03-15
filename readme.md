# Calota Organizer - Versão 1.2

O **Calota Organizer** é um script Python projetado para organizar informações sobre rodas e calotas a partir de uma planilha Excel ou CSV. Ele cria pastas individuais para cada item da planilha, gera arquivos de descrição detalhados (`descricao.txt`) e um arquivo consolidado de aprovação (`aprovacao.txt`).

---

## Funcionalidades Principais

1. **Leitura de Planilha**:
   - O script lê os dados de uma planilha (`.csv` ou `.xlsx`) contendo informações sobre rodas e calotas.
   - As colunas da planilha incluem: `DATA`, `FABRICANTE | MODELO`, `ANO`, `QTD`, `ACABAMENTO`, `NÚMERO DE PEÇA / SKU`, `CONCORRÊNCIA`, `OLX | FACE`, `TOTAL`, `POSTADO`, e `VISITAS`.

2. **Criação de Pastas e Arquivos**:
   - Para cada linha da planilha, o script cria uma pasta nomeada com base no fabricante e modelo.
   - Cada pasta contém um arquivo `descricao.txt` com informações detalhadas sobre a roda/calota.

3. **Arquivo Consolidado de Aprovação**:
   - Um arquivo `aprovacao.txt` é gerado no diretório raiz, listando todas as rodas/calotas organizadas pelo script.

4. **Tratamento de Nomes de Colunas**:
   - O script remove automaticamente espaços extras nos nomes das colunas da planilha para evitar erros.

5. **Codificação UTF-8**:
   - Todos os arquivos gerados são salvos com codificação UTF-8 para garantir compatibilidade com caracteres especiais.

---

## Alterações na Versão 1.2

### Correções e Melhorias
1. **Remoção de Espaços Extras nos Nomes de Colunas**:
   - Ajuste no código para remover automaticamente espaços extras nos nomes das colunas da planilha. Isso resolve problemas como a coluna `QTD` estar escrita como `"QTD "` (com espaço no final).

2. **Correção de Erros Relacionados às Colunas**:
   - Adicionado uma verificação para garantir que todas as colunas necessárias existam na planilha. Caso falte alguma coluna, o script exibirá uma mensagem de erro clara.

3. **Template de Aprovação Exato**:
   - O template de aprovação foi ajustado para seguir **exatamente** o formato fornecido pelo usuário, sem alterações ou adaptações.

4. **Manutenção do Campo "Ano"**:
   - O campo `ANO` continua sendo usado no arquivo `descricao.txt`, mas foi removido do arquivo `aprovacao.txt`, conforme solicitado.

5. **Compatibilidade com Diferentes Formatos de Planilha**:
   - O script agora suporta tanto arquivos `.csv` quanto `.xlsx`, garantindo maior flexibilidade.

6. **Melhoria na Mensagem de Erro**:
   - Mensagens de erro foram refinadas para facilitar a identificação de problemas, como colunas ausentes ou caminhos incorretos.

---

## Como Usar o Script

### Pré-requisitos
1. **Python 3.x** instalado no sistema.
2. Bibliotecas Python necessárias:
   - `pandas`
   - `os`

Instale as dependências com o seguinte comando:
```bash
pip install pandas
```

### Passos para Executar
1. **Baixe ou Clone o Script**:
   - Salve o arquivo `calota_organizer.py` em seu computador.

2. **Prepare a Planilha**:
   - Certifique-se de que sua planilha contenha as seguintes colunas:
     ```
     DATA, FABRICANTE | MODELO, ANO, QTD, ACABAMENTO, NÚMERO DE PEÇA / SKU, CONCORRÊNCIA, OLX | FACE, TOTAL, POSTADO, VISITAS
     ```

3. **Configure o Script**:
   - Abra o arquivo `calota_organizer.py` e ajuste os seguintes parâmetros:
     ```python
     planilha_path = r"C:\caminho\para\sua_planilha.xlsx"  # Caminho para a planilha
     pasta_raiz = r"C:\caminho\para\diretorio_raiz"        # Diretório onde as pastas serão criadas
     ```

4. **Execute o Script**:
   - Execute o script no terminal:
     ```bash
     python calota_organizer.py
     ```

5. **Verifique os Resultados**:
   - Após a execução, confira o diretório raiz para encontrar as pastas e arquivos gerados.

---

## Estrutura de Saída

### Pastas Individuais
Cada pasta será nomeada no formato:
```
01_Nome_da_Roda
```
Dentro de cada pasta, haverá um arquivo `descricao.txt` com informações detalhadas.

#### Exemplo de `descricao.txt`
```
Descrição da Calota: GM Corsa 14''
Data: 2023-03-15
Ano: 2020
Quantidade: 10
Acabamento: Cromado
SKU: SKU123
Concorrência: Modelo X
Preço OLX / Facebook: R$ 100
Total: R$ 1000
Postado: Sim
Visitas: 500

Esta é uma descrição gerada automaticamente pelo script Calota Organizer.
```

### Arquivo Consolidado de Aprovação
No diretório raiz, será gerado um arquivo `aprovacao.txt` com o seguinte formato:

#### Exemplo de `aprovacao.txt`
```
Arquivo de Aprovação de Rodas
============================

Abaixo estão listadas todas as calotas organizadas pelo script Calota Organizer:

------------------------

*GM Corsa 14''*

Data: 2023-03-15
Quantidade: 10
Acabamento: Cromado
SKU: SKU123
*Concorrência: Modelo X
Preço OLX / Facebook: R$ 100
---------------

------------------------

*Honda City 15''*

Data: 2023-03-16
Quantidade: 5
Acabamento: Polido
SKU: SKU456
*Concorrência: Modelo Y
Preço OLX / Facebook: R$ 150

---------------
...
```

---

## Observações Importantes

1. **Formato da Planilha**:
   - Certifique-se de que os nomes das colunas na planilha correspondam exatamente aos esperados pelo script (após a remoção de espaços extras).

2. **Codificação da Planilha**:
   - Se sua planilha estiver em um formato diferente de UTF-8, pode ser necessário convertê-la antes de usar o script.

3. **Erros Comuns**:
   - **Erro ao encontrar colunas**: Verifique se os nomes das colunas na planilha correspondem aos esperados.
   - **Erro ao criar pastas**: Certifique-se de que o caminho para o diretório raiz esteja correto e que você tenha permissão para criar pastas nesse local.

---

## Suporte

Se precisar de ajuda ou quiser sugerir melhorias, entre em contato com o desenvolvedor ou abra uma issue no repositório do projeto.

