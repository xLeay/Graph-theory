
# --- EXERCICE 1 ---
# -- 1.1 MOTS --
# - 1.1.1 -


def pref(mot):
    """
    Renvoie la liste des préfixes de [mot].
    >>> pref('coucou')
    ['', 'c', 'co', 'cou', 'couc', 'couco', 'coucou']
    """
    pref = []
    for lettres in range(len(mot)+1):
        pref.append(mot[:lettres])

    return pref

# - 1.1.2 -


def suf(mot):
    """
    Renvoie la liste des suffixes de [mot].
    >>> suf('coucou')
    ['coucou', 'oucou', 'ucou', 'cou', 'ou', 'u', '']
    """
    suff = []
    for lettres in range(len(mot)+1):
        suff.append(mot[lettres:])

    return suff

# - 1.1.3 -


def fact(mot):
    """
    Renvoie l'ensemble sans doublons des facteurs de [mot].
    >>> fact('coucou')
    ['', 'c', 'co', 'cou', 'couc', 'couco', 'coucou', 'o', 'ou', 'ouc', 'ouco', 'oucou', 'u', 'uc', 'uco', 'ucou']
    """
    fact = []
    for i in range(len(mot)+1):
        for j in range(len(mot)+1):
            fact.append(mot[i:j])

    return sorted(list(set(fact)))

# - 1.1.4 -


def mirr(mot):
    """
    Renvoie le mirroir de [mot].
    >>> mirr('coucou')
    'uocuoc'
    """
    return mot[::-1]

# -- 1.2 LANGAGES --
# - 1.2.1 -


def concatene(langage1, langage2):
    """
    Renvoie le produit de concaténation (sans doublons) de L1 et L2.
    >>> L1 = ['aa','ab','ba','bb']
    >>> L2 = ['a', 'b', '']
    >>> concatene(L1,L2)
    ['aaa', 'aab', 'aa', 'aba', 'abb', 'ab', 'baa', 'bab', 'ba', 'bba', 'bbb', 'bb']
    """
    L3 = []
    for mot1 in langage1:
        for mot2 in langage2:
            L3.append(mot1+mot2)

    return L3

# - 1.2.2 -


def puis(langage, n):
    """
    Renvoie le langage L^n (sans doublons).
    >>> L1=['aa','ab','ba','bb']
    >>> puis(L1,2)
    ['aaaa', 'aaab', 'aaba', 'aabb', 'abaa', 'abab', 'abba', 'abbb', 'baaa', 'baab', 'baba', 'babb', 'bbaa', 'bbab', 'bbba', 'bbbb']
    """
    L2 = langage
    for i in range(n-1):
        L2 = concatene(L2, langage)

    return L2

# - 1.2.3 -

# On ne peux pas faire cela car c'est infini.

# - 1.2.4 -


def tousmots(Alphabet, n):
    """
    Renvoie la liste de tous les mots de A* de longueur inférieure ou égal à n.
    >>> tousmots(['a','b'],3)
    ['', 'a', 'b', 'aa', 'ab', 'ba', 'bb', 'aaa', 'aab', 'aba', 'abb', 'baa', 'bab', 'bba', 'bbb']
    """
    L = ['']
    for i in range(n+1):
        L.extend(puis(Alphabet, i))

    L = sorted(list(set(L)))
    return sorted(L, key=len)

# -- 1.3 AUTOMATES --
# - 1.3.1 -


def defauto():
    """
    Permet de faire la saisie d'un automate sans doublon.
    >>> auto = {"alphabet":['a','b'],"etats": [1,2,3,4], "transitions":[[1,'a',2],[2,'a',2],[2,'b',3],[3,'a',4]], "I":[1],"F":[4]}
    """
    auto = dict()

    auto["alphabet"] = sorted(
        list(set(input("Entrez l'alphabet de l'automate : "))))
    if ' ' in auto["alphabet"]:
        auto["alphabet"].remove(' ')

    auto["etats"] = sorted(
        list(set(input("Entrez les états de l'automate : "))))
    if ' ' in auto["etats"]:
        auto["etats"].remove(' ')

    auto["transitions"] = []
    for etats in auto["etats"]:
        for lettre in auto["alphabet"]:
            transi = input(
                "Entrez la transition de l'état {} pour la lettre {} : ".format(etats, lettre))

            if transi == '' or ' ':
                continue

            if transi in auto["etats"]:
                auto["transitions"].append([etats, lettre, transi])
            else:
                print("L'état {} n'existe pas.".format(transi))
                transition_valide = input(
                    "Entrez la transition de l'état {} pour la lettre {} : ".format(etats, lettre))
                auto["transitions"].append([etats, lettre, transition_valide])

    auto["I"] = sorted(
        list(set(input("Entrez les états initiaux de l'automate : "))))
    if ' ' in auto["I"]:
        auto["I"].remove(' ')

    auto["F"] = sorted(
        list(set(input("Entrez les états finaux de l'automate : "))))
    if ' ' in auto["F"]:
        auto["F"].remove(' ')

    return auto

