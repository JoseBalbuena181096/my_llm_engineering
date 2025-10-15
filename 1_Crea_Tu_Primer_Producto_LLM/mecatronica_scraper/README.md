# MecatronicaScraper

Un scraper especializado para extraer información de sitios web relacionados con mecatrónica y robótica.

## Descripción

Este proyecto implementa un web scraper inteligente que puede extraer información relevante de sitios web educativos y comerciales relacionados con mecatrónica, robótica y automatización.

## Características

- Extracción automática de contenido web
- Filtrado inteligente de información relevante
- Manejo de diferentes tipos de sitios web
- Procesamiento de texto y limpieza de datos
- Exportación de resultados en diferentes formatos

## Archivos del Proyecto

- `mecatronica_robotica_scraper.py` - Script principal del scraper

## Uso

```python
from mecatronica_robotica_scraper import MecatronicaScraper

# Crear instancia del scraper
scraper = MecatronicaScraper()

# Extraer información de un sitio web
data = scraper.scrape_website("https://ejemplo.com")
```

## Requisitos

- Python 3.8+
- requests
- beautifulsoup4
- lxml

## Instalación

```bash
pip install requests beautifulsoup4 lxml
```

## Configuración

Asegúrate de tener configuradas las variables de entorno necesarias en tu archivo `.env`.