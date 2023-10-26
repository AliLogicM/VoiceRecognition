# Importar las librerías necesarias
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from python_speech_features import mfcc
import librosa

# Definir las características de entrada y etiquetas de salida
# En este ejemplo, se utilizan las características MFCC de una señal de voz
# y un vector de etiquetas de salida con 5 clases posibles
X = []
y = []

# Cargar los archivos de audio y extraer las características MFCC
for i in range(1, 6):
    for j in range(1, 11):
        file_path = f"audio/5_lucas_13.wav"  # Archivo de audio
        signal, sr = librosa.load(file_path, sr=22050)  # Cargar la señal de audio
        mfcc_features = mfcc(signal, sr, n_mfcc=13)  # Extraer las características MFCC
        X.append(
            mfcc_features.flatten()
        )  # Aplanar las características y agregarlas a la matriz de entrada
        y.append(i)  # Agregar la etiqueta correspondiente a la matriz de salida

# Normalizar las características de entrada
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Crear el modelo de regresión logística
lr = LogisticRegression()

# Entrenar el modelo utilizando los datos de entrada y salida
lr.fit(X, y)

# Utilizar el modelo entrenado para clasificar una nueva señal de voz
# En este ejemplo, se utiliza una señal de voz de tamaño 2 segundos
new_signal, sr = librosa.load("audio/new_signal.wav", sr=22050, duration=2)
new_mfcc = mfcc(new_signal, sr, n_mfcc=13)
new_features = scaler.transform(new_mfcc.flatten().reshape(1, -1))
predicted_label = lr.predict(new_features)

# Imprimir la etiqueta de salida predicha
print("Etiqueta de salida predicha:", predicted_label[0])
