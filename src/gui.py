import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from barbearia import criar_barbearia, listar_barbearias, atualizar_barbearia, remover_barbearia
from barbeiro import criar_barbeiro, listar_barbeiros, remover_barbeiro
from cliente import criar_cliente, listar_clientes, remover_cliente
from agendamento import (criar_agendamento, listar_agendamentos,
                         atualizar_status as agendamento_atualizar_status,
                         eliminar_agendamento as agendamento_eliminar)
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

    # ── Estilo ──────────────────────────────────────────────────────────────
    def _criar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", rowheight=25)
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

    # ── Interface principal ─────────────────────────────────────────────────
    def _criar_interface(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self._criar_aba_barbearias(notebook)
        self._criar_aba_barbeiros(notebook)
        self._criar_aba_clientes(notebook)
        self._criar_aba_agendamentos(notebook)
        self._criar_aba_produtos(notebook)

        self.status_bar = tk.Label(
            self.root, text="Sistema pronto. Selecione uma aba.",
            bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#f0f0f0"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _set_status(self, msg):
        self.status_bar.config(text=msg)

    # ── Utilitários de UI ───────────────────────────────────────────────────
    def _criar_treeview(self, parent, colunas):
        """
        CORRIGIDO: o container é criado mas NÃO empacotado aqui.
        O chamador decide a ordem de pack (botões primeiro, depois treeview)
        para garantir que os botões nunca ficam ocultos.
        """
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

        larguras = {
            "ID": 70, "Nome": 200, "Morada": 220, "NIF": 110,
            "Email": 200, "Telefone": 120, "Barbearia": 90,
            "Especialidade": 160, "Data/Hora": 160,
            "Serviço": 150, "Status": 120,
            "Preço": 90, "Stock": 80,
        }
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=larguras.get(col, 130), minwidth=60)

        return container, tree

    def _janela_formulario(self, titulo, campos, funcao_guardar, funcao_atualizar):
        """Janela de formulário genérica, modal."""
        altura = min(80 + len(campos) * 65, 700)
        win = tk.Toplevel(self.root)
        win.title(titulo)
        win.geometry(f"520x{altura}")
        win.resizable(False, True)
        win.grab_set()  # modal

        # Frame com scroll para formulários longos (barbeiro tem 8 campos)
        canvas = tk.Canvas(win, borderwidth=0)
        scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        inner = ttk.Frame(canvas)

        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        entries = []
        for label_text, default in campos:
            ttk.Label(inner, text=label_text + ":").pack(
                pady=(8, 0), anchor="w", padx=10)
            entry = ttk.Entry(inner, width=55)
            entry.insert(0, str(default))
            entry.pack(pady=(0, 2), padx=10, fill="x")
            entries.append(entry)

        def salvar():
            valores = [e.get().strip() for e in entries]
            code, result = funcao_guardar(valores)
            if code in (200, 201):
                messagebox.showinfo("Sucesso", f"{titulo} guardado com sucesso!")
                funcao_atualizar()
                win.destroy()
            else:
                messagebox.showerror("Erro", str(result))

        ttk.Button(inner, text="  Guardar", command=salvar).pack(pady=16)

    # ── BARBEARIAS ──────────────────────────────────────────────────────────
    def _criar_aba_barbearias(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="  Barbearias")

        # CORRIGIDO: botões empacotados ANTES da treeview para não ficarem ocultos
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text=" Atualizar",     command=self._atualizar_barbearias).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Nova Barbearia", command=self._nova_barbearia).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Editar",         command=self._editar_barbearia).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Remover",        command=self._remover_barbearia).pack(side=tk.LEFT, padx=4)

        container, self.tree_barbearias = self._criar_treeview(
            frame, ["ID", "Nome", "Morada", "NIF"])
        container.pack(fill="both", expand=True, padx=10, pady=5)

        self._atualizar_barbearias()

    def _atualizar_barbearias(self):
        for item in self.tree_barbearias.get_children():
            self.tree_barbearias.delete(item)
        code, data = listar_barbearias()
        if code == 200:
            for iid, info in data.items():
                self.tree_barbearias.insert("", "end", values=(
                    iid, info.get("nome", ""), info.get("morada", ""), info.get("nif", "")))
        self._set_status(f"Barbearias carregadas.")

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
            messagebox.showwarning("Aviso", "Selecione uma barbearia para editar.")
            return
        v = self.tree_barbearias.item(sel[0])['values']
        iid, nome, morada, nif = v[0], v[1], v[2], v[3]
        self._janela_formulario(
            "Editar Barbearia",
            [("Nome", nome), ("Morada", morada), ("NIF", nif)],
            # CORRIGIDO: iid capturado via argumento padrão, não por referência
            lambda d, _iid=iid: atualizar_barbearia(_iid, d[0], d[1], d[2]),
            self._atualizar_barbearias
        )

    def _remover_barbearia(self):
        sel = self.tree_barbearias.selection()
        if not sel:
            # CORRIGIDO: aviso em vez de falha silenciosa
            messagebox.showwarning("Aviso", "Selecione uma barbearia para remover.")
            return
        iid = self.tree_barbearias.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Remover barbearia {iid}?"):
            code, msg = remover_barbearia(iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Barbearia removida!")
                self._atualizar_barbearias()
            else:
                messagebox.showerror("Erro", str(msg))

    # ── BARBEIROS ───────────────────────────────────────────────────────────
    def _criar_aba_barbeiros(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="  Barbeiros")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text=" Atualizar",    command=self._atualizar_barbeiros).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Novo Barbeiro", command=self._novo_barbeiro).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Remover",       command=self._remover_barbeiro).pack(side=tk.LEFT, padx=4)

        container, self.tree_barbeiros = self._criar_treeview(
            frame, ["ID", "Nome", "Especialidade", "Telefone", "Barbearia"])
        container.pack(fill="both", expand=True, padx=10, pady=5)

        self._atualizar_barbeiros()

    def _atualizar_barbeiros(self):
        for item in self.tree_barbeiros.get_children():
            self.tree_barbeiros.delete(item)
        code, data = listar_barbeiros()
        if code == 200:
            for iid, info in data.items():
                self.tree_barbeiros.insert("", "end", values=(
                    iid, info.get("nome", ""), info.get("especialidade", ""),
                    info.get("telefone", ""), info.get("id_barbearia", "")))
        self._set_status("Barbeiros carregados.")

    def _novo_barbeiro(self):
        self._janela_formulario(
            "Novo Barbeiro",
            [("Nome", ""), ("Especialidade", ""), ("Telefone", ""),
             ("NIF", ""), ("IBAN", ""), ("Morada", ""), ("Email", ""), ("ID Barbearia", "")],
            lambda d: criar_barbeiro(d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7]),
            self._atualizar_barbeiros
        )

    def _remover_barbeiro(self):
        sel = self.tree_barbeiros.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um barbeiro para remover.")
            return
        iid = self.tree_barbeiros.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Remover barbeiro {iid}?"):
            code, msg = remover_barbeiro(iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Barbeiro removido!")
                self._atualizar_barbeiros()
            else:
                messagebox.showerror("Erro", str(msg))

    # ── CLIENTES ────────────────────────────────────────────────────────────
    def _criar_aba_clientes(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="  Clientes")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text=" Atualizar",  command=self._atualizar_clientes).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Novo Cliente", command=self._novo_cliente).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Remover",    command=self._remover_cliente).pack(side=tk.LEFT, padx=4)

        container, self.tree_clientes = self._criar_treeview(
            frame, ["ID", "Nome", "Telefone", "Email", "Barbearia"])
        container.pack(fill="both", expand=True, padx=10, pady=5)

        self._atualizar_clientes()

    def _atualizar_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        code, data = listar_clientes()
        if code == 200:
            for iid, info in data.items():
                self.tree_clientes.insert("", "end", values=(
                    iid, info.get("nome", ""), info.get("telefone", ""),
                    info.get("email", ""), info.get("id_barbearia", "")))
        self._set_status("Clientes carregados.")

    def _novo_cliente(self):
        self._janela_formulario(
            "Novo Cliente",
            [("ID Barbearia", ""), ("Nome", ""), ("Telefone", ""),
             ("NIF", ""), ("IBAN", ""), ("Morada", ""), ("Email", "")],
            lambda d: criar_cliente(d[0], d[1], d[2], d[3], d[4], d[5], d[6]),
            self._atualizar_clientes
        )

    def _remover_cliente(self):
        sel = self.tree_clientes.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um cliente para remover.")
            return
        iid = self.tree_clientes.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Remover cliente {iid}?"):
            code, msg = remover_cliente(iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Cliente removido!")
                self._atualizar_clientes()
            else:
                messagebox.showerror("Erro", str(msg))

    # ── AGENDAMENTOS ────────────────────────────────────────────────────────
    def _criar_aba_agendamentos(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="  Agendamentos")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text=" Atualizar",        command=self._atualizar_agendamentos).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Novo Agendamento", command=self._novo_agendamento).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Mudar Status",     command=self._mudar_status).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Eliminar",         command=self._eliminar_agendamento).pack(side=tk.LEFT, padx=4)

        container, self.tree_agendamentos = self._criar_treeview(
            frame, ["ID", "Data/Hora", "Cliente", "Barbeiro", "Serviço", "Status"])
        container.pack(fill="both", expand=True, padx=10, pady=5)

        self._atualizar_agendamentos()

    def _atualizar_agendamentos(self):
        for item in self.tree_agendamentos.get_children():
            self.tree_agendamentos.delete(item)
        code, data = listar_agendamentos()
        if code == 200:
            for iid, info in data.items():
                self.tree_agendamentos.insert("", "end", values=(
                    iid, info.get("data_hora", ""), info.get("cliente", ""),
                    info.get("barbeiro", ""), info.get("servico", ""), info.get("status", "")))
        self._set_status("Agendamentos carregados.")

    def _novo_agendamento(self):
        """
        CORRIGIDO: win.grab_set() adicionado para tornar a janela modal,
        consistente com todas as outras janelas de formulário.
        """
        win = tk.Toplevel(self.root)
        win.title("Novo Agendamento")
        win.geometry("500x420")
        win.resizable(False, False)
        win.grab_set()

        campos_info = [
            ("Data e Hora (YYYY-MM-DD HH:MM)", ""),
            ("ID Cliente", ""),
            ("ID Barbeiro", ""),
            ("Serviço", ""),
            ("ID Barbearia", ""),
        ]
        entries = []
        for label_text, default in campos_info:
            ttk.Label(win, text=label_text + ":").pack(pady=(8, 0), anchor="w", padx=20)
            entry = ttk.Entry(win, width=50)
            entry.insert(0, default)
            entry.pack(pady=(0, 2), padx=20, fill="x")
            entries.append(entry)

        def salvar():
            code, result = criar_agendamento(
                entries[0].get(), entries[1].get(), entries[2].get(),
                entries[3].get(), entries[4].get()
            )
            if code in (200, 201):
                messagebox.showinfo("Sucesso", "Agendamento criado!")
                self._atualizar_agendamentos()
                win.destroy()
            else:
                messagebox.showerror("Erro", str(result))

        ttk.Button(win, text="  Guardar Agendamento", command=salvar).pack(pady=16)

    def _mudar_status(self):
        sel = self.tree_agendamentos.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um agendamento.")
            return
        iid = self.tree_agendamentos.item(sel[0])['values'][0]
        # CORRIGIDO: renomeado para agendamento_atualizar_status para evitar
        # qualquer confusão com o método _set_status da classe
        novo_status = simpledialog.askstring(
            "Mudar Status", "Novo status:", initialvalue="Confirmado", parent=self.root)
        if novo_status:
            code, _ = agendamento_atualizar_status(iid, novo_status)
            if code == 200:
                messagebox.showinfo("Sucesso", "Status atualizado!")
                self._atualizar_agendamentos()
            else:
                messagebox.showerror("Erro", "Não foi possível atualizar o status.")

    def _eliminar_agendamento(self):
        sel = self.tree_agendamentos.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um agendamento para eliminar.")
            return
        iid = self.tree_agendamentos.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Eliminar agendamento {iid}?"):
            # CORRIGIDO: renomeado para agendamento_eliminar para evitar
            # conflito com o nome do método desta classe
            code, _ = agendamento_eliminar(iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Agendamento eliminado!")
                self._atualizar_agendamentos()
            else:
                messagebox.showerror("Erro", "Não foi possível eliminar o agendamento.")

    # ── PRODUTOS ────────────────────────────────────────────────────────────
    def _criar_aba_produtos(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="  Produtos")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text=" Atualizar",   command=self._atualizar_produtos).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Novo Produto", command=self._novo_produto).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text=" Remover",      command=self._remover_produto).pack(side=tk.LEFT, padx=4)

        container, self.tree_produtos = self._criar_treeview(
            frame, ["ID", "Nome", "Preço", "Stock", "Barbearia"])
        container.pack(fill="both", expand=True, padx=10, pady=5)

        self._atualizar_produtos()

    def _atualizar_produtos(self):
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        code, data = listar_produtos()
        if code == 200:
            for iid, info in data.items():
                self.tree_produtos.insert("", "end", values=(
                    iid, info.get("nome", ""), info.get("preco_venda", ""),
                    info.get("quantidade_stock", ""), info.get("id_barbearia", "")))
        self._set_status("Produtos carregados.")

    def _novo_produto(self):
        self._janela_formulario(
            "Novo Produto",
            [("Nome", ""), ("Preço", ""), ("Quantidade", ""), ("ID Barbearia", "")],
            lambda d: adicionar_produto(d[0], d[1], d[2], d[3]),
            self._atualizar_produtos
        )

    def _remover_produto(self):
        sel = self.tree_produtos.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um produto para remover.")
            return
        iid = self.tree_produtos.item(sel[0])['values'][0]
        if messagebox.askyesno("Confirmar", f"Remover produto {iid}?"):
            code, msg = remover_produto(iid)
            if code == 200:
                messagebox.showinfo("Sucesso", "Produto removido!")
                self._atualizar_produtos()
            else:
                messagebox.showerror("Erro", str(msg))

    # ── Arranque ────────────────────────────────────────────────────────────
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GestorBarbeariaGUI()
    app.run()