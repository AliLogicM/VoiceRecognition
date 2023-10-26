import librosa
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import sounddevice as sd

# Función para extraer características de audio utilizando librosa
def extract_features(audio, sr):
    duration = 3.0  # Duración del audio para extraer características
    # Extraer características de audio utilizando librosa
    features = []
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=20)
    features.extend(np.mean(mfcc, axis=1))
    return features


# Directorios que contienen los archivos de audio de cada género (uno por género)
female_dir = './female'
male_dir = './male'
# Crear listas vacías para almacenar características y etiquetas
features = []
labels = []

# Recorrer archivos de audio femeninos y extraer características
for filename in os.listdir(female_dir):
    if filename.endswith('.wav' or ".mp3"):
        file_path = os.path.join(female_dir, filename)
        audio, sr = librosa.load(file_path, duration=3.0)
        audio_features = extract_features(audio, sr)
        features.append(audio_features)
        labels.append(0)  # Etiqueta 0 para género femenino

# Recorrer archivos de audio masculinos y extraer características
for filename in os.listdir(male_dir):
    if filename.endswith('.wav'):
        file_path = os.path.join(male_dir, filename)
        audio, sr = librosa.load(file_path, duration=3.0)
        audio_features = extract_features(audio, sr)
        features.append(audio_features)
        labels.append(1)  # Etiqueta 1 para género masculino

# Convertir listas a matrices numpy
features = np.array(features)
labels = np.array(labels)

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Crear un clasificador de máquina de soporte vectorial (SVM)
classifier = SVC()

# Entrenar el clasificador
classifier.fit(X_train, y_train)

# Evaluar el rendimiento en el conjunto de prueba
accuracy = classifier.score(X_test, y_test)
print('Precisión General del clasificador:', accuracy)
#reportes de precición
target_names = ['male', 'female']
y_pred = classifier.predict(X_test)
report = classification_report(y_test, y_pred, target_names=target_names)
print(report, "\n--------------------------------------------------------\n")


# Bucle principal para las pruebas de voz
while True:
    # Grabar audio utilizando sounddevice
    print("\nHabla ahora!, Escuchando...")
    duration = 4  # Duración de la grabación en segundos
    sr = 22050  # Frecuencia de muestreo
    audio = sd.rec(int(duration * sr), samplerate=sr, channels=1, blocking=True)
    audio = audio.flatten()

    # Extraer características del audio grabado
    recorded_features = extract_features(audio, sr)

    # Predecir el género utilizando el clasificador entrenado
    prediction = classifier.predict([recorded_features])

    # Mapear la predicción a "male" o "female"
    gender = "Mujer" if prediction == 0 else "Hombre"

    # Imprimir la predicción
    print("El género predicho es: ", gender,"\n")

    # Solicitar al usuario que ingrese una opción (continuar o salir)
    option = input("Ingresa cualquier tecla para continuar o 's' para salir: ")

    # Verificar la opción ingresada
    if option.lower() == 's':
        break  # Salir del bucle si la opción es 's'