# Version 0.7.0.5

# Ajouts
- Ajout d'un système de déchiffrement et décompression (fonctionnement inverse à `__create_container()`)
- Ajout de l'attribut `self.decompressed_datas_file_name` qui contient le chemin du fichier temporaire des données des fichiers déchiffrés & décompressés

# Modifications
- Les métadonnées `start` et `end` recorrespondent maintenant aux données non chiffrées et non compressées
- Le niveau de compression passe de 9 à 4

# Suppressions
- Suppression de toutes les utilisations de `self.table_length`
- Suppression de la métadonnée `virtual_size`, inutilisée

# Corrections
- Bug qui ajoutait `vdisk.vdcr` dans la liste des fichiers dans `__get_datas()`.
  - `vdisk.vdcr` était créé avant l'exécution de `__get_datas()`, ajoutant le container à la liste de fichier
  - Cet ajout causait un problème dans le calcul de la taille des données des fichiers, empêchant le chargement de la table dans `__load_container()`