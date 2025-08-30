# Version 0.7.0.1

# Ajouts
- Ajout de la librairie `pycryptodome` pour le chiffrage chunk par chunk des fichiers
- Ajout de `self.nonce` qui stocke le nonce

# Modifications
- Remplacement des méthodes de chiffrage de `cryptography` par celles de `pycryptodome`
- `self.f` est renommé `self.cipher`

# Suppressions
- Suppression de la librairie `cryptography`, remplacée par `pycryptodome`