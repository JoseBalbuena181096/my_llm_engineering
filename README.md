# Ingeniería de LLM - Proyecto de Aprendizaje

Un proyecto completo de aprendizaje en Ingeniería de Modelos de Lenguaje Grande (LLM), desde conceptos básicos hasta implementaciones avanzadas.

## 🎯 Objetivo

Este repositorio contiene el material de aprendizaje y proyectos prácticos para dominar la ingeniería de LLM, incluyendo el desarrollo de productos basados en IA, trabajo con modelos locales y comerciales, y la implementación de soluciones reales.

## 📁 Estructura del Proyecto

```
my_llm_engineering/
├── README.md                          # Este archivo
├── SETUP.md                          # Guía de configuración
├── requirements.txt                   # Dependencias del proyecto
├── .env.example                      # Plantilla de variables de entorno
├── .gitignore                        # Archivos a ignorar en Git
├── 1_Crea_Tu_Primer_Producto_LLM/    # Módulo 1: Fundamentos
│   ├── README.md
│   ├── day1.ipynb
│   ├── test.ipynb
│   ├── Notas.md
│   └── mecatronica_scraper/          # Proyecto MecatronicaScraper
│       ├── README.md
│       └── mecatronica_robotica_scraper.py
├── 2_modelos_locales/                # Módulo 2: Modelos Locales
│   ├── README.md
│   ├── Notas.ipynb
│   └── day2 EXERCISE.ipynb
├── 3_modelos_frontera/               # Módulo 3: Modelos de Frontera
│   └── notas.ipynb
├── 4_teoria_transformers/            # Módulo 4: Teoría de Transformers
│   ├── Notas.ipynb
│   └── *.png                        # Imágenes explicativas
└── 5_laboratorio_final_semana_1/     # Módulo 5: Laboratorio Final
    ├── README.md
    ├── day5.ipynb
    ├── tutor_robotica/              # Proyecto Tutor Inteligente
    │   ├── README.md
    │   ├── tutor_robotica.py
    │   ├── tutor_robotica_local.py
    │   ├── test_languages.py
    │   └── prompts/
    └── brochure_generator/           # Proyecto Generador de Folletos
        ├── README.md
        ├── brochure_generator.py
        └── folleto_*.md
```

## 🚀 Proyectos Destacados

### 1. Tutor Inteligente de Robótica
- **Ubicación**: `5_laboratorio_final_semana_1/tutor_robotica/`
- **Descripción**: Tutor personalizado basado en IA para diferentes niveles educativos
- **Tecnologías**: OpenAI GPT, Ollama, Python
- **Características**: Multiidioma, múltiples niveles educativos, prompts especializados

### 2. Generador de Folletos Empresariales
- **Ubicación**: `5_laboratorio_final_semana_1/brochure_generator/`
- **Descripción**: Generador automático de folletos comerciales mediante análisis web
- **Tecnologías**: OpenAI GPT, Web Scraping, Python
- **Características**: Análisis automático, contenido personalizado, múltiples formatos

### 3. MecatronicaScraper
- **Ubicación**: `1_Crea_Tu_Primer_Producto_LLM/mecatronica_scraper/`
- **Descripción**: Scraper especializado en contenido técnico de mecatrónica y robótica
- **Tecnologías**: BeautifulSoup, Requests, Python
- **Características**: Extracción inteligente, filtrado de contenido, múltiples formatos

## 📚 Módulos de Aprendizaje

### Módulo 1: Crea Tu Primer Producto LLM
- Fundamentos de LLM
- Configuración del entorno
- Primer proyecto práctico
- Web scraping básico

### Módulo 2: Modelos Locales
- Configuración de Ollama
- Comparación de modelos
- Implementación local vs. comercial
- Optimización de rendimiento

### Módulo 3: Modelos de Frontera
- Últimos avances en LLM
- Modelos de vanguardia
- Técnicas avanzadas

### Módulo 4: Teoría de Transformers
- Arquitectura de transformers
- Mecanismos de atención
- Fundamentos teóricos

### Módulo 5: Laboratorio Final
- Proyectos integradores
- Aplicaciones reales
- Implementación completa

## 🛠️ Configuración del Entorno

### Requisitos Previos
- Python 3.8+
- Anaconda o Miniconda (recomendado)
- Cuenta de OpenAI (opcional)
- Ollama (para modelos locales)

### Instalación Rápida

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd my_llm_engineering
```

2. **Crear entorno virtual**
```bash
conda create -n llm_engineering python=3.11
conda activate llm_engineering
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus API keys
```

### Configuración Detallada
Ver [SETUP.md](SETUP.md) para instrucciones completas de configuración.

## 🚀 Uso Rápido

### Tutor de Robótica
```bash
cd 5_laboratorio_final_semana_1/tutor_robotica
python tutor_robotica_local.py  # Para modelos locales
# o
python tutor_robotica.py        # Para OpenAI
```

### Generador de Folletos
```bash
cd 5_laboratorio_final_semana_1/brochure_generator
python brochure_generator.py
```

### MecatronicaScraper
```bash
cd 1_Crea_Tu_Primer_Producto_LLM/mecatronica_scraper
python mecatronica_robotica_scraper.py
```

## 📖 Documentación Adicional

- [SETUP.md](SETUP.md) - Configuración completa del proyecto
- [requirements.txt](requirements.txt) - Lista de dependencias
- Cada módulo tiene su propio README con instrucciones específicas
- Cada proyecto tiene documentación detallada en su carpeta

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🔗 Enlaces Útiles

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Ollama Documentation](https://ollama.ai/docs)
- [Jupyter Notebook Documentation](https://jupyter-notebook.readthedocs.io/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)