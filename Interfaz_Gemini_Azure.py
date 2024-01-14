 
#Interfaz:
import tkinter as tk 
from PIL import Image
from io import BytesIO
import os
import cv2

#Texto a Audio
import pyttsx3    

#texto
import re 

#HTMLtexto consola
from rich.console import Console
from rich.syntax import Syntax
 

#pip install python-docx
#pip install html2text
from docx import Document
import html2text 

#
#GEMINI-1
import textwrap
import google.generativeai as genai  
from markdown import Markdown
###
#

#
#Azure-1
import os
import azure.cognitiveservices.speech as speechsdk
## 
#


class VentanaPrincipal:

    def to_markdown(self,text):
        return Markdown().convert(textwrap.indent(text, '> ', predicate=lambda _: True)) 
    
    def to_plain_string(self,text):
        # Eliminar caracteres especiales excepto letras, números y tildes
        cleaned_text = re.sub(r'[^\w\sáéíóúÁÉÍÓÚ.,;:?!¡¿]', '', text)
        return cleaned_text 
    
    def contiene_palabra(self,cadena, palabra):
    # Verificar si la cadena no es None antes de intentar la comparación
        if cadena is not None:
            return palabra in cadena
        else:
            return False
     
            
   
    def hablar(self,texto):
        console = Console()
        syntax = Syntax(texto, "html", theme="monokai", line_numbers=True)
        console.print(syntax)

        #Azure-2                    AQUI Tu KEY DE AZURE
        
        speech_config = speechsdk.SpeechConfig(subscription=' Tu Key de Azure', region="brazilsouth")
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True) 
        speech_config.speech_synthesis_voice_name='es-EC-AndreaNeural' #definimos la voz a utilizar
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text_async(texto).get()
        stream = speechsdk.AudioDataStream(speech_synthesis_result)  


    def hablarpy(self,texto):
        print(texto)
        engine = pyttsx3.init()
        engine.say(texto)
        engine.startLoop(False)
        engine.iterate()
        engine.endLoop()


    def __init__(self, master):
                
        #GEMINI-2                       AQUI Tu KEY DE GOOGLE
        
        GOOGLE_API_KEY=' Tu key de google'
        genai.configure(api_key=GOOGLE_API_KEY)
        #
    
        self.master = master
        master.title("Gemini + AzureCognitionServices") 
        # Ocultar barra de título y botones de ventana
        #master.overrideredirect(True)
        
        # Personalizar color de fondo
        master.configure(bg='#000000')  # Puedes usar cualquier código de color hexadecimal

        # Personalizar tamaño de fuente

        # Personalizar color de fondo de la etiqueta y color del texto
        etiqueta = tk.Label(master, text="Bienvenido: \n \n     Selecciona una opcion:", font=("Arial", 12), bg='#000000', fg='#ffffff')
        etiqueta.pack(pady=20)  
        # Centrar la ventana en la pantalla
        self.centra_ventana()
  
        # Agregar botones con el mismo tamaño
        self.boton_chat = tk.Button(master, text="Chat", command=self.abrir_ventana_chat, bg='#333333', fg='#ffffff', width=12, height=2)
        self.boton_chat.pack()

        self.boton_foto = tk.Button(master, text="Foto", command=self.abrir_ventana_foto, bg='#333333', fg='#ffffff', width=12, height=2)
        self.boton_foto.pack()

        # Agregar un botón para cerrar la ventana
        self.boton_cerrar = tk.Button(master, text="Cerrar", command=master.destroy, bg='#500', fg='#ffffff', width=12, height=2)
        self.boton_cerrar.pack()

    def centra_ventana(self):
        ancho_ventana = 600
        alto_ventana = 300  

        # Obtener el tamaño de la pantalla
        ancho_pantalla = self.master.winfo_screenwidth()
        alto_pantalla = self.master.winfo_screenheight()

        # Calcular la posición para centrar la ventana
        x = (ancho_pantalla - ancho_ventana) // 2
        y = (alto_pantalla - alto_ventana) // 2

        # Establecer la geometría de la ventana para centrarla
        self.master.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y-90}')