# - 1.3.2 -


def lirelettre(transitions, etats, lettre):
    """
    Renvoie la liste des états dans lesquels on peut arriver en partant d'un état de E et en lisant la lettre a.
    >>> lirelettre([[1,'a',2],[2,'a',2],[2,'b',3],[3,'a',4]], [1,2,3,4], 'a')
    [2, 4]
    """
    L = []
    for i in range(len(transitions)):
        # print(transitions[i][0], transitions[i][1], etats)
        if transitions[i][0] in etats and transitions[i][1] == lettre:
            L.append(transitions[i][2])

    return list(set(L))

# - 1.3.3 -


def liremot(transitions, etats, mot):
    """
    Renvoie la liste des états dans lesquels on peut arriver en partant d'un état de E et en lisant le mot m.
    >>> liremot([[1,'a',2],[2,'a',2],[2,'b',3],[3,'a',4]], [1,2,3,4], 'aba')
    [4]
    >>> liremot([[1,'a',2],[2,'a',2],[2,'b',3],[3,'a',4]], [1,2,3,4], 'ab')
    [3]
    >>> liremot([[1,'a',2],[2,'b',3],[3,'c',3]], [1,2,3], 'abcc')
    [3]
    >>> liremot([[1,'a',2],[2,'a',2],[2,'b',3],[3,'a',4]], [1,2,3,4], 'aa')
    [2]
    >>> liremot([[1,'a',2],[1,'a',6],[2,'b',2],[2,'b',3],[3,'a',4],[4,'b',5],[5,'b',5],[6,'b',6],[6,'a',5]], [1,2,3,4,5,6], 'abba')
    [4, 5]
    """
    etats_suivants = [etats[0]]

    for lettre in mot:
        etats_suivants = lirelettre(transitions, etats_suivants, lettre)

    return list(set(etats_suivants))

# - 1.3.4 -


def accepte(automate, mot):
    """
    Renvoie True si le mot m est accepté par l'automate. Un chemin est dit acceptant s'il mène d'un état initial à un état final. Un mot est accepté par un automate s'il est l'étiquette d'un chemin acceptant.
    >>> auto = {"alphabet":['a','b'],"etats": [1,2,3,4], "transitions":[[1,'a',2],[2,'a',2],[2,'b',3],[3,'a',4]], "I":[1],"F":[4]}
    >>> accepte(auto, 'aba')
    True
    >>> accepte(auto, 'ab')
    False
    >>> accepte(auto, 'aa')
    False
    >>> accepte(auto, 'abba')
    False
    """
    etats_suivants = liremot(automate["transitions"], automate["I"], mot)

    for etat in etats_suivants:
        if etat in automate["F"]:
            return True
    return False

# - 1.3.5 -


def langage_accept(automate, n):
    """
    Renvoie la liste des mots de longueur inférieure ou égal à n acceptés par l'automate.
    >>> auto = {"alphabet":['a','b'],"etats": [1,2,3,4], "transitions":[[1,'a',2],[2,'a',2],[2,'b',3],[3,'a',4]], "I":[1],"F":[4]}
    >>> auto2 = {"alphabet":['a','b'],"etats": [1,2,3,4,5,6], "transitions":[[1,'a',1],[1,'a',6],[1,'b',2],[2,'b',2],[2,'a',3],[3,'a',3],[3,'a',4],[4,'b',5],[5,'b',5],[6,'b',6],[6,'a',5]], "I":[1],"F":[1,5]}
    >>> langage_accept(auto, 1)
    []
    >>> langage_accept(auto, 4)
    ['aba', 'aaba']
    >>> langage_accept(auto2, 3)
    ['', 'a', 'aa', 'aaa', 'aab', 'aba']
    """
    L = []
    for mot in tousmots(automate["alphabet"], n):
        if accepte(automate, mot):
            L.append(mot)

    return L

# - 1.3.6 -


# Pour cela, il faudrait tester toutes les possibilités de mots et ce jusqu'à l'infini. Ce qui n'est pas possible pour un programme.

# --- EXERCICE 2 ---
# -- 2.1 --


def deterministe(automate):
    """
    Renvoie True s'il est déterministe et False sinon. Un automate est déterministe s'il possède un seul état initial et si pour tout état p et toute lettre a, il existe au plus une transition partant de p et étiquetée par a.
    >>> auto0 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2, 3], "transitions": [[0, 'a', 1], [1, 'a', 1], [1, 'b', 2], [2, 'a', 3]], "I": [0], "F": [3]}
    >>> auto1 = {"alphabet": ['a', 'b'], "etats": [0, 1], "transitions": [[0, 'a', 0], [0, 'b', 1], [1, 'b', 1], [1, 'a', 1]], "I": [0], "F": [1]}
    >>> auto2 = {"alphabet": ['a', 'b'], "etats": [0, 1], "transitions": [[0, 'a', 0], [0, 'a', 1], [1, 'b', 1], [1, 'a', 1]], "I": [0], "F": [1]}
    >>> auto3 = {"alphabet": ['a', 'b'], "etats": [1, 2, 3, 4, 5, 6], "transitions": [[1, 'a', 2], [1, 'b', 6], [2, 'b', 2], [2, 'a', 3], [3, 'b', 3], [3, 'a', 4], [4, 'b', 5], [5, 'b', 5], [6, 'b', 6], [6, 'a', 5]], "I": [1], "F": [1, 5]}
    >>> deterministe(auto0)
    True
    >>> deterministe(auto1)
    True
    >>> deterministe(auto2)
    False
    >>> deterministe(auto3)
    True
    """
    if len(automate["I"]) != 1:
        return False

    for etat in automate["etats"]:
        for lettre in automate["alphabet"]:
            if len(lirelettre(automate["transitions"], [etat], lettre)) > 1:
                return False

    return True

