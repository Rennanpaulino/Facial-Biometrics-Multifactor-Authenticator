from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder

# Carregando o arquivo .kv
Builder.load_file('login.kv')

class LoginScreen(Screen):
    def verify_credentials(self, instance):
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        if email == "ruadosbobos@num0.br" and password == "bobolandia":
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
        label = Label(text="Deu certo!", font_size='24sp', bold=True)
        self.add_widget(label)
        
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
