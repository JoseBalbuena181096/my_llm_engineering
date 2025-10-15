# Tutor Inteligente de Robótica

Un tutor personalizado basado en IA para el aprendizaje de robótica y mecatrónica, adaptado a diferentes niveles educativos.

## Descripción

Este proyecto implementa un tutor inteligente que utiliza modelos de lenguaje (tanto OpenAI como modelos locales con Ollama) para proporcionar educación personalizada en robótica y mecatrónica.

## Características

- **Múltiples niveles educativos**: Preescolar, Primaria, Secundaria, Preparatoria
- **Soporte multiidioma**: Español, Inglés, Francés, Alemán, Italiano, Portugués
- **Modelos flexibles**: Compatible con OpenAI GPT y modelos locales (Ollama)
- **Prompts especializados**: Contenido adaptado por nivel educativo
- **Interfaz interactiva**: Conversación natural con el tutor

## Archivos del Proyecto

- `tutor_robotica.py` - Versión con OpenAI GPT
- `tutor_robotica_local.py` - Versión con modelos locales (Ollama)
- `test_languages.py` - Script de prueba para diferentes idiomas
- `prompts/` - Carpeta con prompts especializados por nivel
  - `preescolar.txt` - Prompts para nivel preescolar
  - `primaria.txt` - Prompts para nivel primaria
  - `secundaria.txt` - Prompts para nivel secundaria
  - `preparatoria.txt` - Prompts para nivel preparatoria

## Uso

### Versión OpenAI
```bash
python tutor_robotica.py
```

### Versión Local (Ollama)
```bash
python tutor_robotica_local.py
```

## Configuración

### Para OpenAI
Configura tu API key en el archivo `.env`:
```
OPENAI_API_KEY=tu_api_key_aqui
```

### Para Ollama
1. Instala Ollama
2. Descarga un modelo compatible (ej: `gpt-oss:20b`)
3. Inicia el servidor: `ollama serve`

## Niveles Educativos Soportados

1. **Preescolar (3-5 años)**: Conceptos básicos con analogías simples
2. **Primaria (6-11 años)**: Introducción a la robótica de forma lúdica
3. **Secundaria (12-14 años)**: Fundamentos técnicos básicos
4. **Preparatoria (15-18 años)**: Conceptos avanzados y aplicaciones

## Idiomas Soportados

- Español (es)
- Inglés (en)
- Francés (fr)
- Alemán (de)
- Italiano (it)
- Portugués (pt)

## Requisitos

- Python 3.8+
- openai (para versión OpenAI)
- ollama (para versión local)
- python-dotenv