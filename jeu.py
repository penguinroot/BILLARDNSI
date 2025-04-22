from email import message
import math
import sys
import tkinter as tk
from tkinter import messagebox
import time
# Removed unused tkinter import
class Bille:
    def __init__(self, canevas, numero, x, y, rayon, couleur):
        self.canevas = canevas
        self.numero = numero
        self.x = x
        self.y = y
        self.rayon = rayon
        self.couleur = couleur
        self.id = self.dessiner()
        self.text_id = self.dessiner_nombre()  # ID pour le texte
        self.vx = 0.0
        self.vy = 0.0

    def dessiner(self):
        return self.canevas.create_oval(
            self.x - self.rayon,
            self.y - self.rayon,
            self.x + self.rayon,
            self.y + self.rayon,
            width=0,
            fill=self.couleur,
            outline=self.couleur
        )

    def dessiner_nombre(self):
        return self.canevas.create_text(
            self.x,
            self.y,
            text=str(self.numero),
            fill="white",
            font=("Arial", 12, "bold")
        )

    def mettre_a_jour_position(self, x, y):
        self.x = x
        self.y = y
        self.canevas.coords(self.id, x - self.rayon, y - self.rayon, x + self.rayon, y + self.rayon)
        self.canevas.coords(self.text_id, x, y)  # Met à jour la position du texte

class Canne:
    def __init__(self, canevas, bille):
        self.canevas = canevas
        self.bille = bille
        self.angle = 90
        self.puissance = 100
        self.proj_id = None
        self.id = None
        self.poids = 0.5
        self.wtour=0
        self.label_info = tk.Label(self.canevas, text='', bg='lightblue', font=("Arial", 16))
        self.label_info.place(x=1000, y=10)


    def dessiner(self):
        if self.id:
            self.canevas.delete(self.id)
        if self.proj_id:
            self.canevas.delete(self.proj_id)

        # Calcul du vecteur directionnel en fonction de l'angle
        dx = math.sin(math.radians(self.angle))
        dy = math.cos(math.radians(self.angle))

        # Longueur de la canne (ligne rouge)
        longueur = 50 + self.puissance
        x2 = self.bille.x + dx * longueur
        y2 = self.bille.y - dy * longueur
        self.id = self.canevas.create_line(
            self.bille.x, self.bille.y,
            x2, y2,
            fill="red", width=4
        )

        # Longueur de la projection (ligne bleue)
        longueur_proj = max(self.canevas.winfo_width(), self.canevas.winfo_height())
        x_proj = self.bille.x - dx * longueur_proj
        y_proj = self.bille.y + dy * longueur_proj
        self.proj_id = self.canevas.create_line(
            self.bille.x, self.bille.y,
            x_proj, y_proj,
            fill="white", width=2, dash=(5, 2)
        )
        self.label_info.config(text=f'Puissance : {self.puissance}  | Angle : {self.angle}°')

    def tourner_gauche(self):
        self.wtour =self.wtour+0.5
        self.angle = (self.angle - self.wtour) % 360
        self.dessiner()

    def tourner_droite(self):
        self.wtour=self.wtour+0.5
        self.angle = (self.angle + self.wtour) % 360
        self.dessiner()
    def raz(self):
        self.wtour=0

    def ajuster_puissance(self, delta):
        self.puissance = min(120,max(0, self.puissance + delta))
        self.dessiner()
