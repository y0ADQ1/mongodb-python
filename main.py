from alumno import Alumno
from maestro import Maestro
from grupo import Grupo
from arreglo import guardar_en_json

alumno1 = Alumno("Juan Antonio", "Deras Duron", "juan@gmail.com", "8714997082", "23170072")
alumno2 = Alumno("Ana", "Perez", "ana@gmail.com", "0987654321", "23170073")
alumno3 = Alumno("Carlos", "Lopez", "carlos@gmail.com", "8714111111", "23170074")

alumno4 = Alumno("Maria", "Gomez", "maria@gmail.com", "8714222222", "23170075")
alumno5 = Alumno("Luis", "Hernandez", "Luis@gmail.com", "8714333333", "23170076")
alumno6 = Alumno("Sofia", "Martinez", "sofia@gmail.com", "8714444444", "23170077")

alumno7 = Alumno("Pedro", "Ramirez", "pedro@gmai.com", "8714555555", "23170078")
alumno8 = Alumno("Laura", "Sanchez", "laura@gmail.com", "8714666666", "23170079")
alumno9 = Alumno("Diego", "Torres", "diego@gmail.com", "8714777777", "23170080")

alumno10 = Alumno("Elena", "Martinez", "elena@gmail.com", "8714888888", "23170081")

maestro1 = Maestro("Luis", "Gomez", "luis@gmail.com", "8714000000", "M12345")
maestro2 = Maestro("Maria", "Sanchez", "maria@gmail.com", "8714111111", "M12346")
maestro3 = Maestro("Pedro", "Ramirez", "pedro@gmail.com", "8714222222", "M12347")

alumnos = Alumno()
alumnos.agregar(alumno1)
alumnos.agregar(alumno2)
alumnos.agregar(alumno3)
alumnos.agregar(alumno4)
alumnos.agregar(alumno5)
alumnos.agregar(alumno6)
alumnos.agregar(alumno7)
alumnos.agregar(alumno8)
alumnos.agregar(alumno9)
alumnos.agregar(alumno10)

maestros = Maestro()
maestros.agregar(maestro1)
maestros.agregar(maestro2)
maestros.agregar(maestro3)

guardar_en_json("alumnos.json", alumnos.to_dict())
guardar_en_json("maestros.json", maestros.to_dict())



grupo1 = Grupo("Grupo 1", "G123", maestro=maestro1, alumnos=alumnos)
grupo2 = Grupo("Grupo 2", "G124", maestro=maestro2, alumnos=[alumno4.to_dict(), alumno5.to_dict(), alumno6.to_dict()])
grupo3 = Grupo("Grupo 3", "G125", maestro=maestro3, alumnos=[alumno7.to_dict(), alumno8.to_dict(), alumno9.to_dict()])

guardar_en_json("grupos.json", [grupo1.to_dict(), grupo2.to_dict(), grupo3.to_dict()])