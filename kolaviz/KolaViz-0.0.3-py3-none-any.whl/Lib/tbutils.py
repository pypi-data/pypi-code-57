from xkcdpass import xkcd_password as xp
from KolaViz.Lib.mlkmtpgenerator import get_words


def get_rnd_names(n, mywords=None, maxlen=10, idtype="uid"):
    """
    génère n noms aléatoire à partir de mots du fichier worfame.  
    Si fullname is given then return
    """
    if mywords is None:
        mywords = get_words(case="lower", minlen=3, maxlen=maxlen)

    if len(mywords) < n:
        raise Exception(
            f"Pas assez de mot dans {len(mywords)} pour les {n} demandés. "
            "changer maxlen"
        )

    L = []
    i = 0
    while i < n:
        name = get_random_name(mywords, idtype)
        if name not in L:
            L.append(name)
            i += 1
    return L


def get_random_name(mywords, idtype="uid"):
    """
    génère un nom complet aléatoire de type idtype.
    """
    if idtype == "uid":
        first = xp.generate_xkcdpassword(mywords, numwords=1).capitalize()
        last = xp.generate_xkcdpassword(mywords, numwords=1, case="upper")
        return " ".join([first, last])
    else:
        name = xp.generate_xkcdpassword(mywords, numwords=1).capitalize()
        return f"{name}{idtype}"


def get_rnd_tokens(nb_tokens, taille_max_token, capitalize=False, case="upper"):
    """
    génère n tokens aléatoire mais de taille p
    """
    wordfile = xp.locate_wordfile("./static/divers/wl_french")
    mywords = xp.generate_wordlist(
        wordfile=wordfile,
        min_length=3,
        max_length=taille_max_token,
        valid_chars="[a-z]",
    )

    if len(mywords) < nb_tokens:
        raise Exception(
            f"Pas assez de mots {len(mywords)} dispo pour {nb_tokens} demandés."
            " Demandez-en moins"
        )

    L = []
    i = 0
    while i < nb_tokens:
        name = get_random_token(mywords, capitalize, case)
        if name not in L:
            L.append(name)
            i += 1
    return L


def get_random_token(mywords, capitalize=False, case="upper"):
    """
    génère un nom complet aléatoire
    """
    if capitalize:
        return xp.generate_xkcdpassword(mywords, numwords=1, case=case).capitalize()
    else:
        return xp.generate_xkcdpassword(mywords, numwords=1, case=case)


def uid_humanize_dico(data, maxlen=12, idtype="uid"):
    """
    renvois un dico où chaque clefs est un nom aléatoire
    data est une série,
    maxlen  est la longueur max des noms aléatoire
    si idtype is uid, renvois 'nom prénom' sinon concatène idtype
    à la fin des noms générés
    """
    rnames = get_rnd_names(len(data.unique()), maxlen=maxlen, idtype=idtype)
    return dict(zip(data.unique(), rnames))
