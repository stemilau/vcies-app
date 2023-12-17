import speech_recognition as sr

# Creăm un obiect Recognizer pentru a efectua recunoașterea vocală
recognizer = sr.Recognizer()

# Utilizăm microfonul pentru a înregistra sunetul
with sr.Microphone() as source:
    print("Vorbiți acum...")
    audio = recognizer.listen(source)

    try:
        # Folosim Google Speech Recognition pentru a converti înregistrarea în text
        text = recognizer.recognize_google(audio, language='ro-RO') # Alege limba corespunzătoare

        print("Textul recunoscut: ", text)

    except sr.UnknownValueError:
        print("Nu s-a putut recunoaște textul.")
    except sr.RequestError as e:
        print("Eroare în obținerea rezultatelor; {0}".format(e))