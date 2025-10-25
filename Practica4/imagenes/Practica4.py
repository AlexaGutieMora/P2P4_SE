import random
intentos = 10

personajes = ["Escarlata", "Mostaza", "Azulino", "Verdi", "Moradillo"]
locaciones = ["Salón", "Cocina", "Patio", "Habitación", "Baño"]
armas = ["Daga", "Candelabro", "Pistola", "Soga", "Llave"]

finales = [
    ("Moradillo", "Cocina", "Pistola"),
    ("Mostaza", "Salón", "Llave"),
    ("Verdi", "Patio", "Soga"),
    ("Azulino", "Baño", "Daga"),
    ("Escarlata", "Habitación", "Candelabro"),
]

culpable = random.choice(finales)
coartadas = {}
loc_aux = [l for l in locaciones if l != culpable[1]]
arm_aux = [a for a in armas if a != culpable[2]]
random.shuffle(loc_aux)
random.shuffle(arm_aux)

for i, p in enumerate(personajes):
    loc_vista = loc_aux[i % len(loc_aux)]
    arma_vista = arm_aux[i % len(arm_aux)]
    coartadas[p] = (loc_vista, arma_vista)

def preguntar_personaje(nombre):
    if nombre == culpable[0]:
        print(f"{nombre}: ++++¿Yo? Bueno, estaba en... eh... bah, todo esto es absurdo, detective. No diré más. ")
    else:
        loc, arma = coartadas[nombre]
        print(f"{nombre}: ---Esto es terrible, señor Poirot, es un alivio que esté aquí. Si le sirve en algo, vi la {arma.lower()} en {loc.lower()}.")

def preguntar_locacion(nombre):
    if nombre == culpable[1]:
        print("+++Hum, hum... manchas de sangre. Estoy un paso más cerca de resolver este misterio.")
    else:
        print("---Ah. Nada aquí por ahora. Necesito buscar en otro lado.")

def preguntar_arma(nombre):
    if nombre == culpable[2]:
        print(f"++++{nombre.lower()} fue indiscutiblemente usada en el crimen, la guardaré como evidencia.")
    else:
        print(f"---. La {nombre.lower()} está limpia y en su lugar habitual. Tengo que seguir investigando")

print("¡Señor Poirot, qué bueno que ha llegado. Ha ocurrido un terrible asesinato en la mansión.")
print("Debe descubrir quién fue el culpable, dónde y con qué arma.")
print("Tendrá solo 10 intentos para hacer preguntas y finalizar el misterio.\n")

while intentos > 0:
    print(f"\nIntentos restantes: {intentos}")
    print("¿Qué deseas preguntar?")
    print("1. Personaje")
    print("2. Locación")
    print("3. Arma")
    opcion = input("Elige una opción (1-3): ")
    if opcion == "1":
        print("\nPersonajes disponibles:", ", ".join(personajes))
        eleccion = input("¿Sobre qué personaje deseas preguntar?: ").capitalize()
        preguntar_personaje(eleccion)
    elif opcion == "2":
        print("\nLocaciones disponibles:", ", ".join(locaciones))
        eleccion = input("¿Sobre qué locación deseas preguntar?: ").capitalize()
        preguntar_locacion(eleccion)
    elif opcion == "3":
        print("\nArmas disponibles:", ", ".join(armas))
        eleccion = input("¿Sobre qué arma deseas preguntar?: ").capitalize()
        preguntar_arma(eleccion)
    else:
        print("Opción no válida.")
        continue

    intentos -= 1

print("\nSeñor Poirot, me temo que no hay más tiempo. Necesita presentar sus conclusiones.")
sospechoso = input("¿Quién fue el culpable?: ").capitalize()
lugar = input("¿En qué locación ocurrió?: ").capitalize()
arma = input("¿Con qué arma?: ").capitalize()
aciertos = [False, False, False]
if sospechoso == culpable[0]:
    aciertos[0] = True
if lugar == culpable[1]:
    aciertos[1] = True
if arma == culpable[2]:
    aciertos[2] = True
print(f"Caso real: {culpable[0]} en el/la {culpable[1]} con la {culpable[2]}.\n")
if all(aciertos):
    print("Oh, señor Poirot, ¡ha resuelto el caso!")
else:
    print("XXXXXXXXXXXXX GAME OVER XXXXXXXXXXXXXXXXXX")
    if not aciertos[0]:
        print(f"XXXXX El personaje no era {sospechoso}.XXXXX")
    if not aciertos[1]:
        print(f"XXXXX La locación no era {lugar}.XXXXX")
    if not aciertos[2]:
        print(f"XXXXX El arma no era {arma.lower()}.XXXXXX")
    print("Inténtelo de nuevo, detective.")