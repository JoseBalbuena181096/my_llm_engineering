#!/usr/bin/env python3
"""
Tutor de Robótica con Gradio
Asistente inteligente que enseña robótica, Arduino, electrónica, mecatrónica 
y programación a estudiantes de diferentes edades usando una interfaz web con Gradio.

Este script combina:
1. La funcionalidad del tutor de robótica original
2. Una interfaz web interactiva con Gradio
3. Adaptación automática según el nivel educativo seleccionado
4. Chat conversacional con historial
"""

# ============================================================================
# IMPORTACIONES NECESARIAS
# ============================================================================
import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, List, Tuple

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

# Cargar variables de entorno
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Validar API key
if not api_key or not api_key.startswith('sk-'):
    print("❌ Error: OPENAI_API_KEY no configurada correctamente")
    exit(1)

# Configuración del modelo
MODEL = 'gpt-5-nano'
openai = OpenAI()

# ============================================================================
# CONFIGURACIÓN DE NIVELES EDUCATIVOS
# ============================================================================

NIVELES_EDUCATIVOS = {
    "preescolar": {
        "edad": "3-6 años",
        "descripcion": "Nivel inicial con conceptos muy básicos y juegos",
        "vocabulario": "simple",
        "ejemplos": "cotidianos",
        "emoji": "🧸"
    },
    "primaria": {
        "edad": "6-12 años", 
        "descripcion": "Conceptos básicos con experimentos sencillos",
        "vocabulario": "básico",
        "ejemplos": "prácticos",
        "emoji": "📚"
    },
    "secundaria": {
        "edad": "12-15 años",
        "descripcion": "Conceptos intermedios con proyectos estructurados", 
        "vocabulario": "técnico básico",
        "ejemplos": "proyectos",
        "emoji": "🔬"
    },
    "preparatoria": {
        "edad": "15-18 años",
        "descripcion": "Conceptos avanzados con aplicaciones reales",
        "vocabulario": "técnico avanzado", 
        "ejemplos": "profesionales",
        "emoji": "🎓"
    }
}

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def cargar_prompt_desde_archivo(nivel: str) -> str:
    """Carga el prompt multi-shot desde un archivo externo."""
    try:
        # Obtener el directorio donde está ubicado este script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_prompt = os.path.join(script_dir, "prompts", f"{nivel}.txt")
        
        with open(archivo_prompt, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"⚠️ Archivo de prompt no encontrado: {archivo_prompt}")
        return "No hay ejemplos disponibles para este nivel."
    except Exception as e:
        print(f"❌ Error al cargar prompt: {e}")
        return "Error al cargar ejemplos."

def get_system_prompt_multishot(nivel: str, language: str = "Español") -> str:
    """Genera el prompt del sistema con ejemplos multi-shot para cada nivel educativo."""
    
    base_prompt = f"""Eres un tutor experto en robótica, Arduino, electrónica, mecatrónica y programación. 
Tu especialidad es adaptar tu enseñanza al nivel educativo del estudiante.

NIVEL ACTUAL: {nivel.upper()} ({NIVELES_EDUCATIVOS[nivel]['edad']})
CARACTERÍSTICAS DEL NIVEL:
- {NIVELES_EDUCATIVOS[nivel]['descripcion']}
- Vocabulario: {NIVELES_EDUCATIVOS[nivel]['vocabulario']}
- Tipo de ejemplos: {NIVELES_EDUCATIVOS[nivel]['ejemplos']}

INSTRUCCIONES GENERALES:
1. Adapta tu lenguaje al nivel de edad especificado
2. Usa analogías y ejemplos apropiados para la edad
3. Incluye emojis para hacer más atractiva la explicación
4. Proporciona ejemplos prácticos cuando sea posible
5. Fomenta la curiosidad y el aprendizaje activo
6. Responde en formato Markdown para mejor legibilidad
7. Mantén un tono amigable y motivador
8. Si no sabes algo, admítelo y sugiere cómo encontrar la respuesta

EJEMPLOS DE RESPUESTAS MULTI-SHOT PARA NIVEL {nivel.upper()}:"""

    # Cargar ejemplos desde archivo externo
    ejemplos = cargar_prompt_desde_archivo(nivel)
    
    # Agregar configuración de idioma
    language_config = f"""

CONFIGURACIÓN DE IDIOMA:
- TODAS las respuestas deben generarse en {language}
- Mantén el formato Markdown y los emojis
- Adapta las expresiones culturalmente al idioma seleccionado
- Los términos técnicos pueden mantenerse en inglés si es estándar internacional
"""

    return base_prompt + ejemplos + language_config

