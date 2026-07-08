# Funcion para registrar ingresos
def registrar_ingreso(conn, cursor):
    # Preguntar datos
    fecha = input("Ingrese fecha (AAAA-MM-DD): ")
    nombre = input("Ingrese nombre: \n")
    baño = float(input("Ingrese monto del baño: "))
    agua = float(input("Ingrese monto del agua: "))
    papel = float(input("Ingrese monto del papel: "))
    
    # Tupla para insertar valores a la tabla
    datos = (fecha, nombre, baño, agua, papel)

    # Insertar valores
    cursor.execute("""INSERT INTO Ingresos (fecha, nombre, baño, agua, papel)
         VALUES (?, ?, ?, ?, ?)""", datos)
    
    # Guardar cambios
    conn.commit()
    print("Ingreso guardado correctamente\n")

def mostrar_ingresos(cursor):
    # Leer datos (Selecciona todos los datos)
    cursor.execute("SELECT * FROM Ingresos")
    
    # Ver resultado
    ingresos = cursor.fetchall()
    for ingreso in ingresos:
        print(ingreso)

def editar_ingreso(conn, cursor):
    id_ingreso = int(input("Ingrese el ID: "))

    # Consultar si el ID existe en la base de datos
    cursor.execute("SELECT * FROM Ingresos WHERE id = ?", (id_ingreso,)) # (id_ingreso,) tupla de un solo elemento

    # Guarda en una tupla la primera fila de lo seleccionado por cursor.execute()
    fila = cursor.fetchone()

    # Comprobar si existe el ID ingresado
    if fila is None:
        print(f"No existe el ID = {id_ingreso} en la base de datos.\n")
    else:
        print(f"""
                DATOS ACTUALES 
              
        Fecha : {fila[1]}
        Nombre: {fila[2]}
        Baño  : {fila[3]}
        Agua  : {fila[4]}
        Papel : {fila[5]}

        Ingrese los nuevos datos.
        (Presione Enter para conservar el valor actual)
        """)

        # Lógica para guardar o mantener datos
        nueva_fecha = input("Nueva Fecha: ")
        if nueva_fecha == "":
            nueva_fecha = fila[1]

        nuevo_nombre = input("Nuevo Nombre: ")
        if nuevo_nombre == "":
            nuevo_nombre = fila[2]
        
        # Cambiar str a float para que no haya errores en los datos
        nuevo_baño = input("Nuevo Baño: ")
        if nuevo_baño == "":
            nuevo_baño = fila[3]
        else:
            nuevo_baño = float(nuevo_baño)

        nuevo_agua = input("Nuevo Agua: ")
        if nuevo_agua == "":
            nuevo_agua = fila[4]
        else:
            nuevo_agua = float(nuevo_agua)
        
        nuevo_papel = input("Nuevo Papel: ")
        if nuevo_papel == "":
            nuevo_papel = fila[5]
        else:
            nuevo_papel = float(nuevo_papel)

        # Tupla creada para pasarle al cursor y actualizar
        datos_actualizados = (nueva_fecha, nuevo_nombre, nuevo_baño, nuevo_agua, nuevo_papel, id_ingreso)

        # Actualizar Ingresos
        cursor.execute("""UPDATE Ingresos 
                       SET 
                        fecha = ?, 
                        nombre = ?, 
                        baño = ?, 
                        agua = ?, 
                        papel = ? 
                        WHERE id = ?
                       """, datos_actualizados)
        
        # Guardar cambios
        conn.commit()
        print("Ingreso actualizado correctamente.\n")

def eliminar_ingreso(conn, cursor):
    id_ingreso = int(input("Ingrese el ID: "))

    # Consultar si el ID existe en la Base de datos
    cursor.execute("SELECT * FROM Ingresos WHERE id = ?", (id_ingreso,))

    # Guardar la fila seleccionada en el cursor
    fila = cursor.fetchone()

    # Comprobar si existe el ID en la base de datos
    if fila is None:
        print(f"No existe el ID = {id_ingreso} en la base de datos.\n")
    else:
        # Mostrar registro
        print(f"""
                DATOS ACTUALES:
                     
        Fecha : {fila[1]}
        Nombre: {fila[2]}
        Baño  : {fila[3]}
        Agua  : {fila[4]}
        Papel : {fila[5]}
        """)

        # Confirmar para eliminar y opciones
        confirmacion = int(input("¿Esta seguro de eliminar el ingreso en pantalla? (1.Si  2.No): "))
        if confirmacion == 1:
            cursor.execute("DELETE FROM Ingresos WHERE id = ?", (id_ingreso,))
            # Guardar cambios
            conn.commit()
            print("Listo. Ingreso eliminado correctamente.\n")
        elif confirmacion == 2:
            print("Ok. Redirigiendo al menu.\n")
        else:
            print("Error: redirigiendo al menu.\n")     