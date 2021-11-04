from flask import jsonify
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re
from numpy import sin
from werkzeug.datastructures import Authorization
import xmltodict
import xml.etree.cElementTree as xmlTree

def add_values_in_dict(sample_dict, key, list_of_values):
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict

def duplicated_ref(_ref, referencias):
    aux = 0
    for i in range(len(referencias)):
        if referencias[i] == _ref:
            aux += 1
    if aux == 1:
        return True
    else:
        return False

def get_hash(_no):
    _string = str(_no)
    length = 8 - len(list(_string))
    aux = ''
    for i in range(length):
        aux += '0'
    aux += str(_string)
    return aux

def modulo_once(_nit):
    if _nit.isnumeric():
        pass
    else:
        return False
    try:
        _nit = _nit.replace('-','')
    except:
        pass
    _nit = _nit.upper()
    _nit = _nit[::-1]
    _nit = list(_nit)
	
    multiplier = 2
    sigma = 0

	#Paso 1 y 2
    for i in range(1, len(_nit)):
        if i%6 == 0:
            #print(int(_nit[i])*multiplier)
            sigma += int(_nit[i])*multiplier
            multiplier = 2
        else:
            #print(int(_nit[i])*multiplier)
            sigma += int(_nit[i])*multiplier
            multiplier += 1
	#Paso 3
    #print("Sumatoria: ",sigma)
	#Paso 4 y 5
    modulo_once = 11 - sigma%11
    #print(modulo_once, " : ", _nit[0])
	#Verificación
    if modulo_once == int(_nit[0]):
        return True
    elif modulo_once == 10 and _nit[0] == 'K':
        return True
    else:
        return False

def response(body: dict, status_code: int):
    response = jsonify(body)
    response.status_code = status_code
    return response

def prettify(element, indent='    '):
    queue = [(0, element)]  # (level, element)
    while queue:
        level, element = queue.pop(0)
        children = [(level + 1, child) for child in list(element)]
        if children:
            element.text = '\n' + indent * (level+1)  
        if queue:
            element.tail = '\n' + indent * queue[0][0]  
        else:
            element.tail = '\n' + indent * (level-1)
        queue[0:0] = children 