##                CHAT#                CHAT#                CHAT#                CHAT#                CHAT#                CHAT#                CHAT
    def abrir_ventana_chat(self): 
        ventana_chat = tk.Toplevel(self.master)
        ventana_chat.title("Chat")

             # Obtener el tamaño de la pantalla principal
        ancho_pantalla = self.master.winfo_screenwidth()
        alto_pantalla = self.master.winfo_screenheight()

        # Centrar la ventana de chat
        ancho_ventana_chat = 600  
        alto_ventana_chat = 300
        x = (ancho_pantalla - ancho_ventana_chat) // 2
        y = (alto_pantalla - alto_ventana_chat) // 2
        #TAMAÑO
        ventana_chat.geometry(f'{ancho_ventana_chat}x{alto_ventana_chat}+{x}+{y}') 
        ventana_chat.configure(bg='#000000')  #Color d fondo
 
        # Personalizar color de fondo de la etiqueta y color del texto
        etiqueta = tk.Label(ventana_chat, text="Ingresa un mensaje:", font=("Arial", 12), bg='#000000', fg='#ffffff')
        etiqueta.pack(pady=12)  
        
        #ENtrada de texto
        entrada = tk.Text(ventana_chat, font=("Arial", 10), bg='#eeeeee', height=4,  width=40, wrap="word")
        entrada.pack(pady=9)
        # Establecer autofocus en la entrada de texto
        entrada.focus_set() 


        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])
        chat     
        boton_enviar2 = tk.Button(ventana_chat, text="Enviar", command=lambda: mostrar_resultado_chat(entrada.get("1.0", tk.END), chat), bg='#333333', fg='#ffffff', width=12, height=2)
        boton_enviar2.pack()

        self.resultado_label = tk.Label(ventana_chat, text="",font=("Arial", 8),bg='#333333', fg='#ffffff', width=90, height=4)
        self.resultado_label.pack() 


        def mostrar_resultado_chat(mensaje, chat): 
            
            boton_enviar2.config(state=tk.DISABLED)
            entrada.delete("1.0", tk.END)

            if mensaje=="salir": 
                exit()    
            try:
                response = chat.send_message(mensaje).text 
                print(response)  
                self.hablar(response)
                #self.html_to_docx(response, "respuestas/texto_escanneado.docx")
                     
                self.resultado_label.config(text=response)  
                entrada.focus_set() 
                boton_enviar2.config(state=tk.NORMAL)

                #Voz con azure
                #self.hablarpy(a)  

            except Exception as e:
                print(f'{type(e).__name__}: {e}')  



