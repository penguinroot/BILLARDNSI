# 🎱 BILLARDNSI

Un projet de billard codé en **Python** avec **Tkinter** pour l’interface graphique.  
Le jeu propose une simulation simple mais complète : gestion des billes, des collisions, de la canne, du score et des conditions de victoire.

---

## 🚀 Fonctionnalités

- 🎮 **Gameplay complet** :
  - Placement de la bille blanche
  - Gestion de la puissance et de l’angle du tir
  - Détection des collisions (bille/mur, bille/bille, trous)
  - Gestion des fautes (bille blanche rentrée)
  - Victoire/défaite avec la bille noire

- 🎨 **Interface graphique soignée** :
  - Fond en dégradé
  - Ombres sur les billes
  - Traces de trajectoires
  - Ligne de projection pour viser
  - Popups personnalisés

- 👥 **Deux joueurs** :
  - Gestion des scores
  - Alternance des tours

---

## 📦 Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/penguinroot/BILLARDNSI.git
cd BILLARDNSI
````

### 2. Créer un environnement virtuel (optionnel mais recommandé)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Installer les dépendances

Le projet repose principalement sur **Tkinter** (déjà inclus avec Python) et **Pillow** :

```bash
pip install pillow
```

---

## ▶️ Lancement du jeu

```bash
python main.py
```

Le jeu démarre en **plein écran**.
Utilisez la souris pour viser et choisir la puissance, puis cliquez pour tirer.

---

## 🕹️ Commandes

* **Souris** : viser et tirer
* **Échap (Esc)** : quitter le plein écran
* **Boutons en bas de l’écran** :

  * 🎮 Nouvelle Partie
  * ❌ Quitter


## ⚠️ Limites connues

* Collision bille/bille simplifiée (pas de vraie conservation de l’énergie)
* Seulement 6 billes colorées + bille blanche (au lieu de 15 dans un vrai billard)
* Quelques incohérences graphiques (`reflection_id` à corriger)

---

## 🛠️ Améliorations possibles

* Ajouter un **mode 8-ball/9-ball**
* Améliorer la **physique des collisions**
* Ajouter des **sons et textures réalistes**
* Mode **multijoueur en ligne** via sockets
* Séparer le code en plusieurs fichiers pour plus de clarté

---
## Contribuer

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le dépôt.
2. Créez une branche pour votre fonctionnalité ou correction de bug :
   ```bash
   git checkout -b feature/ma-fonctionnalite
   ```
3. Commitez vos modifications :
   ```bash
   git commit -m "Ajout de ma fonctionnalité"
   ```
4. Poussez vers votre fork :
   ```bash
   git push origin feature/ma-fonctionnalite
   ```
5. Créez une pull request sur le dépôt principal.
---
## 👨‍💻 Auteur

Projet développé par **penguinroot** dans le cadre de la spécialité NSI.



