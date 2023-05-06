import csv
from datetime import datetime, timedelta
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
archivo = BASE_DIR + '\\csv\\estados.csv'
archivo_viajes = BASE_DIR + '\\csv\\viajes.csv'
archivo_nuevo = BASE_DIR + '\\csv\\estados_chat.csv'

# Read the viajes.csv file into a dictionary
viajes_dict = {}
origen_dict = {}
origen_dict_1 = {}
destino_dict = {}
destino_dict_1 = {}
with open(archivo_viajes) as csv_viajes:
    reader = csv.reader(csv_viajes, delimiter="\t")
    for viaje in reader:
        origen_hora = viaje[1].replace('"', '').strip()
        destino_hora = viaje[2].replace('"', '').strip()
        origen_fecha = viaje[3].replace('"', '').strip()
        destino_fecha = viaje[4].replace('"', '').strip()
        origen_estacion = int(viaje[5])
        destino_estacion = int(viaje[6])

        fecha_hora_str = origen_fecha + ' ' + origen_hora
        fecha_aux = datetime.strptime(fecha_hora_str, '%d/%m/%Y %H:%M:%S')
        fecha_aux = fecha_aux.replace(second=0)
        origen_str = fecha_aux.strftime('%d/%m/%Y %H:%M:%S')
        fecha_aux = fecha_aux + timedelta(minutes=1)
        origen_1_str = fecha_aux.strftime('%d/%m/%Y %H:%M:%S')
        # origen_timestamp = datetime.timestamp(fecha_aux)

        fecha_hora_str = destino_fecha + ' ' + destino_hora
        fecha_aux = datetime.strptime(fecha_hora_str, '%d/%m/%Y %H:%M:%S')
        fecha_aux = fecha_aux.replace(second=0)
        destino_str = fecha_aux.strftime('%d/%m/%Y %H:%M:%S')
        fecha_aux = fecha_aux + timedelta(minutes=1)
        destino_1_str = fecha_aux.strftime('%d/%m/%Y %H:%M:%S')
        # destino_timestamp = datetime.timestamp(fecha_aux)

        origen_dict[(origen_estacion, origen_str)] = int(viaje[0])
        origen_dict_1[(origen_estacion, origen_1_str)] = int(viaje[0])
        destino_dict[(destino_estacion, destino_str)] = int(viaje[0])
        destino_dict_1[(destino_estacion, destino_1_str)] = int(viaje[0])

# Process the estados.csv file and write the output to estados_con_viajes.csv
with open(archivo) as csv_file:
    with open(archivo_nuevo, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
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
                estado_str = fecha+' '+hora

                viaje_id = None
                if estado == 0:
                    # Look up viaje_id using origen_estacion, estacion, and estado_timestamp
                    viaje_id = origen_dict.get((estacion, estado_str), None)
                    if viaje_id:
                        line.append(viaje_id)
                        vacios += 1
                    else:
                        viaje_id = origen_dict_1.get((estacion, estado_str), None)
                        if viaje_id:
                            line.append(viaje_id)
                            vacios += 1
                elif estado == 2:
                    # Look up viaje_id using estacion, destino_estacion, and estado_timestamp
                    viaje_id = destino_dict.get((estacion, estado_str), None)
                    if viaje_id:
                        line.append(viaje_id)
                        llenos += 1
                    else:
                        viaje_id = destino_dict_1.get((estacion, estado_str), None)
                        if viaje_id:
                            line.append(viaje_id)
                            vacios += 1
                elif estado == 1:
                    # Look up viaje_id using origen_estacion, estacion, and estado_timestamp
                    viaje_id = destino_dict.get((estacion, estado_str), None)
                    if viaje_id is None:
                        viaje_id = origen_dict.get((estacion, estado_str), None)
                        if viaje_id:
                            line.append(viaje_id)
                            normales += 1
                        else:
                            viaje_id = destino_dict_1.get((estacion, estado_str), None)
                            if viaje_id:
                                line.append(viaje_id)
                                normales += 1
                            else:
                                viaje_id = origen_dict_1.get((estacion, estado_str), None)
                                if viaje_id:
                                    line.append(viaje_id)
                                    normales += 1
                    else:
                        line.append(viaje_id)
                        normales += 1

                writer.writerow(line)

print('Proceso Terminado. Encontrados: Vacios {}, Llenos {}, normales {}'.format(vacios, llenos, normales))
