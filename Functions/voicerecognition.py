import speech_recognition as sr

def reconocer_comando_voz(stop_thread, tiempo_maximo_escucha=3, tiempo_maximo_frase=5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while not stop_thread.is_set():
            r.adjust_for_ambient_noise(source)
            try:
                print("Escuchando...")
                audio = r.listen(source, timeout=tiempo_maximo_escucha, phrase_time_limit=tiempo_maximo_frase)
                texto = r.recognize_google(audio, language='en-US').lower()
                if "describe" in texto:
                    print("Comando 'describe' detectado, capturando imagen...")
                    stop_thread.set()
                    return True
            except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError) as e:
                print(f"Error de reconocimiento de voz: {e}")

    return False

