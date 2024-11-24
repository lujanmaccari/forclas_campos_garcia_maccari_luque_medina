import peewee as pw 
from peewee import fn
from modelo_orm import sqlite_crear, Obra, Empresa, Etapa, Ubicacion, AreaResponsable, TipoObra, Barrio
import pandas as pd
from abc import ABC 
import numpy as np
import random 
import string

class GestionarObra(ABC):
    
    @classmethod
    def extraer_datos(cls, ruta_dataset):
        try:
            df = pd.read_csv("observatorio-de-obras-urbanas.csv", sep=";", encoding="latin-1")
            print("Datos extraídos con éxito.")
            return df
        except FileNotFoundError as e:
            print(f"Error: El archivo {ruta_dataset} no se encuentra. Verifique la ruta.")
            return None
        except pd.errors.EmptyDataError as e:
            print(f"Error: El archivo está vacío.")
            return None
        except pd.errors.ParserError as e:
            print(f"Error: El archivo no puede ser analizado correctamente. Verifique el formato.")
            return None
        except Exception as e:
            print(f"Error inesperado al extraer los datos: {e}")
            return None

    @classmethod
    def conectar_db(cls):
        try:
            cls.db = pw.SqliteDatabase('obras_urbanas.db')
            cls.db.connect()
            print("Conexión a la base de datos exitosa.")
        except pw.OperationalError as e:
            print(f"Error de conexión a la base de datos: {e}")
        except Exception as e:
            print(f"Error inesperado al conectar a la base de datos: {e}")

    @classmethod
    def mapear_orm(cls):
        try:
            sqlite_crear.create_tables([Etapa, Empresa, Ubicacion, TipoObra, AreaResponsable, Obra, Barrio])
            print("Tablas creadas exitosamente.")
        except pw.OperationalError as e:
            print(f"Error al crear las tablas: {e}")
    
    @classmethod
    def limpiar_datos(cls):
        try:
            df = pd.read_csv("observatorio-de-obras-urbanas.csv", sep=";", encoding="utf8")                      
            
            columnasAEliminar = ['ba_elige', 'link_interno', 'pliego_descarga', 'imagen_1', 'imagen_2', 'imagen_3', 'imagen_4', 'estudio_ambiental_descarga', 'entorno', 'compromiso','financiamiento']
            
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df = df.drop(columns=columnasAEliminar, axis=1)
            
            df.fillna({'nombre': 'Area ambiental'}, inplace=True)            
            df.fillna({'tipo_obra': 'Salud'}, inplace=True)            
            df.fillna({'descripcion': 'Obra en ejecucion'}, inplace=True)            
            df.fillna({'monto_contrato': '300.000.000'}, inplace=True)            
            df.fillna({'porcentaje_avance': '0'}, inplace=True)            
            df.fillna({'fecha_fin_inicial': '31/12/2024'}, inplace=True)            
            df['expediente-numero'] = df['expediente-numero'].apply(lambda x: ''.join(random.choices(string.ascii_uppercase + string.digits, k=9)) if pd.isnull(x) else x)
            df.fillna({'mano_obra': '10'}, inplace=True)            
            df.fillna({'nro_contratacion': '1816/SIGAF/2014'}, inplace=True)            
            df.fillna({'cuit_contratista': '30505454436'}, inplace=True)            
            df.fillna({'beneficiarios': 'vecinos'}, inplace=True)            
            df.fillna({'contratacion_tipo': 'Licitación Pública'}, inplace=True)
            df.fillna({'licitacion_anio': '2024'}, inplace=True)  
            df.fillna({'destacada': 'NO'},inplace=True)          
            
            columnas_verificables = [col for col in df.columns if col not in columnasAEliminar]
            
            df = df.dropna(subset=columnas_verificables, how='any')
            
            df.to_csv("datos_limpios_obras_urbanas.csv", sep=";", encoding="utf8", index=False)
                        
            print("Datos limpios guardados en 'datos_limpios_obras_urbanas.csv'.", df)
            return df
        except Exception as e:
            print(f"Error al limpiar los datos: {e}")
            
    @classmethod
    def cargar_datos(cls):
        df = GestionarObra.limpiar_datos()    

        # try:
        #     datosTipoObra = list(df['tipo'].unique())
        #     for tipo in datosTipoObra:
        #         try:
        #             tipo_existente = TipoObra.select().where(TipoObra.nombre == tipo).first()
                    
        #             if tipo_existente:
        #                 print(f"Tipo de obra ya existente: {tipo}")
        #                 continue

        #             tipo_obra = TipoObra.create(nombre=tipo)
        #             tipo_obra.save()
        #             print(f"Tipo de obra creado: {tipo}")
                
        #         except Exception as e:
        #             print(f"Error al procesar el tipo de obra '{tipo}': {e}")

        # except Exception as e:
        #     print(f"Error general al cargar datos para TipoObra: {e}")

        try:
            datosEtapa = list(df['etapa'].unique())
            for etapa in datosEtapa:
                try:
                    etapa_existente = Etapa.select().where(Etapa.nombre == etapa).first()
                    
                    if etapa.lower() == "en obra":
                        etapa = "en ejecución"

                    if etapa_existente:
                        print(f"Etapa ya existente: {etapa}")
                        continue
                    
                    nueva_etapa = Etapa.create(nombre=etapa)
                    nueva_etapa.save()
                    print(f"Etapa creada: {etapa}")

                    
                
                except Exception as e:
                    print(f"Error al procesar la etapa '{etapa}': {e}")

        except Exception as e:
            print(f"Error general al cargar datos para Etapa: {e}")
       
        # try:
        #     for _, row in df[['barrio', 'comuna']].drop_duplicates().iterrows():
        #         try:
        #             # Verificar si el barrio ya existe en la base de datos
        #             barrio_existente = Barrio.select().where(Barrio.nombre == row['barrio']).first()
                    
        #             if barrio_existente:
        #                 print(f"Barrio ya existente: {row['barrio']} - Comuna: {barrio_existente.comuna}")
        #                 continue

        #             Barrio.create(nombre=row['barrio'], comuna=row['comuna'])
        #             print(f"Barrio creado: {row['barrio']} - Comuna: {row['comuna']}")
                
        #         except Exception as e:
        #             print(f"Error al insertar barrio {row['barrio']}: {e}")

        # except Exception as e:
        #     print(f"Error general al cargar datos para Barrio: {e}")

        # try:
        #     for area in df['area_responsable'].unique():
        #         try:
        #             area_existente = AreaResponsable.select().where(AreaResponsable.nombre == area).first()
                    
        #             if area_existente:
        #                 print(f"Área responsable ya existente: {area}")
        #                 continue
        #             AreaResponsable.create(nombre=area)
        #             print(f"Área responsable creada: {area}")
                
        #         except Exception as e:
        #             print(f"Error al insertar área responsable {area}: {e}")

        # except Exception as e:
        #     print(f"Error general al cargar datos para Área Responsable: {e}")
        
        # try:
        #     for _, row in df[['barrio', 'direccion', 'lat', 'lng']].drop_duplicates().iterrows():
        #         try:
        #             barrio = Barrio.get(Barrio.nombre == row['barrio'])

        #             ubicacion_existente = Ubicacion.select().where(
        #                 (Ubicacion.idBarrio == barrio) &
        #                 (Ubicacion.direccion == row['direccion']) &
        #                 (Ubicacion.latitud == row['lat']) &
        #                 (Ubicacion.longitud == row['lng'])
        #             ).first()
                    
        #             if ubicacion_existente:
        #                 print(f"Ubicación ya existente: {row['direccion']} en Barrio: {row['barrio']}")
        #                 continue

                    # Ubicacion.create(
                    #     idBarrio=barrio,
                    #     direccion=row['direccion'],
                    #     latitud=row['lat'],
                    #     longitud=row['lng']
                    # )
        #             print(f"Ubicación creada: {row['direccion']} en Barrio: {row['barrio']}")
                
        #         except Barrio.DoesNotExist:
        #             print(f"Error: El barrio '{row['barrio']}' no existe en la base de datos. Verifica los datos.")
        #         except Exception as e:
        #             print(f"Error inesperado al procesar la ubicación '{row['direccion']}': {e}")

        # except Exception as e:
        #     print(f"Error general al cargar datos para Ubicacion: {e}")
        
       
        # try:
        #     datos_empresas = df[['licitacion_oferta_empresa', 'licitacion_anio', 'cuit_contratista', 
        #                     'nro_contratacion', 'contratacion_tipo', 'area_responsable']].drop_duplicates()
        #     for _, row in datos_empresas.iterrows():
        #         try:
        #             area_responsable = AreaResponsable.get(AreaResponsable.nombre == row['area_responsable'])
        #             empresa_existente = Empresa.select().where(
        #                 (Empresa.licitacionOfertaEmpresa == row['licitacion_oferta_empresa']) &
        #                 (Empresa.cuitContratista == str(row['cuit_contratista'])[:13]) &
        #                 (Empresa.numeroContratacion == row['nro_contratacion'])
        #             ).first()
                    
        #             if empresa_existente:
        #                 print(f"Empresa ya existente: {row['licitacion_oferta_empresa']} - CUIT: {row['cuit_contratista']}")
        #                 continue

        #             Empresa.create(
        #                 licitacionOfertaEmpresa=row['licitacion_oferta_empresa'],
        #                 licitacionAnio=row.get('licitacion_anio', 0),
        #                 tipoContratacion=row.get('contratacion_tipo', 'Desconocido'),
        #                 cuitContratista=str(row['cuit_contratista'])[:13],
        #                 areaContratacion=area_responsable,
        #                 numeroContratacion=row['nro_contratacion']
        #             )
        #             print(f"Empresa creada: {row['licitacion_oferta_empresa']} - CUIT: {row['cuit_contratista']}")
                
        #         except KeyError as ke:
        #             print(f"Error: Falta una columna clave en el DataFrame. Detalles: {ke}")
        #         except ValueError as ve:
        #             print(f"Error de valor: Datos inválidos al crear Empresa. Detalles: {ve}")
        #         except pw.IntegrityError as ie:
        #             print(f"Error de integridad: {ie}")
        #         except Exception as e:
        #             print(f"Error inesperado al insertar empresa: {row.get('licitacion_oferta_empresa', 'Desconocido')}, {e}")

        # except KeyError as ke:
        #     print(f"Error: Falta una columna clave en el DataFrame principal. Detalles: {ke}")
        # except ValueError as ve:
        #     print(f"Error de valor general al procesar datos de empresas. Detalles: {ve}")
        # except Exception as e:
        #     print(f"Error inesperado al procesar datos de empresas: {e}")

        
        # Recorrer el archivo registro por registro y dentro del for pasamos los dtos dl archivo a objetos
        # si es necesario, instanciar una obra y guardarla.Esto podria hacerse en un metodo aparte     

        # try:  
        #     for _, row in df[['tipo', 'area_responsable', 'etapa', 'direccion', 'nombre', 'fecha_inicio', 'fecha_fin_inicial', 'plazo_meses', 'mano_obra', 'expediente-numero', 'porcentaje_avance', 'monto_contrato', 'descripcion']].drop_duplicates().iterrows():
        #         try:
        #             tipoObra = TipoObra.get(TipoObra.nombre == row['tipo'])
        #             areaResponsable = AreaResponsable.get(AreaResponsable.nombre == row['area_responsable'])
        #             etapa = Etapa.get(Etapa.nombre == row['etapa'])
        #             ubicacion = Ubicacion.get(Ubicacion.direccion == row['direccion'])
        #             montoContrato = row['monto_contrato'].replace('$', '').replace(',', '')
                    
        #             obraExistente = Obra.select().where(
        #                 Obra.nombre == row['nombre'],
        #                 Obra.idUbicacion == ubicacion,
        #                 Obra.idTipoObra == tipoObra,
        #                 Obra.idAreaResponsable == areaResponsable,
        #                 Obra.idEtapa == etapa
        #             ).first()
                    
        #             if obraExistente:
        #                 print(f"La obra '{row['nombre']}' ya existe en la base de datos.")
        #                 continue
                    
        #             Obra.create(
        #                 idTipoObra=tipoObra,
        #                 idAreaResponsable=areaResponsable,
        #                 idUbicacion=ubicacion,
        #                 idEtapa=etapa,
        #                 nombre=row['nombre'],
        #                 fechaInicio=row['fecha_inicio'],
        #                 fechaFinIinicial=row['fecha_fin_inicial'],
        #                 plazoMeses=row['plazo_meses'],
        #                 manoObra=row['mano_obra'],
        #                 numeroExpediente=row['expediente-numero'],
        #                 porcentajeAvance=row['porcentaje_avance'],
        #                 montoContrato=montoContrato,
        #                 descripcion=row['descripcion'],
        #                 destacada=row['destacada']
        #             )
        #         except TipoObra.DoesNotExist:
        #             print(f"Error: El tipo de obra '{row['tipo']}' no existe en la base de datos. Verifica los datos.")
        #         except AreaResponsable.DoesNotExist:
        #             print(f"Área responsable '{row['area_responsable']}' no encontrado.")
        #         except Ubicacion.DoesNotExist:
        #             print(f"Ubicación '{row['direccion']}' no encontrada.")
        #         except Etapa.DoesNotExist:
        #             print(f"Etapa '{row['etapa']}' no encontrada.")
        # except Exception as e:
        #     print(f"Error al cargar datos: {e}")


    
        # for _, row in df[['licitacion_oferta_empresa', 'nombre']].drop_duplicates().iterrows():
        #     try:
        #         empresa = Empresa.get_or_none(Empresa.licitacionOfertaEmpresa == row['licitacion_oferta_empresa'])
        #         if not empresa:
        #             print(f"Error: La empresa '{row['licitacion_oferta_empresa']}' no existe en la base de datos.")
        #             continue

        #         obra = Obra.get_or_none(Obra.nombre == row['nombre'])
        #         if not obra:
        #             print(f"Error: La obra '{row['nombre']}' no existe en la base de datos.")
        #             continue

        #         
      
        #print("Datos cargados exitosamente.")
        
       

