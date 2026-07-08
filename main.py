from database import *
from ingresos import *
from egresos import *
from pdf import *

# Conectarse a la base de datos
conn, cursor = conectar()

# Crear tabla si no existe
crear_tablas(cursor)

# Menu de opciones y programa
while True:
    print("""
    =========== COMEDOR POPULAR ===========
          
    1. Registrar Ingreso
    2. Registrar Egreso
    3. Mostrar Ingresos
    4. Mostrar Egresos
    5. Editar Ingreso
    6. Editar Egreso
    7. Generar PDF
    8. Salir
    """)

    opcion = int(input("Seleccione una opción: "))

    match opcion:
        case 1:
            registrar_ingreso(conn, cursor)
        case 2:
            registrar_egreso(conn, cursor)
        case 3:
            mostrar_ingresos(cursor)
        case 4:
            mostrar_egresos(cursor)
        case 5:
            editar_ingreso(conn, cursor)
        case 6:
            editar_egreso(conn, cursor)
        case 7:
            month = int(input("Ingrese mes: \n"))
            year = int(input("Ingrese año: \n"))
            generar_pdf(conn, month, year)
        case 8:
            #Cerrar la conexión
            conn.close()
            break
        case _:
            print("Opcion no válida.")

    