# ============================================================================
# CLASE PRINCIPAL DEL TUTOR PARA GRADIO
# ============================================================================

class TutorRoboticaGradio:
    """
    Clase del tutor de robótica adaptada para funcionar con Gradio.
    Maneja el estado del chat y la configuración del nivel educativo.
    """
    
    def __init__(self):
        """Inicializa el tutor con configuración por defecto."""
        self.nivel_actual = "primaria"
        self.language = "Español"
        self.system_prompt = get_system_prompt_multishot(self.nivel_actual, self.language)
    
    def cambiar_nivel(self, nuevo_nivel: str) -> str:
        """
        Cambia el nivel educativo del tutor.
        
        Args:
            nuevo_nivel (str): Nuevo nivel educativo
            
        Returns:
            str: Mensaje de confirmación del cambio
        """
        if nuevo_nivel not in NIVELES_EDUCATIVOS:
            return f"❌ Nivel '{nuevo_nivel}' no válido."
        
        self.nivel_actual = nuevo_nivel
        self.system_prompt = get_system_prompt_multishot(nuevo_nivel, self.language)
        
        emoji = NIVELES_EDUCATIVOS[nuevo_nivel]['emoji']
        edad = NIVELES_EDUCATIVOS[nuevo_nivel]['edad']
        descripcion = NIVELES_EDUCATIVOS[nuevo_nivel]['descripcion']
        
        return f"""🤖 **Tutor de Robótica Actualizado**

{emoji} **Nivel:** {nuevo_nivel.title()} ({edad})
📝 **Características:** {descripcion}

¡Listo para ayudarte con robótica, Arduino, electrónica y programación! 🚀

¿Qué te gustaría aprender hoy?"""
    
    def cambiar_idioma(self, nuevo_idioma: str) -> str:
        """
        Cambia el idioma de las respuestas del tutor.
        
        Args:
            nuevo_idioma (str): Nuevo idioma para las respuestas
            
        Returns:
            str: Mensaje de confirmación del cambio
        """
        self.language = nuevo_idioma
        self.system_prompt = get_system_prompt_multishot(self.nivel_actual, nuevo_idioma)
        
        # Mensajes de confirmación en diferentes idiomas
        mensajes = {
            "Español": f"🌍 **Idioma cambiado a Español**\n\n¡Ahora responderé en español! ¿En qué puedo ayudarte?",
            "English": f"🌍 **Language changed to English**\n\nI will now respond in English! How can I help you?",
            "Français": f"🌍 **Langue changée en Français**\n\nJe vais maintenant répondre en français ! Comment puis-je vous aider ?",
            "Português": f"🌍 **Idioma alterado para Português**\n\nAgora vou responder em português! Como posso ajudá-lo?",
            "Italiano": f"🌍 **Lingua cambiata in Italiano**\n\nOra risponderò in italiano! Come posso aiutarti?",
            "日本語": f"🌍 **言語が日本語に変更されました**\n\nこれから日本語でお答えします。ご質問はありますか？",
            "Deutsch": f"🌍 **Sprache auf Deutsch geändert**\n\nIch antworte jetzt auf Deutsch! Wie kann ich dir helfen?",
            "中文": f"🌍 **语言已切换为中文**\n\n我现在将用中文回答！我能帮你什么？"
        }
        
        return mensajes.get(nuevo_idioma, f"🌍 **Language changed to {nuevo_idioma}**\n\nI will now respond in {nuevo_idioma}! How can I help you?")
    
    def chat(self, message: str, history: List) -> str:
        """
        Función principal de chat que responde a los mensajes del usuario.
        
        Args:
            message (str): Mensaje del usuario
            history (List): Historial de la conversación
            
        Yields:
            str: Respuesta del tutor en streaming
        """
        # Preparar mensajes para OpenAI
        messages = [{"role": "system", "content": self.system_prompt}] + history + [{"role": "user", "content": message}]
        
        try:
            # Llamada a OpenAI con streaming
            stream = openai.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=True,
                max_completion_tokens=5000
            )
            
            # Procesar respuesta en streaming
            response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    response += content
                    yield response
                    
        except Exception as e:
            error_msg = f"❌ Error al procesar tu pregunta: {str(e)}\n\nPor favor, intenta de nuevo o reformula tu pregunta."
            yield error_msg

