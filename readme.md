<p align="center">
  <img src="logo_guidom.png" alt="Guidom Logo" width="200"/>
</p>

<img src="https://i.imgur.com/waxVImv.png" width="100%"/>

### 📌 **Descrição**

O script foi criado para automatizar a organização de pastas relacionadas a calotas/rodas automotivas. Ele foi desenvolvido para facilitar a criação de diretórios com nomes padronizados, baseados em uma lista predefinida de modelos de veículos.

Com este script, você pode criar pastas numeradas e formatadas automaticamente, garantindo uma estrutura organizada e fácil de navegar.

<img src="https://i.imgur.com/waxVImv.png" width="100%"/>

### 🔧 **Problema Resolvido**

A principal necessidade atendida é a organização sistemática de dados relacionados a calotas automotivas. Ao trabalhar com uma grande quantidade de modelos de veículos, manter uma estrutura de pastas consistente pode ser desafiador. Este script resolve esse problema ao:

- Criar pastas numeradas sequencialmente (`01_nome`, `02_nome`, etc.).
- Substituir espaços por underscores (`_`) para nomes válidos no sistema de arquivos.
- Remover caracteres inválidos que podem causar erros no Windows.
- Garantir que cada pasta tenha um nome único, mesmo que haja duplicatas na lista original.

<img src="https://i.imgur.com/waxVImv.png" width="100%"/>

### 🚀 **Funcionalidades**

- **Criação Automática de Pastas**: Gera diretórios com nomes padronizados com base em uma lista fornecida.
- **Contador Sequencial**: Adiciona um número de ordem (`01_`, `02_`, etc.) antes de cada nome.
- **Formatação de Nomes**: Substitui espaços por underscores (`_`) e remove caracteres inválidos.
- **Diretório Raiz Configurável**: Permite definir o caminho onde as pastas serão criadas.
- **Verificação de Existência**: Evita a criação de pastas duplicadas.

<img src="https://i.imgur.com/waxVImv.png" width="100%"/>

### 🛠️ **Requisitos**

Para usar o **Calota Organizer**, você precisa ter os seguintes requisitos instalados:

- **Python 3.x**: O script foi desenvolvido para funcionar com Python 3. Certifique-se de que o Python está instalado no seu sistema.
- **Bibliotecas Necessárias**: Este script usa `pandas` para ler planilhas. Instale-o com:
  ```bash
  pip install pandas openpyxl
  ```

<img src="https://i.imgur.com/waxVImv.png" width="100%"/>

### 📝 **Como Usar**

1. **Clone ou Baixe o Projeto**:
   - Clone este repositório usando o comando:
     ```bash
     git clone https://github.com/seu-usuario/guidon_wheels.git
     ```
   - Ou baixe o código-fonte diretamente como um arquivo ZIP.

2. **Prepare Sua Planilha**:
   - Crie uma planilha no formato `.csv` ou `.xlsx` com uma coluna chamada `"Nomes"` contendo os nomes dos modelos de veículos.

3. **Configurar o Script**:
   - Abra o arquivo `script.py` e altere as variáveis `planilha_path` e `pasta_raiz` para os caminhos corretos. Por exemplo:
     ```python
     planilha_path = r"C:\caminho\para\sua_planilha.csv"
     pasta_raiz = r"C:\Users\Guido\Desktop\calotas\12_mar_25"
     ```

4. **Executar o Script**:
   - No terminal, navegue até o diretório do projeto e execute o script:
     ```bash
     python script.py
     ```

5. **Resultado**:
   - As pastas serão criadas no caminho especificado, com nomes no formato `01_Nissan_Kicks_16`, `02_Nissan_March_14`, etc.

<img src="https://i.imgur.com/waxVImv.png" width="100%"/>

### 📂 **Exemplo de Estrutura de Pastas**

Após a execução do script, a estrutura de pastas será semelhante a esta:

```
C:\Users\Guido\Desktop\calotas\12_mar_25\
    ├── 01_Nissan_Kicks_16
    ├── 02_Nissan_March_14
    ├── 03_Nissan_Tiida_Versa_15
    ├── 04_Toyota_Corolla_16
    ├── 05_Hyundai_HB20_14
    └── ...
```

<img src="https://i.imgur.com/waxVImv.png" width="100%"/>

### 🤝 **Contribuições**

Este é um projeto em desenvolvimento, e contribuições são bem-vindas! Se você deseja melhorar o script ou adicionar novas funcionalidades, fique à vontade para abrir uma issue ou enviar um pull request.

<img src="https://i.imgur.com/waxVImv.png" width="100%"/>

### 📄 **Licença**

Este projeto está licenciado sob a [MIT License](LICENSE). Você pode usá-lo, modificá-lo e distribuí-lo conforme necessário.

<img src="https://i.imgur.com/waxVImv.png" width="100%"/>

### 🌐 **Contato**

Se tiver dúvidas, sugestões ou quiser entrar em contato, sinta-se à vontade para me procurar:

<p align="center">
  <a href="https://linkedin.com/in/seu-perfil">
    <img src="https://skillicons.dev/icons?i=linkedin" alt="LinkedIn"/>
  </a>
  <a href="https://github.com/seu-usuario">
    <img src="https://skillicons.dev/icons?i=github" alt="GitHub"/>
  </a>
  <a href="mailto:seu-email@example.com">
    <img src="https://skillicons.dev/icons?i=gmail" alt="Gmail"/>
  </a>
</p>