#     @classmethod
#     def nueva_obra(cls):
#         try:
#             nombre = input("Ingresar el nombre de la nueva obra: ")          
#             try:
#                 fechaDeInicio = int(input("Ingresar fecha de inicio de obra (solo año, en formato AAAA): "))
#             except ValueError:
#                 print("Error: La fecha de inicio debe ser un número entero.")
#                 return
#             try:
#                 montoDeContrato = int(input("Ingresar monto de contrato: "))
#             except ValueError:
#                 print("Error: El monto de contrato debe ser un número entero.")
#                 return
#             try:
#                 nroDeExpediente = int(input("Ingresar nro de expediente: "))
#             except ValueError:
#                 print("Error: El número de expediente debe ser un número entero.")
#                 return
#             manoDeObra = input("Ingresar tipo de mano de obra: ")
#             while True:
#                 tipoObra = input("Ingrese tipo de obra: ")
#                 try:
#                     if TipoObra.objects.filter(nombre=tipoObra).exists():
#                         print("El tipo de obra existe.")
#                         break
#                     else:
#                         print("El tipo de obra no existe. Ingrese uno correcto.")
#                 except Exception as e:
#                     print(f"Error al validar el tipo de obra: {e}")
#                     return
#             while True:
#                 tipoDeArea = input("Ingrese el tipo de área: ")
#                 try:
#                     if AreaResponsable.objects.filter(nombre=tipoDeArea).exists():
#                         print("El tipo de área existe.")
#                         break
#                     else:
#                         print("El tipo de área no existe. Ingrese uno correcto.")
#                 except Exception as e:
#                     print(f"Error al validar el tipo de área: {e}")
#                     return
#             while True:
#                 ubicacion = input("Ingrese la ubicación de la obra: ")
#                 try:
#                     if Ubicacion.objects.filter(nombre=ubicacion).exists():
#                         print("La ubicación es existente.")
#                         break
#                     else:
#                         print("La ubicación no existe. Ingrese los datos correctamente.")
#                 except Exception as e:
#                     print(f"Error al validar la ubicación: {e}")
#                     return
#             try:
#                 nueva_obra = Obra.create(
#                     nombre=nombre, 
#                     fechaDeInicio=fechaDeInicio,
#                     montoDeContrato=montoDeContrato,
#                     nroDeExpediente=nroDeExpediente,
#                     manoDeObra=manoDeObra
#                 )
#                 nueva_obra.save()
#                 print("Obra creada exitosamente.")
#             except Exception as e:
#                 print(f"Error al crear la nueva obra: {e}")
#         except Exception as e:
#             print(f"Ocurrió un error inesperado: {e}")


