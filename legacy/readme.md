<h1 align="center">
Guidon Organizer - Versão 2.0
</h1>

<p align="center">
<img src="assets/logo_guidom.png" alt="Guidom Logo" width="200"/>
</p>

<img src="https://i.imgur.com/waxVImv.png " width="100%"/>
Descrição
O Guidon Organizer é uma ferramenta Python projetada para organizar informações sobre rodas, calotas e outros produtos automotivos a partir de uma planilha Excel ou CSV. Ele cria pastas individuais para cada item da planilha, gera arquivos de descrição detalhados (descricao.txt) e um arquivo consolidado de aprovação (aprovacao.txt). Agora com suporte para dois tipos de produtos: calotas e rodas de ferro , com descrições personalizadas para cada tipo.

Funcionalidades Principais
<ul>
<li><strong>Leitura de Planilha:</strong> Suporta arquivos .csv e .xlsx.</li>
<li><strong>Criação de Pastas e Arquivos:</strong> Gera pastas nomeadas com base no fabricante e modelo, contendo um arquivo `descricao.txt` detalhado.</li>
<li><strong>Arquivo Consolidado de Aprovação:</strong> Cria um arquivo `aprovacao.txt` no diretório raiz, listando todas as rodas/calotas organizadas.</li>
<li><strong>Identificação de Marcas Conhecidas:</strong> Identifica automaticamente marcas como "VW", "GM", "FIAT", "GRID", etc., e substitui abreviações (ex.: "VW" → "Volkswagen").</li>
<li><strong>Tratamento Especial para "GRID":</strong> Trata "GRID" como uma marca genérica para rodas e mantém sua presença no campo do modelo quando necessário.</li>
<li><strong>Extração Automática de Aro e Modelo:</strong> Para entradas que começam com "Calota Aro", extrai o diâmetro (aro) e o modelo de forma consistente.</li>
<li><strong>Remoção de Caracteres Inválidos:</strong> Remove caracteres inválidos dos nomes de pastas para evitar problemas de criação.</li>
<li><strong>Codificação UTF-8:</strong> Garante compatibilidade com caracteres especiais em todos os arquivos gerados.</li>
<li><strong>Suporte para Calotas e Rodas de Ferro:</strong> Permite ao usuário escolher qual tipo de produto deseja processar na interface gráfica.</li>
</ul>

Alterações na Versão 2.0
Novidades
<ul>
<li><strong>Suporte para Rodas de Ferro:</strong> Adicionado um processador específico para rodas de ferro, com lógicas e descrições personalizadas.</li>
<li><strong>Interface Gráfica:</strong> Implementada uma interface gráfica usando `tkinter`, permitindo ao usuário selecionar o tipo de produto (calota ou roda de ferro), bem como os caminhos da planilha e da pasta raiz.</li>
<li><strong>Arquitetura Modular:</strong> O código foi reestruturado em múltiplos arquivos para facilitar a manutenção e escalabilidade:
<ul>
<li><code>main.py</code>: Ponto de entrada do programa.</li>
<li><code>processors/</code>: Contém classes específicas para processar calotas e rodas de ferro.</li>
<li><code>ui/</code>: Contém a interface gráfica.</li>
<li><code>utils/</code>: Funções auxiliares reutilizáveis.</li>
<li><code>templates/</code>: Modelos de descrição para calotas e rodas de ferro.</li>
</ul>
</li>
<li><strong>Seleção Dinâmica de Descrições:</strong> O script carrega automaticamente a descrição correta com base no tipo de produto selecionado pelo usuário.</li>
<li><strong>Array de Marcas Conhecidas Expandido:</strong> Adicionadas mais marcas ao array, incluindo "LAND ROVER", "RANGE ROVER", "BYD", "MINI COOPER", entre outras.</li>
</ul>

Correções e Melhorias
<ul>
<li><strong>Remoção de Espaços Extras nos Nomes de Colunas:</strong> Ajuste no código para remover automaticamente espaços extras nos nomes das colunas da planilha.</li>
<li><strong>Correção de Erros Relacionados às Colunas:</strong> Adicionada uma verificação para garantir que todas as colunas necessárias existam na planilha.</li>
<li><strong>Melhoria na Mensagem de Erro:</strong> Mensagens de erro foram refinadas para facilitar a identificação de problemas.</li>
<li><strong>Validação de Entradas na Interface Gráfica:</strong> O programa verifica se todos os campos estão preenchidos antes de iniciar o processamento.</li>
</ul>

