import tkinter as tk
from tkinter import filedialog, messagebox
from processors.calota_processor import CalotaProcessor
from processors.roda_ferro_processor import RodaFerroProcessor
from config import DEFAULT_PASTA_RAIZ, DESCRICAO_CALOTA, DESCRICAO_RODA_FERRO
from utils.helpers import carregar_template

class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Pastas e Arquivos")
        self.planilha_path = ""
        self.pasta_raiz = DEFAULT_PASTA_RAIZ
        self.tipo_produto = tk.StringVar(value="calota")

        self.criar_interface()

    def criar_interface(self):
        # Selecionar tipo de produto
        tk.Label(self.root, text="Tipo de Produto:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Radiobutton(self.root, text="Calota", variable=self.tipo_produto, value="calota").grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Radiobutton(self.root, text="Roda de Ferro", variable=self.tipo_produto, value="roda_ferro").grid(row=0, column=2, padx=5, pady=5, sticky="w")

        # Caminho da planilha
        tk.Label(self.root, text="Caminho da Planilha:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_planilha = tk.Entry(self.root, width=50)
        self.entry_planilha.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Procurar", command=self.selecionar_planilha).grid(row=1, column=2, padx=5, pady=5)

        # Caminho da pasta raiz
        tk.Label(self.root, text="Caminho da Pasta Raiz:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_pasta_raiz = tk.Entry(self.root, width=50)
        self.entry_pasta_raiz.insert(0, self.pasta_raiz)
        self.entry_pasta_raiz.grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Procurar", command=self.selecionar_pasta_raiz).grid(row=2, column=2, padx=5, pady=5)

        # Botão Executar
        tk.Button(self.root, text="Executar", command=self.executar_script).grid(row=3, column=1, pady=10)

    def selecionar_planilha(self):
        arquivo = filedialog.askopenfilename(title="Selecione a planilha", filetypes=[("Arquivos Excel", "*.xlsx *.xls")])
        if arquivo:
            self.entry_planilha.delete(0, tk.END)
            self.entry_planilha.insert(0, arquivo)

    def selecionar_pasta_raiz(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta raiz")
        if pasta:
            self.entry_pasta_raiz.delete(0, tk.END)
            self.entry_pasta_raiz.insert(0, pasta)

    def executar_script(self):
        self.planilha_path = self.entry_planilha.get()
        self.pasta_raiz = self.entry_pasta_raiz.get()

        if not self.planilha_path or not self.pasta_raiz:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        tipo = self.tipo_produto.get()
        descricao_base = carregar_template(DESCRICAO_CALOTA if tipo == "calota" else DESCRICAO_RODA_FERRO)

        try:
            if tipo == "calota":
                processor = CalotaProcessor(self.planilha_path, self.pasta_raiz, descricao_base)
            elif tipo == "roda_ferro":
                processor = RodaFerroProcessor(self.planilha_path, self.pasta_raiz, descricao_base)
            processor.processar()
            messagebox.showinfo("Sucesso", "Processo concluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")