#     @classmethod
#     def obtener_indicadores(cls):
#         try:
#             print("\nListado de todas las áreas responsables:")
#             areas = AreaResponsable.select()
#             for area in areas:
#                 print(f"- {area.nombre}")

#             print("\nListado de todos los tipos de obra:")
#             tipos_obra = TipoObra.select()
#             for tipo in tipos_obra:
#                 print(f"- {tipo.nombre}")

#             print("\nCantidad de obras por etapa:")
#             etapas = Etapa.select()
#             for etapa in etapas:
#                 cantidad = Obra.select().where(Obra.idEtapa == etapa).count()
#                 print(f"- {etapa.nombre}: {cantidad} obras")

#             print("\nCantidad de obras y monto total de inversión por tipo de obra:")
#             for tipo in tipos_obra:
#                 cantidad = Obra.select().where(Obra.idTipoObra == tipo).count()
#                 monto_total = (
#                 Obra.select(fn.SUM(Obra.montoContrato))
#                 .where((Obra.idTipoObra == tipo) & (Obra.montoContrato.is_null(False)))
#                 .scalar() or 0
#                 )
#                 print(f"- {tipo.nombre}: {cantidad} obras, Inversión total: ${monto_total}")
            
#             print("\nListado de todos los barrios pertenecientes a las comunas 1, 2 y 3:")
#             barrios = Barrio.select().where(Barrio.comuna.in_([1, 2, 3]))
#             for barrio in barrios:
#                 print(f"- {barrio.nombre} (Comuna {barrio.comuna})")

