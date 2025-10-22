#!/usr/bin/env python3
"""
Tutor de Robótica Multimodal
Agente educativo inteligente que combina texto, imágenes y audio para enseñar robótica,
Arduino, electrónica, mecatrónica y programación a estudiantes de diferentes edades.

Características:
- Adaptación del lenguaje según el nivel educativo
- Generación de imágenes educativas con DALL-E-3
- Síntesis de voz para explicaciones habladas
- Interfaz web interactiva con Gradio
- Herramientas especializadas para conceptos de robótica
"""

# ============================================================================
# IMPORTACIONES NECESARIAS
# ============================================================================
import os
import json
import tempfile
import subprocess
from io import BytesIO
from typing import Dict, List, Optional, Tuple
import base64

# Librerías principales
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from PIL import Image
import requests

# Librerías de audio
try:
    from pydub import AudioSegment
    from pydub.playback import play
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️ Librerías de audio no disponibles. Funcionalidad de audio limitada.")

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-'):
    print("✓ API Key de OpenAI configurada correctamente")
else:
    print("❌ Error: API Key de OpenAI no configurada")
    exit(1)

MODEL = 'gpt-4o-mini'
openai = OpenAI()

# ============================================================================
# CONFIGURACIÓN EDUCATIVA
# ============================================================================
NIVELES_EDUCATIVOS = {
    "preescolar": {
        "edad": "3-6 años",
        "descripcion": "Conceptos muy básicos con juegos y analogías simples",
        "vocabulario": "simple",
        "ejemplos": "cotidianos",
        "complejidad_imagen": "simple y colorida"
    },
    "primaria": {
        "edad": "6-12 años", 
        "descripcion": "Conceptos básicos con experimentos sencillos",
        "vocabulario": "básico",
        "ejemplos": "prácticos",
        "complejidad_imagen": "educativa con diagramas simples"
    },
    "secundaria": {
        "edad": "12-15 años",
        "descripcion": "Conceptos intermedios con proyectos estructurados", 
        "vocabulario": "técnico básico",
        "ejemplos": "proyectos",
        "complejidad_imagen": "técnica con esquemas detallados"
    },
    "preparatoria": {
        "edad": "15-18 años",
        "descripcion": "Conceptos avanzados con aplicaciones reales",
        "vocabulario": "técnico avanzado", 
        "ejemplos": "profesionales",
        "complejidad_imagen": "profesional con diagramas complejos"
    }
}

IDIOMAS_DISPONIBLES = {
    "Español": "es",
    "English": "en", 
    "Français": "fr",
    "Deutsch": "de",
    "Italiano": "it",
    "Português": "pt",
    "中文": "zh",
    "日本語": "ja",
    "한국어": "ko"
}

TEMAS_ROBOTICA = [
    "arduino", "electronica", "mecatronica", "programacion", 
    "sensores", "actuadores", "motores", "circuitos", "codigo",
    "proyectos", "robotica_basica", "automatizacion"
]

# ============================================================================
# FUNCIONES MULTIMODALES
# ============================================================================

