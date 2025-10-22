# 🤖 Tutor de Robótica Multimodal

Un agente educativo inteligente que combina texto, imágenes y audio para enseñar robótica, Arduino, electrónica, mecatrónica y programación a estudiantes de diferentes edades.

## ✨ Características

- **🎯 Adaptación por Nivel**: Ajusta explicaciones según la edad del estudiante (preescolar, primaria, secundaria, preparatoria)
- **🎨 Generación de Imágenes**: Crea imágenes educativas automáticamente usando DALL-E-3
- **🔊 Síntesis de Voz**: Convierte explicaciones a audio para reforzar el aprendizaje
- **💻 Ejemplos de Código**: Muestra código de Arduino adaptado al nivel educativo
- **🌐 Interfaz Web**: Interfaz intuitiva con Gradio para interacción multimodal
- **🛠️ Herramientas Especializadas**: Funciones específicas para conceptos de robótica

## 🚀 Instalación

1. **Clonar o descargar los archivos**
2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar API Key de OpenAI**:
   - Crear archivo `.env` en el directorio del proyecto
   - Agregar tu API key:
     ```
     OPENAI_API_KEY=sk-tu-api-key-aqui
     ```

4. **Ejecutar el tutor**:
   ```bash
   python tutor_robotica_multimodal.py
   ```

## 📚 Niveles Educativos

### 🧸 Preescolar (3-6 años)
- Conceptos muy básicos con juegos y analogías simples
- Vocabulario simple y ejemplos cotidianos
- Imágenes coloridas estilo cartoon

### 🎒 Primaria (6-12 años)
- Conceptos básicos con experimentos sencillos
- Vocabulario básico y ejemplos prácticos
- Imágenes educativas con diagramas simples

### 🔬 Secundaria (12-15 años)
- Conceptos intermedios con proyectos estructurados
- Vocabulario técnico básico
- Imágenes técnicas con esquemas detallados

### 🎓 Preparatoria (15-18 años)
- Conceptos avanzados con aplicaciones reales
- Vocabulario técnico avanzado
- Imágenes profesionales con diagramas complejos

## 🛠️ Herramientas Disponibles

### 1. Explicación de Componentes
- Explica componentes de Arduino (LED, sensores, motores, etc.)
- Genera imagen educativa del componente
- Proporciona audio explicativo

### 2. Ejemplos de Código
- Muestra código de Arduino adaptado al nivel
- Genera imagen del código o circuito
- Explica línea por línea según el nivel

### 3. Generación de Imágenes
- Crea imágenes educativas sobre cualquier tema de robótica
- Adapta complejidad visual al nivel educativo
- Integra conceptos técnicos de forma visual

## 💡 Ejemplos de Uso

### Preguntas que puedes hacer:
- "¿Qué es Arduino y para qué sirve?"
- "¿Cómo funciona un sensor de temperatura?"
- "Muéstrame código para hacer parpadear un LED"
- "¿Qué es un motor servo y cómo se controla?"
- "Explícame qué son las resistencias"

### Funcionalidades Multimodales:
- **Texto**: Explicaciones adaptadas al nivel
- **Imagen**: Diagramas, esquemas y ilustraciones automáticas
- **Audio**: Narración de explicaciones para reforzar aprendizaje

## 🔧 Configuración Técnica

### Modelos Utilizados:
- **Chat**: GPT-4o-mini (OpenAI)
- **Imágenes**: DALL-E-3 (OpenAI)
- **Audio**: TTS-1 (OpenAI)

### Dependencias Principales:
- `openai`: API de OpenAI para chat, imágenes y audio
- `gradio`: Interfaz web interactiva
- `pillow`: Procesamiento de imágenes
- `pydub`: Manejo de audio (opcional)

## 🎯 Casos de Uso

### Para Estudiantes:
- Aprender conceptos de robótica de forma visual y auditiva
- Obtener explicaciones adaptadas a su nivel de comprensión
- Ver ejemplos de código progresivos
- Reforzar aprendizaje con múltiples modalidades

### Para Educadores:
- Herramienta de apoyo para clases de robótica
- Generación automática de material visual
- Adaptación instantánea a diferentes niveles
- Ejemplos de código listos para usar

## 🚨 Requisitos del Sistema

- Python 3.8+
- Conexión a internet (para APIs de OpenAI)
- API Key válida de OpenAI
- Navegador web moderno (para interfaz Gradio)

## 📝 Notas Importantes

- El audio requiere las librerías `pydub` y `ffmpeg` para reproducción local
- Las imágenes se generan en tiempo real y pueden tardar unos segundos
- El historial de conversación se mantiene durante la sesión
- La interfaz web se ejecuta en `http://localhost:7862`

## 🤝 Contribuciones

Este proyecto está diseñado para ser extensible. Puedes:
- Agregar nuevos niveles educativos
- Incluir más herramientas especializadas
- Mejorar los prompts para mejor adaptación
- Añadir soporte para más idiomas

¡Disfruta aprendiendo robótica de forma multimodal! 🚀🤖