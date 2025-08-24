import os
import pathlib
import json


class VDCrypt:
    def __init__(self):
        self.root = pathlib.Path("F:\\")
        self.datas = bytearray()
        self.table = []  # Voir "test template table.json"
        self.previous_element_end = 0

    def get_folders(self, path, directories):
        # Récupérer les fichiers
        listdir = os.listdir(path)
        if "System Volume Information" in listdir:
            listdir.remove("System Volume Information")

        # Récupérer les données des fichiers
        for element in listdir:
            # Récupérer le chemin de l'élément (probablement à changer car prend pas en compte sous dossiers jpense)
            element_path = os.path.join(path, element)
            print(f"Element path : {element_path}")

            # Vérifier si l'élément est un fichier
            if os.path.isfile(element_path):
                """ RECUPERATION DONNEES FICHIERS """
                # Récupérer le contenu du fichier
                with open(element_path, "rb") as file:
                    file_content = file.read()
                    self.datas.extend(file_content)  # Ajouter les donnés du fichier à la liste des données des fichiers
                    file.close()

                print(self.datas)

                """ CREATION TABLE """
                # Ajouter le fichier dans la table
                infos = {}
                infos["name"] = element
                infos["type"] = "file"
                infos["size"] = os.path.getsize(element_path)

                # Définir là où le fichier commence et se termine
                if listdir[0] == element:
                    infos["start"] = 0  # Si le fichier est le premier, il commence à 0

                else:
                    # Sinon il commence là où le fichier précédent s'est arrêté
                    infos["start"] = self.previous_element_end

                infos["end"] = infos["start"] + infos["size"]  # Calculer là où le fichier se termine

                # Mettre à jour la variable contenant le point de fin du précédent
                self.previous_element_end = infos["end"]
                print(infos)

                # Mettre à jour la table des fichiers
                self.table.append(infos)
                print(self.table)

                # Supprimer les fichiers
                os.remove(element_path)

    def create_container(self):
        self.get_folders(path=self.root, directories=[self.root])

        """ SAUVEGARDE """
        # Sauver les données des fichiers
        datas_path = os.path.join(self.root, "datas")
        with open(datas_path, "wb") as datas_file:
            datas_file.write(self.datas)
            datas_file.close()

        # Sauvegarder la table de fichiers
        table_path = os.path.join(self.root, "table.json")
        with open(table_path, "w") as table_file:
            json.dump(self.table, table_file)
            table_file.close()

    def load_container(self):
        """ CHARGEMENT DES FICHIERS DE DONNEES """
        # Charger les données
        datas_path = os.path.join(self.root, "datas")
        with open(datas_path, "rb") as datas_file:
            self.datas = datas_file.read()
            datas_file.close()
            print(self.datas)

        # Charger la table
        table_path = os.path.join(self.root, "table.json")
        with open(table_path, "r") as table_file:
            self.table = json.load(table_file)
            table_file.close()
            print(self.table)

        """ Création fichiers """
        # Parcourir chaque élément
        for element in self.table:
            path = os.path.join(self.root, element["name"])
            # Vérifier que l'élément est un fichier
            if element["type"] == "file":
                # Ecrire le contenu du fichier dans le fichier
                with open(path, "wb") as file:
                    # Ecrire du byte de départ au byte de fin
                    file.write(self.datas[element["start"]:element["end"]])
                    file.close()

        # Supprimer les fichiers de table
        os.remove(datas_path)
        os.remove(table_path)

    def run(self):
        self.create_container()
        # self.load_container()


if __name__ == "__main__":
    vdcrypt = VDCrypt()
    vdcrypt.run()
