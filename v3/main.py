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
btn_remise_zero = None

# === DESIGN GLOBAL ===
PRIMARY = "#0078D7"
DANGER = "#E53935"
BG = "#F4F6F9"
TEXT_BG = "#FFFFFF"

FONT = ("Segoe UI", 11)
FONT_BOLD = ("Segoe UI", 11, "bold")

# ------------------ FONCTIONS UTILITAIRES ------------------ #

def mettre_a_jour_affichage():
    if text_list_display:
        text_list_display.config(state=tk.NORMAL)
        text_list_display.delete('1.0', tk.END)

        if not liste:
            text_list_display.insert(tk.END, "Aucun article dans la liste.")
        else:
            for i, (ref, typ, prix, desc) in enumerate(liste):
                ligne = f"{i+1}. REF: {ref}, TYPE: {typ}, PRIX TTC: {prix}"
                if desc:
                    ligne += f", DESC: {desc.upper()}"
                ligne += "\n"
                text_list_display.insert(tk.END, ligne)

        text_list_display.config(state=tk.DISABLED)

def effacer_champs():
    entry_ref.delete(0, tk.END)
    entry_type.delete(0, tk.END)
    entry_prix.delete(0, tk.END)
    entry_desc.delete(0, tk.END)

# ------------------ ACTIONS ------------------ #

def ajouter():
    ref = entry_ref.get().strip().upper()
    typ = entry_type.get().strip().upper()
    prix = entry_prix.get().strip()
    desc = entry_desc.get().strip()

    if ref == "" or typ == "" or prix == "":
        messagebox.showwarning("Attention", "Remplir tous les champs obligatoires !")
        return

    # MODE MODIFICATION
    if index_a_modifier.get() != -1:
        liste[index_a_modifier.get()] = (ref, typ, prix, desc)
        annuler_modification()
        return

    liste.append((ref, typ, prix, desc))
    effacer_champs()
    mettre_a_jour_affichage()

def charger_article_pour_edition(event):
    global btn_remise_zero
    try:
        index = int(text_list_display.index(tk.CURRENT).split('.')[0]) - 1
        ref, typ, prix, desc = liste[index]

        effacer_champs()
        entry_ref.insert(0, ref)
        entry_type.insert(0, typ)
        entry_prix.insert(0, prix)
        entry_desc.insert(0, desc)

        index_a_modifier.set(index)
        btn_ajouter.config(text="Confirmer Modification")

        btn_supprimer.grid(row=4, column=2, padx=5)
        btn_annuler.grid(row=4, column=3, padx=5)

        # 🔴 CACHER remise à zéro
        btn_remise_zero.grid_forget()

    except:
        pass

def annuler_modification():
    index_a_modifier.set(-1)
    effacer_champs()
    btn_ajouter.config(text="Ajouter l'Article")

    btn_supprimer.grid_forget()
    btn_annuler.grid_forget()

    # 🟢 RÉAFFICHER remise à zéro
    btn_remise_zero.grid(row=4, column=2, padx=5)

    mettre_a_jour_affichage()

def supprimer_article():
    idx = index_a_modifier.get()
    if idx != -1 and messagebox.askyesno("Confirmation", "Supprimer cet article ?"):
        del liste[idx]
        annuler_modification()

def remise_a_zero():
    if not liste:
        messagebox.showinfo("Info", "La liste est déjà vide.")
        return
    if messagebox.askyesno("Confirmation", "Tout supprimer ?"):
        liste.clear()
        annuler_modification()

# ------------------ PDF ------------------ #

