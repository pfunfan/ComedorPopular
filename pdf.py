from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.platypus import Spacer
from reportlab.platypus import PageBreak
import os

def ingresos_encontrados(cursor, fecha):
    # Busca todos los ingresos registrados dentro del mes seleccionado.
    # Utiliza LIKE para encontrar fechas que comiencen con el formato AAAA-MM.
    # Ejemplo: "2026-07%" encuentra todos los registros de julio del 2026.
    patron_buscado = f"{fecha}%"

    # Ejecuta la consulta usando un parámetro seguro para evitar
    # insertar directamente valores dentro de la consulta SQL.
    cursor.execute("SELECT * FROM Ingresos WHERE fecha LIKE ?", (patron_buscado,))

    # Obtiene todos los registros encontrados.
    # Si no existen registros, devuelve una lista vacía.
    ingresos = cursor.fetchall()

    return ingresos

def egresos_encontrados(cursor, fecha):
    # Busca todos los egresos registrados dentro del mes seleccionado.
    # Utiliza LIKE para encontrar fechas que comiencen con el formato AAAA-MM.
    # Ejemplo: "2026-07%" encuentra todos los registros de julio del 2026.
    patron_buscado = f"{fecha}%"

    # Ejecuta la consulta usando un parámetro seguro.
    cursor.execute("SELECT * FROM Egresos WHERE fecha LIKE ?", (patron_buscado,))

    # Obtiene todos los registros encontrados.
    # Si no existen registros, devuelve una lista vacía.
    egresos = cursor.fetchall()

    return egresos

def fecha_texto(fecha):
    # Convierte el número de mes de una fecha AAAA-MM
    # a su nombre correspondiente.
    #
    # Ejemplos:
    # "2026-01" -> "ENERO"
    # "2026-07" -> "JULIO"
    # "2026-12" -> "DICIEMBRE"
    if fecha[-2:] == "01":
        return "ENERO"
    elif fecha[-2:] == "02":
        return "FEBRERO"
    elif fecha[-2:] == "03":
        return "MARZO"
    elif fecha[-2:] == "04":
        return "ABRIL"
    elif fecha[-2:] == "05":
        return "MAYO"
    elif fecha[-2:] == "06":
        return "JUNIO"
    elif fecha[-2:] == "07":
        return "JULIO"
    elif fecha[-2:] == "08":
        return "AGOSTO"
    elif fecha[-2:] == "09":
        return "SETIEMBRE"
    elif fecha[-2:] == "10":
        return "OCTUBRE"
    elif fecha[-2:] == "11":
        return "NOVIEMBRE"
    elif fecha[-2:] == "12":
        return "DICIEMBRE"


def total_ingresos_egresos(ingresos, egresos):
    # Calcula el total acumulado de ingresos y egresos del periodo.
    #
    # Los ingresos se calculan sumando los conceptos:
    # baño + agua + papel de cada registro.
    total_ingresos = 0

    for _, _, _, baño, agua, papel in ingresos:
        total_ingreso = baño + agua + papel
        total_ingresos += total_ingreso
    
    # Los egresos solamente tienen un monto asociado.
    total_egresos = 0

    for _, _, _, monto in egresos:
        total_egresos += monto
    
    return total_ingresos, total_egresos


def crear_listas_de_datos(ingresos, egresos, total_ingresos, total_egresos):

    # Crea la estructura de datos que será utilizada por ReportLab
    # para construir la tabla de ingresos.
    datos_ingresos = [
        ["Fecha", "Nombre", "S/.Baño", "S/.Agua", "S/.Papel", "S/.Total"],
    ]

    # Recorre los ingresos y genera cada fila de la tabla.
    # También calcula el total individual de cada ingreso.
    for _, fecha, nombre, baño, agua, papel in ingresos:
        total = baño + agua + papel
        fila = [fecha, nombre, f"{baño:.2f}", f"{agua:.2f}", f"{papel:.2f}", f"{total:.2f}"]
        datos_ingresos.append(fila)

    # Agrega una fila final con el total general de ingresos.
    datos_ingresos.append(["TOTAL", "", "", "", "", f"S/. {total_ingresos:.2f}"])


    # Crea la estructura de datos que será utilizada por ReportLab
    # para construir la tabla de egresos.
    datos_egresos = [
        ["Fecha", "Concepto", "Monto"]
    ]

    # Recorre los egresos y genera cada fila de la tabla.
    for _, fecha, concepto, monto in egresos:
        fila = [fecha, concepto, f"{monto:.2f}"]
        datos_egresos.append(fila)

    # Agrega una fila final con el total general de egresos.
    datos_egresos.append(["TOTAL", "", f"S/. {total_egresos:.2f}"])

    return datos_ingresos, datos_egresos


