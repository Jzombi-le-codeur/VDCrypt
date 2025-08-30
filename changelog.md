# Version 0.7.0.3

# Corrections
- Correction d'un bug majeur, dû au fait que `self.virtual_file_size` qui stockait la taille d'UN fichier était utilisé dans le header pour indiquer la taille de TOUS les fichiers containeurisés
  - Création d'une variable locale `virtual_file_size` pour récupérer la valeur d'un fichier
  - Renommage de `self.virtual_file_size` en `self.virtual_files_size`, qui enregistre la taille de TOUS les fichiers par incrémentation
- Note : la méthode pour charger le container n'a pas encore été mise à jour : il y a donc des incohérences avec le code de création du container