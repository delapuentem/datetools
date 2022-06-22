#!/usr/bin/env python3
import sys, re, datetime, time

def __regex_match(stringdate):
    '''Comprueba que el string que se pasa como parametro contenga una fecha que haga match con el regex especificado, y devuelve una diccionario con el regex que ha hecho match y su formato de fecha correspondiente'''
    # Formatos de fecha aceptados con los que va a comprobar si hace match o no la fecha
    formatos_aceptados = (
        ("\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d", "%Y-%m-%dT%H:%M:%S"),
        ("\d{4}-[01]\d-[0-3]\d\s[0-2]\d:[0-5]\d:[0-5]\d", "%Y-%m-%d %H:%M:%S"),
    )    
    # Recorre los formatos aceptados y si el string que se le pasa como argumento hace match con algún formato, devuelve el regex y formato correspondiente
    try:
        formato_fecha = next(filter(lambda formato: re.findall(formato[0], stringdate), formatos_aceptados))
    except StopIteration:
        print(f"Error! '{stringdate}' no hace match con los formatos aceptados")
        sys.exit()
    # Devuelve una tupla con el regex que hace match con la fecha string que hems pasado, y el formato fecha correspondiente con ese regex que usaremos para pasarlo con sfrtime a objeto de tiempo
    return dict(match=True, formato_fecha=formato_fecha)

def __weekday_map(weekday_num):
    '''Se le pasa el dia de la semana de 0 hasta 6 y devuelve a que dia corresponde en una tupla con los dias en formato string'''
    # Lista de mapeos de días de la semana  
    LISTA_WEEKDAY = ((1, 'Lunes', 'Monday'),(2, 'Martes', 'Tuesday'),(3, 'Miércoles', 'Wednesday'),(4, 'Jueves', 'Thursday'),(5, 'Viernes', 'Friday'),(6, 'Sábado', 'Saturday'),(0, 'Domingo', 'Sunday'))
    # Recorre los dias de la semana y devuelve el primer match con numero del dia de la semana, el dia de la semana en español y en ingles
    weekday_map = next(filter(lambda weekday: weekday[0] == int(weekday_num) ,LISTA_WEEKDAY))
    return weekday_map

def normalize_date(stringdate, **kwars):
    '''A partir de un string que contenga una fecha que haga match con el regex especificado, aplica la zona horaria y devuelve la fecha normalizada. Por defecto, el formato de salida es %Y-%m-%d %H:%M:%S, pero se puede especificar cualquier formato de salida.
    Por defecto, la zona horaria es +0, pero se puede ajustar con numero positivos o negativos.'''
    
    # Argumentos por defecto
    defaultargs = dict(output_format='%Y-%m-%d %H:%M:%S', time_zone=+0,)
    # Argumentos por defecto. Si no se le pasa parametro coge como defecto el segundo parameto del get
    output_format = kwars.get('output_format', defaultargs['output_format'])
    time_zone = kwars.get('time_zone', defaultargs['time_zone'])

    # Formato regex y formato fecha
    formato_fecha_regex = __regex_match(stringdate)['formato_fecha'][0] # Regex
    formato_fecha_fecha = __regex_match(stringdate)['formato_fecha'][1]  # Formato de la fecha

    # Extramos la fecha del string que se le pasa como argumento a la funcion
    fecha = re.findall(formato_fecha_regex, stringdate)[0]

    # Parseamos la fecha con el formato correspondiente para convertir la fecha del string en un objeto de tiempo y ajustamos la zona horaria
    fecha_objeto =  datetime.datetime.strptime(str(fecha), str(formato_fecha_fecha)) + datetime.timedelta(hours=time_zone)

    # Aplicamos el formato de salida
    fecha_output = fecha_objeto.strftime(output_format)

    return fecha_output   

def tag_date(stringdate, **kwars):
    '''Devuelve una fecha MES-AÑO en inglés o español en formato string. Por defecto es en español.'''
    # Argumentos por defecto
    defaultargs = dict(language = 'es',)
    # Argumentos por defecto. Si no se le pasa parametro coge como defecto el segundo parameto del get
    language = kwars.get('language', defaultargs['language'])

    LISTA_MES = (
        (1,'Enero', 'January'),
        (2,'Ferero', 'February'),
        (3,'Marzo', 'March'),
        (4,'Abril', 'April'),
        (5,'Mayo', 'May'),
        (6,'Junio', 'June'),
        (7,'Julio', 'July'),
        (8,'Agosto', 'August'),
        (9,'Septiembre', 'September'),
        (10,'Octubre', 'October'),
        (11,'Noviembre', 'November'),
        (12,'Diciembre', 'December'),                                                                                         
    )

    formato_fecha_regex = __regex_match(stringdate)['formato_fecha'][0] # Regex
    formato_fecha_fecha = __regex_match(stringdate)['formato_fecha'][1]  # Formato de la fecha
    # Extramos la fecha del string que se le pasa como argumento a la funcion
    fecha = re.findall(formato_fecha_regex, stringdate)[0]  
    # Parseamos la fecha con el formato correspondiente para convertir la fecha del string en un objeto de tiempo y ajustamos la zona horaria
    fecha_objeto =  datetime.datetime.strptime(str(fecha), str(formato_fecha_fecha))
    # Aplicamos el formato de salida
    mes = next(filter(lambda numero_mes: numero_mes[0] == int(fecha_objeto.strftime("%m")) ,LISTA_MES))
    if str(language) == 'es':
       etiqueta = fecha_objeto.strftime(f"{str(mes[1]).upper()[:3]}-%Y")   
    elif str(language) == 'en':
        etiqueta = fecha_objeto.strftime(f"{str(mes[2]).upper()[:3]}-%Y")   
    else:
        print(f"Error! en language='{language}' valor no admitido. Valores admitidos 'es','en'. Por defecto 'es'")
        sys.exit()       
     
    return etiqueta

