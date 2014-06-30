from tkinter import *
from tkinter.filedialog import *

#classe des coordonnees
class Coord:
    def __init__(self):
        self.x = 0
        self.y = 0


#construction la classe de l'arbre
class Arbre:
    def __init__(self):
        self.val = 0
        self.gche = None
        self.drte = None
        self.coordG = Coord()
        self.coordD = Coord()
    
    def __len__(self):
        return len(self.gche) + len(self.drte)
    

#donner le total des poids de l'arbre
    def poidValeur(self):
        return self.gche.poidValeur() + self.drte.poidValeur()

    def poidMax(self):
        pg = self.gche.poidMax()
        pd = self.drte.poidMax()
        if pg < pd:
            return pd
        else:
            return pg

    def poidMin(self):
        pg = self.gche.poidMin()
        pd = self.drte.poidMin()
        if pg > pd:
            return pd
        else:
            return pg


#calcule la coordonnee du fil gauche et droite
    def calculCoord(self):
        larg = self.largeurNoeud()/2
        self.coordG.x = -larg * self.val
        self.coordG.y = 0
        self.coordD.x = self.coordG.x + larg
        self.coordD.y = 0
        if type (self.gche)!= Poid:
            self.gche.calculCoord()
        if type(self.drte) != Poid:
            self.drte.calculCoord()


#calcule largeur des noeuds et des sous arbres
    def largeurNoeud(self):
        gauche = 0
        droite = 0
        if type(self.gche) ==  Poid:
            gauche = self.gche.val
        else:
            gauche = self.gche.largeurNoeud()
        if type(self.drte) == Poid:
            droite = self.drte.val
        else:
            droite = self.drte.largeurNoeud()
        return droite + gauche

#calcule la valeur (pdroite/(pgauche+pdroite)) pour calcule la coordonnee du fil gauche
    def proportion(self):
        if type(self.gche) == Arbre:
            self.gche.proportion()
        if type(self.drte) == Arbre:
            self.drte.proportion()
        self.val = self.drte.poidValeur() / (self.gche.poidValeur() + self.drte.poidValeur())


#calcule largeur de l'arbre pour le canvas en soustraction la maximum coordonnee(x) du droite a celle du gauche
    def largeurArbre(self):
        g = self.gche.largeurArbreGche() + self.coordG.x
        d = self.drte.largeurArbreDrte() + self.coordD.x
        return d - g

    def largeurArbreGche(self):
        return self.coordG.x + self.gche.largeurArbreGche()

    def largeurArbreDrte(self):
        return self.coordD.x + self.drte.largeurArbreDrte()


#calcule hauteur de l'arbre pour le canvas en prenant le diametre du plus grand poid le longueur du fil(jusqu'a le centre du cercle)
    def hauteurArbre(self):
        haut = self.poidMax()
        return self.hauteurArbreBis(haut)
    
    def hauteurArbreBis(self, h):
        g = self.coordG.y + self.gche.hauteurArbreBis(h)
        d = self.coordD.y + self.drte.hauteurArbreBis(h)
        return h + max(d,g)
    

#return la liste des poids
    def renduListe(self):
        list = self.gche.renduListe()
        list.extend(self.drte.renduListe())
        return list

#return la liste en forme arbre
    def renduArbre(self):
        list = []
        if type(self.gche) == Poid:
            list.extend([self.gche.val])
        else:
            list.append(self.gche.renduArbre())
        if type(self.drte) == Poid:
            list.extend([self.drte.val])
        else:
            list.append(self.drte.renduArbre())
        return list



#construction la classe des poids, heritage de la classe Arbre
class Poid(Arbre):
    def __init__(self, valeur):
        self.val = valeur
        self.coord = Coord()

    def __str__(self):
        return str(self.val)
    
    def __len__(self):
        return 1

    def poidValeur(self):
        return self.val

    def renduListe(self):
        return [self.val]
    
    def renduArbre(self):
        return [self.val]

    def poidMax(self):
        return self.val
    
    def poidMin(self):
        return self.val

    def largeurArbreGche(self):
        return -self.val/2

    def largeurArbreDrte(self):
        return self.val/2

    def hauteurArbre(self):
        haut = self.val()
        return self.hauteurArbreBis(haut)
    
    

#on compte la longueur du fil jusqu'a le centre du cercle, donc il faut juste ajouter le rayon du cercle, dont valeur/2
    def hauteurArbreBis(self, h):
        return h + self.val/2



#fonction qui ouvre le fichier txt des poids, rend la liste des poids et construire le mobile(2 differences methodes selon la liste donnee)
def importlist():
    global mobile
    ouv = askopenfilename(filetypes=[("Tout",".*"),("Selection du fichier des poids","*.txt")])
    fic = open(ouv,"r")
    contenu = fic.readlines()
    fic.close()
    if len(contenu) == 0:
        print("Fichier vide")
    elif len(contenu) == 1:
        l = eval(contenu[0])
        mobile = consArbre(l)
    elif len(contenu) > 1:
        l = list()
        for i in contenu:
            n = i[:-1]
            if len(n) > 0:
                l.append(int(n))
        mobile = consDecroissant(l)
    lancerMobile()



#construction le mobile a partir d'une liste reconnaissant un arbre
def consArbre(l):
    a = Arbre()
    if isinstance(l[0], int):
        a.gche = Poid(l[0])
    elif isinstance(l[0], list):
        a.gche = consArbre(l[0])
    if isinstance(l[1], int):
        a.drte = Poid(l[1])
    elif isinstance(l[1], list):
        a.drte = consArbre(l[1])
    return a


