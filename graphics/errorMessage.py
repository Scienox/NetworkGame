def errSelectCidr(error):
    if "base 10" in error:
        return "Nombre décimal invalide.\nChangez de cidr ou nombre d'utilisateurs.\n" \
        "Un CIDR valide: 1-30"
    elif "not a valid CIDR" in error:
        return "Masque de sous réseau invalide."
    else:
        return error + "#8"


def errIpv4(error):
    if "not a valid CIDR" in error:
        return errSelectCidr("base 10")
    elif "base 10" in error:
        return "Veuillez entrer une adresse réseau, ipv4, ou broadcast valide."
    else:
        return error + "#17"


def errVlsm(error):
    if "list index out of range" in error:
        return "Des sous réseaux doivent être créés."
    elif "base 10" in error:
        return errIpv4("base 10")
    elif "avaible" in error:
        requirement, avaible =  error.split("\n")[1].split(",")
        return "La taille du réseau ne permet pas d'acceuillir les sous réseaux.\n" \
        f"{requirement} hôte(s) requis et seulement {avaible} disponible(s)."
    elif "not a valid CIDR" in error:
        return errSelectCidr("base 10")
    else:
        return error + "#25"


def errSubnet(error):
    if "Network not created" in error:
        return "Des sous réseaux doivent être créés."
    elif "NoneType" in error:
        return "Il faut au moins désigner un nombre d'utilisateurs\n" \
        "par sous réseau."
    else:
        return error + "#35"
