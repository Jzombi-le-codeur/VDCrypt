# Ajouts
- Ajout d'un système de chiffrage du contenu du container (non sécurisé & non optimisé) :
  - La clé est stockée dans un fichier `key.json` en clair
- Ajout de la méthode `__create_crypted_container_content()` qui permet de créer et chiffrer le contenu du container
- Ajout de la méthode `__get_clear_container_content()` qui permet de charger et déchiffrer le contenu du container
  - Fonctionne actuellement en déchiffrant le contenu entier du container puis en réécrivant le contenu déchiffré dans le container
- Ajout d'un `requirements.txt` (la bibliothèque `cryptography`ayant été ajoutée)