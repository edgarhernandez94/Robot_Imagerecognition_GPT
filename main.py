import base64
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from Functions.imagewithvoice import capture_image_with_voice_command
from Functions.analyzeimage import analyze_image
from reportlab.pdfgen import canvas
import threading
import os
from reportlab.lib.pagesizes import letter

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
    base64_image = encode_image(image_file)
    analysis_result = analyze_image(base64_image)
    print(analysis_result)
    return analysis_result['choices'][0]['message']['content']
def create_pdf(image_descriptions):
    c = canvas.Canvas("Image_Descriptions.pdf", pagesize=letter)
    width, height = letter

    for image_path, description in image_descriptions:
        # Asegúrate de que la imagen existe antes de intentar añadirla al PDF
        if os.path.exists(image_path):
            c.drawImage(image_path, 50, height - 550, width=400, preserveAspectRatio=True, mask='auto')
            c.drawString(50, height - 570, description)
            c.showPage()  # Crea una nueva página para la siguiente imagen y descripción

    c.save()
while True:
    image_file = capture_image_with_voice_command()
    if image_file is not None:
        try:
            description = process_image_and_get_description(image_file)
            play_sound('./Assets/4602.mp3')
            speak(description)
        except Exception as e:
            print(f"Error al procesar la imagen: {e}")
    else:
        print("No se capturó ninguna imagen.")

    create_pdf(description)
