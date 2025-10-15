#!/usr/bin/env python3
"""
Script para conversación entre tres modelos de IA: Claude, GPT y Gemini
Basado en el patrón de conversación del notebook day1.ipynb
"""

import os
import openai
import anthropic
import google.generativeai as genai
from dotenv import load_dotenv
import time

# Cargar variables de entorno
load_dotenv()

# Configurar APIs
openai.api_key = os.getenv("OPENAI_API_KEY")
claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configuración de modelos
GPT_MODEL = "gpt-4o-mini"
CLAUDE_MODEL = "claude-3-haiku-20240307"
GEMINI_MODEL = "gemini-flash-latest"

# Personalidades de los modelos
GPT_SYSTEM = """Eres un chatbot muy argumentativo y sarcástico. 
No estás de acuerdo con nada en la conversación y cuestionas todo de manera sarcástica.
Siempre encuentras algo que criticar o debatir."""

CLAUDE_SYSTEM = """Eres un chatbot muy educado y cortés. Intentas estar de acuerdo con 
todo lo que dice la otra persona o encontrar puntos en común. Si alguien discute, 
intentas calmarlos y seguir charlando de manera diplomática."""

GEMINI_SYSTEM = """Eres un chatbot filosófico y reflexivo. Te gusta hacer preguntas profundas
y analizar las situaciones desde múltiples perspectivas. Eres curioso y siempre buscas
el significado más profundo de las cosas."""

