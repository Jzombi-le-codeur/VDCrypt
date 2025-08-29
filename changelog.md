# Version 0.5.0

# Ajouts
- Ajout d'un système qui chiffre & déchiffre le contenu des fichiers un par un
  - Dans `__get_datas()`, les données des fichiers, dès qu'ils sont chiffrées, sont désormais stockés dans l'attribut `crypted_datas`
.

# Modifications
- La méthode `__create_crypted_container_content()` est renommée `__create_container_content()` et ne chiffre plus le container entier

# Suppressions
- Suppression du système qui chiffrait l'ensemble des données des fichiers en une fois
- Suppression de la méthode `__get_clear_container_content()` qui déchiffrait l'ensemble des données des fichiers