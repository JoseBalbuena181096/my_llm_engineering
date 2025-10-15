# 🚀 Crea Tu Primer Producto LLM

Este módulo introduce los fundamentos para desarrollar tu primera solución basada en Modelos de Lenguaje Grande (LLM).

## 📋 Contenido del Módulo

### 📓 Notebooks y Documentación
- `day1.ipynb` - Tutorial paso a paso del primer día
- `test.ipynb` - Notebook de pruebas y experimentación
- `Notas.md` - Notas teóricas y conceptos fundamentales

### 🔧 Proyectos Prácticos
- `mecatronica_scraper/` - Directorio del proyecto MecatronicaScraper
  - `mecatronica_robotica_scraper.py` - Script principal del scraper
  - `README.md` - Documentación del proyecto

### 🖼️ Recursos
- `image.png` - Diagrama de temas del curso

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ✅ Configurar un entorno de desarrollo para LLMs
- ✅ Realizar tu primera integración con APIs de LLM
- ✅ Implementar web scraping para alimentar modelos
- ✅ Crear soluciones prácticas con casos de uso reales
- ✅ Entender los fundamentos de prompting efectivo

## 🛠️ Configuración Inicial

### 1. Entorno de Desarrollo

#### Con Anaconda (Recomendado):
```bash
# Crear entorno
conda create -n llm_env python=3.9
conda activate llm_env

# Instalar Jupyter
conda install jupyter

# Iniciar Jupyter
jupyter notebook --no-browser
```

#### Con Python Virtual Environment:
```bash
# Crear entorno virtual
python -m venv llm_env
source llm_env/bin/activate  # Linux/Mac
llm_env\Scripts\activate     # Windows

# Instalar dependencias
pip install jupyter openai python-dotenv requests beautifulsoup4
```

### 2. Configuración de APIs

#### OpenAI API:
1. Crear cuenta en [OpenAI Platform](https://platform.openai.com/)
2. Generar clave API
3. Crear archivo `.env`:
```bash
OPENAI_API_KEY=tu_clave_api_aqui
```

### 3. Verificación de Instalación
```bash
# Activar entorno
conda activate llm_env

# Iniciar Jupyter
jupyter notebook
```

## 📚 Temas Cubiertos

### Día 1: Fundamentos
- Introducción a LLMs y sus aplicaciones
- Configuración del entorno de desarrollo
- Primera integración con OpenAI API
- Conceptos básicos de prompting

### Conceptos Clave:
- **APIs de LLM**: Integración con servicios externos
- **Web Scraping**: Extracción de datos para alimentar modelos
- **Prompting**: Técnicas para obtener mejores respuestas
- **Casos de Uso**: Aplicaciones prácticas en el mundo real

## 🔍 Proyecto Principal: Scraper de Mecatrónica

### Descripción
El `mecatronica_robotica_scraper.py` es una herramienta especializada que:

- 🌐 Extrae contenido técnico de sitios web
- 🤖 Procesa información de robótica y mecatrónica
- 📊 Estructura datos para análisis posterior
- 🔧 Proporciona base para aplicaciones LLM

### Características:
- Scraping inteligente con BeautifulSoup
- Filtrado de contenido relevante
- Manejo de errores y timeouts
- Exportación de datos estructurados

### Uso:
```python
from mecatronica_robotica_scraper import MecatronicaScraper

scraper = MecatronicaScraper()
data = scraper.scrape_website("https://ejemplo.com")
```

## 📖 Recursos de Aprendizaje

### Documentación Oficial:
- [OpenAI API Docs](https://platform.openai.com/docs)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Documentation](https://docs.python-requests.org/)

### Tutoriales Recomendados:
- Jupyter Notebook básico
- Python para web scraping
- Fundamentos de APIs REST

## 🧪 Ejercicios Prácticos

### Ejercicio 1: Primera Consulta LLM
Implementar una consulta básica a OpenAI API para generar texto.

### Ejercicio 2: Web Scraping Básico
Extraer información de una página web usando BeautifulSoup.

### Ejercicio 3: Integración Completa
Combinar scraping con LLM para procesar contenido web.

## 🔧 Solución de Problemas Comunes

### Error: "Module not found"
```bash
pip install nombre_del_modulo
```

### Error: "Invalid API key"
- Verificar que la clave esté correcta en `.env`
- Confirmar que la clave tenga créditos disponibles

### Error: "Connection timeout"
- Verificar conexión a internet
- Revisar configuración de proxy si aplica

## 📈 Próximos Pasos

Después de completar este módulo:

1. **Módulo 2**: Modelos Locales con Ollama
2. **Módulo 3**: Modelos de Frontera
3. **Módulo 4**: Teoría de Transformers
4. **Módulo 5**: Laboratorio Final

## 💡 Consejos para el Éxito

- 🎯 **Practica regularmente**: Los conceptos se asimilan mejor con práctica constante
- 📝 **Toma notas**: Documenta tus aprendizajes y experimentos
- 🤝 **Colabora**: Comparte dudas y soluciones con otros estudiantes
- 🔍 **Experimenta**: Prueba variaciones de los ejemplos dados

---

**¡Bienvenido al mundo de la Ingeniería de LLM!** 🎓