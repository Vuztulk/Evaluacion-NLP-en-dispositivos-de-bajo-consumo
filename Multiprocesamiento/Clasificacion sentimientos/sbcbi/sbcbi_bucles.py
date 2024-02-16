import torch
from torch.profiler import profile, record_function, ProfilerActivity
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import psutil
import os
import time

# Cargamos el modelo y el tokenizador preentrenados
tokenizer = AutoTokenizer.from_pretrained('sbcBI/sentiment_analysis_model')
model = AutoModelForSequenceClassification.from_pretrained('sbcBI/sentiment_analysis_model')

# Abrimos el archivo de resultados
with open('resultados.txt', 'w') as f:
    # Ejecutamos el código 10 veces
    for i in range(10):
        start_time = time.time()

        # Definimos una frase de entrada
        with open('/home/tfg1/TFG/Problemas/Clasificacion sentimientos/input.txt', 'r') as file:
            lines = file.read().strip().split('. ')

        for input_text in lines:
            encoded_input = tokenizer(input_text, return_tensors='pt')

            # Inicializamos el perfilador de PyTorch
            with torch.no_grad():
                with profile(activities=[ProfilerActivity.CPU], record_shapes=True) as prof:
                    with record_function("model_inference"):
                        outputs = model(**encoded_input)
                        logits = outputs.logits
                        predicted_class = torch.argmax(logits).item()

            # Guardamos las métricas del perfilador en el archivo
            model_inference_event = [item for item in prof.key_averages() if item.key == "model_inference"]
            if model_inference_event:
                cpu_time = model_inference_event[0].cpu_time_total
                cpu_time_seconds = cpu_time / 1_000_000
                cpu_time_str = f'{cpu_time_seconds:.4f}'.replace('.', ',')
                f.write(f'{cpu_time_str}\n')

        end_time = time.time()
        duration = end_time - start_time
        duration_str = f'{duration:.4f}'.replace('.', ',')
        f.write(f'{duration_str}\n')