def generar_imagen_educativa(tema: str, nivel: str, descripcion_especifica: str = "") -> Optional[Image.Image]:
    """
    Genera una imagen educativa relacionada con robótica usando DALL-E-3.
    
    Args:
        tema: Tema de robótica (arduino, sensores, etc.)
        nivel: Nivel educativo del estudiante
        descripcion_especifica: Descripción adicional para la imagen
    
    Returns:
        PIL.Image: Imagen generada o None si hay error
    """
    try:
        complejidad = NIVELES_EDUCATIVOS[nivel]["complejidad_imagen"]
        
        # Crear prompt adaptado al nivel educativo
        if nivel == "preescolar":
            prompt = f"Una ilustración {complejidad} y amigable para niños sobre {tema} en robótica, con colores brillantes, personajes simpáticos tipo robot, estilo cartoon educativo"
        elif nivel == "primaria":
            prompt = f"Una imagen {complejidad} sobre {tema} en robótica, mostrando componentes básicos de forma clara y colorida, estilo educativo para niños"
        elif nivel == "secundaria":
            prompt = f"Un diagrama {complejidad} sobre {tema} en robótica, mostrando componentes, conexiones y conceptos técnicos de forma clara, estilo educativo técnico"
        else:  # preparatoria
            prompt = f"Un esquema {complejidad} sobre {tema} en robótica, con diagramas técnicos detallados, componentes reales, conexiones precisas, estilo técnico profesional"
        
        if descripcion_especifica:
            prompt += f", específicamente mostrando {descripcion_especifica}"
        
        print(f"🎨 Generando imagen para {tema} (nivel {nivel})...")
        
        response = openai.images.generate(
            model='dall-e-3',
            prompt=prompt,
            size='1024x1024',
            n=1,
        )
        
        image_url = response.data[0].url
        img_response = requests.get(image_url)
        image = Image.open(BytesIO(img_response.content))
        
        print("✅ Imagen generada exitosamente")
        return image
        
    except Exception as e:
        print(f"❌ Error generando imagen: {e}")
        return None

def generar_audio_educativo(texto: str, velocidad: str = "normal") -> Optional[str]:
    """
    Genera audio educativo usando TTS de OpenAI.
    
    Args:
        texto: Texto a convertir en audio
        velocidad: Velocidad de habla (normal, slow, fast)
    
    Returns:
        str: Ruta del archivo de audio temporal o None si hay error
    """
    try:
        print(f"🔊 Generando audio educativo...")
        
        # Seleccionar voz apropiada para educación
        voice = "nova"  # Voz clara y amigable para educación
        
        response = openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=texto,
            speed=1.0 if velocidad == "normal" else (0.8 if velocidad == "slow" else 1.2)
        )
        
        # Guardar en archivo temporal
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name
        
        print("✅ Audio generado exitosamente")
        return temp_file_path
        
    except Exception as e:
        print(f"❌ Error generando audio: {e}")
        return None

# ============================================================================
# HERRAMIENTAS ESPECIALIZADAS
# ============================================================================

def explicar_componente_arduino(componente: str, nivel: str) -> Dict:
    """Herramienta para explicar componentes de Arduino con imagen."""
    explicaciones = {
        "led": {
            "preescolar": "Un LED es como una lucecita mágica que se enciende cuando le damos energía ⚡✨",
            "primaria": "Un LED es un diodo emisor de luz que convierte electricidad en luz de colores 💡",
            "secundaria": "Un LED es un semiconductor que emite luz cuando la corriente eléctrica pasa a través de él",
            "preparatoria": "Un LED es un diodo semiconductor que emite fotones mediante electroluminiscencia cuando se polariza directamente"
        },
        "sensor": {
            "preescolar": "Un sensor es como los ojos y oídos del robot, le ayuda a ver y sentir el mundo 👀👂",
            "primaria": "Un sensor detecta cambios en el ambiente como luz, temperatura o movimiento 🌡️",
            "secundaria": "Un sensor convierte magnitudes físicas en señales eléctricas que Arduino puede leer",
            "preparatoria": "Un sensor es un transductor que convierte variables físicas en señales eléctricas analógicas o digitales"
        }
    }
    
    explicacion = explicaciones.get(componente, {}).get(nivel, f"Información sobre {componente} para nivel {nivel}")
    
    return {
        "explicacion": explicacion,
        "generar_imagen": True,
        "tema_imagen": componente,
        "generar_audio": True
    }