# ============================================================================
# INSTANCIA GLOBAL DEL TUTOR
# ============================================================================

# Crear instancia global del tutor
tutor = TutorRoboticaGradio()

# ============================================================================
# FUNCIONES PARA LA INTERFAZ DE GRADIO
# ============================================================================

def cambiar_nivel_interface(nivel_seleccionado: str) -> Tuple[str, List]:
    """
    Función para cambiar el nivel desde la interfaz de Gradio.
    
    Args:
        nivel_seleccionado (str): Nivel seleccionado por el usuario
        
    Returns:
        Tuple[str, List]: Mensaje de confirmación y historial limpio
    """
    mensaje_confirmacion = tutor.cambiar_nivel(nivel_seleccionado)
    return mensaje_confirmacion, []  # Limpiar historial al cambiar nivel

def obtener_info_nivel_actual() -> str:
    """Obtiene información del nivel actual."""
    nivel = tutor.nivel_actual
    info = NIVELES_EDUCATIVOS[nivel]
    
    return f"""📊 **Configuración Actual**

{info['emoji']} **Nivel:** {nivel.title()} ({info['edad']})
📝 **Descripción:** {info['descripcion']}
🗣️ **Vocabulario:** {info['vocabulario']}
💡 **Ejemplos:** {info['ejemplos']}
🌍 **Idioma:** {tutor.language}

¡Listo para ayudarte con robótica y electrónica! 🚀"""

def obtener_ejemplos_preguntas(nivel: str) -> str:
    """Obtiene ejemplos de preguntas para cada nivel."""
    ejemplos = {
        "preescolar": [
            "¿Qué es un robot?",
            "¿Cómo se enciende una luz?",
            "¿Por qué se mueven los carros de juguete?",
            "¿Qué hace que suene un timbre?"
        ],
        "primaria": [
            "¿Cómo funciona un LED?",
            "¿Qué es Arduino?",
            "¿Cómo hacer que un motor gire?",
            "¿Qué es un sensor de temperatura?"
        ],
        "secundaria": [
            "¿Cómo programar un Arduino?",
            "¿Qué es PWM y para qué sirve?",
            "¿Cómo funciona un servo motor?",
            "¿Cómo hacer un robot que siga líneas?"
        ],
        "preparatoria": [
            "¿Cómo implementar PID en robótica?",
            "¿Qué es la comunicación I2C?",
            "¿Cómo diseñar un sistema de control?",
            "¿Cómo integrar sensores IoT?"
        ]
    }
    
    lista_ejemplos = ejemplos.get(nivel, [])
    ejemplos_texto = "\n".join([f"• {ejemplo}" for ejemplo in lista_ejemplos])
    
    return f"""💡 **Ejemplos de preguntas para {nivel.title()}:**

{ejemplos_texto}

¡Puedes hacer cualquiera de estas preguntas o crear las tuyas propias!"""

# ============================================================================
# CREAR INTERFAZ DE GRADIO
# ============================================================================

