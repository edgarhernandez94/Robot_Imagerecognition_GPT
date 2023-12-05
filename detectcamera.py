import cv2
import threading

def show_camera(index):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"No se pudo abrir la cámara {index}")
        return

    cv2.namedWindow(f"Cámara {index}")
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow(f"Cámara {index}", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyWindow(f"Cámara {index}")

def detect_cameras(max_cameras=10):
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
        else:
            break
    return available_cameras

def main():
    cameras = detect_cameras()
    if not cameras:
        print("No se encontraron cámaras disponibles.")
        return

    print(f"Cámaras disponibles: {cameras}")

    # Crear y comenzar hilos para cada cámara
    threads = []
    for index in cameras:
        thread = threading.Thread(target=show_camera, args=(index,))
        thread.start()
        threads.append(thread)

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
