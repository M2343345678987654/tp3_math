def calculer_minimum(offre, demande, i, j):
    return min(offre[i], demande[j])
def mettre_a_jour(offre, demande, i, j, allocation):
    offre[i] -= allocation
    demande[j] -= allocation
def coin_nord_ouest(offre, demande):
    i, j = 0, 0
    m, n = len(offre), len(demande)

    allocation = [[0 for _ in range(n)] for _ in range(m)]

    while i < m and j < n:
        x = min(offre[i], demande[j])
        allocation[i][j] = x

        offre[i] -= x
        demande[j] -= x

        if offre[i] == 0:
            i += 1
        elif demande[j] == 0:
            j += 1

    return allocation
def afficher_allocation(allocation, titre):
    print("\n" + "="*40)
    print(titre)
    print("="*40)
    for ligne in allocation:
        print(ligne)


def calculer_cout_total(allocation, couts):
    cout = 0
    for i in range(len(allocation)):
        for j in range(len(allocation[0])):
            cout += allocation[i][j] * couts[i][j]
    return cout
def main_coin_nord_ouest():
    # Coûts
    couts = [
        [7, 12, 1, 5, 9],
        [15, 3, 12, 6, 14],
        [8, 16, 10, 12, 7],
        [18, 8, 17, 11, 16]
    ]

    # Offres et demandes
    offre = [12, 11, 14, 8]
    demande = [10, 11, 15, 5, 4]

    # Copie pour éviter modification
    offre_copy = offre.copy()
    demande_copy = demande.copy()

    allocation = coin_nord_ouest(offre_copy, demande_copy)

    afficher_allocation(allocation, "Allocation - Coin Nord-Ouest")

    cout_total = calculer_cout_total(allocation, couts)
    print("\nCoût total =", cout_total)
if __name__ == "__main__":
    print("\n===== TEST MÉTHODE DU COIN NORD-OUEST =====")
    main_coin_nord_ouest()

