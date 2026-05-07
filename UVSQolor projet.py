import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

#création de la fenetre et du canva servant d'interface 
fenetre=tk.Tk()
fenetre.title("UVSQolor, projet de manipulation d'images")
fenetre.geometry("700x550")
tableau=tk.Canvas(fenetre,width=600,height=300,bg="white")
tableau.pack()

#création du bouton pour charger l'image et celui pour le supp
cadre_boutons=tk.Frame(fenetre)
cadre_boutons.pack()

def charger_fichier():
    chemin_image=filedialog.askopenfilename(title="Choisir une image",filetypes=[("Images","*.png *.jpeg *.jpg *.bmp")])
    if chemin_image:
        global image_pil,image_tk,image_originale
        image_pil=Image.open(chemin_image)
        image_pil=image_pil.resize((600,300))
        image_tk=ImageTk.PhotoImage(image_pil)
        tableau.create_image(300,150,image=image_tk)
        image_originale=image_pil.copy()

bouton_fichier=tk.Button(cadre_boutons,text="Charger une image",bg="lightblue",font=("Times",12),command=charger_fichier)
bouton_fichier.pack(side="left")

def supprimer_fichier():
    tableau.delete("all")

bouton_supprimer=tk.Button(cadre_boutons,text="Supprimer le fichier",bg="lightblue",font=("Times",12),command=supprimer_fichier)
bouton_supprimer.pack(side="left",padx=5)

#création des boutons de manipulation d'images
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
        appliquer_flou()
    elif filtre=="MIROIR":
        appliquer_miroir()

cadre_menu=tk.Frame(fenetre)
cadre_menu.pack()
txt_longueur=tk.Label(cadre_menu,text="Choisissez le filtre sur le menu déroulant:",font=("Times",14))
txt_longueur.pack()
menu=tk.StringVar(cadre_menu)
menu.set("SEPIA")
options=["SEPIA","LUMINOSITE","CONTRASTE","FLOU","FLOU GAUSSIEN","NETTETE","FUSIONNER","MIROIR"]
menu_deroulant=tk.OptionMenu(cadre_menu,menu,*options)
menu_deroulant.pack(pady=10)
bouton_valider=tk.Button(cadre_menu,text="Valider",font=("Times",11),bg="#7B99FE",command=valider)
bouton_valider.pack(pady=10)

def enlever_filtre():
    global image_pil,image_tk,image_originale
    if image_originale:
        image_pil=image_originale.copy()
        image_tk=ImageTk.PhotoImage(image_pil)
        tableau.delete("all")
        tableau.create_image(300,150,image=image_tk)

bouton_enlever=tk.Button(cadre_menu,text="Enlever le filtre",font=("Times",11),bg="#7B99FE",command=enlever_filtre)
bouton_enlever.pack(pady=10)

def appliquer_sepia():
    global image_pil,image_tk
    if image_pil:
        matrice_sepia=(0.393,0.769,0.189,0,
                       0.49,0.686,0.168,0,
                       0.272,0.534,0.131,0)
        image_pil=image_pil.convert("RGB").convert("RGB",matrice_sepia)
        image_tk=ImageTk.PhotoImage(image_pil)
        tableau.create_image(300,150,image=image_tk)

def appliquer_lumi():
    global image_pil,image_tk
    if image_pil:
        matrice_lumi=(1.2,0,0,0,
                       0,1.2,0,0,
                       0,0,1.2,0)
        image_pil=image_pil.convert("RGB").convert("RGB",matrice_lumi)
        image_tk=ImageTk.PhotoImage(image_pil)
        tableau.create_image(300,150,image=image_tk)


def appliquer_contraste():
    global image_pil,image_tk
    if image_pil:
        matrice_contraste=(1.2,0,0,-70,
                           0,1.2,0,-70,
                           0,0,1.2,-70)
        image_pil=image_pil.convert("RGB").convert("RGB",matrice_contraste)
        image_tk=ImageTk.PhotoImage(image_pil)
        tableau.create_image(300,150,image=image_tk)

def appliquer_miroir():
    global image_pil,image_tk
    if image_pil:
        nouvelle_img=Image.new("RGB",(600,300))
        for y in range(300):
            for x in range(600):
                pixel=image_pil.getpixel((x,y))
                nouvelle_img.putpixel((599-x,y),pixel)
        image_pil=nouvelle_img
        image_tk=ImageTk.PhotoImage(image_pil)
        tableau.create_image(300,150,image=image_tk)