#             print("\nCantidad de obras finalizadas y su monto total de inversion en la Comuna 1")
#             obras_finalizadas_comuna1 = (
#                                         Obra.select()
#                                         .join(Etapa, on=(Obra.idEtapa == Etapa.idEtapa))
#                                         .join(Ubicacion, on=(Obra.idUbicacion == Ubicacion.idUbicacion))
#                                         .join(Barrio, on=(Ubicacion.idBarrio == Barrio.idBarrio))
#                                         .where(
#                                             (Etapa.nombre == "Finalizada") & (Barrio.comuna == 1)
#                                         )
#                                         )
#             cantidad_finalizadas = obras_finalizadas_comuna1.count()
#             monto_total_comuna1 = (
#                                     Obra.select(fn.SUM(Obra.montoContrato))
#                                     .join(Etapa, on=(Obra.idEtapa == Etapa.idEtapa))
#                                     .join(Ubicacion, on=(Obra.idUbicacion == Ubicacion.idUbicacion))
#                                     .join(Barrio, on=(Ubicacion.idBarrio == Barrio.idBarrio))
#                                     .where(
#                                         (Etapa.nombre == "Finalizada") & (Barrio.comuna == 1)
#                                     )
#                                     .scalar() or 0
#             )
#             print(f" Obras Finalizadas en Comuna 1: {cantidad_finalizadas} obras, Inversión total: ${monto_total_comuna1}")