def crear_tablas_ie(datos_ingresos, datos_egresos):
    # Crea las tablas de ingresos y egresos utilizando los datos preparados.
    # En esta función solamente se define la estructura visual del PDF:
    # bordes, alineación, tamaño de letra y formato de encabezados.

    tabla_ingresos = Table(datos_ingresos)

    tabla_ingresos.setStyle(
        TableStyle([
            # Agrega bordes a todas las celdas de la tabla.
            ("GRID", (0, 0), (-1, -1), 1.5, colors.black),

            # Formato del encabezado de la tabla de ingresos.
            # Se aplica color de fondo, color de texto y negrita.
            ("BACKGROUND", (0, 0), (-1, 0), colors.teal),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            # Alinea los valores monetarios hacia la derecha.
            ("ALIGN", (2, 1), (-1, -1), "RIGHT"),

            # Centra los títulos de las columnas.
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),

            # Centra verticalmente todo el contenido.
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            # Ajusta el espacio inferior del encabezado.
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            # Define el tamaño de letra de toda la tabla.
            ("FONTSIZE", (0, 0), (-1, -1), 11),

            # Une las primeras columnas de la fila TOTAL para crear
            # una etiqueta más limpia visualmente.
            ("SPAN", (0, -1), (4, -1)),

            # Centra la fila del total.
            ("ALIGN", (0, -1), (5, -1), "CENTER"),
            ("VALIGN", (0, -1), (5, -1), "MIDDLE"),

            # Da formato especial a la fila TOTAL.
            ("FONTNAME", (0, -1), (5, -1), "Helvetica-Bold"),
            ("BACKGROUND", (0, -1), (5, -1), colors.teal),
            ("TEXTCOLOR", (0, -1), (5, -1), colors.white),

            # Ajusta el espacio inferior de la fila TOTAL.
            ("BOTTOMPADDING", (0, -1), (5, -1), 7)
        ])
    )

    tabla_egresos = Table(datos_egresos)

    tabla_egresos.setStyle(
        TableStyle([
            # Agrega bordes a todas las celdas de la tabla.
            ("GRID", (0, 0), (-1, -1), 1.5, colors.black),

            # Formato del encabezado de la tabla de egresos.
            ("BACKGROUND", (0, 0), (-1, 0), colors.teal),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            # Alinea el monto hacia la derecha.
            ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),

            # Centra los títulos de las columnas.
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),

            # Centra verticalmente todo el contenido.
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            # Ajusta espacio inferior del encabezado.
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            # Tamaño de letra general de la tabla.
            ("FONTSIZE", (0, 0), (-1, -1), 11),

            # Une las primeras dos columnas de la fila TOTAL.
            ("SPAN", (0, -1), (1, -1)),

            # Centra la etiqueta TOTAL.
            ("ALIGN", (0, -1), (1, -1), "CENTER"),

            # Formato especial de la fila TOTAL.
            ("BACKGROUND", (0, -1), (2, -1), colors.teal),
            ("TEXTCOLOR", (0, -1), (2, -1), colors.white),
            ("FONTNAME", (0, -1), (2, -1), "Helvetica-Bold"),

            # Ajusta espacio inferior de la fila TOTAL.
            ("BOTTOMPADDING", (0, -1), (2, -1), 7),
        ])
    )

    return tabla_ingresos, tabla_egresos