class JeuDeBillard:
    def __init__(self):
        self.racine = tk.Tk()
        self.racine.attributes('-fullscreen', True)
        self.largeur = self.racine.winfo_screenwidth()
        self.hauteur = self.racine.winfo_screenheight()

        self.marge = 60
        self.rayon_bille = 15
        self.billes = []
        self.trous = []
        self.billes_tombees = []
        self.position_precedente = None
        self.temps_precedent = None

        # Variables pour deux joueurs
        self.joueur_actuel = 1
        self.points_j1 = 0
        self.points_j2 = 0
        self.en_placement_apres_faute = False
        self.faute = False
        self.billes_tombees_tour = []

        self.creer_canevas()
        self.creer_trous()
        self.creer_billes_depart()

        self.label_info = tk.Label(self.racine, text='', bg='lightblue', font=("Arial", 16))
        self.label_info.place(x=10, y=10)

        self.canne = None
        self.bille_blanche = None

    def creer_canevas(self):
        self.canevas = tk.Canvas(self.racine, bg='#1B4D3E', width=self.largeur, height=self.hauteur)
        self.canevas.pack()
        self.canevas.create_rectangle(
            self.marge,
            self.marge,
            self.largeur - self.marge,
            self.hauteur - self.marge,
            outline="gray",
            width=10
        )
        ligne_placement = self.marge + 3/4 * (self.largeur - 2 * self.marge)
        self.canevas.create_line(
            ligne_placement,
            self.marge,
            ligne_placement,
            self.hauteur - self.marge,
            fill="white",
            width=10
        )

    def creer_trous(self):
        decalage = 10
        positions = [
            (self.marge + decalage, self.marge + decalage),
            (self.largeur - self.marge - decalage, self.marge + decalage),
            (self.marge + decalage, self.hauteur - self.marge - decalage),
            (self.largeur - self.marge - decalage, self.hauteur - self.marge - decalage)
        ]
        for i, (x, y) in enumerate(positions):
            self.canevas.create_oval(
                x - self.rayon_bille*1.5,
                y - self.rayon_bille*1.5,
                x + self.rayon_bille*1.5,
                y + self.rayon_bille*1.5,
                fill='black'
            )
            if i == 0:
                tx, ty = x + self.rayon_bille*1.5, y + self.rayon_bille*1.5
            elif i == 1:
                tx, ty = x - self.rayon_bille*1.5, y + self.rayon_bille*1.5
            elif i == 2:
                tx, ty = x + self.rayon_bille*1.5, y - self.rayon_bille*1.5
            else:
                tx, ty = x - self.rayon_bille*1.5, y - self.rayon_bille*1.5
            self.trous.append((tx, ty))

    def creer_billes_depart(self):
        couleurs = ["red", "blue", "green", "yellow", "black", "orange"]
        x_depart, y_depart = 500, 400
        espacement = self.rayon_bille * 2 + 2
        k = 0
        for i in range(1, 6):
            for j in range(i):
                y = y_depart + (j - (i - 1) / 2) * espacement
                x = x_depart - (i - 1) * espacement
                if k < len(couleurs):
                    bille = Bille(self.canevas, k, x, y, self.rayon_bille, couleurs[k])
                    self.billes.append(bille)
                    k += 1

    def commencer(self):
        self.canevas.bind("<Button-1>", self.placer_bille_blanche)
        self.mettre_a_jour_infos_en_boucle()
        self.racine.mainloop()

    def placer_bille_blanche(self, event):
        ligne_placement = self.marge + 3/4 * (self.largeur - 2 * self.marge)
        if self.en_placement_apres_faute or event.x > ligne_placement:
            self.bille_blanche = Bille(self.canevas, -1, event.x, event.y, self.rayon_bille, "white")
            self.billes.append(self.bille_blanche)
            self.canne = Canne(self.canevas, self.bille_blanche)
            self.configurer_controles()
            self.en_placement_apres_faute = False
        else:
            messagebox.showwarning("Mauvais placement", "Placez la bille à droite de la ligne blanche !")

    def configurer_controles(self):
        self.canevas.unbind("<Button-1>")
        self.canne.dessiner()
        self.canevas.focus_set()
        self.racine.bind("<Left>", lambda _: self.canne.tourner_gauche())
        self.racine.bind("<KeyRelease-Left>", lambda _: self.canne.raz())
        self.racine.bind("<Right>", lambda _: self.canne.tourner_droite())
        self.racine.bind("<KeyRelease-Right>", lambda _: self.canne.raz())
        self.racine.bind("<Up>", lambda _: self.canne.ajuster_puissance(1))
        self.racine.bind("<Down>", lambda _: self.canne.ajuster_puissance(-1))
        self.racine.bind("<Return>", self.valider_angle)
        self.racine.bind("<space>", self.tirer)

    def valider_angle(self, _):
        self.racine.unbind("<Left>")
        self.racine.unbind("<Right>")
        self.racine.unbind("<Return>")

    def tirer(self, event):
        self.racine.unbind("<Shift_R>")
        self.racine.unbind("<Up>")
        self.racine.unbind("<Down>")
        self.racine.unbind("<space>")
        self.valider_angle(event)
        self.canevas.delete(self.canne.id)
        self.canevas.delete(self.canne.proj_id)
        angle_rad = math.radians(self.canne.angle)
        energie_cinetique = 0.5 * self.canne.poids * self.canne.puissance ** 2
        self.bille_blanche.vx = -energie_cinetique * math.sin(angle_rad) / 100
        self.bille_blanche.vy = energie_cinetique * math.cos(angle_rad) / 100
        self.mettre_a_jour_physique()

    def mettre_a_jour_physique(self):
        en_mouvement = False
        for bille in self.billes:
            bille.vx *= 0.99
            bille.vy *= 0.99
            nouvelle_x = bille.x + bille.vx
            nouvelle_y = bille.y + bille.vy
            vx, vy = self.verifier_collision(bille, bille.vx, bille.vy)
            bille.vx, bille.vy = vx, vy
            if bille in self.billes:
                bille.mettre_a_jour_position(nouvelle_x, nouvelle_y)
                if abs(bille.vx) > 1 or abs(bille.vy) > 1:
                    en_mouvement = True
        self.verifier_collisions_billes()

        if en_mouvement:
            self.racine.after(20, self.mettre_a_jour_physique)
        else:
            # Gestion du changement de tour
            if not self.faute and len(self.billes_tombees_tour) == 0:
                self.joueur_actuel = 2 if self.joueur_actuel == 1 else 1
            
            self.billes_tombees_tour = []
            self.faute = False
            
            for bille in self.billes:
                bille.vx = 0.0
                bille.vy = 0.0
                
            if self.bille_blanche and self.bille_blanche in self.billes:
                self.canne = Canne(self.canevas, self.bille_blanche)
                self.configurer_controles()

    def verifier_collision(self, bille, vx, vy):
        x1 = bille.x - bille.rayon
        y1 = bille.y - bille.rayon
        x2 = bille.x + bille.rayon
        y2 = bille.y + bille.rayon

        if x1 <= self.marge:
            vx = abs(vx)
        elif x2 >= self.largeur - self.marge:
            vx = -abs(vx)
        if y1 <= self.marge:
            vy = abs(vy)
        elif y2 >= self.hauteur - self.marge:
            vy = -abs(vy)

        for tx, ty in self.trous:
            distance = math.hypot(bille.x - tx, bille.y - ty)
            if distance < self.rayon_bille * 1.5:
                self.canevas.delete(bille.id)
                self.canevas.delete(bille.text_id)

                if bille == self.bille_blanche:
                    self.billes.remove(bille)
                    self.bille_blanche = None
                    self.faute = True
                    self.joueur_actuel = 2 if self.joueur_actuel == 1 else 1
                    self.en_placement_apres_faute = True
                    messagebox.showinfo('Info', f"Joueur {self.joueur_actuel}, placez la bille blanche")
                    self.canevas.bind("<Button-1>", self.placer_bille_blanche)
                    return vx, vy

                elif bille.couleur == "black":
                    billes_restantes = [b for b in self.billes if b != self.bille_blanche and b.couleur != "black"]
                    
                    if len(billes_restantes) == 0:
                        messagebox.showinfo("Victoire", f"Joueur {self.joueur_actuel} gagne !")
                    else:
                        messagebox.showinfo("Défaite", f"Joueur {self.joueur_actuel} perd !")
                    time.sleep(2)
                    self.racine.destroy()
                    return vx, vy

                else:
                    if self.joueur_actuel == 1:
                        self.points_j1 += 1
                    else:
                        self.points_j2 += 1
                    self.billes_tombees_tour.append(bille)
                    self.billes.remove(bille)
                    self.billes_tombees.append(bille)
                    
                    xdep = 500
                    ydep = 30
                    self.canevas.delete("billes_tombees")
                    for i, b in enumerate(self.billes_tombees):
                        self.canevas.create_oval(
                            xdep + i*30 - self.rayon_bille,
                            ydep - self.rayon_bille,
                            xdep + i*30 + self.rayon_bille,
                            ydep + self.rayon_bille,
                            fill=b.couleur,
                            tags="billes_tombees"
                        )
        return vx, vy

    def verifier_collisions_billes(self):
        for i in range(len(self.billes)):
            b1 = self.billes[i]
            for j in range(i + 1, len(self.billes)):
                b2 = self.billes[j]
                dx = b2.x - b1.x
                dy = b2.y - b1.y
                distance = math.hypot(dx, dy)
                distance_min = b1.rayon + b2.rayon
                if distance < distance_min:
                    nx = dx / distance
                    ny = dy / distance
                    dvx = b2.vx - b1.vx
                    dvy = b2.vy - b1.vy
                    produit_scalaire = dvx * nx + dvy * ny
                    if produit_scalaire > 0:
                        continue
                    e = 1.0
                    j = -(1 + e) * produit_scalaire / (2)
                    b1.vx -= j * nx
                    b1.vy -= j * ny
                    b2.vx += j * nx
                    b2.vy += j * ny

    def mettre_a_jour_infos_en_boucle(self):
        texte_info = f'Joueur {self.joueur_actuel} | Points J1: {self.points_j1} | Points J2: {self.points_j2}'
        if hasattr(self, 'label_info'):
            self.label_info.config(text=texte_info)
        self.racine.after(100, self.mettre_a_jour_infos_en_boucle)
        
if __name__ == "__main__":
    jeu = JeuDeBillard()
    jeu.commencer()
