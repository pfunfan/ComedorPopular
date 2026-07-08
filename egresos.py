# Funcion para registrar egresos
def registrar_egreso(conn, cursor):
    # Preguntar datos
    fecha = input("Ingrese fecha (AAAA-MM-DD): \n")
    concepto = input("Ingrese concepto: \n")
    monto = float(input("Ingrese el monto: \n"))
    
    # Tupla para insertar valores a la tabla
    tupla = (fecha, concepto, monto)

    # Insertar valores
    cursor.execute("""INSERT INTO Egresos (fecha, concepto, monto)
         VALUES (?, ?, ?)""", tupla)
    
    # Guardar cambios
    conn.commit()
    
    print("Egreso guardado correctamente\n")

def mostrar_egresos(cursor):
    # Leer datos (Selecciona todos los datos)
    cursor.execute("SELECT * FROM Egresos")
    
    # Ver resultado
    egresos = cursor.fetchall()
    for egreso in egresos:
        print(egreso)

def editar_egreso(conn, cursor):
    id_egreso = int(input("Escriba el ID: \n"))

    # Consultar si el ID existe en la base de datos
    cursor.execute("SELECT * FROM Egresos WHERE id = ?", (id_egreso,)) # (id_egreso,) tupla de un solo elemento
   
    # Guarda en una tupla la primera fila de lo seleccionado por cursor.execute()
    fila = cursor.fetchone()

    # Comprobar si existe el ID ingresado
    if fila is None:
        print(f"No existe el ID = {id_egreso} en la base de datos")
    else:
        print(f"""DATOS ACTUALES: 
              
              Fecha   : {fila[1]}
              Concepto: {fila[2]}
              Monto   : {fila[3]}

              Ingrese los nuevos datos.
              (Presione Enter para conservar el valor actual)
        """)

        # Lógica para guardar o mantener datos
        nueva_fecha = input("Nueva Fecha: \n")
        if nueva_fecha == "":
            nueva_fecha = fila[1]

        nuevo_concepto = input("Nuevo Concepto: \n")
        if nuevo_concepto == "":
            nuevo_concepto = fila[2]
        
        # Cambiar str a float para que no haya errores en los datos
        nuevo_monto = input("Nuevo Monto: \n")
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