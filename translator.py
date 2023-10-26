from googletrans import Translator
import speech_recognition as sr
import pyttsx3, pywhatkit

listener = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)



translator = Translator()

texto = ""
resultado = ""
contador = 0
contador2 = 0
saber = 0

#habla en castellano ----------------

def talkES(text):
    engine.say(text)
    engine.runAndWait()

#habla en inglés -------------------

def talkEN(text):
    engine2 = pyttsx3.init()
    voices = engine2.getProperty("voices")
    engine2.setProperty("voice", voices[1].id)

    engine2.say(text)
    engine2.runAndWait()
#-------------------------------------------

def listenES():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language='es-ES')
            rec = rec.lower(0)
            #if name in rec:
                #rec = rec.replace(name, "")
    except:
        pass
    return rec

def listenEN():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc)
            rec = rec.lower(0)

    except:
        pass
    return rec

def main():
    global texto
    global resultado
    global contador
    global contador2
    global saber    
    print("¿Quieres traducir del inglés al español o del español al inglés?")
    talkES("¿Quieres traducir del inglés al español o del español al inglés?")
    rec = listenES()
    if "del inglés al español" in rec:
        print("Qué quieres decir?")
        talkES("Qué quieres decir?")
        rec = listenEN()
        if "" in rec: 
            texto = rec
            resultado = str(translator.translate(texto, src = "en", dest = "es"))
            for i in resultado:
                contador +=1
                if i == ",":
                    contador2 +=1
                    if contador2 == 3:
                        saber = contador
                        contador2 = 0
                        print(resultado[33:saber-16])
                        talkES(resultado[33:saber-16])
                    else:
                        pass
                    
    elif "del español al inglés" in rec:
        print("Qué quieres decir?")
        talkES("Qué quieres decir?")
        rec = listenES()
        if "" in rec: 
            texto = rec
        texto = rec
        resultado = str(translator.translate(texto, src = "es", dest = "en"))  
        for i in resultado:
            contador +=1
            if i == "=":
                contador2 +=1
                if contador2 == 4:
                    saber = contador
                    contador2 = 0
                    print(resultado[33:saber-16])
                    talkEN(resultado[33:saber-16])
                else:
                    pass
                
    else:
        print("No te entiendo, intentalo nuevamente")
        talkES("No te entiendo, intentalo nuevamente")
        main()

if __name__=="__main__":
    main()