def mostrar_codigo_ejemplo(concepto: str, nivel: str) -> Dict:
    """Herramienta para mostrar código de ejemplo adaptado al nivel."""
    codigos = {
        "led_parpadeo": {
            "primaria": """
// Hacer parpadear un LED
void setup() {
  pinMode(13, OUTPUT); // Pin 13 como salida
}

void loop() {
  digitalWrite(13, HIGH); // Encender LED
  delay(1000);           // Esperar 1 segundo
  digitalWrite(13, LOW);  // Apagar LED
  delay(1000);           // Esperar 1 segundo
}
""",
            "secundaria": """
// Control de LED con variable de tiempo
const int ledPin = 13;
const int delayTime = 500;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(ledPin, HIGH);
  Serial.println("LED encendido");
  delay(delayTime);
  
  digitalWrite(ledPin, LOW);
  Serial.println("LED apagado");
  delay(delayTime);
}
""",
            "preparatoria": """
// Control avanzado de LED con PWM y comunicación serie
const int ledPin = 9;        // Pin PWM
const int potPin = A0;       // Potenciómetro
int brightness = 0;
int fadeAmount = 5;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
  Serial.println("Sistema de control de LED iniciado");
}

void loop() {
  int potValue = analogRead(potPin);
  brightness = map(potValue, 0, 1023, 0, 255);
  
  analogWrite(ledPin, brightness);
  
  Serial.print("Potenciómetro: ");
  Serial.print(potValue);
  Serial.print(" - Brillo: ");
  Serial.println(brightness);
  
  delay(100);
}
"""
        }
    }
    
    codigo = codigos.get(concepto, {}).get(nivel, f"// Código de ejemplo para {concepto}")
    
    return {
        "codigo": codigo,
        "explicacion": f"Ejemplo de código para {concepto} adaptado al nivel {nivel}",
        "generar_imagen": True,
        "tema_imagen": f"código {concepto}",
        "generar_audio": False
    }

# ============================================================================
# DEFINICIÓN DE HERRAMIENTAS PARA OPENAI
# ============================================================================

