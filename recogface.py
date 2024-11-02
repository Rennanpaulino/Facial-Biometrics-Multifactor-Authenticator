import cv2
import face_recognition as fr
import os

def recogface():
    # Pasta onde as imagens dos usuários estão armazenadas
    path = 'imagens'
    imagens = []
    cpfs = []
    meusArquivos = os.listdir(path)

    # Carregar e codificar imagens base
    for arquivo in meusArquivos:
        img = fr.load_image_file(f'{path}/{arquivo}')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        imagens.append(encode)
        cpfs.append(os.path.splitext(arquivo)[0])

    # Inicializa a webcam
    webcam = cv2.VideoCapture(0)
    reconhecido = False

    while not reconhecido:
        # Captura um frame da webcam
        verificador, frame = webcam.read()
        if not verificador:
            print("Erro ao capturar imagem da webcam")
            continue

        # Converte o frame para RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detecta faces e faz o encode do frame capturado
        faceLocs = fr.face_locations(frame_rgb)
        for faceLoc in faceLocs:
            encodeTest = fr.face_encodings(frame_rgb, [faceLoc])[0]

            # Compara os encodes e calcula a distância
            comparacoes = fr.compare_faces(imagens, encodeTest)
            distancia = fr.face_distance(imagens, encodeTest)

            # Verifica se a face foi reconhecida
            melhor_correspondencia = min(distancia)
            if melhor_correspondencia < 0.4:
                melhor_indice = distancia.tolist().index(melhor_correspondencia)
                CPF = cpfs[melhor_indice]
                print("Bem-vindo,", CPF)
                reconhecido = True
                break
            else:
                cv2.putText(frame, "Desconhecido", (faceLoc[3], faceLoc[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                cv2.rectangle(frame, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (0, 0, 255), 2)

        # Mostra o frame com a face detectada
        cv2.imshow('Webcam', frame)

        # Tecla 'esc' quebra o loop
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Finaliza
    webcam.release()
    cv2.destroyAllWindows()
