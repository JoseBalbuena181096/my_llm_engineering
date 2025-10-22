# 🛫 Asistente de IA para Aerolínea FlightAI

Un asistente de atención al cliente inteligente para aerolíneas que utiliza las herramientas (tools) de OpenAI para consultar precios de billetes de forma dinámica.

## 📋 Descripción

Este proyecto implementa un chatbot conversacional que simula un asistente de atención al cliente para una aerolínea ficticia llamada **FlightAI**. El asistente puede:

- Mantener conversaciones naturales con los clientes
- Consultar precios de billetes de avión en tiempo real
- Proporcionar respuestas breves y corteses
- Manejar consultas sobre destinos disponibles

## 🚀 Características Principales

### ✨ Tecnologías Utilizadas
- **OpenAI GPT-4o-mini**: Modelo de lenguaje para conversaciones naturales
- **OpenAI Tools**: Sistema de herramientas para funcionalidades específicas
- **Gradio**: Interfaz web interactiva para el chat
- **Python**: Lenguaje de programación principal

### 🔧 Funcionalidades
- **Chat Interactivo**: Interfaz web amigable para conversar con el asistente
- **Consulta de Precios**: Herramienta automática para buscar precios de billetes
- **Gestión de Historial**: Mantiene el contexto de la conversación
- **Respuestas Contextuales**: El asistente usa la información de las herramientas para responder

## 🗺️ Destinos Disponibles

El asistente puede consultar precios para los siguientes destinos:

| Destino | Precio (ida y vuelta) |
|---------|----------------------|
| Londres | 799€ |
| París   | 899€ |
| Tokio   | 1400€ |
| Berlín  | 499€ |

## 📁 Estructura del Proyecto

```
9_Herramientas/
├── asistente_aerolinea.py    # Script principal del asistente
├── README.md                 # Este archivo
└── day4.ipynb               # Notebook original de referencia
```

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- Cuenta de OpenAI con API key

### 1. Instalar Dependencias

```bash
pip install openai gradio python-dotenv
```

### 2. Configurar Variables de Entorno

Crea un archivo `.env` en el directorio raíz del proyecto:

```env
OPENAI_API_KEY=tu_api_key_aqui
```

### 3. Ejecutar el Asistente

```bash
python asistente_aerolinea.py
```

El asistente se ejecutará en `http://localhost:7860`

## 💬 Ejemplos de Uso

### Consulta de Precios
```
Usuario: ¿Cuánto cuesta un billete a París?
Asistente: El precio de un billete de ida y vuelta a París es de 899€.
```

### Consulta de Destino No Disponible
```
Usuario: ¿Hay vuelos a Nueva York?
Asistente: Lo siento, no tengo información sobre precios para Nueva York en este momento.
```

### Conversación General
```
Usuario: Hola, ¿me puedes ayudar?
Asistente: ¡Hola! Soy tu asistente de FlightAI, estaré encantado de ayudarte con información sobre vuelos y precios.
```

## 🔍 Cómo Funciona

### 1. Arquitectura del Sistema

```mermaid
graph TD
    A[Usuario] --> B[Interfaz Gradio]
    B --> C[Función chat()]
    C --> D[OpenAI API]
    D --> E{¿Necesita herramienta?}
    E -->|Sí| F[handle_tool_call()]
    F --> G[get_ticket_price()]
    G --> H[Base de datos de precios]
    H --> F
    F --> D
    E -->|No| I[Respuesta directa]
    D --> I
    I --> B
    B --> A
```

### 2. Flujo de Conversación

1. **Entrada del Usuario**: El usuario escribe un mensaje en la interfaz web
2. **Procesamiento Inicial**: El sistema envía el mensaje a OpenAI junto con el historial
3. **Decisión de Herramienta**: OpenAI decide si necesita usar la herramienta de precios
4. **Ejecución de Herramienta** (si es necesario): Se consulta el precio del destino
5. **Respuesta Final**: OpenAI genera una respuesta usando la información obtenida
6. **Visualización**: La respuesta se muestra al usuario en la interfaz

### 3. Sistema de Herramientas

El proyecto utiliza el sistema de **Function Calling** de OpenAI:

- **Definición**: Se describe la función `get_ticket_price` en formato JSON
- **Detección**: OpenAI detecta automáticamente cuándo usar la herramienta
- **Ejecución**: El sistema ejecuta la función y devuelve el resultado
- **Integración**: OpenAI usa el resultado para generar la respuesta final

## 📚 Conceptos Técnicos Explicados

### OpenAI Tools (Function Calling)

Las herramientas permiten que los modelos de OpenAI ejecuten funciones específicas:

```python
# Definición de la herramienta
price_function = {
    "name": "get_ticket_price",
    "description": "Obtén el precio de un billete...",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "La ciudad de destino"
            }
        },
        "required": ["destination_city"]
    }
}
```

### Manejo de Respuestas de Herramientas

```python
if response.choices[0].finish_reason == "tool_calls":
    # El modelo quiere usar una herramienta
    tool_response = handle_tool_call(message)
    # Segunda llamada con el resultado
    final_response = openai.chat.completions.create(...)
```

## 🎯 Posibles Extensiones

### Funcionalidades Adicionales
- **Reserva de Billetes**: Implementar sistema de reservas
- **Consulta de Horarios**: Agregar información de vuelos y horarios
- **Estado de Vuelos**: Consultar retrasos y cancelaciones
- **Gestión de Equipaje**: Información sobre políticas de equipaje
- **Programa de Fidelidad**: Consultar puntos y beneficios

### Mejoras Técnicas
- **Base de Datos Real**: Conectar a una base de datos de vuelos real
- **API Externa**: Integrar con APIs de aerolíneas reales
- **Autenticación**: Sistema de login para clientes
- **Historial Persistente**: Guardar conversaciones en base de datos
- **Múltiples Idiomas**: Soporte para diferentes idiomas

## 🐛 Solución de Problemas

### Error: "OpenAI API Key Sin Configurar"
- Verifica que el archivo `.env` existe y contiene tu API key
- Asegúrate de que la variable se llama exactamente `OPENAI_API_KEY`

### Error: "Module not found"
- Instala las dependencias: `pip install openai gradio python-dotenv`

### La interfaz no se abre
- Verifica que el puerto 7860 no esté en uso
- Revisa la consola para mensajes de error

### El asistente no usa la herramienta
- Verifica que la definición de la herramienta esté correcta
- Asegúrate de que la descripción sea clara sobre cuándo usarla

## 📄 Licencia

Este proyecto está basado en el material educativo del notebook `day4.ipynb` y es para fines de aprendizaje.

## 🤝 Contribuciones

Este es un proyecto educativo. Para mejoras o sugerencias:

1. Revisa el código y los comentarios
2. Experimenta con diferentes configuraciones
3. Prueba agregar nuevas herramientas
4. Modifica la interfaz de usuario

## 📞 Soporte

Para preguntas sobre el funcionamiento del código:
- Revisa los comentarios detallados en `asistente_aerolinea.py`
- Consulta la documentación de OpenAI sobre Function Calling
- Revisa la documentación de Gradio para personalizar la interfaz

---

**¡Disfruta experimentando con tu asistente de IA para aerolíneas! ✈️**