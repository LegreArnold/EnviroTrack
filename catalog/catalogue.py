# catalog/catalogue.py
# Catalogue de donnees - EnviroTrack DGPR

import pandas as pd
import json

catalogue = [
    {
        "table": "etablissements",
        "colonne": "id_etablissement",
        "nom_complet": "Identifiant etablissement",
        "description": "Identifiant unique de chaque installation classee",
        "type": "Entier",
        "obligatoire": True,
        "regle_qualite": "Doit etre unique et non nul"
    },
    {
        "table": "etablissements",
        "colonne": "nom_etablissement",
        "nom_complet": "Nom de l'etablissement",
        "description": "Denomination officielle de l'installation classee",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Ne doit pas etre vide"
    },
    {
        "table": "etablissements",
        "colonne": "secteur_activite",
        "nom_complet": "Secteur d'activite",
        "description": "Secteur industriel de l'etablissement",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Valeurs autorisees : Petrochimie, Chimie, Elevage, Materiaux, Dechets, Energie, Textile, Extraction"
    },
    {
        "table": "etablissements",
        "colonne": "niveau_risque",
        "nom_complet": "Niveau de risque",
        "description": "Niveau de risque environnemental et technologique de l'etablissement",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Valeurs autorisees : Faible, Moyen, Eleve"
    },
    {
        "table": "etablissements",
        "colonne": "statut",
        "nom_complet": "Statut ICPE",
        "description": "Regime d'autorisation de l'installation classee",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Valeurs autorisees : Autorise, Declare, Enregistre"
    },
    {
        "table": "inspections",
        "colonne": "type_inspection",
        "nom_complet": "Type d'inspection",
        "description": "Nature de la visite d'inspection realisee par l'inspecteur",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Valeurs autorisees : Programmee, Inopinee"
    },
    {
        "table": "inspections",
        "colonne": "resultat",
        "nom_complet": "Resultat de l'inspection",
        "description": "Conclusion de l'inspecteur a l'issue de la visite",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Valeurs autorisees : Conforme, Non conforme"
    },
    {
        "table": "inspections",
        "colonne": "suites_donnees",
        "nom_complet": "Suites donnees",
        "description": "Action administrative engagee suite a l'inspection",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Valeurs autorisees : Aucune, Avertissement, Mise en demeure"
    },
    {
        "table": "infractions",
        "colonne": "gravite",
        "nom_complet": "Gravite de l'infraction",
        "description": "Niveau de gravite de l'infraction constatee",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Valeurs autorisees : Mineure, Moderee, Grave"
    },
    {
        "table": "infractions",
        "colonne": "amende_euros",
        "nom_complet": "Montant de l'amende",
        "description": "Montant de l'amende administrative prononcee en euros",
        "type": "Entier",
        "obligatoire": True,
        "regle_qualite": "Doit etre positif et superieur a 0"
    },
    {
        "table": "infractions",
        "colonne": "regularisee",
        "nom_complet": "Infraction regularisee",
        "description": "Indique si l'etablissement a corrige l'infraction constatee",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Valeurs autorisees : Oui, Non"
    },
    {
        "table": "regions",
        "colonne": "budget_inspection",
        "nom_complet": "Budget d'inspection",
        "description": "Budget annuel alloue a l'inspection des ICPE dans la region en euros",
        "type": "Entier",
        "obligatoire": True,
        "regle_qualite": "Doit etre positif et superieur a 0"
    },
    {
        "table": "regions",
        "colonne": "nb_inspecteurs",
        "nom_complet": "Nombre d'inspecteurs",
        "description": "Nombre d'inspecteurs de l'environnement affectes dans la region",
        "type": "Entier",
        "obligatoire": True,
        "regle_qualite": "Doit etre positif et superieur a 0"
    },
]

df_catalogue = pd.DataFrame(catalogue)

print("=" * 60)
print("CATALOGUE DE DONNEES - EnviroTrack DGPR")
print("=" * 60)
print(df_catalogue[["table", "colonne", "nom_complet", "type", "obligatoire"]].to_string(index=False))

df_catalogue.to_csv("catalog/catalogue.csv", index=False)

with open("catalog/catalogue.json", "w", encoding="utf-8") as f:
    json.dump(catalogue, f, ensure_ascii=False, indent=2)

print("\nCatalogue sauvegarde en CSV et JSON dans catalog/")
print(f"Nombre de colonnes documentees : {len(catalogue)}")