## FOTO                   # FOTO                   # FOTO                   # FOTO                   # FOTO                   # FOTO                   # FOTO         

    def abrir_ventana_foto(self):
        # Lógica de la Foto aquí
        # messagebox.showinfo("Foto", "Lógica de la Foto")
        ventana_foto = tk.Toplevel(self.master)
        ventana_foto.title("Prompt con Foto")

        # Crear el botón "Guardar Documento"
        #boton_guardar = tk.Button(ventana_foto, text="Guardar Documento", command=self.guardar_documento, bg='#333333', fg='#ffffff', width=20, height=2)
        #boton_guardar.pack()

        # Obtener el tamaño de la pantalla principal
        ancho_pantalla = self.master.winfo_screenwidth()
        alto_pantalla = self.master.winfo_screenheight()

        # Centrar la ventana de chat
        ancho_ventana_foto = 600  
        alto_ventana_foto = 300
        x = (ancho_pantalla - ancho_ventana_foto) // 2
        y = (alto_pantalla - alto_ventana_foto) // 2
        #TAMAÑO
        ventana_foto.geometry(f'{ancho_ventana_foto}x{alto_ventana_foto}+{x}+{y}') 
        ventana_foto.configure(bg='#000000')  #Color d fondo 

        # Función para actualizar la vista de la cámara en la ventana 
        def tomar_foto():
            # Inicializar la cámara
            camara = cv2.VideoCapture(0)

            if not camara.isOpened():
                print("Error al abrir la cámara.")
                return None

            # Capturar un solo cuadro (foto)
            ret, frame = camara.read()
            retval, buffer = cv2.imencode('.jpg', frame)
            # Crear un objeto BytesIO para almacenar la imagen en memoria
            img_bytes = BytesIO(buffer.tobytes())

            # Abrir la imagen desde BytesIO usando PIL
            img_pil = Image.open(img_bytes)

            # Puedes mostrar la imagen si lo deseas
            img_pil.show()
            
            camara.release()

            if ret:
                return img_pil
            else:
                print("Error al capturar la foto.")
                return None
          

        #Color de fondo de la etiqueta y color del texto
        etiqueta = tk.Label(ventana_foto, text="Ingresa un mensaje:", font=("Arial", 12), bg='#000000', fg='#ffffff')
        etiqueta.pack(pady=12)  
        
 
        #ENtrada de texto
        entry_mensaje = tk.Text(ventana_foto, font=("Arial", 10), bg='#eeeeee', height=4, width=40, wrap="word")
        entry_mensaje.pack(pady=10)

        # Establecer autofocus en la entrada de texto
        entry_mensaje.focus_set()  

        #Boton ENVIAR
        boton_enviar = tk.Button(ventana_foto, text="Enviar", command=lambda: mostrar_resultado_foto(entry_mensaje.get("1.0", tk.END)), bg='#333333', fg='#ffffff', width=12, height=2)
        boton_enviar.pack()

        #Salida Respuesta
        self.resultado_label = tk.Label(ventana_foto, text="",font=("Arial", 8),bg='#222222', fg='#ffffff', width=90, height=4)
        self.resultado_label.pack() 


        def mostrar_resultado_foto(mensaje):
            def html_to_docx(text):
                # Carpeta donde se guardarán los documentos
                folder_path = "respuestas"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Nombre base del archivo
                base_name = "respuesta"

                # Extensión del archivo
                file_extension = ".docx"

                # Verificar si el archivo ya existe
                counter = 1
                output_path = os.path.join(folder_path, f"{base_name}{counter}{file_extension}")

                while os.path.exists(output_path):
                    # Si el archivo ya existe, incrementar el contador y probar con un nuevo nombre
                    counter += 1
                    output_path = os.path.join(folder_path, f"{base_name}{counter}{file_extension}")

                # Crear un nuevo documento de Word
                doc = Document()
                text_content = html2text.html2text(text)
                doc.add_paragraph(text_content)
                doc.save(output_path)
                print(f'Documento Word guardado en: {output_path}')
            foto =tomar_foto()  
            print(" mensaje ",mensaje)  
            print(" foto ",foto)   
            boton_enviar.config(state=tk.DISABLED)
            entry_mensaje.delete("1.0", tk.END)

            if mensaje=="salir": 
                exit()    
            else: 
                model = genai.GenerativeModel('gemini-pro-vision')  
                response = model.generate_content([mensaje, foto], stream=True)
                response.resolve()
                print(response) 
                        
                if response.candidates[0].content.parts : 
                    testo= response.candidates[0].content.parts[0].text
                    self.resultado_label.config(text=testo)
                    self.hablar(testo)
                    self.doc_text = testo 
                    try:
                    # Guardar el documento y obtener la ruta del archivo
                        html_to_docx(testo) 
                    except Exception as e:
                        print('Error al guardar!') 
                        print(f'{type(e).__name__}: {e}')     
                else: 
                    try:  
                        a=response.text
                        html_to_docx(a)
                        self.resultado_label.config(text=a)
                        self.hablar(a) 

                    except Exception as e:
                        print(f'{type(e).__name__}: {e}')    

                # Reactivar el botón después de completar la función  
                entry_mensaje.focus_set() 
                boton_enviar.config(state=tk.NORMAL)
                 
if __name__ == "__main__":
    root = tk.Tk()
    ventana_principal = VentanaPrincipal(root)
    root.mainloop()