def lista_balance(total_ingresos, total_egresos, mes):
    # Solicita datos adicionales que no vienen de la base de datos.
    # Estos valores forman parte del balance mensual del comedor.
    ingreso_cobranza = float(input("Ingreso por cobranza (socias): "))
    alquiler_pescado = float(input("Alquiler pescado: "))
    ingreso_luz = float(input("Ingreso por luz: "))
    saldo_mes_anterior = float(input("Saldo mes anterior: "))

    # Calcula el total real de ingresos incluyendo:
    # ingresos registrados + ingresos adicionales + saldo anterior.
    total_ingresos_final = (
        total_ingresos +
        ingreso_cobranza +
        alquiler_pescado +
        ingreso_luz +
        saldo_mes_anterior
    )

    # Calcula el saldo disponible para el siguiente mes.
    saldo_mes_siguiente = total_ingresos_final - total_egresos

    # Determina el mes anterior.
    # Enero necesita un tratamiento especial porque el mes anterior es diciembre.
    if mes == "01":
        mes_anterior = "12"
    else:
        mes_anterior = str(int(mes) - 1).zfill(2)

    # Determina el mes siguiente.
    # Diciembre necesita un tratamiento especial porque el siguiente mes es enero.
    if mes == "12":
        mes_siguiente = "01"
    else:
        mes_siguiente = str(int(mes) + 1).zfill(2)

    # Crea la estructura de datos que será convertida en una tabla PDF.
    datos_balance = [
        
        ["Ingreso por baño", f"S/. {total_ingresos:.2f}"],
        ["Ingreso por cobranza (socias)", f"{ingreso_cobranza:.2f}"],
        ["Alquiler pescado", f"{alquiler_pescado:.2f}"],
        ["Ingreso por luz", f"{ingreso_luz:.2f}"],
        [f"Saldo de {fecha_texto(mes_anterior)}", f"{saldo_mes_anterior:.2f}"],
        [f"Total Ingresos {fecha_texto(mes)}", f"S/. {total_ingresos_final:.2f}"],
        [f"Total Egresos {fecha_texto(mes)}", f"S/. {total_egresos:.2f}"],
        [f"Saldo para {fecha_texto(mes_siguiente)}", f"S/. {saldo_mes_siguiente:.2f}"]      
    ]

    return datos_balance


