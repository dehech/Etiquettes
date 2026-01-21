# 🏷️ Gestion des Étiquettes – COCOMACO

Application desktop développée en **Python (Tkinter)** permettant de gérer des articles, de générer des **étiquettes PDF**, et d’importer des articles depuis des fichiers PDF existants.

Cette application est destinée à un usage interne pour faciliter la gestion et l’impression d’étiquettes produits.

---

## 📌 Fonctionnalités principales

- ➕ Ajout d’articles (Référence, Type, Prix TTC, Description)
- ✏️ Modification d’articles existants
- ❌ Suppression d’articles
- 🔄 Remise à zéro complète de la liste
- 🧾 Génération automatique de PDF d’étiquettes
- 📥 Importation des articles depuis un PDF
- 🔠 Choix dynamique de la taille de la police du PDF
- 🖥️ Interface graphique simple, moderne et intuitive

---

## ▶️ Lancement de l’application

### 🔹 Lancement via l’exécutable (recommandé)

1. Accéder au dossier :
   dist/
2. Lancer le fichier :
   Etiquettes.exe

Aucune installation de Python n’est nécessaire.  
L’application est prête à l’emploi sous Windows.

---

### 🔹 Lancement via le code source

#### Prérequis
- Python 3.8 ou supérieur

#### Installation des dépendances
pip install reportlab pdfplumber

#### Lancement
python main.py

---

## 🖼️ Présentation de l’interface

L’interface se compose de trois parties principales :

### 1) Formulaire de saisie
- Référence
- Type
- Prix TTC
- Description (optionnelle)
- Taille de police du PDF

### 2) Boutons d’actions
- Ajouter l’article
- Générer PDF
- Importer PDF
- Remise à zéro
- Supprimer / Annuler (en mode modification)

### 3) Liste des articles
- Affichage de tous les articles
- Double-clic pour modifier un article

---

## ➕ Ajout d’un article

1. Remplir les champs obligatoires :
   - Référence
   - Type
   - Prix TTC
2. Ajouter une description si nécessaire
3. Cliquer sur « Ajouter »

L’article apparaît immédiatement dans la liste.

---

## ✏️ Modification d’un article

1. Double-cliquer sur un article dans la liste
2. Les champs sont chargés automatiquement
3. Modifier les informations
4. Cliquer sur « Confirmer Modification »

Options disponibles :
- Supprimer l’article
- Annuler la modification

---

## ❌ Suppression d’un article

- Possible uniquement en mode modification
- Une confirmation est demandée avant la suppression

---

## 🔄 Remise à zéro

- Supprime tous les articles de la liste
- Une confirmation est demandée

Attention : cette action est irréversible.

---

## 🧾 Génération du PDF

- Cliquer sur « Générer PDF »
- Le PDF est généré au format A4
- Disposition : 3 étiquettes par ligne

Chaque étiquette contient :
- REF
- TYPE
- PRIX TTC (en rouge)
- DESCRIPTION (si présente, en rouge)

Nom du fichier généré :
liste_articles.pdf

La taille de la police est configurable avant la génération.

---

## 📥 Importation d’un PDF

- Cliquer sur « Importer PDF »
- Sélectionner un fichier PDF

Conditions :
- Le PDF doit être généré par l’application
- Champs reconnus :
  - Référence
  - Type
  - Prix TTC
  - Description (si existante)

Les PDF externes ou non conformes peuvent ne pas être reconnus correctement.

---

## 📂 Structure du projet

project/
├── main.py
├── dist/
│   └── Etiquettes.exe
├── liste_articles.pdf
└── README.md

---

## ⚠️ Limitations connues

- Les données sont stockées uniquement en mémoire
- Pas de sauvegarde automatique
- Import PDF dépend du format généré par l’application
- Application prévue principalement pour Windows

---

## 👤 Auteur

Mohamed Firas Dehech 
Ingénieur en systèmes informatiques  
Spécialisation : Cloud Computing & Virtualisation  
Email: [firas.dehech@gmail.com]
GitHub: https://github.com/dehech

Projet développé pour COCOMACO

---

## 📄 Licence

Vous êtes libre de l'utiliser, de le modifier et de le distribuer en mentionnant correctement la source.


---

## 📬 Support

Pour toute question, amélioration ou problème technique :
- Contacter l’auteur du projet : [firas.dehech@gmail.com]

