# Funcion para registrar egresos
def registrar_egreso(conn, cursor):
    # Preguntar datos
    fecha = input("Ingrese fecha (AAAA-MM-DD): ")
    concepto = input("Ingrese concepto: ")
    monto = float(input("Ingrese el monto: "))
    
    # Tupla para insertar valores a la tabla
    egreso = (fecha, concepto, monto)

    # Insertar valores
    cursor.execute("""INSERT INTO Egresos (fecha, concepto, monto)
         VALUES (?, ?, ?)""", egreso)
    
    # Guardar cambios
    conn.commit()
    
    print("Egreso guardado correctamente.\n")

def mostrar_egresos(cursor):
    # Leer datos (Selecciona todos los datos)
    cursor.execute("SELECT * FROM Egresos")
    
    # Ver resultado
    egresos = cursor.fetchall()
    for egreso in egresos:
        print(egreso)

def editar_egreso(conn, cursor):
    id_egreso = int(input("Escriba el ID: "))

    # Consultar si el ID existe en la base de datos
    cursor.execute("SELECT * FROM Egresos WHERE id = ?", (id_egreso,)) # (id_egreso,) tupla de un solo elemento
   
    # Guarda en una tupla la primera fila de lo seleccionado por cursor.execute()
    fila = cursor.fetchone()

    # Comprobar si existe el ID ingresado
    if fila is None:
        print(f"No existe el ID = {id_egreso} en la base de datos")
    else:
        print(f"""
                DATOS ACTUALES: 
              
        Fecha   : {fila[1]}
        Concepto: {fila[2]}
        Monto   : {fila[3]}

        Ingrese los nuevos datos.
        (Presione Enter para conservar el valor actual)
        """)

        # Lógica para guardar o mantener datos
        nueva_fecha = input("Nueva Fecha: ")
        if nueva_fecha == "":
            nueva_fecha = fila[1]

        nuevo_concepto = input("Nuevo Concepto: ")
        if nuevo_concepto == "":
            nuevo_concepto = fila[2]
        
        # Cambiar str a float para que no haya errores en los datos
        nuevo_monto = input("Nuevo Monto: ")
        if nuevo_monto == "":
            nuevo_monto = fila[3]
        else:
            nuevo_monto = float(nuevo_monto)

        # Tupla creada para pasarle al cursor y almacenar los nuevos datos
        datos_actualizados = (nueva_fecha, nuevo_concepto, nuevo_monto, id_egreso)

        # Actualizar Egresos
        cursor.execute("""UPDATE Egresos 
                       SET 
                        fecha = ?, 
                        concepto = ?,
                        monto = ?
                        WHERE id = ?
                       """, datos_actualizados)
        
        #Guardar cambios
        conn.commit()
        print("Egreso actualizado correctamente.\n")

def eliminar_egreso(conn, cursor):
    id_egreso = int(input("Ingrese el ID: "))

    # Consultar si el ID existe en la Base de datos
    cursor.execute("SELECT * FROM Egresos WHERE id = ?", (id_egreso,))

    # Guardar la fila seleccionada en el cursor
    fila = cursor.fetchone()

    # Comprobar si existe el ID en la base de datos
    if fila is None:
        print(f"No existe el ID = {id_egreso} en la base de datos.\n")
    else:
        # Mostrar registro
        print(f"""
                DATOS ACTUALES:
                     
        Fecha   : {fila[1]}
        Concepto: {fila[2]}
        Monto   : {fila[3]}
        """)

        # Confirmar para eliminar y opciones
        confirmacion = int(input("¿Esta seguro de eliminar el egreso en pantalla? (1.Si  2.No): "))
        if confirmacion == 1:
            cursor.execute("DELETE FROM Egresos WHERE id = ?", (id_egreso,))
            # Guardar cambios
            conn.commit()
            print("Listo. Egreso eliminado correctamente.\n")
        elif confirmacion == 2:
            print("Ok. Redirigiendo al menu.\n")
        else:
            print("Error: redirigiendo al menu.\n")  