# -- 2.2 --


def determinise(automate):
    """
    Renvoie l'automate déterminisé de l'automate donné.
    >>> auto0 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2, 3], "transitions": [[0, 'a', 1], [1, 'a', 1], [1, 'b', 2], [2, 'a', 3]], "I": [0], "F": [3]}
    >>> auto1 = {"alphabet": ['a', 'b'], "etats": [0, 1], "transitions": [[0, 'a', 0], [0, 'b', 1], [1, 'b', 1], [1, 'a', 1]], "I": [0], "F": [1]}
    >>> deterministe(determinise(auto0))
    True
    >>> deterministe(determinise(auto1))
    True
    >>> auto5 = {"alphabet": ['a', 'b'], "etats": [1, 2, 3, 4, 5, 6], "transitions": [[1, 'a', 1], [1, 'a', 2], [1, 'b', 6], [2, 'b', 2], [2, 'a', 3], [3, 'b', 3], [3, 'b', 4], [4, 'a', 5], [5, 'b', 5], [6, 'a', 6], [6, 'a', 5]], "I": [1], "F": [5]}
    >>> auto5det = determinise(auto5)
    >>> print(auto5det)
    {'alphabet': ['a', 'b'], 'etats': [[1], [1, 2], [1, 2, 3], [2], [2, 3, 4], [2, 3, 4, 6], [2, 6], [3], [3, 4], [3, 4, 5], [3, 5], [3, 5, 6], [5], [5, 6], [6]], 'transitions': [[[1], 'a', [1, 2]], [[1], 'b', [6]], [[1, 2], 'a', [1, 2, 3]], [[1, 2], 'b', [2, 6]], [[1, 2, 3], 'a', [1, 2, 3]], [[1, 2, 3], 'b', [2, 3, 4, 6]], [[2], 'a', [3]], [[2], 'b', [2]], [[2, 3, 4], 'a', [3, 5]], [[2, 3, 4], 'b', [2, 3, 4]], [[2, 3, 4, 6], 'a', [3, 5, 6]], [[2, 3, 4, 6], 'b', [2, 3, 4]], [[2, 6], 'a', [3, 5, 6]], [[2, 6], 'b', [2]], [[3], 'b', [3, 4]], [[3, 4], 'a', [5]], [[3, 4], 'b', [3, 4]], [[3, 4, 5], 'a', [5]], [[3, 4, 5], 'b', [3, 4, 5]], [[3, 5], 'b', [3, 4, 5]], [[3, 5, 6], 'a', [5, 6]], [[3, 5, 6], 'b', [3, 4, 5]], [[5], 'b', [5]], [[5, 6], 'a', [5, 6]], [[5, 6], 'b', [5]], [[6], 'a', [5, 6]]], 'I': [1], 'F': [[3, 4, 5], [3, 5], [3, 5, 6], [5], [5, 6]]}

    >>> auto3 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2], "transitions": [[0,'a',0], [0,'a',1], [1,'b',1], [1,'b',2], [2,'b',2]], "I": [0], "F": [2]}
    >>> auto3det = determinise(auto3)
    >>> print(auto3det)
    {'alphabet': ['a', 'b'], 'etats': [[0], [0, 1], [1, 2]], 'transitions': [[[0], 'a', [0, 1]], [[0, 1], 'a', [0, 1]], [[0, 1], 'b', [1, 2]], [[1, 2], 'b', [1, 2]]], 'I': [0], 'F': [[1, 2]]}
    """
    if deterministe(automate):
        return automate

    alphabet = automate["alphabet"]
    transitions = automate["transitions"]
    I = automate["I"]
    F = automate["F"]
    etats_deter = [I]

    transitions_deter = []
    for etat in etats_deter:
        for lettre in alphabet:
            etat_suivant = lirelettre(transitions, etat, lettre)
            if etat_suivant not in etats_deter:
                etats_deter.append(etat_suivant)
            transitions_deter.append([etat, lettre, etat_suivant])

            if etat_suivant == []:
                transitions_deter.remove([etat, lettre, etat_suivant])

    F_deter = []
    for etat in etats_deter:
        for etat_final in F:
            if etat_final in etat:
                F_deter.append(etat)

        if [] in etats_deter:
            etats_deter.remove([])


    etats_deter.sort()
    transitions_deter.sort()
    F_deter.sort()
    
    return {"alphabet": alphabet, "etats": etats_deter, "transitions": transitions_deter, "I": I, "F": F_deter}

