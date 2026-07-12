from funciones_auxiliares import *

# Registra un nuevo egreso en la base de datos.
# Solicita los datos al usuario, valida el monto y guarda el registro.
def registrar_egreso(conn, cursor):
    # Solicitar información del egreso
    fecha = input("Ingrese fecha (AAAA-MM-DD): ")
    concepto = input("Ingrese concepto: ")
    monto = pedir_monto("Ingrese el monto: ")
    
    # Agrupar los datos en una tupla para enviarlos a la consulta SQL
    datos_egreso = (fecha, concepto, monto)

    # Insertar el nuevo egreso en la tabla Egresos
    cursor.execute("""INSERT INTO Egresos (fecha, concepto, monto)
         VALUES (?, ?, ?)""", datos_egreso)
    
    # Confirmar los cambios realizados en la base de datos
    conn.commit()
    
    print("Egreso guardado correctamente.\n")

# Muestra todos los egresos registrados en la base de datos.
def mostrar_egresos(cursor):
    # Obtener todos los registros de la tabla Egresos
    cursor.execute("SELECT * FROM Egresos")
    
    # Guardar los resultados obtenidos y mostrarlos
    egresos = cursor.fetchall()
    for egreso in egresos:
        print(egreso)

# Edita un egreso existente mediante su ID.
# Permite conservar los valores actuales dejando campos vacíos.
def editar_egreso(conn, cursor):
    # Solicitar el ID del egreso que se desea modificar
    id_egreso = pedir_entero("Escriba el ID: ")

    # Buscar el egreso seleccionado en la base de datos
    cursor.execute("SELECT * FROM Egresos WHERE id = ?", (id_egreso,))
   
    # Obtener la primera fila encontrada
    fila = cursor.fetchone()

    # Verificar si existe el registro solicitado
    if fila is None:
        print(f"No existe el ID = {id_egreso} en la base de datos")
    else:
        print(f"""
        ======= DATOS ACTUALES =======
              
        Fecha   : {fila[1]}
        Concepto: {fila[2]}
        Monto   : {fila[3]}

        Ingrese los nuevos datos.
        (Presione Enter para conservar el valor actual)
        """)

        # Solicitar nuevos datos.
        # Si el usuario deja un campo vacío, se conserva el valor anterior.
        nueva_fecha = input("Nueva Fecha: ")
        if nueva_fecha == "":
            nueva_fecha = fila[1]

        nuevo_concepto = input("Nuevo Concepto: ")
        if nuevo_concepto == "":
            nuevo_concepto = fila[2]
        
        # Solicitar nuevo monto permitiendo conservar el valor actual
        nuevo_monto = pedir_monto_opcional("Nuevo Monto: ", fila[3])

        # Crear tupla con los datos actualizados y el ID del registro
        datos_actualizados = (
            nueva_fecha,
            nuevo_concepto,
            nuevo_monto,
            id_egreso
        )

        # Actualizar el registro seleccionado en la tabla Egresos
        cursor.execute("""UPDATE Egresos 
                       SET 
                        fecha = ?, 
                        concepto = ?,
                        monto = ?
                        WHERE id = ?
                       """, datos_actualizados)
        
        # Guardar los cambios realizados
        conn.commit()
        print("Egreso actualizado correctamente.\n")

# Elimina un egreso existente mediante su ID.
# Antes de eliminar solicita confirmación al usuario.
def eliminar_egreso(conn, cursor):
    # Solicitar el ID del egreso a eliminar
    id_egreso = pedir_entero("Ingrese el ID: ")

    # Buscar el registro antes de eliminarlo para verificar que existe
    cursor.execute("SELECT * FROM Egresos WHERE id = ?", (id_egreso,))

    # Obtener el registro encontrado
    fila = cursor.fetchone()

    # Verificar si existe el egreso
    if fila is None:
        print(f"No existe el ID = {id_egreso} en la base de datos.\n")
    else:
        # Mostrar los datos del egreso que será eliminado
        print(f"""
        ======= DATOS ACTUALES =======
                     
        Fecha   : {fila[1]}
        Concepto: {fila[2]}
        Monto   : {fila[3]}
        """)

        # Solicitar confirmación antes de eliminar el registro
        print("Se eliminará el egreso mostrado.")

        if pedir_confirmacion() == "s":
            # Eliminar el egreso seleccionado
            cursor.execute("DELETE FROM Egresos WHERE id = ?", (id_egreso,))

            # Guardar los cambios realizados
            conn.commit()
            print("Egreso eliminado correctamente.\n")
        else:
            print("Ok. Redirigiendo al menú.\n")