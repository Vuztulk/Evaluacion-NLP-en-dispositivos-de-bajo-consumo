# Evaluación de Modelos de Lenguaje Natural (NLP) en Dispositivos de Bajo Consumo


Proyecto de investigación desarrollado como Trabajo de Fin de Grado en Ingeniería de Computadores (Universidad Complutense de Madrid), enfocado en analizar el rendimiento de modelos de NLP en entornos con restricciones de hardware y energía.

## 📌 Descripción
Este proyecto evalúa múltiples arquitecturas de lenguaje natural (BERT, GPT-2...) en dispositivos de bajo consumo como Raspberry Pi y Jetson Nano, midiendo:
- **Latencia de inferencia**
- **Consumo energético**
- **Uso de memoria**

## 🔍 Características Clave
- Métricas de eficiencia energética por ciclo de inferencia
- Guía práctica para despliegue en entornos IoT/Edge
- Scripts reproducibles para pruebas en Raspberry Pi 4 y Jetson Nano

## 🛠 Tecnologías Utilizadas
**Modelos & Frameworks**  
`Transformers` | `PyTorch` | `Hugging Face`

**Hardware**  
`Raspberry Pi 4` | `Jetson Nano`

**Monitorización**  
`PowerMonitor` | `Perf` 

## 📂 Estructura del Repositorio
```
.
├── /Aplicacion            # Contiene la aplicacion para interactuar con los distintos modelos
├── /Consumo               # Scripts de evaluación del consumo de cada modelo
├── /Datos                 # Resultados y evaluaciones de las pruebas
├── /GPU                   # Scripts para la ejecucion de los modelos con GPU
```
