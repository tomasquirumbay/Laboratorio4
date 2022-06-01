#Proporciona clases para manipular fechas y horas.
import datetime
#Facilita el trabajo con peticiones HTTP.
import requests
#Realiza operaciones dependiente del SO como crear una carpeta o listar contenido de esta.
import os
#Facilita la escritura de interfaces de línea de comandos amigables.
import argparse
#Especifica un conjunto de cadenas que coinciden con ella
import re
#Sirve para el intercambio de datos
import json
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase

class FeriadoEcuador(HolidayBase):
    """
    Una clase que representar el feriado en Ecuador por provincia (FeriadoEcuador)
     Su objetivo es determinar si un fecha especifica es unas vacaciones lo mas 
     rapido y flexible posible.
     https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
     ...
     Atributos (Se hereda en la clase HolidayBase)
     ----------
     prov: str
         codigo de provincia segun ISO3166-2
     Métodos
     -------
     __init__(self, placa, fecha, hora, en linea=False):
         Construye todos los atributos necesarios para el objeto HolidayEcuador.
     _poblar(self, año):
         Devuelve si una fecha es feriado o no
    """     
    # ISO 3166-2 códigos para la subdivisión principal, 
    # llamado provincias
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    PROVINCIA = ["EC-P"]  # TODO agregar más provincias

    def __init__(self, **kwargs):
        """
       Contructor con todos los métodos necesario para los dias festivos de Ecuador.
        """         
        self.pais = "Ecuador"
        self.prov = kwargs.pop("provincia", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _poblacion(self, año):
        """
        Revisa si una fecha es feriado o no
        
         Parámetros
         ----------
         año: str
             año de una fecha
         Devuelve
         -------
         Devuelve "verdadero" si una fecha es un día festivo, caso contrario da falso.
        """                    
        #Año Nuevo 
        self[datetime.date(año, JAN, 1)] = "Año Nuevo [Nuevo año]"
        
        #Navidades
        self[datetime.date(año, DEC, 25)] = "Navidad [Navidades]"
        
        #Semana Sata
        self[easter(año) + rd(weekday=FR(-1))] = "Semana Santa (Viernes Santo) [Good Friday)]"
        self[easter(año)] = "D�a de Pascuas [Easter Day]"
        
        #Carnavales
        total_dias_libres = 46
        self[easter(año) - datetime.timedelta(days=total_dias_libres+2)] = "Lunes de carnaval [Carnival of Monday)]"
        self[easter(año) - datetime.timedelta(days=total_dias_libres+1)] = "Martes de carnaval [Tuesday of Carnival)]"
        
        # Dia nacional del trabajador
        nombre = "Día Nacional del Trabajo [Día del laborador]"
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Si el feriado cae un sábado o martes
        # el descanso obligatorio será trasladado al viernes o lunes
        # respectivamente:
        if año > 2015 and datetime.date(año, MAY, 1).weekday() in (5,1):
            self[datetime.date(año, MAY, 1) - datetime.timedelta(days=1)] = nombre
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) si el feriado cae un domingo
        # el descanso obligatorio sera para el lunes
        elif año > 2015 and datetime.date(año, MAY, 1).weekday() == 6:
            self[datetime.date(año, MAY, 1) + datetime.timedelta(days=1)] = nombre
        # (Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016 /R.O # 906)) Feriados que sean en mi�rcoles o jueves
        # se moverán al viernes de esa semana
        elif año > 2015 and  datetime.date(año, MAY, 1).weekday() in (2,3):
            self[datetime.date(año, MAY, 1) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(año, MAY, 1)] = nombre
        
        # La Batalla de Pichincha, tiene las mismas raglas del dia del trabajador
        nombre = "La batalla del Pichincha [Batalla de Pichincha]"
        if año > 2015 and datetime.date(año, MAY, 24).weekday() in (5,1):
            self[datetime.date(año, MAY, 24).weekday() - datetime.timedelta(days=1)] = nombre
        elif año > 2015 and datetime.date(año, MAY, 24).weekday() == 6:
            self[datetime.date(año, MAY, 24) + datetime.timedelta(days=1)] = nombre
        elif año > 2015 and  datetime.date(año, MAY, 24).weekday() in (2,3):
            self[datetime.date(año, MAY, 24) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(año, MAY, 24)] = nombre
        
        #El Primer grito de Independencia, tiene las mismas raglas del dia del trabajador
        nombre = "El primer Grito de la Independencia [Primer grito de independencia]"
        if año > 2015 and datetime.date(año, AUG, 10).weekday() in (5,1):
            self[datetime.date(año, AUG, 10)- datetime.timedelta(days=1)] = nombre
        elif año > 2015 and datetime.date(año, AUG, 10).weekday() == 6:
            self[datetime.date(año, AUG, 10) + datetime.timedelta(days=1)] = nombre
        elif año > 2015 and  datetime.date(año, AUG, 10).weekday() in (2,3):
            self[datetime.date(año, AUG, 10) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(año, AUG, 10)] = nombre       
        
        #La Independencia de Guayaquil, tiene las mismas raglas del dia del trabajador
        nombre = "La independencia de Guayaquil [Independencia de Guayaquil]"
        if año > 2015 and datetime.date(año, OCT, 9).weekday() in (5,1):
            self[datetime.date(año, OCT, 9) - datetime.timedelta(days=1)] = nombre
        elif año > 2015 and datetime.date(año, OCT, 9).weekday() == 6:
            self[datetime.date(año, OCT, 9) + datetime.timedelta(days=1)] = nombre
        elif año > 2015 and  datetime.date(año, MAY, 1).weekday() in (2,3):
            self[datetime.date(año, OCT, 9) + rd(weekday=FR)] = nombre
        else:
            self[datetime.date(año, OCT, 9)] = nombre        
        
        #Dia de los Difuntos
        nombreagregar = "Día de los difuntos [Día de difuntos]" 
        # Independencia de Cuenca
        nombreic = "Independencia de Cuenca [Independence of Cuenca]"
        #(Ley 858/Ley de Reforma a la LOSEP (vigente desde el 21 de diciembre de 2016/R.O # 906))
        #Para festivos nacionales y/o locales que coincidan en días corridos,
        #serán aplicadas las siguientes reglas:
        if (datetime.date(año, NOV, 2).weekday() == 5 and  datetime.date(año, NOV, 3).weekday() == 6):
            self[datetime.date(año, NOV, 2) - datetime.timedelta(days=1)] = nombreagregar
            self[datetime.date(año, NOV, 3) + datetime.timedelta(days=1)] = nombreic     
        elif (datetime.date(año, NOV, 3).weekday() == 2):
            self[datetime.date(año, NOV, 2)] = nombreagregar
            self[datetime.date(año, NOV, 3) - datetime.timedelta(days=2)] = nombreic
        elif (datetime.date(año, NOV, 3).weekday() == 3):
            self[datetime.date(año, NOV, 3)] = nombreic
            self[datetime.date(año, NOV, 2) + datetime.timedelta(days=2)] = nombreagregar
        elif (datetime.date(año, NOV, 3).weekday() == 5):
            self[datetime.date(año, NOV, 2)] =  nombreagregar
            self[datetime.date(año, NOV, 3) - datetime.timedelta(days=2)] = nombreic
        elif (datetime.date(año, NOV, 3).weekday() == 0):
            self[datetime.date(año, NOV, 3)] = nombreic
            self[datetime.date(año, NOV, 2) + datetime.timedelta(days=2)] = nombreagregar
        else:
            self[datetime.date(año, NOV, 2)] = nombreagregar
            self[datetime.date(año, NOV, 3)] = nombreic  
            
        #Fundación de Quito (Aplica solo para la provincia de Pichincha)
        #Las reglas son las mismas que el día del trabajo
        nombre = "La fundación de Quito [Fundación de Quito]"        
        if self.prov in ("EC-P"):
            if año > 2015 and datetime.date(año, DEC, 6).weekday() in (5,1):
                self[datetime.date(año, DEC, 6) - datetime.timedelta(days=1)] = nombre
            elif año > 2015 and datetime.date(año, DEC, 6).weekday() == 6:
                self[(datetime.date(año, DEC, 6).weekday()) + datetime.timedelta(days=1)] =nombre
            elif año > 2015 and  datetime.date(año, DEC, 6).weekday() in (2,3):
                self[datetime.date(año, DEC, 6) + rd(weekday=FR)] = nombre
            else:
                self[datetime.date(año, DEC, 6)] = nombre

