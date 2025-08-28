# Ajouts
- Ajout d'un système de container en un fichier (en `.vdcr`), en 3 parties :
  - **Le header** : contenant la taille de la table de fichiers
  - **La table de fichiers** : toujours au format JSON
  - **Les données des fichiers**
- Ajout d'un système pour créer ce container
- Ajout d'un système pour charger ce container

# Modification
- Modification des noms des méthodes `get_datas()` et `set_datas()` qui deviennent respectivement `__get_datas()` et `__set_datas()` pour signaler le fait qu'elles sont **privées**

# Suppression
- Suppresion de l'ancien système pour créer et charger le container en deux fichiers `table.json` et `datas`
- Les `print()` de debug ont été supprimés