def analize_XML(nameFile, write):
    with open("./shared/"+nameFile, 'r') as file:
        obj = xmltodict.parse(file.read())
        aux = obj['SOLICITUD_AUTORIZACION']['DTE']
        fechas = {}
        reply = {} #Para el que voy a mostrar
        temp = {}

        _list = []
        _list2 = []
        referencias = []
        fechas_keys = []
        #Consigo el número de fechas
        for x in range(len(aux)):
            def_fecha = re.findall(r"\d\d\/\d\d\/\d\d\d\d", aux[x]['TIEMPO'])
            fechas[def_fecha[0]] = def_fecha[0]
        
        fechas_keys = list(fechas.keys())

        for x in range(len(aux)):
            referencias.append(aux[x]['REFERENCIA'])

        for x in range(len(fechas_keys)):
            facturas_recibidas = 0
            ref_duplicada = 0
            NIT_EMISOR = 0
            NIT_RECEPTOR = 0
            ERROR_IVA = 0
            ERROR_TOTAL = 0
            FACTURAS_CORRECTAS = 0
            CANTIDAD_EMISORES = 0
            CANTIDAD_RECEPTORES = 0
            for y in range(len(aux)):
                def_fecha = re.findall(r"\d\d\/\d\d\/\d\d\d\d", aux[y]['TIEMPO'])
                if def_fecha[0] == fechas_keys[x]:
                    #print(def_fecha[0],' , ',fechas_keys[x], ',')
                    facturas_recibidas += 1
                    #comprobar si hay errores
                    if duplicated_ref(aux[y]['REFERENCIA'], referencias):
                        if modulo_once(aux[y]['NIT_EMISOR']):
                            if modulo_once(aux[y]['NIT_RECEPTOR']):
                                _d = round(float(aux[y]['VALOR']),2)
                                _iva = round(float(aux[y]['IVA']),2)
                                if round(_d*0.12,2) == _iva:
                                    if round((_d + _iva),2) == round(float(aux[y]['TOTAL']),2):
                                        aprobacion = def_fecha[0].split('/')
                                        aprobacion = aprobacion[::-1]
                                        reverse_date = ''.join(aprobacion)
                                        FACTURAS_CORRECTAS += 1
                                        second = get_hash(FACTURAS_CORRECTAS)
                                        reverse_date = reverse_date + second
                                        _list.append({'ref': aux[y]['REFERENCIA'], 'NIT_EMISOR':aux[y]['NIT_EMISOR'], 'CODIGO_APROBACION': reverse_date, 'TOTAL':aux[y]['TOTAL']})
                                        print(len(_list))
                                    else:
                                        ERROR_TOTAL += 1
                                else:
                                    ERROR_IVA += 1
                            else:
                                NIT_RECEPTOR += 1
                        else:
                            NIT_EMISOR += 1
                    else:
                        ref_duplicada += 1

            for z in range(len(_list)):
                temp[_list[z]['NIT_EMISOR']] = _list[z]['NIT_EMISOR']
            CANTIDAD_EMISORES = len(temp)

            temp = {}

            for z in range(len(_list)):
                temp[_list[z]['NIT_EMISOR']] = _list[z]['NIT_EMISOR']
            CANTIDAD_RECEPTORES = len(temp)

            _list2.append({"FECHA": fechas_keys[x],
            'FACTURAS_RECIBIDAS':facturas_recibidas,
            'ERRORES':{'NIT_EMISOR': NIT_EMISOR,'NIT_RECEPTOR':NIT_RECEPTOR,'IVA': ERROR_IVA, 'TOTAL': ERROR_TOTAL, 'REFERENCIA_DUPLICADA': ref_duplicada},
            'FACTURAS_CORRECTAS': FACTURAS_CORRECTAS, 'CANTIDAD_EMISORES':CANTIDAD_EMISORES,'CANTIDAD_RECEPTORES':CANTIDAD_RECEPTORES})
            _list2[len(_list2)-1] = add_values_in_dict(_list2[len(_list2)-1], 'LISTADO_AUTORIZACIONES', _list)
            _list = []
        try:
            if write:
                write_XML('database.xml',_list2)
            #return({"Message":"Documento de Salida creado exitosamente"})
            return(_list2)
        except:
            return({"Message":"No se pudo crear el documento"})  

def read_XML(nameFile):
    with open("./shared/"+nameFile, "r") as file:
        obj = xmltodict.parse(file.read())
        return(obj)

