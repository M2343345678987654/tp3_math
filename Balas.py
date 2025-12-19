import math

def calculer_differences(couts, offre, demande, lignes_actives, colonnes_actives):
    m, n = len(offre), len(demande)
    diff_lignes = [-1] * m
    diff_colonnes = [-1] * n

    for i in range(m):
        if lignes_actives[i]:
            valeurs = [couts[i][j] for j in range(n) if colonnes_actives[j]]
            if len(valeurs) >= 2:
                valeurs.sort()
                diff_lignes[i] = valeurs[1] - valeurs[0]
            elif len(valeurs) == 1:
                diff_lignes[i] = math.inf

    for j in range(n):
        if colonnes_actives[j]:
            valeurs = [couts[i][j] for i in range(m) if lignes_actives[i]]
            if len(valeurs) >= 2:
                valeurs.sort()
                diff_colonnes[j] = valeurs[1] - valeurs[0]
            elif len(valeurs) == 1:
                diff_colonnes[j] = math.inf

    return diff_lignes, diff_colonnes

def afficher_allocation(allocation, titre):
    print("\n" + "=" * 40)
    print(titre)
    print("=" * 40)
    for ligne in allocation:
        print(ligne)
def trouver_position_optimale(couts, diff_lignes, diff_colonnes, lignes_actives, colonnes_actives):
    if max(diff_colonnes) >= max(diff_lignes):  # ← ICI LA CLÉ
        j = diff_colonnes.index(max(diff_colonnes))
        i = min(
            [i for i in range(len(lignes_actives)) if lignes_actives[i]],
            key=lambda i: couts[i][j]
        )
    else:
        i = diff_lignes.index(max(diff_lignes))
        j = min(
            [j for j in range(len(colonnes_actives)) if colonnes_actives[j]],
            key=lambda j: couts[i][j]
        )
    return i, j


def mettre_a_jour(offre, demande, i, j, allocation):
    offre[i] -= allocation
    demande[j] -= allocation
def balas_hammer(offre, demande, couts):
    m, n = len(offre), len(demande)
    allocation = [[0]*n for _ in range(m)]

    lignes_actives = [True]*m
    colonnes_actives = [True]*n

    while any(lignes_actives) and any(colonnes_actives):

        diff_l, diff_c = calculer_differences(
            couts, offre, demande, lignes_actives, colonnes_actives
        )

        i, j = trouver_position_optimale(
            couts, diff_l, diff_c, lignes_actives, colonnes_actives
        )

        x = min(offre[i], demande[j])
        allocation[i][j] = x

        offre[i] -= x
        demande[j] -= x

        if offre[i] == 0:
            lignes_actives[i] = False
        if demande[j] == 0:
            colonnes_actives[j] = False

    return allocation

def calculer_cout_total(allocation, couts):
    cout = 0
    for i in range(len(allocation)):
        for j in range(len(allocation[0])):
            cout += allocation[i][j] * couts[i][j]
    return cout

def main_balas_hammer():
    couts = [
        [3, 6, 4, 8],
        [3, 4, 7, 9],
        [9, 4, 5, 6]
    ]

    offre = [20, 17, 13]
    demande = [12, 10, 15, 13]

    offre_copy = offre.copy()
    demande_copy = demande.copy()

    allocation = balas_hammer(offre_copy, demande_copy, couts)

    afficher_allocation(allocation, "Allocation - Balas Hammer")

    cout_total = calculer_cout_total(allocation, couts)
    print("\nCoût total =", cout_total)
if __name__ == "__main__":
    print("\n\n===== TEST MÉTHODE DE BALAS-HAMMER =====")
    main_balas_hammer()
