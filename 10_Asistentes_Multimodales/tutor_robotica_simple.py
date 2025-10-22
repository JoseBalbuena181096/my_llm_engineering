#!/usr/bin/env python3
"""
Tutor de Robótica Simple
Versión simplificada del agente educativo que combina texto y audio para enseñar robótica,
Arduino, electrónica, mecatrónica y programación a estudiantes de diferentes edades.

Características:
- Adaptación del lenguaje según el nivel educativo
- Síntesis de voz para explicaciones habladas
- Interfaz web interactiva con Gradio
- Herramientas especializadas para conceptos de robótica
- Sin generación automática de imágenes (versión ligera)
"""

# ============================================================================
# IMPORTACIONES NECESARIAS
# ============================================================================
import os
import json
import tempfile
from typing import Dict, List, Optional, Tuple

# Librerías principales
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

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
        "ejemplos": "cotidianos"
    },
    "primaria": {
        "edad": "6-12 años", 
        "descripcion": "Conceptos básicos con experimentos sencillos",
        "vocabulario": "básico",
        "ejemplos": "prácticos"
    },
    "secundaria": {
        "edad": "12-15 años",
        "descripcion": "Conceptos intermedios con proyectos estructurados", 
        "vocabulario": "técnico básico",
        "ejemplos": "proyectos"
    },
    "preparatoria": {
        "edad": "15-18 años",
        "descripcion": "Conceptos avanzados con aplicaciones reales",
        "vocabulario": "técnico avanzado", 
        "ejemplos": "profesionales"
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
# FUNCIONES DE AUDIO
# ============================================================================

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
    """Herramienta para explicar componentes de Arduino."""
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
        },
        "resistencia": {
            "preescolar": "Una resistencia es como un obstáculo que hace que la electricidad vaya más despacio 🚧",
            "primaria": "Una resistencia limita la cantidad de corriente que puede pasar por un circuito ⚡",
            "secundaria": "Una resistencia controla el flujo de corriente eléctrica según la ley de Ohm (V=I×R)",
            "preparatoria": "Una resistencia es un componente pasivo que se opone al paso de la corriente eléctrica, disipando energía en forma de calor"
        },
        "motor": {
            "preescolar": "Un motor es como el músculo del robot que lo ayuda a moverse 💪🤖",
            "primaria": "Un motor convierte electricidad en movimiento para hacer girar ruedas o mover partes 🔄",
            "secundaria": "Un motor eléctrico transforma energía eléctrica en energía mecánica rotacional",
            "preparatoria": "Un motor es una máquina eléctrica que convierte energía eléctrica en energía mecánica mediante campos magnéticos"
        }
    }
    
    explicacion = explicaciones.get(componente, {}).get(nivel, f"Información sobre {componente} para nivel {nivel}")
    
    return {
        "explicacion": explicacion,
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
        },
        "sensor_lectura": {
            "primaria": """
// Leer un sensor de luz
void setup() {
  Serial.begin(9600);
}

void loop() {
  int luz = analogRead(A0);
  Serial.print("Nivel de luz: ");
  Serial.println(luz);
  delay(500);
}
""",
            "secundaria": """
// Sensor de temperatura con LED indicador
const int sensorPin = A0;
const int ledPin = 13;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int lectura = analogRead(sensorPin);
  float voltaje = lectura * (5.0 / 1023.0);
  float temperatura = (voltaje - 0.5) * 100;
  
  Serial.print("Temperatura: ");
  Serial.print(temperatura);
  Serial.println(" °C");
  
  if (temperatura > 25) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }
  
  delay(1000);
}
""",
            "preparatoria": """
// Sistema de monitoreo con múltiples sensores
const int tempPin = A0;
const int lightPin = A1;
const int ledPin = 9;
const int buzzerPin = 8;

float temperatura, luz;
unsigned long tiempoAnterior = 0;
const unsigned long intervalo = 1000;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
  Serial.println("Sistema de monitoreo iniciado");
}

void loop() {
  unsigned long tiempoActual = millis();
  
  if (tiempoActual - tiempoAnterior >= intervalo) {
    leerSensores();
    procesarDatos();
    mostrarDatos();
    tiempoAnterior = tiempoActual;
  }
}

void leerSensores() {
  int lecturaTemp = analogRead(tempPin);
  int lecturaLuz = analogRead(lightPin);
  
  temperatura = (lecturaTemp * 5.0 / 1023.0 - 0.5) * 100;
  luz = lecturaLuz * (100.0 / 1023.0);
}

void procesarDatos() {
  // Control de LED según temperatura
  int brillo = map(temperatura, 20, 40, 0, 255);
  brillo = constrain(brillo, 0, 255);
  analogWrite(ledPin, brillo);
  
  // Alarma si temperatura muy alta
  if (temperatura > 35) {
    tone(buzzerPin, 1000, 200);
  }
}

void mostrarDatos() {
  Serial.print("Temp: ");
  Serial.print(temperatura, 1);
  Serial.print("°C | Luz: ");
  Serial.print(luz, 1);
  Serial.println("%");
}
"""
        }
    }
    
    codigo = codigos.get(concepto, {}).get(nivel, f"// Código de ejemplo para {concepto}")
    
    return {
        "codigo": codigo,
        "explicacion": f"Ejemplo de código para {concepto} adaptado al nivel {nivel}",
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
            "description": "Explica componentes de Arduino adaptado al nivel del estudiante",
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
    }
]