herramientas_educativas = [
    {
        "type": "function",
        "function": {
            "name": "explicar_componente_arduino",
            "description": "Explica componentes de Arduino con imagen educativa adaptada al nivel del estudiante",
            "parameters": {
                "type": "object",
                "properties": {
                    "componente": {
                        "type": "string",
                        "description": "Componente a explicar (led, sensor, motor, resistencia, etc.)"
                    },
                    "nivel": {
                        "type": "string",
                        "enum": ["preescolar", "primaria", "secundaria", "preparatoria"],
                        "description": "Nivel educativo del estudiante"
                    }
                },
                "required": ["componente", "nivel"]
            }
        }
    },
    {
        "type": "function", 
        "function": {
            "name": "mostrar_codigo_ejemplo",
            "description": "Muestra código de ejemplo de Arduino adaptado al nivel educativo",
            "parameters": {
                "type": "object",
                "properties": {
                    "concepto": {
                        "type": "string",
                        "description": "Concepto de programación (led_parpadeo, sensor_lectura, motor_control, etc.)"
                    },
                    "nivel": {
                        "type": "string",
                        "enum": ["primaria", "secundaria", "preparatoria"],
                        "description": "Nivel educativo del estudiante"
                    }
                },
                "required": ["concepto", "nivel"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generar_imagen_educativa",
            "description": "Genera una imagen educativa sobre un tema específico de robótica",
            "parameters": {
                "type": "object",
                "properties": {
                    "tema": {
                        "type": "string",
                        "description": "Tema de robótica para la imagen"
                    },
                    "nivel": {
                        "type": "string",
                        "enum": ["preescolar", "primaria", "secundaria", "preparatoria"],
                        "description": "Nivel educativo para adaptar la complejidad"
                    },
                    "descripcion_especifica": {
                        "type": "string",
                        "description": "Descripción específica de lo que debe mostrar la imagen"
                    }
                },
                "required": ["tema", "nivel"]
            }
        }
    }
]

# ============================================================================
# CLASE PRINCIPAL DEL TUTOR MULTIMODAL
# ============================================================================

class TutorRoboticaMultimodal:
    """
    Tutor de robótica con capacidades multimodales (texto, imagen, audio).
    """
    
    def __init__(self, nivel: str = "primaria", idioma: str = "Español"):
        self.nivel = nivel
        self.idioma = idioma
        self.historial_conversacion = []
        
        # System prompt adaptado
        self.system_prompt = f"""
Eres un tutor experto en robótica, Arduino, electrónica y programación especializado en enseñar a estudiantes de nivel {nivel} ({NIVELES_EDUCATIVOS[nivel]['edad']}).

INSTRUCCIONES CRÍTICAS DE IDIOMA:
- DEBES responder EXCLUSIVAMENTE en {idioma}
- NUNCA uses otro idioma que no sea {idioma}
- Si el usuario pregunta en otro idioma, responde en {idioma}
- Todas tus explicaciones, ejemplos y comentarios deben estar en {idioma}

CARACTERÍSTICAS DE TU ENSEÑANZA:
- Adapta tu lenguaje al nivel {nivel}
- Usa vocabulario {NIVELES_EDUCATIVOS[nivel]['vocabulario']}
- Proporciona ejemplos {NIVELES_EDUCATIVOS[nivel]['ejemplos']}
- Incluye emojis para hacer más atractiva la explicación
- Responde SIEMPRE en {idioma}

HERRAMIENTAS DISPONIBLES:
- Puedes generar imágenes educativas para explicar conceptos
- Puedes mostrar código de ejemplo adaptado al nivel
- Puedes explicar componentes con apoyo visual

INSTRUCCIONES:
1. Siempre considera si una imagen o código de ejemplo ayudaría al estudiante
2. Usa las herramientas cuando sea apropiado para enriquecer la explicación
3. Mantén un tono educativo, paciente y motivador
4. Fomenta la curiosidad y el aprendizaje práctico
5. RESPONDE EXCLUSIVAMENTE EN {idioma}
"""
        
        print(f"🤖 Tutor de Robótica Multimodal inicializado")
        print(f"📚 Nivel: {nivel.title()} ({NIVELES_EDUCATIVOS[nivel]['edad']})")
        print(f"🌍 Idioma: {idioma}")
    
    def manejar_herramienta(self, tool_call) -> Tuple[Dict, Optional[Image.Image], Optional[str]]:
        """
        Maneja las llamadas a herramientas y retorna resultados multimodales.
        
        Returns:
            Tuple[Dict, Optional[Image.Image], Optional[str]]: (respuesta, imagen, audio)
        """
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        imagen_generada = None
        audio_generado = None
        
        if function_name == "explicar_componente_arduino":
            resultado = explicar_componente_arduino(arguments["componente"], arguments["nivel"])
            
            if resultado.get("generar_imagen"):
                imagen_generada = generar_imagen_educativa(
                    resultado["tema_imagen"], 
                    arguments["nivel"],
                    f"componente {arguments['componente']} para educación"
                )
            
            if resultado.get("generar_audio"):
                audio_generado = generar_audio_educativo(resultado["explicacion"])
        
        elif function_name == "mostrar_codigo_ejemplo":
            resultado = mostrar_codigo_ejemplo(arguments["concepto"], arguments["nivel"])
            
            if resultado.get("generar_imagen"):
                imagen_generada = generar_imagen_educativa(
                    "programacion arduino",
                    arguments["nivel"], 
                    f"código de ejemplo para {arguments['concepto']}"
                )
        
        elif function_name == "generar_imagen_educativa":
            imagen_generada = generar_imagen_educativa(
                arguments["tema"],
                arguments["nivel"],
                arguments.get("descripcion_especifica", "")
            )
            resultado = {"mensaje": f"Imagen generada para {arguments['tema']}"}
        
        else:
            resultado = {"error": f"Herramienta {function_name} no reconocida"}
        
        # Crear respuesta para OpenAI
        respuesta_herramienta = {
            "role": "tool",
            "content": json.dumps(resultado),
            "tool_call_id": tool_call.id
        }
        
        return respuesta_herramienta, imagen_generada, audio_generado
    
    def responder(self, mensaje: str) -> Tuple[str, Optional[Image.Image], Optional[str]]:
        """
        Procesa un mensaje del estudiante y retorna respuesta multimodal.
        
        Returns:
            Tuple[str, Optional[Image.Image], Optional[str]]: (texto, imagen, audio)
        """
        try:
            # Preparar mensajes para OpenAI
            mensajes = [
                {"role": "system", "content": self.system_prompt}
            ] + self.historial_conversacion + [
                {"role": "user", "content": mensaje}
            ]
            
            # Primera llamada a OpenAI
            response = openai.chat.completions.create(
                model=MODEL,
                messages=mensajes,
                tools=herramientas_educativas,
                temperature=0.7
            )
            
            imagen_resultado = None
            audio_resultado = None
            
            # Verificar si hay llamadas a herramientas
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                
                # Agregar el mensaje del asistente con tool_calls
                mensajes.append({
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": [
                        {
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.function.name,
                                "arguments": tool_call.function.arguments
                            }
                        } for tool_call in message.tool_calls
                    ]
                })
                
                # Procesar cada herramienta llamada
                for tool_call in message.tool_calls:
                    respuesta_herramienta, imagen, audio = self.manejar_herramienta(tool_call)
                    
                    if imagen:
                        imagen_resultado = imagen
                    if audio:
                        audio_resultado = audio
                    
                    # Agregar respuesta de la herramienta
                    mensajes.append(respuesta_herramienta)
                
                # Segunda llamada para generar respuesta final
                response = openai.chat.completions.create(
                    model=MODEL,
                    messages=mensajes,
                    temperature=0.7
                )
            
            respuesta_texto = response.choices[0].message.content
            
            # GENERAR AUDIO AUTOMÁTICAMENTE para todas las respuestas
            if not audio_resultado:  # Solo si no se generó audio en las herramientas
                print("🔊 Generando audio automático para la respuesta...")
                audio_resultado = generar_audio_educativo(respuesta_texto)
            
            # GENERAR IMAGEN AUTOMÁTICAMENTE si la pregunta es sobre conceptos técnicos
            if not imagen_resultado:  # Solo si no se generó imagen en las herramientas
                # Detectar si la pregunta requiere imagen
                palabras_clave = ["arduino", "sensor", "led", "motor", "circuito", "robot", "componente", 
                                "electronica", "programacion", "codigo", "esquema", "diagrama"]
                
                if any(palabra in mensaje.lower() for palabra in palabras_clave):
                    print("🎨 Generando imagen automática para el concepto...")
                    # Extraer tema principal de la pregunta
                    tema_detectado = next((palabra for palabra in palabras_clave if palabra in mensaje.lower()), "robotica")
                    imagen_resultado = generar_imagen_educativa(
                        tema_detectado, 
                        self.nivel,
                        f"concepto educativo sobre {tema_detectado}"
                    )
            
            # Actualizar historial
            self.historial_conversacion.append({"role": "user", "content": mensaje})
            self.historial_conversacion.append({"role": "assistant", "content": respuesta_texto})
            
            # Limitar historial para evitar tokens excesivos
            if len(self.historial_conversacion) > 10:
                self.historial_conversacion = self.historial_conversacion[-10:]
            
            return respuesta_texto, imagen_resultado, audio_resultado
            
        except Exception as e:
            error_msg = f"❌ Error procesando mensaje: {e}"
            print(error_msg)
            return error_msg, None, None

