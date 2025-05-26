import mysql.connector
from faker import Faker
import random
import argparse
import csv

# Argumentos CLI
parser = argparse.ArgumentParser(description="Gerar registros de funcionários e exportar para CSV/HTML.")
parser.add_argument("--host", default="localhost", help="Servidor MySQL")
parser.add_argument("--user", required=True, help="Usuário MySQL")
parser.add_argument("--password", required=True, help="Senha MySQL")
parser.add_argument("--database", required=True, help="Nome do banco de dados")
parser.add_argument("--quantidade", type=int, default=100, help="Número de registros")
parser.add_argument("--csv", help="Arquivo CSV para exportação (opcional)")
parser.add_argument("--html", help="Arquivo HTML para exportação (opcional)")
args = parser.parse_args()

# Conexão MySQL
conn = mysql.connector.connect(
    host=args.host,
    user=args.user,
    password=args.password
)
cursor = conn.cursor()

# Criar banco de dados e usar
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {args.database}")
cursor.execute(f"USE {args.database}")

# Criar tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    cargo VARCHAR(50),
    departamento VARCHAR(50),
    salario DECIMAL(10, 2),
    data_admissao DATE,
    telefone VARCHAR(20),
    cidade VARCHAR(50),
    senioridade VARCHAR(20)
);
""")

# Dados fictícios
fake = Faker("pt_BR")
cargos = ["Desenvolvedor", "Analista de Sistemas", "Tech Lead", "Scrum Master", "DBA", "DevOps", "QA Engineer"]
departamentos = ["Engenharia", "Suporte", "RH", "Financeiro", "TI Interno"]
senioridades = ["Estagiário", "Júnior", "Pleno", "Sênior"]

dados = []

# Gerar e inserir registros
for _ in range(args.quantidade):
    nome = fake.name()
    email = fake.email()
    cargo = random.choice(cargos)
    departamento = random.choice(departamentos)
    salario = round(random.uniform(2500.00, 18000.00), 2)
    data_admissao = fake.date_between(start_date='-10y', end_date='today')
    telefone = fake.phone_number()
    cidade = fake.city()
    senioridade = random.choice(senioridades)

    cursor.execute("""
        INSERT INTO funcionarios (nome, email, cargo, departamento, salario, data_admissao, telefone, cidade, senioridade)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (nome, email, cargo, departamento, salario, data_admissao, telefone, cidade, senioridade))

    dados.append([
        nome, email, cargo, departamento, salario,
        data_admissao.strftime("%Y-%m-%d"), telefone, cidade, senioridade
    ])

conn.commit()
cursor.close()
conn.close()
print(f"✅ Inseridos {args.quantidade} registros em '{args.database}'.")

# Exportar para CSV
if args.csv:
    with open(args.csv, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nome", "email", "cargo", "departamento", "salario", "data_admissao", "telefone", "cidade", "senioridade"])
        writer.writerows(dados)
    print(f"📁 Dados exportados para CSV: {args.csv}")

# Exportar para HTML com DataTables (paginação, ordenação e busca)
if args.html:
    with open(args.html, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Funcionários da Empresa</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- DataTables CSS -->
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css">

    <style>
        body {
            padding: 2rem;
            background-color: #f8f9fa;
            font-family: 'Segoe UI', sans-serif;
        }
        h2 {
            text-align: center;
            margin-bottom: 2rem;
        }
    </style>
</head>
<body>
    <h2>Funcionários da Empresa</h2>
    <div class="table-responsive">
        <table id="funcionarios" class="table table-striped table-bordered align-middle">
            <thead class="table-dark">
                <tr>
                    <th>Nome</th>
                    <th>Email</th>
                    <th>Cargo</th>
                    <th>Departamento</th>
                    <th>Salário</th>
                    <th>Admissão</th>
                    <th>Telefone</th>
                    <th>Cidade</th>
                    <th>Senioridade</th>
                </tr>
            </thead>
            <tbody>
""")
        for row in dados:
            f.write("                <tr>\n")
            for col in row:
                f.write(f"                    <td>{col}</td>\n")
            f.write("                </tr>\n")

        f.write("""            </tbody>
        </table>
    </div>

    <!-- jQuery + DataTables + Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js"></script>

    <!-- Inicialização do DataTable -->
    <script>
        $(document).ready(function() {
            $('#funcionarios').DataTable({
                "language": {
                    "url": "//cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json"
                },
                "pageLength": 10,
                "lengthMenu": [10, 25, 50, 100]
            });
        });
    </script>
</body>
</html>
""")

    print(f"🌐 Tabela HTML com paginação e busca gerada: {args.html}")