# -- 2.3 --


def renommage(automate):
    """
    Renvoie l'automate obtenu par le renommage de l'automate donné. Si il existe des états composés de plusieurs états, ils doivent être renommés en état d'un simple chiffre
    >>> auto2det = {'alphabet': ['a', 'b'], 'etats': [[0], [0, 1], [1]], 'transitions': [[[0], 'a', [0, 1]], [[0, 1], 'a', [0, 1]], [[0, 1], 'b', [1]], [[1], 'a', [1]], [[1], 'b', [1]]], 'I': [[0]], 'F': [[0, 1], [1]]}
    >>> renommage(auto2det)
    {'alphabet': ['a', 'b'], 'etats': [[1], [2], [3]], 'transitions': [[[1], 'a', [2]], [[2], 'a', [2]], [[2], 'b', [3]], [[3], 'a', [3]], [[3], 'b', [3]]], 'I': [1], 'F': [[2], [3]]}
    """
    alphabet = automate["alphabet"]
    transitions = automate["transitions"]
    I = automate["I"]
    F = automate["F"]
    etats = automate["etats"]

    start = 0
    offset = 0
    etats_renom = []
    if etats[0]:
        start = 1
        offset = 1

    for i in range(start, len(etats)+offset):
        etats_renom.append([i])

    transitions_renom = []
    for transition in transitions:
        if not isinstance(transition[0], list):
            transition[0] = [transition[0]]
        if not isinstance(transition[2], list):
            transition[2] = [transition[2]]

    for transi in range(len(transitions)):

        etat_depart = transitions[transi][0]
        lettre = transitions[transi][1]
        etat_arrivee = transitions[transi][2]

        #debug
        try:
            transitions_renom.append([etats_renom[etats.index(etat_depart)], lettre, etats_renom[etats.index(etat_arrivee)]])
        except ValueError:
            # print("Erreur: l'état " + str(etat_depart) + " n'existe pas dans l'automate. Boucle: " + str(transi))
            # print(etats_renom[transi-1][0])
            # print(etat_depart[0])
            transitions_renom.append([etats_renom[etats.index(etat_depart[0])][0], lettre, etats_renom[etats.index(etat_arrivee[0])][0]])


    for etat in etats:
        if etat in I:
            I = etats_renom[etats.index(etat)]

    F_renom = []
    for etat_final in F:
        if not isinstance(etat_final, list):
            etat_final = [etat_final]

        #debug
        try:
            F_renom.append(etats_renom[etats.index(etat_final)])
        except ValueError:
            # print("Erreur: l'état " + str(etat_final) + " n'existe pas dans l'automate. Boucle: " + str(transi))
            F_renom.append(etats_renom[etats.index(etat_final[0])])




    return {"alphabet": alphabet, "etats": etats_renom, "transitions": transitions_renom, "I": I, "F": F_renom}

# --- EXERCICE 3 ---
# -- 3.1 --


def complet(automate):
    """
    Un automate fini est dit complet si, pour tout état Q et toute lettre a, il existe au moins un état r tel que (Q, 'a', r) soit une transition de l'automate.
    Renvoie True si l'automate est complet et False sinon.
    >>> auto3 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2], "transitions": [[0, 'a', 1], [0, 'a', 0], [1, 'b', 2], [1, 'b', 1]], "I": [0], "F": [2]}
    >>> auto4 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2], "transitions": [[0, 'a', 0], [0, 'b', 1], [1, 'a', 1], [1, 'b', 2], [2, 'a', 2], [2, 'b', 2]], "I": [0], "F": [2]}
    >>> complet(auto3)
    False
    >>> complet(auto4)
    True
    """
    alphabet = automate["alphabet"]
    transitions = automate["transitions"]
    etats = automate["etats"]

    for etat in etats:
        for lettre in alphabet:
            if not lirelettre(transitions, [etat], lettre):
                return False

    return True

# -- 3.2 --


def complete(automate):
    """
    Complète et renvoie l’automate passé en paramètre en ajoutant un état puits si il n'est pas déjà complet.
    >>> auto5 = {'alphabet': ['a', 'b'], 'etats': [1, 2, 3, 4, 5, 6], 'transitions': [[1, 'a', 1], [1, 'a', 2], [1, 'b', 6], [2, 'b', 2], [2, 'a', 3], [3, 'b', 3], [3, 'b', 4], [4, 'a', 5], [5, 'b', 5], [6, 'a', 6], [6, 'a', 5]], 'I': [1], 'F': [5]}
    >>> complete(auto5)
    {'alphabet': ['a', 'b'], 'etats': [1, 2, 3, 4, 5, 6, 'Ø'], 'transitions': [[1, 'a', 1], [1, 'a', 2], [1, 'b', 6], [2, 'b', 2], [2, 'a', 3], [3, 'b', 3], [3, 'b', 4], [4, 'a', 5], [5, 'b', 5], [6, 'a', 6], [6, 'a', 5], [3, 'a', 'Ø'], [4, 'b', 'Ø'], [5, 'a', 'Ø'], [6, 'b', 'Ø'], ['Ø', 'a', 'Ø'], ['Ø', 'b', 'Ø']], 'I': [1], 'F': [5]}
    """
    if complet(automate):
        return automate

    alphabet = automate["alphabet"]
    transitions = automate["transitions"]
    I = automate["I"]
    F = automate["F"]
    etats = automate["etats"]

    etats.append("Ø")
    # etats.append(etats[-1] + 1)
    for etat in etats:
        for lettre in alphabet:
            if not lirelettre(transitions, [etat], lettre):
                transitions.append([etat, lettre, etats[-1]])

    return {"alphabet": alphabet, "etats": etats, "transitions": transitions, "I": I, "F": F}

