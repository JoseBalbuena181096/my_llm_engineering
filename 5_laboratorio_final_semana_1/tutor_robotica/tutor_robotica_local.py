#!/usr/bin/env python3
"""
Tutor de Robótica Inteligente - Versión Local con Ollama
Script que actúa como tutor personalizado para enseñar robótica, Arduino, 
electrónica, mecatrónica y programación a estudiantes de diferentes edades.

Esta versión utiliza Ollama con modelos locales en lugar de OpenAI para:
1. Adaptar el lenguaje según el nivel educativo (preescolar, primaria, secundaria, preparatoria)
2. Explicar conceptos de robótica de manera apropiada para cada edad
3. Proporcionar ejemplos prácticos y proyectos adaptados
4. Soportar múltiples idiomas para la enseñanza
5. Funcionar completamente offline sin costos de API

REQUISITOS:
- Ollama instalado y ejecutándose (ollama serve)
- Modelo descargado (ollama run gpt-oss:20b)
"""

# ============================================================================
# IMPORTACIONES NECESARIAS
# ============================================================================
import os                    # Para variables de entorno
import json                 # Para manejar respuestas JSON
import ollama               # Cliente de Ollama para modelos locales
from typing import Dict, List       # Para type hints

# ============================================================================
# CONFIGURACIÓN INICIAL Y VALIDACIÓN
# ============================================================================

# Configuración del modelo local de Ollama
MODEL = 'gpt-oss:20b'   # Modelo local eficiente para tareas educativas
OLLAMA_HOST = 'http://127.0.0.1:11434'  # Servidor local de Ollama

def verificar_ollama():
    """
    Verifica que Ollama esté ejecutándose y el modelo esté disponible.
    """
    try:
        # Intentar listar modelos disponibles
        models_response = ollama.list()
        
        # La respuesta de ollama.list() tiene una estructura diferente
        # Contiene un atributo 'models' que es una lista de objetos Model
        if hasattr(models_response, 'models') and models_response.models:
            model_names = [model.model for model in models_response.models]
            
            if MODEL in model_names:
                print(f"✓ Modelo {MODEL} disponible en Ollama")
                return True
            else:
                print(f"❌ Modelo {MODEL} no encontrado. Modelos disponibles: {model_names}")
                print(f"💡 Ejecuta: ollama run {MODEL}")
                return False
        else:
            print("❌ No se encontraron modelos en Ollama")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando con Ollama: {e}")
        print("💡 Asegúrate de que Ollama esté ejecutándose: ollama serve")
        return False

# Verificar Ollama al importar
if not verificar_ollama():
    print("⚠️ Continuando sin verificación de Ollama...")

# ============================================================================
# CONFIGURACIÓN DE NIVELES EDUCATIVOS
# ============================================================================