class ConversacionTresModelos:
    def __init__(self):
        self.gpt_messages = ["¡Hola a todos!"]
        self.claude_messages = ["Hola, encantado de conocerlos"]
        self.gemini_messages = ["Saludos, ¿qué nos depara esta conversación?"]
        
        # Inicializar modelo Gemini con system_instruction
        self.gemini_model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=GEMINI_SYSTEM
        )
        
    def call_gpt(self):
        """Llama a GPT con el historial de conversación"""
        messages = [{"role": "system", "content": GPT_SYSTEM}]
        
        # Construir historial alternando entre los tres modelos
        max_len = max(len(self.gpt_messages), len(self.claude_messages), len(self.gemini_messages))
        
        for i in range(max_len):
            if i < len(self.gpt_messages):
                messages.append({"role": "assistant", "content": self.gpt_messages[i]})
            if i < len(self.claude_messages):
                messages.append({"role": "user", "content": f"Claude dice: {self.claude_messages[i]}"})
            if i < len(self.gemini_messages):
                messages.append({"role": "user", "content": f"Gemini dice: {self.gemini_messages[i]}"})
        
        try:
            completion = openai.chat.completions.create(
                model=GPT_MODEL,
                messages=messages,
                max_tokens=300
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error en GPT: {str(e)}"
    
    def call_claude(self):
        """Llama a Claude con el historial de conversación"""
        messages = []
        
        # Construir historial alternando entre los tres modelos
        max_len = max(len(self.gpt_messages), len(self.claude_messages), len(self.gemini_messages))
        
        for i in range(max_len):
            if i < len(self.claude_messages):
                messages.append({"role": "assistant", "content": self.claude_messages[i]})
            if i < len(self.gpt_messages):
                messages.append({"role": "user", "content": f"GPT dice: {self.gpt_messages[i]}"})
            if i < len(self.gemini_messages):
                messages.append({"role": "user", "content": f"Gemini dice: {self.gemini_messages[i]}"})
        
        try:
            message = claude.messages.create(
                model=CLAUDE_MODEL,
                system=CLAUDE_SYSTEM,
                messages=messages,
                max_tokens=300
            )
            return message.content[0].text
        except Exception as e:
            return f"Error en Claude: {str(e)}"
    
    def call_gemini(self):
        """Llama a Gemini con el historial de conversación"""
        # Construir prompt con historial
        conversation_history = "Historial de conversación:\n"
        
        max_len = max(len(self.gpt_messages), len(self.claude_messages), len(self.gemini_messages))
        SSS
        for i in range(max_len):
            if i < len(self.gemini_messages):
                conversation_history += f"Gemini: {self.gemini_messages[i]}\n"
            if i < len(self.gpt_messages):
                conversation_history += f"GPT: {self.gpt_messages[i]}\n"
            if i < len(self.claude_messages):
                conversation_history += f"Claude: {self.claude_messages[i]}\n"
        
        conversation_history += "\nResponde como Gemini:"
        
        try:
            response = self.gemini_model.generate_content(conversation_history)
            return response.text
        except Exception as e:
            return f"Error en Gemini: {str(e)}"
    
    def ejecutar_conversacion(self, num_turnos=5):
        """Ejecuta la conversación entre los tres modelos"""
        print("=== CONVERSACIÓN ENTRE TRES MODELOS DE IA ===\n")
        print("🤖 GPT (Argumentativo)")
        print("🎭 Claude (Diplomático)")  
        print("🧠 Gemini (Filosófico)")
        print("\n" + "="*50 + "\n")
        
        # Mostrar mensajes iniciales
        print(f"🤖 GPT:\n{self.gpt_messages[0]}\n")
        print(f"🎭 Claude:\n{self.claude_messages[0]}\n")
        print(f"🧠 Gemini:\n{self.gemini_messages[0]}\n")
        print("-" * 50 + "\n")
        
        for turno in range(num_turnos):
            print(f"--- TURNO {turno + 1} ---\n")
            
            # GPT responde
            gpt_response = self.call_gpt()
            print(f"🤖 GPT:\n{gpt_response}\n")
            self.gpt_messages.append(gpt_response)
            time.sleep(1)  # Pausa para evitar rate limits
            
            # Claude responde
            claude_response = self.call_claude()
            print(f"🎭 Claude:\n{claude_response}\n")
            self.claude_messages.append(claude_response)
            time.sleep(1)
            
            # Gemini responde
            gemini_response = self.call_gemini()
            print(f"🧠 Gemini:\n{gemini_response}\n")
            self.gemini_messages.append(gemini_response)
            time.sleep(1)
            
            print("-" * 50 + "\n")
    
    def guardar_conversacion(self, archivo="conversacion_tres_modelos.txt"):
        """Guarda la conversación en un archivo"""
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write("=== CONVERSACIÓN ENTRE TRES MODELOS DE IA ===\n\n")
            
            max_len = max(len(self.gpt_messages), len(self.claude_messages), len(self.gemini_messages))
            
            for i in range(max_len):
                f.write(f"--- INTERCAMBIO {i + 1} ---\n")
                if i < len(self.gpt_messages):
                    f.write(f"GPT: {self.gpt_messages[i]}\n\n")
                if i < len(self.claude_messages):
                    f.write(f"Claude: {self.claude_messages[i]}\n\n")
                if i < len(self.gemini_messages):
                    f.write(f"Gemini: {self.gemini_messages[i]}\n\n")
                f.write("-" * 50 + "\n\n")
        
        print(f"Conversación guardada en: {archivo}")

def main():
    """Función principal"""
    print("Iniciando conversación entre tres modelos de IA...")
    
    # Verificar que las API keys estén configuradas
    if not all([os.getenv("OPENAI_API_KEY"), os.getenv("ANTHROPIC_API_KEY"), os.getenv("GOOGLE_API_KEY")]):
        print("❌ Error: Faltan API keys. Asegúrate de tener configuradas:")
        print("   - OPENAI_API_KEY")
        print("   - ANTHROPIC_API_KEY") 
        print("   - GOOGLE_API_KEY")
        return
    
    try:
        conversacion = ConversacionTresModelos()
        conversacion.ejecutar_conversacion(num_turnos=3)
        conversacion.guardar_conversacion()
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Conversación interrumpida por el usuario.")
    except Exception as e:
        print(f"\n❌ Error durante la conversación: {str(e)}")

if __name__ == "__main__":
    main()