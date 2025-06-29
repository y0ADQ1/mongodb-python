from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
connection_string = os.getenv("MONGODB_URI")

client = MongoClient(connection_string)
db = client["python-mongo"]



if __name__ == "__main__":
    try:
        print("Bases de datos disponibles", client.list_database_names())
        print("la conexion si jalo papi")
    except Exception as e:
        print("Error al conectar a mongo: ", e)
