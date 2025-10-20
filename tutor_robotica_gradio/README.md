# 🤖 Tutor de Robótica con Gradio

Un asistente inteligente que enseña robótica, Arduino, electrónica, mecatrónica y programación a estudiantes de diferentes edades usando una interfaz web interactiva.

## 🌟 Características

- **Adaptación por edad**: El tutor ajusta su lenguaje y explicaciones según el nivel educativo (preescolar, primaria, secundaria, preparatoria)
- **Interfaz web intuitiva**: Desarrollada con Gradio para una experiencia de usuario amigable
- **Chat conversacional**: Mantiene el contexto de la conversación para un aprendizaje continuo
- **Prompts multi-shot**: Utiliza ejemplos específicos para cada nivel educativo
- **Temas especializados**: Cubre robótica, Arduino, electrónica, mecatrónica y programación

## 📚 Niveles Educativos

### 🧸 Preescolar (3-6 años)
- Conceptos muy básicos con juegos
- Vocabulario simple
- Ejemplos cotidianos

### 📚 Primaria (6-12 años)
- Conceptos básicos con experimentos sencillos
- Vocabulario básico
- Ejemplos prácticos

### 🔬 Secundaria (12-15 años)
- Conceptos intermedios con proyectos estructurados
- Vocabulario técnico básico
- Ejemplos de proyectos

### 🎓 Preparatoria (15-18 años)
- Conceptos avanzados con aplicaciones reales
- Vocabulario técnico avanzado
- Ejemplos profesionales

## 🚀 Instalación y Uso

### Prerrequisitos

```bash
pip install gradio openai python-dotenv
```

### Configuración

1. Crea un archivo `.env` en el directorio raíz:
```env
OPENAI_API_KEY=tu_clave_api_aqui
```

2. Asegúrate de que los archivos de prompts estén en la carpeta `prompts/`:
   - `preescolar.txt`
   - `primaria.txt`
   - `secundaria.txt`
   - `preparatoria.txt`

### Ejecutar la aplicación

```bash
python tutor_robotica_gradio.py
```

La aplicación se abrirá en `http://127.0.0.1:7860`

## 🎯 Temas que Cubre

- **Arduino y microcontroladores**
- **Electrónica básica y avanzada**
- **Robótica y automatización**
- **Programación para robots**
- **Mecatrónica y sensores**
- **Proyectos prácticos paso a paso**

## 💡 Ejemplos de Preguntas por Nivel

### Preescolar
- ¿Qué es un robot?
- ¿Cómo se enciende una luz?
- ¿Por qué se mueven los carros de juguete?

### Primaria
- ¿Cómo funciona un LED?
- ¿Qué es Arduino?
- ¿Cómo hacer que un motor gire?

### Secundaria
- ¿Cómo programar un Arduino?
- ¿Qué es PWM y para qué sirve?
- ¿Cómo hacer un robot que siga líneas?

### Preparatoria
- ¿Cómo implementar PID en robótica?
- ¿Qué es la comunicación I2C?
- ¿Cómo diseñar un sistema de control?

## 🛠️ Estructura del Proyecto

```
tutor_robotica_gradio/
├── tutor_robotica_gradio.py    # Archivo principal
├── prompts/                    # Prompts para cada nivel
│   ├── preescolar.txt
│   ├── primaria.txt
│   ├── secundaria.txt
│   └── preparatoria.txt
└── README.md                   # Este archivo
```

## 🔧 Funcionalidades Técnicas

- **Streaming de respuestas**: Las respuestas se generan en tiempo real
- **Gestión de historial**: Mantiene el contexto de la conversación
- **Cambio dinámico de nivel**: Permite cambiar el nivel educativo sin reiniciar
- **Interfaz responsive**: Se adapta a diferentes tamaños de pantalla
- **Manejo de errores**: Gestión robusta de errores de API

## 🎨 Personalización

El tutor puede personalizarse modificando:

1. **Prompts**: Edita los archivos en `prompts/` para cambiar el estilo de enseñanza
2. **Niveles**: Modifica `NIVELES_EDUCATIVOS` para agregar o cambiar niveles
3. **Interfaz**: Personaliza el CSS y la estructura en `crear_interfaz()`
4. **Modelo**: Cambia `MODEL` para usar diferentes modelos de OpenAI

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Siéntete libre de usarlo y modificarlo según tus necesidades.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Si tienes preguntas o problemas, por favor abre un issue en el repositorio.

---

**¡Diviértete aprendiendo robótica! 🚀**