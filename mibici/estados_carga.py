import csv
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
archivo = BASE_DIR + '\\csv\\estados.csv'
archivo_viajes = BASE_DIR + '\\csv\\viajes.csv'
archivo_nuevo = BASE_DIR + '\\csv\\estados_con_viajes.csv'


def repeated_reader(input, reader):
    while True:
        input.seek(0)
        for row in reader:
            yield row
        break


with open(archivo) as csv_file:
    with open(archivo_viajes) as csv_viajes:
        with open(archivo_nuevo, 'w', newline='') as outfile:
            # Create a CSV writer object
            writer = csv.writer(outfile)

            reader = csv.reader(csv_viajes, delimiter="\t")
            estados_reader = csv.reader(csv_file, delimiter="\t")
            vacios = 0
            llenos = 0
            normales = 0
            for line in estados_reader:
                if line:
                    id = int(line[0])
                    estacion = int(line[1])
                    estado = int(line[2])
                    fecha = line[3].replace('"', '').strip()
                    hora = line[4].replace('"', '').strip()
                    fecha_hora_str = fecha+' '+hora
                    fecha_aux = datetime.strptime(fecha_hora_str, '%d/%m/%Y %H:%M:%S')
                    estado_timestamp = datetime.timestamp(fecha_aux)

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
                                        # print('Encontró el viaje que vació la estación. Viaje ID {}'.format(id_viaje))
                                        line.append(id_viaje)
                                        vacios += 1
                                        break
                            elif estado == 2:
                                if estacion == destino_estacion:
                                    if estado_timestamp - 60 <= destino_timestamp <= estado_timestamp+60:
                                        # print('Encontró el viaje que llenó la estación. Viaje ID {}'.format(id_viaje))
                                        line.append(id_viaje)
                                        llenos += 1
                                        break
                            elif estado == 1:
                                if estacion == destino_estacion:
                                    if estado_timestamp - 60 <= destino_timestamp <= estado_timestamp + 60:
                                        # print('Encontró el viaje que dejó NORMAL a la estación. Viaje ID {}'.format(id_viaje))
                                        line.append(id_viaje)
                                        normales += 1
                                        break
                                elif estacion == origen_estacion:
                                    if estado_timestamp-60 <= origen_timestamp <= estado_timestamp+60:
                                        # print('Encontró el viaje que dejó NORMAL a la estación. Viaje ID {}'.format(id_viaje))
                                        line.append(id_viaje)
                                        normales += 1
                                        break

                    writer.writerow(line)

print('Proceso Terminado. Encontrados: Vacios {}, Llenos {}, normales {}'.format(vacios, llenos, normales))
