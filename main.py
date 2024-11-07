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
        cpf = self.ids.email_input.text
        password = self.ids.password_input.text

        person.setLogin(cpf, password)

        if password == person.verifySenha(cpf):
            self.manager.current = 'face_recognition'
        else:
            self.show_error_popup("Login ou senha incorretos")

    def show_error_popup(self, message):
        popup = Popup(title='Erro', content=Label(text=message), size_hint=(0.5, 0.5))
        popup.open()

class MainScreen(Screen):
    pass

class FaceRecognitionScreen(Screen):
    def __init__(self, **kwargs):
        super(FaceRecognitionScreen, self).__init__(**kwargs)
        label = Label(text="Prepare seu rosto", font_size='24sp', bold=True)
        self.add_widget(label)

    def on_enter(self):
        cpf = person.cpf
        reconhecimento.recogface(cpf)
        
        if reconhecimento:
            self.navigate_based_on_access_level()

    def navigate_based_on_access_level(self):
        access_level = person.verifyLvlAcss(person.cpf)
        screens = {
            1: 'lvl1',  # Example for level 1 access
            2: 'lvl2',  # Example for level 2 access
            3: 'lvl3',  # Example for level 3 access
            # Add more levels if needed
        }
        screen_name = screens.get(access_level, 'login')  # Default to login if level not found
        self.manager.current = screen_name

    def go_back_to_login(self, instance):
        self.manager.current = 'login'

class LvlAcss1(Screen):
    def __init__(self, **kwargs):
        super(LvlAcss1, self).__init__(**kwargs)
        label = Label(text="Welcome Level 1", font_size='24sp', bold=True)
        self.add_widget(label)

class LvlAcss2(Screen):
    def __init__(self, **kwargs):
        super(LvlAcss2, self).__init__(**kwargs)
        label = Label(text="Welcome Level 2", font_size='24sp', bold=True)
        self.add_widget(label)

class LvlAcss3(Screen):
    def __init__(self, **kwargs):
        super(LvlAcss3, self).__init__(**kwargs)
        label = Label(text="Welcome Level 3", font_size='24sp', bold=True)
        self.add_widget(label)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(FaceRecognitionScreen(name='face_recognition'))
        sm.add_widget(LvlAcss1(name='lvl1'))
        sm.add_widget(LvlAcss2(name='lvl2'))
        sm.add_widget(LvlAcss3(name='lvl3'))
        return sm

if __name__ == '__main__':
    MyApp().run()
