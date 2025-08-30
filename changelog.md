# Version 0.7.0.2

# Ajouts
- Ajout d'un système de compression des données du fichier chunk par chunk avant son chiffrage
- Ajout d'un système de chiffrage se faisant *chunk par chunk* sur les données compressées

# Modifications
- L'ordre des éléments dans le container est maintenant `[header][datas][table]`.  
Ainsi :
  - Le header n'est plus composé de la taille de la table mais de celle de l'ensemble des données des fichiers containeurisées
- `__get_avaible_ram()` renvoie maintenant une erreur s'il n'y a pas assez de RAM
- `self.previous_element_end` contient maintenant la position de la fin du fichier compressé et chiffré
- Les métadonnées `start` et `end` contiennent maintenant respectivement les positions du début et de la fin du fichier compressé et chiffré
- La métadonnée `crypted_size` est renommé `infos["virtual_size"]`

# Suppressions
- Suppression de l'ancien système de chiffrage qui opérait en une fois sur le fichier entier
- Suppression de la méthode `__create_container_content()`
- Supression des métadonnées `crypted_start` et `crypted_end`
- Suppression de l'attribut `self.previous_crypted_element_end`
- Suppression de `self.table_length`
- Suppression des `close()` après utilisation des fichiers (les `with` ferment déjà le fichier)