import speech_recognition as sr
from PIL import Image, ImageEnhance, ImageFilter
import matplotlib.pyplot as plt

def show_image(img):
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def rotire_imagine_catre_stanga(imagine):
    return imagine.transpose(Image.ROTATE_270)

def rotire_imagine_catre_dreapta(imagine):
    return imagine.transpose(Image.ROTATE_90)

def process_image(command):
    img_path = r"C:\\Users\\anca2\\Desktop\\proiect-iom-2023\\Photos\\lena2.png"
    img = Image.open(img_path)

#   Apicarea filtrului alb-negru
    if "alb negru" in command.lower():
        img = img.convert("LA")
        show_image(img)

#   Apicarea filtrului de blur
    if "blur" in command.lower():
        img = img.filter(ImageFilter.BLUR)
        show_image(img)

#   Apicarea crop
    if any(keyword in command.lower() for keyword in ["crop", "tăie", "selectează"]):
        words = command.lower().split()
        left_index = words.index("stânga")
        top_index = words.index("sus")
        right_index = words.index("dreapta")
        bottom_index = words.index("jos")

        left = int(words[left_index + 1])
        top = int(words[top_index + 1])
        right = int(words[right_index + 1])
        bottom = int(words[bottom_index + 1])

        img = img.crop((left, top, right, bottom))
        show_image(img)

#   Schimbarea luminozitatii
    if "luminozitatea" in command and ("crește" in command or "scade" in command):
        words = command.split()
        try:
            brightness_index = next(i for i, word in enumerate(words) if word.isdigit() or (word.replace('.', '', 1).isdigit() and '.' in word))
            brightness = float(words[brightness_index].replace(",", "."))
            if "scade" in words:
                brightness = -brightness

            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.0 + brightness)
            show_image(img)
        except (ValueError, IndexError):
            print("Valoarea luminozității nu este validă.")
    else:
        print("Comanda vocală nu este recunoscută sau nu conține instrucțiuni valide.")

#   Rotirea imaginii
    if "rotire stânga" in command:
        imagine_rotita = rotire_imagine_catre_stanga(img)
        imagine_rotita.show()
    elif "rotire dreapta" in command:
        imagine_rotita = rotire_imagine_catre_dreapta(img)
        imagine_rotita.show()
    else:
        print("Comanda necunoscuta. Te rog sa spui 'rotire  stânga' sau 'rotire dreapta'.")


def recognize_and_process():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Ascultă comanda vocală...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio, language='ro-RO')
            print("Comanda vocală recunoscută:", command)
            process_image(command)
        except sr.UnknownValueError:
            print("Nu s-a putut recunoaște comanda vocală.")
        except sr.RequestError as e:
            print(f"Eroare în obținerea rezultatelor; {e}")

if _name_ == "_main_":
    recognize_and_process()