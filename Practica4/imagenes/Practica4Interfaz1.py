import tkinter as tk
from PIL import Image, ImageTk  
from tkinter import PhotoImage, messagebox
import random

class JuegoClue:
    def __init__(self, root):
        self.root = root
        self.root.title("CLUE")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        self.intentos = 10
        self.personajes = ["Escarlata", "Mostaza", "Azulino", "Verdi", "Moradillo"]
        self.locaciones = ["Salón", "Cocina", "Patio", "Habitación", "Baño"]
        self.armas = ["Daga", "Candelabro", "Pistola", "Soga", "Llave"]

        self.finales = [
            ("Moradillo", "Cocina", "Pistola"),
            ("Mostaza", "Salón", "Llave"),
            ("Verdi", "Patio", "Soga"),
            ("Azulino", "Baño", "Daga"),
            ("Escarlata", "Habitación", "Candelabro"),
        ]

        self.culpable = random.choice(self.finales)
        self.crear_coartadas()

        self.img_mansion = PhotoImage(file="Mansion.png")
        self.img_mayordomo = PhotoImage(file="Mayordomo.png")
        self.img_policia = PhotoImage(file="Policia.png")
        self.img_sangre = PhotoImage(file="Sangre_derramada.png")

        self.frame_inicio = tk.Frame(self.root, bg="black")
        self.frame_inicio.pack(fill="both", expand=True)

        self.lbl_inicio = tk.Label(self.frame_inicio, image=self.img_mansion, bg="black")
        self.lbl_inicio.image = self.img_mansion
        self.lbl_inicio.pack()

        tk.Button(self.frame_inicio, text="Comenzar", font=("Courier New", 20),
                  command=self.mostrar_menu).pack(pady=20)

    def crear_coartadas(self):
        loc_aux = [l for l in self.locaciones if l != self.culpable[1]]
        arm_aux = [a for a in self.armas if a != self.culpable[2]]
        random.shuffle(loc_aux)
        random.shuffle(arm_aux)

        self.coartadas = {}
        for i, p in enumerate(self.personajes):
            loc_vista = loc_aux[i % len(loc_aux)]
            arma_vista = arm_aux[i % len(arm_aux)]
            self.coartadas[p] = (loc_vista, arma_vista)

    def mostrar_menu(self):
        self.frame_inicio.pack_forget()
        self.limpiar_pantalla()

        self.frame_menu = tk.Frame(self.root, bg="black")
        self.frame_menu.pack(fill="both", expand=True)

        texto = (
            "¡Oh, señor Poirot, qué bueno que ha llegado!\n"
            "Ha ocurrido un terrible asesinato en la mansión. \n"
            "Debe descubrir quién fue el culpable, dónde y con qué arma.\n"
            f"Tendrá solo {self.intentos} intentos para resolver el misterio."
        )
        tk.Label(self.frame_menu, text=texto, fg="yellow", bg="black",
                 font=("Courier New", 20), justify="center", wraplength=700).pack(pady=20)

        tk.Label(self.frame_menu, text=f"Intentos restantes: {self.intentos}",
                 fg="yellow", bg="black", font=("Courier New", 14)).pack(pady=10)

        tk.Button(self.frame_menu, text="Preguntar por personaje", font=("Courier New", 14),
                  command=self.menu_personaje).pack(pady=5)
        tk.Button(self.frame_menu, text="Preguntar por locación", font=("Courier New", 14),
                  command=self.menu_locacion).pack(pady=5)
        tk.Button(self.frame_menu, text="Preguntar por arma", font=("Courier New", 14),
                  command=self.menu_arma).pack(pady=5)

    def menu_personaje(self):
        self.mostrar_opciones(self.personajes, tipo="personaje")

    def menu_locacion(self):
        self.mostrar_opciones(self.locaciones, tipo="locacion")

    def menu_arma(self):
        self.mostrar_opciones(self.armas, tipo="arma")

    def mostrar_opciones(self, lista, tipo):
        self.frame_menu.pack_forget()
        self.limpiar_pantalla()
        
        self.frame_opciones = tk.Frame(self.root, bg="black")
        self.frame_opciones.pack(fill="both", expand=True)
        
        tk.Label(self.frame_opciones, text=f"Seleccione un {tipo}:",
                 fg="white", bg="black", font=("Courier New", 16)).pack(pady=15)

        ancho, alto = 120, 120  

        grid_frame = tk.Frame(self.frame_opciones, bg="black")
        grid_frame.pack()
        
        columnas = 3  
        
        for i, elemento in enumerate(lista):
            try:
                img = Image.open(f"{elemento}.png").resize((ancho, alto))
            except Exception:
                img = Image.open("Mansion.png").resize((ancho, alto))  # imagen por defecto

            img_tk = ImageTk.PhotoImage(img)

            subframe = tk.Frame(grid_frame, bg="black")
            subframe.grid(row=i // columnas, column=i % columnas, padx=15, pady=15)

            lbl = tk.Label(subframe, image=img_tk, bg="black")
            lbl.image = img_tk  
            lbl.pack()

            tk.Button(subframe, text=elemento, font=("Courier New", 12),
                      command=lambda e=elemento, t=tipo: self.resultado_pregunta(e, t)
                      ).pack(pady=5)

        tk.Button(self.frame_opciones, text="Volver", font=("Courier New", 12),
                  command=self.mostrar_menu).pack(pady=20)

    def resultado_pregunta(self, eleccion, tipo):
        self.frame_opciones.pack_forget()
        self.limpiar_pantalla()

        frame_res = tk.Frame(self.root, bg="black")
        frame_res.pack(fill="both", expand=True)

        culpable = False
        mensaje = ""

        if tipo == "personaje":
            if eleccion == self.culpable[0]:
                img = PhotoImage(file=f"{eleccion}_culpable.png")
                mensaje = f"{eleccion}: ¿Yo? Bueno, estaba en... eh... bah, todo esto es absurdo, detective. No diré más."
                culpable = True
            else:
                img = PhotoImage(file=f"{eleccion}_inocente.png")
                loc, arma = self.coartadas[eleccion]
                mensaje = f"{eleccion}: Esto es terrible, señor Poirot, es un alivio que está aquí. Si le sirve de algo, yo vi la {arma.lower()} en {loc.lower()}."

        elif tipo == "locacion":
            if eleccion == self.culpable[1]:
                img = PhotoImage(file=f"{eleccion}_culpable.png")
                mensaje = "Hum, hum... manchas de sangre. Estoy un paso más cerca este misterio."
                culpable = True
            else:
                img = PhotoImage(file=f"{eleccion}_inocente.png")
                mensaje = "Ah. Nada aquí por ahora. \nNecesito buscar en otro lado."

        elif tipo == "arma":
            if eleccion == self.culpable[2]:
                img = PhotoImage(file=f"{eleccion}_culpable.png")
                mensaje = f"Indiscutiblemente fue usada en el crimen. Le guardaré como evidencia. \n Cada vez estoy más cerca."
                culpable = True
            else:
                img = PhotoImage(file=f"{eleccion}_inocente.png")
                mensaje = f"La {eleccion.lower()} está limpia y en su lugar habitual. \nTengo que seguir investigando."

        lbl = tk.Label(frame_res, image=img, bg="black")
        lbl.image = img
        lbl.pack()

        tk.Label(frame_res, text=mensaje, fg="white", bg="black",
                 font=("Courier New", 14), wraplength=700).pack(pady=20)

        self.intentos -= 1
        if self.intentos <= 0:
            tk.Button(frame_res, text="Finalizar", command=self.final_juego).pack(pady=10)
        else:
            tk.Button(frame_res, text="Continuar", command=self.mostrar_menu).pack(pady=10)

    def final_juego(self):
        self.limpiar_pantalla()
        frame_fin = tk.Frame(self.root, bg="black")
        frame_fin.pack(fill="both", expand=True)

        lbl = tk.Label(frame_fin, image=self.img_mayordomo, bg="black")
        lbl.image = self.img_mayordomo
        lbl.pack()

        tk.Label(frame_fin, text="Señor Poirot, me temo que no hay más tiempo.\nNecesita presentar sus conclusiones.",
                 fg="white", bg="black", font=("Courier New", 14)).pack(pady=20)

        tk.Label(frame_fin, text="¿Quién fue el culpable?", fg="yellow", bg="black").pack()
        self.sospechoso = tk.StringVar()
        tk.Entry(frame_fin, textvariable=self.sospechoso).pack()

        tk.Label(frame_fin, text="¿En qué locación ocurrió?", fg="yellow", bg="black").pack()
        self.lugar = tk.StringVar()
        tk.Entry(frame_fin, textvariable=self.lugar).pack()

        tk.Label(frame_fin, text="¿Con qué arma?", fg="yellow", bg="black").pack()
        self.arma = tk.StringVar()
        tk.Entry(frame_fin, textvariable=self.arma).pack()

        tk.Button(frame_fin, text="Resolver", command=self.verificar_solucion).pack(pady=15)

    def verificar_solucion(self):
        sospechoso = self.sospechoso.get().capitalize()
        lugar = self.lugar.get().capitalize()
        arma = self.arma.get().capitalize()

        self.limpiar_pantalla()
        frame_res = tk.Frame(self.root, bg="black")
        frame_res.pack(fill="both", expand=True)

        caso_real = f"Caso real: {self.culpable[0]} en {self.culpable[1]} con {self.culpable[2]}."
        tk.Label(frame_res, text=caso_real, fg="yellow", bg="black", font=("Courier New", 14)).pack(pady=20)

        if (sospechoso, lugar, arma) == self.culpable:
            lbl = tk.Label(frame_res, image=self.img_policia, bg="black")
            lbl.image = self.img_policia
            lbl.pack()
            tk.Label(frame_res, text="¡Increíble! ¡Ha resuelto el caso, señor Poirot! \n\n WIN", fg="lightgreen", bg="black",
                     font=("Courier New", 20)).pack(pady=20)
        else:
            lbl = tk.Label(frame_res, image=self.img_sangre, bg="black")
            lbl.image = self.img_sangre
            lbl.pack()
            tk.Label(frame_res, text="El crimen no fue resuelto. Usted ha fallado, detective. \n\nGAME OVER", fg="red", bg="black",
                     font=("Courier New", 20)).pack(pady=20)

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

root = tk.Tk()
juego = JuegoClue(root)
root.mainloop()