class PicoPlaca:
    """
    Clase para representar un carro/vehiculo.
    medida de restriccion (Pico y Placa)
    -ORDENANZA METROPOLITANA No. 0305
    http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf
    ...
    Atributos
    ----------
    placa : str
        El registro o patente de un vehículo/carro es una combinación de caracteres alfabéticos o numéricos
        caracteres que identifican e individualizan el vehículo respecto de los demás:
        
        El formato que se usa es:
        XX-YYYY o XXX-YYYY,
        donde X es una letra mayúscula e Y es un dígito.
    fecha: str
        Fecha en la que el vehículo pretende transitar
        esta siguiendo el
        Formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.
    tiempo: str
        tiempo en que el vehículo pretende transitar
        esta siguiendo el formato
        HH:MM: por ejemplo, 08:35, 19:30
    en línea: booleano, opcional
        si está en línea == Verdadero, se utilizará la API de días festivos abstractos
    Métodos
    -------
    __init__(self, placa, fecha, hora, online=False):
        Construye todos los atributos necesarios.
        para el objeto PicoPlaca.
    placa (uno mismo):
        Obtiene el valor del atributo de placa
    placa (auto, valor):
        Establece el valor del atributo de la placa
    fecha (uno mismo):
        Obtiene el valor del atributo de fecha
    fecha (auto, valor):
        Establece el valor del atributo de fecha
    hora (uno mismo):
        Obtiene el valor del atributo de hora
    hora (uno mismo, valor):
        Establece el valor del atributo de hora
    __encontar_dia(yo, fecha):
        Devuelve el día a partir de la fecha: por ejemplo, miércoles
    __is_forbidden_time(self, check_time):
        Devuelve True si el tiempo proporcionado está dentro de las horas pico prohibidas, de lo contrario sería Falso
    __es_vacaciones:
        Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador, de lo contrario, False
    predecir (auto):
        Devuelve True si el vehículo con la placa especificada puede estar en la carretera en la fecha y hora especificadas, de lo contrario, False
    """
    #Días de la semana
    __dias = [
            "Lunes",
            "Martes",
            "Miercoles",
            "Jueves",
            "Viernes",
            "Sabado",
            "Domingo"]

    #Diccionario que contiene las restricciones en la forma {día: último dígito prohibido}
    __restricciones = {
            "Lunes": [1, 2],
            "Martes": [3, 4],
            "Miercoles": [5, 6],
            "Jueves": [7, 8],
            "Viernes": [9, 0],
            "Sabado": [],
            "Domingo": []}

    def __init__(self, placa, fecha, hora, enlinea=False):
        """
        Construye todos los atributos necesarios para el objeto PicoPlaca.
        
         Parámetros
         ----------
             placa : str
                 El registro o patente de un vehículo es una combinación de caracteres alfabéticos o numéricos
                 caracteres que identifican e individualizan el vehículo respecto de los demás;
                 El formato utilizado es AA-YYYY o XXX-YYYY, donde X es una letra mayúscula e Y es un dígito.
             fecha: str
                 Fecha en la que el vehículo pretende transitar
                 Sigue el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22.
             tiempo: str
                 tiempo en que el vehículo pretende transitar
                 Sigue el formato HH:MM: por ejemplo, 08:35, 19:30
             en línea: booleano, opcional
                 si en línea == Verdadero, se usará la API de días festivos abstractos (el valor predeterminado es Falso)               
        """                
        self.placa = placa
        self.fecha = fecha
        self.hora = hora
        self.enlinea = enlinea

    @property
    def placa(self):
        """Obtiene el valor del atributo placa"""
        return self._placa

    @placa.setter
    def placa(self, valor):
        """
        Establece evaluar el atributo placa
         Parámetros
         ----------
         valor: srt
        
         Aumenta
         ------
         ValorError
             Si el string de valor no tiene el formato
             XX-YYYY o XXX-YYYY,
             donde X es una letra mayúscula e Y es un dígito
        """
        if not re.match('^[A-Z]{2,3}-[0-9]{4}$', valor):
            raise ValueError(
                'La placa debe tener el siguiente formato: XX-YYYY o XXX-YYYY, donde X es una letra mayuscula e Y es un digito')
        self._placa = valor

    @property
    def fecha(self):
        """Obtiene el valor del atributo de fecha"""
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        """
        Establece el valor del atributo de fecha
         Parámetros
         ----------
         valor: str
        
         Aumenta
         ------
         ValorError
             Si el str de valor no tiene el formato AAAA-MM-DD (por ejemplo, 2021-04-02)
        """
        try:
            if len(valor) != 10:
                raise ValueError
            datetime.datetime.strptime(valor, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                'La fecha debe tener el siguiente formato: AAAA-MM-DD (por ejemplo: 2021-04-02)') from None
        self._fecha = valor
        

    @property
    def hora(self):
        """Obtiene el valor del atributo de tiempo"""
        return self._hora

    @hora.setter
    def hora(self, valor):
        """
        Establece el valor del atributo de tiempo
         Parámetros
         ----------
         valor: str
        
         aumenta
         ------
         ValorError
             Si el str de valor no tiene el formato HH:MM (por ejemplo, 08:31, 14:22, 00:01)
        """
        if not re.match('^([01][0-9]|2[0-3]):([0-5][0-9]|)$', valor):
            raise ValueError(
                'La hora debe tener el siguiente formato: HH:MM (por ejemplo, 08:31, 14:22, 00:01)')
        self._hora = valor

    def __encontrar_dia(self, fecha):
        """
        Encuentra el día a partir de la fecha: por ejemplo, miércoles
         Parámetros
         ----------
         fecha: str
             Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
         Devoluciones
         -------
         Devuelve el día a partir de la fecha como una cadena
        """        
        d = datetime.datetime.strptime(fecha, '%Y-%m-%d').weekday()
        return self.__dias[d]

    def __es_tiempo_prohibido(self, check_fecha):
        """
        Comprueba si el tiempo proporcionado está dentro de las horas pico prohibidas,
         donde las horas pico son: 07:00 - 09:30 y 16:00 - 19:30
         Parámetros
         ----------
         check_fecha : str
             Tiempo que se comprobará. Está en formato HH:MM: por ejemplo, 08:35, 19:15
         Devoluciones
         -------
         Devuelve verdadero si el tiempo proporcionado está dentro de las horas pico prohibidas, de lo contrario sería Falso
        """           
        t = datetime.datetime.strptime(check_fecha, '%H:%M').time()
        return ((t >= datetime.time(7, 0) and t <= datetime.time(9, 30)) or
                (t >= datetime.time(16, 0) and t <= datetime.time(19, 30)))

    def __es_vacaciones(self, fecha, enlinea):
        """
        Comprueba si la fecha (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador
         si está en línea == Verdadero, utilizará una API REST, de lo contrario, generará los días festivos del año examinado
        
         Parámetros
         ----------
         fecha: calle
             Está siguiendo el formato ISO 8601 AAAA-MM-DD: por ejemplo, 2020-04-22
         en línea: booleano, opcional
             si en línea == Verdadero, se utilizará la API de días festivos abstractos
         Devoluciones
         -------
         Devuelve True si la fecha marcada (en formato ISO 8601 AAAA-MM-DD) es un día festivo en Ecuador, de lo contrario, False
        """            
        y, m, d = fecha.split('-')

        if enlinea:
            #API de vacaciones abstractapi, versión gratuita: 1000 solicitudes por mes
             #1 solicitud por segundo
             #recuperar la clave API de la variable de entorno
            codigo = os.environ.get('VACACIONES_API_CODIGO')
            respuesta = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(codigo, y, m, d))
            if (respuesta.status_code == 401):
                #Esto significa que falta un codigo API
                raise requests.HTTPError(
                    'Falta la clave API. Guarde su clave en la variable de entorno HOLIDAYS API_KEY')
            if respuesta.content == b'[]':  #Si no hay vacaciones obtenemos una matriz vacía
                return False
            #Arreglar el Jueves Santo incorrectamente denotado como feriado
            if json.loads(respuesta.text[1:-1])['nombre'] == 'Maundy Thursday':
                return False
            return True
        else:
            ecu_holidays = FeriadoEcuador(prov='EC-P')
            return fecha in ecu_holidays

    def predecir(self):
        """
        Comprueba si el vehículo con la placa especificada puede estar en la carretera en la fecha y hora proporcionada según las reglas de Pico y Placa:
         http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf
         Devoluciones
         -------
         Devoluciones
         Verdadero si el vehículo con
         la placa especificada puede estar en el camino
         en la fecha y hora especificadas, de lo contrario Falso
        """
        #Comprobar si la fecha es un día festivo
        if self.__es_vacaciones(self.fecha, self.enlinea):
            return True

        #Consultar vehículos excluidos de la restricción según la segunda letra de la placa o si se utilizan solo dos letras
         #https://es.wikipedia.org/wiki/Matr%C3%ADculas_automovil%C3%ADsticas_de_Ecuador
        if self.placa[1] in 'AUZEXM' or len(self.placa.split('-')[0]) == 2:
            return True

       #Compruebe si el tiempo proporcionado no está en las horas pico prohibidas
        if not self.__es_tiempo_prohibido(self.hora):
            return True

        dia = self.__encontrar_dia(self.fecha) # Encuentra el día de la semana a partir de la fecha
         #Verifique si el último dígito de la placa no está restringido en este día en particular
        if int(self.placa[-1]) not in self.__restricciones[dia]:
            return True

        return False

if __name__ == '__main__':
    enlinea=False
    #Ingreso de datos lo que es la placa, fecha y hora... respectando los devidos formatos
    placa=input("Ingrese la placa por favor, la placa del vehiculo va asi: XXX-YYYY o XX-YYYY, donde X es una letra mayuscula e Y es un dígito: ")
    fecha=input("Ingrese la fecha por favor, la fecha a comprobar: AAAA-MM-DD: ")
    hora=input("Ingrese la hora por favor,la hora a comprobar: HH:MM:  ")

    pyp = PicoPlaca(placa, fecha, hora, enlinea)
  #En esta parte se muestra el vehiculo y su placa respectiva la cual puede o no 
  #estar en carretera con fecha y de que hora a que hora 
    if pyp.predecir():
        print(
            'El vehiculo con placa {} PUEDE estar en la carretera el {} a las {}.'.format(
                placa,
                fecha,
                hora))
    else:
        print(
            'El vehículo con la placa {} NOPUEDE estra en la carrtera el {} a las {}.'.format(
                placa,
                fecha,
                hora))