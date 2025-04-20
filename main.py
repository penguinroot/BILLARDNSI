import math
import tkinter as tk
from tkinter import messagebox, simpledialog
import time

# Variables globales
billeb_id = None
global bille_x
global bille_y
queue_id = None
angle_actuel = 0
rayon_bille = 15
puiss = 100
marge = 60
poidsqueue = 0.5


def drawcircle(canv, x, y, rad,color):
    canv.create_oval(x - rad, y - rad, x + rad, y + rad, width=0, fill=color, outline=color)
    return canv.find_closest(x, y)[0]

def start():
    messagebox.showinfo("Placez la bille", "Cliquez dans la zone verte, à droite de la ligne blanche pour placer la bille.")
    canvas.bind("<Button-1>", place_bille)
def debug_keypress(event):
    print(f"Touche pressée : {event.keysym}")



def place_bille(event):
    global billeb_id,bille_x,bille_y
    ligne_placement = marge + 3/4 * (w - 2 * marge)
    if event.x > ligne_placement:
        billeb_id = drawcircle(canvas, event.x, event.y, rayon_bille,"white")
        bille_x, bille_y = event.x, event.y
        print(event.x, event.y)
        canvas.unbind("<Button-1>")
        place_canne()
    else:
        messagebox.showwarning("Mauvais placement", "Placez la bille à droite de la ligne blanche !")
def place_canne():
        global queue_id, angle_actuel, puiss,bille_x, bille_y,x1, y1, x2, y2
        x1, y1, x2, y2 = canvas.coords(billeb_id)
        dessin_canne()
        root.bind("<Left>", rotate_left)
        root.bind("<Right>", rotate_right)
        root.bind("<Return>", validate_angle)
        root.bind("<Up>", more_power)
        root.bind("<Down>", less_power)
        root.bind("<Shift_R>", set_puissance)
def dessin_canne():
    global queue_id,angle_actuel, puiss,x1, y1, x2, y2,bille_x, bille_y
    if queue_id:
        canvas.delete(queue_id)
    print("la bille est en ", bille_x, bille_y)
    # Dépendance de la longueur à la puissance
    longueur = 50 + puiss  # Tu peux ajuster le "+ puiss" si c'est trop long
    x2 = bille_x + longueur * math.sin(math.radians(angle_actuel))
    y2 = bille_y - longueur * math.cos(math.radians(angle_actuel))
    queue_id = canvas.create_line(bille_x, bille_y, x2, y2, fill="red", width=4)

def rotate_left(event=None):
    global angle_actuel
    angle_actuel = (angle_actuel - 1) % 360
    dessin_canne()

def rotate_right(event=None):
    global angle_actuel
    angle_actuel = (angle_actuel + 1) % 360
    dessin_canne()

def validate_angle(event=None):
    root.unbind("<Left>")
    root.unbind("<Right>")
    root.unbind("<Return>")
    print("Angle actuel : ", angle_actuel)

def more_power(event=None):
    global puiss
    puiss += 1
    dessin_canne()
    print("Puissance actuelle : ", puiss)
    return puiss

def less_power(event=None):
    global puiss
    puiss -= 1
    dessin_canne()
    print("Puissance actuelle : ", puiss)
    return puiss

def set_puissance(event=None):
    global puiss
    root.unbind("<Shift_R>")
    root.unbind("<Up>")
    root.unbind("<Down>")
    print("Puissance actuelle : ", puiss)
    canvas.delete(queue_id)  # Enlève la queue du canvas
    shoot()

def shoot():
    global billeb_id, angle_actuel, puiss, bille_x, bille_y, x1, y1, x2, y2
    angle_rad = math.radians(angle_actuel)
    Ec = 1/2*poidsqueue*puiss*puiss #puiss est = à la vitesse
    print("Énergie cinétique : ", Ec)
    dx = -Ec * math.sin(angle_rad)
    dy = Ec * math.cos(angle_rad)
    friction = 0.90

    while abs(dx) > 1 or abs(dy) > 1:
        canvas.move(billeb_id, dx / 100, dy / 100)
        x1, y1, x2, y2 = canvas.coords(billeb_id)
        dx, dy = check_collision(x1, y1, x2, y2, dx, dy)
        dx *= friction
        dy *= friction
        canvas.update()
        time.sleep(0.05)
    print("Fin du mouvement")
    bille_x, bille_y = (x1+x2)/2, (y1+y2)/2
    print("Position finale de la bille : ", bille_x, bille_y)
    place_canne()

