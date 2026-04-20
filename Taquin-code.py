import tkinter as tk
from tkinter import messagebox
import random
import os
from tkinter import messagebox  # Obligatoire pour afficher la fenêtre de victoire
class TaquinL1:
    def __init__(self, root):
        self.root = root
        self.root.title("Projet IN200 : Jeu du Taquin")
        
        # --- DONNÉES DU JEU ---
        self.taille = 4  # Grille 4x4
        self.solution = list(range(1, 16)) + [0] # [1, 2, ..., 15, 0]
        self.plateau = list(self.solution)
        self.historique = [] # Pile pour l'annulation (Undo)
        self.fichier_save = "sauvegarde_taquin.txt"
        
        # --- INTERFACE GRAPHIQUE ---
        self.boutons = []
        self.cadre_jeu = tk.Frame(self.root, bg="black", bd=2)
        self.cadre_jeu.pack(pady=10)
        
        # Création des 16 boutons
        for i in range(16):
            btn = tk.Button(self.cadre_jeu, text="", width=6, height=3, 
                            font=('Arial', 14, 'bold'),
                            command=lambda idx=i: self.jouer_coup(idx))
            btn.grid(row=i//4, column=i%4, padx=1, pady=1)
            self.boutons.append(btn)
            
        # --- BOUTONS DE CONTRÔLE ---
        cadre_ctrl = tk.Frame(self.root)
        cadre_ctrl.pack(pady=10)
        
        tk.Button(cadre_ctrl, text="Mélanger", command=self.nouveau_jeu).pack(side="left", padx=5)
        tk.Button(cadre_ctrl, text="Annuler (Undo)", command=self.annuler).pack(side="left", padx=5)
        tk.Button(cadre_ctrl, text="Sauvegarder", command=self.sauvegarder).pack(side="left", padx=5)
        tk.Button(cadre_ctrl, text="Charger", command=self.charger).pack(side="left", padx=5)
        
        # Lancement initial
        self.nouveau_jeu()

    def actualiser_affichage(self):
        """Met à jour le texte et la couleur des boutons selon self.plateau."""
        for i in range(16):
            valeur = self.plateau[i]
            if valeur == 0:
                self.boutons[i].config(text="", bg="#bdc3c7", state="disabled")
            else:
                self.boutons[i].config(text=str(valeur), bg="#ecf0f1", state="normal")

    def jouer_coup(self, i):
        """Déplace la case si elle est adjacente au vide."""
        vide = self.plateau.index(0)
        
        # Calcul des positions (ligne, colonne)
        r_clic, c_clic = i // 4, i % 4
        r_vide, c_vide = vide // 4, vide % 4
        
        # Distance de Manhattan doit être égale à 1 (Voisin direct)
        if abs(r_clic - r_vide) + abs(c_clic - c_vide) == 1:
            # On enregistre l'état actuel AVANT de bouger
            self.historique.append(list(self.plateau))
            
            # Échange des valeurs
            self.plateau[vide], self.plateau[i] = self.plateau[i], self.plateau[vide]
            
            self.actualiser_affichage()
            self.verifier_victoire()

    def nouveau_jeu(self):
        """Remet le jeu à zéro et mélange."""
        self.plateau = list(self.solution)
        self.historique = []
        # Mélange par mouvements réels pour garantir la solution
        for _ in range(100):
            vide = self.plateau.index(0)
            r, c = vide // 4, vide % 4
            voisins = []
            if r > 0: voisins.append(vide - 4) # Haut
            if r < 3: voisins.append(vide + 4) # Bas
            if c > 0: voisins.append(vide - 1) # Gauche
            if c < 3: voisins.append(vide + 1) # Droite
            
            cible = random.choice(voisins)
            self.plateau[vide], self.plateau[cible] = self.plateau[cible], self.plateau[vide]
        
        self.actualiser_affichage()

    def annuler(self):
        """Revient au coup précédent."""
        if self.historique:
            self.plateau = self.historique.pop()
            self.actualiser_affichage()

    def sauvegarder(self):
        """Enregistre la liste dans un fichier texte."""
        with open(self.fichier_save, "w") as f:
            # On transforme [1, 2...] en "1,2,..."
            txt = ",".join(map(str, self.plateau))
            f.write(txt)
        messagebox.showinfo("Sauvegarde", "Partie enregistrée !")

    def charger(self):
        """Charge la partie depuis le fichier."""
        if os.path.exists(self.fichier_save):
            with open(self.fichier_save, "r") as f:
                data = f.read().split(",")
                self.plateau = [int(x) for x in data]
            self.historique = [] # On vide l'historique après un chargement
            self.actualiser_affichage()
        else:
            messagebox.showwarning("Erreur", "Aucune sauvegarde trouvée.")

    def verifier_victoire(self):
        if self.plateau == self.solution:
            messagebox.showinfo("Gagné !", "Félicitations, vous avez résolu le taquin !")

# --- LANCEMENT ---
if __name__ == "__main__":
    fenetre = tk.Tk()
    jeu = TaquinL1(fenetre)
    fenetre.mainloop()
