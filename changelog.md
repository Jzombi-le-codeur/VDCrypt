# Ajouts
- Création du projet
- Ajout d'un système de sauvegarde/chargement de fichiers
  - Ne fonctionne uniquement sur les fichiers d'un dossier racine
  - Fonctionne à partir d'un système de container en deux fichiers
    - `table.json` : Contient les métadonnées des fichiers
    - `datas` : Contient les données des fichiers (bytes concaténés)