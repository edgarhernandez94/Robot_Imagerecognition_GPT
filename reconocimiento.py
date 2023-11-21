import base64
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

from imagewithvoice import capture_image_with_voice_command
from analyzeimage import analyze_image

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
def play_sound(file_path):
    sound = AudioSegment.from_file(file_path)
    play(sound)
def speak(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio = AudioSegment.from_file(fp)
    play(audio)

def process_image_and_get_description(image_file):
    """Procesa la imagen capturada y obtiene una descripción de la misma."""
    base64_image = encode_image(image_file)
    analysis_result = analyze_image(base64_image)
    print(analysis_result)
    return analysis_result['choices'][0]['message']['content']

while True:
    image_file = capture_image_with_voice_command()
    if image_file is not None:
        try:
            description = process_image_and_get_description(image_file)
            play_sound('./Maria/4602.mp3')
            speak(description)
        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
    else:
        print("No se capturó ninguna imagen.")
