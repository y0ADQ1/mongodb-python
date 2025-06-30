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
        



    @staticmethod
    def actualizar_en_mongo_conexion(filtro, nuevos_datos, db_name, collection_name):

        """
        actualiza un documento en mongo si hay conexion
        el filtro: dict para buscar el documento unico por ej la matricula
        y ya con los nuevos datos: dict con los nuevos valores 
        """
        client = MongoSyncUtils.conectar_mongo()
        if client:
            db = client[db_name]
            coleccion = db[collection_name]

            try: 
                resultado = coleccion.update_one(filtro, {"$set": nuevos_datos})
                if resultado.matched_count:
                    print("Objeto actualizado en Mongo")
                    return True
                else:
                    print("No se encontro el documento para actualizar")
                    return False
            except Exception as e:
                print(f"Error al actualizar en Mongo{e}")
        else:
            print("No hay conexion a Mongo. No se actualizo en Mongo")
            return False



    @staticmethod
    def eliminar_en_mongo_conexion(filtro, db_name, collection_name):
        client = MongoSyncUtils.conectar_mongo()
        if client: 
            db = client[db_name]
            coleccion = db[collection_name]
            try: 
                resultado = coleccion.delete_one(filtro)
                if resultado.deleted_count:
                    print("Objeto eliminado en Mongo")
                    return True
                else:
                    print("No se encontro el documento para eliminar")
                    return False
            except Exception as e:
                print(f"Error al eliminar en Mongo{e}")
                return False
        else:
            print("No hay conexion a Mongo. No se elimino en mongo")
            return False
    


    """
    validacion cuando se quiera agregar, para que no se dupliquen datos
    @staticmethod
    def existe_en_mongo(matricula, db_name, collection_name):
        client = MongoSyncUtils.conectar_mongo()
        if client:
            db = client[db_name]
            coleccion = db[collection_name]
            return coleccion.find_one({"matricula": matricula}) is not None
        return False
    """