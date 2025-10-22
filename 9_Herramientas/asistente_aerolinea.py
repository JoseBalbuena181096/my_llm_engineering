"""
Asistente de IA para Aerolínea con Herramientas (Tools)
=====================================================

Este script implementa un asistente de atención al cliente para una aerolínea ficticia 
llamada FlightAI. El asistente utiliza las herramientas (tools) de OpenAI para poder 
consultar precios de billetes de avión de forma dinámica.

Características principales:
- Interfaz de chat web usando Gradio
- Integración con OpenAI GPT-4o-mini
- Uso de herramientas para consultar precios de billetes
- Respuestas breves y corteses

Autor: Basado en el notebook day4.ipynb
"""

# ============================================================================
# IMPORTACIONES
# ============================================================================

import os          # Para acceder a variables de entorno
import json        # Para manejar datos JSON en las herramientas
from dotenv import load_dotenv  # Para cargar variables de entorno desde .env
from openai import OpenAI       # Cliente de OpenAI
import gradio as gr             # Para crear la interfaz web

# ============================================================================
# CONFIGURACIÓN E INICIALIZACIÓN
# ============================================================================

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Verificar que la API key de OpenAI esté configurada
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key Sin Configurar")
    exit(1)  # Salir si no hay API key
    
# Configuración del modelo a utilizar
MODEL = "gpt-4o-mini"

# Inicializar el cliente de OpenAI
openai = OpenAI()

# ============================================================================
# CONFIGURACIÓN DEL ASISTENTE
# ============================================================================

# Mensaje del sistema que define el comportamiento del asistente
# Este mensaje le dice al LLM cómo debe comportarse y responder
system_message = "Eres un asistente útil para una aerolínea llamada FlightAI. "
system_message += "Da respuestas breves y corteses, de no más de una oración. "
system_message += "Se siempre preciso. Si no sabes la respuesta, dilo."

# ============================================================================
# BASE DE DATOS DE PRECIOS (SIMULADA)
# ============================================================================

# Diccionario que simula una base de datos de precios de billetes
# En un sistema real, esto vendría de una base de datos o API externa
ticket_prices = {
    "londres": "799€", 
    "parís": "899€", 
    "tokyo": "1400€", 
    "berlín": "499€"
}

# ============================================================================
# FUNCIONES DE HERRAMIENTAS (TOOLS)
# ============================================================================

def get_ticket_price(destination_city):
    """
    Función que consulta el precio de un billete a una ciudad específica.
    
    Esta función será llamada automáticamente por el LLM cuando necesite
    consultar precios de billetes.
    
    Args:
        destination_city (str): Nombre de la ciudad de destino
        
    Returns:
        str: Precio del billete o "Unknown" si no se encuentra la ciudad
    """
    print(f"Se solicitó la herramienta get_ticket_price para {destination_city}")
    
    # Convertir a minúsculas para hacer la búsqueda case-insensitive
    city = destination_city.lower()
    
    # Buscar el precio en nuestro diccionario
    return ticket_prices.get(city, "Unknown")

# ============================================================================
# DEFINICIÓN DE HERRAMIENTAS PARA OPENAI
# ============================================================================

# Estructura JSON que describe nuestra función para que OpenAI la entienda
# Esta es la especificación que le dice al LLM:
# - Qué hace la función
# - Qué parámetros necesita
# - Cuándo debe usarla
price_function = {
    "name": "get_ticket_price",
    "description": "Obtén el precio de un billete de ida y vuelta a la ciudad de destino. Llámalo siempre que necesites saber el precio del billete, por ejemplo, cuando un cliente pregunte '¿Cuánto cuesta un billete a esta ciudad?'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "La ciudad a la que el cliente desea viajar",
            },
        },
        "required": ["destination_city"],  # Parámetros obligatorios
        "additionalProperties": False      # No permitir parámetros adicionales
    }
}

# Lista de herramientas disponibles para el LLM
# Cada herramienta debe tener el tipo "function" y la definición de la función
tools = [{"type": "function", "function": price_function}]

