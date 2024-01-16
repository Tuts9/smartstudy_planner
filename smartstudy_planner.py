from fpdf import FPDF
from tkinter import messagebox, ttk
import customtkinter as ctk
from datetime import date
import requests
import sqlite3
import json
import threading

API_KEY = 'SUA_CHAVE_API'

ctk.set_appearance_mode('System')
ctk.set_default_color_theme('blue')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('SmartStudy Planner')
        self.geometry(f'{1100}x{580}')

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.criar_banco()

        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text='SmartStudy Planner', font=ctk.CTkFont(size=20, weight='bold'))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text='Salvar em PDF', command=self.criar_pdf)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text='Histórico', command=self.open_toplevel)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # Adicionar funcionalidade de ler arquivos PDF futuramente
        # self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, text='Selecionar Arquivo', command=self.selecionar_arquivo)
        # self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        
        self.combobox_label = ctk.CTkLabel(self.sidebar_frame, text='O que deseja gerar:', anchor='w')
        self.combobox_label.grid(row=5, column=0, padx=20, pady=(10,0))
        self.combobox_var = ctk.StringVar(value='')
        self.combobox_1 = ctk.CTkComboBox(self.sidebar_frame, values=['Mapa mental', 'Plano de estudos'], variable=self.combobox_var)
        self.combobox_1.set('Escolha...')
        self.combobox_1.configure(state='readonly')
        self.combobox_1.grid(row=6, column=0, padx=20, pady=(10,10))
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text='Appearance Mode:', anchor='w')
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10,0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=['Light', 'Dark', 'System'], 
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.set('Dark')
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10,20))

        self.main_entry = ctk.CTkEntry(self, placeholder_text='Digite o nome do conteúdo')
        self.main_entry.grid(row=3, column=1, columnspan=2, padx=(20,0), pady=(20,20), sticky='nsew')
        self.main_button = ctk.CTkButton(master=self, text='Gerar', fg_color='transparent', border_width=2, text_color=('gray10', '#DCE4EE'),
                                          command=self.pesquisa)
        self.main_button.grid(row=3, column=3, padx=(20,20), pady=(20,20), sticky='nsew')

        self.title_label = ctk.CTkLabel(self, text='Titulo', font=ctk.CTkFont(size=20, weight='bold'))
        self.title_label.grid(row=0, column=1, columnspan=3, padx=(10,10), pady=(10,0), sticky='nsew')
        
        self.progressbar_1 = ctk.CTkProgressBar(self.sidebar_frame)
        self.progressbar_1.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky='ew')
        self.progressbar_1.configure(mode="determinate")
        self.progressbar_1.set(0)
        
        self.textbox = ctk.CTkTextbox(self, width=400, height=300, state='disabled')
        self.textbox.grid(row=1, column=1, columnspan=3, rowspan=2, padx=(20,20), pady=(20,0), sticky='nsew')

        self.historic_window = None

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def clean_textbox(self):
        self.textbox.configure(state='normal')
        self.textbox.delete('0.0', 'end')
        self.textbox.configure(state='disabled')

    def update(self):
        self.titulo = f'{self.prompt_escol}: {self.assunto.capitalize()}'
        self.clean_textbox()

        self.title_label.configure(text=f'{self.titulo}')
        self.textbox.configure(state='normal')
        self.textbox.insert('0.0', self.mensagem)
        self.progressbar_1.stop()
        self.progressbar_1.set(0)

        self.data_atual = date.today()
        self.salvar_pesquisa()

        self.textbox.configure(state='disabled')
        self.main_entry.delete('0', 'end')

    def pesquisa(self):  

        self.prompt_escol = self.combobox_var.get()
        self.assunto = self.main_entry.get()

        if self.prompt_escol == 'Mapa mental':
            prompt = f'''Tópico: {self.assunto}
                        Crie um mapa mental sobre o tópico acima
                        Liste a ideia central, os ramos principais e os subramos'''
        
        elif self.prompt_escol == 'Plano de estudos':
            prompt = f'''Elabore um plano de estudos sobre {self.assunto}'''

        else:
            messagebox.showerror('Erro', 'Escolha uma das duas opções!')
            return

        ger = threading.Thread(target=self.gerar_resposta, args=(prompt,))
        ger.start()

        self.progressbar_1.start()

    def gerar_resposta(self, prompt):

        headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
        link = 'https://api.openai.com/v1/chat/completions'
        id_modelo = 'gpt-3.5-turbo'

        subject = prompt

        body_mensagem = {
            'model': id_modelo,
            'stream': False,
            'messages': [{'role': 'user', 'content': f'{subject}'}]
        }
        body_mensagem = json.dumps(body_mensagem)
        
        try:
            requisicao = requests.post(link, headers=headers, data=body_mensagem, timeout=None)
            resposta = requisicao.json()

            if 'choices' in resposta:
                self.mensagem = resposta['choices'][0]['message']['content']
                # Atualizar a interface gráfica com a resposta da API
                self.update()
            else:
                self.mensagem = "Resposta não recebida."
                self.update()
        except requests.exceptions.RequestException as e:
            self.mensagem = f"Erro na requisição: {str(e)}"
            self.update()
        
    def selecionar_arquivo(self):
        messagebox.showinfo('Aviso', 'Em breve')

    def criar_banco(self):
        conexao = sqlite3.connect('pesquisas.db')
        c = conexao.cursor()
        c.execute('''
                CREATE TABLE IF NOT EXISTS tb_pesquisa_historic(
                    N_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    T_PESQUISA TEXT NOT NULL,
                    T_METODO TEXT NOT NULL,
                    D_DATE DATE NOT NULL
            )'''
        )
        conexao.commit()
        conexao.close()

    def salvar_pesquisa(self):
        pesquisa = self.main_entry.get()
        metodo = self.combobox_var.get()
        data = self.data_atual
        
        conexao = sqlite3.connect('pesquisas.db')
        c = conexao.cursor()
        c.execute('''
                    INSERT INTO tb_pesquisa_historic (T_PESQUISA, T_METODO, D_DATE) VALUES (?, ?, ?)''', 
                    (pesquisa, metodo, data))
        
        conexao.commit()
        conexao.close()

    def open_toplevel(self):
        if self.historic_window is None or not self.historic_window.winfo_exists():
            self.historic_window = HistoricWindow()  # create window if its None or destroyed
        else:
            self.historic_window.focus()  # if window exists focus it

    def criar_pdf(self):
        title = self.assunto
        text = self.mensagem

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font('Arial', 'B', 18)
            pdf.multi_cell(190, 10, f'{self.titulo}', align='C')
            pdf.ln()
            pdf.set_font('Arial', '', 12)
            pdf.multi_cell(190, 5, f'{text}', align='L')
            nome_pdf = f'{title}.pdf'
            pdf.output(nome_pdf)

            messagebox.showinfo('Aviso', 'O arquivo PDF foi criado com sucesso.')

        except:
            messagebox.showerror('Erro', 'Não foi possível gerar seu arquivo PDF.')

class HistoricWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title('Histórico de pesquisas')
        self.geometry('600x300')
        self.resizable(False, False)

        self.frame_main = ctk.CTkFrame(self, fg_color='transparent', width=600)
        self.frame_main.grid(row=0, column=0)

        self.tree = ttk.Treeview(self.frame_main, columns=('ID', 'Pesquisa', 'Método', 'Data'), show='headings')

        self.tree.heading('ID', text='ID')
        self.tree.heading('Pesquisa', text='Pesquisa')
        self.tree.heading('Método', text='Método')
        self.tree.heading('Data', text='Data')

        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Pesquisa', width=250, anchor='center')
        self.tree.column('Método', width=100, anchor='center')
        self.tree.column('Data', width=100, anchor='center')

        self.tree.pack(side='left', fill='both', expand=True)
        self.listar_pesquisas()

        self.scrollbar = ttk.Scrollbar(self.frame_main, orient='vertical', command=self.tree.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.frame_bt = ctk.CTkFrame(self)
        self.frame_bt.grid(row=1, column=0, columnspan=3, pady=10)
        self.bt_excluir = ctk.CTkButton(self.frame_bt, text='Excluir', fg_color='red', hover_color='darkred', command=self.excluir_pesquisa)
        self.bt_excluir.pack()

    def listar_pesquisas(self):
        conexao = sqlite3.connect('pesquisas.db')
        c = conexao.cursor()
        c.execute("SELECT * FROM tb_pesquisa_historic")
        self.rows = c.fetchall()
        conexao.close()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in self.rows:
            self.tree.insert('', 'end', values=row)

    def excluir_pesquisa(self):
        selected_item = self.tree.selection()

        if selected_item:

            if messagebox.askyesno('Aviso', 'Deseja realmente excluir o item selecionado?'):
                conexao = sqlite3.connect('pesquisas.db')
                c = conexao.cursor()

                for item in selected_item:
                    c.execute("DELETE FROM tb_pesquisa_historic WHERE N_ID=?", (self.tree.item(item, 'values')[0],))

                conexao.commit()
                conexao.close()
                self.listar_pesquisas()
        else:
            messagebox.showerror('Erro', 'Selecione um item para excluir.')

if __name__ == '__main__':
    app = App()
    app.mainloop()
