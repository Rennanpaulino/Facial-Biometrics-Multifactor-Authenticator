import cv2
import face_recognition as fr

class Pessoa:

    def __init__(self, nome, cpf, email, access_level):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.access_level = access_level
        pass

    def tirar_foto(self):
        
        webcam = cv2.VideoCapture(0)
        while True:
            verificador, frame = webcam.read()
            if verificador:
                img_salvar = frame.copy()
                tecla = cv2.waitKey(1) & 0xFF

                faces = fr.face_locations(frame)
                for face in faces:
                    top, right, bottom, left = face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
                cv2.imshow('Cadastro', frame)

                if tecla == 32:
                    cv2.imwrite(f'imagens/{self.cpf}.jpg', img_salvar)
                elif tecla == 27:
                    break
            else:
                print("Não foi possível iniciar a webcam")
        webcam.release()
        cv2.destroyAllWindows()