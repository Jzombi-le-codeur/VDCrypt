# Ajouts
- Ajouts de commentaires sur la partie "directory" de `get_datas()`
- Ajout d'une fonctionnalité pour charger les fichiers du container `load_container()`

# Modifications
- Le type `folder` devient `directory` (cohérence par rapport au code)
- Dans `get_datas()`, `dirname` a été supprimé et `element` est désormais utilisé (comme pour les types `file`)
- Dans `get_datas()` sur la partie directory, suppression de `new_path` car `element_path` existe et fait la même chose