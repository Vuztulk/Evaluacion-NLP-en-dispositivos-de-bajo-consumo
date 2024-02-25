import torch
from torch.utils.data import Dataset, DataLoader
from torch.profiler import profile, record_function, ProfilerActivity
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import time

class TextDataset(Dataset):
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.text = file.read().replace('\n', '').split('. ')

    def __len__(self):
        return len(self.text)

    def __getitem__(self, idx):
        return self.text[idx]

# Cargar el tokenizador y el modelo
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')
model.config.pad_token_id = model.config.eos_token_id

# Crear un DataLoader con paralelización a nivel de datos
dataset = TextDataset('/home/tfg1/TFG/Problemas/Predictor de Texto/input.txt')
dataloader = DataLoader(dataset, batch_size=1, shuffle=False, num_workers=4)

# Ejecutar el código una vez
start_time = time.time()

# Realizar la inferencia del modelo con el perfilador
with torch.no_grad():
    with profile(activities=[ProfilerActivity.CPU], record_shapes=True) as prof:
        with record_function("model_inference"):
            for i, input_text in enumerate(dataloader):
                input_ids = tokenizer.encode(input_text[0], return_tensors='pt')
                attention_mask = torch.ones(input_ids.shape)
                outputs = model.generate(input_ids, max_length=100, temperature=0.7, num_return_sequences=1, do_sample=True, attention_mask=attention_mask)

cpu_time = prof.key_averages().total_cpu_time
cpu_time_seconds = cpu_time / 1_000_000
cpu_time_str = f'{cpu_time_seconds:.4f}'.replace('.', ',')
print(f'Tiempo de CPU: {cpu_time_str} segundos')

output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Calcular el tiempo de CPU y total
end_time = time.time()
duration = end_time - start_time
duration_str = f'{duration:.4f}'.replace('.', ',')
print(f'Tiempo total: {duration_str} segundos')
