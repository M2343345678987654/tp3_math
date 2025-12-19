import numpy as np

# ---------------------------------------------------------------------
# PARTIE 3 — Fonctions demandées dans le TP
# ---------------------------------------------------------------------

def generate_tabinitial(A, b, c):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    m, n = A.shape
    T = np.zeros((m + 1, n + 1))

    T[:m, :n] = A
    T[:m, n] = b
    T[m, :n] = c
    T[m, n] = 0.0
    return T


def positivite(v):
    v = list(v)
    v_min = min(v)
    idx = v.index(v_min)
    is_positive = all(x >= 0 for x in v)
    return is_positive, v_min, idx


def rapportmin(b, a):
    rapports = []
    for i in range(len(b)):
        if a[i] > 0:
            rapports.append(b[i] / a[i])
        else:
            rapports.append(float('inf'))
    r = rapports.index(min(rapports))
    if rapports[r] == float('inf'):
        return None
    return r


def pivotgauss(T, r, s):
    pivot = T[r][s]
    if abs(pivot) < 1e-12:
        raise ValueError("Pivot nul !")

    T[r, :] /= pivot
    for i in range(len(T)):
        if i != r:
            facteur = T[i][s]
            T[i, :] -= facteur * T[r, :]
    return T


# ---------------------------------------------------------------------
# PARTIE 4 — Algorithme du Simplexe
# ---------------------------------------------------------------------

def simplexe(A, b, c, max_iter=100):
    T = generate_tabinitial(A, b, c)

    m_total, n_total = T.shape
    m = m_total - 1
    n = n_total - 1

    print("\n===== TABLEAU INITIAL =====")
    print(T, "\n")

    for it in range(max_iter):
        couts = list(T[m, :n])
        is_pos, _, _ = positivite(couts)

        print(f"--- ITERATION {it} ---")
        print("Coûts réduits :", couts)

        if is_pos:
            print("Tous les coûts sont positifs → OPTIMALITÉ atteinte.\n")
            break

        s = couts.index(min(couts))

        a_col = T[:m, s]
        b_col = T[:m, n]
        r = rapportmin(b_col, a_col)

        if r is None:
            raise Exception("Problème non borné !")

        print("Colonne pivot =", s)
        print("Ligne pivot =", r)
        print("Pivot =", T[r][s])

        T = pivotgauss(T, r, s)

        print("Tableau après pivot :")
        print(T, "\n")

    # EXTRACTION SOLUTION
    x = np.zeros(n)
    for i in range(m):
        for j in range(n):
            if abs(T[i][j] - 1) < 1e-4 and all(abs(T[k][j]) < 1e-4 for k in range(m) if k != i):
                x[j] = T[i][n]

    z = T[m][n]
    return x, z, T


# ---------------------------------------------------------------------
# PARTIE 5 — INTERFACE UTILISATEUR
# ---------------------------------------------------------------------

	def saisie_interactive():
	    print("=== SIMPLEXE INTERACTIF ===")
	    print("1) Minimisation")
	    print("2) Maximisation")
	    choix = int(input("Choisissez 1 ou 2 : "))

	    # Nombre de variables
	    n = int(input("Nombre de variables de décision ? "))

	    # Fonction objectif
	    print("\n--- Fonction Objectif ---")
	    print("Entrez les coefficients séparés par des espaces :")
	    c = list(map(float, input("c1 c2 ... cn : ").split()))

	    # Conversion maximisation → minimisation
	    if choix == 2:
		c = [-x for x in c]

	    # Contraintes
	    m = int(input("\nNombre de contraintes (<= uniquement) ? "))

	    A = []
	    b = []

	    print("\n--- Contraintes (format : a1 a2 ... an b) ---")
	    for i in range(m):
		vals = list(map(float, input(f"Contrainte {i+1} : ").split()))
		A.append(vals[:n])    # coefficients
		b.append(vals[n])    # second membre

	    # Ajout variables d'écart
	    for i in range(m):
		slack = [0] * m
		slack[i] = 1
		A[i] += slack

	    c += [0] * m

	    # 👉 Correction : on retourne bien 4 valeurs
	    return A, b, c, choix



# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------

if __name__ == "__main__":
    A, b, c, choix = saisie_interactive()

    x, z, T = simplexe(A, b, c)

    print("===== SOLUTION =====")
    print("x* =", x)
    print("z* =", z)
    print("Tableau final :\n", T)
