import PySimpleGUI as sg


def arquivoExiste(arq):
    try:
        a = open(arq, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


def criarArquivo(arq):
    try:
        a = open(arq, 'wt+')  # gravação de arquivo texto
        a.close()
    except:
        print('Houve um erro na criação do arquivo.')
    else:
        print(f'Arquivo {arq} criado com sucesso.')


def cadastrar(arq, usuario, senha):
    a = open(arq, 'at')
    a.write(f'{usuario},{senha}\n')
    return f' Cadastro do usuário {usuario} feito com sucesso!'
    a.close()


def buscar_usuario(arq, usuario):
    try:
        a = open(arq, 'r+')
        for linha in a:
            linha = linha.split(',')
            if linha[0] == usuario:
                return True

    except FileNotFoundError:
        return False


def acessarLogin(arq, usuario, senha):
    try:
        a = open(arq, 'r+')
        for linha in a:
            linha = linha.split(',')
            linha[1] = linha[1].replace('\n', '')
            if linha[0] == usuario and linha[1] == senha:
                return True

    except FileNotFoundError:
        return False


arq = 'baselogin.txt'
if not arquivoExiste(arq):
    criarArquivo(arq)


class TelaLogin:
    def __init__(self):

        sg.theme('Default1')

        layout = [
            [sg.Text('Usuário:', size=(7, 0)), sg.Input(size=(20, 0), key='usuario')],
            [sg.Text('Senha:', size=(7, 0)), sg.Input(size=(10, 0), key='senha', password_char='*')],
            [sg.Text('Status:', size=(7, 0)), sg.Text(size=(35, 0), key='status')],
            [sg.Button('Entrar'), sg.Button('Novo Usuário'), sg.Button('Sair')]
        ]

        self.janela_main = sg.Window('Tela de Login').layout(layout)

    def limpar(self):
        self.janela_main['usuario'].update('')
        self.janela_main['senha'].update('')

    def Iniciar(self):
        while True:
            self.button, self.values = self.janela_main.Read()

            usuario = self.values['usuario']
            senha = self.values['senha']

            if self.button == 'Entrar':

                user = acessarLogin(arq, usuario, senha)

                if user:
                    self.janela_main['status'].update('Login realizado com sucesso!')

                    self.janela_main['usuario'].update('')
                    self.janela_main['senha'].update('')

                elif senha == '' or usuario == '':
                    self.janela_main['status'].update('Erro. Favor digite todos os campos.')
                else:
                    self.janela_main['status'].update('Usuário/senha não encontrado ou incorreto. Tentar novamente.')

            elif self.button == 'Novo Usuário':

                user = buscar_usuario(arq, usuario)

                if senha == '' or usuario == '':
                    self.janela_main['status'].update('Erro. Favor digite todos os campos.')
                elif usuario == senha:
                    self.janela_main['status'].update('Erro. O Usuário deve ser diferente da senha.')
                elif user:
                    self.janela_main['status'].update('Erro. Usuário ja existe.')

                else:
                    texto = cadastrar(arq, usuario, senha)
                    self.janela_main['status'].update(str(texto))

                    self.janela_main['usuario'].update('')
                    self.janela_main['senha'].update('')

            elif self.button == 'Sair':
                break

tela = TelaLogin()
tela.Iniciar()
