import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from scipy.signal import convolve2d

#setting des variables de départ
image_pil = None
image_tk = None
image_originale = None
matrice_pixels = None

#création de la fenetre et du canva servant d'interface 
fenetre=tk.Tk()
fenetre.title("Application de filtres | PROJET ")
fenetre.geometry("800x700")
fenetre['bg']="#FDE7EB"
tableau=tk.Canvas(fenetre,width=600,height=400,bg='#FDE7EB',highlightthickness=1, highlightbackground="gray")
tableau.pack(pady=20)

#création du bouton pour charger l'image et celui pour le supp

def rafraichir():
    global image_pil, image_tk, matrice_pixels
    image_pil = Image.fromarray(matrice_pixels.astype(np.uint8))
    image_redim = image_pil.resize((600, 400))
    image_tk = ImageTk.PhotoImage(image_redim)
    
    tableau.delete("all")
    tableau.create_image(0, 0, anchor=tk.NW, image=image_tk)
    tableau.image = image_tk #pour que tkinter continue d'afficher la photo/ image
    fenetre.update_idletasks()


cadre_boutons=tk.Frame(fenetre, bg='#FDE7EB')
cadre_boutons.pack(side="top", pady=10)

def charger_fichier(elem):
    global image_pil,image_originale,matrice_pixels
    chemin_image=filedialog.askopenfilename(title="Image à charger")
    if chemin_image:
        image_originale = Image.open(chemin_image).convert("RGB")
        image_pil = image_originale.copy()
        matrice_pixels = np.array(image_pil)
        rafraichir()

bouton_fichier=tk.Button(cadre_boutons,text="Charger une image",bg="lightblue",font=("Times",12),command=lambda:charger_fichier(fenetre))
bouton_fichier.pack(side="left", padx=10)

def supprimer_fichier():
    global image_pil,image_originale,image_tk
    tableau.delete("all")
    image_pil = None
    image_originale = None
    image_tk = None

bouton_supprimer=tk.Button(cadre_boutons,text="Supprimer le fichier",bg="lightblue",font=("Times",12),command=supprimer_fichier)
bouton_supprimer.pack(side="left",padx=10)

def enregistrer_fichier():
    global image_pil
    chemin_image=filedialog.asksaveasfilename(title="Enregistrer l'image avec le filtre", filetypes=[("Image", "*.png *.jpeg *.jpg")])
    if chemin_image:
        image_pil.save(chemin_image)
        rafraichir()

bouton_enregistrer=tk.Button(cadre_boutons, text="Enregistrer le fichier", bg="lightblue", font=("Times", 12), command= enregistrer_fichier)
bouton_enregistrer.pack(side="left", padx=10)

#création de la partie de manipulation d'images


txt_filtres=tk.Label(fenetre,text="ᗢ-----------Filtres-----------ᗢ", bg="#FDE7EB")
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
    elif filtre=="FLOU GAUSSIEN":
        appliquer_Gauss()
    elif filtre=="NETTETE":
        appliquer_nettete()
    elif filtre=="FUSIONNER":
        fusionner()
    elif filtre=="MIROIR":
        appliquer_miroir()
    elif filtre=="INVERSE":
        appliquer_inverse()
    elif filtre=="NOIR ET BLANC":
        appliquer_noirblanc()
    elif filtre=="MONTAGE WARHOL":
        appliquer_warhol()
    

cadre_menu=tk.Frame(fenetre, bg="#FDE7EB")
cadre_menu.pack(pady=5)

txt_longueur=tk.Label(cadre_menu,text="Choisissez le filtre sur le menu déroulant:",font=("Times",12), bg="#FDE7EB")
txt_longueur.pack()

menu=tk.StringVar(cadre_menu)
menu.set("SEPIA")
options=["SEPIA","LUMINOSITE","CONTRASTE","FLOU GAUSSIEN","NETTETE","FUSIONNER","MIROIR","INVERSE","NOIR ET BLANC", "MONTAGE WARHOL"]
menu_deroulant=tk.OptionMenu(cadre_menu,menu,*options)
menu_deroulant.config(width=14)
menu_deroulant.pack()

cadre_actions=tk.Frame(fenetre, bg="#FDE7EB")
cadre_actions.pack(pady=10)


bouton_valider=tk.Button(cadre_actions,text="Valider",font=("Times",11),bg="#95ACF9",command=valider, width=12)
bouton_valider.pack(side="left",padx=5)

def enlever_filtre():
    global image_pil, matrice_pixels
    if image_originale:
        image_pil = image_originale.copy()
        matrice_pixels = np.array(image_pil) 
        rafraichir()

