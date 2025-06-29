import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

class MongoSyncUtils:
    @staticmethod
    def conectar_mongo():
        load_dotenv()
        connection_string = os.getenv("MONGODB_URI")
        try:
            client = MongoClient(connection_string, serverSelectionTimeoutMS=2000)
            client.admin.command('ping')
            return client
        except Exception:
            return None

    @staticmethod
    def cargar_offline(archivo, clase):
        if os.path.exists(archivo):
            with open(archivo, "r") as f:
                data = json.load(f)
                arreglo = clase()
                for item in data:
                    obj = clase(**item)
                    arreglo.agregar(obj)
                return arreglo
        return clase()

    @staticmethod
    def guardar_offline(arreglo, archivo):
        with open(archivo, "w") as f:
            json.dump([a.to_dict() for a in arreglo.items], f, indent=4)

    @staticmethod
    def sincronizar_offline(arreglo, db_name, collection_name, archivo):
        client = MongoSyncUtils.conectar_mongo()
        if client and arreglo.items:
            db = client[db_name]
            coleccion = db[collection_name]
            try:
                datos = [a.to_dict() for a in arreglo.items]
                coleccion.insert_many(datos)
                print(f"✅ Sincronizados {len(datos)} registros offline con MongoDB.")
                arreglo.items.clear()
                MongoSyncUtils.guardar_offline(arreglo, archivo)
            except Exception as e:
                print(f"❌ Error al sincronizar: {e}")
        elif not client:
            print("⚠ No hay conexión a MongoDB. No se pudo sincronizar.")

    @staticmethod
    def guardar_en_mongo_conexion(objeto, db_name, collection_name):
        client = MongoSyncUtils.conectar_mongo()
        if client:
            db = client[db_name]
            coleccion = db[collection_name]
            try:
                coleccion.insert_one(objeto.to_dict())
                print("Objeto guardado en Mongo")
                return True
            except Exception as e:
                print(f"Error al guardar en Mongo: {e}")
                return False
        else:
            print("No hay conexion a Mongo, no se guardo en Mongo")
            return False