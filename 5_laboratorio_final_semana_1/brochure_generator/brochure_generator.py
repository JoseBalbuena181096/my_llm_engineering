#!/usr/bin/env python3
"""
Generador de Folletos Empresariales
Script extraído del notebook day5.ipynb que genera folletos para empresas
basándose en el análisis de sus sitios web.

Este script utiliza web scraping y OpenAI GPT para:
1. Analizar el contenido de un sitio web empresarial
2. Identificar enlaces relevantes automáticamente
3. Extraer información de múltiples páginas
4. Generar un folleto profesional en formato Markdown
"""

# ============================================================================
# IMPORTACIONES NECESARIAS
# ============================================================================
import os                    # Para variables de entorno
import requests             # Para realizar peticiones HTTP a sitios web
import json                 # Para manejar respuestas JSON de OpenAI
from dotenv import load_dotenv      # Para cargar variables de entorno desde .env
from bs4 import BeautifulSoup       # Para parsear y extraer contenido HTML
from openai import OpenAI           # Cliente oficial de OpenAI

# ============================================================================
# CONFIGURACIÓN INICIAL Y VALIDACIÓN
# ============================================================================

# Cargar variables de entorno desde el archivo .env
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Validar que la clave API de OpenAI esté configurada correctamente
if api_key and api_key[:8] == 'sk-proj-':
    print("✓ La clave de API parece buena")
else:
    print("❌ Puede haber un problema con tu clave API")
    exit(1)  # Terminar el programa si no hay API key válida

# Configuración del modelo de OpenAI a utilizar
MODEL = 'gpt-5-nano'   # Modelo eficiente y económico para esta tarea
openai = OpenAI()      # Inicializar el cliente de OpenAI

# ============================================================================
# CLASE PARA MANEJO DE SITIOS WEB
# ============================================================================

class Website:
    """
    Clase utilitaria para representar y procesar un sitio web.
    
    Esta clase se encarga de:
    - Descargar el contenido HTML de una URL
    - Extraer el texto limpio (sin scripts, estilos, etc.)
    - Obtener todos los enlaces de la página
    - Proporcionar métodos para acceder al contenido procesado
    """

    def __init__(self, url):
        """
        Constructor que inicializa el objeto Website.
        
        Args:
            url (str): La URL del sitio web a procesar
        """
        self.url = url
        
        # Realizar petición HTTP para obtener el contenido de la página
        response = requests.get(url)
        self.body = response.content
        
        # Crear objeto BeautifulSoup para parsear el HTML
        soup = BeautifulSoup(self.body, 'html.parser')
        
        # Extraer el título de la página (si existe)
        self.title = soup.title.string if soup.title else "Sin título"
        
        # Procesar el contenido del body
        if soup.body:
            # Eliminar elementos irrelevantes para el análisis de texto
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()  # Remover completamente estos elementos
            
            # Extraer texto limpio con saltos de línea como separadores
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""
        
        # Extraer todos los enlaces (href) de la página
        links = [link.get('href') for link in soup.find_all('a')]
        # Filtrar enlaces vacíos o None
        self.links = [link for link in links if link]

    def get_contents(self):
        """
        Método que devuelve el contenido formateado de la página.
        
        Returns:
            str: Título y contenido de la página en formato legible
        """
        return f"Título de la Web:\n{self.title}\nContenido de la Web:\n{self.text}\n\n"

# ============================================================================
# PROMPTS DEL SISTEMA PARA OPENAI
# ============================================================================

# Prompt para que GPT identifique enlaces relevantes
# Prompt mejorado con multi-shot prompting para identificar enlaces relevantes
link_system_prompt = """Se te proporciona una lista de enlaces que se encuentran en una página web. \
Puedes decidir cuáles de los enlaces serían los más relevantes para incluir en un folleto sobre la empresa, \
como enlaces a una página Acerca de, una página de la empresa, las carreras/empleos disponibles o páginas de Cursos/Packs.

Debes responder en JSON siguiendo estos ejemplos:

Ejemplo 1 - Empresa de tecnología:
{
    "links": [
        {"type": "Pagina Sobre nosotros", "url": "https://techcorp.com/about-us"},
        {"type": "Pagina de Servicios", "url": "https://techcorp.com/services"},
        {"type": "Pagina de Carreras", "url": "https://techcorp.com/careers"}
    ]
}

Ejemplo 2 - Empresa educativa:
{
    "links": [
        {"type": "Pagina Sobre nosotros", "url": "https://educacion.com/nosotros"},
        {"type": "Pagina de Cursos", "url": "https://educacion.com/cursos"},
        {"type": "Pagina de Testimonios", "url": "https://educacion.com/testimonios"},
        {"type": "Pagina de Contacto", "url": "https://educacion.com/contacto"}
    ]
}

Ejemplo 3 - Empresa de consultoría:
{
    "links": [
        {"type": "Pagina de Servicios", "url": "https://consultora.com/servicios"},
        {"type": "Pagina de Equipo", "url": "https://consultora.com/equipo"},
        {"type": "Pagina de Casos de Exito", "url": "https://consultora.com/casos-exito"}
    ]
}
"""