# -- 3.3 --


def complement(automate):
    """
    Renvoie le complément d'un automate. Pour obtenir le complément d'un automate, on le déterminise, on le complète puis on échange les états terminaux.
    C'est à dire que tous les états non terminaux deviennent terminaux, et tous les états terminaux deviennent non terminaux.
    >>> auto3 = {'alphabet': ['a', 'b'], 'etats': [1, 2, 3], 'transitions': [[1, 'a', 2], [1, 'a', 1], [2, 'b', 3], [2, 'b', 2]], 'I':[1], 'F': [3]}
    >>> complement(auto3)
    {'alphabet': ['a', 'b'], 'etats': [1, 2, 3, 'Ø'], 'transitions': [[1, 'a', 2], [2, 'a', 2], [2, 'b', 3], [3, 'b', 3], [1, 'b', 'Ø'], [3, 'a', 'Ø'], ['Ø', 'a', 'Ø'], ['Ø', 'b', 'Ø']], 'I': [1], 'F': [1, 2, 'Ø']}
    """
    automate = determinise(automate)
    automate = renommage(automate)

    etats = automate["etats"]
    transitions = automate["transitions"]
    I = automate["I"]
    F = automate["F"]

    etatssimple = []
    transitionssimple = []
    Fsimple = []

    for etat in etats:
        if isinstance(etat, list):

            etat = etat[0]
            etatssimple.append(etat)
            
    for transition in transitions:
        if isinstance(transition[0], list):

            transition[0], transition[2] = transition[0][0], transition[2][0]
            transitionssimple.append(transition)

    for final in F:
        if isinstance(final, list):

            final = final[0]
            Fsimple.append(final)

    for etatsimple in etatssimple:
        if etatsimple in Fsimple:
                
            Fsimple.remove(etatsimple)
        else:
            Fsimple.append(etatsimple)
    
    automaterenomme = {"alphabet": automate["alphabet"], "etats": etatssimple, "transitions": transitionssimple, "I": I, "F": Fsimple}
    automaterenomme = complete(automaterenomme)
    Fsimple.append(etatssimple[-1])

    return automaterenomme


# --- EXERCICE 4 ---
# -- 4.1 --

def produit(automate1, automate2):
    """
    >>> auto4 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2], "transitions": [[0, 'a', 1], [1, 'b', 2], [2, 'b', 2], [2, 'a', 2]], "I": [0], "F": [2]}
    >>> auto5 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2], "transitions": [[0, 'a', 0], [0, 'b', 1], [1, 'a', 1], [1, 'b', 2], [2, 'a', 2], [2, 'b', 0]], "I": [0], "F": [0, 1]}
    >>> produit(auto4, auto5)
    {'alphabet': ['a', 'b'], 'etats': [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], 'transitions': [[(0, 0), 'a', (1, 0)], [(1, 0), 'b', (2, 1)], [(2, 0), 'a', (2, 0)], [(2, 0), 'b', (2, 1)], [(2, 1), 'a', (2, 1)], [(2, 1), 'b', (2, 2)], [(2, 2), 'a', (2, 2)], [(2, 2), 'b', (2, 0)]], 'I': [(0, 0)], 'F1': [2], 'F2': [0, 1]}
    """
    if not deterministe(automate1) or not deterministe(automate2):
        automate1 = determinise(automate1)
        automate2 = determinise(automate2)
        automate1 = renommage(automate1)
        automate2 = renommage(automate2)

    alphabet = automate1["alphabet"]
    transitions1, transitions2 = automate1["transitions"], automate2["transitions"]
    I1, I2, F1, F2 = automate1["I"], automate2["I"], automate1["F"], automate2["F"]
    
    etats1 = automate1["etats"]
    etats2 = automate2["etats"]
    etats = []
    I = [(x, y) for x in I1 for y in I2]
    F1 = [x for x in F1]
    F2 = [x for x in F2]

    for etatall in etats1:
        for etatall2 in etats2:
            etat = (etatall, etatall2)
            etats.append(etat)

    autoEtat = I.copy()
    autoTransitions = []

    for etat in autoEtat:
        for lettre in alphabet:
            etat1 = lirelettre(transitions1, [etat[0]], lettre)
            etat2 = lirelettre(transitions2, [etat[1]], lettre)

            if etat1 != [] and etat2 != []:
                etat = (etat1[0], etat2[0])

                if etat not in autoEtat:
                    autoEtat.append(etat)
    
    autoEtat.sort()

    for ele in autoEtat:
        for lettre in alphabet:
            etat1 = lirelettre(transitions1, [ele[0]], lettre)
            etat2 = lirelettre(transitions2, [ele[1]], lettre)

            if etat1 != [] and etat2 != []:
                etat = (etat1[0], etat2[0])
                autoTransitions.append([ele, lettre, etat])

    return {"alphabet": alphabet, "etats": autoEtat, "transitions": autoTransitions, "I": I, "F1": F1, "F2": F2}


