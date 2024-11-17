import cv2
import face_recognition as fr
import firebase_admin
from firebase_admin import credentials, db
import numpy as np
import bcrypt

# Autenticação Firebase 
cred = credentials.Certificate('C:/Users/Rennan/Desktop/Facial_Biometrics_Multifactor_Authenticator/Facial-Biometrics-Multifactor-Authenticator/credenciais/credenciais.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://biometria-5cb35-default-rtdb.firebaseio.com/"
})

class Pessoa:
    def __init__(self):
        self.nome = None
        self.cpf = None
        self.email = None
        self.password = None
        self.access_level = 1
        self.encode_rosto = None

    def setLogin(self, cpf, password):
        self.cpf = cpf
        self.password = password
    
    def setCadastro(self, nome, cpf, email, password):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.password = password
        self.access_level = 1
        self.encode_rosto = None

    #Função que gera o hash da senha
    def gerar_hash_senha(self):
        #gera um valor aleatório e faz o hash
        salt = bcrypt.gensalt()
        hash_senha = bcrypt.hashpw(self.password.encode('utf-8'), salt)
        return hash_senha

    def tirar_foto(self):
        webcam = cv2.VideoCapture(0)
        if not webcam.isOpened():
            print("Não foi possível iniciar a webcam")
            return None

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

                if tecla == 32:  # Espaço
                    faces = fr.face_locations(img_salvar)
                    if faces:
                        self.encode_rosto = fr.face_encodings(img_salvar, known_face_locations=faces)[0]
                        print("Rosto detectado e encode gerado.")
                        break
                    else:
                        print("Não foram encontrados rostos.")
                elif tecla == 27:  # Esc
                    print("Captura de imagem cancelada.")
                    break
            else:
                print("Erro ao capturar imagem da webcam")        
        
        webcam.release()
        cv2.destroyAllWindows()

        # Verificação de encode gerado
        if self.encode_rosto is None:
            print("Erro: Encode não gerado.")
        return self.encode_rosto


    def salvar_db(self):
        if self.encode_rosto is not None:
            ref = db.reference(f"/CPFs/{self.cpf}")
            hash_senha = self.gerar_hash_senha()
            dados = {
                "Nome": self.nome,
                "Email": self.email,
                "Senha": hash_senha.decode('utf-8'),
                "Nível de Acesso": self.access_level,
                "Biometria": self.encode_rosto.tolist()  # Converte o numpy array para lista
            }
            ref.set(dados)
            print("Salvo no DB")
        else:
            print("Erro: encode_rosto é None, não foi possível salvar.")


    def getEncodeDB(self, cpf):
        ref = db.reference(f"/CPFs/{cpf}/Biometria")
        encode = ref.get()
        return np.array(encode) if encode else None

    def verifySenha(self, cpf, password):
        ref = db.reference(f"/CPFs/{cpf}/Senha")
        hash_senha_armazenada = ref.get()

        if hash_senha_armazenada and bcrypt.checkpw(password.encode('utf-8'), hash_senha_armazenada.encode('utf-8')):
            return True
        else:
            return False


    def verifyLvlAcss(self, cpf):
        ref = db.reference(f"CPFs/{cpf}/")
        dados = ref.get()
        if dados:
            return dados.get("Nível de Acesso")
        else:
            return 1
        