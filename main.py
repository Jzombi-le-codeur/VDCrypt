import os
import pathlib
import json
import struct
import sys
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import psutil
import base64
import tempfile
import zstandard


class VDCrypt:
    def __init__(self):
        self.format = "vdscc"
        self.root = pathlib.Path("F:\\")
        self.key_file_location = "."
        self.key = None
        self.nonce = None
        self.cipher = None
        self.__get_key()  # Charger la clés
        self.usable_ram = 0
        self.cctx = zstandard.ZstdCompressor(level=9)
        self.dctx = zstandard.ZstdDecompressor()
        self.vd_path = os.path.join(self.root, "vdisk.vdcr")
        self.header = None
        self.datas = bytearray()
        self.crypted_datas = bytearray()
        self.table = []  # Voir "test template table.json"
        self.virtual_files_size = 0
        self.previous_element_end = 0
        self.container_content = bytearray()

    def __get_key(self):
        # Vérifier si la clé a été chargée
        if self.key is None:
            # Vérifier si la clé existe ou non
            key_file_path = os.path.join(self.key_file_location, "key.json")
            if os.path.exists(key_file_path):
                # Charger le fichier contenant la clé
                with open("key.json", "r") as key_file:
                    key_file_content = json.load(key_file)

                # Récupérer la clé
                self.key = base64.b64decode(key_file_content["key"].encode("utf-8"))
                self.nonce = base64.b64decode(key_file_content["nonce"].encode("utf-8"))

            else:
                # Générer la clé & le nonce
                self.key = get_random_bytes(16)
                self.nonce = get_random_bytes(8)

                # Sauvegarder la clé
                with open(key_file_path, "w") as key_file:
                    key_file_content = {
                        "key": base64.b64encode(self.key).decode("utf-8"),
                        "nonce": base64.b64encode(self.nonce).decode("utf-8")
                    }
                    json.dump(key_file_content, key_file)

        self.cipher = AES.new(self.key, AES.MODE_CTR, nonce=self.nonce)

    def __get_avaiable_ram(self):
        # Obtenir la RAM disponible
        avaiable_ram = psutil.virtual_memory().available

        # Calculer la RAM utilisable
        ram_limit_go = 1*1024**3  # Limite de RAM en GO
        if avaiable_ram < ram_limit_go:
            raise MemoryError("Pas assez de mémoire pour compresser/chiffrer le fichier")

        else:
            self.usable_ram = avaiable_ram - ram_limit_go

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
                """ CREATION TABLE """
                # Ajouter les métadonnées du fichier
                infos = {}
                infos["name"] = element
                infos["type"] = "file"
                infos["size"] = os.path.getsize(element_path)

                """ RECUPERATION DONNEES FICHIERS """
                # Récupérer le contenu du fichier

                # COMPRESSION DONNÉES
                with open(element_path, "rb") as file:
                    with tempfile.NamedTemporaryFile(dir=self.root, delete=False, mode="wb") as temp_data_file:
                        temp_data_file_name = temp_data_file.name  # Récupérer le nom du fichier temporaire

                        # Compresser le fichier par chunks
                        with self.cctx.stream_writer(temp_data_file) as compressor:
                            while True:
                                # Obtenir la RAM dispo pour récupérer un chunk de sa taille
                                try:
                                    self.__get_avaiable_ram()

                                except MemoryError as e:
                                    print(e)
                                    sys.exit()

                                # Récupérer un chunk
                                file_chunk = file.read(self.usable_ram)

                                # Arrêter la compression si tout le fichier a été compressé
                                if not file_chunk:
                                    break

                                # Compresser les données et les écrire
                                compressor.write(file_chunk)

                # Supprimer le fichier original
                os.remove(element_path)

                # CHIFFRAGE DONNÉES
                virtual_file_size = 0
                with open(temp_data_file_name, "rb") as temp_data_file:
                    with open(self.vd_path, "ab") as temp_datas_file:
                        while True:
                            # Obtenir la RAM dispo pour récupérer un chunk de sa taille
                            try:
                                self.__get_avaiable_ram()

                            except MemoryError as e:
                                print(e)
                                sys.exit()

                            # Récupérer un chunk
                            file_chunk = temp_data_file.read(self.usable_ram)

                            # Arrêter le chiffrage si tout le fichier a été chiffré
                            if not file_chunk:
                                break

                            # Chiffrer le chunk & écrire dans datas
                            crypted_data = self.cipher.encrypt(file_chunk)
                            virtual_file_size += len(crypted_data)  # Ajouter la taille du chunk à la taille du fichier
                            # conteneurisé
                            temp_datas_file.write(crypted_data)

                self.virtual_files_size += virtual_file_size  # Ajouter la taille du fichier traîté à l'ensemble
                os.remove(temp_data_file_name)  # Supprimer le fichier temporaire

                """ Ajouts infos données à la table """
                # Connaître la taille des données du fichier conteneurisé
                infos["virtual_size"] = virtual_file_size

                # Définir là où le fichier commence et se termine (version claire et chiffrée)
                infos["start"] = self.previous_element_end

                infos["end"] = infos["start"] + infos["virtual_size"]  # Calculer là où le fichier se termine

                # Mettre à jour la variable contenant le point de fin du précédent
                self.previous_element_end = infos["end"]

                # Mettre à jour la table des fichiers
                if path == self.root:
                    self.table.append(infos)

                else:
                    directory_infos["content"].append(infos)

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

    def __allocate_header(self):
        with open(self.vd_path, "wb") as virtual_disk_file:
            temp_header = struct.pack("14s", b"\x00" * 14)
            virtual_disk_file.write(temp_header)

    def __create_header(self):
        # Packer le format du container (en 6 octets) + la table (en 8 octets)
        self.header = struct.pack(">6sQ", self.format.encode("utf-8"), self.virtual_files_size)

    def create_container(self):
        # Allouer de l'espace pour le header
        self.__allocate_header()

        # Récupérer les données des fichiers & créer la table
        self.__get_datas(path=self.root, directories=[self.root])

        # Encoder la table
        self.table = json.dumps(self.table).encode("utf-8")

        # Créer le header
        self.__create_header()

        """ SAUVEGARDE """
        with open(self.vd_path, "r+b") as vd_file:
            # Sauvegarder le header
            vd_file.seek(0)
            vd_file.write(self.header)
            vd_file.seek(0, os.SEEK_END)
            vd_file.write(self.table)

    def __get_header(self):
        # Unpacker le header
        unpacked_header = struct.unpack(">6sQ", self.header)

        # Récupérer le format
        self.format = unpacked_header[0]  # Récupérer le format "binarisé"
        self.format = self.format.split(b"\x00")  # Supprimer le padding
        self.format = self.format[0].decode("utf-8")  # Récupérer le format

        # Récupérer la taille de la table
        self.table_length = unpacked_header[1]

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
                    decrypted_file_content = self.cipher.decrypt(
                        self.datas[element["crypted_start"]:element["crypted_end"]]
                    )
                    file.write(decrypted_file_content)

            elif element["type"] == "directory":
                # Créer le dossier
                os.mkdir(element_path)

                # Créer les éléments du dossier
                self.__set_datas(path=element_path, directory=element["content"])

    def load_container(self):
        """ CHARGEMENT DU FICHIER """
        with open(self.vd_path, "rb") as vd_file:
            self.header = vd_file.read(14)  # Récupérer le header packé
            self.__get_header()  # Récupérer le header, le format et la longueur de la table
            self.table = vd_file.read(self.table_length).decode("utf-8")  # Récupérer la table
            self.table = json.loads(self.table)  # Avoir le bon format de la table
            self.datas = vd_file.read()  # Récupérer les données des fichiers

        """ Création fichiers """
        self.__set_datas(path=self.root, directory=self.table)  # Recréer les fichiers et dossiers

        # Supprimer les fichiers de table
        os.remove(self.vd_path)

    def run(self):
        self.create_container()
        # self.load_container()


if __name__ == "__main__":
    vdcrypt = VDCrypt()
    vdcrypt.run()