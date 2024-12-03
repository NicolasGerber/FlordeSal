import tkinter as tk
from tkinter import messagebox
import json
from produtos import produtos

# PASTA COM CLIENTES
ARQUIVO_CLIENTES = "clientes.json"


# CARREGA OS DADOS DOS CLIENTES DO JSON
def carregar_clientes():
    try:
        with open(ARQUIVO_CLIENTES, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# SALVA OS DADOS DOS CLIENTES NO JSON
def salvar_clientes():
    with open(ARQUIVO_CLIENTES, "w") as file:
        json.dump(clientes, file, indent=4)


# DICT QUE ARMAZENA AS  INFOS DOS CLIENTES
clientes = carregar_clientes()


def cadastrar_cliente():
    nome = entry_nome.get()
    telefone = entry_telefone.get()
    local_entrega = entry_local_entrega.get()
    data_entrega = entry_data_entrega.get()
    hora_entrega = entry_hora_entrega.get()

    if not nome or not telefone or not local_entrega or not data_entrega or not hora_entrega:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
        return

    clientes[nome] = {
        "telefone": telefone,
        "local_entrega": local_entrega,
        "data_entrega": data_entrega,
        "hora_entrega": hora_entrega,
        "pedido": {}
    }

    #SALVA CLIENTE NO JSON
    salvar_clientes()

    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")


def cadastrar_pedido():
    nome_cliente = entry_cliente_pedido.get()

    if nome_cliente not in clientes:
        messagebox.showerror("Erro", "Cliente não encontrado!")
        return

    janela_pedido = tk.Toplevel(root)  # <--- CRIA UMA JANELA SECUNDARIA
    janela_pedido.title(f"Pedido para {nome_cliente}")

    quantidade_total = 0

    #MOSTRA OS PRODUTOS DISPONIVEIS
    produto_var = tk.StringVar()
    produto_menu = tk.OptionMenu(janela_pedido, produto_var, *produtos.keys())
    produto_menu.pack()

    quantidade_var = tk.IntVar()
    quantidade_entry = tk.Entry(janela_pedido, textvariable=quantidade_var)
    quantidade_entry.pack()

    lista_pedido = tk.Listbox(janela_pedido)
    lista_pedido.pack()

    def adicionar_produto():
        nonlocal quantidade_total

        produto_selecionado = produto_var.get()
        quantidade = quantidade_var.get()

        if produto_selecionado and quantidade > 0:

            if produto_selecionado in clientes[nome_cliente]["pedido"]:
                clientes[nome_cliente]["pedido"][produto_selecionado] += quantidade
            else:
                clientes[nome_cliente]["pedido"][produto_selecionado] = quantidade


            lista_pedido.insert(tk.END, f"{quantidade} X {produto_selecionado}")

            quantidade_total += quantidade

            label_contador.config(text=f"Quantidade total de itens: {quantidade_total}")

            #SALVA OS  DADOS NO JSON
            salvar_clientes()
        else:
            messagebox.showerror("Erro", "Selecione um produto e insira uma quantidade válida!")

    adicionar_prod = tk.Button(janela_pedido, text="Adicionar ao Pedido", command=adicionar_produto)
    adicionar_prod.pack()


    def calcular_total():
        total = sum(clientes[nome_cliente]["pedido"].values())
        label_total.config(text=f"Total a pagar: R${total * produtos[produto_var.get()]:.2f}")

    button_calcular = tk.Button(janela_pedido, text="Calcular Total", command=calcular_total)
    button_calcular.pack()

    label_total = tk.Label(janela_pedido, text="Total a pagar: R$0.00")
    label_total.pack()

    label_contador = tk.Label(janela_pedido, text="Quantidade total de itens: 0")
    label_contador.pack()

    def fechar_janela():
        janela_pedido.destroy()

    fechar_btn = tk.Button(janela_pedido, text="Fechar", command=fechar_janela)
    fechar_btn.pack()

def visualizar_clientes():

    clientes_info = ""
    for nome, info in clientes.items():
        clientes_info += f"\n{nome}: {info['telefone']}, {info['local_entrega']}, {info['data_entrega']} {info['hora_entrega']}"

        if info['pedido']:
            pedidos_info = "\n  Pedidos:"
            total_pedido = 0
            for produto, quantidade in info['pedido'].items():
                pedidos_info += f"\n    {quantidade} und {produto} - R${produtos[produto] * quantidade:.2f}"
                total_pedido += produtos[produto] * quantidade


            pedidos_info += f"\n  Total do Pedido: R${total_pedido:.2f}"
            clientes_info += pedidos_info
        else:
            clientes_info += "\n  Nenhum pedido registrado."

    if clientes_info:
        messagebox.showinfo("Clientes e Pedidos", clientes_info)
    else:
        messagebox.showinfo("Clientes e Pedidos", "Nenhum cliente cadastrado!")


#JANELA ROOT
root = tk.Tk()
root.title("Cadastro de Clientes e Pedidos de Salgados")

#TELAS DE CADASTRO
label_nome = tk.Label(root, text="Nome:")
label_nome.grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

label_telefone = tk.Label(root, text="Telefone:")
label_telefone.grid(row=1, column=0)
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=1, column=1)

label_local_entrega = tk.Label(root, text="Local de Entrega:")
label_local_entrega.grid(row=2, column=0)
entry_local_entrega = tk.Entry(root)
entry_local_entrega.grid(row=2, column=1)

label_data_entrega = tk.Label(root, text="Data de Entrega (DD/MM/AAAA):")
label_data_entrega.grid(row=3, column=0)
entry_data_entrega = tk.Entry(root)
entry_data_entrega.grid(row=3, column=1)

label_hora_entrega = tk.Label(root, text="Hora de Entrega (HH:MM):")
label_hora_entrega.grid(row=4, column=0)
entry_hora_entrega = tk.Entry(root)
entry_hora_entrega.grid(row=4, column=1)

btn_cadastrar_cliente = tk.Button(root, text="Cadastrar Cliente", command=cadastrar_cliente)
btn_cadastrar_cliente.grid(row=5, column=0, columnspan=2)

#JANELA DE  PEDIDOS
label_cliente_pedido = tk.Label(root, text="Nome do Cliente (para pedido):")
label_cliente_pedido.grid(row=6, column=0)
entry_cliente_pedido = tk.Entry(root)
entry_cliente_pedido.grid(row=6, column=1)

btn_pedido = tk.Button(root, text="Cadastrar Pedido", command=cadastrar_pedido)
btn_pedido.grid(row=7, column=0, columnspan=2)

#JANELA DE VISUALIZAÇÃO
btn_visualizar_clientes = tk.Button(root, text="Ver Clientes e Pedidos", command=visualizar_clientes)
btn_visualizar_clientes.grid(row=8, column=0, columnspan=2)

root.mainloop()
