from tkinter import *
from tkinter import messagebox, ttk
from customtkinter import *
import sqlite3
import pygame.mixer

#inicia as variáveis que definem o que a criança quer ou não quer e qual é o menu selecionado no momento, começa com querer = true e selecinado = 0, que é a aba "alimentos"
global Querer
global selecionado
Querer = True
selecionado = 0
pygame.mixer.init()
v=0

#função usada pra ir da j1() ou j2() ou telaFuncionário() para a j0
def j0():

    som()

    global tela
    if tela == 1:
        canvasHud1.destroy()
    elif tela == 2:
        canvasHud3.destroy()
    elif tela == 3:
        canvasHud4.destroy()

    global canvasHud, v

    v=0

    imgCanvas = PhotoImage(file='canvas2.png')
    canvasHud = Canvas(janela, width=471, height=331, bg='orange', highlightthickness=0)
    canvasHud.create_image(0, 0, image=imgCanvas, anchor='nw')
    canvasHud.place(relx=0.5, rely=0.5, anchor='center')

    imgLogo = PhotoImage(file='logo.png')
    l_logo = Label(canvasHud, image=imgLogo, bg='white')
    l_logo.place(relx=0.49, rely=0.25, anchor='center')

    imgLogin = PhotoImage(file='login_botão.png')
    botãoLogin = Button(canvasHud, image=imgLogin, command = j1, bg='white', border=0, activebackground='white', cursor='hand2')
    botãoLogin.place(relx=0.49, rely=0.55, anchor='center')

    imgCadastro = PhotoImage(file='criar_botão.png')
    botãoCadastro = Button(canvasHud, image = imgCadastro, command = j2, bg='white', border=0, activebackground='white', cursor='hand2')
    botãoCadastro.place(relx=0.49, rely=0.71, anchor='center')

    imgSair = PhotoImage(file='b_sair.png')
    botãoSair = Button(canvasHud, image = imgSair, command = sair, bg='white', border=0, activebackground='white', cursor='hand2')
    botãoSair.place(relx=0.49, rely=0.87, anchor='center')

    janela.wm_minsize(width = 800, height = 600)
    janela.mainloop()

#fecha o programa
def sair():
    som()
    resposta = messagebox.askyesno("Confirmação", "Tem certeza de que deseja sair do Autikids?")
    if resposta:
        sys.exit()

#toca o som menuclick
def som():
    pygame.mixer.Sound('menu-click.wav').play()

#toca o arquivo de voz necessário com relação a selecionar menu
def falamenu(arquivo):
    pygame.mixer.Sound(arquivo).play()

#toca o arquivo de voz necessário para botões que independem de Querer
def fala0(arquivo):
    som()
    pygame.mixer.Sound(arquivo).play()

#toca o arquivo de voz necessário para botões que dependem de Querer
def fala(arquivo):
    if Querer:
        som()
        pygame.mixer.Sound(f'QR{arquivo}').play()
    else:
        som()
        pygame.mixer.Sound(f'NQR{arquivo}').play()