#trier et construction le mobile a l'ordre decroissant
def consDecroissant(l):
    l.sort()
    a = Arbre()
    if len(l) == 1:
        a = Poid(l[0])
        return a
    else:
        a.gche = Poid(l[0])
        a.drte = Poid(l[1])
    for i in range(2, len(l)):
        tmp = Arbre()
        tmp.drte = Poid(l[i])
        tmp.gche = a
        a = tmp
    return a

#trier et construction le mobile a l'ordre croissant
def consCroissant(l):
    l.sort()
    l.reverse()
    a = Arbre()
    if len(l) == 1:
        a = Poid(l[0])
        return a
    else:
        a.gche = Poid(l[1])
        a.drte = Poid(l[0])
    for i in range(2, len(l)):
        tmp = Arbre()
        tmp.gche = Poid(l[i])
        tmp.drte = a
        a = tmp
    return a

#rendu la liste en formant des listes de 2 elements comme un arbre
def sousListe(l):
    while len(l)%2 == 1 and len(l)>2:
        l = [sousListe(l[:-1]), l[-1]]
    while len(l)%2 == 0 and len(l)>2:
        l = [l[0:len(l)//2], l[len(l)//2:]]
        l =[sousListe(l[0]), sousListe(l[1])]
    return l

#construction arbre peu profond
def consArbreProfond(l):
    a =Arbre()
    liste = sousListe(l)
    a = consArbre(liste)
    return a 


#appel a l'affiche du mobile
def lancerMobile():
    global mobile
    if type(mobile) != Poid:
        mobile.proportion()
    afficheMobile()


#reconstruire le mobile selon le choix
def reconstruction(choix):
    global mobile
    if mobile != None:
        list = mobile.renduListe()
        if choix == DECROISSANT:
            mobile = consDecroissant(list)
        elif choix == CROISSANT:
            mobile = consCroissant(list)
        elif choix == PROFOND:
            mobile = consArbreProfond(list)
        lancerMobile()


#sauvegarde dans un fichier txt sous forme arbre
def exportArbre():
    global mobile
    nomfic = asksaveasfilename(title="Exporte mobile", filetypes=[("texte",".txt"),("tout",".*")])
    ficExport = open(nomfic, "w")
    list = mobile.renduArbre()
    ficExport.write(str(list))
    ficExport.close()

#sauvegarde dans un fichier txt sous forme liste
def exportListe():
    global mobile
    nomfic = asksaveasfilename(title="Exporte liste", filetypes=[("texte",".txt"),("tout",".*")])
    ficExport = open(nomfic, "w")
    list = mobile.renduListe()
    for i in list:
        ficExport.write(str(i)+"\n")
    ficExport.write("\n")
    ficExport.close()



#calcule l'echelle (en prenant la minimum de la proportion du largeur et du hauteur) et affiche le mobile
def afficheMobile():
    global mobile
    global canvas
    canvas.delete("all")
    largeur = canvas.winfo_width()
    hauteur = canvas.winfo_height()
    hautMax = mobile.poidMax()
    mobile.calculCoord()
    echelleLarg = largeur / mobile.largeurArbre()
    echelleHaut = hauteur / mobile.hauteurArbre()
    echelle = min(echelleLarg, echelleHaut)
    afficheNoeudFil(mobile, largeur/2, 0, hautMax)
    canvas.scale("all", largeur/2, 0, echelle, echelle)
    canvas.update()


#affiche les noeuds et les fils de l'arbre
def afficheNoeudFil(n , x, y, hauteur):
    global canvas
    canvas.create_line(x, y, x, y+hauteur, fill ="blue")
    if type(n) == Poid:
        if n.val == mobile.poidMax():
            canvas.create_oval(x-n.val/2, y+hauteur - n.val/2, x + n.val/2, y+hauteur +n.val/2, fill = "red")
        elif n.val == mobile.poidMin():
            canvas.create_oval(x-n.val/2, y+hauteur - n.val/2, x + n.val/2, y+hauteur +n.val/2, fill = "yellow")
        else:
            canvas.create_oval(x-n.val/2, y+hauteur - n.val/2, x + n.val/2, y+hauteur +n.val/2, fill = "green")
        canvas.create_text(x, y + hauteur, text=str(n))
    else:
        canvas.create_line(x + n.coordG.x, y + hauteur + n.coordG.y, x + n.coordD.x, y + hauteur + n.coordD.y, fill = "blue")
        afficheNoeudFil(n.gche, x + n.coordG.x, y + n.coordG.y + hauteur, hauteur)
        afficheNoeudFil(n.drte, x + n.coordD.x, y + n.coordD.y + hauteur, hauteur)




#construction de l'interface graphique en demarant
interface = Tk()
interface.geometry("600x800")


#variable pour la reconstruction
DECROISSANT = 0
CROISSANT = 1
PROFOND = 2

#creation de bouton des options
fm = Frame (interface)
boutonOuvrir = Button(fm, text="Importer", command=importlist)
boutonOuvrir.pack(side = LEFT)
boutonExportListe = Button(fm, text="Exporter Liste", command = exportListe)
boutonExportListe.pack(side = LEFT)
boutonExportArbre = Button(fm, text="Exporter Arbre", command = exportArbre)
boutonExportArbre.pack(side = LEFT)
boutonProfond = Button(fm, text="Profond", command =lambda:reconstruction(PROFOND))
boutonProfond.pack(side = LEFT)
boutonDecroissant = Button(fm, text="Decroissant", command=lambda:reconstruction(DECROISSANT))
boutonDecroissant.pack(side = LEFT)
boutonCroissant = Button(fm, text="Croissant", command=lambda:reconstruction(CROISSANT))
boutonCroissant.pack(side = LEFT)
fm.pack(side =TOP)

canvas = Canvas(interface, background = "#FFFFF0")
canvas.pack(side=TOP, fill=BOTH, expand = YES)
canvas.update()


interface.mainloop()



