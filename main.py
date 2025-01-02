import json
from flask import Flask, render_template, request, redirect, url_for

# Tabela de produtos e preços
produtos = {
    "Tartelette Bacalhau": 2.45,
    "Tartelette Figo": 2.45,
    "Tartelette Frango": 1.15,
    "Quiche Alho Poro": 1.35,
    "Quiche Marguerita": 1.35,
    "Quiche Carne de Panela": 1.35,
    "Canape Pera": 2.45,
    "Canape Camarão": 2.45,
    "Canape Salame": 2.45,
    "Bolinha Carne de Panela": 2.15,
    "Bolinha Bacalhau": 2.45,
    "Kibe": 1.35,
    "Caprese": 2.15,
    "Prensadinho": 2.15,
    "Panquequinha": 2.45,
    "Empanada": 1.35,
    "Palito Folhado": 2.15,
    "Doguinho": 2.15,
    "Torta Fria": 98.00,
    "Cheesecake Frutas Vermelhas": 98.00,
    "Cheesecake Frutas Maracuja": 98.00,
    "Cheesecake Frutas Goiaba": 98.00
}

# Pasta com clientes
ARQUIVO_CLIENTES = "clientes.json"

# Carrega os dados dos clientes do JSON
def carregar_clientes():
    try:
        with open(ARQUIVO_CLIENTES, "r") as file:
            data = file.read().strip()
            if not data:
                return {}
            return json.loads(data)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Arquivo JSON corrompido. Criando um novo arquivo.")
        return {}

# Salva os dados dos clientes no JSON
def salvar_clientes():
    with open(ARQUIVO_CLIENTES, "w") as file:
        json.dump(clientes, file, indent=4)

# Dict que armazena as infos dos clientes
clientes = carregar_clientes()

app = Flask(__name__)

@app.route('/')
def index():
    clientes_com_pedidos = []
    total_geral = 0
    quantidade_total_produtos = {produto: 0 for produto in produtos.keys()}

    # Preparando os dados para o HTML
    for nome, info in clientes.items():
        if 'total_venda' not in info:
            info['total_venda'] = 0

        # Calcula o total do pedido do cliente
        if info['pedido']:
            info['total_venda'] = sum(produtos.get(produto, 0) * quantidade for produto, quantidade in info['pedido'].items())

            # Soma as quantidades de produtos no total geral
            for produto, quantidade in info['pedido'].items():
                quantidade_total_produtos[produto] += quantidade

        total_geral += info['total_venda']

        # Adiciona informações do cliente para renderizar no template
        clientes_com_pedidos.append({
            'nome': nome,
            'telefone': info['telefone'],
            'local_entrega': info['local_entrega'],
            'data_entrega': info['data_entrega'],
            'hora_entrega': info['hora_entrega'],
            'pedido': info['pedido'],
            'total_venda': info['total_venda']
        })

    # Renderiza o HTML
    return render_template(
        'index.html',
        clientes=clientes_com_pedidos,
        produtos=produtos,
        total_geral=total_geral,
        quantidade_total_produtos=quantidade_total_produtos
    )

@app.route('/cadastrar_cliente', methods=['POST'])
def cadastrar_cliente():
    nome = request.form['nome']
    telefone = request.form['telefone']
    local_entrega = request.form['local_entrega']
    data_entrega = request.form['data_entrega']
    hora_entrega = request.form['hora_entrega']

    if not nome or not telefone or not local_entrega or not data_entrega or not hora_entrega:
        return "Todos os campos são obrigatórios!", 400

    clientes[nome] = {
        "telefone": telefone,
        "local_entrega": local_entrega,
        "data_entrega": data_entrega,
        "hora_entrega": hora_entrega,
        "pedido": {},
        "total_venda": 0
    }

    salvar_clientes()
    return redirect(url_for('index'))

@app.route('/cadastrar_pedido', methods=['POST'])
def cadastrar_pedido():
    nome_cliente = request.form['nome_cliente']
    if nome_cliente not in clientes:
        return "Cliente não encontrado!", 404

    produto = request.form['produto']
    quantidade = int(request.form['quantidade'])

    if produto not in produtos:
        return "Produto inválido!", 400

    # Atualiza o pedido do cliente
    if produto in clientes[nome_cliente]["pedido"]:
        clientes[nome_cliente]["pedido"][produto] += quantidade
    else:
        clientes[nome_cliente]["pedido"][produto] = quantidade

    # Recalcula o total_venda
    clientes[nome_cliente]["total_venda"] = sum(
        produtos.get(produto, 0) * quantidade for produto, quantidade in clientes[nome_cliente]["pedido"].items()
    )

    salvar_clientes()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