def imprimer():
    if not liste:
        messagebox.showwarning("Aucun", "Aucune donnée à imprimer")
        return

    fichier = "liste_articles.pdf"
    c = canvas.Canvas(fichier, pagesize=A4)
    page_width, page_height = A4

    margin_left = 35
    margin_top = 40
    margin_bottom = 40
    margin_right = 35

    usable_width = page_width - margin_left - margin_right
    block_width = usable_width / 3

    block_height = 65 
    v_gap = 12

    x = margin_left
    y = page_height - margin_top - block_height

    # 🔹 TAILLE DE POLICE (modifiable librement)
    FONT_SIZE = font_size_var.get()
    c.setFont("Helvetica-Bold", FONT_SIZE)

    nb_col = 0

    for ref, typ, prix, desc in liste:
        if nb_col == 3:
            nb_col = 0
            x = margin_left
            y -= (block_height + v_gap)

        if y < margin_bottom:
            c.showPage()
            c.setFont("Helvetica-Bold", FONT_SIZE)
            x = margin_left
            y = page_height - margin_top - block_height
            nb_col = 0

        c.setFillColor(black)
        c.drawString(x, y + block_height - 14, f"REF: {ref}")
        c.drawString(x, y + block_height - 30, f"TYPE: {typ}")

        # 🔹 PRIX TTC AVEC ESPACEMENT DYNAMIQUE
        label = "PRIX TTC: "
        label_width = c.stringWidth(label, "Helvetica-Bold", FONT_SIZE)

        c.setFillColor(black)
        c.drawString(x, y + block_height - 46, label)

        c.setFillColor(red)
        c.drawString(x + label_width + 4, y + block_height - 46, str(prix))

        if desc:
            c.setFillColor(red)
            c.drawString(x, y + block_height - 60, desc.upper())

        x += block_width
        nb_col += 1

    c.save()
    messagebox.showinfo("PDF généré", f"Fichier enregistré : {fichier}")


# ------------------ INTERFACE ------------------ #

root = tk.Tk()
root.title("Etiquettes - COCOMACO")
root.config(bg=BG)

index_a_modifier = tk.IntVar(value=-1)
font_size_var = tk.IntVar(value=14)  # Taille par défaut du PDF


frame = tk.Frame(root, bg=TEXT_BG, bd=2, relief=tk.GROOVE)
frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

tk.Label(frame, text="Référence :", font=FONT_BOLD, bg=TEXT_BG).grid(row=0, column=0)
entry_ref = tk.Entry(frame, font=FONT, width=30)
entry_ref.grid(row=0, column=1)

tk.Label(frame, text="Type :", font=FONT_BOLD, bg=TEXT_BG).grid(row=1, column=0)
entry_type = tk.Entry(frame, font=FONT, width=30)
entry_type.grid(row=1, column=1)

tk.Label(frame, text="Prix TTC :", font=FONT_BOLD, bg=TEXT_BG).grid(row=2, column=0)
entry_prix = tk.Entry(frame, font=FONT, width=30)
entry_prix.grid(row=2, column=1)

tk.Label(frame, text="Description :", font=FONT_BOLD, bg=TEXT_BG).grid(row=3, column=0)
entry_desc = tk.Entry(frame, font=FONT, width=30)
entry_desc.grid(row=3, column=1)

tk.Label(frame, text="Taille écriture PDF :", font=FONT_BOLD, bg=TEXT_BG).grid(row=4, column=0, pady=5)

spin_font_size = tk.Spinbox(
    frame,
    from_=8,
    to=20,
    textvariable=font_size_var,
    width=5,
    font=FONT
)
spin_font_size.grid(row=4, column=1, sticky="w", pady=5)


btn_ajouter = tk.Button(root, text="Ajouter l'Article", command=ajouter, bg=PRIMARY, fg="white", font=FONT_BOLD)
btn_ajouter.grid(row=4, column=0, pady=10)

tk.Button(root, text="Générer PDF", command=imprimer, bg="#4CAF50", fg="white", font=FONT_BOLD).grid(row=4, column=1)

btn_remise_zero = tk.Button(root, text="Remise à zéro", command=remise_a_zero, bg="#9E9E9E", fg="white", font=FONT_BOLD)
btn_remise_zero.grid(row=4, column=2, pady=10)

btn_supprimer = tk.Button(root, text="Supprimer", command=supprimer_article, bg=DANGER, fg="white", font=FONT_BOLD)
btn_annuler = tk.Button(root, text="Annuler", command=annuler_modification, font=FONT_BOLD)

text_list_display = scrolledtext.ScrolledText(root, width=60, height=10, font=FONT)
text_list_display.grid(row=6, column=0, columnspan=4, padx=10, pady=10)
text_list_display.bind("<Double-Button-1>", charger_article_pour_edition)
text_list_display.config(state=tk.DISABLED)

root.mainloop()
