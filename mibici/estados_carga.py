import csv
from datetime import datetime

archivo = 'c:\\modelos\\ModelosPy\\bicicletas\\csv\\estados.csv'
archivo_viajes = 'c:\\modelos\\ModelosPy\\bicicletas\\csv\\viajes.csv'


def repeated_reader(input, reader):
    while True:
        input.seek(0)
        for row in reader:
            yield row
        break


with open(archivo) as csv_file:
    with open(archivo_viajes) as csv_viajes:
        reader = csv.reader(csv_viajes, delimiter="\t")
        vacios = 0
        llenos = 0
        normales = 0
        for cnt, line in enumerate(csv_file):
            if line:
                values = line.split('\t')
                id = int(values[0])
                estacion = int(values[1])
                estado = int(values[2])
                fecha = values[3].replace('"', '').strip()
                hora = values[4].replace('"', '').strip()
                fecha_hora_str = fecha+' '+hora
                fecha_aux = datetime.strptime(fecha_hora_str, '%d/%m/%Y %H:%M:%S')
                estado_timestamp = datetime.timestamp(fecha_aux)
                # if cnt<=10:
                print('ID {} - Estado: {} - Estación {} - Fecha {} {} - Timestamp {}'.format(id,
                                                                                         estado,
                                                                                         estacion,
                                                                                         fecha,
                                                                                         hora,
                                                                                         estado_timestamp))

                for viaje in repeated_reader(csv_viajes, reader):
                    if viaje:
                        id_viaje = int(viaje[0])
                        origen_hora = viaje[1].replace('"', '').strip()
                        destino_hora = viaje[2].replace('"', '').strip()
                        origen_fecha = viaje[3].replace('"', '').strip()
                        destino_fecha = viaje[4].replace('"', '').strip()
                        origen_estacion = int(viaje[5])
                        destino_estacion = int(viaje[6])

                        fecha_hora_str = origen_fecha + ' ' + origen_hora
                        fecha_aux = datetime.strptime(fecha_hora_str, '%d/%m/%Y %H:%M:%S')
                        origen_timestamp = datetime.timestamp(fecha_aux)

                        fecha_hora_str = destino_fecha + ' ' + destino_hora
                        fecha_aux = datetime.strptime(fecha_hora_str, '%d/%m/%Y %H:%M:%S')
                        destino_timestamp = datetime.timestamp(fecha_aux)

                        """
                        Si el estado es 0 (vacia). Viajes según fecha, hora y estación. EL mayor timestamp de los posibles Origenes.
                        Si el estado es 2 (llena). Viajes según fecha, hora y estación. EL mayor timestamp de los posibles Destinos.
                        Si el estado es 1 (normal). Viajes según fecha, hora y estación. EL menor timestamp de los posibles Ori/Des.
                        """
                        if estado == 0:
                            if estacion == origen_estacion:
                                if estado_timestamp-60 <= origen_timestamp <= estado_timestamp+60:
                                    print('Encontró el viaje que vació la estación. Viaje ID {}'.format(id_viaje))
                                    vacios += 1
                                    break
                        elif estado == 2:
                            if estacion == destino_estacion:
                                if estado_timestamp - 60 <= destino_timestamp <= estado_timestamp+60:
                                    print('Encontró el viaje que llenó la estación. Viaje ID {}'.format(id_viaje))
                                    llenos += 1
                                    break
                        elif estado == 1:
                            if estacion == destino_estacion:
                                if estado_timestamp - 60 <= destino_timestamp <= estado_timestamp + 60:
                                    print('Encontró el viaje que dejó NORMAL a la estación. Viaje ID {}'.format(id_viaje))
                                    normales += 1
                                    break
                            elif estacion == origen_estacion:
                                if estado_timestamp-60 <= origen_timestamp <= estado_timestamp+60:
                                    print('Encontró el viaje que dejó NORMAL a la estación. Viaje ID {}'.format(id_viaje))
                                    normales += 1
                                    break

print('Proceso Terminado. Encontrados: Vacios {}, Llenos {}, normales {}'.format(vacios, llenos, normales))
