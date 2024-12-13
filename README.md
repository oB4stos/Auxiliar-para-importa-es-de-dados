# Auxiliar de Importações de Planilhas

## Descrição
Este programa foi criado para facilitar a rotina de manipulação de dados para a inserção em planilhas da empresa. Ele oferece funcionalidades úteis, como busca de informações com base no CEP, formatação de documentos e padronização de texto. Possui uma interface gráfica amigável e permite a geração de um executável para facilitar o uso.

## Funcionalidades
- **Busca de Dados pelo CEP:** Preenche automaticamente cidade e UF com base no CEP informado.
- **Formatação de CPF/CNPJ:** Ajusta os números para o formato correto.
- **Transformação de Texto:** Converte qualquer texto para maiúsculas.

## Instruções de Uso
Para alteração ou uso próprio do algoritmo:
1. **Baixe ou clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/auxiliar-importacao-planilhas.git
   ```
2. **Certifique-se de que o Python está instalado no seu computador.**
3. **Instale as dependências necessárias:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Execute o programa:**
   ```bash
   python app.py
   ```
5. **Utilize o programa para o auxílio no ajuste e busca de certos dados.**

## Geração de Executável
Caso prefira usar o programa como executável:
1. Certifique-se de que o [PyInstaller](https://pyinstaller.org/en/stable/) está instalado:
   ```bash
   pip install pyinstaller
   ```
2. Gere o executável com o comando:
   ```bash
   pyinstaller --onefile app.py
   ```
3. O executável estará disponível na pasta `dist`.

## Observações
- Em breve, o arquivo executável do programa será disponibilizado.
- Este projeto está em desenvolvimento e pode receber novas funcionalidades no futuro.
- Caso encontre problemas ou tenha sugestões, fique à vontade para contribuir!
