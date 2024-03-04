from flask import Flask, render_template, request
from Modelos.Clasificacion_Sentimientos import clasificacion_sentimiento

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def recibir_texto():
    if request.method == 'POST':
        texto = request.form['texto']
        return clasificacion_sentimiento(texto)
        
if __name__ == '__main__':
    app.run(debug=True)
