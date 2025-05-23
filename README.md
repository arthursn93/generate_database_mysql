# Gerador de Dados de Funcionários com MySQL

Este projeto em Python tem como objetivo **gerar registros fictícios de funcionários** de uma empresa de TI, inserir esses dados em uma tabela MySQL e exportar os resultados para arquivos CSV e HTML, conforme desejado.

---

## 📌 Funcionalidades

- Geração de dados realistas de funcionários usando `Faker` (nome, email, cargo, salário, etc.)
- Criação automática da tabela `funcionarios` no MySQL
- Inserção de dados diretamente no banco de dados
- Exportação dos dados para:
  - Arquivo `.csv`
  - Página `.html` com tabela

---

## 🧪 Requisitos

- Python 3.8+
- Banco de dados MySQL
- Dependências Python:
  - `mysql-connector-python`
  - `faker`

Instale com:

```bash
pip install mysql-connector-python faker


▶️ Como usar
No Modify Run Configuration do código gerar_funcionario.py, execute o script com os parâmetros desejados:

```bash
--host localhost --user seu_usuario --password sua_senha --database seu_database --quantidade 100 --csv funcionarios.csv --html funcionarios.html
