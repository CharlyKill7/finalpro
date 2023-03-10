import vosk
import time
import zmq
import pyaudio

context = zmq.Context()
socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://127.0.0.1:5555")

# Cargar el modelo de lenguaje en español
modelo = vosk.Model("models/vosk-model-es-0.42")

# Crear el reconocedor de voz
rec = vosk.KaldiRecognizer(modelo, 16000)

# Configurar el dispositivo de audio
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16,   # formato de datos de audio que se van a grabar. En este caso, se utiliza pyaudio.paInt16, que es un formato de 16 bits que se utiliza comúnmente para la grabación de voz.
                    channels=1,               # número de canales de audio que se van a grabar. En este caso, se utiliza 1, que es el número de canales para grabación mono.
                    rate=16000,               # tasa de muestreo de audio que se va a utilizar. En este caso, se utiliza 16000, que es una tasa de muestreo común para grabación de voz.
                    input=True,               # booleano que indica si el flujo de audio es de entrada o salida. En este caso, se utiliza True para indicar que se va a grabar audio desde el dispositivo.
                    frames_per_buffer=8000)   # número de cuadros de audio que se van a leer cada vez que se lee del flujo de audio. En este caso, se utiliza 8000, que es el número de cuadros que se leerán cada vez que se lee del flujo de audio.

# Definir las palabras clave
clave = "luna"
clave_stop = "tierra"

# Inicializar el reconocedor de voz
rec = vosk.KaldiRecognizer(modelo, 16000)

# Variables de control
grabando = False

while True:   
    # Leer un fragmento de audio
    data = stream.read(4000, exception_on_overflow=False)
    # Alimentar el fragmento de audio al reconocedor de voz
    if rec.AcceptWaveform(data):
        # Obtener la transcripción
        result = rec.Result()
        if clave in result:
            grabando = True
            while grabando:
                data = stream.read(4000, exception_on_overflow=False)
                if rec.AcceptWaveform(data):
                    result2 = rec.Result()
                    if 'whatsapp' in result2 and 'xt" : ""' not in result2:
                        time.sleep(0.2)
                        print(result2)
                        socket_pub.send_string(result2)#, zmq.SNDMORE)
                        #socket_pub.send_string('whatsapp')
                        if clave_stop in result2:
                            grabando = False
                                