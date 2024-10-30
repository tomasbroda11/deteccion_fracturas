import tensorflow as tf
import numpy as np
from keras.preprocessing import image

# Ruta al modelo
model_path = 'weights\ResNet50_Elbow_frac.keras'
# Cargar el modelo solo una vez
modelo = tf.keras.models.load_model(model_path)

def fractureElbow(file_path):    
    size = 224
    temp_img = image.load_img(file_path, target_size=(size, size))
    x = image.img_to_array(temp_img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    prediction = modelo.predict(images)
    print(prediction)
    result = {
        'fracture_probability': float(prediction[0][0]),
        'fracture_detected': prediction[0][0] > 0.5  
    }
    
    return result