def appliquer_net():
    global image_pil,image_tk
    if image_pil:
        img_original=image_pil.convert("RGB")
        nouvelle_img=Image.new("RGB",(600,300))
        for y in range(1,299):
            for x in range(1,599):
                r_final=0
                g_final=0
                b_final=0
                matrice_nette=[(-1,0,(x,y-1)),  
                    (-1,0,(x-1,y)),(5,0,(x,y)),(-1,0,(x+1,y)), 
                              (-1,0,(x,y+1))]
                for poids,_,coord in matrice_nette:
                    r,g,b=img_original.getpixel(coord)
                    r_final+=r*poids
                    g_final+=g*poids
                    b_final+=b*poids
                r_final=max(0,min(255,r_final))
                g_final=max(0,min(255,g_final))
                b_final=max(0,min(255,b_final))
                nouvelle_img.putpixel((x,y),(r_final,g_final,b_final))
        image_pil=nouvelle_img
        image_tk=ImageTk.PhotoImage(image_pil)
        tableau.create_image(300,150,image=image_tk)

def appliquer_flou():
    global image_pil,image_tk
    if image_pil:
        img_original=image_pil.convert("RGB")
        nouvelle_img=Image.new("RGB",(600,300))
        for y in range(1,299):
            for x in range(1,599):
                r_final=0
                g_final=0
                b_final=0
                matrice_flou = [            (1,(x,y-1)),
                                (1,(x-1,y)),(1,(x,y)),(1,(x+1,y)),  
                                            (1,(x,y+1))]
                for poids, coord in matrice_flou:
                    r,g,b=img_original.getpixel(coord)
                    r_final+=r*poids
                    g_final+=g*poids
                    b_final+=b*poids
                r_final=r_final//5
                g_final=g_final//5
                b_final=b_final//5
                nouvelle_img.putpixel((x,y),(r_final,g_final,b_final))
        image_pil=nouvelle_img
        image_tk=ImageTk.PhotoImage(image_pil)
        tableau.create_image(300,150,image=image_tk)

def fusionner():
    global image_pil,image_tk
    if image_pil:
        chemin_image2=filedialog.askopenfilename(title="Choisir une image",filetypes=[("Images","*.png *.jpeg *.jpg")])
        if chemin_image2:
            img_1=image_pil.convert("RGB")
            img_2=Image.open(chemin_image2)
            img_2=img_2.convert("RGB")
            img_2=img_2.resize((600,300))
            img_finale=Image.new("RGB",(600,300))
            for y in range(300):
                for x in range(600):
                    r1,g1,b1=img_1.getpixel((x,y))
                    r2,g2,b2=img_2.getpixel((x,y))
                    r_final=(r1+r2)//2
                    g_final=(g1+g2)//2
                    b_final=(b1+b2)//2
                    img_finale.putpixel((x,y),(r_final,g_final,b_final))
            image_pil=img_finale
            image_tk=ImageTk.PhotoImage(image_pil)
            tableau.delete("all")
            tableau.create_image(300,150,image=image_tk)

def appliquer_gauss():
    global image_pil,image_tk
    if image_pil:
        img_original=image_pil.convert("RGB")
        nouvelle_img=Image.new("RGB",(600,300))
        for y in range(1,299):
            for x in range(1,599):
                r_final=0
                g_final=0
                b_final=0
                matrice_flou=[
                    (1,(x-1,y-1)),(2,(x,y-1)),(1,(x+1,y-1)), 
                    (2,(x-1,y)),(4,(x,y)),(2,(x+1,y)),
                    (1,(x-1,y+1)),(2,(x,y+1)),(1,(x+1,y+1)),]
                for poids, coord in matrice_flou:
                    r,g,b=img_original.getpixel(coord)
                    r_final+=r*poids
                    g_final+=g*poids
                    b_final+=b*poids
                r_final=r_final//16
                g_final=g_final//16
                b_final=b_final//16
                nouvelle_img.putpixel((x,y),(r_final,g_final,b_final))
        image_pil=nouvelle_img
        image_tk=ImageTk.PhotoImage(image_pil)
        tableau.create_image(300,150,image=image_tk)

def appliquer_inverse():
    global image_pil,image_tk
    if image_pil:
        matrice_inv=(-1,0,0,255,
                     0,-1,0,255,
                     0,0,-1,255,)
        image_pil=image_pil.convert("RGB").convert("RGB",matrice_inv)
        image_tk=ImageTk.PhotoImage(image_pil)
        tableau.create_image(300,150,image=image_tk)


def enlever_filtre():
    global image_pil,image_tk,image_originale
    if image_originale:
        image_pil=image_originale.copy()
        image_tk=ImageTk.PhotoImage(image_pil)
        tableau.delete("all")
        tableau.create_image(300,150,image=image_tk)

tableau.mainloop()