# ============================================================================
# MANEJO DE LLAMADAS A HERRAMIENTAS
# ============================================================================

def handle_tool_call(message):
    """
    Procesa una llamada a herramienta solicitada por el LLM.
    
    Cuando el LLM decide que necesita usar una herramienta, nos envía una
    solicitud con los parámetros. Esta función ejecuta la herramienta
    y devuelve el resultado en el formato que espera OpenAI.
    
    Args:
        message: Mensaje de OpenAI que contiene la solicitud de herramienta
        
    Returns:
        tuple: (respuesta_formateada, ciudad_consultada)
    """
    # Extraer la primera (y única en este caso) llamada a herramienta
    tool_call = message.tool_calls[0]
    
    # Parsear los argumentos JSON enviados por el LLM
    arguments = json.loads(tool_call.function.arguments)
    
    # Extraer la ciudad de los argumentos
    city = arguments.get('destination_city')
    
    # Ejecutar nuestra función de herramienta
    price = get_ticket_price(city)
    
    # Formatear la respuesta en el formato que espera OpenAI
    response = {
        "role": "tool",                                                    # Rol: respuesta de herramienta
        "content": json.dumps({"destination_city": city, "price": price}), # Contenido en JSON
        "tool_call_id": message.tool_calls[0].id                          # ID de la llamada original
    }
    
    return response, city

# ============================================================================
# FUNCIÓN PRINCIPAL DE CHAT
# ============================================================================

def chat(message, history):
    """
    Función principal que maneja la conversación con el usuario.
    
    Esta función:
    1. Prepara los mensajes para enviar a OpenAI
    2. Hace la llamada inicial al LLM
    3. Si el LLM quiere usar una herramienta, la ejecuta
    4. Hace una segunda llamada al LLM con el resultado de la herramienta
    5. Devuelve la respuesta final al usuario
    
    Args:
        message (str): Mensaje actual del usuario
        history (list): Historial de la conversación
        
    Returns:
        str: Respuesta del asistente
    """
    # Construir la lista de mensajes para OpenAI
    # Incluye: mensaje del sistema + historial + mensaje actual
    messages = [
        {"role": "system", "content": system_message}  # Instrucciones del sistema
    ] + history + [                                    # Historial de conversación
        {"role": "user", "content": message}           # Mensaje actual del usuario
    ]
    
    # Primera llamada a OpenAI con las herramientas disponibles
    response = openai.chat.completions.create(
        model=MODEL, 
        messages=messages, 
        tools=tools  # Herramientas disponibles
    )

    # Verificar si el LLM quiere usar una herramienta
    if response.choices[0].finish_reason == "tool_calls":
        # El LLM quiere usar una herramienta
        
        # Obtener el mensaje con la solicitud de herramienta
        message = response.choices[0].message
        
        # Ejecutar la herramienta solicitada
        tool_response, city = handle_tool_call(message)
        
        # Agregar la solicitud de herramienta al historial
        messages.append(message)
        
        # Agregar la respuesta de la herramienta al historial
        messages.append(tool_response)
        
        # Segunda llamada a OpenAI con el resultado de la herramienta
        # Ahora el LLM puede usar esta información para responder al usuario
        response = openai.chat.completions.create(model=MODEL, messages=messages)
    
    # Devolver la respuesta final del asistente
    return response.choices[0].message.content

# ============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    """
    Punto de entrada principal del programa.
    
    Cuando se ejecuta el script directamente, se lanza la interfaz web de Gradio
    con nuestro asistente de aerolínea.
    """
    print("🛫 Iniciando Asistente de Aerolínea FlightAI...")
    print("📋 Herramientas disponibles: Consulta de precios de billetes")
    print("🌐 Lanzando interfaz web...")
    
    # Crear y lanzar la interfaz de chat usando Gradio
    # - fn=chat: Función que maneja la conversación
    # - type="messages": Formato de mensajes para el historial
    gr.ChatInterface(fn=chat, type="messages").launch()