NIVELES_EDUCATIVOS = {
    "preescolar": {
        "edad": "3-6 años",
        "descripcion": "Nivel inicial con conceptos muy básicos y juegos",
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

TEMAS_ROBOTICA = [
    "arduino", "electronica", "mecatronica", "programacion", 
    "sensores", "actuadores", "motores", "circuitos", "codigo",
    "proyectos", "robotica_basica", "automatizacion"
]

# ============================================================================
# PROMPTS MULTI-SHOT PARA DIFERENTES NIVELES
# ============================================================================

def cargar_prompt_desde_archivo(nivel: str) -> str:
    """
    Carga el prompt multi-shot desde un archivo externo.
    
    Args:
        nivel (str): Nivel educativo (preescolar, primaria, secundaria, preparatoria)
        
    Returns:
        str: Contenido del archivo de prompt
    """
    try:
        archivo_prompt = f"prompts/{nivel}.txt"
        with open(archivo_prompt, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"⚠️ Archivo de prompt no encontrado: {archivo_prompt}")
        return "No hay ejemplos disponibles para este nivel."
    except Exception as e:
        print(f"❌ Error al cargar prompt: {e}")
        return "Error al cargar ejemplos."

def get_system_prompt_multishot(nivel: str, language: str = "Español") -> str:
    """
    Genera el prompt del sistema con ejemplos multi-shot para cada nivel educativo.
    
    Args:
        nivel (str): Nivel educativo (preescolar, primaria, secundaria, preparatoria)
        language (str): Idioma para las respuestas
        
    Returns:
        str: Prompt del sistema con ejemplos multi-shot
    """
    
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
# CLASE PRINCIPAL DEL TUTOR LOCAL
# ============================================================================

class TutorRoboticaLocal:
    """
    Clase principal del tutor de robótica que maneja la interacción 
    con el estudiante y adapta las respuestas según el nivel educativo.
    Utiliza Ollama para funcionar completamente offline.
    """
    
    def __init__(self, nivel: str = "primaria", language: str = "Español"):
        """
        Inicializa el tutor con un nivel educativo y idioma específico.
        
        Args:
            nivel (str): Nivel educativo del estudiante
            language (str): Idioma para las respuestas
        """
        if nivel not in NIVELES_EDUCATIVOS:
            raise ValueError(f"Nivel '{nivel}' no válido. Opciones: {list(NIVELES_EDUCATIVOS.keys())}")
        
        self.nivel = nivel
        self.language = language
        self.system_prompt = get_system_prompt_multishot(nivel, language)
        
        print(f"🤖 Tutor de Robótica Local inicializado")
        print(f"📚 Nivel: {nivel.title()} ({NIVELES_EDUCATIVOS[nivel]['edad']})")
        print(f"🌍 Idioma: {language}")
        print(f"🔧 Modelo: {MODEL} (Local)")
        print(f"✨ {NIVELES_EDUCATIVOS[nivel]['descripcion']}")
    
    def cambiar_nivel(self, nuevo_nivel: str):
        """
        Cambia el nivel educativo del tutor.
        
        Args:
            nuevo_nivel (str): Nuevo nivel educativo
        """
        if nuevo_nivel not in NIVELES_EDUCATIVOS:
            print(f"❌ Nivel '{nuevo_nivel}' no válido. Opciones: {list(NIVELES_EDUCATIVOS.keys())}")
            return
        
        self.nivel = nuevo_nivel
        self.system_prompt = get_system_prompt_multishot(nuevo_nivel, self.language)
        print(f"📚 Nivel cambiado a: {nuevo_nivel.title()} ({NIVELES_EDUCATIVOS[nuevo_nivel]['edad']})")
    
    def cambiar_idioma(self, nuevo_idioma: str):
        """
        Cambia el idioma de las respuestas del tutor.
        
        Args:
            nuevo_idioma (str): Nuevo idioma para las respuestas
        """
        self.language = nuevo_idioma
        self.system_prompt = get_system_prompt_multishot(self.nivel, nuevo_idioma)
        print(f"🌍 Idioma cambiado a: {nuevo_idioma}")
    
    def responder_pregunta(self, pregunta: str, tema: str = "general") -> str:
        """
        Responde una pregunta del estudiante adaptada a su nivel usando Ollama.
        
        Args:
            pregunta (str): Pregunta del estudiante
            tema (str): Tema específico (opcional)
            
        Returns:
            str: Respuesta del tutor adaptada al nivel
        """
        try:
            # Crear el prompt del usuario con contexto del tema
            user_prompt = f"""
TEMA: {tema.upper() if tema != "general" else "ROBÓTICA GENERAL"}
PREGUNTA DEL ESTUDIANTE: {pregunta}

Por favor, responde esta pregunta adaptando tu explicación al nivel {self.nivel} 
({NIVELES_EDUCATIVOS[self.nivel]['edad']}). Usa el estilo y formato de los ejemplos 
multi-shot proporcionados en el prompt del sistema.
"""
            
            # Preparar mensajes para Ollama
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Mostrar encabezado
            print(f"\n🤖 Tutor de Robótica Local - Nivel {self.nivel.title()}")
            print("=" * 50)
            print("🔄 Generando respuesta con modelo local...")
            
            # Realizar llamada a Ollama
            response = ollama.chat(
                model=MODEL,
                messages=messages
            )
            
            # Obtener y mostrar respuesta
            content = response['message']['content']
            print(content)
            print("\n" + "=" * 50)
            return content
            
        except Exception as e:
            error_msg = f"❌ Error al generar respuesta con Ollama: {e}"
            print(error_msg)
            print("💡 Verifica que Ollama esté ejecutándose: ollama serve")
            print(f"💡 Verifica que el modelo esté disponible: ollama run {MODEL}")
            return error_msg

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def mostrar_menu():
    """Muestra el menú principal del tutor."""
    print("\n🤖 TUTOR DE ROBÓTICA LOCAL - MENÚ PRINCIPAL")
    print("=" * 45)
    print("1. 💬 Hacer una pregunta")
    print("2. 📚 Cambiar nivel educativo")
    print("3. 🌍 Cambiar idioma")
    print("4. ℹ️  Mostrar información actual")
    print("5. 📖 Mostrar temas disponibles")
    print("6. 🔧 Verificar estado de Ollama")
    print("7. 🚪 Salir")
    print("=" * 45)

def mostrar_niveles():
    """Muestra los niveles educativos disponibles."""
    print("\n📚 NIVELES EDUCATIVOS DISPONIBLES:")
    print("-" * 35)
    for nivel, info in NIVELES_EDUCATIVOS.items():
        print(f"• {nivel.title()}: {info['edad']} - {info['descripcion']}")

def mostrar_temas():
    """Muestra los temas de robótica disponibles."""
    print("\n🔧 TEMAS DE ROBÓTICA DISPONIBLES:")
    print("-" * 35)
    temas_formateados = [
        "Arduino", "Electrónica", "Mecatrónica", "Programación",
        "Sensores", "Actuadores", "Motores", "Circuitos", 
        "Código", "Proyectos", "Robótica Básica", "Automatización"
    ]
    for i, tema in enumerate(temas_formateados, 1):
        print(f"{i:2d}. {tema}")

def mostrar_ejemplos_preguntas(nivel: str):
    """Muestra ejemplos de preguntas según el nivel."""
    ejemplos = {
        "preescolar": [
            "¿Qué es un robot?",
            "¿Cómo se enciende un LED?",
            "¿Por qué los robots se mueven?"
        ],
        "primaria": [
            "¿Cómo funciona Arduino?",
            "¿Qué son los sensores?",
            "¿Cómo hago que un LED parpadee?"
        ],
        "secundaria": [
            "¿Cómo programo un motor con Arduino?",
            "¿Cómo calculo resistencias para LEDs?",
            "¿Qué es PWM y cómo se usa?"
        ],
        "preparatoria": [
            "¿Cómo implemento comunicación I2C?",
            "¿Qué es un controlador PID?",
            "¿Cómo diseño un sistema de control automático?"
        ]
    }
    
    print(f"\n💡 EJEMPLOS DE PREGUNTAS PARA {nivel.upper()}:")
    print("-" * 40)
    for pregunta in ejemplos[nivel]:
        print(f"• {pregunta}")

def verificar_estado_ollama():
    """Verifica y muestra el estado de Ollama."""
    print("\n🔧 VERIFICANDO ESTADO DE OLLAMA")
    print("-" * 30)
    
    try:
        # Verificar conexión
        models_response = ollama.list()
        print("✓ Ollama está ejecutándose correctamente")
        
        # Verificar si la respuesta tiene modelos
        if hasattr(models_response, 'models') and models_response.models:
            # Mostrar modelos disponibles
            print(f"\n📦 Modelos disponibles:")
            for model in models_response.models:
                model_name = model.model
                status = "✓ ACTIVO" if model_name == MODEL else "○ Disponible"
                print(f"  {status} {model_name}")
            
            # Verificar modelo específico
            model_names = [model.model for model in models_response.models]
            if MODEL in model_names:
                print(f"\n✓ Modelo {MODEL} está listo para usar")
            else:
                print(f"\n❌ Modelo {MODEL} no encontrado")
                print(f"💡 Ejecuta: ollama run {MODEL}")
        else:
            print("❌ No se encontraron modelos en Ollama")
            
    except Exception as e:
        print(f"❌ Error conectando con Ollama: {e}")
        print("💡 Soluciones:")
        print("  1. Ejecuta: ollama serve")
        print("  2. Verifica que Ollama esté instalado")
        print("  3. Reinicia el servicio de Ollama")

# ============================================================================
# FUNCIÓN PRINCIPAL INTERACTIVA
# ============================================================================

def main():
    """
    Función principal que maneja la interfaz interactiva del tutor local.
    """
    print("🤖 TUTOR DE ROBÓTICA LOCAL CON OLLAMA")
    print("=" * 40)
    print("¡Bienvenido al tutor personalizado de robótica!")
    print("Funciona completamente offline con modelos locales 🔧✨")
    
    # Verificar Ollama antes de continuar
    if not verificar_ollama():
        print("\n⚠️ Ollama no está disponible. El tutor puede no funcionar correctamente.")
        continuar = input("¿Deseas continuar de todos modos? (s/n): ").lower().strip()
        if continuar != 's':
            print("👋 ¡Configura Ollama y vuelve pronto!")
            return
    
    # Configuración inicial
    print("\n🔧 CONFIGURACIÓN INICIAL")
    print("-" * 25)
    
    # Seleccionar nivel
    mostrar_niveles()
    while True:
        nivel = input("\n📚 Selecciona tu nivel educativo: ").lower().strip()
        if nivel in NIVELES_EDUCATIVOS:
            break
        print("❌ Nivel no válido. Intenta de nuevo.")
    
    # Seleccionar idioma
    idiomas_disponibles = ["Español", "English", "Français", "Deutsch", "Italiano", "Português"]
    print(f"\n🌍 Idiomas disponibles: {', '.join(idiomas_disponibles)}")
    idioma = input("🌍 Selecciona el idioma (por defecto Español): ").strip()
    if not idioma:
        idioma = "Español"
    
    # Inicializar tutor local
    tutor = TutorRoboticaLocal(nivel, idioma)
    
    # Mostrar ejemplos de preguntas
    mostrar_ejemplos_preguntas(nivel)
    
    # Bucle principal
    while True:
        mostrar_menu()
        opcion = input("\n🎯 Selecciona una opción (1-7): ").strip()
        
        if opcion == "1":
            # Hacer pregunta
            print("\n💬 HACER UNA PREGUNTA")
            print("-" * 20)
            mostrar_temas()
            tema = input("\n🔧 Tema (opcional, presiona Enter para general): ").strip()
            if not tema:
                tema = "general"
            
            pregunta = input("❓ Tu pregunta: ").strip()
            if pregunta:
                tutor.responder_pregunta(pregunta, tema)
            else:
                print("❌ Por favor, escribe una pregunta.")
        
        elif opcion == "2":
            # Cambiar nivel
            print("\n📚 CAMBIAR NIVEL EDUCATIVO")
            print("-" * 25)
            mostrar_niveles()
            nuevo_nivel = input("📚 Nuevo nivel: ").lower().strip()
            tutor.cambiar_nivel(nuevo_nivel)
            if nuevo_nivel in NIVELES_EDUCATIVOS:
                mostrar_ejemplos_preguntas(nuevo_nivel)
        
        elif opcion == "3":
            # Cambiar idioma
            print("\n🌍 CAMBIAR IDIOMA")
            print("-" * 15)
            print(f"Idiomas disponibles: {', '.join(idiomas_disponibles)}")
            nuevo_idioma = input("🌍 Nuevo idioma: ").strip()
            if nuevo_idioma:
                tutor.cambiar_idioma(nuevo_idioma)
        
        elif opcion == "4":
            # Mostrar información actual
            print(f"\n📊 CONFIGURACIÓN ACTUAL")
            print("-" * 25)
            print(f"📚 Nivel: {tutor.nivel.title()} ({NIVELES_EDUCATIVOS[tutor.nivel]['edad']})")
            print(f"🌍 Idioma: {tutor.language}")
            print(f"🔧 Modelo: {MODEL} (Local)")
            print(f"✨ Descripción: {NIVELES_EDUCATIVOS[tutor.nivel]['descripcion']}")
        
        elif opcion == "5":
            # Mostrar temas
            mostrar_temas()
            mostrar_ejemplos_preguntas(tutor.nivel)
        
        elif opcion == "6":
            # Verificar Ollama
            verificar_estado_ollama()
        
        elif opcion == "7":
            # Salir
            print("\n👋 ¡Gracias por usar el Tutor de Robótica Local!")
            print("¡Sigue aprendiendo y creando proyectos increíbles! 🚀✨")
            break
        
        else:
            print("❌ Opción no válida. Selecciona un número del 1 al 7.")

# ============================================================================
# FUNCIÓN PARA USO PROGRAMÁTICO
# ============================================================================

def crear_tutor_local_personalizado(nivel: str = "primaria", idioma: str = "Español") -> TutorRoboticaLocal:
    """
    Función auxiliar para crear un tutor local personalizado desde otros scripts.
    
    Args:
        nivel (str): Nivel educativo
        idioma (str): Idioma para las respuestas
        
    Returns:
        TutorRoboticaLocal: Instancia del tutor local configurada
    """
    return TutorRoboticaLocal(nivel, idioma)

# ============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    """
    Punto de entrada del script.
    
    Ejecuta la interfaz interactiva del tutor local cuando el script
    se ejecuta directamente.
    """
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego! Gracias por usar el Tutor de Robótica Local 🤖✨")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("Por favor, verifica tu configuración de Ollama y vuelve a intentar.")
        print("💡 Comandos útiles:")
        print("  - ollama serve")
        print(f"  - ollama run {MODEL}")