# Prompt para que GPT genere el folleto empresarial
# Prompt mejorado para que GPT genere el folleto empresarial con formato específico
system_prompt = """Eres un asistente especializado que analiza el contenido de varias páginas relevantes del sitio web de una empresa \
y crea un folleto profesional y atractivo para posibles clientes, inversores y nuevos empleados.

DEBES seguir EXACTAMENTE esta estructura en formato Markdown:

# 🏢 [Nombre de la Empresa]

## 📋 Resumen Ejecutivo
- Breve descripción de la empresa (2-3 líneas)
- Sector/industria principal
- Año de fundación (si está disponible)

## 🎯 Misión y Visión
### Misión
[Descripción de la misión de la empresa]

### Visión
[Descripción de la visión de la empresa]

## 🚀 Servicios y Productos Principales
- **Servicio/Producto 1**: Descripción breve
- **Servicio/Producto 2**: Descripción breve
- **Servicio/Producto 3**: Descripción breve

## 📚 Cursos y Formación (si aplica)
### Cursos Destacados:
- **Curso 1**: Descripción y duración
- **Curso 2**: Descripción y duración
- **Curso 3**: Descripción y duración

### Modalidades de Estudio:
- Presencial / Online / Híbrido

## 👥 Cultura Empresarial y Valores
- **Valor 1**: Descripción
- **Valor 2**: Descripción  
- **Valor 3**: Descripción

## 🎓 Oportunidades de Carrera
### Áreas de Trabajo:
- Área 1
- Área 2
- Área 3

### Beneficios para Empleados:
- Beneficio 1
- Beneficio 2
- Beneficio 3

## 🌟 Testimonios y Casos de Éxito
> "Testimonio de cliente/estudiante destacado"
> 
> — Nombre del Cliente/Estudiante

## 📞 Información de Contacto
- **Sitio Web**: [URL]
- **Email**: [si está disponible]
- **Teléfono**: [si está disponible]
- **Dirección**: [si está disponible]

---
*Folleto generado automáticamente basado en análisis web*

INSTRUCCIONES IMPORTANTES:
1. Usa emojis para hacer el folleto más atractivo visualmente
2. Si no tienes información para una sección, escribe "Información no disponible en el sitio web"
3. Mantén un tono profesional pero accesible
4. Prioriza la información más relevante y específica
5. Usa listas con viñetas para facilitar la lectura
6. Incluye citas textuales cuando sea posible para testimonios"""

# ============================================================================
# FUNCIONES PARA CONFIGURACIÓN DE IDIOMA
# ============================================================================

def set_output_language(base_prompt, language="Español"):
    """
    Integra la configuración de idioma directamente en el prompt del sistema.
    
    Esta función modifica el prompt base para incluir instrucciones específicas
    sobre el idioma de salida, asegurando que toda la respuesta del LLM
    se genere en el idioma especificado.
    
    Args:
        base_prompt (str): El prompt del sistema base
        language (str): Idioma deseado para la respuesta (por defecto: "Español")
        
    Returns:
        str: Prompt del sistema modificado con instrucciones de idioma
    """
    language_instruction = f"""

CONFIGURACIÓN DE IDIOMA:
- TODOS los textos, títulos, descripciones y contenido DEBEN generarse en {language}
- Mantén la estructura y formato Markdown, pero traduce TODO el contenido
- Si el idioma es diferente al español, adapta también los emojis y expresiones culturalmente apropiadas
- Los nombres propios de empresas y marcas se mantienen en su idioma original
"""
    
    return base_prompt + language_instruction

# ============================================================================
# FUNCIONES PARA PROCESAMIENTO DE ENLACES
# ============================================================================