# ============================================================================
# CLASE PRINCIPAL DEL TUTOR SIMPLE
# ============================================================================

class TutorRoboticaSimple:
    """
    Tutor de robótica simplificado con capacidades de texto y audio.
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
- Puedes mostrar código de ejemplo adaptado al nivel
- Puedes explicar componentes de forma detallada
- Enfócate en explicaciones claras y didácticas

INSTRUCCIONES:
1. Usa las herramientas cuando sea apropiado para enriquecer la explicación
2. Mantén un tono educativo, paciente y motivador
3. Fomenta la curiosidad y el aprendizaje práctico
4. Proporciona ejemplos prácticos y proyectos
5. RESPONDE EXCLUSIVAMENTE EN {idioma}
"""
        
        print(f"🤖 Tutor de Robótica Simple inicializado")
        print(f"📚 Nivel: {nivel.title()} ({NIVELES_EDUCATIVOS[nivel]['edad']})")
        print(f"🌍 Idioma: {idioma}")
    
    def manejar_herramienta(self, tool_call) -> Tuple[Dict, Optional[str]]:
        """
        Maneja las llamadas a herramientas y retorna resultados.
        
        Returns:
            Tuple[Dict, Optional[str]]: (respuesta, audio)
        """
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        audio_generado = None
        
        if function_name == "explicar_componente_arduino":
            resultado = explicar_componente_arduino(arguments["componente"], arguments["nivel"])
            
            if resultado.get("generar_audio"):
                audio_generado = generar_audio_educativo(resultado["explicacion"])
        
        elif function_name == "mostrar_codigo_ejemplo":
            resultado = mostrar_codigo_ejemplo(arguments["concepto"], arguments["nivel"])
        
        else:
            resultado = {"error": f"Herramienta {function_name} no reconocida"}
        
        # Crear respuesta para OpenAI
        respuesta_herramienta = {
            "role": "tool",
            "content": json.dumps(resultado),
            "tool_call_id": tool_call.id
        }
        
        return respuesta_herramienta, audio_generado
    
    def responder(self, mensaje: str) -> Tuple[str, Optional[str]]:
        """
        Procesa un mensaje del estudiante y retorna respuesta con audio.
        
        Returns:
            Tuple[str, Optional[str]]: (texto, audio)
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
                    respuesta_herramienta, audio = self.manejar_herramienta(tool_call)
                    
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
            if not audio_resultado:
                # Detectar si la respuesta contiene temas de robótica para generar audio
                mensaje_lower = mensaje.lower()
                respuesta_lower = respuesta_texto.lower()
                
                if any(tema in mensaje_lower or tema in respuesta_lower for tema in TEMAS_ROBOTICA):
                    print("🔊 Generando audio automático para respuesta de robótica...")
                    audio_resultado = generar_audio_educativo(respuesta_texto)
            
            # Actualizar historial
            self.historial_conversacion.extend([
                {"role": "user", "content": mensaje},
                {"role": "assistant", "content": respuesta_texto}
            ])
            
            # Mantener historial limitado
            if len(self.historial_conversacion) > 10:
                self.historial_conversacion = self.historial_conversacion[-10:]
            
            return respuesta_texto, audio_resultado
            
        except Exception as e:
            error_msg = f"Error procesando mensaje: {e}"
            print(f"❌ {error_msg}")
            return error_msg, None
    
    def actualizar_configuracion(self, nivel: str = None, idioma: str = None):
        """Actualiza la configuración del tutor."""
        if nivel and nivel != self.nivel:
            self.nivel = nivel
            print(f"📚 Nivel actualizado a: {nivel}")
        
        if idioma and idioma != self.idioma:
            self.idioma = idioma
            print(f"🌍 Idioma actualizado a: {idioma}")
            
        # Regenerar system prompt
        self.system_prompt = f"""
