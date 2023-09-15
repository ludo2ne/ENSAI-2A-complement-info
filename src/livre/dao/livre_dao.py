class LivreDao:
    def create(self, livre) -> Livre:
        """Pour créer un livre en base"""
        with DBConnection().connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO livre (isbm, titre, auteur)         "
                    "     VALUES (%(isbm)s, %(titre)s, %(auteur)s)   "
                    "  RETURNING id_livre;                           ",
                    {"isbm": livre.isbm, 
                    "titre": livre.titre, 
                    "auteur": livre.auteur},
                )
                livre.id = cursor.fetchone()["id_livre"]
        return livre 
        
    def find_all(self) -> list[Livre]:
        """Pour récupérer tous les livres en base"""
        with DBConnection().connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id_livre,                  "
                    "       isbm,                      "
                    "       titre,                     "
                    "       auteur                     "
                    "  FROM livre ;                    "
                )
                livre_bdd = cursor.fetchall()
                
        liste_livres = []
    
        if livre_bdd:
            for livre in livre_bdd:
                liste_livres.append(
                    Livre(
                        id=livre["id_livre"],
                        isbm=livre["isbm"],
                        titre=livre["titre"],
                        auteur=livre["auteur"],
                    )
                )
                
        return liste_livres
        
    def find_by_isbm(self, isbm) -> Livre:
        """Pour récupérer un livre depuis son isbm"""
        with DBConnection().connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT *                          "
                    "  FROM livre                      "
                    " WHERE isbm = %(isbm)s            ",
                    {"isbm": livre.isbm}
                livre_bdd = cursor.fetchone()
                
        livre = None
        if livre_bdd:
            livre = Livre(
                id=livre_bdd["id_livre"],
                isbm=livre_bdd["isbm"],
                titre=livre_bdd["titre"],
                auteur=livre_bdd["auteur"],
            )
        return livre     