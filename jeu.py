from email import message
import math
import sys
import tkinter as tk
from tkinter import messagebox
import time

class Bille:
    def __init__(self, canevas, numero, x, y, rayon, couleur):
        self.canevas = canevas
        self.numero = numero
        self.x = x
        self.y = y
        self.rayon = rayon
        self.couleur = couleur
        self.id = self.dessiner()
        self.text_id = self.dessiner_nombre()
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
        self.canevas.coords(self.text_id, x, y)

class Canne:
    def __init__(self, canevas, bille):
        self.canevas = canevas
        self.bille = bille
        self.angle = 90
        self.puissance = 100
        self.proj_id = None
        self.id = None
        self.poids = 0.5
        self.wtour = 0
        self.label_info = tk.Label(self.canevas, text='', bg='lightblue', font=("Arial", 16))
        self.label_info.place(x=1000, y=10)

    def dessiner(self):
        if self.id:
            self.canevas.delete(self.id)
        if self.proj_id:
            self.canevas.delete(self.proj_id)

        dx = math.sin(math.radians(self.angle))
        dy = math.cos(math.radians(self.angle))

        longueur = 50 + self.puissance
        x2 = self.bille.x + dx * longueur
        y2 = self.bille.y - dy * longueur
        self.id = self.canevas.create_line(
            self.bille.x, self.bille.y,
            x2, y2,
            fill="red", width=4
        )

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
        self.wtour += 0.5
        self.angle = (self.angle - self.wtour) % 360
        self.dessiner()

    def tourner_droite(self):
        self.wtour += 0.5
        self.angle = (self.angle + self.wtour) % 360
        self.dessiner()

    def raz(self):
        self.wtour = 0

    def ajuster_puissance(self, delta):
        self.puissance = min(120, max(0, self.puissance + delta))
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
            friction = 0.98 - 0.02 * (math.hypot(bille.vx, bille.vy) / 100)
            friction = max(0.9, min(0.99, friction))
            
            bille.vx *= friction
            bille.vy *= friction
            
            nouvelle_x = bille.x + bille.vx
            nouvelle_y = bille.y + bille.vy
            
            vx, vy = self.verifier_collision(bille, bille.vx, bille.vy)
            bille.vx, bille.vy = vx, vy
            
            if bille in self.billes:
                bille.mettre_a_jour_position(nouvelle_x, nouvelle_y)
                if abs(bille.vx) > 0.5 or abs(bille.vy) > 0.5:
                    en_mouvement = True

        self.verifier_collisions_billes()

        if en_mouvement:
            self.racine.after(20, self.mettre_a_jour_physique)
        else:
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
        # Collisions avec les bords
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

        # Nouvelle détection des trous améliorée
        for tx, ty in self.trous:
            dx = bille.x - tx
            dy = bille.y - ty
            distance = math.hypot(dx, dy)
            rayon_effectif_trou = self.rayon_bille * 1.2
            
            vitesse = math.hypot(vx, vy)
            if vitesse == 0:
                continue
                
            dir_vx = vx / vitesse
            dir_vy = vy / vitesse
            
            dir_trou_x = dx / distance if distance != 0 else 0
            dir_trou_y = dy / distance if distance != 0 else 0
            
            alignement = (dir_vx * dir_trou_x) + (dir_vy * dir_trou_y)
            
            if (distance < rayon_effectif_trou and 
                alignement > 0.85 and
                vitesse > 2.5):
                
                # Animation de spirale avant suppression
                for i in range(10):
                    bille.x += (tx - bille.x) * 0.1
                    bille.y += (ty - bille.y) * 0.1
                    bille.mettre_a_jour_position(bille.x, bille.y)
                    self.racine.update()
                    time.sleep(0.03)
                
                self.gerer_bille_tombee(bille)
                return vx, vy
            
            elif rayon_effectif_trou < distance < rayon_effectif_trou + bille.rayon:
                angle = math.atan2(dy, dx)
                point_col_x = tx + rayon_effectif_trou * math.cos(angle)
                point_col_y = ty + rayon_effectif_trou * math.sin(angle)
                
                nx = (bille.x - point_col_x) / bille.rayon
                ny = (bille.y - point_col_y) / bille.rayon
                
                restitution = 0.6
                dot_product = vx * nx + vy * ny
                vx -= (1 + restitution) * dot_product * nx
                vy -= (1 + restitution) * dot_product * ny
                
                return vx * 0.8, vy * 0.8

        return vx, vy

    def gerer_bille_tombee(self, bille):
        self.canevas.delete(bille.id)
        self.canevas.delete(bille.text_id)

        if bille == self.bille_blanche:
            self.billes.remove(bille)
            self.bille_blanche = None
            self.faute = True
            self.en_placement_apres_faute = True
            messagebox.showinfo('Faute', "Bille blanche tombée ! Placez-la à nouveau.")
            self.canevas.bind("<Button-1>", self.placer_bille_blanche)
        elif bille.couleur == "black":
            self.verifier_fin_de_partie()
        else:
            if self.joueur_actuel == 1:
                self.points_j1 += 1
            else:
                self.points_j2 += 1
            self.billes.remove(bille)
            self.billes_tombees.append(bille)
            self.afficher_billes_tombees()
            
    def afficher_billes_tombees(self):
        xdep, ydep = 500, 30
        self.canevas.delete("billes_tombees")
        
        for i, b in enumerate(self.billes_tombees):
            self.canevas.create_oval(
                xdep + i*35 - self.rayon_bille,
                ydep - self.rayon_bille,
                xdep + i*35 + self.rayon_bille,
                ydep + self.rayon_bille,
                fill=b.couleur, outline="white",
                tags="billes_tombees"
            )
            self.canevas.create_text(
                xdep + i*35, ydep,
                text=str(b.numero), fill="white",
                font=("Arial", 10, "bold"),
                tags="billes_tombees"
            )

    def verifier_fin_de_partie(self):
        billes_restantes = [b for b in self.billes if b != self.bille_blanche and b.couleur != "black"]
        
        if not billes_restantes:
            messagebox.showinfo("Victoire", f"Joueur {self.joueur_actuel} a gagné !")
        else:
            messagebox.showinfo("Défaute", "La bille noire est tombée trop tôt !")
        
        self.racine.after(2000, self.racine.destroy)

    def verifier_collisions_billes(self):
        for i in range(len(self.billes)):
            b1 = self.billes[i]
            for j in range(i + 1, len(self.billes)):
                b2 = self.billes[j]
                dx = b2.x - b1.x
                dy = b2.y - b1.y
                distance = math.hypot(dx, dy)
                distance_min = b1.rayon + b2.rayon
                
                dvx = b2.vx - b1.vx
                dvy = b2.vy - b1.vy
                dot_product = dvx * dx + dvy * dy
                if dot_product > 0:
                    continue
                    
                if distance < distance_min:
                    overlap = distance_min - distance
                    nx = dx / distance
                    ny = dy / distance
                    
                    b1.x -= overlap * nx * 0.5
                    b1.y -= overlap * ny * 0.5
                    b2.x += overlap * nx * 0.5
                    b2.y += overlap * ny * 0.5
                    
                    m1, m2 = 1, 1
                    v1n = b1.vx * nx + b1.vy * ny
                    v2n = b2.vx * nx + b2.vy * ny
                    
                    v1t = -b1.vx * ny + b1.vy * nx
                    v2t = -b2.vx * ny + b2.vy * nx
                    
                    v1n_after = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
                    v2n_after = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)
                    
                    b1.vx = v1n_after * nx - v1t * ny
                    b1.vy = v1n_after * ny + v1t * nx
                    b2.vx = v2n_after * nx - v2t * ny
                    b2.vy = v2n_after * ny + v2t * nx

    def mettre_a_jour_infos_en_boucle(self):
        texte_info = f'Joueur {self.joueur_actuel} | Points J1: {self.points_j1} | Points J2: {self.points_j2}'
        if hasattr(self, 'label_info'):
            self.label_info.config(text=texte_info)
        self.racine.after(100, self.mettre_a_jour_infos_en_boucle)

if __name__ == "__main__":
    jeu = JeuDeBillard()
    jeu.commencer()