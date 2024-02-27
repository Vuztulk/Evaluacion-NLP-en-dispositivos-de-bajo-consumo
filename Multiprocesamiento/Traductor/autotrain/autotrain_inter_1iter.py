import torch
from torch.profiler import profile, record_function, ProfilerActivity
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import time

torch.set_num_interop_threads(4)

# Cargar el tokenizador y el modelo
tokenizer = AutoTokenizer.from_pretrained("robertrengel/autotrain-traductor-en-es-2023-3608896666")
model = AutoModelForSeq2SeqLM.from_pretrained("robertrengel/autotrain-traductor-en-es-2023-3608896666")

# Ejecutar el código una vez
start_time = time.time()

# Leer el texto de entrada desde un archivo .txt
with open('/home/tfg1/TFG/Problemas/Traductor/input.txt', 'r') as file:
    input_text = file.read().replace('\n', '')

# Codificar entrada
input_ids = tokenizer.encode(input_text, return_tensors='pt')

# Realizar la inferencia del modelo con el perfilador
with torch.no_grad():
    with profile(activities=[ProfilerActivity.CPU], record_shapes=True) as prof:
        with record_function("model_inference"):
            outputs = model.generate(input_ids, max_length=200, num_return_sequences=1)


model_inference_event = [item for item in prof.key_averages() if item.key == "model_inference"]
if model_inference_event:
    cpu_time = model_inference_event[0].cpu_time_total
    cpu_time_seconds = cpu_time / 1_000_000
    cpu_time_str = f'{cpu_time_seconds:.4f}'.replace('.', ',')
    print(f'Tiempo de CPU: {cpu_time_str} segundos')

output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

end_time = time.time()
duration = end_time - start_time
duration_str = f'{duration:.4f}'.replace('.', ',')
print(f'Tiempo total: {duration_str} segundos')