def inter(autoEtat, autoTransitions, alphabet, I, F1, F2):
    """
    Renvoie l'intersection de deux automates.
    >>> auto4 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2], "transitions": [[0, 'a', 1], [1, 'b', 2], [2, 'b', 2], [2, 'a', 2]], "I": [0], "F": [2]}
    >>> auto5 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2], "transitions": [[0, 'a', 0], [0, 'b', 1], [1, 'a', 1], [1, 'b', 2], [2, 'a', 2], [2, 'b', 0]], "I": [0], "F": [0, 1]}
    >>> produit(auto4, auto5)
    {'alphabet': ['a', 'b'], 'etats': [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], 'transitions': [[(0, 0), 'a', (1, 0)], [(1, 0), 'b', (2, 1)], [(2, 0), 'a', (2, 0)], [(2, 0), 'b', (2, 1)], [(2, 1), 'a', (2, 1)], [(2, 1), 'b', (2, 2)], [(2, 2), 'a', (2, 2)], [(2, 2), 'b', (2, 0)]], 'I': [(0, 0)], 'F1': [2], 'F2': [0, 1]}
    >>> inter(produit(auto4, auto5)['etats'], produit(auto4, auto5)['transitions'], produit(auto4, auto5)['alphabet'], produit(auto4, auto5)['I'], produit(auto4, auto5)['F1'], produit(auto4, auto5)['F2'])
    {'alphabet': ['a', 'b'], 'etats': [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], 'transitions': [[(0, 0), 'a', (1, 0)], [(1, 0), 'b', (2, 1)], [(2, 0), 'a', (2, 0)], [(2, 0), 'b', (2, 1)], [(2, 1), 'a', (2, 1)], [(2, 1), 'b', (2, 2)], [(2, 2), 'a', (2, 2)], [(2, 2), 'b', (2, 0)]], 'I': [(0, 0)], 'F': [(2, 0), (2, 1)]}

    Quand en a, l'automate 1 va dans un état, l'automate 2 va dans un état avec cette même lettre composée des deux états. Exemple: L'automate 1 va dans l'état 1 avec la lettre a, l'automate 2 va dans l'état 2 avec la lettre a. Cela fait l'état (1, 2). 
    """
    
    F = []
    for etat in autoEtat:
        if etat[0] in F1 and etat[1] in F2:
            F.append(etat)

    autoTransitions.sort()
    return {"alphabet": alphabet, "etats": autoEtat, "transitions": autoTransitions, "I": I, "F": F}

# -- 4.2 --


def difference(autoEtat, autoTransitions, alphabet, I, F1, F2):
    """
    Renvoie l'intersection de deux automates.
    >>> auto4 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2], "transitions": [[0, 'a', 1], [1, 'b', 2], [2, 'b', 2], [2, 'a', 2]], "I": [0], "F": [2]}
    >>> auto5 = {"alphabet": ['a', 'b'], "etats": [0, 1, 2], "transitions": [[0, 'a', 0], [0, 'b', 1], [1, 'a', 1], [1, 'b', 2], [2, 'a', 2], [2, 'b', 0]], "I": [0], "F": [0, 1]}
    >>> produit(auto4, auto5)
    {'alphabet': ['a', 'b'], 'etats': [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], 'transitions': [[(0, 0), 'a', (1, 0)], [(1, 0), 'b', (2, 1)], [(2, 0), 'a', (2, 0)], [(2, 0), 'b', (2, 1)], [(2, 1), 'a', (2, 1)], [(2, 1), 'b', (2, 2)], [(2, 2), 'a', (2, 2)], [(2, 2), 'b', (2, 0)]], 'I': [(0, 0)], 'F1': [2], 'F2': [0, 1]}
    >>> difference(produit(auto4, auto5)['etats'], produit(auto4, auto5)['transitions'], produit(auto4, auto5)['alphabet'], produit(auto4, auto5)['I'], produit(auto4, auto5)['F1'], produit(auto4, auto5)['F2'])
    {'alphabet': ['a', 'b'], 'etats': [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], 'transitions': [[(0, 0), 'a', (1, 0)], [(1, 0), 'b', (2, 1)], [(2, 0), 'a', (2, 0)], [(2, 0), 'b', (2, 1)], [(2, 1), 'a', (2, 1)], [(2, 1), 'b', (2, 2)], [(2, 2), 'a', (2, 2)], [(2, 2), 'b', (2, 0)]], 'I': [(0, 0)], 'F': [(2, 2)]}

    Quand en a, l'automate 1 va dans un état, l'automate 2 va dans un état avec cette même lettre composée des deux états. Exemple: L'automate 1 va dans l'état 1 avec la lettre a, l'automate 2 va dans l'état 2 avec la lettre a. Cela fait l'état (1, 2). 
    """
    
    F = []
    for etat in autoEtat:
        if etat[0] in F1 and etat[1] not in F2:
            F.append(etat)

    autoTransitions.sort()
    return {"alphabet": alphabet, "etats": autoEtat, "transitions": autoTransitions, "I": I, "F": F}


