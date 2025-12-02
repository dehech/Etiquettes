import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import red, black
from tkinter import scrolledtext 

liste = [] 
text_list_display = None
index_a_modifier = None 
btn_supprimer = None 

# === DESIGN GLOBAL ===
PRIMARY = "#0078D7"      # Bleu moderne
DANGER = "#E53935"       # Rouge Supprimer
BG = "#F4F6F9"           # Arrière-plan
TEXT_BG = "#FFFFFF"
BTN_HOVER = "#005A9E"
FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")

# ------------------ FONCTIONS UTILITAIRES ------------------ #

def mettre_a_jour_affichage():
    if index_a_modifier is None:
        return
        
    if text_list_display:
        text_list_display.config(state=tk.NORMAL) 
        text_list_display.delete('1.0', tk.END) 
        
        if not liste:
             text_list_display.insert(tk.END, "Aucun article dans la liste.")
        
        for i, (ref, typ, prix, desc) in enumerate(liste):
            ligne = f"{i+1}. REF: {ref}, TYPE: {typ}, PRIX: {prix}"
            if desc:
                ligne += f", DESC: {desc.upper()}"
            ligne += "\n"
            text_list_display.insert(tk.END, ligne)
            
            if i == index_a_modifier.get():
                 start_index = f"{i+1}.0"
                 end_index = f"{i+2}.0"
                 text_list_display.tag_add("highlight", start_index, end_index)
                 
        text_list_display.config(state=tk.DISABLED) 
        text_list_display.tag_config("highlight", background="yellow", foreground="black")

def effacer_champs():
    entry_ref.delete(0, tk.END)
    entry_type.delete(0, tk.END)
    entry_prix.delete(0, tk.END)
    entry_desc.delete(0, tk.END) 

# ------------------ FONCTIONS D’ACTION ------------------ #

def ajouter():
    ref = entry_ref.get().strip().upper()
    typ = entry_type.get().strip().upper()
    prix = entry_prix.get().strip().upper()
    desc = entry_desc.get().strip() 

    if ref == "" or typ == "" or prix == "":
        messagebox.showwarning("Attention", "Remplir tous les champs obligatoires (Référence, Type, Prix) !")
        return
    
    if index_a_modifier.get() != -1:
        modifier_article()
        return

    liste.append((ref, typ, prix, desc))
    effacer_champs()
    mettre_a_jour_affichage()
    
def charger_article_pour_edition(event):
    try:
        index_str = text_list_display.index(tk.CURRENT)
        ligne_index = int(index_str.split('.')[0]) - 1 

        if 0 <= ligne_index < len(liste):
            ref, typ, prix, desc = liste[ligne_index]
            
            effacer_champs()
            entry_ref.insert(0, ref)
            entry_type.insert(0, typ)
            entry_prix.insert(0, prix)
            entry_desc.insert(0, desc) 

            index_a_modifier.set(ligne_index)
            btn_ajouter.config(text="Confirmer Modification", command=ajouter)
            
            btn_supprimer.grid(row=4, column=2, padx=5, pady=10) 
            btn_annuler.grid(row=4, column=3, padx=5, pady=10)
            
            mettre_a_jour_affichage() 
    except:
        pass 

def annuler_modification():
    index_a_modifier.set(-1)
    effacer_champs()
    
    btn_ajouter.config(text="Ajouter l'Article", command=ajouter)
    btn_supprimer.grid_forget() 
    btn_annuler.grid_forget()
    mettre_a_jour_affichage()

def modifier_article():
    idx = index_a_modifier.get()
    
    ref = entry_ref.get().strip().upper()
    typ = entry_type.get().strip().upper()
    prix = entry_prix.get().strip().upper()
    desc = entry_desc.get().strip() 
    
    if ref == "" or typ == "" or prix == "":
        messagebox.showwarning("Attention", "Remplir tous les champs obligatoires (Référence, Type, Prix) !")
        return
        
    liste[idx] = (ref, typ, prix, desc)
    messagebox.showinfo("Modification", f"Article #{idx+1} modifié avec succès.")
    annuler_modification()

def supprimer_article():
    idx = index_a_modifier.get()
    
    if idx != -1 and 0 <= idx < len(liste):
        confirmation = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer l'article #{idx+1} ({liste[idx][0]}) ?")
        if confirmation:
            del liste[idx]
            messagebox.showinfo("Suppression", "Article supprimé avec succès.")
        
        annuler_modification()
    else:
        messagebox.showwarning("Erreur", "Aucun article sélectionné pour la suppression.")
        annuler_modification()

