# 🏠 Modelos Locales

Este módulo explora la implementación y uso de Modelos de Lenguaje Grande (LLM) ejecutándose localmente, con especial énfasis en Ollama y alternativas a las APIs comerciales.

## 📋 Contenido del Módulo

### 📓 Notebooks y Documentación
- `day2 EXERCISE.ipynb` - Ejercicios prácticos con modelos locales
- `Notas.ipynb` - Conceptos teóricos y comparativas

## 🎯 Objetivos de Aprendizaje

Al completar este módulo, serás capaz de:

- ✅ Instalar y configurar Ollama para modelos locales
- ✅ Comparar ventajas y desventajas de modelos locales vs APIs
- ✅ Implementar soluciones usando modelos locales
- ✅ Optimizar el rendimiento de modelos locales
- ✅ Integrar modelos locales en aplicaciones Python

## 🔧 Configuración de Ollama

### Instalación

#### Linux/Mac:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Windows:
Descargar desde [ollama.ai](https://ollama.ai/download)

### Modelos Disponibles

#### Modelos Recomendados:
```bash
# Modelo ligero y rápido
ollama pull llama2

# Modelo más potente
ollama pull llama2:13b

# Modelo especializado en código
ollama pull codellama

# Modelo multimodal
ollama pull llava
```

### Iniciar Servidor:
```bash
ollama serve
```

## 🆚 Comparativa: Local vs API

### ✅ Ventajas de Modelos Locales

| Aspecto | Modelos Locales | APIs Comerciales |
|---------|----------------|------------------|
| **Privacidad** | ✅ Datos permanecen locales | ❌ Datos enviados a terceros |
| **Costo** | ✅ Sin costo por uso | ❌ Costo por token/request |
| **Latencia** | ✅ Baja latencia local | ❌ Depende de internet |
| **Disponibilidad** | ✅ Funciona offline | ❌ Requiere conexión |
| **Personalización** | ✅ Modelos fine-tuneables | ❌ Limitado |

### ❌ Desventajas de Modelos Locales

| Aspecto | Modelos Locales | APIs Comerciales |
|---------|----------------|------------------|
| **Recursos** | ❌ Requiere hardware potente | ✅ Sin requisitos locales |
| **Calidad** | ❌ Menor que GPT-4 | ✅ Estado del arte |
| **Mantenimiento** | ❌ Actualizaciones manuales | ✅ Automático |
| **Escalabilidad** | ❌ Limitada por hardware | ✅ Ilimitada |

## 🛠️ Implementación Práctica

### Ejemplo Básico con Ollama:
```python
import ollama

# Configuración
MODEL = "llama2"

# Consulta simple
response = ollama.chat(
    model=MODEL,
    messages=[
        {"role": "user", "content": "Explica qué es la robótica"}
    ]
)

print(response['message']['content'])
```

### Integración con Aplicaciones:
```python
import ollama
import requests

class LocalLLM:
    def __init__(self, model="llama2"):
        self.model = model
        self.verify_model()
    
    def verify_model(self):
        """Verificar que el modelo esté disponible"""
        try:
            models = ollama.list()
            available = [m.model for m in models.models]
            if self.model not in available:
                print(f"Modelo {self.model} no encontrado")
                return False
            return True
        except Exception as e:
            print(f"Error conectando con Ollama: {e}")
            return False
    
    def generate_response(self, prompt, context=""):
        """Generar respuesta usando el modelo local"""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error: {e}"
```

## 🔍 Casos de Uso Ideales

### ✅ Cuándo Usar Modelos Locales:

1. **Datos Sensibles**: Información confidencial o privada
2. **Aplicaciones Offline**: Sin conexión a internet
3. **Costos Controlados**: Evitar costos por uso
4. **Baja Latencia**: Respuestas inmediatas
5. **Experimentación**: Pruebas y desarrollo

### ❌ Cuándo NO Usar Modelos Locales:

1. **Tareas Complejas**: Requieren máxima calidad
2. **Recursos Limitados**: Hardware insuficiente
3. **Escalabilidad**: Muchos usuarios concurrentes
4. **Mantenimiento**: Sin recursos para actualizaciones

## 📊 Modelos Populares y Especificaciones

### Llama 2 Family:
- **llama2:7b** - 7B parámetros, ~4GB RAM
- **llama2:13b** - 13B parámetros, ~8GB RAM
- **llama2:70b** - 70B parámetros, ~40GB RAM

### Modelos Especializados:
- **codellama** - Optimizado para código
- **llava** - Multimodal (texto + imágenes)
- **mistral** - Eficiente y rápido
- **neural-chat** - Conversacional

## 🚀 Optimización de Rendimiento

### Configuración de Hardware:
```bash
# Verificar GPU disponible
nvidia-smi

# Configurar Ollama para GPU
export OLLAMA_GPU=1
```

### Parámetros de Optimización:
```python
# Configuración para mejor rendimiento
response = ollama.chat(
    model="llama2",
    messages=[{"role": "user", "content": prompt}],
    options={
        "temperature": 0.7,      # Creatividad
        "top_p": 0.9,           # Diversidad
        "num_ctx": 2048,        # Contexto
        "num_predict": 512      # Longitud respuesta
    }
)
```

## 🧪 Ejercicios Prácticos

### Ejercicio 1: Instalación y Configuración
1. Instalar Ollama
2. Descargar modelo llama2
3. Probar consulta básica

### Ejercicio 2: Comparativa de Modelos
1. Probar diferentes modelos
2. Comparar calidad de respuestas
3. Medir tiempos de respuesta

### Ejercicio 3: Integración en Aplicación
1. Crear clase wrapper para Ollama
2. Implementar manejo de errores
3. Agregar logging y métricas

## 🔧 Solución de Problemas

### Error: "Connection refused"
```bash
# Verificar que Ollama esté ejecutándose
ollama serve

# Verificar puerto (default: 11434)
netstat -an | grep 11434
```

### Error: "Model not found"
```bash
# Listar modelos disponibles
ollama list

# Descargar modelo faltante
ollama pull nombre_modelo
```

### Error: "Out of memory"
```bash
# Usar modelo más pequeño
ollama pull llama2:7b

# Verificar RAM disponible
free -h
```

## 📈 Próximos Pasos

Después de dominar modelos locales:

1. **Módulo 3**: Explorar modelos de frontera
2. **Módulo 4**: Profundizar en arquitectura Transformers
3. **Módulo 5**: Integrar en proyectos finales

## 💡 Mejores Prácticas

- 🎯 **Elige el modelo adecuado**: Balancea calidad vs recursos
- 📊 **Monitorea recursos**: CPU, RAM, GPU usage
- 🔄 **Actualiza regularmente**: Nuevos modelos y versiones
- 🧪 **Experimenta**: Prueba diferentes configuraciones
- 📝 **Documenta**: Registra configuraciones exitosas

---

**¡Domina los modelos locales y gana independencia tecnológica!** 🏠🤖