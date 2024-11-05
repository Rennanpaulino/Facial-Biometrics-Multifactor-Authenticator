from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.email_input = TextInput(hint_text='Email', multiline=False)
        self.password_input = TextInput(hint_text='Senha', password=True)
        login_button = Button(text='Sign In')
        login_button.bind(on_press=self.verify_credentials)



        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        self.add_widget(layout)

    def verify_credentials(self, instance):
        email = self.email_input.text
        password = self.password_input.text

        # Substitua pelos seus métodos de autenticação
        if email == "ruadosbobos@num0.br" and password == "bobolandia":
            self.manager.current = 'main'
        else:
            self.show_error_popup("Login ou senha incorretos")

    def show_error_popup(self, message):
        popup = Popup(title='Erro', content=Label(text=message), size_hint=(0.5, 0.5))
        popup.open()

    def go_to_face_recognition(self, instance):
        self.manager.current = 'face_recognition'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout()
        layout.add_widget(Label(text='Bem-vindo à tela principal!'))
        self.add_widget(layout)

class FaceRecognitionScreen(Screen):
    def __init__(self, **kwargs):
        super(FaceRecognitionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Tela de Reconhecimento Facial'))
        # Aqui você pode adicionar seu código para abrir a câmera e realizar o reconhecimento
        back_button = Button(text='Voltar ao Login')
        back_button.bind(on_press=self.go_back_to_login)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back_to_login(self, instance):
        self.manager.current = 'login'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(FaceRecognitionScreen(name='face_recognition'))
        return sm

if __name__ == '__main__':
    MyApp().run()
