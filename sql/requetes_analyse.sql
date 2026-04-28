USE envirotrack;

-- REQUETE 1 : Taux de non-conformite par secteur
SELECT
    e.secteur_activite,
    COUNT(*) AS total_inspections,
    SUM(CASE WHEN i.resultat = 'Non conforme' THEN 1 ELSE 0 END) AS non_conformes,
    ROUND(SUM(CASE WHEN i.resultat = 'Non conforme' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS taux_non_conformite
FROM inspections i
JOIN etablissements e ON i.id_etablissement = e.id_etablissement
GROUP BY e.secteur_activite
ORDER BY taux_non_conformite DESC;

-- REQUETE 2 : Etablissements les plus inspectes
SELECT
    e.nom_etablissement,
    e.region,
    e.niveau_risque,
    COUNT(i.id_inspection) AS nb_inspections,
    SUM(CASE WHEN i.resultat = 'Non conforme' THEN 1 ELSE 0 END) AS nb_non_conformes
FROM etablissements e
JOIN inspections i ON e.id_etablissement = i.id_etablissement
GROUP BY e.id_etablissement
ORDER BY nb_inspections DESC;

-- REQUETE 3 : Total amendes par gravite
SELECT
    gravite,
    COUNT(*) AS nb_infractions,
    SUM(amende_euros) AS total_amendes,
    ROUND(AVG(amende_euros), 0) AS amende_moyenne
FROM infractions
GROUP BY gravite
ORDER BY total_amendes DESC;

-- REQUETE 4 : Budget inspection par region vs nb etablissements
SELECT
    r.region,
    r.nb_etablissements_total,
    r.budget_inspection,
    r.nb_inspecteurs,
    ROUND(r.budget_inspection / r.nb_etablissements_total, 0) AS budget_par_etablissement
FROM regions r
ORDER BY budget_par_etablissement DESC;

-- REQUETE 5 : Infractions non regularisees
SELECT
    e.nom_etablissement,
    e.region,
    inf.type_infraction,
    inf.gravite,
    inf.amende_euros
FROM infractions inf
JOIN inspections i ON inf.id_inspection = i.id_inspection
JOIN etablissements e ON i.id_etablissement = e.id_etablissement
WHERE inf.regularisee = 'Non'
ORDER BY inf.amende_euros DESC;