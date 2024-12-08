import cv2
import numpy as np

# Caminhos dos arquivos
ARQUIVO_VIDEO = 'pub.mp4'
ARQUIVO_MODELO = 'frozen_inference_graph.pb'
ARQUIVO_CFG = 'ssd_mobilenet_v2_coco.pbtxt'

def carregar_modelo(ARQUIVO_MODELO, ARQUIVO_CFG):
    '''
    Carrega o modelo de deep learning do TensorFlow para detecção de objetos.
    '''
    try:
        modelo = cv2.dnn.readNetFromTensorflow(ARQUIVO_MODELO, ARQUIVO_CFG)
    except cv2.error as erro:
        print(f"Erro ao carregar o modelo: {erro}")
        exit()
    return modelo

def aplicar_supressao_nao_maxima(caixas, confiancas, limiar_conf, limiar_supr):
    '''
    Aplica a Supressão Não Máxima para reduzir o número de caixas delimitadoras sobrepostas.
    '''
    indices = cv2.dnn.NMSBoxes(caixas, confiancas, limiar_conf, limiar_supr)
    return [caixas[i] for i in indices.flatten()] if len(indices) > 0 else []

def main():
    '''
    Função principal que executa o rastreio de pessoas no vídeo.
    '''
    captura = cv2.VideoCapture(ARQUIVO_VIDEO)
    detector_pessoas = carregar_modelo(ARQUIVO_MODELO, ARQUIVO_CFG)
    pausado = False

    # Definição da região de interesse (coordenadas da porta)
    ROI_X_INICIO, ROI_Y_INICIO = 400, 220 # Ajuste baseado na imagem
    ROI_X_FIM, ROI_Y_FIM = 600, 420      # Ajuste baseado na imagem


    while True:
        if not pausado:
            ret, frame = captura.read()
            if not ret:
                break

            # Definir a região de interesse (ROI)
            roi = frame[ROI_Y_INICIO:ROI_Y_FIM, ROI_X_INICIO:ROI_X_FIM]

            # Criação do blob a partir do ROI e realização da detecção
            blob = cv2.dnn.blobFromImage(roi, size=(100, 100), swapRB=True, crop=False)
            detector_pessoas.setInput(blob)
            deteccoes = detector_pessoas.forward()

            caixas = []
            confiancas = []

            # Extração das caixas delimitadoras e confianças das detecções
            for i in range(deteccoes.shape[2]):
                confianca = deteccoes[0, 0, i, 2]
                if confianca > 0.6:
                    (altura, largura) = roi.shape[:2]
                    caixa = deteccoes[0, 0, i, 3:7] * np.array([largura, altura, largura, altura])
                    (inicioX, inicioY, fimX, fimY) = caixa.astype("int")
                    caixas.append([inicioX, inicioY, fimX - inicioX, fimY - inicioY])
                    confiancas.append(float(confianca))

            # Aplicação da supressão não máxima para finalizar as caixas delimitadoras
            caixas_finais = aplicar_supressao_nao_maxima(caixas, confiancas, limiar_conf=0.5, limiar_supr=0.4)
            numero_pessoas = len(caixas_finais)

            # Desenho das caixas e exibição do número de pessoas detectadas na ROI
            for (inicioX, inicioY, largura, altura) in caixas_finais:
                cv2.rectangle(roi, (inicioX, inicioY), (inicioX + largura, inicioY + altura), (0, 200, 0), 2)
            cv2.putText(frame, f"Pessoas perto da porta: {numero_pessoas}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)

            # Desenhar o retângulo da ROI no frame completo
            cv2.rectangle(frame, (ROI_X_INICIO, ROI_Y_INICIO), (ROI_X_FIM, ROI_Y_FIM), (255, 255, 255), 2)

        # Exibição do frame processado e controle de pausa/play
        cv2.imshow("Rastreio de Pessoas", frame)
        
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord('q'):
            break
        elif tecla == ord('p'):
            pausado = not pausado

    # Liberação dos recursos ao finalizar
    captura.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()




