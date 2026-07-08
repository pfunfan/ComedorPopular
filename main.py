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
          
    1. Ingresos
    2. Egresos
    3. Generar reporte mensual (PDF)
    0. Salir
    """)

    opcion_main = int(input("Seleccione una opción: "))

    if opcion_main == 1:
        print("""
        ========= INGRESOS =========

        1. Registrar ingreso
        2. Mostrar ingresos
        3. Editar ingreso
        4. Eliminar ingreso
        0. Volver
        """)

        opcion_ingresos = int(input("Seleccione una opción: "))

        if opcion_ingresos == 1:
            registrar_ingreso(conn, cursor)
        elif opcion_ingresos == 2:
            mostrar_ingresos(cursor)
        elif opcion_ingresos == 3:
            editar_ingreso(conn, cursor)
        elif opcion_ingresos == 4:
            eliminar_ingreso(conn, cursor)
        elif opcion_ingresos == 0:
            pass # No hace nada y regresa al menú de arriba automáticamente
        else:
            print("Opción no válida. Intente de nuevo.")
    elif opcion_main == 2:
        print("""
        ========= EGRESOS =========

        1. Registrar egreso
        2. Mostrar egresos
        3. Editar egreso
        4. Eliminar egreso
        0. Volver""")

        opcion_egresos = int(input("Seleccione una opción: "))

        if opcion_egresos == 1:
            registrar_egreso(conn, cursor)
        elif opcion_egresos == 2:
            mostrar_egresos(cursor)
        elif opcion_egresos == 3:
            editar_egreso(conn, cursor)
        elif opcion_egresos == 4:
            eliminar_egreso(conn, cursor)
        elif opcion_egresos == 0:
            pass # No hace nada y regresa al menú de arriba automáticamente
        else:
            print("Opción no válida. Intente de nuevo.")
    elif opcion_main == 3:
        month = int(input("Ingrese mes: "))
        year = int(input("Ingrese año: "))
        generar_pdf(conn, month, year)
    elif opcion_main == 0:
        conn.close()
        break
    else:
        print("Opcion no válida. Intente de nuevo.")

    