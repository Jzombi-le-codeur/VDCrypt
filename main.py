import os
import pathlib
import json
import struct


class VDCrypt:
    def __init__(self):
        self.root = pathlib.Path("F:\\")
        self.datas = bytearray()
        self.table = []  # Voir "test template table.json"
        self.previous_element_end = 0

    def __get_datas(self, path, directories, directory_infos=None):
        # Récupérer les éléments (fichiers et dossiers)
        listdir = os.listdir(path)
        if "System Volume Information" in listdir:
            listdir.remove("System Volume Information")

        # Récupérer uniquement les dossiers
        fileslistdir = listdir.copy()
        for element in fileslistdir:
            element_path = os.path.join(path, element)
            if os.path.isdir(element_path):
                fileslistdir.remove(element)

        # Récupérer les données des fichiers
        for element in listdir:
            # Récupérer le chemin de l'élément (probablement à changer car prend pas en compte sous dossiers jpense)
            element_path = os.path.join(path, element)

            # Vérifier si l'élément est un fichier
            if os.path.isfile(element_path):
                """ RECUPERATION DONNEES FICHIERS """
                # Récupérer le contenu du fichier
                with open(element_path, "rb") as file:
                    file_content = file.read()
                    self.datas.extend(file_content)  # Ajouter les donnés du fichier à la liste des données des fichiers
                    file.close()

                """ CREATION TABLE """
                # Ajouter les métadonnées du fichier
                infos = {}
                infos["name"] = element
                infos["type"] = "file"
                infos["size"] = os.path.getsize(element_path)

                # Définir là où le fichier commence et se termine
                infos["start"] = self.previous_element_end

                infos["end"] = infos["start"] + infos["size"]  # Calculer là où le fichier se termine

                # Mettre à jour la variable contenant le point de fin du précédent
                self.previous_element_end = infos["end"]

                # Mettre à jour la table des fichiers
                if path == self.root:
                    self.table.append(infos)

                else:
                    directory_infos["content"].append(infos)

                # Supprimer le fichier
                os.remove(element_path)

            elif os.path.isdir(element_path):
                # Ajouter les métadonnées du dossier
                infos = {}
                infos["name"] = element
                infos["type"] = "directory"
                infos["content"] = []

                # Mettre à jour la table des fichiers
                if path == self.root:
                    self.table.append(infos)

                else:
                    directory_infos["content"].append(infos)

                # Créer les informations du répertoire pour récupérer ses éléments
                new_directory = directories + [element]

                # Récupérer les éléments du dossier
                self.__get_datas(path=element_path, directories=new_directory, directory_infos=infos)

                # Supprimer le dossier
                os.rmdir(element_path)

    def create_container(self):
        # Récupérer les données des fichiers & créer la table
        self.__get_datas(path=self.root, directories=[self.root])

        # Encoder la table
        table = json.dumps(self.table).encode("utf-8")

        # Récupérer la taille de la table
        table_bytes = len(table)  # Récupérer la taille de la table
        header = struct.pack(">Q", table_bytes)  # Mettre le header en bytes

        """ SAUVEGARDE """
        vd_path = os.path.join(self.root, "vdisk.vdcr")
        with open(vd_path, "wb") as vd_file:
            vd_file.write(header)  # Ecrire le header
            vd_file.write(table)  # Ecrire la table
            vd_file.write(self.datas)  # Ecrire les données des fichiers
            vd_file.close()  # Fermer les fichiers

    def __set_datas(self, path, directory):
        # Parcourir les éléments
        for element in directory:
            # Obtenir le chemin de l'élément
            element_path = os.path.join(path, element["name"])

            # Vérifier que l'élément est un fichier ou un dossier
            if element["type"] == "file":
                # Ecrire le contenu du fichier dans le fichier
                with open(element_path, "wb") as file:
                    # Ecrire du byte de départ au byte de fin
                    file.write(self.datas[element["start"]:element["end"]])
                    file.close()

            elif element["type"] == "directory":
                # Créer le dossier
                os.mkdir(element_path)

                # Créer les éléments du dossier
                self.__set_datas(path=element_path, directory=element["content"])

    def load_container(self):
        """ CHARGEMENT DU FICHIER """
        vd_path = os.path.join(self.root, "vdisk.vdcr")
        with open(vd_path, "rb") as vd_file:
            header = struct.unpack(">Q", vd_file.read(8))[0]
            self.table = vd_file.read(header).decode("utf-8")
            self.table = json.loads(self.table)
            self.datas = vd_file.read()

        """ Création fichiers """
        self.__set_datas(path=self.root, directory=self.table)

        # Supprimer les fichiers de table
        os.remove(vd_path)

    def run(self):
        # self.create_container()
        # self.load_container()


if __name__ == "__main__":
    vdcrypt = VDCrypt()
    vdcrypt.run()