# --- EXERCICE 5 ---
# -- 5.1 --


def accessible(automate):
    """
    Renvoie True si l'automate est accessible et False sinon.
    """
    alphabet = automate["alphabet"]
    eta = automate["etats"]
    trans = automate["transitions"]
    I = automate["I"]
    Fin = automate["F"]

    etats = []
    transitions = []
    F = []

    for etat in eta:
        if isinstance(etat, list):
            etat = etat[0]
            etats.append(etat)
            
    for transition in trans:
        if isinstance(transition[0], list):
            transition[0], transition[2] = transition[0][0], transition[2][0]
            transitions.append(transition)

    for final in Fin:
        if isinstance(final, list):
            final = final[0]
            F.append(final)

    etats_accessibles = []
    etats_accessibles.append(I)

    for etat in etats_accessibles:
        for lettre in alphabet:
            etat_suivant = lirelettre(transitions, etat, lettre)
            if etat_suivant not in etats_accessibles:
                etats_accessibles.append(etat_suivant)

    etats_accessibles2 = []
    for et in etats_accessibles:
        if isinstance(et, list):
            if et != []:
                et = et[0]
            etats_accessibles2.append(et)

    if etats_accessibles2 != []:
        for etat in etats:
            if etat not in etats_accessibles2:
                return False
    
    else:
        for etat in etats:
            if etat not in etats_accessibles:
                return False

    return True


def prefixe(automate, L):
    """
    Renvoie un automate acceptant l'ensemble des préfixes des mots de L.
    """
    alphabet = automate["alphabet"]
    etats = automate["etats"]
    transitions = automate["transitions"]
    I = automate["I"]
    F = automate["F"]

    if I[0] not in F:
        F.append(I[0])

    transitions.sort()
    for lettre in alphabet:
        if [transitions[-1][2], lettre, transitions[-1][2]] not in transitions:
            transitions.append([transitions[-1][2], lettre, transitions[-1][2]])

    etats.sort()
    I.sort()
    F.sort()

    return {"alphabet": alphabet, "etats": etats, "transitions": transitions, "I": I, "F": F}

# -- 5.2 --


def suffixe(automate, L):
    """
    Renvoie un automate acceptant l'ensemble des suffixes des mots de L.
    """
    alphabet = automate["alphabet"]
    etats = automate["etats"]
    transitions = automate["transitions"]
    I = automate["I"]
    F = automate["F"]

    if I[0] not in F:
        F.append(I[0])

    transitions.sort()
    for lettre in alphabet:
        if [transitions[0][0], lettre, transitions[0][0]] not in transitions:
            transitions.insert(0, [transitions[0][0], lettre, transitions[0][0]])

    etats.sort()
    I.sort()
    F.sort()
    return {"alphabet": alphabet, "etats": etats, "transitions": transitions, "I": I, "F": F}

# -- 5.3 --


def facteur(automate, L):
    """
    Renvoie un automate acceptant l'ensemble des facteurs des mots de L.
    """
    alphabet = automate["alphabet"]
    etats = automate["etats"]
    transitions = automate["transitions"]
    I = automate["I"]
    F = automate["F"]

    if I[0] not in F:
        F.append(I[0])

    transitions.sort()

    for lettre in alphabet:
        if [transitions[0][0], lettre, transitions[0][0]] not in transitions:
            transitions.insert(0, [transitions[0][0], lettre, transitions[0][0]])

        if [transitions[-1][2], lettre, transitions[-1][2]] not in transitions:
            transitions.append([transitions[-1][2], lettre, transitions[-1][2]])

    etats.sort()
    I.sort()
    F.sort()
    return {"alphabet": alphabet, "etats": etats, "transitions": transitions, "I": I, "F": F}

# -- 5.4 --


def mirroir(automate, L):
    """
    Renvoie un automate acceptant l'ensemble des facteurs des mots de L.
    """
    alphabet = automate["alphabet"]
    etats = automate["etats"]
    transitions = automate["transitions"]
    I = automate["I"]
    F = automate["F"]

    if I[0] not in F:
        F.append(I[0])

    transitions.sort()

    for lettre in alphabet:
        if [transitions[0][0], lettre, transitions[0][0]] not in transitions:
            transitions.insert(0, [transitions[0][0], lettre, transitions[0][0]])

        if [transitions[-1][2], lettre, transitions[-1][2]] not in transitions:
            transitions.append([transitions[-1][2], lettre, transitions[-1][2]])

    etats.sort()
    I.sort()
    F.sort()
    return {"alphabet": alphabet, "etats": etats, "transitions": transitions, "I": I, "F": F}


