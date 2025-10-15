#!/usr/bin/env python3
"""
Script para conversación entre Claude y GPT como expertos en educación y tecnología
Tema: Soluciones al problema de desconexión entre educación universitaria y mundo laboral en México
Enfoque: Uso de IA, tecnología e internet para soluciones accesibles y de bajo costo
"""

import os
import openai
import anthropic
from dotenv import load_dotenv
import time

# Cargar variables de entorno
load_dotenv()

# Configurar APIs
openai.api_key = os.getenv("OPENAI_API_KEY")
claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Configuración de modelos
GPT_MODEL = "gpt-4o-mini"
CLAUDE_MODEL = "claude-3-haiku-20240307"

# Personalidades de los expertos
GPT_SYSTEM = """Eres un experto en tecnología educativa y transformación digital con amplia experiencia en México. 
Tu enfoque es pragmático y orientado a resultados. Te especializas en:
- Implementación de tecnologías educativas de bajo costo
- Plataformas digitales para capacitación laboral
- Soluciones de IA para democratizar el acceso a la educación
- Modelos de negocio sostenibles para EdTech en economías emergentes

Siempre propones soluciones concretas, factibles y escalables. Consideras las limitaciones económicas 
de México y buscas maximizar el impacto con recursos limitados. Eres directo y práctico en tus propuestas."""

CLAUDE_SYSTEM = """Eres un experto en políticas educativas y desarrollo social con profundo conocimiento del contexto mexicano.
Tu enfoque es holístico y considera los aspectos sociales, económicos y culturales. Te especializas en:
- Análisis de brechas entre educación superior y mercado laboral
- Políticas públicas para inclusión digital
- Programas de capacitación para poblaciones vulnerables
- Ecosistemas de innovación social y tecnológica

Eres reflexivo, empático y siempre consideras el impacto social de las soluciones tecnológicas. 
Buscas equilibrar la innovación con la equidad y la sostenibilidad social."""