Eres un tutor experto en robótica, Arduino, electrónica y programación especializado en enseñar a estudiantes de nivel {self.nivel} ({NIVELES_EDUCATIVOS[self.nivel]['edad']}).

INSTRUCCIONES CRÍTICAS DE IDIOMA:
- DEBES responder EXCLUSIVAMENTE en {self.idioma}
- NUNCA uses otro idioma que no sea {self.idioma}
- Si el usuario pregunta en otro idioma, responde en {self.idioma}
- Todas tus explicaciones, ejemplos y comentarios deben estar en {self.idioma}

CARACTERÍSTICAS DE TU ENSEÑANZA:
- Adapta tu lenguaje al nivel {self.nivel}
- Usa vocabulario {NIVELES_EDUCATIVOS[self.nivel]['vocabulario']}
- Proporciona ejemplos {NIVELES_EDUCATIVOS[self.nivel]['ejemplos']}
- Incluye emojis para hacer más atractiva la explicación
- Responde SIEMPRE en {self.idioma}

HERRAMIENTAS DISPONIBLES:
- Puedes mostrar código de ejemplo adaptado al nivel
- Puedes explicar componentes de forma detallada
- Enfócate en explicaciones claras y didácticas

INSTRUCCIONES:
1. Usa las herramientas cuando sea apropiado para enriquecer la explicación
2. Mantén un tono educativo, paciente y motivador
3. Fomenta la curiosidad y el aprendizaje práctico
4. Proporciona ejemplos prácticos y proyectos
5. RESPONDE EXCLUSIVAMENTE EN {self.idioma}
"""

# ============================================================================
# INTERFAZ GRADIO
# ============================================================================

# Variable global para el tutor
tutor = None

def inicializar_tutor(nivel, idioma):
    """Inicializa el tutor con la configuración seleccionada."""
    global tutor
    tutor = TutorRoboticaSimple(nivel=nivel, idioma=idioma)
    return f"🤖 Tutor inicializado para nivel {nivel} en {idioma}"

def procesar_mensaje(mensaje, nivel, idioma):
    """Procesa un mensaje del usuario."""
    global tutor
    
    if tutor is None:
        tutor = TutorRoboticaSimple(nivel=nivel, idioma=idioma)
    else:
        # Actualizar configuración si cambió
        tutor.actualizar_configuracion(nivel=nivel, idioma=idioma)
    
    respuesta, audio = tutor.responder(mensaje)
    return respuesta, audio

def enviar_mensaje(mensaje, historial, nivel, idioma):
    """Envía un mensaje y actualiza el historial del chat."""
    if not mensaje.strip():
        return historial, "", None
    
    # Agregar mensaje del usuario al historial
    historial.append({"role": "user", "content": mensaje})
    
    # Procesar mensaje
    respuesta, audio = procesar_mensaje(mensaje, nivel, idioma)
    
    # Agregar respuesta del asistente al historial
    historial.append({"role": "assistant", "content": respuesta})
    
    return historial, "", audio

def crear_interfaz():
    """Crea la interfaz de Gradio."""
    with gr.Blocks(title="🤖 Tutor de Robótica Simple", theme=gr.themes.Soft()) as interfaz:
        gr.Markdown("""
        # 🤖 Tutor de Robótica Simple
        ### Aprende robótica, Arduino y programación de forma interactiva
        
        **Versión simplificada** - Sin generación automática de imágenes para mayor velocidad
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                nivel_selector = gr.Dropdown(
                    choices=list(NIVELES_EDUCATIVOS.keys()),
                    value="primaria",
                    label="📚 Nivel Educativo",
                    info="Selecciona tu nivel de estudios"
                )
                
                idioma_selector = gr.Dropdown(
                    choices=list(IDIOMAS_DISPONIBLES.keys()),
                    value="Español",
                    label="🌍 Idioma",
                    info="Selecciona el idioma de las respuestas"
                )
                
                inicializar_btn = gr.Button("🚀 Inicializar Tutor", variant="primary")
                estado_tutor = gr.Textbox(label="Estado", interactive=False)
            
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="💬 Conversación",
                    height=400,
                    type="messages"
                )
                
                with gr.Row():
                    mensaje_input = gr.Textbox(
                        label="Escribe tu pregunta",
                        placeholder="Pregúntame sobre Arduino, sensores, programación...",
                        scale=4
                    )
                    enviar_btn = gr.Button("📤 Enviar", variant="primary", scale=1)
                
                audio_output = gr.Audio(label="🔊 Audio de la respuesta", autoplay=True)
        
        # Ejemplos de preguntas
        gr.Examples(
            examples=[
                "¿Qué es Arduino?",
                "¿Cómo funciona un LED?",
                "Muéstrame código para hacer parpadear un LED",
                "¿Qué tipos de sensores existen?",
                "¿Cómo programo un sensor de temperatura?",
                "Explícame qué es una resistencia",
                "¿Cómo controlo un motor con Arduino?"
            ],
            inputs=mensaje_input
        )
        
        # Eventos
        inicializar_btn.click(
            inicializar_tutor,
            inputs=[nivel_selector, idioma_selector],
            outputs=estado_tutor
        )
        
        enviar_btn.click(
            enviar_mensaje,
            inputs=[mensaje_input, chatbot, nivel_selector, idioma_selector],
            outputs=[chatbot, mensaje_input, audio_output]
        )
        
        mensaje_input.submit(
            enviar_mensaje,
            inputs=[mensaje_input, chatbot, nivel_selector, idioma_selector],
            outputs=[chatbot, mensaje_input, audio_output]
        )
    
    return interfaz

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal para ejecutar el tutor."""
    print("🚀 Iniciando Tutor de Robótica Simple...")
    
    # Inicializar tutor por defecto
    global tutor
    tutor = TutorRoboticaSimple()
    print(f"🌍 Idioma por defecto: Español")
    
    # Crear y lanzar interfaz
    interfaz = crear_interfaz()
    
    print("🌐 Lanzando interfaz web...")
    interfaz.launch(
        server_name="127.0.0.1",
        server_port=7864,  # Puerto diferente para evitar conflictos
        share=False,
        show_error=True
    )

if __name__ == "__main__":
    main()