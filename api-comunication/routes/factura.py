import re
from django.shortcuts import redirect
from flask import Blueprint, request, flash
from shared.functions import response, read_XML,analize_XML, movimientos, resume_iva, graphfy, quote_erase
import uuid
from fpdf import FPDF

factura = Blueprint('facturas', __name__)

peticiones = []

@factura.route("/all")
def get_all():
    peticiones.append('Peticion [GET]: Todas las facturas')
    data = read_XML("database.xml")
    return response(data, 200)

@factura.route("/test")
def test():
    data = read_XML("entrada.xml")
    return response(data, 200)

@factura.route("/parse_upload/", methods=['GET','POST'])
def parse_XML():
    peticiones.append('Petición [POST]: Subir archivo XML')
    peticiones.append('Petición [GET]: Analizar el archivo XML')
    data = analize_XML('entrada.xml', True)
    return response(data, 200)

@factura.route("/resumen/<fecha>/<nit>")
def resumen_nit(fecha, nit):
    peticiones.append('Peticiones [GET]: Resumen de fecha por NIT')
    data = movimientos('entrada.xml', fecha, nit)
    return response(data[0], 200)

@factura.route('/graph_nit/<fecha>/<nit>')
def graph_nit(fecha, nit):
    peticiones.append('Peticiones [GET]: Grafica de resumen de fecha por NIT')
    data = movimientos('entrada.xml', fecha, nit)
    graphfy(['EMITIDAS', 'RECIBIDAS'], data[1], 'pie')
    return response(data[0], 200)

@factura.route("/graph_iva/<inicio>/<fin>/<_iva>")
def graph_iva(inicio, fin, _iva):
    peticiones.append('Peticiones [GET]: Grafica de resumen por fecha')
    data = resume_iva('entrada.xml',inicio, fin, _iva)
    graphfy(data[1], data[2], 'bar')
    return response(data[0], 200)

@factura.route("/resumen_iva/<inicio>/<fin>/<_iva>")
def no_graph_iva(inicio, fin, _iva):
    peticiones.append('Peticiones [GET]: Resumen por fecha')
    data = resume_iva('entrada.xml',inicio, fin, _iva)
    return response(data[0], 200)

@factura.route('/pdf')
def reporte_pdf():
    peticiones.append('Peticiones [GET]: Reporte PDF')
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(w=0,h=15, txt='Reporte de Peticiones', ln=1, align='C', fill=0)
    for i in range(len(peticiones)):
        pdf.cell(w=0,h=15, txt=peticiones[i], border=1,align='C', ln= 1+(i+1), fill=0.25)
    pdf.output('reporte.pdf')
    return response({'Status':'Documento creado exitosamente'}, 200)

@factura.route('/reset')
def reset_db():
    quote_erase('database.xml')
    return response({'Status':'Base de Datos reseteada'}, 200)