def crear_interfaz():
    """Crea y configura la interfaz de Gradio."""
    
    # CSS personalizado para mejorar la apariencia
    css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .nivel-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
    }
    """
    
    with gr.Blocks(css=css, title="🤖 Tutor de Robótica", theme=gr.themes.Soft()) as demo:
        
        # Título principal
        gr.Markdown("""
        # 🤖 Tutor de Robótica Inteligente
        
        ### ¡Aprende robótica, Arduino, electrónica y programación de forma divertida! 🚀
        
        **Selecciona tu nivel educativo y comienza a hacer preguntas sobre:**
        - 🔧 Arduino y microcontroladores
        - ⚡ Electrónica básica y avanzada  
        - 🤖 Robótica y automatización
        - 💻 Programación para robots
        - 🔩 Mecatrónica y sensores
        """)
        
        with gr.Row():
            with gr.Column(scale=1):
                # Panel de configuración
                gr.Markdown("## ⚙️ Configuración")
                
                nivel_dropdown = gr.Dropdown(
                    choices=list(NIVELES_EDUCATIVOS.keys()),
                    value="primaria",
                    label="📚 Selecciona tu nivel educativo",
                    info="El tutor adaptará sus explicaciones a tu edad"
                )
                
                idioma_dropdown = gr.Dropdown(
                    choices=["Español", "English", "Français", "Português", "Italiano", "日本語", "Deutsch", "中文"],
                    value="Español",
                    label="🌍 Idioma",
                    info="Selecciona el idioma para las respuestas"
                )
                
                info_nivel = gr.Markdown(obtener_info_nivel_actual())
                
                ejemplos_btn = gr.Button("💡 Ver ejemplos de preguntas", variant="secondary")
                ejemplos_output = gr.Markdown("")
                
            with gr.Column(scale=2):
                # Panel de chat
                gr.Markdown("## 💬 Chat con el Tutor")
                
                chatbot = gr.Chatbot(
                    height=500,
                    show_label=False,
                    container=True,
                    bubble_full_width=False
                )
                
                msg = gr.Textbox(
                    placeholder="Escribe tu pregunta sobre robótica, Arduino, electrónica...",
                    label="Tu pregunta",
                    lines=2
                )
                
                with gr.Row():
                    enviar_btn = gr.Button("📤 Enviar", variant="primary")
                    limpiar_btn = gr.Button("🗑️ Limpiar chat", variant="secondary")
        
        # Eventos de la interfaz
        def responder_usuario(message, history):
            """Función que maneja la respuesta del tutor."""
            return "", history + [[message, ""]]
        
        def generar_respuesta(history):
            """Función que genera la respuesta del tutor."""
            if history:
                user_message = history[-1][0]
                history[-1][1] = ""
                
                # Convertir historial de Gradio a formato OpenAI
                openai_history = []
                for user_msg, assistant_msg in history[:-1]:
                    if user_msg:
                        openai_history.append({"role": "user", "content": user_msg})
                    if assistant_msg:
                        openai_history.append({"role": "assistant", "content": assistant_msg})
                
                # Generar respuesta en streaming
                for response in tutor.chat(user_message, openai_history):
                    history[-1][1] = response
                    yield history
        
        # Configurar eventos
        msg.submit(responder_usuario, [msg, chatbot], [msg, chatbot]).then(
            generar_respuesta, chatbot, chatbot
        )
        
        enviar_btn.click(responder_usuario, [msg, chatbot], [msg, chatbot]).then(
            generar_respuesta, chatbot, chatbot
        )
        
        limpiar_btn.click(lambda: ([], ""), outputs=[chatbot, msg])
        
        nivel_dropdown.change(
            cambiar_nivel_interface, 
            inputs=[nivel_dropdown], 
            outputs=[info_nivel, chatbot]
        )
        
        idioma_dropdown.change(
            lambda idioma: tutor.cambiar_idioma(idioma),
            inputs=[idioma_dropdown],
            outputs=[info_nivel]
        )
        
        ejemplos_btn.click(
            lambda nivel: obtener_ejemplos_preguntas(nivel),
            inputs=[nivel_dropdown],
            outputs=[ejemplos_output]
        )
        
        # Información adicional en el pie
        gr.Markdown("""
        ---
        ### 📋 Instrucciones de uso:
        1. **Selecciona tu nivel educativo** en el panel izquierdo
        2. **Haz preguntas** sobre robótica, Arduino, electrónica, programación, etc.
        3. **El tutor adaptará** sus respuestas a tu edad y nivel de conocimiento
        4. **Explora diferentes temas** y no tengas miedo de preguntar
        
        ### 🎯 Temas que puedes explorar:
        - Conceptos básicos de robótica y electrónica
        - Programación de Arduino y microcontroladores  
        - Sensores, actuadores y componentes electrónicos
        - Proyectos prácticos paso a paso
        - Resolución de problemas técnicos
        
        **¡Diviértete aprendiendo! 🚀**
        """)
    
    return demo

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal que lanza la aplicación."""
    print("🤖 Iniciando Tutor de Robótica con Gradio...")
    print(f"📚 Niveles disponibles: {list(NIVELES_EDUCATIVOS.keys())}")
    print(f"🌍 Idioma: {tutor.language}")
    print("🚀 Creando interfaz...")
    
    # Crear y lanzar la interfaz
    demo = crear_interfaz()
    
    # Lanzar la aplicación
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=True,
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego! Gracias por usar el Tutor de Robótica 🤖✨")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("Por favor, verifica tu configuración y vuelve a intentar.")