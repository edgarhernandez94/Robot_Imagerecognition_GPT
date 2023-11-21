import cv2
import numpy as np
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import openai

# Tu clave API de OpenAI
openai.api_key = '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'


def generar_respuesta_gpt(prompt):
    try:
        respuesta = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50
        )
        return respuesta.choices[0].text.strip()
    except Exception as e:
        print(f"Error al generar la respuesta GPT: {e}")
        return None

def speak(text):
    tts = gTTS(text=text, lang='es')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio = AudioSegment.from_file(fp)
    play(audio)

# Función para detectar el color dominante en una imagen
def detectar_color_dominante(image):
    # [Agregar la implementación de la función aquí]
    pass

def capture_camera_frame(cap):
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo capturar un fotograma.")
        return None
    return frame

def reconocer_habla(r, source, tiempo_maximo_escucha=5, tiempo_maximo_frase=10):
    r.adjust_for_ambient_noise(source)
    try:
        audio = r.listen(source, timeout=tiempo_maximo_escucha, phrase_time_limit=tiempo_maximo_frase)
        return r.recognize_google(audio, language='es-ES').lower()
    except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError) as e:
        print(f"Error de reconocimiento de voz: {e}")
        return None

def procesar_texto_y_imagen(text, r, cap):
    frame = capture_camera_frame(cap)
    if frame is not None:
        cv2.imshow("Camara", frame)
        color_dominante = detectar_color_dominante(frame)
    else:
        color_dominante = "un color no identificado"

    if "perro" in text:
        prompt = f"Soy un perro robot asistente para ciegos. Acabo de ver {color_dominante}. ¿Cómo puedo describirlo para asistir a una persona ciega?"
        response = generar_respuesta_gpt(prompt)
        speak(response)

def main():
    r = sr.Recognizer()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    with sr.Microphone() as source:
        while True:
            text = reconocer_habla(r, source)
            if text:
                procesar_texto_y_imagen(text, r, cap)

            # Comprueba si se presionó la tecla 'q' para salir
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

main()