# ============================================================================
# INTERFAZ GRADIO
# ============================================================================

def crear_interfaz_gradio():
    """Crea la interfaz web multimodal con Gradio."""
    
    # Inicializar tutor
    tutor = TutorRoboticaMultimodal()
    
    def procesar_mensaje(mensaje, nivel, idioma, historial):
        """Procesa mensaje y retorna respuesta multimodal."""
        if nivel != tutor.nivel or idioma != tutor.idioma:
            tutor.nivel = nivel
            tutor.idioma = idioma
            tutor.system_prompt = tutor.system_prompt.replace(
                f"nivel {tutor.nivel}", f"nivel {nivel}"
            ).replace(
                f"en {tutor.idioma}", f"en {idioma}"
            )
        
        respuesta_texto, imagen, audio = tutor.responder(mensaje)
        
        # Actualizar historial de chat en formato messages
        historial.append({"role": "user", "content": mensaje})
        historial.append({"role": "assistant", "content": respuesta_texto})
        
        return historial, imagen, audio, ""
    
    # Crear interfaz
    with gr.Blocks(title="🤖 Tutor de Robótica Multimodal", theme=gr.themes.Soft()) as interfaz:
        gr.Markdown("""
        # 🤖 Tutor de Robótica Multimodal
        
        ¡Aprende robótica, Arduino y programación con explicaciones adaptadas a tu nivel!
        
        **Características:**
        - 📚 Explicaciones adaptadas por edad
        - 🎨 Imágenes educativas generadas automáticamente  
        - 🔊 Audio para reforzar el aprendizaje
        - 💻 Ejemplos de código personalizados
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # Chat principal
                chatbot = gr.Chatbot(
                    label="💬 Conversación con el Tutor",
                    height=400,
                    show_label=True,
                    type="messages"  # Usar formato moderno
                )
                
                with gr.Row():
                    mensaje_input = gr.Textbox(
                        placeholder="Escribe tu pregunta sobre robótica, Arduino, sensores, etc.",
                        label="Tu pregunta",
                        scale=4
                    )
                    enviar_btn = gr.Button("Enviar 🚀", scale=1, variant="primary")
                
                # Selectores de configuración
                with gr.Row():
                    nivel_selector = gr.Dropdown(
                        choices=list(NIVELES_EDUCATIVOS.keys()),
                        value="primaria",
                        label="📚 Nivel Educativo",
                        info="Selecciona tu nivel para adaptar las explicaciones"
                    )
                    
                    idioma_selector = gr.Dropdown(
                        choices=list(IDIOMAS_DISPONIBLES.keys()),
                        value="Español",
                        label="🌍 Idioma",
                        info="Selecciona el idioma para las respuestas"
                    )
            
            with gr.Column(scale=1):
                # Salidas multimodales
                imagen_output = gr.Image(
                    label="🎨 Imagen Educativa",
                    show_label=True,
                    height=300
                )
                
                audio_output = gr.Audio(
                    label="🔊 Explicación en Audio",
                    show_label=True
                )
        
        # Ejemplos de preguntas
        gr.Markdown("### 💡 Ejemplos de preguntas:")
        ejemplos = [
            "¿Qué es Arduino y para qué sirve?",
            "¿Cómo funciona un sensor de temperatura?",
            "Muéstrame código para hacer parpadear un LED",
            "¿Qué es un motor servo y cómo se controla?",
            "Explícame qué son las resistencias"
        ]
        
        for ejemplo in ejemplos:
            gr.Button(ejemplo, size="sm").click(
                lambda x=ejemplo: x,
                outputs=mensaje_input
            )
        
        # Eventos
        def enviar_mensaje(mensaje, nivel, idioma, historial):
            return procesar_mensaje(mensaje, nivel, idioma, historial)
        
        enviar_btn.click(
            enviar_mensaje,
            inputs=[mensaje_input, nivel_selector, idioma_selector, chatbot],
            outputs=[chatbot, imagen_output, audio_output, mensaje_input]
        )
        
        mensaje_input.submit(
            enviar_mensaje,
            inputs=[mensaje_input, nivel_selector, idioma_selector, chatbot],
            outputs=[chatbot, imagen_output, audio_output, mensaje_input]
        )
    
    return interfaz

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal para ejecutar el tutor multimodal."""
    print("🚀 Iniciando Tutor de Robótica Multimodal...")
    
    # Crear y lanzar interfaz
    interfaz = crear_interfaz_gradio()
    interfaz.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7863,  # Cambiar puerto para evitar conflictos
        show_error=True
    )

if __name__ == "__main__":
    main()