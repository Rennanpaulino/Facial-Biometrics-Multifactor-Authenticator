import cv2
import face_recognition as fr
import pessoa
import numpy as np

class Recogface:

    def get_encoded_faces(self, cpf):
        person = pessoa.Pessoa()  # Instanciação de Pessoa
        encoded_face = person.getEncodeDB(cpf)
        if encoded_face is not None:
            encoded_face_array = np.array(encoded_face)
            return [encoded_face_array]
        print("Nenhum encode encontrado.")
        return []

    def recogface(self, cpf):
        # Inicializa a webcam
        webcam = cv2.VideoCapture(0)
        reconhecido = False

        while not reconhecido:
            # Captura um frame da webcam
            verificador, frame = webcam.read()
            if not verificador:
                print("Erro ao capturar imagem da webcam")
                continue

            # Verifica se o frame foi capturado corretamente
            if frame is None or frame.size == 0:
                print("Frame vazio ou corrompido")
                continue

            # Converte o frame para RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detecta faces e faz o encode do frame capturado
            faceLocs = fr.face_locations(frame_rgb)
            for faceLoc in faceLocs:
                encode = fr.face_encodings(frame_rgb, [faceLoc])[0]

                # Recupera encode do banco de dados
                db_encodes = self.get_encoded_faces(cpf)

                if db_encodes:
                    # Compara os encodes e calcula a distância
                    comparacoes = fr.compare_faces(db_encodes, encode)
                    distancia = fr.face_distance(db_encodes, encode)

                    if any(comparacoes) and np.any(distancia < 0.4):
                        reconhecido = True
                    else:
                        cv2.putText(frame, "Desconhecido", (faceLoc[3], faceLoc[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                        cv2.rectangle(frame, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (0, 0, 255), 2)

                # Mostra o frame com a face detectada
                cv2.imshow('Webcam', frame)

            # 'esc' quebra o loop
            if cv2.waitKey(1) & 0xFF == 27:
                break

        # Finaliza
        webcam.release()
        cv2.destroyAllWindows()
        if not reconhecido:
            print("Reconhecimento facial não concluído.")
            return False
        else:
            return True
