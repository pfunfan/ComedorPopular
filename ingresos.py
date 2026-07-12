from funciones_auxiliares import *

# Registra un nuevo ingreso en la base de datos.
# Solicita los datos al usuario, valida los montos y guarda el registro.
def registrar_ingreso(conn, cursor):
    # Solicitar información del ingreso
    fecha = input("Ingrese fecha (AAAA-MM-DD): ")
    nombre = input("Ingrese nombre: ")
    baño = pedir_monto("Ingrese monto del baño: ")
    agua = pedir_monto("Ingrese monto del agua: ")
    papel = pedir_monto("Ingrese monto del papel: ")
    
    # Agrupar los datos en una tupla para enviarlos a la consulta SQL
    datos = (fecha, nombre, baño, agua, papel)

    # Insertar el nuevo ingreso en la tabla Ingresos
    cursor.execute("""INSERT INTO Ingresos (fecha, nombre, baño, agua, papel)
         VALUES (?, ?, ?, ?, ?)""", datos)
    
    # Confirmar los cambios realizados en la base de datos
    conn.commit()
    print("Ingreso guardado correctamente\n")

# Muestra todos los ingresos registrados en la base de datos.
def mostrar_ingresos(cursor):
    # Obtener todos los registros de la tabla Ingresos
    cursor.execute("SELECT * FROM Ingresos")
    
    # Guardar los resultados obtenidos y mostrarlos
    ingresos = cursor.fetchall()
    for ingreso in ingresos:
        print(ingreso)

# Edita un ingreso existente mediante su ID.
# Permite conservar los valores actuales dejando campos vacíos.
def editar_ingreso(conn, cursor):
    # Solicitar el ID del registro que se desea modificar
    id_ingreso = pedir_entero("Ingrese el ID: ")

    # Buscar el ingreso seleccionado en la base de datos
    cursor.execute("SELECT * FROM Ingresos WHERE id = ?", (id_ingreso,))

    # Obtener la primera fila encontrada
    fila = cursor.fetchone()

    # Verificar si existe el registro solicitado
    if fila is None:
        print(f"No existe el ID = {id_ingreso} en la base de datos.\n")
    else:
        print(f"""
        ======= DATOS ACTUALES ======= 
              
        Fecha : {fila[1]}
        Nombre: {fila[2]}
        Baño  : {fila[3]}
        Agua  : {fila[4]}
        Papel : {fila[5]}

        Ingrese los nuevos datos.
        (Presione Enter para conservar el valor actual)
        """)

        # Solicitar nuevos datos. Si el usuario deja vacío, mantiene el valor anterior.
        nueva_fecha = input("Nueva Fecha: ")
        if nueva_fecha == "":
            nueva_fecha = fila[1]

        nuevo_nombre = input("Nuevo Nombre: ")
        if nuevo_nombre == "":
            nuevo_nombre = fila[2]
        
        # Pedir nuevos montos permitiendo conservar los valores actuales
        nuevo_baño = pedir_monto_opcional("Nuevo Baño: ", fila[3])
        nuevo_agua = pedir_monto_opcional("Nuevo Agua: ", fila[4])
        nuevo_papel = pedir_monto_opcional("Nuevo Papel: ", fila[5])

        # Crear tupla con los nuevos datos y el ID del registro a actualizar
        datos_actualizados = (
            nueva_fecha,
            nuevo_nombre,
            nuevo_baño,
            nuevo_agua,
            nuevo_papel,
            id_ingreso
        )

        # Actualizar el registro seleccionado en la tabla Ingresos
        cursor.execute("""UPDATE Ingresos 
                       SET 
                        fecha = ?, 
                        nombre = ?, 
                        baño = ?, 
                        agua = ?, 
                        papel = ? 
                        WHERE id = ?
                       """, datos_actualizados)
        
        # Guardar los cambios en la base de datos
        conn.commit()
        print("Ingreso actualizado correctamente.\n")

# Elimina un ingreso existente mediante su ID.
# Antes de eliminar solicita confirmación al usuario.
def eliminar_ingreso(conn, cursor):
    # Solicitar el ID del ingreso a eliminar
    id_ingreso = pedir_entero("Ingrese el ID: ")

    # Buscar el registro antes de eliminarlo para verificar que existe
    cursor.execute("SELECT * FROM Ingresos WHERE id = ?", (id_ingreso,))

    # Obtener el registro encontrado
    fila = cursor.fetchone()

    # Verificar si existe el ingreso
    if fila is None:
        print(f"No existe el ID = {id_ingreso} en la base de datos.\n")
    else:
        # Mostrar los datos del ingreso que será eliminado
        print(f"""
        ======= DATOS ACTUALES ======= 
                     
        Fecha : {fila[1]}
        Nombre: {fila[2]}
        Baño  : {fila[3]}
        Agua  : {fila[4]}
        Papel : {fila[5]}
        """)

        # Pedir confirmación antes de eliminar el registro
        print("Se eliminará el ingreso mostrado.")
        
        if pedir_confirmacion() == "s":
            # Eliminar el ingreso seleccionado
            cursor.execute("DELETE FROM Ingresos WHERE id = ?", (id_ingreso,))

            # Guardar los cambios realizados
            conn.commit()
            print("Ingreso eliminado correctamente.\n")
        else:
            print("Ok. Redirigiendo al menú.\n")