# --- EXERCICE 6 ---


def minimise(automate):
    """
    Renvoie l'automate minimisé.
    >>> auto6 = {"alphabet":['a','b'],"etats": [0,1,2,3,4,5], "transitions":[[0,'a',4],[0,'b',3],[1,'a',5],[1,'b',5],[2,'a',5],[2,'b',2],[3,'a',1],[3,'b',0], [4,'a',1],[4,'b',2],[5,'a',2],[5,'b',5]], "I":[0],"F":[0,1,2,5]}
    >>> minimise(auto6)
    {'alphabet': ['a', 'b'], 'etats': [[0], [1, 2, 5], [3], [4]], 'I': [[0]], 'transitions': [[[0], 'a', [4]], [[0], 'b', [3]], [[1, 2, 5], 'a', [1, 2, 5]], [[1, 2, 5], 'b', [1, 2, 5]], [[3], 'a', [1, 2, 5]], [[3], 'b', [0]], [[4], 'a', [1, 2, 5]], [[4], 'b', [1, 2, 5]]], 'F': [[0], [1, 2, 5]]}
    """
    if not complet(automate) and deterministe(automate):
        return "L'automate n'est pas complet et/ou deterministe."

    groupes = [[x for x in automate["F"]], [x for x in automate["etats"] if x not in automate["F"]]]
    groupe_prec = []

    transi = { x: { a: {"vers": 0, "symbole": 0} for a in automate["alphabet"] } for x in automate["etats"] }

    for transition in automate["transitions"]:
        transi[transition[0]][transition[1]]["vers"] = transition[2]
        transi[transition[0]]["symbole"] = 0

    while groupe_prec != groupes:
        groupe_prec = groupes
        for group in groupes:
            for etat in group:
                transi[etat]["symbole"] = groupes.index(group)
            for etat in automate["etats"]:
                for a in transi[etat].keys():
                    if a not in automate["alphabet"] or transi[etat][a]["vers"] not in group:
                        continue
                    transi[etat][a]["symbole"] = groupes.index(group)
        
        groupe_nouv = {}
        
        for etat in transi:
            key = [transi[etat]["symbole"]]
            for a in transi[etat].values():
                if isinstance(a, dict):
                    key.append(a["symbole"])
            key = tuple(key)
            if key not in groupe_nouv:
                groupe_nouv[key] = []
            groupe_nouv[key].append(etat)
        groupes = [x for x in groupe_nouv.values()]

    minimise = { "alphabet": automate["alphabet"],"etats": groupes,"I": [],"transitions": [],"F": [] }

    for group in groupes:
        for a in automate["alphabet"]:
            etat = group[0]
            vers = transi[etat][a]["vers"]

            for dest in groupes:
                if vers in dest:
                    minimise["transitions"].append([group, a, dest])
                    break

        if automate["I"][0] in group:
            minimise["I"].append(group)

        for etat in group:
            if etat in automate["F"] and group not in minimise["F"]:
                minimise["F"].append(group)

    return minimise


if __name__ == '__main__':

    import doctest

    # doctest.testmod(verbose=True)
    # doctest.testmod()

    determinisation = {"alphabet":['a','b'],"etats": [1,2,3,4],"transitions":[[1,'a',2],[1,'b',2],[1,'a',3],[2,'b',1],[2,'a',4],[3,'b',4],[4,'b',3],[4,'a',2]],"I":[1,4],"F":[3,4] }

    inter1 = {"alphabet":['a','b'],"etats": [0,1],"transitions":[[0,'a',0],[0,'b',1],[1,'a',1],[1,'b',0]],"I":[0],"F":[0] }

    inter2 = {"alphabet":['a','b'],"etats": [0,1,2],"transitions":[[0,'b',0],[0,'a',1],[1,'b',1],[1,'a',2],[2,'a',0],[1,'a',2],[2,'b',2]],"I":[0],"F":[0] }

    minimisation = {"alphabet":['a','b'],"etats": [1,2,3,4,5,6],"transitions":[[1,'a',2],[1,'b',2],[2,'a',3],[2,'b',4],[3,'a',4],[3,'b',5],[4,'a',3],[4,'b',6],[5,'b',5],[5,'a',6],[6,'a',5],[6,'b',6]],"I":[1],"F":[5,6] }

    print("Determinisation : ", determinise(determinisation))
    print()

    print("Intersection : ", renommage(inter(produit(inter1, inter2)['etats'], produit(inter1, inter2)['transitions'], produit(inter1, inter2)['alphabet'], produit(inter1, inter2)['I'], produit(inter1, inter2)['F1'], produit(inter1, inter2)['F2'])))
    print()

    print("Minimisation : ", renommage(minimise(minimisation)))
    
    