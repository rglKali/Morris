import fltk

fltk.cree_fenetre(640, 640)
number = 0

while True:
    fltk.efface_tout()
    ev = fltk.donne_ev()
    if ev:
        if ev[0] == 'Quitte':
            break
    fltk.mise_a_jour()

fltk.ferme_fenetre()