bouton_enlever=tk.Button(cadre_actions,text="Enlever le filtre",font=("Times",11),bg="#95ACF9",command=enlever_filtre, width=12)
bouton_enlever.pack(side="left", padx=5)

#filtres

def appliquer_sepia():
    global image_pil, matrice_pixels
    matrice_pixels = np.array(image_pil).astype(float)
    r= matrice_pixels[:,:,[0]]
    v= matrice_pixels[:,:,[1]]
    b= matrice_pixels[:,:,[2]]
    r_prime= r+0.5*v+0.1*b
    v_prime= 0.5*r+0.8*v+0.1*b
    b_prime= 0.2*r+0.3*v+0.5*b
    r_prime = np.clip(r_prime, 0, 255)
    v_prime = np.clip(v_prime, 0, 255)
    b_prime = np.clip(b_prime, 0, 255)
    matrice_pixels[:,:,[0]]=r_prime
    matrice_pixels[:,:,[1]]=v_prime
    matrice_pixels[:,:,[2]]=b_prime
    image_pil = Image.fromarray(matrice_pixels.astype(np.uint8))
    rafraichir()

def appliquer_noirblanc():
    global matrice_pixels, image_pil
    matrice_pixels = np.array(image_pil)
    r= matrice_pixels[:,:,[0]]
    v= matrice_pixels[:,:,[1]]
    b= matrice_pixels[:,:,[2]]
    r_prime= 0.299*r
    v_prime= 0.587*v
    b_prime= 0.114*b
    r_prime = np.clip(r_prime, 0, 255)
    v_prime = np.clip(v_prime, 0, 255)
    b_prime = np.clip(b_prime, 0, 255)
    Y= r_prime+v_prime+b_prime
    matrice_pixels[:,:,[0,1,2]]=Y
    image_pil=Image.fromarray(matrice_pixels.astype(np.uint8))
    rafraichir()

def appliquer_warhol():
    global matrice_pixels, image_pil
    h, w, c = matrice_pixels.shape # recup les 3 canaux
    matrice_pixels=np.array(image_pil).astype(float)
    image_1 = matrice_pixels.copy()
    image_2 = matrice_pixels.copy()
    image_3 = matrice_pixels.copy()
    image_4 = matrice_pixels.copy()

    image_1[:,:,0] *=1.2
    image_1[:,:,1] *=0.9
    image_1[:,:,2] *=0.4

    image_2[:,:,0] *=0.2
    image_2[:,:,1] *=1.1
    image_2[:,:,2] *=0.4

    image_3[:,:,0] *=0.74
    image_3[:,:,1] *=0.543
    image_3[:,:,2] *=1.34

    image_4[:,:,0] *=1.13
    image_4[:,:,1] *=0.129
    image_4[:,:,2] *=1.13

    image_1 = np.clip(image_1, 0, 255).astype(np.uint8)
    image_2 = np.clip(image_2, 0, 255).astype(np.uint8)
    image_3 = np.clip(image_3, 0, 255).astype(np.uint8)
    image_4 = np.clip(image_4, 0, 255).astype(np.uint8)

    #matrice finale qui fait 2 fois la taille initialle pour faire rentrer les 4 images
    matrice_finale=np.zeros((h*2,w*2,c), dtype=np.uint8)

    matrice_finale[0:h, 0:w]=image_1
    matrice_finale[h:h*2, 0:w]=image_2
    matrice_finale[0:h, w:w*2]=image_3
    matrice_finale[h:h*2, w:w*2]=image_4

    matrice_pixels = matrice_finale

    image_pil=Image.fromarray(matrice_pixels)
    rafraichir()
    

def appliquer_lumi():
    global matrice_pixels, image_pil
    matrice_pixels = np.array(image_pil).astype(float)
    r= matrice_pixels[:,:,[0]]
    v= matrice_pixels[:,:,[1]]
    b= matrice_pixels[:,:,[2]]
    r_prime= r+50
    v_prime= v+50
    b_prime= b+50
    r_prime = np.clip(r_prime, 0, 255)
    v_prime = np.clip(v_prime, 0, 255)
    b_prime = np.clip(b_prime, 0, 255)
    matrice_pixels[:,:,[0]]=r_prime
    matrice_pixels[:,:,[1]]=v_prime
    matrice_pixels[:,:,[2]]=b_prime
    image_pil = Image.fromarray(matrice_pixels.astype(np.uint8))
    rafraichir()


