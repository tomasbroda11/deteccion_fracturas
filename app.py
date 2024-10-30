from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from model import fractureElbow
app = Flask(__name__)

# Configuración para almacenar archivos subidos
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Función para verificar si el archivo tiene una extensión válida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/acerca-de')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        respuesta = fractureElbow(filepath)

        return render_template('respuesta.html', fracture_probability=respuesta['fracture_probability'], 
                       fracture_detected=respuesta['fracture_detected'], 
                       filename=filename)


    return "Tipo de archivo no permitido", 400 

@app.route('/vaciar', methods=['POST'])
def vaciar():
    UPLOAD_FOLDER = 'static/uploads/'
    vaciar_carpeta(UPLOAD_FOLDER)  # Llama a la función para vaciar la carpeta
    return redirect('/')  # Redirige a la página de carga de imágenes


def vaciar_carpeta(upload_folder):
    if os.path.exists(upload_folder):
        for archivo in os.listdir(upload_folder):
            archivo_path = os.path.join(upload_folder, archivo)
            try:
                if os.path.isfile(archivo_path):
                    os.remove(archivo_path)
            except Exception as e:
                print(f"Error al eliminar {archivo_path}: {e}")
    else:
        print(f"La carpeta {upload_folder} no existe.")


if __name__ == '__main__':
    app.run(debug=True)
