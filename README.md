# NetworkGame

Outil de réseau graphique:

    Analyse Ipv4:
        1) Entrer une adresse Ipv4 valide avec un masque de sous réseau, cidr ou un nombre 
            d'hôtes requis
        2) Infos sur les informations qui la compose -> [type, classe, réservation, @Réseau,
            masque de sous réseau, CIDR, 1ère @Disponible, dernière @Disponible, @Broadcast,
            nombre d'utilisateurs possible]
    
    Analyse binaire:
        1) Entrer une adresse Ipv4 valide avec un masque de sous réseau, cidr ou un nombre
            d'hôtes requis
        2) Comparaison des adresses du réseau avec vision binaire en deux parties, partie
            réseau et partie hôtes

    VLSM:
        1) Entrer une adresse réseau à subdivisé valide avec masque de sous réseau, cidr ou un 
            nombre d'hôtes requis
        2) Ajout de sous réseau composé d'un [nom (facultatif), nombre d'hôtes requis]
        3) Supression de sous réseau par sélection de la cellule celulle
        4) Génération des sous réseaux via l'adresse réseau de subdivision -> [Nom, masque
            de sous réseau, @Reseau, nombres d'hôtes possible, CIDR]

    Génération de plan d'adressage:
        1) Plan d'adressage éditable via l'interface
        2) Ajouter une nouvelle ligne à la fin du plan
        3) Ajouter une ligne juste après la ligne sélectionnée
        4) Ajouter une nouvelle ligne au début du plan
        5) Ajouter une ligne avant celle sélectionnée
        6) Supprimer la ligne sélectionnée
        7) Importer le sous réseautage généré par VLSM
        8) Importer un fichier CSV (*csv) ou Excel (*xlxs)
        9) Exporter ou écraser le plan d'adressage vers un fichier CSV (*csv) ou Excel (*xlxs)

    Jeux/Entraînement:
        Analyse Ip:
            1) Analyser une adresse Ip ainsi que son CIDR afin de compléter le formulaire
                dans le temps imparti définit avant le lancement de la partie
            2) Définir un genre d'Ip par des modes de défis [Classe=alléatoire, Type=alléatoire,
                temps 02:00-60:00min=60:00, CIDR plage 1-30=1-30]