class ConversacionEducacionMexico:
    def __init__(self):
        # Mensaje inicial que establece el contexto del debate
        self.tema_inicial = """El problema: En México existe una gran desconexión entre lo que se enseña en las universidades 
        y las habilidades que demanda el mercado laboral actual. Muchos graduados no encuentran empleo en su área, 
        mientras que las empresas no encuentran talento con las competencias necesarias. Además, la mayoría de la 
        población tiene recursos económicos limitados para acceder a capacitación adicional o programas de reconversión laboral.
        
        ¿Cómo podemos usar la inteligencia artificial, internet y tecnología en general para crear soluciones 
        accesibles y de bajo costo que ayuden a cerrar esta brecha?"""
        
        self.gpt_messages = []
        self.claude_messages = []
        
    def call_gpt(self, turno):
        """Llama a GPT con el contexto de la conversación"""
        messages = [{"role": "system", "content": GPT_SYSTEM}]
        
        if turno == 0:
            # Primer mensaje: presentar el problema
            messages.append({"role": "user", "content": f"Contexto del debate:\n{self.tema_inicial}\n\nComo experto en tecnología educativa, ¿cuál es tu análisis inicial del problema y qué soluciones tecnológicas propones?"})
        else:
            # Construir historial de la conversación
            messages.append({"role": "user", "content": f"Contexto del debate:\n{self.tema_inicial}"})
            
            for i in range(len(self.claude_messages)):
                if i < len(self.gpt_messages):
                    messages.append({"role": "assistant", "content": self.gpt_messages[i]})
                messages.append({"role": "user", "content": f"El experto en políticas educativas responde: {self.claude_messages[i]}"})
            
            messages.append({"role": "user", "content": "Continúa el debate con tu siguiente propuesta o respuesta a los puntos planteados."})
        
        try:
            completion = openai.chat.completions.create(
                model=GPT_MODEL,
                messages=messages,
                max_tokens=400,
                temperature=0.7
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error en GPT: {str(e)}"
    
    def call_claude(self, turno):
        """Llama a Claude con el contexto de la conversación"""
        messages = []
        
        if turno == 0:
            # Primer mensaje: responder al análisis de GPT
            if self.gpt_messages:
                messages.append({"role": "user", "content": f"Contexto del debate:\n{self.tema_inicial}\n\nEl experto en tecnología educativa dice: {self.gpt_messages[0]}\n\nComo experto en políticas educativas, ¿cuál es tu perspectiva sobre este análisis y qué complementarías o matizarías?"})
        else:
            # Construir historial de la conversación
            messages.append({"role": "user", "content": f"Contexto del debate:\n{self.tema_inicial}"})
            
            for i in range(len(self.gpt_messages)):
                messages.append({"role": "user", "content": f"Experto en tecnología: {self.gpt_messages[i]}"})
                if i < len(self.claude_messages):
                    messages.append({"role": "assistant", "content": self.claude_messages[i]})
            
            messages.append({"role": "user", "content": "Continúa el debate con tu siguiente análisis o propuesta."})
        
        try:
            message = claude.messages.create(
                model=CLAUDE_MODEL,
                system=CLAUDE_SYSTEM,
                messages=messages,
                max_tokens=400
            )
            return message.content[0].text
        except Exception as e:
            return f"Error en Claude: {str(e)}"
    
    def ejecutar_debate(self, num_mensajes=10):
        """Ejecuta el debate entre los dos expertos"""
        print("=== DEBATE: EDUCACIÓN UNIVERSITARIA Y MUNDO LABORAL EN MÉXICO ===\n")
        print("🚀 GPT - Experto en Tecnología Educativa (Enfoque Pragmático)")
        print("🎓 Claude - Experto en Políticas Educativas (Enfoque Holístico)")
        print("\n" + "="*80 + "\n")
        
        print("📋 CONTEXTO DEL DEBATE:")
        print(self.tema_inicial)
        print("\n" + "="*80 + "\n")
        
        for turno in range(num_mensajes):
            print(f"--- INTERCAMBIO {turno + 1} ---\n")
            
            # GPT inicia o responde
            gpt_response = self.call_gpt(turno)
            print(f"🚀 EXPERTO EN TECNOLOGÍA EDUCATIVA (GPT):\n{gpt_response}\n")
            self.gpt_messages.append(gpt_response)
            time.sleep(2)  # Pausa para evitar rate limits
            
            # Claude responde
            claude_response = self.call_claude(turno)
            print(f"🎓 EXPERTO EN POLÍTICAS EDUCATIVAS (Claude):\n{claude_response}\n")
            self.claude_messages.append(claude_response)
            time.sleep(2)
            
            print("-" * 80 + "\n")
    
    def generar_resumen_final(self):
        """Genera un resumen final de las propuestas discutidas"""
        print("=== RESUMEN EJECUTIVO DE PROPUESTAS ===\n")
        
        # Llamar a GPT para generar resumen
        messages = [
            {"role": "system", "content": "Eres un analista experto que debe crear un resumen ejecutivo conciso de las principales propuestas discutidas en el debate sobre educación y tecnología en México."},
            {"role": "user", "content": f"Basándote en este debate completo, crea un resumen ejecutivo con las 5 propuestas más viables y concretas que surgieron:\n\nDebate completo:\n{self._obtener_debate_completo()}"}
        ]
        
        try:
            completion = openai.chat.completions.create(
                model=GPT_MODEL,
                messages=messages,
                max_tokens=500,
                temperature=0.3
            )
            resumen = completion.choices[0].message.content
            print(f"📊 RESUMEN EJECUTIVO:\n{resumen}\n")
            return resumen
        except Exception as e:
            print(f"Error generando resumen: {str(e)}")
            return ""
    
    def _obtener_debate_completo(self):
        """Obtiene el texto completo del debate"""
        debate_completo = ""
        max_len = max(len(self.gpt_messages), len(self.claude_messages))
        
        for i in range(max_len):
            if i < len(self.gpt_messages):
                debate_completo += f"GPT: {self.gpt_messages[i]}\n\n"
            if i < len(self.claude_messages):
                debate_completo += f"Claude: {self.claude_messages[i]}\n\n"
        
        return debate_completo
    
    def convertir_a_markdown(self):
        """Convierte el debate completo a formato Markdown usando GPT"""
        debate_texto = self._obtener_debate_completo()
        
        prompt_conversion = f"""Convierte el siguiente debate entre expertos a un formato Markdown profesional y bien estructurado.

INSTRUCCIONES:
- Usa encabezados apropiados (##, ###)
- Formatea las citas y propuestas con > (blockquotes)
- Usa listas con viñetas para las propuestas
- Resalta conceptos importantes con **negrita**
- Usa emojis apropiados para hacer más visual
- Estructura el contenido de manera clara y profesional
- Mantén todo el contenido técnico y las propuestas

CONTEXTO DEL DEBATE:
{self.tema_inicial}

DEBATE A CONVERTIR:
{debate_texto}

Genera un documento Markdown completo, profesional y bien estructurado."""

        try:
            completion = openai.chat.completions.create(
                model=GPT_MODEL,
                messages=[
                    {"role": "system", "content": "Eres un experto en documentación técnica y formato Markdown. Creas documentos profesionales, bien estructurados y visualmente atractivos."},
                    {"role": "user", "content": prompt_conversion}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error convirtiendo a Markdown: {str(e)}")
            return None

    def guardar_debate(self, archivo_txt="debate_educacion_mexico.txt", archivo_md="debate_educacion_mexico.md"):
        """Guarda el debate completo en formato texto y Markdown"""
        
        # Guardar en formato texto original
        with open(archivo_txt, 'w', encoding='utf-8') as f:
            f.write("=== DEBATE: EDUCACIÓN UNIVERSITARIA Y MUNDO LABORAL EN MÉXICO ===\n\n")
            f.write("PARTICIPANTES:\n")
            f.write("🚀 GPT - Experto en Tecnología Educativa (Enfoque Pragmático)\n")
            f.write("🎓 Claude - Experto en Políticas Educativas (Enfoque Holístico)\n\n")
            
            f.write("CONTEXTO:\n")
            f.write(f"{self.tema_inicial}\n\n")
            f.write("="*80 + "\n\n")
            
            max_len = max(len(self.gpt_messages), len(self.claude_messages))
            
            for i in range(max_len):
                f.write(f"--- INTERCAMBIO {i + 1} ---\n\n")
                if i < len(self.gpt_messages):
                    f.write(f"🚀 EXPERTO EN TECNOLOGÍA EDUCATIVA (GPT):\n{self.gpt_messages[i]}\n\n")
                if i < len(self.claude_messages):
                    f.write(f"🎓 EXPERTO EN POLÍTICAS EDUCATIVAS (Claude):\n{self.claude_messages[i]}\n\n")
                f.write("-" * 80 + "\n\n")
            
            # Agregar resumen si existe
            resumen = self.generar_resumen_final()
            if resumen:
                f.write("=== RESUMEN EJECUTIVO ===\n\n")
                f.write(resumen)
        
        print(f"💾 Debate en formato texto guardado en: {archivo_txt}")
        
        # Convertir y guardar en formato Markdown
        print("🔄 Convirtiendo debate a formato Markdown...")
        markdown_content = self.convertir_a_markdown()
        
        if markdown_content:
            with open(archivo_md, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"📝 Debate en formato Markdown guardado en: {archivo_md}")
        else:
            print("❌ Error al convertir a Markdown")

def main():
    """Función principal"""
    print("🇲🇽 Iniciando debate sobre educación y tecnología en México...\n")
    
    # Verificar que las API keys estén configuradas
    if not all([os.getenv("OPENAI_API_KEY"), os.getenv("ANTHROPIC_API_KEY")]):
        print("❌ Error: Faltan API keys. Asegúrate de tener configuradas:")
        print("   - OPENAI_API_KEY")
        print("   - ANTHROPIC_API_KEY")
        return
    
    try:
        debate = ConversacionEducacionMexico()
        debate.ejecutar_debate(num_mensajes=10)  # 10 mensajes por modelo
        debate.guardar_debate()
        
        print("\n🎉 Debate completado exitosamente!")
        print("📄 Revisa los archivos generados:")
        print("   - debate_educacion_mexico.txt (formato texto)")
        print("   - debate_educacion_mexico.md (formato Markdown)")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Debate interrumpido por el usuario.")
    except Exception as e:
        print(f"\n❌ Error durante el debate: {str(e)}")

if __name__ == "__main__":
    main()