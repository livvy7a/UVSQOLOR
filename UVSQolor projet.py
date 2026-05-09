import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

#setting des variables de départ
image_pil = None
image_tk = None
image_originale = None
matrice_pixels = None

#création de la fenetre et du canva servant d'interface 
fenetre=tk.Tk()
fenetre.title("UVSQolor, projet de manipulation d'images")
fenetre.geometry("700x550")
tableau=tk.Canvas(fenetre,width=600,height=300,bg="white")
tableau.pack()

#création du bouton pour charger l'image et celui pour le supp

def rafraichir():
    global image_tk
    if image_pil:
        image_tk = ImageTk.PhotoImage(image_pil)
        tableau.delete("all")
        tableau.config(width=600, height=300)
        tableau.create_image(0,0,anchor=tk.NW,image=image_tk)
cadre_boutons=tk.Frame(fenetre)
cadre_boutons.pack()

def charger_fichier():
    global image_pil,image_originale,matrice_pixels
    chemin_image=filedialog.askopenfilename(title="Image à charger")
    if chemin_image:
        image_pil = Image.open(chemin_image).convert("RGB")
        image_pil = image_pil.resize((600,300))
        image_originale = image_pil.copy()
        matrice_pixels = np.array(image_pil)
        rafraichir()

bouton_fichier=tk.Button(cadre_boutons,text="Charger une image",bg="lightblue",font=("Times",12),command=charger_fichier)
bouton_fichier.pack(side="left")

def supprimer_fichier():
    global image_pil,image_originale,image_tk
    tableau.delete("all")
    image_pil = None
    image_originale = None
    image_tk = None

bouton_supprimer=tk.Button(cadre_boutons,text="Supprimer le fichier",bg="lightblue",font=("Times",12),command=supprimer_fichier)
bouton_supprimer.pack(side="left",padx=5)

#création de la partie de manipulation d'images

#yasmine fais les boutons pour enlever le filtre precedent et le remettre que tu vas mettre dans "cadre_boutons"

txt_filtres=tk.Label(fenetre,text="ᗢ-----------Filtres-----------ᗢ")
txt_filtres.pack()

cadre_filtres=tk.Frame(fenetre)
cadre_filtres.pack()

def valider(): 
    filtre=menu.get()
    if filtre=="SEPIA":
        appliquer_sepia()
    elif filtre=="LUMINOSITE":
        appliquer_lumi()
    elif filtre=="CONTRASTE":
        appliquer_contraste()
    elif filtre=="FLOU":
        appliquer_flou()
    elif filtre=="FLOU GAUSSIEN":
        appliquer_gauss()
    elif filtre=="NETTETE":
        appliquer_net()
    elif filtre=="FUSIONNER":
        fusionner()
    elif filtre=="MIROIR":
        appliquer_miroir()
    elif filtre=="INVERSE":
        appliquer_inverse()

cadre_menu=tk.Frame(fenetre)
cadre_menu.pack()

txt_longueur=tk.Label(cadre_menu,text="Choisissez le filtre sur le menu déroulant:",font=("Times",14))
txt_longueur.pack()

menu=tk.StringVar(cadre_menu)
menu.set("SEPIA")
options=["SEPIA","LUMINOSITE","CONTRASTE","FLOU","FLOU GAUSSIEN","NETTETE","FUSIONNER","MIROIR","INVERSE"]
menu_deroulant=tk.OptionMenu(cadre_menu,menu,*options)
menu_deroulant.pack(pady=10)

bouton_valider=tk.Button(cadre_menu,text="Valider",font=("Times",11),bg="#7B99FE",command=valider)
bouton_valider.pack(pady=10)

def enlever_filtre():
    global image_pil
    if image_originale:
        image_pil = image_originale.copy()
        rafraichir()

bouton_enlever=tk.Button(cadre_menu,text="Enlever le filtre",font=("Times",11),bg="#7B99FE",command=enlever_filtre)
bouton_enlever.pack(pady=10)

#filtres

def appliquer_sepia():
    global image_pil
    image_numpy = np.array(image_pil).astype(float)
    r = image_numpy[:,:,[0]]
    v = image_numpy[:,:,[1]]
    b = image_numpy[:,:,[2]]
    r_prime= r+0.5*v+0.1*b
    v_prime = 0.5*r+0.8*v+0.1*b
    b_prime= 0.2*r+0.3*v+0.5*b
    r_prime = np.clip(r_prime, 0, 255)
    v_prime = np.clip(v_prime, 0, 255)
    b_prime = np.clip(b_prime, 0, 255)
    image_numpy[:,:,[0]]= r_prime
    image_numpy[:,:,[1]]= v_prime
    image_numpy[:,:,[2]]= b_prime
    image_numpy = image_numpy.astype(np.uint8)
    image_pil = Image.fromarray(image_numpy)
    rafraichir()

def appliquer_lumi():
    global image_pil
    if image_pil:
        image_numpy = np.array(image_pil).astype(float)
        r = image_numpy[:,:,0]*1.2
        v = image_numpy[:,:,1]*1.2
        b = image_numpy[:,:,2]*1.2
        r = np.clip(r,0,255)
        v = np.clip(v,0,255)
        b = np.clip(b,0,255)
        image_numpy = np.dstack((r,v,b))   
        image_numpy = image_numpy.astype(np.uint8)
        image_pil = Image.fromarray(image_numpy)
        rafraichir()

def appliquer_contraste():
    global image_pil
    if image_pil:
        matrice_contraste = (1.2,0,0,-70,
                             0,1.2,0,-70,
                             0,0,1.2,-70)
        image_pil = image_pil.convert("RGB",matrice_contraste)
        rafraichir()

def appliquer_miroir():
    global image_pil
    if image_pil:
        image_numpy = np.array(image_pil)
        image_numpy = image_numpy[:,::-1] 
        image_pil = Image.fromarray(image_numpy)
        rafraichir()

def appliquer_net():
    "dépose ton programme Yasmine"

def appliquer_flou():
    "dépose ton programme Yasmine"

def fusionner():
    global image_pil
    if image_pil:
        chemin2 = filedialog.askopenfilename(title="Image à fusionner")
        if chemin2:
            img2 = Image.open(chemin2).convert("RGB").resize((600, 300))
            matrice1 = np.array(image_pil).astype(float)
            matrice2 = np.array(img2).astype(float)
            fusion = (matrice1 + matrice2) / 2
            image_pil = Image.fromarray(np.uint8(fusion))
            rafraichir()

def appliquer_gauss():
    "dépose ton programme Yasmine"

def appliquer_inverse():
    global image_pil
    if image_pil:
        image_numpy = np.array(image_pil) 
        image_numpy = 255-image_numpy
        image_pil = Image.fromarray(image_numpy.astype(np.uint8))
        rafraichir()

#yasmine ajoute tous tes filtres et n'oublie pas de les incrémenter au menu déroulant

tableau.mainloop()