def get_links_user_prompt(website):
    """
    Genera el prompt del usuario para obtener enlaces relevantes.
    
    Esta función crea un mensaje que se enviará a GPT con la lista de enlaces
    encontrados en el sitio web, pidiendo que identifique cuáles son relevantes.
    
    Args:
        website (Website): Objeto Website con los enlaces extraídos
        
    Returns:
        str: Prompt formateado para enviar a OpenAI
    """
    user_prompt = f"Aquí hay una lista de enlaces de la página web {website.url} - "
    user_prompt += "Por favor, decide cuáles de estos son enlaces web relevantes para un folleto sobre la empresa. Responde con la URL https completa en formato JSON. \
No incluyas Términos y Condiciones, Privacidad ni enlaces de correo electrónico.\n"
    user_prompt += "Links (puede que algunos sean links relativos):\n"
    user_prompt += "\n".join(website.links)  # Unir todos los enlaces con saltos de línea
    return user_prompt


def get_links(url):
    """
    Obtiene los enlaces relevantes de un sitio web usando OpenAI.
    
    Esta función:
    1. Crea un objeto Website para la URL dada
    2. Envía los enlaces a GPT para que identifique los relevantes
    3. Devuelve la respuesta en formato JSON
    
    Args:
        url (str): URL del sitio web a analizar
        
    Returns:
        dict: Diccionario con los enlaces relevantes identificados por GPT
    """
    website = Website(url)
    
    # Realizar llamada a OpenAI para identificar enlaces relevantes
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
        ],
        response_format={"type": "json_object"}  # Forzar respuesta en JSON
    )
    
    # Extraer y parsear la respuesta JSON
    result = response.choices[0].message.content
    return json.loads(result)

# ============================================================================
# FUNCIONES PARA RECOPILACIÓN DE INFORMACIÓN
# ============================================================================

def get_all_details(url):
    """
    Recopila todos los detalles de la página principal y enlaces relevantes.
    
    Esta función:
    1. Obtiene el contenido de la página principal
    2. Identifica enlaces relevantes usando GPT
    3. Visita cada enlace relevante y extrae su contenido
    4. Combina toda la información en un solo texto
    
    Args:
        url (str): URL del sitio web principal
        
    Returns:
        str: Texto combinado con toda la información recopilada
    """
    # Comenzar con el contenido de la página principal
    result = "Landing page:\n"
    result += Website(url).get_contents()
    
    # Obtener enlaces relevantes usando GPT
    links = get_links(url)
    print("Links encontrados:", links)  # Mostrar enlaces para debugging
    
    # Procesar cada enlace relevante
    for link in links["links"]:
        try:
            # Agregar sección para este enlace
            result += f"\n\n{link['type']}\n"
            # Obtener y agregar el contenido de este enlace
            result += Website(link["url"]).get_contents()
        except Exception as e:
            # Manejar errores (enlaces rotos, timeouts, etc.)
            print(f"Error procesando {link['url']}: {e}")
            continue  # Continuar con el siguiente enlace
    
    return result


def get_brochure_user_prompt(company_name, url):
    """
    Genera el prompt del usuario para crear el folleto.
    
    Esta función combina el nombre de la empresa con toda la información
    recopilada del sitio web para crear un prompt completo para GPT.
    
    Args:
        company_name (str): Nombre de la empresa
        url (str): URL del sitio web de la empresa
        
    Returns:
        str: Prompt completo para generar el folleto
    """
    user_prompt = f"Estás mirando una empresa llamada: {company_name}\n"
    user_prompt += f"Aquí se encuentra el contenido de su página de inicio y otras páginas relevantes; usa esta información para crear un breve folleto de la empresa en Markdown.\n"
    
    # Agregar toda la información recopilada
    user_prompt += get_all_details(url)
    
    # Truncar si es muy largo para evitar límites de tokens
    user_prompt = user_prompt[:20_000]  # Máximo 20,000 caracteres
    return user_prompt

def change_language_prompt(language):
    """
    Genera un prompt para cambiar el idioma de la respuesta.
    
    Args:
        language (str): Idioma deseado para la respuesta
        
    Returns:
        str: Prompt formateado para cambiar el idioma
    """
    return f"Por favor, genera todos tus resultados en el idioma {language}."

# ============================================================================
# FUNCIÓN PRINCIPAL PARA GENERAR FOLLETOS
# ============================================================================

