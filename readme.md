<h1 align="center">
Calota Organizer - Versão 1.2
 </h1>

<p align="center">
<img src="logo_guidom.png" alt="Guidom Logo" width="200"/>
</p>

## <img src="https://i.imgur.com/waxVImv.png" width="100%"/>

## **Descrição**

O **Calota Organizer** é uma ferramenta Python projetada para organizar informações sobre rodas e calotas a partir de uma planilha Excel ou CSV. Ele cria pastas individuais para cada item da planilha, gera arquivos de descrição detalhados (`descricao.txt`) e um arquivo consolidado de aprovação (`aprovacao.txt`).

---

## **Funcionalidades Principais**

<ul>
  <li><strong>Leitura de Planilha:</strong> Suporta arquivos .csv e .xlsx.</li>
  <li><strong>Criação de Pastas e Arquivos:</strong> Gera pastas nomeadas com base no fabricante e modelo, contendo um arquivo `descricao.txt` detalhado.</li>
  <li><strong>Arquivo Consolidado de Aprovação:</strong> Cria um arquivo `aprovacao.txt` no diretório raiz, listando todas as rodas/calotas organizadas.</li>
  <li><strong>Tratamento de Nomes de Colunas:</strong> Remove automaticamente espaços extras nos nomes das colunas da planilha para evitar erros.</li>
  <li><strong>Codificação UTF-8:</strong> Garante compatibilidade com caracteres especiais em todos os arquivos gerados.</li>
</ul>

---

## **Alterações na Versão 1.2**

### **Correções e Melhorias**

<ul>
  <li><strong>Remoção de Espaços Extras nos Nomes de Colunas:</strong> Ajuste no código para remover automaticamente espaços extras nos nomes das colunas da planilha.</li>
  <li><strong>Correção de Erros Relacionados às Colunas:</strong> Adicionada uma verificação para garantir que todas as colunas necessárias existam na planilha.</li>
  <li><strong>Template de Aprovação Exato:</strong> O template de aprovação foi ajustado para seguir exatamente o formato fornecido pelo usuário.</li>
  <li><strong>Manutenção do Campo "Ano":</strong> O campo `ANO` continua sendo usado no arquivo `descricao.txt`, mas foi removido do arquivo `aprovacao.txt`.</li>
  <li><strong>Compatibilidade com Diferentes Formatos de Planilha:</strong> O script agora suporta tanto arquivos `.csv` quanto `.xlsx`.</li>
  <li><strong>Melhoria na Mensagem de Erro:</strong> Mensagens de erro foram refinadas para facilitar a identificação de problemas.</li>
</ul>

---

## **Como Usar o Script**

### **Pré-requisitos**

<ul>
  <li><strong>Python 3.x</strong> instalado no sistema.</li>
  <li>Bibliotecas Python necessárias:
    <ul>
      <li><code>pandas</code></li>
      <li><code>os</code></li>
    </ul>
  </li>
</ul>

Instale as dependências com o seguinte comando:

```bash
pip install pandas
```

### **Passos para Executar**

<ol>
  <li><strong>Baixe ou Clone o Script:</strong> Salve o arquivo <code>calota_organizer.py</code> em seu computador.</li>
  <li><strong>Prepare a Planilha:</strong> Certifique-se de que sua planilha contenha as seguintes colunas:
    <pre>
DATA, FABRICANTE | MODELO, ANO, QTD, ACABAMENTO, NÚMERO DE PEÇA / SKU, CONCORRÊNCIA, OLX | FACE, TOTAL, POSTADO, VISITAS
    </pre>
  </li>
  <li><strong>Configure o Script:</strong> Abra o arquivo <code>calota_organizer.py</code> e ajuste os seguintes parâmetros:
    ```python
    planilha_path = r"C:\caminho\para\sua_planilha.xlsx"  # Caminho para a planilha
    pasta_raiz = r"C:\caminho\para\diretorio_raiz"        # Diretório onde as pastas serão criadas
    ```
  </li>
  <li><strong>Execute o Script:</strong> Execute o script no terminal:
    ```bash
    python calota_organizer.py
    ```
  </li>
  <li><strong>Verifique os Resultados:</strong> Após a execução, confira o diretório raiz para encontrar as pastas e arquivos gerados.</li>
</ol>

---

## **Estrutura de Saída**

### **Pastas Individuais**

Cada pasta será nomeada no formato:

```
01_Nome_da_Roda
```

Dentro de cada pasta, haverá um arquivo `descricao.txt` com informações detalhadas.

#### **Exemplo de `descricao.txt`**

```plaintext
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

### **Arquivo Consolidado de Aprovação**

No diretório raiz, será gerado um arquivo `aprovacao.txt` com o seguinte formato:

#### **Exemplo de `aprovacao.txt`**

```plaintext
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

## **Observações Importantes**

<ul>
  <li><strong>Formato da Planilha:</strong> Certifique-se de que os nomes das colunas na planilha correspondam exatamente aos esperados pelo script (após a remoção de espaços extras).</li>
  <li><strong>Codificação da Planilha:</strong> Se sua planilha estiver em um formato diferente de UTF-8, pode ser necessário convertê-la antes de usar o script.</li>
  <li><strong>Erros Comuns:</strong>
    <ul>
      <li><strong>Erro ao encontrar colunas:</strong> Verifique se os nomes das colunas na planilha correspondem aos esperados.</li>
      <li><strong>Erro ao criar pastas:</strong> Certifique-se de que o caminho para o diretório raiz esteja correto e que você tenha permissão para criar pastas nesse local.</li>
    </ul>
  </li>
</ul>

---

## **Suporte**

Se precisar de ajuda ou quiser sugerir melhorias, entre em contato com o desenvolvedor ou abra uma issue no repositório do projeto.

