# Funcion para registrar ingresos
def registrar_ingreso(conn, cursor):
    # Preguntar datos
    fecha = input("Ingrese fecha (AAAA-MM-DD): \n")
    nombre = input("Ingrese nombre: \n")
    baño = float(input("Ingrese monto del baño: \n"))
    agua = float(input("Ingrese monto del agua: \n"))
    papel = float(input("Ingrese monto del papel: \n"))
    
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
    registros = cursor.fetchall()
    for registro in registros:
        print(registro)

def editar_ingreso(conn, cursor):
    id_ingreso = int(input("Escriba el ID: \n"))

    # Consultar si el ID existe en la base de datos
    cursor.execute("SELECT * FROM Ingresos WHERE id = ?", (id_ingreso,)) # (id_ingreso,) tupla de un solo elemento

    # Guarda en una tupla la primera fila de lo seleccionado por cursor.execute()
    fila = cursor.fetchone()

    # Comprobar si existe el ID ingresado
    if fila is None:
        print(f"No existe el ID = {id_ingreso} en la base de datos.\n")
    else:
        print(f"""DATOS ACTUALES: 
              
              Fecha : {fila[1]}
              Nombre: {fila[2]}
              Baño  : {fila[3]}
              Agua  : {fila[4]}
              Papel : {fila[5]}

              Ingrese los nuevos datos.
              (Presione Enter para conservar el valor actual)
        """)

        # Lógica para guardar o mantener datos
        nueva_fecha = input("Nueva Fecha: \n")
        if nueva_fecha == "":
            nueva_fecha = fila[1]

        nuevo_nombre = input("Nuevo Nombre: \n")
        if nuevo_nombre == "":
            nuevo_nombre = fila[2]
        
        # Cambiar str a float para que no haya errores en los datos
        nuevo_baño = input("Nuevo Baño: \n")
        if nuevo_baño == "":
            nuevo_baño = fila[3]
        else:
            nuevo_baño = float(nuevo_baño)

        nuevo_agua = input("Nuevo Agua: \n")
        if nuevo_agua == "":
            nuevo_agua = fila[4]
        else:
            nuevo_agua = float(nuevo_agua)
        
        nuevo_papel = input("Nuevo Papel: \n")
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