def imprimer():
    if not liste:
        messagebox.showwarning("Aucun", "Aucune donnée à imprimer")
        return

    try:
        fichier = "liste_articles.pdf"
        c = canvas.Canvas(fichier, pagesize=A4)
        page_width, page_height = A4

        margin_left = 35
        margin_top = 40
        margin_bottom = 40
        margin_right = 35

        usable_width = page_width - margin_left - margin_right
        block_width = usable_width / 3

        block_height = 60
        v_gap = 12

        x = margin_left
        y = page_height - margin_top - block_height

        c.setFont("Helvetica", 10)
        nb_col = 0

        for ref, typ, prix, desc in liste:
            if nb_col == 3:
                nb_col = 0
                x = margin_left
                y -= (block_height + v_gap)

            if y < margin_bottom:
                c.showPage()
                c.setFont("Helvetica", 10)
                x = margin_left
                y = page_height - margin_top - block_height
                nb_col = 0

            c.setFillColor(black)
            c.drawString(x, y + block_height - 12, f"REF: {ref}")
            c.drawString(x, y + block_height - 26, f"TYPE: {typ}")

            #c.setFillColor(red)
            #c.drawString(x, y + block_height - 40, f"PRIX: {prix}")
            # Mot PRIX: en noir
            c.setFillColor(black)
            c.drawString(x, y + block_height - 40, "PRIX: ")

            # Valeur du prix en rouge (à côté)
            c.setFillColor(red)
            c.drawString(x + 35, y + block_height - 40, str(prix))


            if desc: 
                c.setFillColor(red)
                c.drawString(x, y + block_height - 54, desc.upper())

            c.setFillColor(black)
            x += block_width
            nb_col += 1

        c.save()
        messagebox.showinfo("PDF généré", f"Fichier enregistré : {fichier}")

    except Exception as e:
        messagebox.showerror("Erreur", str(e))


# ------------------ INTERFACE TKINTER ------------------ #

root = tk.Tk()
root.title("Etiquettes - Prix et Références")
root.config(bg=BG)

index_a_modifier = tk.IntVar(root) 
index_a_modifier.set(-1) 

# ---------- CADRE DE SAISIE ---------
frame = tk.Frame(root, bg=TEXT_BG, bd=2, relief=tk.GROOVE)
frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

tk.Label(frame, text="Référence :", font=FONT_BOLD, bg=TEXT_BG).grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_ref = tk.Entry(frame, width=30, font=FONT)
entry_ref.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Type :", font=FONT_BOLD, bg=TEXT_BG).grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_type = tk.Entry(frame, width=30, font=FONT)
entry_type.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Prix :", font=FONT_BOLD, bg=TEXT_BG).grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_prix = tk.Entry(frame, width=30, font=FONT)
entry_prix.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Description (opt.) :", font=FONT_BOLD, bg=TEXT_BG).grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_desc = tk.Entry(frame, width=30, font=FONT)
entry_desc.grid(row=3, column=1, padx=5, pady=5)

# ---------- Boutons ----------

btn_ajouter = tk.Button(root, text="Ajouter l'Article", command=ajouter, width=18, bg=PRIMARY, fg="white", font=FONT_BOLD)
btn_ajouter.grid(row=4, column=0, pady=10)

tk.Button(root, text="Générer PDF", command=imprimer, width=18, bg="#4CAF50", fg="white", font=FONT_BOLD).grid(row=4, column=1, pady=10)

btn_supprimer = tk.Button(root, text="Supprimer", command=supprimer_article, width=12, bg=DANGER, fg="white", font=FONT_BOLD)

btn_annuler = tk.Button(root, text="Annuler", command=annuler_modification, width=12, font=FONT_BOLD)

# ---------- LISTE AFFICHAGE ----------

tk.Label(root, text="Liste des Articles (Double-cliquer pour modifier/supprimer) :", font=FONT_BOLD, bg=BG).grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky="w")
text_list_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10, font=FONT, bg="white")
text_list_display.grid(row=6, column=0, columnspan=4, padx=10, pady=(0, 10), sticky="nsew")

text_list_display.bind("<Double-Button-1>", charger_article_pour_edition)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(6, weight=1)

text_list_display.config(state=tk.DISABLED)

root.mainloop()
