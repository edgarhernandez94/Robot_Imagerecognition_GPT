import threading
import cv2
from Functions.voicerecognition import reconocer_comando_voz

def capture_image_with_voice_command():
    stop_thread = threading.Event()
    voice_thread = threading.Thread(target=reconocer_comando_voz, args=(stop_thread,))
    voice_thread.start()

    cam = cv2.VideoCapture(0)
    img_name = None  # Inicializa img_name

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error al capturar imagen.")
            break
        cv2.imshow("Di 'describe' para tomar foto", frame)

        if stop_thread.is_set():
            img_name = "captured_photo.jpg"
            cv2.imwrite(img_name, frame)
            print(f"Imagen capturada: {img_name}")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Se presionó 'q', saliendo...")
            stop_thread.set()
            break

    cam.release()
    cv2.destroyAllWindows()
    voice_thread.join()
    if img_name is None:
        print("La función terminó sin capturar una imagen.")
    return img_name