# Définir les positions des trous


def check_collision(x1, y1, x2, y2, dx, dy):
    # Vérification des collisions avec les bords
    if x1 <= marge + rayon_bille or x2 >= w - marge - rayon_bille:
        dx = -dx
    if y1 <= marge + rayon_bille or y2 >= h - marge - rayon_bille:
        dy = -dy
    
    if x1 < tombe[0][0] and y1 < tombe[0][1]:
        print("bille dans le trou1")
        canvas.delete(billeb_id)  # Enlève la bille du canvas
    if x2 > tombe[1][0] and y1 < tombe[1][1]:
        print("bille dans le trou2")
        canvas.delete(billeb_id)
    if x1 < tombe[2][0] and y2 > tombe[2][1]:
        print("bille dans le trou3")
        canvas.delete(billeb_id)
    if x2 > tombe[3][0] and y2 > tombe[3][1]:
        print("bille dans le trou4")
        canvas.delete(billeb_id)

    return dx, dy


# Création de la fenêtre
root = tk.Tk()
root.attributes('-fullscreen', True)
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
print(w, h)
canvas = tk.Canvas(root, bg='#1B4D3E', width=w, height=h)
canvas.pack()
canvas.focus_set() 
root.bind("<KeyPress>", debug_keypress) 

# Bordures du billard
canvas.create_rectangle(marge, marge, w - marge, h - marge, outline="gray", width=10)

# Ligne blanche de placement
ligne_placement = marge + 3/4 * (w - 2 * marge)
canvas.create_line(ligne_placement, marge, ligne_placement, h - marge, fill="white", width=10)
# Trous pour le billard (experimental)
decal =10
trous = [
    (marge+decal, marge+decal),  # Trou en haut à gauche
    (w - marge-decal, marge+decal),  # Trou en haut à droite
    (marge+decal, h - marge - decal),  # Trou en bas à gauche
    (w - marge - decal, h - marge - decal),  # Trou en bas à droite
]
import array as arr

i=0
global tombe
tombe=[]
tombe.append([])
tombe.append([])
tombe.append([])
tombe.append([])
for trou_x, trou_y in trous:
    canvas.create_oval(
        trou_x - rayon_bille*1.5, trou_y - rayon_bille*1.5, 
        trou_x + rayon_bille*1.5, trou_y + rayon_bille*1.5, 
        fill='black', outline='black'
    )
    if i==0 :
        tombe[i]=trou_x + rayon_bille*1.5, trou_y + rayon_bille*1.5
    if i== 2 :
        tombe[i]=trou_x + rayon_bille*1.5, trou_y - rayon_bille*1.5
    if i==1 :
        tombe[i]=trou_x - rayon_bille*1.5, trou_y + rayon_bille*1.5
    if i==3 :
        tombe[i]=trou_x - rayon_bille*1.5, trou_y - rayon_bille*1.5
    i=i+1

liste_boules = []
couleurs = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan", "white", "black", "gray", "brown", "lime", "magenta", "navy"]
taille_boule = 15
ecart = taille_boule * 2 + 2
depart_x = 300
depart_y = 100

compteur_couleur = 0
nblignes = 5

for colonne in range(nblignes):
    nbboules = colonne + 1
    pos_x = depart_x - colonne * ecart  # Décalage vers la gauche pour chaque colonne
    pos_y = depart_y 
    for boule in range(nbboules):
        y = pos_y + boule * ecart  # Empile verticalement dans la colonne
        couleur = couleurs[compteur_couleur % len(couleurs)]
        boule = drawcircle(canvas, pos_x, y, taille_boule, couleur)
        x1, y1, x2, y2 = canvas.coords(boule)
        centre_x = x1 + taille_boule
        centre_y = y1 + taille_boule
        liste_boules.append([f"boule{compteur_couleur+1}", centre_x, centre_y, pos_x, y, couleur, 0])
        compteur_couleur += 1

print(liste_boules)


root.after(100, start)
root.mainloop()
