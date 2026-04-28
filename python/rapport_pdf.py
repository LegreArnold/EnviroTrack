# python/rapport_pdf.py
# Generation automatique d'un rapport PDF mensuel - EnviroTrack DGPR

import mysql.connector
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import cm
from datetime import datetime

# --- CONNEXION MYSQL ---
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bedel000",  
    database="envirotrack"
)
cursor = conn.cursor()

# --- DONNEES ---

# Statistiques generales
cursor.execute("SELECT COUNT(*) FROM etablissements")
nb_etablissements = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM inspections")
nb_inspections = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM inspections WHERE resultat = 'Non conforme'")
nb_non_conformes = cursor.fetchone()[0]

cursor.execute("SELECT SUM(amende_euros) FROM infractions")
total_amendes = cursor.fetchone()[0]

# Taux non-conformite par secteur
cursor.execute("""
    SELECT
        e.secteur_activite,
        COUNT(*) AS total,
        SUM(CASE WHEN i.resultat = 'Non conforme' THEN 1 ELSE 0 END) AS non_conformes,
        ROUND(SUM(CASE WHEN i.resultat = 'Non conforme' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS taux
    FROM inspections i
    JOIN etablissements e ON i.id_etablissement = e.id_etablissement
    GROUP BY e.secteur_activite
    ORDER BY taux DESC
""")
secteurs = cursor.fetchall()

# Infractions non regularisees
cursor.execute("""
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
    ORDER BY inf.amende_euros DESC
""")
infractions = cursor.fetchall()

conn.close()

# --- GENERATION PDF ---
date_rapport = datetime.now().strftime("%B %Y")
nom_fichier = f"reports/rapport_inspection_{datetime.now().strftime('%Y_%m')}.pdf"

doc = SimpleDocTemplate(
    nom_fichier,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm
)

styles = getSampleStyleSheet()
elements = []

# Titre
titre_style = ParagraphStyle(
    "titre",
    fontSize=18,
    fontName="Helvetica-Bold",
    textColor=colors.HexColor("#1a5276"),
    spaceAfter=10
)
sous_titre_style = ParagraphStyle(
    "sous_titre",
    fontSize=11,
    fontName="Helvetica",
    textColor=colors.grey,
    spaceAfter=20
)
section_style = ParagraphStyle(
    "section",
    fontSize=13,
    fontName="Helvetica-Bold",
    textColor=colors.HexColor("#1a5276"),
    spaceBefore=15,
    spaceAfter=8
)

elements.append(Paragraph("DGPR - Direction Generale de la Prevention des Risques", sous_titre_style))
elements.append(Paragraph("Rapport mensuel de l'inspection des ICPE", titre_style))
elements.append(Paragraph(f"Periode : {date_rapport}", sous_titre_style))
elements.append(Spacer(1, 0.5*cm))

# KPIs generaux
elements.append(Paragraph("1. Indicateurs cles", section_style))

kpi_data = [
    ["Indicateur", "Valeur"],
    ["Etablissements suivis", str(nb_etablissements)],
    ["Inspections realisees", str(nb_inspections)],
    ["Non-conformites detectees", str(nb_non_conformes)],
    ["Taux de non-conformite", f"{round(nb_non_conformes/nb_inspections*100, 1)} %"],
    ["Total amendes prononcees", f"{total_amendes:,} euros"],
]

kpi_table = Table(kpi_data, colWidths=[10*cm, 6*cm])
kpi_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a5276")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#d6eaf8")]),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("PADDING", (0, 0), (-1, -1), 8),
]))
elements.append(kpi_table)
elements.append(Spacer(1, 0.5*cm))

# Non-conformite par secteur
elements.append(Paragraph("2. Taux de non-conformite par secteur", section_style))

secteur_data = [["Secteur", "Inspections", "Non conformes", "Taux (%)"]]
for row in secteurs:
    secteur_data.append([row[0], str(row[1]), str(row[2]), f"{row[3]} %"])

secteur_table = Table(secteur_data, colWidths=[6*cm, 4*cm, 4*cm, 3*cm])
secteur_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a5276")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#d6eaf8")]),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("PADDING", (0, 0), (-1, -1), 8),
]))
elements.append(secteur_table)
elements.append(Spacer(1, 0.5*cm))

# Infractions non regularisees
elements.append(Paragraph("3. Infractions non regularisees - Actions requises", section_style))

infraction_data = [["Etablissement", "Region", "Infraction", "Gravite", "Amende"]]
for row in infractions:
    infraction_data.append([row[0], row[1], row[2], row[3], f"{row[4]:,} euros"])

infraction_table = Table(infraction_data, colWidths=[4*cm, 3.5*cm, 4.5*cm, 2.5*cm, 2.5*cm])
infraction_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#922b21")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fadbd8")]),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("PADDING", (0, 0), (-1, -1), 6),
]))
elements.append(infraction_table)
elements.append(Spacer(1, 0.5*cm))

# Pied de page
elements.append(Paragraph(
    f"Rapport genere automatiquement le {datetime.now().strftime('%d/%m/%Y a %H:%M')} - EnviroTrack DGPR",
    sous_titre_style
))

doc.build(elements)
print(f"Rapport PDF genere : {nom_fichier}")