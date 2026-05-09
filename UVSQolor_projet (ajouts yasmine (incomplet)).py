import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

#setting des variables de départ
image_pil = None
image_tk = None
image_originale = None
matrice_pixels = None
historique=[]
indice_historique = -1

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
    global image_pil,image_originale,historique,indice_historique
    chemin_image=filedialog.askopenfilename(title="Image à charger")
    if chemin_image:
        image_pil = Image.open(chemin_image).convert("RGB")
        image_pil = image_pil.resize((600,300))
        image_originale = image_pil.copy()
        historique = []
        indice_historique = -1
        sauvegarder_etat()
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

txt_filtres=tk.Label(fenetre,text="ᗢ-----------Filtres-----------ᗢ")
txt_filtres.pack()

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
    elif filtre=="NOIR ET BLANC":
        appliquer_noir_et_blanc()

def enlever_filtre():
    global image_pil
    if image_originale:
        image_pil = image_originale.copy()
        rafraichir()

cadre_menu=tk.Frame(fenetre)
cadre_menu.pack()

txt_longueur=tk.Label(cadre_menu,text="Choisissez le filtre sur le menu déroulant:",font=("Times",14))
txt_longueur.pack()

menu=tk.StringVar(cadre_menu)
menu.set("SEPIA")
options=["SEPIA","LUMINOSITE","CONTRASTE","FLOU","FLOU GAUSSIEN","NETTETE","FUSIONNER","MIROIR","INVERSE","NOIR ET BLANC"]
menu_deroulant=tk.OptionMenu(cadre_menu,menu,*options)
menu_deroulant.pack(pady=10)

bouton_valider=tk.Button(cadre_menu,text="Valider",font=("Times",11),bg="#7B99FE",command=valider)
bouton_valider.pack(pady=10)

bouton_enlever=tk.Button(cadre_menu,text="Enlever le filtre",font=("Times",11),bg="#7B99FE",command=enlever_filtre)
bouton_enlever.pack(pady=10)

# création du menu pour retirer ou remettre le filtre 

def sauvegarder_etat():
    global historique,indice_historique,image_pil
    if image_pil is None:
        return
    image_numpy = np.array(image_pil)
    if len(historique) - 1>indice_historique:
        historique = historique[:indice_historique+1]
    historique.append(image_numpy.copy())
    indice_historique = len(historique)-1

def annuler_filtre():
    global indice_historique,historique,image_pil
    if indice_historique>0:
        indice_historique-=1
        image_numpy = historique[indice_historique].copy()
        image_pil = Image.fromarray(image_numpy.astype(np.uint8))
        rafraichir()

def retablir_filtre():
    global indice_historique,historique,image_pil
    if indice_historique<len(historique)-1:
        indice_historique+=1
        image_numpy = historique[indice_historique].copy()
        image_pil = Image.fromarray(image_numpy.astype(np.uint8))
        rafraichir()

barre_menu=tk.Menu(cadre_menu, bg="#F4EDE0", tearoff=0)
menu_fichier= tk.Menu(barre_menu, tearoff=0)
menu_fichier.add_command(label="Annuler le filtre", command=annuler_filtre)
menu_fichier.add_command(label="Rétablir le filtre", command=retablir_filtre)
barre_menu.add_cascade(label=" Fichier", menu=menu_fichier) 
fenetre.config(menu=barre_menu)

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
    sauvegarder_etat()
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
        sauvegarder_etat()
        rafraichir()

def appliquer_contraste():
    global image_pil
    if image_pil:
        matrice_contraste = (1.2,0,0,-70,
                             0,1.2,0,-70,
                             0,0,1.2,-70)
        image_pil = image_pil.convert("RGB",matrice_contraste)
        sauvegarder_etat()
        rafraichir()

def appliquer_miroir():
    global image_pil
    if image_pil:
        image_numpy = np.array(image_pil)
        image_numpy = image_numpy[:,::-1] 
        image_pil = Image.fromarray(image_numpy)
        sauvegarder_etat()
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
            sauvegarder_etat()
            rafraichir()

def appliquer_gauss():
    "dépose ton programme Yasmine"

def appliquer_inverse():
    global image_pil
    if image_pil:
        image_numpy = np.array(image_pil) 
        image_numpy = 255-image_numpy
        image_pil = Image.fromarray(image_numpy.astype(np.uint8))
        sauvegarder_etat()
        rafraichir()

def appliquer_noir_et_blanc():
    global image_pil
    if image_pil:
        image_numpy = np.array(image_pil).astype(float)
        r = image_numpy[:,:,[0]]
        v = image_numpy[:,:,[1]]
        b = image_numpy[:,:,[2]]
        r_prime = 0.299*r
        v_prime = 0.587*v
        b_prime = 0.114*b
        r_prime = np.clip(r_prime,0,255)
        v_prime = np.clip(v_prime,0,255)
        b_prime = np.clip(b_prime,0,255)
        Y = r_prime + v_prime + b_prime
        image_numpy[:,:,[0,1,2]] = Y
        image_pil = Image.fromarray(image_numpy.astype(np.uint8))
        sauvegarder_etat()
        rafraichir()

#yasmine ajoute tous tes filtres et n'oublie pas de les incrémenter au menu déroulant

tableau.mainloop()