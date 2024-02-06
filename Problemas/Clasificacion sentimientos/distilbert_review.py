import torch
from torch.profiler import profile, record_function, ProfilerActivity
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import psutil
import os

# Cargamos el modelo y el tokenizador preentrenados
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')
model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')

# Definimos una frase de entrada
with open('/home/tfg1/TFG/Problemas/Clasificacion sentimientos/sentimientos.txt', 'r') as file:
    input_text = file.readline().strip()
    
encoded_input = tokenizer(input_text, return_tensors='pt')

# Inicializamos el perfilador de PyTorch
with torch.no_grad():
    with profile(activities=[ProfilerActivity.CPU], record_shapes=True) as prof:
        with record_function("model_inference"):
            outputs = model(**encoded_input)
            logits = outputs.logits
            predicted_class = torch.argmax(logits).item()

# Imprimimos el informe del perfilador
print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=10))

# Imprimimos la clase predicha
sentiment_classes = ['negative', 'positive']
print(f'Input text: {input_text}')
print(f'Predicted sentiment: {sentiment_classes[predicted_class]}')

# Métricas adicionales
pid = os.getpid()
py = psutil.Process(pid)

memory_use = py.memory_info()[0]/2.**30  # memory use in GB
print(f'Memory use: {memory_use} GB')

cpu_use = psutil.cpu_percent(interval=None)
print(f'CPU use: {cpu_use} %')
