/*********************************************
 * OPL 22.1.1.0 Model
 * Author: perso
 * Creation Date: 17 nov. 2025 at 15:32:58
 *********************************************/
/***** transport1.mod *****/

/* Ensembles */
{string} Entrepots = ...;     // E1..E4
{string} Clients   = ...;     // C1..C4

/* Paramètres */
float c[Entrepots][Clients] = ...;   // coût de transport
float dispo[Entrepots] = ...;        // disponibilité des entrepôts
float demande[Clients] = ...;        // demande des clients

/* Variables : quantité envoyée de entrepôt i vers client j */
dvar float+ x[Entrepots][Clients];

/* Objectif : minimiser le coût total de transport */
minimize
   sum(i in Entrepots, j in Clients)
      c[i][j] * x[i][j];

/* Contraintes */
subject to {

   // 1. Chaque entrepôt respecte sa disponibilité
   forall(i in Entrepots)
      sum(j in Clients) x[i][j] <= dispo[i];

   // 2. Chaque client doit recevoir toute sa demande
   forall(j in Clients)
      sum(i in Entrepots) x[i][j] >= demande[j];

}
