# 🔧 Configuración de Otras APIs

Este directorio contiene scripts y configuraciones para trabajar con múltiples APIs de modelos de lenguaje (LLMs), incluyendo OpenAI GPT, Anthropic Claude y Google Gemini.

## 📁 Contenido del Directorio

### 🐍 Scripts Python

#### `conversacion_tres_modelos.py`
Script principal que permite realizar conversaciones utilizando tres modelos de IA diferentes:
- **OpenAI GPT-4** - Para análisis y respuestas generales
- **Anthropic Claude** - Para análisis detallado y razonamiento
- **Google Gemini** - Para perspectivas adicionales y validación

**Características:**
- Configuración de roles específicos para cada modelo
- Manejo de historial de conversación
- Guardado automático de resultados
- Manejo de errores y reintentos

#### `educacion_mexico_claude_vs_gpt.py`
Script especializado que simula un debate entre Claude y GPT sobre la desconexión entre la educación universitaria y el mercado laboral en México.

**Características:**
- **Personas expertas definidas:**
  - GPT: Experto en tecnología y transformación digital
  - Claude: Experto en políticas educativas y desarrollo social
- **Enfoque específico:** Soluciones tecnológicas (IA, internet) para reducir costos
- **Intercambio estructurado:** 10 mensajes por modelo
- **Salida dual:** Formato texto (.txt) y Markdown (.md)
- **Conversión automática:** Usa GPT para generar formato Markdown profesional

### 📄 Archivos de Salida

#### `conversacion_tres_modelos.txt`
Resultado de la conversación entre los tres modelos, incluyendo:
- Intercambios completos entre modelos
- Análisis y perspectivas de cada IA
- Resumen final consolidado

#### `debate_educacion_mexico.md`
Debate formateado en Markdown sobre educación en México, con:
- Estructura profesional con encabezados
- Blockquotes para propuestas importantes
- Listas organizadas de soluciones
- Texto destacado y emojis
- Separadores visuales

### 📓 Notebooks

#### `day1.ipynb`
Jupyter Notebook con ejercicios y ejemplos prácticos para:
- Configuración inicial de APIs
- Pruebas de conectividad
- Ejemplos de uso básico
- Troubleshooting común

### ⚙️ Archivos de Configuración

#### `.env`
Archivo de variables de entorno que contiene las claves API:
```
OPENAI_API_KEY=tu_clave_openai
ANTHROPIC_API_KEY=tu_clave_anthropic
GOOGLE_API_KEY=tu_clave_google
```

#### `test_google.json`
Archivo de configuración para pruebas específicas de la API de Google Gemini.

### 📝 Documentación

#### `Notas.md`
Notas y apuntes sobre:
- Configuración de APIs
- Problemas encontrados y soluciones
- Mejores prácticas

## 🚀 Instalación y Configuración

### Prerrequisitos
```bash
# Activar el entorno conda
conda activate llms

# Instalar dependencias
pip install openai anthropic google-generativeai python-dotenv
```

### Configuración de APIs
1. Copia el archivo `.env.example` a `.env`
2. Agrega tus claves API en el archivo `.env`
3. Asegúrate de que el archivo `.env` esté en el directorio correcto

## 💡 Uso

### Conversación con Tres Modelos
```bash
python conversacion_tres_modelos.py
```

### Debate sobre Educación en México
```bash
python educacion_mexico_claude_vs_gpt.py
```

## 🔍 Características Técnicas

### Manejo de APIs
- **Reintentos automáticos** en caso de errores
- **Rate limiting** respetado para cada API
- **Manejo de errores** robusto
- **Logging** detallado para debugging

### Formatos de Salida
- **Texto plano** para análisis programático
- **Markdown** para presentación profesional
- **Estructura organizada** con metadatos

### Modelos Utilizados
- **GPT-4**: `gpt-4` (OpenAI)
- **Claude**: `claude-3-sonnet-20240229` (Anthropic)
- **Gemini**: `gemini-flash-latest` (Google)

## 🛠️ Troubleshooting

### Errores Comunes
1. **ModuleNotFoundError**: Verificar instalación de dependencias
2. **API Key Error**: Verificar configuración en `.env`
3. **Rate Limit**: Esperar y reintentar
4. **Model Not Found**: Verificar nombres de modelos actualizados

### Logs y Debugging
Los scripts incluyen logging detallado para facilitar la identificación de problemas.

## 📊 Resultados Esperados

Los scripts generan debates y conversaciones estructuradas que incluyen:
- Análisis multidimensional de problemas
- Propuestas de solución innovadoras
- Perspectivas complementarias de diferentes modelos
- Formato profesional para presentación

## 🔄 Actualizaciones

Este directorio se actualiza regularmente con:
- Nuevos modelos y APIs
- Mejoras en el manejo de errores
- Optimizaciones de rendimiento
- Nuevos casos de uso y ejemplos

---

**Nota**: Asegúrate de mantener tus claves API seguras y nunca las subas a repositorios públicos.