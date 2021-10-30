from flask import Blueprint, request
from shared.functions import response, read_XML, writeJson
import uuid

factura = Blueprint('facturas', __name__)

@factura.route("/all")
def get_all():
    data = {
        "data": read_XML("salida.xml")
    }
    return response(data, 200)