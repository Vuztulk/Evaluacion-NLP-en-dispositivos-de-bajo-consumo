import torch
from torch.profiler import profile, record_function, ProfilerActivity, schedule
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import psutil
import os
import threading
import time

start_time = time.time()

# Cargar el tokenizador y el modelo
tokenizer = AutoTokenizer.from_pretrained("robertrengel/autotrain-traductor-en-es-2023-3608896666")
model = AutoModelForSeq2SeqLM.from_pretrained("robertrengel/autotrain-traductor-en-es-2023-3608896666")

# Leer el texto de entrada desde un archivo .txt
input_text = "The Great Gatsby is a classic novel by F. Scott Fitzgerald set in the Jazz Age. It follows Jay Gatsby's pursuit of Daisy Buchanan, exploring themes of love, wealth, and the American Dream. Narrated by Nick Carraway, the story delves into the complexities of society and human relationships."

# Codificar entrada
input_ids = tokenizer.encode(input_text, return_tensors='pt')

# Función para realizar la inferencia del modelo
def model_inference(input_ids, outputs):
    with torch.no_grad():
        outputs[0] = model.generate(input_ids, max_length=200, num_return_sequences=1)

# Realizar la inferencia del modelo con el perfilador en paralelo
outputs = [None]
thread = threading.Thread(target=model_inference, args=(input_ids, outputs))

# Define a custom profiling schedule
my_schedule = schedule(
    skip_first=10,  # Ignora las primeras 10 iteraciones
    wait=5,  # Espera 5 iteraciones después del calentamiento
    warmup=10,  # Calienta durante 10 iteraciones
    active=50,  # Recoge datos durante 50 iteraciones
    repeat=10  # Repite el ciclo 10 veces
)

with profile(schedule=my_schedule, activities=[ProfilerActivity.CPU], record_shapes=True) as prof:
    with record_function("model_inference"):
        thread.start()
        thread.join()
print("Métricas del perfilador:")
print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=10))

# Decodificar la salida
output_text = tokenizer.decode(outputs[0][0], skip_special_tokens=True)
print(f'Texto de entrada: {input_text}\n')
print(f'Texto de salida: {output_text}')

# Métricas adicionales
pid = os.getpid()
py = psutil.Process(pid)

memory_use = py.memory_info()[0]/2.**30  # memory use in GB
print(f'Memory use: {memory_use} GB')

cpu_use = psutil.cpu_percent(interval=None)
print(f'CPU use: {cpu_use} %')

end_time = time.time()
duration = end_time - start_time
print(f'La ejecución del código tardó {duration:.4f} segundos.')