#             print("\nCantidad de obras finalizadas en un plazo menor o igual a 24 meses")
#             obras_finalizadas_24_meses = (
#                 Obra.select()
#                 .join(Etapa, on=(Obra.idEtapa == Etapa.idEtapa))
#                 .where(
#                     (Etapa.nombre == 'Finalizada') & (Obra.plazoMeses <= 24)
#                 )
#             )
#             cantidad_obras_24_meses = obras_finalizadas_24_meses.count()
#             print(f"Cantidad de obras finalizadas: {cantidad_obras_24_meses}")

#             print("\nPorcentaje de obras finalizadas")
#             total_obras = Obra.select().count()
#             obras_finalizadas = Obra.select().join(Etapa, on=(Obra.idEtapa == Etapa.idEtapa)).where(Etapa.nombre == 'Finalizada').count()
#             porcentaje_finalizadas = (obras_finalizadas / total_obras) * 100
#             print(f"Porcentaje de obras finalizadas: {porcentaje_finalizadas}%")

#             print("\nCantidad total de mano de obra empleada")
#             mano_obra_list = [obra.manoObra for obra in Obra.select() if obra.manoObra is not None]
#             mano_obra_list = [int(mano) for mano in mano_obra_list if isinstance(mano, (int, float))]
#             total_mano_obra = np.sum(mano_obra_list) if mano_obra_list else 0
#             print(f"- Total de mano de obra empleada: {total_mano_obra}")

#             print("\nMonto total de inversión:")
#             montos_list = [obra.montoContrato for obra in Obra.select() if obra.montoContrato is not None]
#             montos_list = [int(monto) for monto in montos_list if isinstance(monto, (int, float, str)) and str(monto).isdigit()]
#             monto_total_inversion = np.sum(montos_list) if montos_list else 0
#             print(f"- Monto total de inversión: ${monto_total_inversion}")

#         except Exception as e:
#             print(f"Error al obtener indicadores: {e}")
            
prueba = GestionarObra()
# prueba.obtener_indicadores()
prueba.cargar_datos()

