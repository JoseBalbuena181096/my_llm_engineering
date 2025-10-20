#!/usr/bin/env python3
"""
Asistente Multi-Modelo con Gradio
Incluye GPT-4o-mini, Claude-3-Haiku y Gemini Pro
"""

import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

# Configurar clientes de API
openai_client = OpenAI()
claude_client = anthropic.Anthropic()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Mensaje del sistema por defecto
DEFAULT_SYSTEM_MESSAGE = "Eres un asistente útil que responde en formato markdown"

def verificar_apis():
    """Verificar que las APIs estén configuradas correctamente"""
    apis_status = {}
    
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        apis_status['OpenAI'] = f"✅ Configurada (empieza por {openai_key[:8]})"
    else:
        apis_status['OpenAI'] = "❌ No configurada"
    
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    if anthropic_key:
        apis_status['Anthropic'] = f"✅ Configurada (empieza por {anthropic_key[:7]})"
    else:
        apis_status['Anthropic'] = "❌ No configurada"
    
    google_key = os.getenv('GOOGLE_API_KEY')
    if google_key:
        apis_status['Google'] = f"✅ Configurada (empieza por {google_key[:8]})"
    else:
        apis_status['Google'] = "❌ No configurada"
    
    return apis_status

def stream_gpt(prompt, system_message=DEFAULT_SYSTEM_MESSAGE):
    """Función para streaming con GPT-4o-mini"""
    try:
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
        stream = openai_client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            stream=True,
            temperature=0.7
        )
        result = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                result += chunk.choices[0].delta.content
                yield result
    except Exception as e:
        yield f"❌ Error con GPT: {str(e)}"

def stream_claude(prompt, system_message=DEFAULT_SYSTEM_MESSAGE):
    """Función para streaming con Claude-3-Haiku"""
    try:
        result = claude_client.messages.stream(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0.7,
            system=system_message,
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        response = ""
        with result as stream:
            for text in stream.text_stream:
                if text:
                    response += text
                    yield response
    except Exception as e:
        yield f"❌ Error con Claude: {str(e)}"

def stream_gemini(prompt, system_message=DEFAULT_SYSTEM_MESSAGE):
    """Función para streaming con Gemini Pro"""
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # Combinar system message con el prompt del usuario
        full_prompt = f"{system_message}\n\nUsuario: {prompt}"
        
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1000,
            ),
            stream=True
        )
        
        result = ""
        for chunk in response:
            if chunk.text:
                result += chunk.text
                yield result
    except Exception as e:
        yield f"❌ Error con Gemini: {str(e)}"

def chat_with_model(prompt, model_choice, system_message):
    """Función principal que maneja la selección del modelo"""
    if not prompt.strip():
        yield "Por favor, escribe un mensaje."
        return
    
    # Usar el system message por defecto si está vacío
    if not system_message.strip():
        system_message = DEFAULT_SYSTEM_MESSAGE
    
    # Seleccionar la función según el modelo elegido
    if model_choice == "GPT-4o-mini":
        yield from stream_gpt(prompt, system_message)
    elif model_choice == "Claude-3-Haiku":
        yield from stream_claude(prompt, system_message)
    elif model_choice == 'gemini-flash-latest':
        yield from stream_gemini(prompt, system_message)
    else:
        yield "❌ Modelo no válido seleccionado."