Como Usar o Script
Pré-requisitos
<ul>
<li><strong>Python 3.x</strong> instalado no sistema.</li>
<li>Bibliotecas Python necessárias:
<ul>
<li><code>pandas</code></li>
<li><code>openpyxl</code></li>
<li><code>tkinter</code> (biblioteca padrão do Python)</li>
</ul>
</li>
</ul>

Instale as dependências com o seguinte comando:

bash


1
pip install -r requirements.txt
Passos para Executar
<ol>
<li><strong>Baixe ou Clone o Projeto:</strong> Salve o repositório em seu computador.</li>
<li><strong>Prepare a Planilha:</strong> Certifique-se de que sua planilha contenha as colunas necessárias para o tipo de produto que deseja processar:
<ul>
<li><strong>Para Calotas:</strong>
<pre>
DATA, FABRICANTE | MODELO, ANO, QTD, ACABAMENTO, MATERIAL, NÚMERO DE PEÇA / SKU, CONCORRÊNCIA, OLX | FACE, ML, TOTAL, POSTADO, VISITAS, USADO
</pre>
</li>
<li><strong>Para Rodas de Ferro:</strong>
<pre>
DATA, FABRICANTE, MODELO, QTD, ET, ACABAMENTO, MATERIAL, SKU, CONCORRÊNCIA, OLX | FACE, ML
</pre>
</li>
</ul>
</li>
<li><strong>Execute o Script:</strong> Execute o script no terminal:
```bash
python main.py
```
</li>
<li><strong>Use a Interface Gráfica:</strong>
<ul>
<li>Selecione o tipo de produto (calota ou roda de ferro).</li>
<li>Informe os caminhos da planilha e da pasta raiz.</li>
<li>Clique em "Executar" para iniciar o processamento.</li>
</ul>
</li>
<li><strong>Verifique os Resultados:</strong> Após a execução, confira o diretório raiz para encontrar as pastas e arquivos gerados.</li>
</ol>

Estrutura de Saída
Pastas Individuais
Cada pasta será nomeada no formato:

```plaintext
# 01_Nome_da_Roda_ou_Calota
Dentro de cada pasta, haverá um arquivo descricao.txt com informações detalhadas.

Exemplo de descricao.txt para Calotas
plaintext

Guidon - Rodas Antigas traz para você as últimas novidades!

**Características e especificações:**
- **Marca:** Volkswagen
- **Modelo:** Gol
- **Diâmetro:** 13''
- **Acabamento/Cor:** Preto
- **Material:** Plástico
- **Garantia:** 3 meses
- **SKU:** SKU123

[Dúvidas frequentes...]

**INFORMAÇÕES IMPORTANTES:**
- **MERCADO ENVIO TRANSPORTA APENAS 1 KIT (4 CALOTAS) POR PEDIDO.**
[Restante do texto...]
Exemplo de descricao.txt para Rodas de Ferro
plaintext

Guidon - Rodas Antigas traz para você as últimas novidades!

**Características e especificações:**
- **Marca:** Chevrolet
- **Modelo:** Onix
- **Diâmetro:** 15''
- **Acabamento/Cor:** Prata
- **Material:** Ferro
- **Garantia:** 3 meses
- **SKU:** SKU456

[Dúvidas frequentes...]

**INFORMAÇÕES IMPORTANTES:**
- **MERCADO ENVIO TRANSPORTA APENAS 1 KIT (4 RODAS) POR PEDIDO.**
[Restante do texto...]
Arquivo Consolidado de Aprovação
No diretório raiz, será gerado um arquivo aprovacao.txt com o seguinte formato:```

# Exemplo de aprovacao.txt

------------------------
```plaintext
*Calota Aro 14 GRID Fiat Palio*

Quantidade: 10
Acabamento: Cromado
SKU: SKU123
*Concorrência: Modelo X*
*Preço OLX / Facebook: R$ 100*
*Preço Mercado Livre: R$ 120*

---------------

------------------------

*Honda City 15''*

Quantidade: 5
Acabamento: Polido
SKU: SKU456
*Concorrência: Modelo Y*
*Preço OLX / Facebook: R$ 150*
*Preço Mercado Livre: R$ 170*
```

---------------

### Observações Importantes

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

Suporte
Se precisar de ajuda ou quiser sugerir melhorias, entre em contato com o desenvolvedor ou abra uma issue no repositório do projeto.

Esse README reflete as mudanças e melhorias implementadas na nova versão do projeto. 😊