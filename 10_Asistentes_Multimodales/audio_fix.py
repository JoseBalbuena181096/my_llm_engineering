"""
Soluciones alternativas para problemas de audio en entornos sin dispositivos de audio
"""

import os
import tempfile
import subprocess
from io import BytesIO
import openai

def talker_no_audio(message):
    """
    Versión de talker que genera el audio pero no lo reproduce
    Útil para entornos sin dispositivos de audio
    """
    response = openai.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=message
    )
    
    # Guardar el audio en un archivo temporal para verificar que funciona
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file_path = temp_file.name
    
    print(f"Audio generado y guardado en: {temp_file_path}")
    print(f"Mensaje de audio: '{message}'")
    
    # Opcional: eliminar el archivo temporal después de un tiempo
    # os.remove(temp_file_path)
    
    return temp_file_path

def talker_with_ffplay(message):
    """
    Versión de talker que usa ffplay directamente sin pydub
    """
    response = openai.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=message
    )
    
    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file_path = temp_file.name
    
    try:
        # Usar ffplay para reproducir el audio
        subprocess.run([
            "ffplay", 
            "-nodisp", 
            "-autoexit", 
            "-hide_banner",
            temp_file_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error reproduciendo audio: {e}")
        print(f"Audio guardado en: {temp_file_path}")
    except FileNotFoundError:
        print("ffplay no encontrado. Audio guardado en:", temp_file_path)
    finally:
        # Limpiar archivo temporal
        try:
            os.remove(temp_file_path)
        except:
            pass

def talker_simple_save(message):
    """
    Versión más simple que solo guarda el audio
    """
    response = openai.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=message
    )
    
    # Guardar en el directorio actual con nombre descriptivo
    filename = f"audio_{hash(message) % 10000}.mp3"
    filepath = os.path.join(os.getcwd(), filename)
    
    with open(filepath, "wb") as f:
        f.write(response.content)
    
    print(f"✅ Audio generado: '{message}'")
    print(f"📁 Guardado en: {filepath}")
    
    return filepath

# Función de prueba
def test_audio_functions():
    """
    Prueba las diferentes funciones de audio
    """
    test_message = "Hola, esta es una prueba de audio"
    
    print("=== Probando talker_no_audio ===")
    try:
        talker_no_audio(test_message)
        print("✅ talker_no_audio funciona")
    except Exception as e:
        print(f"❌ talker_no_audio falló: {e}")
    
    print("\n=== Probando talker_with_ffplay ===")
    try:
        talker_with_ffplay(test_message)
        print("✅ talker_with_ffplay funciona")
    except Exception as e:
        print(f"❌ talker_with_ffplay falló: {e}")
    
    print("\n=== Probando talker_simple_save ===")
    try:
        talker_simple_save(test_message)
        print("✅ talker_simple_save funciona")
    except Exception as e:
        print(f"❌ talker_simple_save falló: {e}")

if __name__ == "__main__":
    test_audio_functions()