# 🔬 Laboratorio Final - Semana 1

Este módulo contiene los proyectos finales integrados que combinan todos los conocimientos adquiridos durante la primera semana del curso de Ingeniería de LLM.

## 🎯 Proyectos Principales

### 🤖 Tutor de Robótica Inteligente

Un sistema de tutoría personalizado que adapta su enseñanza según el nivel educativo del estudiante.

#### Archivos Principales:
- `tutor_robotica.py` - Versión con OpenAI API
- `tutor_robotica_local.py` - Versión con Ollama (modelos locales)
- `prompts/` - Directorio con prompts especializados por nivel

#### Características:
- ✅ **Adaptación por Edad**: Preescolar, Primaria, Secundaria, Preparatoria
- ✅ **Multiidioma**: Español, Inglés, Francés, Alemán, etc.
- ✅ **Temas Especializados**: Arduino, Electrónica, Mecatrónica, Programación
- ✅ **Prompts Multi-shot**: Optimizados para cada nivel educativo
- ✅ **Interfaz Interactiva**: Menús intuitivos y ejemplos contextuales

#### Uso:
```bash
# Versión OpenAI (requiere API key)
python tutor_robotica.py

# Versión Local (requiere Ollama)
python tutor_robotica_local.py
```

#### Configuración:
1. Para OpenAI: Configurar `OPENAI_API_KEY` en `.env`
2. Para Ollama: Instalar y ejecutar `ollama serve`

---

### 📄 Generador de Folletos Empresariales

Sistema automatizado que analiza sitios web y genera folletos profesionales.

#### Archivo Principal:
- `brochure_generator.py` - Generador completo con web scraping

#### Características:
- ✅ **Web Scraping Inteligente**: Extrae contenido relevante automáticamente
- ✅ **Análisis de Enlaces**: Identifica páginas importantes (About, Services, etc.)
- ✅ **Generación Estructurada**: Folletos en formato Markdown profesional
- ✅ **Multiidioma**: Soporte para diferentes idiomas de salida
- ✅ **Personalización**: Adaptable a diferentes tipos de empresas

#### Uso:
```bash
python brochure_generator.py
```

#### Ejemplos Generados:
- `folleto_frogames_formación_inglés.md`
- `folleto_itsa.md`
- `folleto_itsa_aleman.md`
- `folleto_palmiras_ingles.md`

---

### 🧪 Scripts de Prueba y Utilidades

#### `test_languages.py`
Script para probar el soporte multiidioma del tutor de robótica.

#### Notebooks Jupyter:
- `day5.ipynb` - Desarrollo paso a paso del laboratorio
- `day5_base.ipynb` - Versión base para ejercicios
- `week1 EXERCISE.ipynb` - Ejercicios de la semana 1
- `Notas.ipynb` - Notas y conceptos teóricos

## 🛠️ Configuración del Entorno

### Dependencias Requeridas:
```bash
pip install openai python-dotenv requests beautifulsoup4 ollama
```

### Variables de Entorno:
```bash
# Crear archivo .env
OPENAI_API_KEY=tu_clave_api_aqui
```

### Para Modelos Locales:
```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar modelo
ollama pull llama2

# Iniciar servidor
ollama serve
```

## 🎓 Niveles Educativos Soportados

### 🧸 Preescolar (3-6 años)
- Vocabulario simple y conceptos básicos
- Ejemplos cotidianos y juegos
- Enfoque en exploración y diversión

### 📚 Primaria (6-12 años)
- Conceptos básicos con experimentos sencillos
- Vocabulario básico técnico
- Proyectos prácticos y tangibles

### 🔬 Secundaria (12-15 años)
- Conceptos intermedios estructurados
- Vocabulario técnico básico
- Proyectos con componentes reales

### 🎯 Preparatoria (15-18 años)
- Conceptos avanzados y aplicaciones reales
- Vocabulario técnico avanzado
- Proyectos profesionales y complejos

## 🌍 Idiomas Soportados

- 🇪🇸 Español
- 🇺🇸 Inglés
- 🇫🇷 Francés
- 🇩🇪 Alemán
- 🇮🇹 Italiano
- 🇵🇹 Portugués
- Y más...

## 📊 Estructura del Módulo

```
5_laboratorio_final_semana_1/
├── README.md                          # Este archivo
├── day5.ipynb                        # Notebook principal del laboratorio
├── day5_base.ipynb                   # Notebook base
├── week1 EXERCISE.ipynb              # Ejercicios de la semana 1
├── Notas.ipynb                       # Notas y apuntes
├── tutor_robotica/                   # Proyecto Tutor Inteligente
│   ├── README.md                     # Documentación del proyecto
│   ├── tutor_robotica.py            # Versión con OpenAI
│   ├── tutor_robotica_local.py      # Versión con Ollama
│   ├── test_languages.py            # Tests de idiomas
│   └── prompts/                     # Prompts por nivel educativo
│       ├── preescolar.txt
│       ├── primaria.txt
│       ├── secundaria.txt
│       └── preparatoria.txt
└── brochure_generator/               # Proyecto Generador de Folletos
    ├── README.md                     # Documentación del proyecto
    ├── brochure_generator.py         # Script principal
    ├── folleto_frogames_formación_inglés.md
    ├── folleto_itsa.md
    ├── folleto_itsa_aleman.md
    └── folleto_palmiras_ingles.md
```

## 📊 Estructura de Prompts

Los prompts están organizados por nivel educativo en el directorio `prompts/`:

```
prompts/
├── preescolar.txt    # Prompts para 3-6 años
├── primaria.txt      # Prompts para 6-12 años
├── secundaria.txt    # Prompts para 12-15 años
└── preparatoria.txt  # Prompts para 15-18 años
```

## 🚀 Ejemplos de Uso

### Tutor de Robótica - Sesión Típica:
1. Seleccionar nivel educativo
2. Elegir idioma de enseñanza
3. Hacer preguntas sobre robótica, Arduino, etc.
4. Recibir explicaciones adaptadas al nivel

### Generador de Folletos - Proceso:
1. Ingresar URL de la empresa
2. El sistema analiza el sitio web
3. Extrae información relevante
4. Genera folleto profesional en Markdown

## 🔧 Solución de Problemas

### Error: "No module named 'ollama'"
```bash
pip install ollama
```

### Error: "Connection refused" (Ollama)
```bash
ollama serve
```

### Error: "Invalid API key" (OpenAI)
- Verificar que la clave API esté correcta en `.env`
- Asegurar que la clave tenga créditos disponibles

## 📈 Próximos Pasos

- [ ] Integración con más modelos locales
- [ ] Interfaz web para el tutor
- [ ] Exportación de folletos a PDF
- [ ] Sistema de evaluación de aprendizaje
- [ ] Base de datos de preguntas frecuentes

---

**Desarrollado como proyecto final de la Semana 1 - Ingeniería de LLM** 🎓