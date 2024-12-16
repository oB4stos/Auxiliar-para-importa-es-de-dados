import flet as ft
from time import sleep
import requests
from pyperclip import copy


class Interface:
    def __init__(self, page : ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        # self.page.bgcolor=ft.colors.WHITE
        self.logo = ft.Image(src='ui/assets/background.png', height=70, width=150,scale=5, opacity=1, fit=ft.ImageFit.CONTAIN)
        self.op = 0

        # Configurações da Página
        self.page.title = 'Auxíliar de Importações'
        self.page.vertical_alignment = ft.MainAxisAlignment.START

        # Objetos da Interface
        self.bem_vindo = ft.Text(value='Bem-Vindo(a)', width=1000, size=50, text_align=ft.TextAlign.START)
        self.selecione = ft.Text(value='Clique na opção desejada para auxílio na sua importação.', width=1000, size=20, text_align=ft.TextAlign.START)
        self.dica = ft.Text(value='', text_align= ft.MainAxisAlignment.START, )

        self.mostrar_dados = ft.TextField(value='', text_align=ft.TextAlign.START, read_only=True, multiline=True, height=200, width=500)
        self.pronto = ft.ElevatedButton(text='PRONTO', visible=False, on_click=lambda e: self.getDados(e, self.op))

        self.cep_end_uf = ft.ElevatedButton(text='CEP → Cidade/UF', on_click=lambda e: self.setDados(e, 1, self.cep_end_uf.text))
        self.cidade_ou_uf = ft.Text(value='Qual informação você precisa?', visible=False)
        self.cidade = ft.ElevatedButton(text='Cidade', on_click=lambda e: self.cpu(e, 'localidade'), visible=False)
        self.uf = ft.ElevatedButton(text='UF', on_click=lambda e: self.cpu(e, 'uf'), visible=False)
        self.rua = ft.ElevatedButton(text='Logradouro', on_click=lambda e: self.cpu(e, 'logradouro'), visible=False)
        self.bairro = ft.ElevatedButton(text='Bairro', on_click=lambda e: self.cpu(e, 'bairro'), visible=False)

        self.cpf_cnpj = ft.ElevatedButton(text='Formatação de CPF/CNPJ', on_click= lambda e: self.setDados(e, 2, self.cpf_cnpj.text))
        self.maius = ft.ElevatedButton(text='Letras Maiúsculas', on_click=lambda e: self.setDados(e, 3, self.maius.text))

        self.copy = ft.ElevatedButton(text='Copiar', on_click=self.copiar_dados, visible=False)
        self.repeat = ft.IconButton(ft.icons.REPLAY, icon_size=30, visible=False, on_click=lambda e: self.setDados(self, e))
      
        self.container = ft.Container(
              content=ft.Column([self.cep_end_uf, self.cpf_cnpj, self.maius], alignment=ft.MainAxisAlignment.CENTER),
              alignment=ft.alignment.bottom_right,
              expand=True
        )
        
        # ADIÇÃO DOS ELEMENTOS NA PÁGINA
        page.add(ft.Row([self.bem_vindo], alignment=ft.MainAxisAlignment.START))    
        page.add(ft.Row([self.selecione], alignment=ft.MainAxisAlignment.START))
        page.add(ft.Row([self.dica], alignment=ft.MainAxisAlignment.START))

        page.add(ft.Column([self.mostrar_dados, ft.Row([self.copy, self.repeat])], alignment=ft.MainAxisAlignment.CENTER, expand=True))
        page.add(ft.Row([self.pronto]))

        page.add(ft.Row([self.cidade_ou_uf], alignment=ft.MainAxisAlignment.CENTER))
        page.add(ft.Row([self.cidade, self.uf], alignment=ft.MainAxisAlignment.CENTER))
        page.add(ft.Row([self.rua, self.bairro], alignment=ft.MainAxisAlignment.CENTER))

        page.add(self.container)
 
            
    def getDados(self, e, opc):
        self.pronto.visible = False
        self.dados = self.mostrar_dados.value 
        self.mostrar_dados.value=''
        self.mostrar_dados.read_only=True
        self.page.update() 
        
        if self.op == 1:
            self.cidade_ou_uf.visible=True
            self.cidade.visible=True
            self.uf.visible=True
            self.rua.visible=True
            self.bairro.visible=True
            self.page.update()
        else:
            self.cpu(e)
            

    def setDados(self, e=None, n=None, nome=None):
        sleep(1)
        if nome is not None:
            self.op = n     
            self.bem_vindo.value=nome
            self.selecione.value=''
        self.load()
        sleep(3)
        if self.pronto.visible == False:
            self.pronto.visible = True
        self.mostrar_dados.read_only=False
        self.page.update()


        
    def cpu(self, e, txt='localidade'):
        self.cidade_ou_uf.visible=False
        self.cidade.visible=False
        self.uf.visible=False
        self.rua.visible=False
        self.bairro.visible=False
        match self.op:
            case 1 | 2: # Cep /CPF-CNPJ
                self.mostrar_dados.value= ''
                self.dica.value='Sua solicitação está sendo gerada, aguarde...'
                self.page.update()
                self.dados = self.dados.split()
                for i, dado in enumerate(self.dados):
                    if self.op == 1:
                        self.mostrar_dados.value = self.mostrar_dados.value + self.cidade_uf(dado, txt) + '\n'
                    elif self.op == 2:
                        self.mostrar_dados.value = self.mostrar_dados.value + self.Cpf_e_Cnpj(dado) +'\n'
                    self.page.update()

            case 3: # Maiúscula
                self.dados = self.dados.upper()
                self.mostrar_dados.value=self.dados
                self.page.update()

        self.dica.value='Pressione em COPIAR para copiar os dados para sua área de transferência.'
        self.copy.visible=True
        self.repeat.visible=True
        self.page.update()


    def cidade_uf(self, cep, dado='localidade'):

        cep = cep.replace('-', '').strip()
        url = f'https://viacep.com.br/ws/{cep}/json/'

        try:
            resposta = requests.get(url)
            if resposta.status_code == 200:
                dados = resposta.json()
                if 'erro' not in dados:
                    return dados.get(dado, 'Cidade não encontrada')
                else: 
                    return 'CEP inválido'
            else:
                return f'Erro de requisição {resposta.status_code}'
            

        except Exception as erro:
            print(f'Erro: {erro}')


    def Cpf_e_Cnpj(self, dado):
        dado = dado.replace('-', '').replace('.', '').replace('/', '')
        if len(dado) == 11:
            return dado[:3] + '.' + dado[3:6] + '.' + dado[6:9] + '-' + dado[9:]
        elif len(dado) == 14:
            return dado[:2] + '.' + dado[2:5] + '.' + dado[5:8] + '/0001-' + dado[12:]
        else:
            return 'Documento Inválido'


    def copiar_dados(self, e):
        copy(self.mostrar_dados.value)
        self.dica.value='Dados copiados para sua área de transferência'
        self.page.update()


    def load(self): # Função para a atualização de atributos para a inserção de dados
        match self.op:
            case 1:
                self.cep_end_uf.visible=False
                self.cpf_cnpj.visible=True
                self.maius.visible=True
            case 2:
                self.cep_end_uf.visible=True
                self.cpf_cnpj.visible=False
                self.maius.visible=True
            case 3:
                self.cep_end_uf.visible=True
                self.cpf_cnpj.visible=True
                self.maius.visible=False
        self.dica.value='Cole os dados diretamente da planilha no bloco de notas aberto. Após salvar, clique em PRONTO.'
        self.repeat.visible=False
        self.copy.visible=False
        self.mostrar_dados.value=''
        self.cidade_ou_uf.visible=False
        self.cidade.visible=False
        self.uf.visible=False
        self.rua.visible=False
        self.bairro.visible=False
        self.page.update()
        

def main(page: ft.Page):
    app = Interface(page)     
ft.app(target=main, assets_dir="assets")
  
