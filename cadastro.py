import cv2
import face_recognition as fr
import firebase_admin
from firebase_admin import credentials, db

# Autenticação Firebase 
cred = credentials.Certificate('credenciais.json') 
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://biometria-37217-default-rtdb.firebaseio.com/"
    })

class Pessoa:
    def __init__(self, nome, cpf, email, password, access_level):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.password = password
        self.access_level = access_level

    def tirar_foto(self):
        webcam = cv2.VideoCapture(0)
        if not webcam.isOpened():
            print("Não foi possível iniciar a webcam")
            return

        while True:
            verificador, frame = webcam.read()
            if verificador:
                img_salvar = frame.copy()
                tecla = cv2.waitKey(1) & 0xFF

                faces = fr.face_locations(frame)
                for face in faces:
                    top, right, bottom, left = face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.imshow('Cadastro', frame)

                if tecla == 32:
                    cv2.imwrite(f'imagens/{self.cpf}.jpg', img_salvar)
                    print(f"Foto salva como: imagens/{self.cpf}.jpg")
                elif tecla == 27:
                    break
            else:
                print("Erro ao capturar imagem da webcam")
        webcam.release()
        cv2.destroyAllWindows()

    def salvar_db(self):
        ref = db.reference(f"/CPFs/{self.cpf}")
        dados = {
            "Nome": self.nome,
            "Email": self.email,
            "Senha": self.password,
            "Nível de Acesso": self.access_level
        }
        ref.set(dados)