def different_days(stringdate1, stringdate2):
    '''Devuelve True o False si es el mismo día o no.'''
    # Pasamos las fechas a objeto de tiempo y las convertimos a formato YYYY-MM-DD para compararlas
    fecha1 = datetime.datetime.strptime(normalize_date(stringdate1), '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")
    fecha2 = datetime.datetime.strptime(normalize_date(stringdate2), '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")
    if str(fecha1) == str(fecha2): 
        response = True
    else: 
        response = False
    return response    

def subtract_dates(stringdate1, stringdate2, **kwars):
    '''Resta dos fechas pasadas y devuelve la diferencia en días, horas, minutos o segundos. Por defecto devuelve un valor en segundos.'''
    # Argumentos por defecto
    defaultargs = dict(unit = 'second',)
    # Argumentos por defecto. Si no se le pasa parametro coge como defecto el segundo parameto del get
    unit = kwars.get('unit', defaultargs['unit'])

    # Pasamos las fechas a objeto de tiempo y las convertimos a unix epoch segundos
    fecha1 = int(time.mktime(time.strptime(normalize_date(stringdate1), '%Y-%m-%d %H:%M:%S')))
    fecha2 = int(time.mktime(time.strptime(normalize_date(stringdate2), '%Y-%m-%d %H:%M:%S')))
    if str(unit) == 'second':
        diferencia_minutos = float((fecha1 - fecha2))
    elif str(unit) == 'min':
        diferencia_minutos = float((fecha1 - fecha2) / 60)
    elif str(unit) == 'hour':
        diferencia_minutos = float((fecha1 - fecha2) / 60 / 60)
    elif str(unit) == 'day':
        diferencia_minutos = float((fecha1 - fecha2) / 60 / 60 / 24)
    else:
        print(f"Error! unit='{unit}' unsupported value. Supported values ​​'seconds','min','hour','days'. Default 'seconds'")
        sys.exit()
    # Devolvemos la diferencia, quitando un posible valor negativo. Por que puede que se pase como argumento las fechas al revés.
    return round(float(str(diferencia_minutos).replace(' ','').replace('-','')), 2)

def weekday_num(stringdate):
    '''Devuelve el número del dia de la semana. 0 es Lunes.'''
    weekdaynum = int(datetime.datetime.strptime(normalize_date(stringdate), '%Y-%m-%d %H:%M:%S').weekday())
    return weekdaynum

def weekday_name(stringdate, **kwars):
    '''Devuelve el dia de la semana en inglés o español en formato string. Por defecto es en español.'''
    # Argumentos por defecto
    defaultargs = dict(language = 'es',)
    # Argumentos por defecto. Si no se le pasa parametro coge como defecto el segundo parameto del get
    language = kwars.get('language', defaultargs['language'])

    weekday_map = __weekday_map(weekday_num(stringdate))
 
    if str(language) == 'es':
        weekdayname = weekday_map[1]
    elif str(language) == 'en':
        weekdayname = weekday_map[2]
    else:
        print(f"Error! en language='{language}' valor no admitido. Valores admitidos 'es','en'. Por defecto 'es'")
        sys.exit()        

    return weekdayname

def weekday_counter(weekdaynumero, days_between, language='es'):
    '''Sabiendo el dia de la semana en el que nos encontramos, y la diferencia en dias entre dos fechas, cuenta los días de la semana que hay entre medias (no inclusive principio y fin)'''
    # Contador de seguridad para no caer en un loop infinito
    contador_seguridad = 0
    weekday_counter_list = []
    # Mientras que el contador de seguridad sea menor a la diferencia de fechas entre los dos dias
    while contador_seguridad < int(days_between):
        # Cada ciclo sumamos 1 al contador de seguridad.
        contador_seguridad += 1
        # Cuando el contador de seguridad complete los ciclos correspondientes hasta llegar al valor de los dias entre medias para el ciclo.
        if contador_seguridad == int(days_between):
            break
        # Si el numero de la semana es inferior a 6 (Dias de la semana van del 0 al 6), suma +1. Si llega a 7 se resetea a 0, es decir, la semana vuelve a empezar.
        elif weekdaynumero < 6:
            weekdaynumero += 1
        else:
            weekdaynumero = 0
        # Mapeo el dia de la semana correspondiente
        weekday_map = __weekday_map(weekdaynumero)
        #print(weekday_map)
        # Devuelvo una lista con cuantos dias de la semana hay repartidos por la cantidad por dia de la semana
        # list compresion en dict comrpesion
        weekday_counter_list.append(weekday_map)
    if language == 'es':
        return {item:[item[1] for item in weekday_counter_list].count(item) for item in [item[1] for item in weekday_counter_list]}
    elif language == 'en':
        return {item:[item[2] for item in weekday_counter_list].count(item) for item in [item[2] for item in weekday_counter_list]}