def crear_interfaz():
    """Crear la interfaz de Gradio"""
    
    # CSS personalizado para mejorar la apariencia
    css = """
    .gradio-container {
        max-width: 800px !important;
        margin: auto !important;
    }
    .model-info {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    """
    
    with gr.Blocks(css=css, title="Asistente Multi-Modelo") as demo:
        gr.Markdown("""
        # 🤖 Asistente Multi-Modelo
        
        Chatea con diferentes modelos de IA: **GPT-4o-mini**, **Claude-3-Haiku** y **Gemini Pro**
        
        Selecciona tu modelo preferido y comienza a conversar.
        """)
        
        # Mostrar estado de las APIs
        with gr.Row():
            with gr.Column():
                apis_status = verificar_apis()
                status_text = "**Estado de las APIs:**\n\n"
                for api, status in apis_status.items():
                    status_text += f"- {api}: {status}\n"
                gr.Markdown(status_text)
        
        with gr.Row():
            with gr.Column(scale=1):
                model_choice = gr.Dropdown(
                    choices=["GPT-4o-mini", "Claude-3-Haiku", 'gemini-flash-latest'],
                    value="GPT-4o-mini",
                    label="🎯 Seleccionar Modelo",
                    info="Elige el modelo de IA que quieres usar"
                )
                
                system_message = gr.Textbox(
                    label="⚙️ Mensaje del Sistema (Opcional)",
                    placeholder="Eres un asistente útil que responde en formato markdown",
                    value=DEFAULT_SYSTEM_MESSAGE,
                    lines=2,
                    info="Define cómo debe comportarse el asistente"
                )
        
        with gr.Row():
            with gr.Column():
                prompt_input = gr.Textbox(
                    label="💬 Tu Mensaje",
                    placeholder="Escribe tu pregunta o mensaje aquí...",
                    lines=4
                )
                
                submit_btn = gr.Button("🚀 Enviar", variant="primary", size="lg")
        
        with gr.Row():
            with gr.Column():
                response_output = gr.Markdown(
                    label="🤖 Respuesta del Asistente",
                    value="Selecciona un modelo y escribe tu mensaje para comenzar...",
                    height=400
                )
        
        # Información sobre los modelos
        with gr.Accordion("ℹ️ Información sobre los Modelos", open=False):
            gr.Markdown("""
            ### 🔍 Características de cada modelo:
            
            **GPT-4o-mini:**
            - Desarrollado por OpenAI
            - Excelente para tareas generales y programación
            - Respuestas rápidas y precisas
            
            **Claude-3-Haiku:**
            - Desarrollado por Anthropic
            - Enfocado en seguridad y utilidad
            - Muy bueno para análisis y razonamiento
            
            **Gemini Pro:**
            - Desarrollado por Google
            - Multimodal y versátil
            - Excelente para tareas creativas y técnicas
            """)
        
        # Configurar eventos
        submit_btn.click(
            fn=chat_with_model,
            inputs=[prompt_input, model_choice, system_message],
            outputs=[response_output]
        )
        
        # También permitir envío con Enter
        prompt_input.submit(
            fn=chat_with_model,
            inputs=[prompt_input, model_choice, system_message],
            outputs=[response_output]
        )
        
        # Ejemplos de prompts
        gr.Examples(
            examples=[
                ["Explícame qué es la inteligencia artificial en términos simples"],
                ["Escribe un poema sobre la programación"],
                ["¿Cuáles son las mejores prácticas para aprender machine learning?"],
                ["Ayúdame a crear una función en Python para calcular números primos"],
                ["¿Cuál es la diferencia entre machine learning y deep learning?"]
            ],
            inputs=[prompt_input],
            label="💡 Ejemplos de Prompts"
        )
    
    return demo

def main():
    """Función principal"""
    print("🚀 Iniciando Asistente Multi-Modelo...")
    
    # Verificar APIs
    apis_status = verificar_apis()
    print("\n📊 Estado de las APIs:")
    for api, status in apis_status.items():
        print(f"  {api}: {status}")
    
    # Crear y lanzar la interfaz
    demo = crear_interfaz()
    
    print("\n🌐 Lanzando interfaz de Gradio...")
    demo.launch(
        share=False,  # Cambiar a True para crear enlace público
        inbrowser=True,  # Abrir automáticamente en el navegador
        server_name="127.0.0.1",
        server_port=None,  # Permitir que Gradio encuentre un puerto disponible automáticamente
        show_error=True
    )

if __name__ == "__main__":
    main()