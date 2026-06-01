import tkinter as tk
from tkinter import ttk, messagebox

# Importações das lógicas modulares
from barbearia import criar_barbearia, listar_barbearias, atualizar_barbearia, remover_barbearia
from barbeiro import criar_barbeiro, listar_barbeiros, atualizar_barbeiro, remover_barbeiro
from cliente import criar_cliente, listar_clientes, atualizar_cliente, remover_cliente
from agendamento import (
    criar_agendamento, listar_agendamentos,
    atualizar_status as agendamento_atualizar_status,
    eliminar_agendamento as agendamento_eliminar
)
from produto import adicionar_produto, listar_produtos, remover_produto

class GestorBarbeariaGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestor de Barbearia - Sistema Profissional")
        self.root.geometry("1350x750")
        try:
            self.root.state('zoomed')
        except tk.TclError:
            self.root.attributes('-zoomed', True)

        self._criar_estilo()
        self._criar_interface()

    def _criar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

    def _criar_interface(self):
        self.status_bar = tk.Label(
            self.root, text="Sistema pronto. Selecione uma aba.",
            bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#f0f0f0"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._criar_aba_barbearias(notebook)
        self._criar_aba_barbeiros(notebook)
        self._criar_aba_clientes(notebook)
        self._criar_aba_agendamentos(notebook)
        self._criar_aba_produtos(notebook)

    def _criar_treeview(self, parent, colunas):
        container = ttk.Frame(parent)
        scroll_y = ttk.Scrollbar(container, orient="vertical")
        scroll_x = ttk.Scrollbar(container, orient="horizontal")

        tree = ttk.Treeview(
            container, columns=colunas, show="headings", height=20,
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )

        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(fill="both", expand=True)

        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=120, minwidth=70)

        return container, tree

    def _janela_formulario(self, titulo, campos, funcao_mapeada, funcao_atualizar):
        """
        Janela genérica para formulários.
        funcao_mapeada: recebe uma lista de strings capturadas na interface e trata os argumentos.
        """
        win = tk.Toplevel(self.root)
        win.title(titulo)
        win.geometry("500x550")
        win.grab_set()

        canvas = tk.Canvas(win, borderwidth=0)
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas)

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        entries = []
        for label_text, default in campos:
            ttk.Label(inner, text=label_text + ":").pack(pady=(6, 0), anchor="w", padx=10)
            entry = ttk.Entry(inner, width=50)
            entry.insert(0, str(default))
            entry.pack(pady=(0, 2), padx=10, fill="x")
            entries.append(entry)

        def salvar():
            valores = [e.get().strip() for e in entries]
            code, result = funcao_mapeada(valores)
            if code in (200, 201):
                messagebox.showinfo("Sucesso", "Operação realizada com sucesso!")
                funcao_atualizar()
                win.destroy()
            else:
                messagebox.showerror("Erro", str(result))

        ttk.Button(inner, text="Guardar", command=salvar).pack(pady=20)

    # ── ABA BARBEARIAS ──
    def _criar_aba_barbearias(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Barbearias")
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Atualizar Lista", command=self._atualizar_barbearias).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Nova Barbearia", command=self._nova_barbearia).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Editar", command=self._editar_barbearia).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Remover", command=self._remover_barbearia).pack(side=tk.LEFT, padx=4)

        container, self.tree_barbearias = self._criar_treeview(frame, ["ID", "Nome", "Morada", "NIF"])
        container.pack(fill="both", expand=True, padx=10, pady=5)
        self._atualizar_barbearias()

    def _atualizar_barbearias(self):
        for item in self.tree_barbearias.get_children():
            self.tree_barbearias.delete(item)
        code, data = listar_barbearias()
        if code == 200 and isinstance(data, dict):
            for iid, info in data.items():
                self.tree_barbearias.insert("", "end", values=(iid, info.get("nome"), info.get("morada"), info.get("nif")))

    def _nova_barbearia(self):
        self._janela_formulario(
            "Nova Barbearia",
            [("Nome", ""), ("Morada", ""), ("NIF", "")],
            lambda d: criar_barbearia(d[0], d[1], d[2]),
            self._atualizar_barbearias
        )

    def _editar_barbearia(self):
        sel = self.tree_barbearias.selection()
        if not sel:
            return messagebox.showwarning("Aviso", "Selecione uma barbearia na tabela.")
        v = self.tree_barbearias.item(sel[0])['values']
        self._janela_formulario(
            "Editar Barbearia",
            [("Nome", v[1]), ("Morada", v[2]), ("NIF", v[3])],
            lambda d, iid=v[0]: atualizar_barbearia(id_barbearia=iid, nome=d[0], morada=d[1], nif=d[2]),
            self._atualizar_barbearias
        )

    def _remover_barbearia(self):
        sel = self.tree_barbearias.selection()
        if not sel:
            return messagebox.showwarning("Aviso", "Selecione uma barbearia.")
        iid = self.tree_barbearias.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Tem a certeza que deseja remover a barbearia {iid}?"):
            code, msg = remover_barbearia(iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Barbearia removida!")
                self._atualizar_barbearias()
            else:
                messagebox.showerror("Erro", str(msg))

    # ── ABA BARBEIROS ──
    def _criar_aba_barbeiros(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Barbeiros")
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Atualizar Lista", command=self._atualizar_barbeiros).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Novo Barbeiro", command=self._novo_barbeiro).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Editar", command=self._editar_barbeiro).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Remover", command=self._remover_barbeiro).pack(side=tk.LEFT, padx=4)

        container, self.tree_barbeiros = self._criar_treeview(frame, ["ID", "Nome", "Especialidade", "Telefone", "NIF", "IBAN", "Morada", "Email", "ID Barbearia"])
        container.pack(fill="both", expand=True, padx=10, pady=5)
        self._atualizar_barbeiros()

    def _atualizar_barbeiros(self):
        for item in self.tree_barbeiros.get_children():
            self.tree_barbeiros.delete(item)
        code, data = listar_barbeiros()
        if code == 200 and isinstance(data, dict):
            for iid, info in data.items():
                self.tree_barbeiros.insert("", "end", values=(
                    iid, info.get("nome"), info.get("especialidade"), info.get("telefone"),
                    info.get("nif"), info.get("iban"), info.get("morada"), info.get("email"), info.get("id_barbearia")
                ))

    def _novo_barbeiro(self):
        self._janela_formulario(
            "Novo Barbeiro",
            [("Nome", ""), ("Especialidade", ""), ("Telefone", ""), ("NIF", ""), ("IBAN", ""), ("Morada", ""), ("Email", ""), ("ID Barbearia", "")],
            lambda d: criar_barbeiro(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]),
            self._atualizar_barbeiros
        )

    def _editar_barbeiro(self):
        sel = self.tree_barbeiros.selection()
        if not sel:
            return messagebox.showwarning("Aviso", "Selecione um barbeiro.")
        v = self.tree_barbeiros.item(sel[0])['values']
        self._janela_formulario(
            "Editar Barbeiro",
            [("Nome", v[1]), ("Especialidade", v[2]), ("Telefone", v[3]), ("NIF", v[4]), ("IBAN", v[5]), ("Morada", v[6]), ("Email", v[7]), ("ID Barbearia", v[8])],
            lambda d, iid=v[0]: atualizar_barbeiro(id_barbeiro=iid, nome=d[0], especialidade=d[1], telefone=d[2], nif=d[3], iban=d[4], morada=d[5], email=d[6], id_barbearia=d[7]),
            self._atualizar_barbeiros
        )

    def _remover_barbeiro(self):
        sel = self.tree_barbeiros.selection()
        if not sel:
            return messagebox.showwarning("Aviso", "Selecione um barbeiro.")
        iid = self.tree_barbeiros.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Deseja remover o barbeiro {iid}?"):
            code, msg = remover_barbeiro(id_barbeiro=iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Barbeiro removido!")
                self._atualizar_barbeiros()
            else:
                messagebox.showerror("Erro", str(msg))

    # ── ABA CLIENTES ──
    def _criar_aba_clientes(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Clientes")
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Atualizar Lista", command=self._atualizar_clientes).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Novo Cliente", command=self._novo_cliente).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Editar", command=self._editar_cliente).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Remover", command=self._remover_cliente).pack(side=tk.LEFT, padx=4)

        container, self.tree_clientes = self._criar_treeview(frame, ["ID", "ID Barbearia", "Nome", "Telefone", "NIF", "IBAN", "Morada", "Email"])
        container.pack(fill="both", expand=True, padx=10, pady=5)
        self._atualizar_clientes()

    def _atualizar_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        code, data = listar_clientes()
        if code == 200 and isinstance(data, dict):
            for iid, info in data.items():
                self.tree_clientes.insert("", "end", values=(
                    iid, info.get("id_barbearia"), info.get("nome"), info.get("telefone"),
                    info.get("nif"), info.get("iban"), info.get("morada"), info.get("email")
                ))

    def _novo_cliente(self):
        self._janela_formulario(
            "Novo Cliente",
            [("ID Barbearia", ""), ("Nome", ""), ("Telefone", ""), ("NIF", ""), ("IBAN", ""), ("Morada", ""), ("Email", "")],
            lambda d: criar_cliente(id_barbearia=d[0], nome=d[1], telefone=d[2], nif=d[3], iban=d[4], morada=d[5], email=d[6]),
            self._atualizar_clientes
        )

    def _editar_cliente(self):
        sel = self.tree_clientes.selection()
        if not sel:
            return messagebox.showwarning("Aviso", "Selecione um cliente.")
        v = self.tree_clientes.item(sel[0])['values']
        self._janela_formulario(
            "Editar Cliente",
            [("ID Barbearia", v[1]), ("Nome", v[2]), ("Telefone", v[3]), ("NIF", v[4]), ("IBAN", v[5]), ("Morada", v[6]), ("Email", v[7])],
            lambda d, iid=v[0]: atualizar_cliente(id_cliente=iid, id_barbearia=d[0], nome=d[1], telefone=d[2], nif=d[3], iban=d[4], morada=d[5], email=d[6]),
            self._atualizar_clientes
        )

    def _remover_cliente(self):
        sel = self.tree_clientes.selection()
        if not sel:
            return messagebox.showwarning("Aviso", "Selecione um cliente.")
        iid = self.tree_clientes.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Deseja remover o cliente {iid}?"):
            code, msg = remover_cliente(id_cliente=iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Cliente removido!")
                self._atualizar_clientes()
            else:
                messagebox.showerror("Erro", str(msg))

    # ── ABA AGENDAMENTOS ──
    def _criar_aba_agendamentos(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Agendamentos")
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Atualizar Lista", command=self._atualizar_agendamentos).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Novo Agendamento", command=self._novo_agendamento).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Alterar Status", command=self._editar_status_agendamento).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Cancelar Marcação", command=self._remover_agendamento).pack(side=tk.LEFT, padx=4)

        container, self.tree_agendamentos = self._criar_treeview(frame, ["ID", "Data/Hora", "ID Cliente", "Cliente", "ID Barbeiro", "Barbeiro", "Serviço", "ID Barbearia", "Status"])
        container.pack(fill="both", expand=True, padx=10, pady=5)
        self._atualizar_agendamentos()

    def _atualizar_agendamentos(self):
        for item in self.tree_agendamentos.get_children():
            self.tree_agendamentos.delete(item)
        code, data = listar_agendamentos()
        if code == 200 and isinstance(data, dict):
            for iid, info in data.items():
                self.tree_agendamentos.insert("", "end", values=(
                    iid, info.get("data_hora"), info.get("id_cliente"), info.get("cliente"),
                    info.get("id_barbeiro"), info.get("barbeiro"), info.get("servico"),
                    info.get("id_barbearia"), info.get("status")
                ))

    def _novo_agendamento(self):
        self._janela_formulario(
            "Novo Agendamento",
            [("Data/Hora (YYYY-MM-DD HH:MM)", ""), ("ID Cliente", ""), ("ID Barbeiro", ""), ("Serviço", ""), ("ID Barbearia", "")],
            lambda d: criar_agendamento(d[0], d[1], d[2], d[3], d[4]),
            self._atualizar_agendamentos
        )

    def _editar_status_agendamento(self):
        sel = self.tree_agendamentos.selection()
        if not sel:
            return messagebox.showwarning("Aviso", "Selecione uma marcação.")
        v = self.tree_agendamentos.item(sel[0])['values']
        self._janela_formulario(
            "Alterar Estado",
            [("Novo Status (Pendente/Concluído/Cancelado)", v[8])],
            lambda d, iid=v[0]: agendamento_atualizar_status(iid, d[0]),
            self._atualizar_agendamentos
        )

    def _remover_agendamento(self):
        sel = self.tree_agendamentos.selection()
        if not sel:
            return messagebox.showwarning("Aviso", "Selecione uma marcação.")
        iid = self.tree_agendamentos.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Pretende eliminar permanentemente o agendamento {iid}?"):
            code, msg = agendamento_eliminar(iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Agendamento eliminado do arquivo!")
                self._atualizar_agendamentos()
            else:
                messagebox.showerror("Erro", str(msg))

    # ── ABA PRODUTOS ──
    def _criar_aba_produtos(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Produtos")
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Atualizar Lista", command=self._atualizar_produtos).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Adicionar Produto", command=self._novo_produto).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Remover Stock", command=self._remover_produto).pack(side=tk.LEFT, padx=4)

        container, self.tree_produtos = self._criar_treeview(frame, ["ID", "Nome", "Preço", "Stock"])
        container.pack(fill="both", expand=True, padx=10, pady=5)
        self._atualizar_produtos()

    def _atualizar_produtos(self):
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        code, data = listar_produtos()
        if code == 200 and isinstance(data, dict):
            for iid, info in data.items():
                self.tree_produtos.insert("", "end", values=(iid, info.get("nome"), info.get("preco"), info.get("stock")))

    def _novo_produto(self):
        self._janela_formulario(
            "Adicionar Produto",
            [("Nome", ""), ("Preço", ""), ("Stock", "")],
            lambda d: adicionar_produto(d[0], d[1], d[2]),
            self._atualizar_produtos
        )

    def _remover_produto(self):
        sel = self.tree_produtos.selection()
        if not sel:
            return messagebox.showwarning("Aviso", "Selecione um produto.")
        iid = self.tree_produtos.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Remover o produto {iid} do catálogo?"):
            code, msg = remover_produto(iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Produto removido!")
                self._atualizar_produtos()
            else:
                messagebox.showerror("Erro", str(msg))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GestorBarbeariaGUI()
    app.run()