def  write_XML(nameFile, data):
    r = xmlTree.Element("LISTAAUTORIZACIONES")
    for i in range(len(data)):
        AUTORIZACION =  xmlTree.SubElement(r, 'AUTORIZACION')
        FECHA = xmlTree.SubElement(AUTORIZACION, 'FECHA')
        FECHA.text = str(data[i]['FECHA'])
        FACTURAS_RECIBIDAS = xmlTree.SubElement(AUTORIZACION, 'FACTURAS_RECIBIDAS')
        FACTURAS_RECIBIDAS.text = str(data[i]['FACTURAS_RECIBIDAS'])
        
        ERRORES = xmlTree.SubElement(AUTORIZACION, 'ERRORES')
        NIT_EMISOR = xmlTree.SubElement(ERRORES, 'NIT_EMISOR')
        NIT_EMISOR.text = str(data[i]['ERRORES']['NIT_EMISOR'])
        NIT_RECEPTOR = xmlTree.SubElement(ERRORES, 'NIT_RECEPTOR')
        NIT_RECEPTOR.text = str(data[i]['ERRORES']['NIT_RECEPTOR'])
        IVA_ERRORES = xmlTree.SubElement(ERRORES, 'IVA')
        IVA_ERRORES.text = str(data[i]['ERRORES']['IVA'])
        TOTAL_ERRORES = xmlTree.SubElement(ERRORES, 'TOTAL')
        TOTAL_ERRORES.text = str(data[i]['ERRORES']['TOTAL'])
        REFERENCIA_DUPLICADA = xmlTree.SubElement(ERRORES, 'REFERENCIA_DUPLICADA')
        REFERENCIA_DUPLICADA.text = str(data[i]['ERRORES']['REFERENCIA_DUPLICADA'])

        FACTURAS_CORRECTAS = xmlTree.SubElement(AUTORIZACION, 'FACTURAS_CORRECTAS')
        FACTURAS_CORRECTAS.text = str(data[i]['FACTURAS_CORRECTAS'])
        CANTIDAD_EMISORES = xmlTree.SubElement(AUTORIZACION, 'CANTIDAD_EMISORES')
        CANTIDAD_EMISORES.text = str(data[i]['CANTIDAD_EMISORES'])
        CANTIDAD_RECEPTORES = xmlTree.SubElement(AUTORIZACION, 'CANTIDAD_RECEPTORES')
        CANTIDAD_RECEPTORES.text = str(data[i]['CANTIDAD_RECEPTORES'])

        LISTADO_AUTORIZACIONES = xmlTree.SubElement(AUTORIZACION, 'LISTADO_AUTORIZACIONES')
        for j in range(len(data[i]['LISTADO_AUTORIZACIONES'])):
            APROBACION = xmlTree.SubElement(LISTADO_AUTORIZACIONES,'APROBACION')
            NIT_EMISOR_APROBACION = xmlTree.SubElement(APROBACION, 'NIT_EMISOR', ref=data[i]['LISTADO_AUTORIZACIONES'][j]['ref'])
            NIT_EMISOR_APROBACION.text = str(data[i]['LISTADO_AUTORIZACIONES'][j]['NIT_EMISOR'])
            CODIGO_APROBACION = xmlTree.SubElement(APROBACION,'CODIGO_APROBACION')
            CODIGO_APROBACION.text = str(data[i]['LISTADO_AUTORIZACIONES'][j]['CODIGO_APROBACION'])
            TOTAL = xmlTree.SubElement(APROBACION, 'TOTAL')
            TOTAL.text = str(data[i]['LISTADO_AUTORIZACIONES'][j]['TOTAL'])
        TOTAL_APROBACIONES = xmlTree.SubElement(LISTADO_AUTORIZACIONES, 'TOTAL_APROBACIONES')
        TOTAL_APROBACIONES.text = str(len(data[i]['LISTADO_AUTORIZACIONES']))
    try:
        prettify(r)
        tree = xmlTree.ElementTree(r)
        tree.write("./shared/{}".format(nameFile), 'UTF-8')
    except:
        pass

def movimientos(nameFile, fecha, nit):
    with open("./shared/"+nameFile, 'r') as file:
        obj = xmltodict.parse(file.read())
        aux = obj['SOLICITUD_AUTORIZACION']['DTE']
        reply = {}
        _list = []
        _list2 = []
        for x in range(len(aux)):
            def_fecha = re.findall(r"\d\d\/\d\d\/\d\d\d\d", aux[x]['TIEMPO'])
            apro = def_fecha[0].split('/')
            date = ''.join(apro)
            if date == fecha:
                if nit == aux[x]['NIT_EMISOR']:
                    _list.append({'REFERENCIA':aux[x]['REFERENCIA'],'IVA_EMITIDO':aux[x]['IVA']})
                elif nit == aux[x]['NIT_RECEPTOR']:
                    _list2.append({'REFERENCIA':aux[x]['REFERENCIA'],'IVA_RECIBIDO':aux[x]['IVA']})
            else:
                pass
        reply['EMISOR'] = _list
        reply['RECEPTOR'] = _list2
        valores = []
        valores.append(len(_list))
        valores.append(len(_list2))
        return [reply, valores]

