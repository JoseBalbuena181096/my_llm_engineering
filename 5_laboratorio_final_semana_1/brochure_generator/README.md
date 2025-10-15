# Generador de Folletos Empresariales

Un generador automático de folletos comerciales que analiza sitios web de empresas y crea contenido promocional personalizado.

## Descripción

Este proyecto utiliza web scraping e inteligencia artificial para analizar sitios web empresariales y generar automáticamente folletos comerciales atractivos y personalizados.

## Características

- **Análisis automático de sitios web**: Extrae información clave de empresas
- **Generación de contenido**: Crea folletos promocionales personalizados
- **Múltiples formatos**: Salida en Markdown y otros formatos
- **IA integrada**: Utiliza OpenAI GPT para generar contenido de calidad
- **Personalización**: Adapta el tono y estilo según el tipo de empresa

## Archivos del Proyecto

- `brochure_generator.py` - Script principal del generador
- `folleto_*.md` - Ejemplos de folletos generados
  - `folleto_frogames_formación_inglés.md`
  - `folleto_itsa.md`
  - `folleto_itsa_aleman.md`
  - `folleto_palmiras_ingles.md`

## Uso

```python
from brochure_generator import BrochureGenerator

# Crear instancia del generador
generator = BrochureGenerator()

# Generar folleto para una empresa
brochure = generator.generate_brochure("https://empresa.com")
```

## Configuración

Configura tu API key de OpenAI en el archivo `.env`:
```
OPENAI_API_KEY=tu_api_key_aqui
```

## Proceso de Generación

1. **Análisis del sitio web**: Extrae información relevante
2. **Procesamiento de contenido**: Identifica servicios, valores y características
3. **Generación de folleto**: Crea contenido promocional estructurado
4. **Formato y estilo**: Aplica formato profesional al folleto

## Tipos de Empresas Soportadas

- Empresas de formación y educación
- Servicios tecnológicos
- Consultorías
- Empresas de manufactura
- Servicios profesionales

## Ejemplos de Salida

Los folletos generados incluyen:
- Descripción de la empresa
- Servicios principales
- Valores y ventajas competitivas
- Información de contacto
- Call-to-action personalizado

## Requisitos

- Python 3.8+
- openai
- requests
- beautifulsoup4
- python-dotenv

## Instalación

```bash
pip install openai requests beautifulsoup4 python-dotenv
```