def crear_tabla_balance(datos_balance):

    # Convierte los datos del balance en una tabla de ReportLab.
    # Aplica formato para diferenciar títulos y valores.
    tabla_balance = Table(datos_balance)

    tabla_balance.setStyle(
        TableStyle([
            # Agrega bordes a toda la tabla.
            ("GRID", (0, 0), (-1, -1), 1.5, colors.black),

            # Alinea las etiquetas del balance a la izquierda.
            ("ALIGN", (0, 0), (0, -1), "LEFT"),

            # Alinea los valores monetarios a la derecha.
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),

            # Centra verticalmente todo el contenido.
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            # Define el tamaño de letra.
            ("FONTSIZE", (0, 0), (-1, -1), 11),

            # Resalta la columna de etiquetas.
            ("BACKGROUND", (0, 0), (0, -1), colors.teal),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.white),

            # Coloca las etiquetas en negrita.
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

            # Ajusta el espacio interno de las celdas.
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    return tabla_balance

def crear_pdf(fecha, ingresos, egresos, balance):
    # Define la carpeta donde se almacenarán los reportes PDF.
    # Si la carpeta no existe, será creada automáticamente.
    carpeta = "/home/kiarapigg/Documentos/Reportes"
    os.makedirs(carpeta, exist_ok=True)

    # Crea el documento PDF indicando la ruta y nombre del archivo.
    # El nombre del archivo será el periodo del reporte.
    doc = SimpleDocTemplate(os.path.join(carpeta, f"{fecha}.pdf"))

    # Lista donde se agregan todos los elementos que aparecerán en el PDF.
    # ReportLab construirá el documento respetando el orden de esta lista.
    elementos = []

    # Obtiene los estilos predeterminados de ReportLab.
    # Se utilizan para crear títulos y párrafos.
    estilos = getSampleStyleSheet()

    # Crea el título de la sección de ingresos.
    # Muestra el nombre del comedor, tipo de reporte y periodo seleccionado.
    texto_ingresos = (
        f"COMEDOR POPULAR N°1 (2 DE MAYO)<br/><br/>"
        f"INGRESOS REPORTE MENSUAL<br/>"
        f"{fecha_texto(fecha)} {fecha[:4]}"
    )

    # Calcula los totales del periodo seleccionado.
    # Estos valores serán utilizados para las tablas y el balance.
    total_i, total_e = total_ingresos_egresos(ingresos, egresos)

    # Convierte los registros de la base de datos en listas compatibles
    # con las tablas de ReportLab.
    datos_ingresos, datos_egresos = crear_listas_de_datos(
        ingresos,
        egresos,
        total_i,
        total_e
    )

    # Crea el párrafo del encabezado de ingresos.
    encabezado = Paragraph(texto_ingresos, estilos["Title"])

    # Agrega el título a la lista de elementos del PDF.
    elementos.append(encabezado)

    # Agrega espacio vertical entre el título y la tabla.
    elementos.append(Spacer(1, 20))

    # Crea las tablas con su diseño visual.
    tabla_ingresos, tabla_egresos = crear_tablas_ie(
        datos_ingresos,
        datos_egresos
    )

    # Agrega la tabla de ingresos al PDF.
    elementos.append(tabla_ingresos)

    # Crea una nueva página para separar ingresos y egresos.
    elementos.append(PageBreak())

    # Crea el título de la sección de egresos.
    texto_egresos = (
        f"COMEDOR POPULAR N°1 (2 DE MAYO)<br/><br/>"
        f"EGRESOS REPORTE MENSUAL<br/>"
        f"{fecha_texto(fecha)} {fecha[:4]}"
    )

    # Crea el párrafo del encabezado de egresos.
    encabezado = Paragraph(texto_egresos, estilos["Title"])

    # Agrega el título de egresos al PDF.
    elementos.append(encabezado)

    # Agrega espacio entre el título y la tabla.
    elementos.append(Spacer(1, 20))

    # Agrega la tabla de egresos al PDF.
    elementos.append(tabla_egresos)

    # Verifica si el usuario desea agregar el balance mensual.
    if balance == "1":
        # Agrega espacio antes de la tabla del balance.
        elementos.append(Spacer(1, 40))

        # Crea el título del balance.
        text_balance = (
            f"BALANCE MES DE {fecha_texto(fecha)} {fecha[:4]}<br/><br/>"
        )

        # Crea el párrafo del título del balance.
        p_balance = Paragraph(text_balance, estilos["Title"])

        # Agrega el título del balance al PDF.
        elementos.append(p_balance)

        # Genera los datos del balance solicitando información adicional
        # al usuario y crea la tabla correspondiente.
        elementos.append(
            crear_tabla_balance(
                lista_balance(total_i, total_e, fecha[-2:])
            )
        )

    # Construye finalmente el archivo PDF utilizando todos los elementos
    # agregados anteriormente.
    doc.build(elementos)



def generar_pdf(cursor):
    # Solicita el año y mes que se desea consultar.
    año = input("Año(AAAA): ")
    mes = input("Mes(MM): ")
    print("")

    # Completa el mes con un cero inicial si es necesario.
    # Ejemplo: "7" se convierte en "07".
    mes = mes.zfill(2)

    # Construye el formato utilizado para buscar en la base de datos.
    # Ejemplo: "2026-07".
    fecha = f"{año}-{mes}"

    # Busca los registros de ingresos y egresos correspondientes
    # al mes seleccionado.
    ingresos = ingresos_encontrados(cursor, fecha)
    egresos = egresos_encontrados(cursor, fecha)

    # Verifica que exista información antes de generar el PDF.
    # Evita crear reportes vacíos.
    if not ingresos and not egresos:
        print(f"No existen ingresos ni egresos en el año {fecha}.")
    else:
        # Pregunta si el usuario desea incluir el balance mensual.
        balance = input(
            "Desea agregar el balance al pdf? (1.Si  2.No): "
        )

        # Genera el reporte PDF con la información encontrada.
        crear_pdf(fecha, ingresos, egresos, balance)

        print("PDF generado exitosamente.")