from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.platypus import Spacer
from reportlab.platypus import PageBreak

def ingresos_encontrados(cursor, fecha):
    # Agrega '%' al final para buscar todas las fechas que comiencen
    # con el año y mes ingresados (Ejemplo: "2026-07%").
    patron_buscado = f"{fecha}%"

    # Ejecuta la consulta SQL.
    # '?' es un marcador de posición que será reemplazado por el valor
    # de 'patron_buscado' de forma segura.
    cursor.execute("SELECT * FROM Ingresos WHERE fecha LIKE ?", (patron_buscado,))

    # Obtiene todos los registros encontrados.
    # Si no existen coincidencias, devuelve una lista vacía ([]).
    ingresos = cursor.fetchall()

    # Una lista vacía se evalúa como False en Python.
    return ingresos

def egresos_encontrados(cursor, fecha):
    # Agrega '%' al final para buscar todas las fechas que comiencen
    # con el año y mes ingresados (Ejemplo: "2026-07%").
    patron_buscado = f"{fecha}%"

    # Ejecuta la consulta SQL.
    # '?' es un marcador de posición que será reemplazado por el valor
    # de 'patron_buscado' de forma segura.
    cursor.execute("SELECT * FROM Egresos WHERE fecha LIKE ?", (patron_buscado,))

    # Obtiene todos los registros encontrados.
    # Si no existen coincidencias, devuelve una lista vacía ([]).
    egresos = cursor.fetchall()

    # Una lista vacía se evalúa como False en Python.
    return egresos

# 'fecha[-2:]' obtiene los dos últimos caracteres de la cadena.
# Como la fecha tiene el formato "AAAA-MM", los dos últimos caracteres
# corresponden al número del mes.
# Ejemplos:
# "2026-01" -> "01"
# "2026-07" -> "07"
# "2026-12" -> "12"
def fecha_texto(fecha):
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

def crear_pdf(fecha, ingresos, total_ingresos):
    # Crea el documento PDF.
    doc = SimpleDocTemplate(f"{fecha}.pdf")

    # Lista donde se irán agregando todos los elementos del reporte.
    elementos = []

    # Obtiene los estilos predeterminados de ReportLab.
    estilos = getSampleStyleSheet()
    texto = (
        f"COMEDOR POPULAR N°1 (2 DE MAYO)<br/><br/>"
        f"INGRESOS REPORTE MENSUAL<br/>"
        f"{fecha_texto(fecha)} {fecha[:4]}"
    )

    datos_ingresos = [
        ["Fecha", "Nombre", "S/.Baño", "S/.Agua", "S/.Papel", "S/.Total"],
    ]

    for _, fecha, nombre, baño, agua, papel in ingresos:
        total = baño + agua + papel
        fila = [fecha, nombre, f"{baño:.2f}", f"{agua:.2f}", f"{papel:.2f}", f"{total:.2f}"]
        datos_ingresos.append(fila)

    datos_ingresos.append(["", "", "", "", "S/.TOTAL", f"{total_ingresos:.2f}"])


    # Parrafo y agregarlo a la lista
    encabezado = Paragraph(texto, estilos["Title"])
    elementos.append(encabezado)

    # Espacio entre titulo y tabla Spacer(ancho, alto)
    elementos.append(Spacer(1, 20))

    tabla_ingresos = Table(datos_ingresos)
    tabla_ingresos.setStyle(
        TableStyle([
            # Configura los bordes de la tabla completa
            # Sintaxis: ("ESTILO", (Col,Fila_Inicio), (Col,Fila_Fin), Grosor, Color), (c, f)
            ("GRID", (0, 0), (-1, -1), 1.5, colors.black),
            # Fondo Teal solo para la primera fila (encabezado) desde la col 0 hasta la última (-1)
            ("BACKGROUND", (0, 0), (-1, 0), colors.teal),
            # Letra blanca solo para la primera fila (encabezado) desde la col 0 hasta la última (-1)
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            # Texto en negrita (Helvetica-Bold) solo para los títulos de la primera fila
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            # Alinear los valores de baño, agua y papel a la derecha
            ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
            # Alinea valores de primera fila al centro (encabezado)
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            # Alinea verticalmente todo al centro
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            # Agrega 8 puntos de separación entre el texto y el borde de abajo (solo encabezado)
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            # Agrega tamaño de letra a toda la tabla
            ("FONTSIZE", (0, 0), (-1, -1), 11)
        ])
    )
    elementos.append(tabla_ingresos)

    # Nueva hoja
    elementos.append(PageBreak())
    # Construye el PDF utilizando los elementos de la lista.
    doc.build(elementos)

def generar_pdf(cursor):
    año = input("Año(AAAA): ")
    mes = input("Mes(MM): ")
    print("")

    mes = mes.zfill(2)
    fecha = f"{año}-{mes}"

    ingresos = ingresos_encontrados(cursor, fecha)
    egresos = egresos_encontrados(cursor, fecha)

    if not ingresos:
        print(f"No existen ingresos para el año y mes {fecha}.")
    else:
        print(f"Se encontraron {len(ingresos)} ingresos en {fecha}.")
        
        total_ingresos = 0
        for _, _, _, baño, agua, papel in ingresos:
            total_ingreso = baño + agua + papel
            total_ingresos += total_ingreso
        print(f"Total ingresos: S/. {total_ingresos}\n")
        crear_pdf(fecha, ingresos, total_ingresos)
        print("PDF generado exitosamente.")
    
    if not egresos:
        print(f"No existen egresos para el año y mes {fecha}.")
    else:
        print(f"Se encontraron {len(egresos)} egresos en {fecha}.")

        total_egresos = 0
        for _, _, _, monto in egresos:
            total_egresos += monto
        print(f"Total egresos: S/. {total_egresos}")