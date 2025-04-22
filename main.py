import tkinter as tk
from jeu import JeuDeBillard  # Importez la classe du jeu

class MenuPrincipal:
    def __init__(self):
        self.racine = tk.Tk()
        self.racine.title("Jeu de Billard - Menu Principal")
        self.racine.geometry("400x300")
        
        # Centrer la fenêtre
        largeur_ecran = self.racine.winfo_screenwidth()
        hauteur_ecran = self.racine.winfo_screenheight()
        x = (largeur_ecran - 400) // 2
        y = (hauteur_ecran - 300) // 2
        self.racine.geometry(f"400x300+{x}+{y}")
        
        self.creer_widgets()
        
    def creer_widgets(self):
        # Titre
        label_titre = tk.Label(self.racine, text="Jeu de Billard", font=("Arial", 24, "bold"))
        label_titre.pack(pady=20)
        
        # Bouton Jouer
        btn_jouer = tk.Button(self.racine, text="Jouer", command=self.lancer_jeu, 
                            font=("Arial", 16), width=15, height=2)
        btn_jouer.pack(pady=10)
        
        # Bouton Quitter
        btn_quitter = tk.Button(self.racine, text="Quitter", command=self.racine.quit,
                              font=("Arial", 16), width=15, height=2)
        btn_quitter.pack(pady=10)
        
        # Information sur les contrôles
        label_controles = tk.Label(self.racine, 
                                 text="Contrôles:\nFlèches pour ajuster\nEspace pour tirer", 
                                 font=("Arial", 12))
        label_controles.pack(pady=10)
    
    def lancer_jeu(self):
        self.racine.destroy()  # Ferme le menu
        jeu = JeuDeBillard()   # Crée le jeu
        jeu.commencer()        # Lance le jeu
    
    def demarrer(self):
        self.racine.mainloop()

if __name__ == "__main__":
    menu = MenuPrincipal()
    menu.demarrer()