def appliquer_contraste(): #soit se rapproche de effet poussière ou effet très lumineux selon valeur_contraste
    global matrice_pixels, image_pil
    matrice_pixels=np.array(image_pil).astype(float)
    valeur_contraste=1.5
    r=matrice_pixels[:,:,[0]]
    v=matrice_pixels[:,:,[1]]
    b=matrice_pixels[:,:,[2]]
    r_prime= (r-128)*valeur_contraste+128
    v_prime= (v-128)*valeur_contraste+128
    b_prime= (b-128)*valeur_contraste+128
    r_prime = np.clip(r_prime, 0, 255)
    v_prime = np.clip(v_prime, 0, 255)
    b_prime = np.clip(b_prime, 0, 255)
    matrice_pixels[:,:,[0]]=r_prime
    matrice_pixels[:,:,[1]]=v_prime
    matrice_pixels[:,:,[2]]=b_prime
    image_pil = Image.fromarray(matrice_pixels.astype(np.uint8))
    rafraichir()

def appliquer_miroir():
    global image_pil
    global matrice_pixels
    matrice_pixels = np.array(image_pil)
    matrice_pixels= matrice_pixels[:,::-1,:] #inverse les colonnes avec le slicing
    image_pil = Image.fromarray(matrice_pixels.astype(np.uint8))
    rafraichir()
    


noyau_nettete= np.array([
    [0,-1,0],
    [-1,5,-1],
    [0,-1,0]
    ])

def appliquer_nettete(): #principe de convolution mais avec un noyau avec des chiffres négatifs et positifs pour accentuer les différnces de lignes au lieu de lisser l'image et l'objet comme pour flou
    global matrice_pixels, image_pil, noyau_nettete
    float_matrice=np.array(image_pil).astype(float)
    new_matrice = np.zeros_like(float_matrice)
    for i  in range (3): #convolution sur les 3 canaux; boundary = symm => évite bords noirs
        new_matrice[:,:,i] = convolve2d(float_matrice[:,:,i],noyau_nettete, mode="same",boundary="symm")
    matrice_pixels=np.clip(new_matrice, 0, 255).astype(np.uint8)
    image_pil = Image.fromarray(matrice_pixels.astype(np.uint8)) #si on charge un nouveau filtre après, l'image sera MAJ et on appliquera pas le deuxieme filtre sur le flou
    rafraichir()

noyau_gauss = np.array([
    [1,  4,  6,  4, 1],
    [4, 16, 24, 16, 4],
    [6, 24, 36, 24, 6],
    [4, 16, 24, 16, 4],
    [1,  4,  6,  4, 1]
    ]) / 256


def appliquer_Gauss():
    global matrice_pixels, image_pil, noyau_gauss
    #matrice du même type en float pour ne pas avoir d'arrondis et de la même taille que matrice_pixels
    float_matrice=np.array(image_pil).astype(float)
    new_matrice = np.zeros_like(float_matrice)
    for i  in range (3): #convolution sur les 3 canaux; boundary = symm => évite bords noirs
        new_matrice[:,:,i] = convolve2d(float_matrice[:,:,i],noyau_gauss, mode="same",boundary="symm")
    matrice_pixels=np.clip(new_matrice, 0, 255).astype(np.uint8)
    image_pil = Image.fromarray(matrice_pixels)
    rafraichir()

def appliquer_inverse(): #prend un pixel et donne sont inverse sur le spectre 
    global matrice_pixels, image_pil
    matrice_pixels = np.array(image_pil).astype(float)
    r= matrice_pixels[:,:,[0]]
    v= matrice_pixels[:,:,[1]]
    b= matrice_pixels[:,:,[2]]
    r_prime= 255-r
    v_prime= 255-v
    b_prime= 255-b
    r_prime = np.clip(r_prime, 0, 255)
    v_prime = np.clip(v_prime, 0, 255)
    b_prime = np.clip(b_prime, 0, 255)
    matrice_pixels[:,:,[0]]=r_prime
    matrice_pixels[:,:,[1]]=v_prime
    matrice_pixels[:,:,[2]]=b_prime
    image_pil=Image.fromarray(matrice_pixels.astype(np.uint8))
    rafraichir()

def fusionner():
    global image_pil, matrice_pixels
    if image_pil is not None:
        # Ajout de filetypes pour éviter les erreurs de sélection
        chemin2 = filedialog.askopenfilename(
            title="Image à fusionner",
            filetypes=[("Images", "*.png *.jpg *.jpeg")]
        )
        if chemin2:
            h, w, c = matrice_pixels.shape
            img2 = Image.open(chemin2).convert("RGB").resize((w, h))
            matrice1 = matrice_pixels.astype(float)
            matrice2 = np.array(img2).astype(float)
            # On s'assure que le résultat reste entre 0 et 255
            fusion = np.clip((matrice1 + matrice2) / 2, 0, 255)
            matrice_pixels = fusion.astype(np.uint8)
            rafraichir()


fenetre.mainloop()


