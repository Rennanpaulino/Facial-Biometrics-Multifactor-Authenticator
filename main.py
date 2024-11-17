from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder
import pessoa
import recogface

# Carregando o arquivo .kv
Builder.load_file('login.kv')

person = pessoa.Pessoa()
reconhecimento = recogface.Recogface()

class LoginScreen(Screen):
    def verify_credentials(self, instance):
        cpf = self.ids.cpf_input.text
        password = self.ids.password_input.text

        person.setLogin(cpf, password)

        if person.verifySenha(cpf, password) == True:
            self.manager.current = 'face_recognition'
        else:
            self.show_error_popup("Login ou senha incorretos")

    def show_error_popup(self, message):
        popup = Popup(title='Erro', content=Label(text=message), size_hint=(0.5, 0.5))
        popup.open()
    
    def cadastro(self, instance):
        self.manager.current = 'cadastro'

class MainScreen(Screen):
    pass

class FaceRecognitionScreen(Screen):
    Builder.load_file('recogface.kv')
    def __init__(self, **kwargs):
        super(FaceRecognitionScreen, self).__init__(**kwargs)


    def on_enter(self):
        cpf = person.cpf
        reconhecimento.recogface(cpf)
            
        if reconhecimento.recogface(cpf) == True:
            self.navigate_based_on_access_level()
        else:
            self.manager.current = 'face_recognition'

    def navigate_based_on_access_level(self):
        access_level = person.verifyLvlAcss(person.cpf)
        screens = {
            1: 'lvl1',  
            2: 'lvl2',
            3: 'lvl3'
        }
        
        screen_name = screens.get(access_level, 'login')  # De volta para login se não for encontrado
        self.manager.current = screen_name


    def go_back_to_login(self, instance):
        self.manager.current = 'login'

    def try_again(self, instance):
        cpf = person.cpf
        facial = reconhecimento.recogface(cpf)
            
        if facial:
            self.navigate_based_on_access_level()

class LvlAcss1Screen(Screen):
    Builder.load_file('lvl1.kv')
    def __init__(self, **kwargs):
        super(LvlAcss1Screen, self).__init__(**kwargs)

class LvlAcss2Screen(Screen):
    Builder.load_file('lvl2.kv')
    def __init__(self, **kwargs):
        super(LvlAcss2Screen, self).__init__(**kwargs)

class LvlAcss3Screen(Screen):
    Builder.load_file('lvl3.kv')
    def __init__(self, **kwargs):
        super(LvlAcss3Screen, self).__init__(**kwargs)

class CadastroScreen(Screen):    
    Builder.load_file('cadastro.kv')

    def cadastrar(self, instance):
        nome = self.ids.name_input.text
        cpf = self.ids.cpf_input.text
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        print(f"Cadastrando: Nome={nome}, CPF={cpf}, Email={email}, Senha={password}, AccessLevel={person.access_level}")

        person.setCadastro(nome, cpf, email, password)

        # Chama o método de tirar foto e verifica se o encode foi gerado
        if person.tirar_foto() is not None:
            if person.nome and person.cpf and person.email and person.password is not None:
                person.salvar_db()        
                print("Cadastro realizado.")
            else:
                print("Preencha todos os campos")
        else:
            print("Falha na captura do rosto, cadastro não realizado.")

    def go_back_to_login(self, instance):
        self.manager.current = 'login'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(FaceRecognitionScreen(name='face_recognition'))
        sm.add_widget(LvlAcss1Screen(name='lvl1'))
        sm.add_widget(LvlAcss2Screen(name='lvl2'))
        sm.add_widget(LvlAcss3Screen(name='lvl3'))
        sm.add_widget(CadastroScreen(name='cadastro'))
        return sm

if __name__ == '__main__':
    MyApp().run()
