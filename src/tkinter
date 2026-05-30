import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

# Imports das funções CRUD
from barbearia import criar_barbearia, listar_barbearias, consultar_barbearia, atualizar_barbearia, remover_barbearia
from barbeiro import criar_barbeiro, listar_barbeiros, consultar_barbeiro, atualizar_barbeiro, remover_barbeiro
from cliente import criar_cliente, listar_clientes, consultar_cliente, atualizar_cliente, remover_cliente
from agendamento import criar_agendamento, listar_agendamentos, consultar_agendamento, atualizar_status, eliminar_agendamento
from produto import adicionar_produto, listar_produtos, consultar_produto, atualizar_produto, remover_produto


class GestorBarbeariaGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestor de Barbearia - Sistema Profissional")
        self.root.geometry("1350x750")
        self.root.state('zoomed')  # Maximizar janela
        
        self.criar_estilo()
        self.criar_interface()

    def criar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

    def criar_interface(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.criar_aba_barbearias(notebook)
        self.criar_aba_barbeiros(notebook)
        self.criar_aba_clientes(notebook)
        self.criar_aba_agendamentos(notebook)
        self.criar_aba_produtos(notebook)

        # Status bar
        self.status_bar = tk.Label(self.root, text="Sistema pronto. Selecione uma aba.", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#f0f0f0")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def atualizar_status(self, msg):
        self.status_bar.config(text=msg)

    # ====================== BARBEARIAS ======================
    def criar_aba_barbearias(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=" Barbearias")

        self.tree_barbearias = self.criar_treeview(frame, ["ID", "Nome", "Morada", "NIF"])
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text=" Atualizar", command=self.atualizar_lista_barbearias).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Nova Barbearia", command=self.janela_criar_barbearia).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Editar", command=self.editar_barbearia).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Remover", command=self.remover_barbearia).pack(side=tk.LEFT, padx=4)

        self.atualizar_lista_barbearias()

    def atualizar_lista_barbearias(self):
        for item in self.tree_barbearias.get_children():
            self.tree_barbearias.delete(item)
        code, data = listar_barbearias()
        if code == 200:
            for iid, info in data.items():
                self.tree_barbearias.insert("", "end", values=(iid, info.get("nome",""), info.get("morada",""), info.get("nif","")))

    def janela_criar_barbearia(self):
        self.janela_formulario("Nova Barbearia", [
            ("Nome", ""), ("Morada", ""), ("NIF", "")
        ], lambda d: criar_barbearia(d[0], d[1], d[2]), self.atualizar_lista_barbearias)

    def editar_barbearia(self):
        selected = self.tree_barbearias.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma barbearia")
            return
        iid = self.tree_barbearias.item(selected[0])['values'][0]
        self.atualizar_status(f"Editando barbearia {iid}")

    def remover_barbearia(self):
        selected = self.tree_barbearias.selection()
        if not selected: return
        iid = self.tree_barbearias.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Remover barbearia {iid}?"):
            code, msg = remover_barbearia(iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Barbearia removida!")
                self.atualizar_lista_barbearias()
            else:
                messagebox.showerror("Erro", msg)

    # ====================== BARBEIROS ======================
    def criar_aba_barbeiros(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=" Barbeiros")
        self.tree_barbeiros = self.criar_treeview(frame, ["ID", "Nome", "Especialidade", "Telefone", "Barbearia"])
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text=" Atualizar", command=self.atualizar_lista_barbeiros).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Novo Barbeiro", command=self.janela_criar_barbeiro).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Editar", command=lambda: messagebox.showinfo("Info", "Editar barbeiro em desenvolvimento")).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Remover", command=self.remover_barbeiro).pack(side=tk.LEFT, padx=4)
        self.atualizar_lista_barbeiros()

    def atualizar_lista_barbeiros(self):
        for item in self.tree_barbeiros.get_children():
            self.tree_barbeiros.delete(item)
        code, data = listar_barbeiros()
        if code == 200:
            for iid, info in data.items():
                self.tree_barbeiros.insert("", "end", values=(
                    iid, info.get("nome",""), info.get("especialidade",""), 
                    info.get("telefone",""), info.get("id_barbearia","")
                ))

    def janela_criar_barbeiro(self):
        self.janela_formulario("Novo Barbeiro", [
            ("Nome", ""), ("Especialidade", ""), ("Telefone", ""), 
            ("NIF", ""), ("IBAN", ""), ("Morada", ""), ("Email", ""), ("ID Barbearia", "")
        ], lambda d: criar_barbeiro(*d), self.atualizar_lista_barbeiros)

    def remover_barbeiro(self):
        selected = self.tree_barbeiros.selection()
        if not selected: return
        iid = self.tree_barbeiros.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Remover barbeiro {iid}?"):
            code, msg = remover_barbeiro(iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Barbeiro removido!")
                self.atualizar_lista_barbeiros()

    # ====================== CLIENTES ======================
    def criar_aba_clientes(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=" Clientes")
        self.tree_clientes = self.criar_treeview(frame, ["ID", "Nome", "Telefone", "Email", "Barbearia"])
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text=" Atualizar", command=self.atualizar_lista_clientes).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Novo Cliente", command=self.janela_criar_cliente).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Remover", command=self.remover_cliente).pack(side=tk.LEFT, padx=4)
        self.atualizar_lista_clientes()

    def atualizar_lista_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        code, data = listar_clientes()
        if code == 200:
            for iid, info in data.items():
                self.tree_clientes.insert("", "end", values=(
                    iid, info.get("nome",""), info.get("telefone",""), 
                    info.get("email",""), info.get("id_barbearia","")
                ))

    def janela_criar_cliente(self):
        self.janela_formulario("Novo Cliente", [
            ("ID Barbearia", ""), ("Nome", ""), ("Telefone", ""), 
            ("NIF", ""), ("IBAN", ""), ("Morada", ""), ("Email", "")
        ], lambda d: criar_cliente(*d), self.atualizar_lista_clientes)

    def remover_cliente(self):
        selected = self.tree_clientes.selection()
        if not selected: return
        iid = self.tree_clientes.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Remover cliente {iid}?"):
            code, msg = remover_cliente(iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Cliente removido!")
                self.atualizar_lista_clientes()

    # ====================== AGENDAMENTOS ======================
    def criar_aba_agendamentos(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=" Agendamentos")
        self.tree_agendamentos = self.criar_treeview(frame, ["ID", "Data/Hora", "Cliente", "Barbeiro", "Serviço", "Status"])
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text=" Atualizar", command=self.atualizar_lista_agendamentos).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Novo Agendamento", command=self.janela_criar_agendamento).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Mudar Status", command=self.mudar_status_agendamento).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Eliminar", command=self.eliminar_agendamento).pack(side=tk.LEFT, padx=4)
        self.atualizar_lista_agendamentos()

    def atualizar_lista_agendamentos(self):
        for item in self.tree_agendamentos.get_children():
            self.tree_agendamentos.delete(item)
        code, data = listar_agendamentos()
        if code == 200:
            for iid, info in data.items():
                self.tree_agendamentos.insert("", "end", values=(
                    iid, info.get("data_hora",""), info.get("cliente",""), 
                    info.get("barbeiro",""), info.get("servico",""), info.get("status","")
                ))

    def janela_criar_agendamento(self):
        win = tk.Toplevel(self.root)
        win.title("Novo Agendamento")
        win.geometry("500x400")

        ttk.Label(win, text="Data e Hora (YYYY-MM-DD HH:MM):").pack(pady=5)
        data_hora = ttk.Entry(win, width=40)
        data_hora.pack()

        ttk.Label(win, text="ID Cliente:").pack(pady=5)
        id_cliente = ttk.Entry(win, width=40)
        id_cliente.pack()

        ttk.Label(win, text="ID Barbeiro:").pack(pady=5)
        id_barbeiro = ttk.Entry(win, width=40)
        id_barbeiro.pack()

        ttk.Label(win, text="Serviço:").pack(pady=5)
        servico = ttk.Entry(win, width=40)
        servico.pack()

        ttk.Label(win, text="ID Barbearia:").pack(pady=5)
        id_barbearia = ttk.Entry(win, width=40)
        id_barbearia.pack()

        def salvar():
            code, result = criar_agendamento(
                data_hora.get(), id_cliente.get(), id_barbeiro.get(),
                servico.get(), id_barbearia.get()
            )
            if code in (200, 201):
                messagebox.showinfo("Sucesso", "Agendamento criado!")
                self.atualizar_lista_agendamentos()
                win.destroy()
            else:
                messagebox.showerror("Erro", str(result))

        ttk.Button(win, text="Guardar Agendamento", command=salvar).pack(pady=20)

    def mudar_status_agendamento(self):
        selected = self.tree_agendamentos.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um agendamento")
            return
        iid = self.tree_agendamentos.item(selected[0])['values'][0]
        novo_status = tk.simpledialog.askstring("Status", "Novo status:", initialvalue="Confirmado")
        if novo_status:
            code, _ = atualizar_status(iid, novo_status)
            if code == 200:
                messagebox.showinfo("Sucesso", "Status atualizado!")
                self.atualizar_lista_agendamentos()

    def eliminar_agendamento(self):
        selected = self.tree_agendamentos.selection()
        if not selected: return
        iid = self.tree_agendamentos.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Eliminar agendamento {iid}?"):
            code, _ = eliminar_agendamento(iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Agendamento eliminado!")
                self.atualizar_lista_agendamentos()

    # ====================== PRODUTOS ======================
    def criar_aba_produtos(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Produtos")
        self.tree_produtos = self.criar_treeview(frame, ["ID", "Nome", "Preço", "Stock", "Barbearia"])
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text=" Atualizar", command=self.atualizar_lista_produtos).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Novo Produto", command=self.janela_criar_produto).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Remover", command=self.remover_produto).pack(side=tk.LEFT, padx=4)
        self.atualizar_lista_produtos()

    def atualizar_lista_produtos(self):
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        code, data = listar_produtos()
        if code == 200:
            for iid, info in data.items():
                self.tree_produtos.insert("", "end", values=(
                    iid, info.get("nome",""), info.get("preco_venda",""), 
                    info.get("quantidade_stock",""), info.get("id_barbearia","")
                ))

    def janela_criar_produto(self):
        self.janela_formulario("Novo Produto", [
            ("Nome", ""), ("Preço", ""), ("Quantidade", ""), ("ID Barbearia", "")
        ], lambda d: adicionar_produto(d[0], d[1], d[2], d[3]), self.atualizar_lista_produtos)

    def remover_produto(self):
        selected = self.tree_produtos.selection()
        if not selected: return
        iid = self.tree_produtos.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Remover produto {iid}?"):
            code, msg = remover_produto(iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Produto removido!")
                self.atualizar_lista_produtos()

    # ====================== UTILITÁRIOS ======================
    def criar_treeview(self, parent, colunas):
        tree = ttk.Treeview(parent, columns=colunas, show="headings", height=20)
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill="both", expand=True, padx=10, pady=5)
        return tree

    def janela_formulario(self, titulo, campos, funcao_criar, funcao_atualizar):
        win = tk.Toplevel(self.root)
        win.title(titulo)
        win.geometry("500x500")
        entries = []

        for i, (label_text, default) in enumerate(campos):
            ttk.Label(win, text=label_text + ":").pack(pady=5, anchor="w", padx=20)
            entry = ttk.Entry(win, width=50)
            entry.insert(0, default)
            entry.pack(pady=2, padx=20)
            entries.append(entry)

        def salvar():
            valores = [e.get().strip() for e in entries]
            code, result = funcao_criar(valores)
            if code in (200, 201):
                messagebox.showinfo("Sucesso", f"{titulo} criado com sucesso!")
                funcao_atualizar()
                win.destroy()
            else:
                messagebox.showerror("Erro", str(result))

        ttk.Button(win, text=" Guardar", command=salvar).pack(pady=20)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GestorBarbeariaGUI()
    app.run()