def resume_iva(nameFile, inicio, fin, _iva):
    with open("./shared/"+nameFile, 'r') as file:
        obj = xmltodict.parse(file.read())
        aux = obj['SOLICITUD_AUTORIZACION']['DTE']
        reply = []
        fechas = {}
        raw = {}
        fechas_keys = []
        for x in range(len(aux)):
            def_fecha = re.findall(r"\d\d\/\d\d\/\d\d\d\d", aux[x]['TIEMPO'])
            fecha_aux =  def_fecha[0].split('/')
            date = ''.join(fecha_aux)
            
            raw[def_fecha[0]] = def_fecha[0]
            fechas[date] = date

        fechas_keys = list(fechas.keys())
        raw_keys = list(raw.keys())
        fechas_keys = sorted(fechas_keys) #Sorting out the list
        raw_keys = sorted(raw_keys)       #Sorting out the list
        labels = []
        values = []
        _v = False
        _list = analize_XML(nameFile,False)
        for x in range(len(fechas_keys)):
            if inicio == fechas_keys[x]:
                if inicio == fin:
                    labels.append(raw_keys[x])
                    values.append(int(length_date(_list, raw_keys[x])))
                else:
                    _v = True
            elif fin == fechas_keys[x]:
                _v = False
                labels.append(raw_keys[x])
                values.append(int(length_date(_list, raw_keys[x])))
            
            if _v:
                labels.append(raw_keys[x])
                values.append(int(length_date(_list, raw_keys[x])))
            else:
                pass
        
        _v = False
        for x in range(len(raw_keys)):
            if inicio == fechas_keys[x]:
                if inicio == fin:
                    for y in range(len(_list)):
                        if raw_keys[x] == _list[y]['FECHA']:
                            if _iva == 't':
                                reply.append({raw_keys[x]:_list[y]['LISTADO_AUTORIZACIONES']})
                            else:
                                for z in range(len(_list[y]['LISTADO_AUTORIZACIONES'])):
                                    sin_iva = float(_list[y]['LISTADO_AUTORIZACIONES'][z]['TOTAL'])
                                    sin_iva = round(sin_iva, 2)
                                    sin_iva = round(sin_iva/1.12,2)
                                    
                                    _list[y]['LISTADO_AUTORIZACIONES'][z]['TOTAL'] = str(sin_iva)
                                reply.append({raw_keys[x]:_list[y]['LISTADO_AUTORIZACIONES']})
                else:
                    _v = True
            elif fin == fechas_keys[x]:
                _v = False
                for y in range(len(_list)):
                    if raw_keys[x] == _list[y]['FECHA']:
                        if _iva == 't':
                            reply.append({raw_keys[x]:_list[y]['LISTADO_AUTORIZACIONES']})
                        else:
                            for z in range(len(_list[y]['LISTADO_AUTORIZACIONES'])):
                                sin_iva = float(_list[y]['LISTADO_AUTORIZACIONES'][z]['TOTAL'])
                                sin_iva = round(sin_iva, 2)
                                sin_iva = round(sin_iva/1.12,2)
                                _list[y]['LISTADO_AUTORIZACIONES'][z]['TOTAL'] = str(sin_iva)
                            reply.append({raw_keys[x]:_list[y]['LISTADO_AUTORIZACIONES']})

            if _v:
                for y in range(len(_list)):
                    if raw_keys[x] == _list[y]['FECHA']:
                        if _iva == 't':
                            reply.append({raw_keys[x]:_list[y]['LISTADO_AUTORIZACIONES']})
                        else:
                            for z in range(len(_list[y]['LISTADO_AUTORIZACIONES'])):
                                sin_iva = float(_list[y]['LISTADO_AUTORIZACIONES'][z]['TOTAL'])
                                sin_iva = round(sin_iva, 2)
                                sin_iva = round(sin_iva/1.12,2)
                                _list[y]['LISTADO_AUTORIZACIONES'][z]['TOTAL'] = str(sin_iva)
                            reply.append({raw_keys[x]:_list[y]['LISTADO_AUTORIZACIONES']})
            else:
                pass

        return [reply, labels, values]

def length_date(_list, text):
    for i in range(len(_list)):
        if _list[i]['FECHA'] == text:
            return len(_list[i]['LISTADO_AUTORIZACIONES'])
    return 0

def graphfy(labels, values, _type):
    if _type == 'pie':
        plt.pie(values, labels= labels)
        plt.savefig('piechart.png')
    elif _type == 'bar':
        plt.bar(labels, values)
        plt.savefig('barras.png')
    
    plt.close('all')

def quote_erase(nameFile):
    r = xmlTree.Element("LISTAAUTORIZACIONES")
    tree = xmlTree.ElementTree(r)
    tree.write("./shared/{}".format(nameFile), 'UTF-8')