#interface pra cadastrar, deletar, alterar e visualizar perfis de alunos
def telaBancoAlunos():
    
    global canvasGuia
    global canvasHud
    global canvasHud2
    
    som()
    canvasHud4.destroy()
    global tela
    tela = 5



    def cadastrar_aluno():
        som()
        conexao = sqlite3.connect('banco_alunos.db')
        cursor = conexao.cursor()


        if not entry_nome.get() or not entry_sobrenome.get() or not entry_datadenascimento.get() or not entry_telefone.get():
            messagebox.showwarning("Campos obrigatórios vazios", "Por favor, preencha todos os campos obrigatórios(*).")
            return

        cursor.execute('''
            INSERT INTO alunos (nome, sobrenome, sexo, datadenascimento, telefone, endereco, cep, bairro, cidade, observacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry_nome.get(),
            entry_sobrenome.get(),
            entry_sexo.get(),
            entry_datadenascimento.get(),
            entry_telefone.get(),
            entry_endereco.get(),
            entry_cep.get(),
            entry_bairro.get(),
            entry_cidade.get(),
            entry_observacao.get()
        ))

        conexao.commit()
        conexao.close()

        entry_nome.delete(0, "end")
        entry_sobrenome.delete(0, "end")
        entry_sexo.delete(0, "end")
        entry_datadenascimento.delete(0, "end")
        entry_telefone.delete(0, "end")
        entry_endereco.delete(0, "end")
        entry_cep.delete(0, "end")
        entry_bairro.delete(0, "end")
        entry_cidade.delete(0, "end")
        entry_observacao.delete(0, "end")

        preencher_tabela()

        messagebox.showinfo("Cadastro realizado", "O aluno foi cadastrado com sucesso.")

    def preencher_tabela():
        # Conectar ao banco de dados
        conexao = sqlite3.connect('banco_alunos.db')
        cursor = conexao.cursor()

        # Executar a consulta SQL para buscar os dados
        cursor.execute('SELECT id, nome, sobrenome, sexo, datadenascimento, telefone, endereco, cep, bairro, cidade, observacao FROM alunos')

        # Obter os dados retornados pela consulta
        dados = cursor.fetchall()

        # Limpar a tabela antes de preencher novamente
        tabela.delete(*tabela.get_children())

        # Preencher a tabela com os dados
        for linha in dados:
            id_aluno = linha[0]
            dados_aluno = linha[1:]
            tabela.insert('', 'end', text=id_aluno, values=dados_aluno)

        # Fechar a conexão com o banco de dados

        cursor.close()
        conexao.close()

    def atualizar_resultados():
        global resultados
        resultados = preencher_tabela()

    def excluir_aluno():
        som()
        aluno_selecionado = tabela.selection()

        if aluno_selecionado:
            resposta = messagebox.askyesno("Confirmação", "Tem certeza de que deseja deletar o aluno selecionado?")
            if resposta:
                aluno_id = tabela.item(aluno_selecionado)['text']
                conexao = sqlite3.connect('banco_alunos.db')
                cursor = conexao.cursor()

                cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
                tabela.delete(aluno_selecionado)
                conexao.commit()

                atualizar_resultados()

                messagebox.showinfo("Aluno deletado", "Os dados foram deletados com sucesso.")
        else:
            messagebox.showwarning('Aviso', 'Nenhum aluno selecionado.')

    # Variável global para armazenar o ID do aluno selecionado
    aluno_id_selecionado = None

    def editar_aluno(event):
        global aluno_id_selecionado
        aluno_selecionado = tabela.focus()

        if aluno_selecionado:
            # Obter o ID do aluno selecionado
            aluno_id_selecionado = tabela.item(aluno_selecionado)['text']

            # Obter os dados do aluno selecionado do banco de dados
            conexao = sqlite3.connect('banco_alunos.db')
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id_selecionado,))
            dados_aluno = cursor.fetchone()
            conexao.close()

            # Preencher as entradas com os dados do aluno selecionado
            entry_nome.delete(0, "end")
            entry_nome.insert(0, dados_aluno[1])
            entry_sobrenome.delete(0, "end")
            entry_sobrenome.insert(0, dados_aluno[2])
            entry_sexo.delete(0, "end")
            entry_sexo.insert(0, dados_aluno[3])
            entry_datadenascimento.delete(0, "end")
            entry_datadenascimento.insert(0, dados_aluno[4])
            entry_telefone.delete(0, "end")
            entry_telefone.insert(0, dados_aluno[5])
            entry_endereco.delete(0, "end")
            entry_endereco.insert(0, dados_aluno[6])
            entry_cep.delete(0, "end")
            entry_cep.insert(0, dados_aluno[7])
            entry_bairro.delete(0, "end")
            entry_bairro.insert(0, dados_aluno[8])
            entry_cidade.delete(0, "end")
            entry_cidade.insert(0, dados_aluno[9])
            entry_observacao.delete(0, "end")
            entry_observacao.insert(0, dados_aluno[10])
        else:
            # Limpar as entradas se nenhum aluno estiver selecionado
            entry_nome.delete(0, "end")
            entry_sobrenome.delete(0, "end")
            entry_sexo.delete(0, "end")
            entry_datadenascimento.delete(0, "end")
            entry_telefone.delete(0, "end")
            entry_endereco.delete(0, "end")
            entry_cep.delete(0, "end")
            entry_bairro.delete(0, "end")
            entry_cidade.delete(0, "end")
            entry_observacao.delete(0, "end")

    def atualizar_aluno():
        global aluno_id_selecionado
        conexao = sqlite3.connect('banco_alunos.db')
        cursor = conexao.cursor()

        # Atualizar os dados do aluno no banco de dados
        cursor.execute('''
                        UPDATE alunos SET nome = ?, sobrenome = ?, sexo = ?, datadenascimento = ?, telefone = ?,
                        endereco = ?, cep = ?, bairro = ?, cidade = ?, observacao = ? WHERE id = ?
                    ''', (
            entry_nome.get(),
            entry_sobrenome.get(),
            entry_sexo.get(),
            entry_datadenascimento.get(),
            entry_telefone.get(),
            entry_endereco.get(),
            entry_cep.get(),
            entry_bairro.get(),
            entry_cidade.get(),
            entry_observacao.get(),
            aluno_id_selecionado
        ))

        conexao.commit()
        conexao.close()

        # Limpar as entradas
        entry_nome.delete(0, "end")
        entry_sobrenome.delete(0, "end")
        entry_sexo.delete(0, "end")
        entry_datadenascimento.delete(0, "end")
        entry_telefone.delete(0, "end")
        entry_endereco.delete(0, "end")
        entry_cep.delete(0, "end")
        entry_bairro.delete(0, "end")
        entry_cidade.delete(0, "end")
        entry_observacao.delete(0, "end")
        atualizar_resultados()

        # Atualizar a tabela com os dados atualizados
        preencher_tabela()
        
        messagebox.showinfo("Aluno alterado", "Os dados foram alterados com sucesso.")

        # Limpar o ID do aluno selecionado
        aluno_id_selecionado = None

    canvasGuia = Canvas(janela, width=1366, height=768, bg='orange', highlightthickness=0)
    canvasGuia.place(relx=0.5, rely=0.5, anchor='center')

    imgCanvas = PhotoImage(file='canvas6.png')
    canvasHud = Canvas(canvasGuia, width=1181, height=313, bg='orange', highlightthickness=0)
    canvasHud.create_image(0, 0, image=imgCanvas, anchor='nw')
    canvasHud.place(relx=0.5, rely=0.25, anchor='center')

    imgCanvas2 = PhotoImage(file='canvas8.png')
    canvasHud2 = Canvas(canvasGuia, width=1181, height=345, bg='orange', highlightthickness=0)
    canvasHud2.create_image(0, 0, image=imgCanvas2, anchor='nw')
    canvasHud2.place(relx=0.5, rely=0.725, anchor='center')

    # Labels
    label_nome = Label(canvasHud, text='Nome*: ', bg='white', fg="black", border=2, font=('Poppins 12 bold'))
    label_nome.place(x=26, y=69, anchor='nw')

    label_sobrenome = Label(canvasHud, text='Sobrenome*: ', bg='white', fg="black", border=2, font=('Poppins 12 bold'))
    label_sobrenome.place(x=26, y=115, anchor='nw')

    label_datadenascimento = Label(canvasHud, text='Data De Nascimento*: ', bg='white', fg="black", border=2,
                                font=('Poppins 12 bold'))
    label_datadenascimento.place(x=26, y=161, anchor='nw')

    label_telefone = Label(canvasHud, text='Telefone*: ', bg='white', fg="black", border=2, font=('Poppins 12 bold'))
    label_telefone.place(x=26, y=207, anchor='nw')

    label_sexo = Label(canvasHud, text='Sexo: ', bg='white', fg="black", border=2, font=('Poppins 12 bold'))
    label_sexo.place(x=26, y=253, anchor='nw')

    label_endereco = Label(canvasHud, text='Endereço: ', bg='white', fg="black", border=2, font=('Poppins 12 bold'))
    label_endereco.place(x=525, y=69, anchor='nw')

    label_cep = Label(canvasHud, text='Cep: ', bg='white', fg="black", border=2, font=('Poppins 12 bold'))
    label_cep.place(x=525, y=115, anchor='nw')

    label_bairro = Label(canvasHud, text='Bairro: ', bg='white', fg="black", border=2, font=('Poppins 12 bold'))
    label_bairro.place(x=525, y=161, anchor='nw')

    label_cidade = Label(canvasHud, text='Cidade: ', bg='white', fg="black", border=2, font=('Poppins 12 bold'))
    label_cidade.place(x=525, y=207, anchor='nw')

    label_observacao = Label(canvasHud, text='Observaçâo: ', bg='white', fg="black", border=2, font=('Poppins 12 bold'))
    label_observacao.place(x=525, y=253, anchor='nw')

    global entry_nome, entry_sobrenome, entry_sexo, entry_datadenascimento, entry_telefone, entry_endereco, entry_cep, entry_bairro, entry_cidade, entry_observacao

    # entrys

    entry_nome = Entry(canvasHud, width=30, border=2, font=('Poppins 10'))
    entry_nome.place(x=230, y=69, anchor='nw')

    entry_sobrenome = Entry(canvasHud, width=30, border=2, font=('Poppins 10'))
    entry_sobrenome.place(x=230, y=115, anchor='nw')

    entry_datadenascimento = Entry(canvasHud, width=30, border=2, font=('Poppins 10'))
    entry_datadenascimento.place(x=230, y=161, anchor='nw')

    entry_telefone = Entry(canvasHud, width=30, border=2, font=('Poppins 10'))
    entry_telefone.place(x=230, y=207, anchor='nw')

    entry_sexo = Entry(canvasHud, width=30, border=2, font=('Poppins 10'))
    entry_sexo.place(x=230, y=253, anchor='nw')

    entry_endereco = Entry(canvasHud, width=30, border=2, font=('Poppins 10'))
    entry_endereco.place(x=661, y=69, anchor='nw')

    entry_cep = Entry(canvasHud, width=30, border=2, font=('Poppins 10'))
    entry_cep.place(x=661, y=115, anchor='nw')

    entry_bairro = Entry(canvasHud, width=30, border=2, font=('Poppins 10'))
    entry_bairro.place(x=661, y=161, anchor='nw')

    entry_cidade = Entry(canvasHud, width=30, border=2, font=('Poppins 10'))
    entry_cidade.place(x=661, y=207, anchor='nw')

    entry_observacao = Entry(canvasHud, width=30, border=2, font=('Poppins 10'))
    entry_observacao.place(x=661, y=253, anchor='nw')

    # botoes
    imgCadastro = PhotoImage(file='b_cadastrar_menuDeCadastro.png')
    botao_cadastar = Button(canvasHud, image=imgCadastro, command=cadastrar_aluno, bg='white', border=0,
                            activebackground='white', cursor='hand2')
    botao_cadastar.place(x=960, y=234, anchor='nw')

    imgDeletar = PhotoImage(file='b_deletar_menuDeCadastro.png')
    botao_deletar = Button(canvasHud, image=imgDeletar,command=excluir_aluno,bg='white', border=0, activebackground='white', cursor='hand2')
    botao_deletar.place(x=960, y=179, anchor='nw')

    imgAlterar = PhotoImage(file='b_alterar_menuDeCadastro.png')
    botao_Alterar = Button(canvasHud, command=atualizar_aluno,image=imgAlterar, bg='white', border=0, activebackground='white', cursor='hand2')
    botao_Alterar.place(x=960, y=124, anchor='nw')

    imgVoltar = PhotoImage(file='b_voltar_menuDeCadastro.png')
    botao_Voltar = Button(canvasHud, image=imgVoltar, bg='white', border=0, activebackground='white', cursor='hand2', command=telaFuncionário)
    botao_Voltar.place(x=960, y=69, anchor='nw')

    # Criar o frame para a tabela
    frame_tabela = Frame(canvasHud2, bg='orange')
    frame_tabela.place(relx=0.5, rely=0.55, anchor='center')

    # Criar a tabela
    tabela = ttk.Treeview(frame_tabela)
    tabela.bind("<<TreeviewSelect>>", editar_aluno)

    # Definir as colunas da tabela
    tabela['columns'] =('Nome', 'Sobrenome', 'Sexo', 'Data de Nascimento', 'Telefone', 'Endereço', 'CEP', 'Bairro', 'Cidade', 'Observação')

    # Formatar as colunas
    tabela.column('#0', width=50, anchor='center')  # Definir a largura da coluna de índice

    for coluna in tabela['columns']:
        tabela.column(coluna, width=100, anchor='center')

    id=tabela.heading('#0', text='ID')

    for coluna in tabela['columns']:
        tabela.heading(coluna, text=coluna)

    # Adicionar a tabela ao frame
    tabela.pack(side='left', fill='both')

    # Adicionar scrollbar à tabela
    scrollbar = ttk.Scrollbar(frame_tabela, orient='vertical', command=tabela.yview)
    scrollbar.pack(side='right', fill='y')
    tabela.configure(yscrollcommand=scrollbar.set)

    # Preencher a tabela com os dados do banco de dados
    preencher_tabela()
    janela.mainloop()
    
#interface do funcionário
def telaFuncionário():
    
    global tela, v
    if tela == 4:
        canvasHud6.destroy()
    elif tela == 5:
        canvasGuia.destroy()
    tela = 3

    v=0
    som()
    
    global canvasHud4

    def telainicial():
        resposta = messagebox.askyesno("Confirmação", "Tem certeza de que deseja fazer logoff?")
        if resposta:
            j0()

    imgCanvas4 = PhotoImage(file='canvas4.png')
    canvasHud4 = Canvas(janela, width=627, height=460, bg='orange', highlightthickness=0)
    canvasHud4.create_image(0, 0, image=imgCanvas4, anchor='nw')
    canvasHud4.place(relx=0.5, rely=0.5, anchor='center')

    imgcadastroaluno = PhotoImage(file='b_acessarBanco.png')
    botaocadastroaluno = Button(canvasHud4, image=imgcadastroaluno, bg='white', border=0, activebackground='white', cursor='hand2', command=telaBancoAlunos)
    botaocadastroaluno.place(x=18.47, y=326.72, anchor='nw')

    imginteracao= PhotoImage(file='b_voltar_menu_de_interações.png')
    botaointeracao = Button(canvasHud4, image=imginteracao, bg='white', border=0, activebackground='white', cursor='hand2', command = interfacePrincipal)
    botaointeracao.place(x=18.47, y=387.97, anchor='nw')

    imglogoff= PhotoImage(file='b_logoff.png')
    botaologoff = Button(canvasHud4, image=imglogoff, bg='white', border=0, activebackground='white', cursor='hand2', command = telainicial)
    botaologoff.place(x=324.72, y=387.97, anchor='nw')

    janela.mainloop()

#tela de autenticação do funcionário logado
def confirmarAcesso():
    
    #checa se a senha do funcionário está certa, indo ou não pra área do funcionário
    def checagem():
        
        som()
        
        inputSenha = entry_senhaconfirmar.get().strip()
        if not inputSenha:
            messagebox.showerror(title='Autikids Confirmação', message='Preencha o campo.')

        else:
        
            conexao = sqlite3.connect('funcionários.db')
            c = conexao.cursor()
        
            c.execute("SELECT * FROM funcionários WHERE apelido=? AND senha=?", (inputApelido, inputSenha))
            res = c.fetchone()
        
        if res is None:
            messagebox.showerror(title='Autikids Confirmação', message=f'Senha incorreta. Tente novamente.')
            entry_senhaconfirmar.delete(0,"end")
        
        else:
            messagebox.showinfo(title='Autikids Confirmação', message=f'Login feito com sucesso. Bem vindo(a), {inputApelido}.')
            telaFuncionário() 
        
    global canvasHud6, tela, v
    v=0
    tela = 4
    
    som()
    canvasGuia.destroy()
    
    imgCanvasHud6 = PhotoImage(file='canvas5.png')
    canvasHud6 = Canvas(janela, width = 481, height = 421, bg='orange', highlightthickness=0)
    canvasHud6.create_image(0, 0, image = imgCanvasHud6, anchor='nw')
    canvasHud6.place(relx=0.5, rely=0.5, anchor='center')
    
    labelTítulo = Label(canvasHud6, text=f'Olá, {inputApelido}! Insira sua senha\nno campo abaixo para prosseguir.', font=('Poppins', 18, 'bold'), fg='orange', bg='white', anchor='w', justify='left')
    labelTítulo.place(relx=0.5, rely=0.58, anchor='center')
    
    labelSenha = Label(canvasHud6, text="Sua senha:", font=('Poppins', 12, 'bold'), bg='white', fg='orange')
    labelSenha.place(relx=0.065, rely=0.75, anchor='w')
    
    entry_senhaconfirmar = Entry(canvasHud6, border=2, font=('Poppins 12'), show='*', width=30)
    entry_senhaconfirmar.place(relx=0.3, rely=0.75, anchor='w')
    
    botãoVoltar = Button(canvasHud6, command = interfacePrincipal, border=2, width=10, activebackground='#fdd42a', cursor='hand2', text='Voltar', font=('Poppins 12 bold'))
    botãoVoltar.place(relx=0.065, rely=0.88, anchor='w')
    
    botão_confirmarsenha = Button(canvasHud6, width=30, command = checagem, text='Confirmar acesso', font=('Poppins 12 bold'), border=2, cursor='hand2', activebackground='#fdd42a')
    botão_confirmarsenha.place(relx=0.3, rely=0.88, anchor='w')
    
    janela.mainloop()
    
#janela e função pra cadastrar criança, fica dentro da área do funcionário
def NovoCadastro():

    def cadastrar_aluno():

        som()

        conexao = sqlite3.connect('banco_alunos2.db')
        cursor=conexao.cursor()
        cursor.execute("INSERT INTO alunos VALUES(:nome,:sobrenome,:telefone,:datadenascimento,:endereco,:cep,:bairro)",
            {
                    'nome':entry_nomeAluno.get(),
                    'sobrenome':entry_sobrenome.get(),
                    'telefone':entry_telefone.get(),
                    'datadenascimento':entry_datadenascimento.get(),
                    'endereco':entry_endereco.get(),
                    'cep':entry_cep.get(),
                    'bairro':entry_bairro.get(),
            })

        conexao.commit()
        conexao.close()
            
        entry_nomeAluno.delete(0,"end")
        entry_sobrenome.delete(0, "end")
        entry_telefone.delete(0, "end")
        entry_datadenascimento.delete(0,"end")
        entry_endereco.delete(0, "end")
        entry_cep.delete(0,"end")
        entry_bairro.delete(0,"end")

    som()
    
    global entry_nomeAluno
    global entry_sobrenome
    global entry_telefone
    global entry_datadenascimento
    global entry_endereco
    global entry_cep
    global entry_bairro

    label_titulo = Label(janela, text='Cadastro de aluno')
    label_titulo.configure(font=('Poppins', 20, 'bold'), bg='orange', fg='white')
    label_titulo.grid(row=0, column=1, columnspan=1)

    label_nome= Label(janela, text='Nome: ',bg='orange',fg="black",border=2, font=('Poppins 12 bold'))
    label_nome.grid(row=1, column=0, padx=10, pady=10, sticky='e')

    label_sobrenome= Label(janela, text='Sobrenome: ',bg='orange',fg="black",border=2, font=('Poppins 12 bold'))
    label_sobrenome.grid(row=2, column=0, padx=10, pady=10, sticky='e')

    label_telefone= Label(janela, text='Telefone: ',bg='orange',fg="black",border=2, font=('Poppins 12 bold'))
    label_telefone.grid(row=3, column=0, padx=10, pady=10, sticky='e')

    label_datadenascimento= Label(janela,text='Data de Nascimento: ',bg='orange',fg='black',border=2, font=('Poppins 12 bold'))
    label_datadenascimento.grid(row=4,column=0,padx=10,pady=10, sticky='e')

    label_endereco= Label(janela, text='Endereço: ',bg='orange',fg="black",border=2, font=('Poppins 12 bold'))
    label_endereco.grid(row=5, column=0, padx=10, pady=10, sticky='e')

    label_cep= Label(janela, text='CEP: ',bg='orange',fg="black",border=2, font=('Poppins 12 bold'))
    label_cep.grid(row=6, column=0, padx=10, pady=10, sticky='e')

    label_bairro= Label(janela, text='Bairro: ',bg='orange',fg="black",border=2, font=('Poppins 12 bold'))
    label_bairro.grid(row=7, column=0, padx=10, pady=10, sticky='e')

    # Entrys:
            
    entry_nomeAluno= Entry(janela, width=30, border=2, font=('Poppins 12'))
    entry_nomeAluno.grid(row=1, column=1, pady=10)

    entry_sobrenome= Entry(janela,width=30, border=2, font=('Poppins 12'))
    entry_sobrenome.grid(row=2, column=1, pady=10)

    entry_telefone= Entry(janela,width=30, border=2, font=('Poppins 12'))
    entry_telefone.grid(row=3, column=1, pady=10)

    entry_datadenascimento= Entry(janela,width=30, border=2, font=('Poppins 12'))
    entry_datadenascimento.grid(row=4,column=1,pady=10)

    entry_endereco= Entry(janela,width=30, border=2, font=('Poppins 12'))
    entry_endereco.grid(row=5, column=1, pady=10)

    entry_cep= Entry(janela,width=30, border=2, font=('Poppins 12'))
    entry_cep.grid(row=6, column=1, pady=10)

    entry_bairro= Entry(janela,width=30, border=2, font=('Poppins 12'))
    entry_bairro.grid(row=7, column=1, pady=10)

    # Botoes:
    botao_cadastar= Button(janela,text="Cadastrar Aluno", command = cadastrar_aluno, border=2, font=('Poppins 12 bold'), activebackground='yellow', cursor='hand2')
    botao_cadastar.grid(row=8,column=1,pady=10, sticky='nswe')

    janela.wm_minsize(width = 800, height = 600)
    janela.mainloop()

#janela usada pela criança
def interfacePrincipal():
    
    global canvasInterno0, canvasInterno1, canvasInterno2, canvasInterno3, canvasInterno4, canvasInterno0_1, canvasGuia
    global Querer
    global selecionado
    global canvas
    
    def QR():
        som()
        falamenu('QR.mp3')
        global Querer
        Querer = True
        alterarBotõesQuerer()
    
    def NQR():
        som()
        falamenu('NQR.mp3')
        global Querer
        Querer = False
        alterarBotõesQuerer()
    
    def alterarBotõesQuerer():
        global imgb_Quero
        global imgb_NQuero
        
        imgb_Quero = imgBQR()
        b_Quero.configure(image=imgb_Quero)
        
        imgb_NQuero = imgBNQR()
        b_NQuero.configure(image=imgb_NQuero)
        
    def S0():

        global selecionado, canvas, v
        global canvasInterno0, canvasInterno1, canvasInterno2, canvasInterno3, canvasInterno4
        selecionado = 0
        if v == 0:
            v+=1
        else:
            falamenu('S0.mp3')
        alterarBotõesCategorias()

        if canvas == 1:
            canvasInterno1.destroy()
        elif canvas == 2:
            canvasInterno2.destroy()
        elif canvas == 3:
            canvasInterno3.destroy()
        elif canvas == 4:
            canvasInterno4.destroy()
        canvas = 0

        def menu0_1():
            
            som()
            
            global canvasInterno0, canvasInterno0_1
            
            canvasInterno0.destroy()
            
            canvasInterno0_1 = Canvas(canvasHud7, width=980, height=500, bg='#fdd42a', highlightthickness=0)
            canvasInterno0_1.place(relx=0.5, rely=0.5, anchor='center')

            Botão = Button(canvasInterno0_1, image=imgFrutas, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('fruta.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=64, anchor='nw')
            Botão = Button(canvasInterno0_1, image=imgSuco, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('suco.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=64, anchor='nw')
            Botão = Button(canvasInterno0_1, image=imgPão, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('pão.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=64, anchor='nw')
            Botão = Button(canvasInterno0_1, image=imgLeite, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('leite.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=64, anchor='nw')
            Botão = Button(canvasInterno0_1, image=imgLanche, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('lanche.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=64, anchor='nw')
            Botão = Button(canvasInterno0_1, image=imgBiscoito, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('biscoito.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=263, anchor='nw')
            Botão = Button(canvasInterno0_1, image=imgChocolate, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('chocolate.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=263, anchor='nw')
            Botão = Button(canvasInterno0_1, image=imgBatataF, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('batataF.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=263, anchor='nw')
            Botão = Button(canvasInterno0_1, image=imgPipoca, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('pipoca.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=263, anchor='nw')
            Botão = Button(canvasInterno0_1, image=imgSorvete, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('sorvete.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=263, anchor='nw')
            
            bCima = Button(canvasInterno0_1, image=imgbCima, border=0, command=menu0_0, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bCima.place(x=471, y=10, anchor='nw')

        def menu0_0():
            
            global canvasInterno0, canvasInterno0_1
            som()
            
            try:
                canvasInterno0_1.destroy()
            except Exception:
                pass

            canvasInterno0 = Canvas(canvasHud7, width=980, height=500, bg='#fdd42a', highlightthickness=0)
            canvasInterno0.place(relx=0.5, rely=0.5, anchor='center')

            Botão = Button(canvasInterno0, image=imgComer, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('comer.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=64, anchor='nw')
            Botão = Button(canvasInterno0, image=imgAlmoçar, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('almoçar.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=64, anchor='nw')
            Botão = Button(canvasInterno0, image=imgJantar, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('jantar.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=64, anchor='nw')
            Botão = Button(canvasInterno0, image=imgÁgua, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('água.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=64, anchor='nw')
            Botão = Button(canvasInterno0, image=imgCaféDaManhã, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('caféDM.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=64, anchor='nw')
            Botão = Button(canvasInterno0, image=imgArroz, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('arroz.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=263, anchor='nw')
            Botão = Button(canvasInterno0, image=imgFeijão, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('feijão.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=263, anchor='nw')
            Botão = Button(canvasInterno0, image=imgCarne, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('carne.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=263, anchor='nw')
            Botão = Button(canvasInterno0, image=imgSalada, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('salada.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=263, anchor='nw')
            Botão = Button(canvasInterno0, image=imgMacarrão, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('macarrão.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=263, anchor='nw')
            
            bBaixo = Button(canvasInterno0, image=imgbBaixo, border=0, command=menu0_1, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bBaixo.place(x=471, y=453, anchor='nw')
        
        menu0_0()
        
    def S1():
        
        falamenu('S1.mp3')
        global selecionado, canvas
        global canvasInterno0, canvasInterno1, canvasInterno2, canvasInterno3, canvasInterno4
        selecionado = 1
        alterarBotõesCategorias()
        
        if canvas == 0:
            canvasInterno0.destroy()
        if canvas == 2:
            canvasInterno2.destroy()
        if canvas == 3:
            canvasInterno3.destroy()
        if canvas == 4:
            canvasInterno4.destroy()
        canvas = 1
        
        def menu1_3():
            
            som()
            global canvasInterno1, canvasInterno1_1, canvasInterno1_2, canvasInterno1_3
            
            canvasInterno1_2.destroy()
            
            canvasInterno1_3 = Canvas(canvasHud7, width=980, height=500, bg='#fdd42a', highlightthickness=0)
            canvasInterno1_3.place(relx=0.5, rely=0.5, anchor='center')

            Botão = Button(canvasInterno1_3, image=imgBanho, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('banho.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=64, anchor='nw')
            Botão = Button(canvasInterno1_3, image=imgXixi, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('xixi.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=64, anchor='nw')
            Botão = Button(canvasInterno1_3, image=imgCocô, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('cocô.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=64, anchor='nw')
            Botão = Button(canvasInterno1_3, image=imgFicar, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('ficar.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=64, anchor='nw')
            Botão = Button(canvasInterno1_3, image=imgSair, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('sair.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=64, anchor='nw')

            bCima = Button(canvasInterno1_3, image=imgbCima, border=0, command=menu1_2, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bCima.place(x=471, y=10, anchor='nw')
        
        def menu1_2():
            
            som()
            global canvasInterno1, canvasInterno1_1, canvasInterno1_2, canvasInterno1_3
            
            try:
                canvasInterno1_1.destroy()
            except Exception:
                pass
            
            try:
                canvasInterno1_3.destroy()
            except Exception:
                pass
            
            canvasInterno1_2 = Canvas(canvasHud7, width=980, height=500, bg='#fdd42a', highlightthickness=0)
            canvasInterno1_2.place(relx=0.5, rely=0.5, anchor='center')

            Botão = Button(canvasInterno1_2, image=imgAtéMais, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('até+.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=64, anchor='nw')
            Botão = Button(canvasInterno1_2, image=imgBdia, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('bdia.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=64, anchor='nw')
            Botão = Button(canvasInterno1_2, image=imgBtarde, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('btarde.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=64, anchor='nw')
            Botão = Button(canvasInterno1_2, image=imgBnoite, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('bnoite.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=64, anchor='nw')
            Botão = Button(canvasInterno1_2, image=imgBem, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('tobem.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=64, anchor='nw')
            Botão = Button(canvasInterno1_2, image=imgCansada, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('tocansada.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=263, anchor='nw')
            Botão = Button(canvasInterno1_2, image=imgTriste, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('totriste.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=263, anchor='nw')
            Botão = Button(canvasInterno1_2, image=imgComo, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('como.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=263, anchor='nw')
            Botão = Button(canvasInterno1_2, image=imgVc, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('evc.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=263, anchor='nw')
            Botão = Button(canvasInterno1_2, image=imgLmão, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('lavarMão.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=263, anchor='nw')

            bCima = Button(canvasInterno1_2, image=imgbCima, border=0, command=menu1_1, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bCima.place(x=471, y=10, anchor='nw')
            
            bBaixo = Button(canvasInterno1_2, image=imgbBaixo, border=0, command=menu1_3, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bBaixo.place(x=471, y=453, anchor='nw')
        
        def menu1_1():
            
            som()
            
            global canvasInterno1, canvasInterno1_1, canvasInterno1_2, canvasInterno1_3
            
            try:
                canvasInterno1.destroy()
            except Exception:
                pass
            
            try:
                canvasInterno1_2.destroy()
            except Exception:
                pass
            
            canvasInterno1_1 = Canvas(canvasHud7, width=980, height=500, bg='#fdd42a', highlightthickness=0)
            canvasInterno1_1.place(relx=0.5, rely=0.5, anchor='center')

            Botão = Button(canvasInterno1_1, image=imgEntendi, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('tendi.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=64, anchor='nw')
            Botão = Button(canvasInterno1_1, image=imgNentendi, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('Nentendi.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=64, anchor='nw')
            Botão = Button(canvasInterno1_1, image=imgMtGnt, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('gente.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=64, anchor='nw')
            Botão = Button(canvasInterno1_1, image=imgBarulho, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('barulho.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=64, anchor='nw')
            Botão = Button(canvasInterno1_1, image=imgSilêncio, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('sh.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=64, anchor='nw')
            Botão = Button(canvasInterno1_1, image=imgFeliz, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('tofeliz.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=263, anchor='nw')
            Botão = Button(canvasInterno1_1, image=imgDor, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('comdor.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=263, anchor='nw')
            Botão = Button(canvasInterno1_1, image=imgMedo, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('commedo.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=263, anchor='nw')
            Botão = Button(canvasInterno1_1, image=imgFrio, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('comfrio.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=263, anchor='nw')
            Botão = Button(canvasInterno1_1, image=imgCalor, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('comcalor.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=263, anchor='nw')

            bCima = Button(canvasInterno1_1, image=imgbCima, border=0, command=menu1_0, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bCima.place(x=471, y=10, anchor='nw')
            
            bBaixo = Button(canvasInterno1_1, image=imgbBaixo, border=0, command=menu1_2, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bBaixo.place(x=471, y=453, anchor='nw')

        def menu1_0():
            
            som()
            global canvasInterno1, canvasInterno1_1, canvasInterno1_2, canvasInterno1_3
            
            try:
                canvasInterno1_1.destroy()
            except Exception:
                pass

            canvasInterno1 = Canvas(canvasHud7, width=980, height=500, bg='#fdd42a', highlightthickness=0)
            canvasInterno1.place(relx=0.5, rely=0.5, anchor='center')

            Botão = Button(canvasInterno1, image=imgAjd, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('ajd.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=64, anchor='nw')
            Botão = Button(canvasInterno1, image=imgSim, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('s.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=64, anchor='nw')
            Botão = Button(canvasInterno1, image=imgN, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('n.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=64, anchor='nw')
            Botão = Button(canvasInterno1, image=imgPare, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('pare.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=64, anchor='nw')
            Botão = Button(canvasInterno1, image=imgObg, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('obg.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=64, anchor='nw')
            Botão = Button(canvasInterno1, image=imgPf, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('pf.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=263, anchor='nw')
            Botão = Button(canvasInterno1, image=imgAonde, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('aonde.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=263, anchor='nw')
            Botão = Button(canvasInterno1, image=imgQnd, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('qnd.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=263, anchor='nw')
            Botão = Button(canvasInterno1, image=imgGostei, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('gostei.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=263, anchor='nw')
            Botão = Button(canvasInterno1, image=imgNgostei, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala0('ngostei.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=263, anchor='nw')
            
            bBaixo = Button(canvasInterno1, image=imgbBaixo, border=0, command=menu1_1, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bBaixo.place(x=471, y=453, anchor='nw')
        
        menu1_0()
        
    def S2():
        
        falamenu('S2.mp3')
        global selecionado, canvas
        global canvasInterno0, canvasInterno1, canvasInterno2, canvasInterno3, canvasInterno4
        selecionado = 2
        alterarBotõesCategorias()
        
        if canvas == 0:
            canvasInterno0.destroy()
        if canvas == 1:
            canvasInterno1.destroy()
        if canvas == 3:
            canvasInterno3.destroy()
        if canvas == 4:
            canvasInterno4.destroy()
        canvas = 2

        def menu2_1():
            
            som()
            
            global canvasInterno2, canvasInterno2_1
            
            canvasInterno2.destroy()
            
            canvasInterno2_1 = Canvas(canvasHud7, width=980, height=500, bg='#fdd42a', highlightthickness=0)
            canvasInterno2_1.place(relx=0.5, rely=0.5, anchor='center')

            Botão = Button(canvasInterno2_1, image=imgCasa, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('casa.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=64, anchor='nw')
            Botão = Button(canvasInterno2_1, image=imgcVovô, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('vô.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=64, anchor='nw')
            Botão = Button(canvasInterno2_1, image=imgcVovó, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('vó.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=64, anchor='nw')
            Botão = Button(canvasInterno2_1, image=imgcTitio, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('tio.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=64, anchor='nw')
            Botão = Button(canvasInterno2_1, image=imgcTitia, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('tia.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=64, anchor='nw')
            Botão = Button(canvasInterno2_1, image=imgQuarto, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('quarto.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=263, anchor='nw')
            Botão = Button(canvasInterno2_1, image=imgPraia, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('praia.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=263, anchor='nw')
            Botão = Button(canvasInterno2_1, image=imgIgreja, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('igreja.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=263, anchor='nw')
            Botão = Button(canvasInterno2_1, image=imgEstádio, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('jogo.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=263, anchor='nw')
            Botão = Button(canvasInterno2_1, image=imgCozinha, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('cozinha.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=263, anchor='nw')
            
            bCima = Button(canvasInterno2_1, image=imgbCima, border=0, command=menu2_0, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bCima.place(x=471, y=10, anchor='nw')

        def menu2_0():
            
            som()
            global canvasInterno2, canvasInterno2_1
            
            try:
                canvasInterno2_1.destroy()
            except Exception:
                pass

            canvasInterno2 = Canvas(canvasHud7, width=980, height=500, bg='#fdd42a', highlightthickness=0)
            canvasInterno2.place(relx=0.5, rely=0.5, anchor='center')

            Botão = Button(canvasInterno2, image=imgIr, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('ir.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=64, anchor='nw')
            Botão = Button(canvasInterno2, image=imgIrComVocê, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('você.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=64, anchor='nw')
            Botão = Button(canvasInterno2, image=imgEscola, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('escola.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=64, anchor='nw')
            Botão = Button(canvasInterno2, image=imgMédico, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('médico.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=64, anchor='nw')
            Botão = Button(canvasInterno2, image=imgParquinho, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('parquinho.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=64, anchor='nw')
            Botão = Button(canvasInterno2, image=imgPiscina, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('piscina.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=263, anchor='nw')
            Botão = Button(canvasInterno2, image=imgPraça, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('praça.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=263, anchor='nw')
            Botão = Button(canvasInterno2, image=imgCinema, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('cinema.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=263, anchor='nw')
            Botão = Button(canvasInterno2, image=imgSorveteria, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('sorveteria.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=263, anchor='nw')
            Botão = Button(canvasInterno2, image=imgShopping, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('shopping.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=263, anchor='nw')
            
            bBaixo = Button(canvasInterno2, image=imgbBaixo, border=0, command=menu2_1, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bBaixo.place(x=471, y=453, anchor='nw')
        
        menu2_0()
        
    def S3():
        
        falamenu('S3.mp3')
        global selecionado, canvas, canvasInterno0, canvasInterno1, canvasInterno2, canvasInterno3, canvasInterno4
        selecionado = 3
        alterarBotõesCategorias()
        
        if canvas == 0:
            canvasInterno0.destroy()
        if canvas == 1:
            canvasInterno1.destroy()
        if canvas == 2:
            canvasInterno2.destroy()
        if canvas == 4:
            canvasInterno4.destroy()
        canvas = 3
        
        def menu3_1():
            
            som()
            
            global canvasInterno3, canvasInterno3_1
            
            canvasInterno3.destroy()
            
            canvasInterno3_1 = Canvas(canvasHud7, width=980, height=500, bg='#fdd42a', highlightthickness=0)
            canvasInterno3_1.place(relx=0.5, rely=0.5, anchor='center')

            Botão = Button(canvasInterno3_1, image=imgVovô, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('fvô.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=64, anchor='nw')
            Botão = Button(canvasInterno3_1, image=imgVovó, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('fvó.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=64, anchor='nw')
            Botão = Button(canvasInterno3_1, image=imgIrmão, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('firmão.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=64, anchor='nw')
            Botão = Button(canvasInterno3_1, image=imgIrmã, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('firmã.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=64, anchor='nw')

            bCima = Button(canvasInterno3_1, image=imgbCima, border=0, command=menu3_0, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bCima.place(x=471, y=10, anchor='nw')

        def menu3_0():
            
            global canvasInterno3, canvasInterno3_1
            som()
            
            try:
                canvasInterno3_1.destroy()
            except Exception:
                pass

            canvasInterno3 = Canvas(canvasHud7, width=980, height=500, bg='#fdd42a', highlightthickness=0)
            canvasInterno3.place(relx=0.5, rely=0.5, anchor='center')

            Botão = Button(canvasInterno3, image=imgEle, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('fele.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=64, anchor='nw')
            Botão = Button(canvasInterno3, image=imgEla, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('fela.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=64, anchor='nw')
            Botão = Button(canvasInterno3, image=imgCozinheira, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('fcozinheira.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=64, anchor='nw')
            Botão = Button(canvasInterno3, image=imgProfessora, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('fprof.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=64, anchor='nw')
            Botão = Button(canvasInterno3, image=imgFisio, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('fisio.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=64, anchor='nw')
            Botão = Button(canvasInterno3, image=imgDiretora, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('fdiretora.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=263, anchor='nw')
            Botão = Button(canvasInterno3, image=imgPapai, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('fpai.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=263, anchor='nw')
            Botão = Button(canvasInterno3, image=imgMamãe, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('fmãe.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=263, anchor='nw')
            Botão = Button(canvasInterno3, image=imgTitio, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('ftio.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=263, anchor='nw')
            Botão = Button(canvasInterno3, image=imgTitia, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('ftia.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=263, anchor='nw')
            
            bBaixo = Button(canvasInterno3, image=imgbBaixo, border=0, command=menu3_1, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bBaixo.place(x=471, y=453, anchor='nw')
        
        menu3_0()
        
    def S4():

        falamenu('S4.mp3')
        global selecionado, canvas, canvasInterno0, scrollbar
        global canvasInterno0, canvasInterno1, canvasInterno2, canvasInterno3, canvasInterno4
        selecionado = 4
        alterarBotõesCategorias()
        
        if canvas == 0:
            canvasInterno0.destroy()
        if canvas == 1:
            canvasInterno1.destroy()
        if canvas == 2:
            canvasInterno2.destroy()
        if canvas == 3:
            canvasInterno3.destroy()
        
        canvas = 4
        
        def menu4_1():
            
            som()
            
            global canvasInterno4, canvasInterno4_1
            
            canvasInterno4.destroy()
            
            canvasInterno4_1 = Canvas(canvasHud7, width=980, height=500, bg='#fdd42a', highlightthickness=0)
            canvasInterno4_1.place(relx=0.5, rely=0.5, anchor='center')

            Botão = Button(canvasInterno4_1, image=imgBoneca, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('boneca.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=64, anchor='nw')
            Botão = Button(canvasInterno4_1, image=imgUrsinho, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('ursinho.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=64, anchor='nw')
            Botão = Button(canvasInterno4_1, image=imgCarrinho, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('carrinho.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=64, anchor='nw')
            Botão = Button(canvasInterno4_1, image=imgBola, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('bola.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=64, anchor='nw')
            Botão = Button(canvasInterno4_1, image=imgVideogame, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('videogame.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=64, anchor='nw')
            Botão = Button(canvasInterno4_1, image=imgTv, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('tv.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=263, anchor='nw')
            Botão = Button(canvasInterno4_1, image=imgTablet, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('tablet.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=263, anchor='nw')
            Botão = Button(canvasInterno4_1, image=imgCelular, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('celular.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=263, anchor='nw')

            bCima = Button(canvasInterno4_1, image=imgbCima, border=0, command=menu4_0, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bCima.place(x=471, y=10, anchor='nw')

        def menu4_0():
            
            som()
            global canvasInterno4, canvasInterno4_1
            
            try:
                canvasInterno4_1.destroy()
            except Exception:
                pass

            canvasInterno4 = Canvas(canvasHud7, width=980, height=500, bg='#fdd42a', highlightthickness=0)
            canvasInterno4.place(relx=0.5, rely=0.5, anchor='center')

            Botão = Button(canvasInterno4, image=imgBrincar, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('brincar.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=64, anchor='nw')
            Botão = Button(canvasInterno4, image=imgPuzzle, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('quebra.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=64, anchor='nw')
            Botão = Button(canvasInterno4, image=imgDesenhar, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('desenhar.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=64, anchor='nw')
            Botão = Button(canvasInterno4, image=imgPintar, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('pintar.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=64, anchor='nw')
            Botão = Button(canvasInterno4, image=imgMúsica, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('música.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=64, anchor='nw')
            Botão = Button(canvasInterno4, image=imgLivro, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('livro.mp3'), cursor='hand2', border=0)
            Botão.place(x=0, y=263, anchor='nw')
            Botão = Button(canvasInterno4, image=imgGibi, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('gibi.mp3'), cursor='hand2', border=0)
            Botão.place(x=200, y=263, anchor='nw')
            Botão = Button(canvasInterno4, image=imgDançar, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('dançar.mp3'), cursor='hand2', border=0)
            Botão.place(x=400, y=263, anchor='nw')
            Botão = Button(canvasInterno4, image=imgFora, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('fora.mp3'), cursor='hand2', border=0)
            Botão.place(x=600, y=263, anchor='nw')
            Botão = Button(canvasInterno4, image=imgBicicleta, activebackground='#fdd42a', bg='#fdd42a', command=lambda: fala('bicicleta.mp3'), cursor='hand2', border=0)
            Botão.place(x=800, y=263, anchor='nw')
                        
            bBaixo = Button(canvasInterno4, image=imgbBaixo, border=0, command=menu4_1, bg='#fdd42a', activebackground='#fdd42a', cursor='hand2')
            bBaixo.place(x=471, y=453, anchor='nw')
        
        menu4_0()
    
    def alterarBotõesCategorias():
        
        global imgb_Alimentos
        global imgb_Interações
        global imgb_Lugares
        global imgb_Pessoas
        global imgb_Brinquedos
        
        imgb_Alimentos = imgbALIMENTOS()
        b_Alimentos.configure(image=imgb_Alimentos)
        
        imgb_Interações = imgbINTERAÇÕES()
        b_Interações.configure(image=imgb_Interações)
        
        imgb_Lugares = imgbLUGARES()
        b_Lugares.configure(image=imgb_Lugares)
        
        imgb_Pessoas = imgbPESSOAS()
        b_Pessoas.configure(image=imgb_Pessoas)
        
        imgb_Brinquedos = imgbBRINQUEDOS()
        b_Brinquedos.configure(image=imgb_Brinquedos)
    
    def imgBQR():
        if Querer:
            imgb_Quero = PhotoImage(file='b_Quero_ON.png')
        else:
            imgb_Quero = PhotoImage(file='b_Quero_OFF.png')
        return imgb_Quero
        
    def imgBNQR():
        if not Querer:
            imgb_NQuero = PhotoImage(file='b_nãoQuero_ON.png')
        else:
            imgb_NQuero = PhotoImage(file='b_nãoQuero_OFF.png')
        return imgb_NQuero
    
    def imgbALIMENTOS():
        global selecionado
        if selecionado == 0:
            imgb_Alimentos = PhotoImage(file='b_alimentos_on.png')
        else:
            imgb_Alimentos = PhotoImage(file='b_alimentos_off.png')
        return imgb_Alimentos
    
    def imgbINTERAÇÕES():
        if selecionado == 1:
            imgb_Interações = PhotoImage(file='b_interações_on.png')
        else:
            imgb_Interações = PhotoImage(file='b_interações_off.png')
        return imgb_Interações
    
    def imgbLUGARES():
        if selecionado == 2:
            imgb_Lugares = PhotoImage(file='b_lugares_on.png')
        else:
            imgb_Lugares = PhotoImage(file='b_lugares_off.png')
        return imgb_Lugares
    
    def imgbPESSOAS():
        if selecionado == 3:
            imgb_Pessoas = PhotoImage(file='b_pessoas_on.png')
        else:
            imgb_Pessoas = PhotoImage(file='b_pessoas_off.png')
        return imgb_Pessoas
    
    def imgbBRINQUEDOS():
        if selecionado == 4:
            imgb_Brinquedos = PhotoImage(file='b_brinquedos_on.png')
        else:
            imgb_Brinquedos = PhotoImage(file='b_brinquedos_off.png')
        return imgb_Brinquedos
    
    if tela == 4:
        canvasHud6.destroy()
    elif tela == 3:
        canvasHud4.destroy()
    else:
        canvasHud1.destroy()
    
    canvas = 0
    canvasGuia = Canvas(janela, width=1366, height=768, bg='orange', highlightthickness=0)
    canvasGuia.place(relx=0.5, rely=0.5, anchor='center')
    
    imgCanvas7 = PhotoImage(file='canvas7.png')
    canvasHud7 = Canvas(canvasGuia, width=1022, height=530, bg='orange', highlightthickness=0)
    canvasHud7.create_image(0, 0, image=imgCanvas7, anchor='nw')
    canvasHud7.place(x=305, y=186, anchor='nw')
    
    imgb_ÁreaDoFuncionário = PhotoImage(file='b_ÁreaDoFuncionário.png')
    b_ÁreaDoFuncionário = Button(canvasGuia, image=imgb_ÁreaDoFuncionário, width=197, height=29, bg='#fdd42a', activebackground='#fdd42a', border=0, cursor='hand2', command=confirmarAcesso)
    b_ÁreaDoFuncionário.place(x=1105, y=660, anchor='nw')

    imgb_Quero = imgBQR()
    b_Quero = Button(canvasGuia, image=imgb_Quero, width=239, height=327, border=0, highlightthickness=0, activebackground='orange', bg='orange', cursor='hand2', command=QR)
    b_Quero.image = imgb_Quero
    b_Quero.place(x=48, y=62, anchor='nw')
    
    imgb_NQuero = imgBNQR()
    b_NQuero = Button(canvasGuia, image=imgb_NQuero, width=239, height=327, border=0, highlightthickness=0, activebackground='orange', bg='orange', cursor='hand2', command=NQR)
    b_NQuero.image = imgb_NQuero
    b_NQuero.place(x=48, y=388, anchor='nw')

    imgb_Alimentos = imgbALIMENTOS()
    b_Alimentos = Button(canvasGuia, image=imgb_Alimentos, width=194, height=133, border=0, highlightthickness=0, activebackground='orange', bg='orange', cursor='hand2', command=S0)
    b_Alimentos.image = imgb_Alimentos
    b_Alimentos.place(x=305, y=62, anchor='nw')
    
    imgb_Interações = imgbINTERAÇÕES()
    b_Interações = Button(canvasGuia, image=imgb_Interações, width=194, height=133, border=0, highlightthickness=0, activebackground='orange', bg='orange', cursor='hand2', command=S1)
    b_Interações.image = imgb_Interações
    b_Interações.place(x=512, y=62, anchor='nw')

    imgb_Lugares = imgbLUGARES()
    b_Lugares = Button(canvasGuia, image=imgb_Lugares, width=194, height=133, border=0, highlightthickness=0, activebackground='orange', bg='orange', cursor='hand2', command=S2)
    b_Lugares.image = imgb_Lugares
    b_Lugares.place(x=719, y=62, anchor='nw')
    
    imgb_Pessoas = imgbPESSOAS()
    b_Pessoas = Button(canvasGuia, image=imgb_Pessoas, width=194, height=133, border=0, highlightthickness=0, activebackground='orange', bg='orange', cursor='hand2', command=S3)
    b_Pessoas.image = imgb_Pessoas
    b_Pessoas.place(x=926, y=62, anchor='nw')
    
    imgb_Brinquedos = imgbBRINQUEDOS()
    b_Brinquedos = Button(canvasGuia, image=imgb_Brinquedos, width=194, height=133, border=0, highlightthickness=0, activebackground='orange', bg='orange', cursor='hand2', command=S4)
    b_Brinquedos.image = imgb_Brinquedos
    b_Brinquedos.place(x=1133, y=62, anchor='nw')
       
    imgbBaixo = PhotoImage(file='setaBaixo.png')
    imgbCima = PhotoImage(file='setaCima.png')
    
    #S0 alimentos pg1
    imgComer = PhotoImage(file='S0_comer.png')
    imgAlmoçar = PhotoImage(file='S0_almoçar.png')
    imgJantar = PhotoImage(file='S0_jantar.png')
    imgÁgua = PhotoImage(file='S0_água.png')
    imgCaféDaManhã = PhotoImage(file='S0_caféDaManhã.png')
    
    imgArroz = PhotoImage(file='S0_arroz.png')
    imgFeijão = PhotoImage(file='S0_feijão.png')
    imgCarne = PhotoImage(file='S0_carne.png')
    imgSalada = PhotoImage(file='S0_salada.png')
    imgMacarrão = PhotoImage(file='S0_macarrão.png')
    
    #S0 alimentos pg2
    imgFrutas = PhotoImage(file='S0_frutas.png')
    imgSuco = PhotoImage(file='S0_suco.png')
    imgPão = PhotoImage(file='S0_pão.png')
    imgLeite = PhotoImage(file='S0_leite.png')
    imgLanche = PhotoImage(file='S0_lanche.png')
    
    imgBiscoito = PhotoImage(file='S0_biscoito.png')
    imgChocolate = PhotoImage(file='S0_chocolate.png')
    imgBatataF = PhotoImage(file='S0_batataF.png')
    imgPipoca = PhotoImage(file='S0_pipoca.png')
    imgSorvete = PhotoImage(file='S0_sorvete.png')

    #S1 necessidades pg1
    imgAjd = PhotoImage(file='S1_ajuda.png')
    imgSim = PhotoImage(file='S1_sim.png')
    imgN = PhotoImage(file='S1_não.png')
    imgPare = PhotoImage(file='S1_pare.png')
    imgObg = PhotoImage(file='S1_obg.png')
    
    imgPf = PhotoImage(file='S1_pf.png')
    imgAonde = PhotoImage(file='S1_aonde.png')
    imgQnd = PhotoImage(file='S1_qnd.png')
    imgGostei = PhotoImage(file='S1_gostei.png')
    imgNgostei = PhotoImage(file='S1_Ngostei.png')

    #S1 necessidades pg2
    imgEntendi = PhotoImage(file='S1_entendi.png')
    imgNentendi = PhotoImage(file='S1_Nentendi.png')
    imgMtGnt = PhotoImage(file='S1_muitaGnt.png')
    imgBarulho = PhotoImage(file='S1_barulho.png')
    imgSilêncio = PhotoImage(file='S1_silêncio.png')
    
    imgFeliz = PhotoImage(file='S1_feliz.png')
    imgDor = PhotoImage(file='S1_dor.png')
    imgMedo = PhotoImage(file='S1_medo.png')
    imgFrio = PhotoImage(file='S1_frio.png')
    imgCalor = PhotoImage(file='S1_calor.png')

    #S1 necessidades pg3
    imgAtéMais = PhotoImage(file='S1_atéMais.png')
    imgBdia = PhotoImage(file='S1_bomdia.png')
    imgBtarde = PhotoImage(file='S1_boatarde.png')
    imgBnoite = PhotoImage(file='S1_boanoite.png')
    imgBem = PhotoImage(file='S1_bem.png')
    
    imgCansada = PhotoImage(file='S1_cansada.png')
    imgTriste = PhotoImage(file='S1_triste.png')
    imgComo = PhotoImage(file='S1_como.png')
    imgVc = PhotoImage(file='S1_você.png')
    imgLmão = PhotoImage(file='S1_lavarMão.png')

    #S1 necessidades pg4
    imgBanho = PhotoImage(file='S1_banho.png')
    imgXixi = PhotoImage(file='S1_xixi.png')
    imgCocô = PhotoImage(file='S1_cocô.png')
    imgFicar = PhotoImage(file='S1_ficar.png')
    imgSair = PhotoImage(file='S1_sair.png')

    #S2 lugares pg1
    imgIr = PhotoImage(file='S2_ir.png')
    imgIrComVocê = PhotoImage(file='S2_irComVocê.png')
    imgEscola = PhotoImage(file='S2_escola.png')
    imgMédico = PhotoImage(file='S2_médico.png')
    imgParquinho = PhotoImage(file='S2_parquinho.png')
    
    imgPiscina = PhotoImage(file='S2_piscina.png')
    imgPraça = PhotoImage(file='S2_praça.png')
    imgCinema = PhotoImage(file='S2_cinema.png')
    imgSorveteria = PhotoImage(file='S2_sorveteria.png')
    imgShopping = PhotoImage(file='S2_shopping.png')
    
    #S2 lugares pg2
    imgCasa = PhotoImage(file='S2_casa.png')
    imgcVovô = PhotoImage(file='S2_cVovô.png')
    imgcVovó = PhotoImage(file='S2_cVovó.png')
    imgcTitio = PhotoImage(file='S2_cTitio.png')
    imgcTitia = PhotoImage(file='S2_cTitia.png')
    
    imgQuarto = PhotoImage(file='S2_quarto.png')
    imgPraia = PhotoImage(file='S2_praia.png')
    imgIgreja = PhotoImage(file='S2_igreja.png')
    imgEstádio = PhotoImage(file='S2_estádio.png')
    imgCozinha = PhotoImage(file='S2_cozinha.png')

    #S3 pessoas pg1
    imgEle = PhotoImage(file='S3_ele.png')
    imgEla = PhotoImage(file='S3_ela.png')
    imgCozinheira = PhotoImage(file='S3_cozinheira.png')
    imgProfessora = PhotoImage(file='S3_professora.png')
    imgFisio = PhotoImage(file='S3_fisioterapeuta.png')
    
    imgDiretora = PhotoImage(file='S3_diretora.png')
    imgPapai = PhotoImage(file='S3_papai.png')
    imgMamãe = PhotoImage(file='S3_mamãe.png')
    imgTitio = PhotoImage(file='S3_titio.png')
    imgTitia = PhotoImage(file='S3_titia.png')
    
    #S3 pessoas pg2
    imgVovô = PhotoImage(file='S3_vovô.png')
    imgVovó = PhotoImage(file='S3_vovó.png')
    imgIrmão = PhotoImage(file='S3_irmão.png')
    imgIrmã = PhotoImage(file='S3_irmã.png')
    
    #S4 brinquedos pg1
    imgBrincar = PhotoImage(file='S4_brincar.png')
    imgPuzzle = PhotoImage(file='S4_puzzle.png')
    imgDesenhar = PhotoImage(file='S4_desenhar.png')
    imgPintar = PhotoImage(file='S4_pintar.png')
    imgMúsica = PhotoImage(file='S4_música.png')
    
    imgLivro = PhotoImage(file='S4_livro.png')
    imgGibi = PhotoImage(file='S4_gibi.png')
    imgDançar = PhotoImage(file='S4_dançar.png')
    imgFora = PhotoImage(file='S4_fora.png')
    imgBicicleta = PhotoImage(file='S4_bicicleta.png')
    
    #S4 brinquedos pg2
    imgBoneca = PhotoImage(file='S4_boneca.png')
    imgUrsinho = PhotoImage(file='S4_ursinho.png')
    imgCarrinho = PhotoImage(file='S4_carrinho.png')
    imgBola = PhotoImage(file='S4_bola.png')
    imgVideogame = PhotoImage(file='S4_videogame.png')
    
    imgTv = PhotoImage(file='S4_tv.png')
    imgTablet = PhotoImage(file='S4_tablet.png')
    imgCelular = PhotoImage(file='S4_celular.png')

    falamenu('início.mp3')
    S0()

    janela.mainloop()

#banco de dados funcionário
def cadastrar_funcionário():
    
    som()
    
    global conexao
    global c
    
    global nomeUp
    global sobrenomeUp
    global apelidoUp
    global senhaUp
    
    conexao = sqlite3.connect('funcionários.db')
    c = conexao.cursor()
    
    nomeUp = entryNome.get().strip()
    sobrenomeUp = entrySobrenome.get().strip()
    apelidoUp = entryApelido.get().strip()
    senhaUp = entrySenha.get().strip()
    
    if not nomeUp or not sobrenomeUp or not apelidoUp or not senhaUp:
        messagebox.showerror(title='Autikids Cadastro', message='Preencha todos os campos.')
        
    elif len(senhaUp) < 8:
        
        messagebox.showerror(title='Autikids Cadastro', message='Sua senha deve ter no mínimo 8 caracteres.')
        entrySenha.delete(0,"end")
        
    elif nomeUp.upper() in senhaUp.upper() or senhaUp.upper() in nomeUp.upper():
        
        messagebox.showerror(title='Autikids Cadastro', message='Sua senha não pode conter seu nome ou vice-versa.')
        entrySenha.delete(0,"end")
        
    elif len(apelidoUp) > 11:
    
        messagebox.showerror(title='Autikids Cadastro', message='Seu apelido deve ter no máximo 11 caractéres.')
        entryApelido.delete(0,"end")
    
    else:
        
        c.execute("SELECT * FROM funcionários WHERE apelido=?", (apelidoUp,))
        ApelidoCheck = c.fetchone()
        
        if ApelidoCheck is None:
            #Inserir dados na tabela:
            c.execute("INSERT INTO funcionários VALUES (:nome,:sobrenome,:apelido,:senha)",
                    {
                        'nome': entryNome.get().strip(),
                        'sobrenome': entrySobrenome.get().strip(),
                        'apelido': entryApelido.get().strip(),
                        'senha': entrySenha.get().strip()
                    })

            # Commit das mudanças:
            conexao.commit()

            # Fechar o banco de dados:
            conexao.close()
            
            # #Apaga os valores das caixas de entrada
            entryNome.delete(0,"end"),
            entrySobrenome.delete(0,"end"),
            entryApelido.delete(0,"end"),
            entrySenha.delete(0,"end")

            messagebox.showinfo(title='Autikids Cadastro', message=f'Usuário {nomeUp} cadastrado com sucesso!\nVolte para o menu e faça Login.')
            
        else:
            messagebox.showerror(title='Autikids Cadastro', message='Este Apelido já está cadastrado.')
            entryApelido.delete(0,"end") 

#checagens e autenticações do login da janela 1
def logar():
    
    som()
    
    global inputApelido
    
    inputApelido = entryInputApelido.get().strip()
    inputSenha = entryInputSenha.get().strip()
    
    if not inputApelido or not inputSenha:
        
        messagebox.showerror(title='Autikids Login', message='Preencha os campos.')
    
    else:
        
        conexao = sqlite3.connect('funcionários.db')
        c = conexao.cursor()
        
        c.execute("SELECT * FROM funcionários WHERE apelido=? AND senha=?", (inputApelido, inputSenha))
        res = c.fetchone()
        
        if res is None:
            messagebox.showerror(title='Autikids Login', message=f'Apelido ou senha incorreto(s). Tente novamente.')
            entryInputApelido.delete(0,"end"),
            entryInputSenha.delete(0,"end")
        
        else:
            messagebox.showinfo(title='Autikids Login', message=f'Login feito com sucesso. Bem vindo(a), {res[0]}.')
            interfacePrincipal()

#janela 1 (tela de login de funcionário)
def j1():
    
    global tela
    tela = 1
    
    som()
    canvasHud.destroy()
    
    global canvasHud1
    
    global entryInputApelido
    global entryInputSenha
    
    imgCanvasLog = PhotoImage(file='canvas1.png')
    canvasHud1 = Canvas(janela, width=469, height=297, bg='orange', highlightthickness=0)
    canvasHud1.create_image(0, 0, image=imgCanvasLog, anchor='nw')
    canvasHud1.place(relx=0.5, rely=0.5, anchor='center')
    
    labelLogTitle = Label(canvasHud1, text='Login de Funcionário')
    labelLogTitle.configure(font=('Poppins', 28, 'bold'), fg='orange', bg='white')
    labelLogTitle.place(relx=0.5, rely=0.2, anchor='center')
    
    #LABELS
    
    labelInputLogin = Label(canvasHud1, text='Apelido:', background='white', fg='orange', font=('Poppins 12 bold'))
    labelInputLogin.place(relx=0.075, rely=0.4, anchor='w')
    
    labelInputSenha = Label(canvasHud1, text='Senha:', background='white', fg='orange', font=('Poppins 12 bold'))
    labelInputSenha.place(relx=0.075, rely=0.6, anchor='w')
    
    ##ENTRYS
    
    entryInputApelido = Entry(canvasHud1, border=2, font=('Poppins 12'))
    entryInputApelido.place(relx=0.25, rely=0.4, anchor='w', width=320)
    
    entryInputSenha = Entry(canvasHud1, show='*', border=2, font=('Poppins 12'))
    entryInputSenha.place(relx=0.25, rely=0.6, anchor='w', width=320)
    
    ##BOTÃO
    
    botãoVoltarMenu = Button(canvasHud1, text='Voltar', activebackground='#fdd42a', font=('Poppins 12 bold'), command=j0, cursor='hand2')
    botãoVoltarMenu.place(relx=0.075, rely=0.8, anchor='w', width=80)
    
    botãoConfirmarLog = Button(canvasHud1, text='Fazer login', activebackground='#fdd42a', font=('Poppins 12 bold'), command=logar, cursor='hand2')
    botãoConfirmarLog.place(relx=0.25, rely=0.8, anchor='w', width=320)
    
    janela.wm_minsize(width = 800, height = 600)
    janela.mainloop()
    
#janela 2 (tela de cadastrar funcionário)
def j2():
    
    global tela
    tela = 2
    
    som()
    canvasHud.destroy()
    
    global canvasHud3
    
    global entryNome
    global entrySobrenome
    global entryApelido
    global entrySenha
    
    imgCanvas3 = PhotoImage(file='canvas3.png')
    canvasHud3 = Canvas(janela, width=518, height=323, bg='orange', highlightthickness=0)
    canvasHud3.create_image(0, 0, image=imgCanvas3, anchor='nw')
    canvasHud3.place(relx=0.5, rely=0.5, anchor='center')
    
    labelCadastro = Label(canvasHud3, text='Cadastro de Funcionário')
    labelCadastro.configure(font=('Poppins', 25, 'bold'), bg='white', fg='orange')
    labelCadastro.place(relx=0.5, rely=0.125, anchor='center')
    
    labelNome = Label(canvasHud3, text='Nome:', background='white', fg='orange', font=('Poppins 12 bold'))
    labelNome.place(relx=0.070, rely=0.27, anchor='w')
    
    labelSobrenome = Label(canvasHud3, text='Sobrenome:', background='white', fg='orange', font=('Poppins 12 bold'))
    labelSobrenome.place(relx=0.070, rely=0.41, anchor='w')
    
    labelApelido = Label(canvasHud3, text='Apelido:', background='white', fg='orange', font=('Poppins 12 bold'))
    labelApelido.place(relx=0.070, rely=0.55, anchor='w')
    
    labelSenha = Label(canvasHud3, text='Senha:', background='white', fg='orange', font=('Poppins 12 bold'))
    labelSenha.place(relx=0.070, rely=0.69, anchor='w')
    
    ##ENTRYS
    
    entryNome = Entry(canvasHud3, text='Nome:', border=2, font=('Poppins 12'))
    entryNome.place(relx=0.295, rely=0.27, anchor='w', width=330)
    
    entrySobrenome = Entry(canvasHud3, text='Sobrenome:', border=2, font=('Poppins 12'))
    entrySobrenome.place(relx=0.295, rely=0.41, anchor='w', width=330)
    
    entryApelido = Entry(canvasHud3, text='Apelido:', border=2, font=('Poppins 12'), width=30)
    entryApelido.place(relx=0.295, rely=0.55, anchor='w', width=330)
    
    entrySenha = Entry(canvasHud3, text='Senha:', show='*', border=2, font=('Poppins 12'))
    entrySenha.place(relx=0.295, rely=0.69, anchor='w', width=330)
    
    ##BOTÕES
    
    botãoVoltarMenu = Button(canvasHud3, text='Voltar', width = 10, activebackground='#fdd42a', font=('Poppins 12 bold'), command=j0, cursor='hand2')
    botãoVoltarMenu.place(relx=0.07, rely=0.85, anchor='w', width=115)
    
    botãoConfirmarCad = Button(canvasHud3, text='Criar conta', width = 15, activebackground='#fdd42a', command=cadastrar_funcionário, font=('Poppins 12 bold'), cursor='hand2')
    botãoConfirmarCad.place(relx=0.295, rely=0.85, anchor='w', width=330)
    
    janela.wm_minsize(width = 800, height = 600)
    janela.mainloop()

#janela inicial =)
janela = Tk()
janela.title('Autikids')
janela.iconbitmap('icon.ico')

imgCanvas = PhotoImage(file='canvas2.png')
canvasHud = Canvas(janela, width=471, height=331, bg='orange', highlightthickness=0)
canvasHud.create_image(0, 0, image=imgCanvas, anchor='nw')
canvasHud.place(relx=0.5, rely=0.5, anchor='center')

imgLogo = PhotoImage(file='logo.png')
l_logo = Label(canvasHud, image=imgLogo, bg='white')
l_logo.place(relx=0.49, rely=0.25, anchor='center')

imgLogin = PhotoImage(file='login_botão.png')
botãoLogin = Button(canvasHud, image=imgLogin, command=j1, bg='white', border=0, activebackground='white', cursor='hand2')
botãoLogin.place(relx=0.49, rely=0.55, anchor='center')

imgCadastro = PhotoImage(file='criar_botão.png')
botãoCadastro = Button(canvasHud, image = imgCadastro, command = j2, bg='white', border=0, cursor='hand2')
botãoCadastro.place(relx=0.49, rely=0.71, anchor='center')

imgSair = PhotoImage(file='b_sair.png')
botãoSair = Button(canvasHud, image = imgSair, command = sair, bg='white', border=0, activebackground='white', cursor='hand2')
botãoSair.place(relx=0.49, rely=0.87, anchor='center')

janela.attributes("-fullscreen", True)
janela.wm_minsize(width = 800, height = 600)
janela.config(bg='orange')
janela.mainloop()