def stream_brochure(company_name, url, language="Español"):
    """
    Genera un folleto empresarial con streaming de respuesta.
    
    Esta es la función principal que:
    1. Recopila información del sitio web
    2. Envía todo a GPT para generar el folleto
    3. Muestra la respuesta en tiempo real (streaming)
    4. Devuelve el texto completo del folleto
    
    Args:
        company_name (str): Nombre de la empresa
        url (str): URL del sitio web de la empresa
        language (str): Idioma para generar el folleto (por defecto: "Español")
        
    Returns:
        str: Texto completo del folleto generado, o None si hay error
    """
    print(f"🚀 Generando folleto para {company_name}...")
    print(f"📊 Analizando sitio web: {url}")
    print(f"🌍 Idioma de salida: {language}")
    
    try:
        # Crear el prompt del sistema con configuración de idioma integrada
        localized_system_prompt = set_output_language(system_prompt, language)
        
        # Crear stream de respuesta de OpenAI
        stream = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": localized_system_prompt},
                {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
            ],
            stream=True  # Habilitar streaming para mostrar respuesta en tiempo real
        )
        
        # Mostrar encabezado
        print(f"\n📄 Folleto para {company_name}:")
        print("=" * 50)
        
        # Procesar y mostrar la respuesta en tiempo real
        response = ""
        for chunk in stream:
            # Verificar si el chunk contiene contenido
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                response += content  # Acumular respuesta completa
                print(content, end='', flush=True)  # Mostrar inmediatamente
        
        # Mostrar mensaje de finalización
        print("\n" + "=" * 50)
        print("✅ Folleto generado exitosamente!")
        
        return response
        
    except Exception as e:
        # Manejar cualquier error durante la generación
        print(f"❌ Error generando el folleto: {e}")
        return None

# ============================================================================
# FUNCIONES AUXILIARES PARA USO PERSONALIZADO
# ============================================================================

def generate_custom_brochure(company_name, url, language="Español", output_file=None):
    """
    Función auxiliar para generar folletos con parámetros personalizados.
    
    Esta función permite usar el generador de folletos con parámetros específicos
    sin modificar la función main, ideal para uso programático o desde otros scripts.
    
    Args:
        company_name (str): Nombre de la empresa
        url (str): URL del sitio web de la empresa
        language (str): Idioma para generar el folleto (por defecto: "Español")
        output_file (str): Nombre del archivo de salida (opcional)
        
    Returns:
        tuple: (resultado_texto, nombre_archivo) o (None, None) si hay error
    """
    print("🏢 Generador de Folletos Empresariales - Modo Personalizado")
    print("=" * 55)
    
    # Generar el folleto con los parámetros especificados
    result = stream_brochure(company_name, url, language)
    
    # Si la generación fue exitosa, guardar en archivo
    if result:
        # Determinar el nombre del archivo de salida
        if output_file is None:
            language_suffix = f"_{language.lower()}" if language != "Español" else ""
            output_file = f"folleto_{company_name.replace(' ', '_').lower()}{language_suffix}.md"
        
        # Guardar el folleto en archivo Markdown
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Folleto Empresarial: {company_name}\n\n")
            f.write(result)
        
        print(f"\n💾 Folleto guardado en: {output_file}")
        return result, output_file
    else:
        return None, None

# ============================================================================
# FUNCIÓN PRINCIPAL DEL PROGRAMA
# ============================================================================

def main(language="Español"):
    """
    Función principal del script.
    
    Esta función:
    1. Muestra el título del programa
    2. Define los parámetros de la empresa a analizar
    3. Ejecuta la generación del folleto
    4. Guarda el resultado en un archivo Markdown
    
    Args:
        language (str): Idioma para generar el folleto (por defecto: "Español")
    """
    print("🏢 Generador de Folletos Empresariales")
    print("=" * 40)
    
    # Configuración de la empresa a analizar
    # (Puedes cambiar estos valores para analizar otras empresas)
    company_name = "Frogames Formación"
    url = "https://cursos.frogamesformacion.com"
    
    # Generar el folleto con el idioma especificado
    result = stream_brochure(company_name, url, language)
    
    # Si la generación fue exitosa, guardar en archivo
    if result:
        # Crear nombre de archivo basado en el nombre de la empresa y el idioma
        language_suffix = f"_{language.lower()}" if language != "Español" else ""
        output_file = f"folleto_{company_name.replace(' ', '_').lower()}{language_suffix}.md"
        
        # Guardar el folleto en archivo Markdown
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Folleto Empresarial: {company_name}\n\n")
            f.write(result)
        
        print(f"\n💾 Folleto guardado en: {output_file}")

# ============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    """
    Punto de entrada del script.
    
    Esta condición asegura que main() solo se ejecute cuando el script
    se ejecuta directamente (no cuando se importa como módulo).
    """
    main()