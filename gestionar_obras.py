import peewee as pw
from modelo_orm import sqlite_crear, Obra, Empresa, Etapa, Ubicacion, AreaResponsable, TipoObra,Barrio, EmpresaObra
import pandas as pd
from abc import ABC 
from abc import abstractmethod
import numpy as np

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
            sqlite_crear.create_tables([Etapa, Empresa, Ubicacion, TipoObra, AreaResponsable, Obra, EmpresaObra, Barrio])
            print("Tablas creadas exitosamente.")
        except pw.OperationalError as e:
            print(f"Error al crear las tablas: {e}")
    
    @classmethod
    def limpiar_datos(cls):
        try:
            df = pd.read_csv("observatorio-de-obras-urbanas.csv", sep=";", encoding="utf8")                      
            
            columnasAEliminar = ['ba_elige', 'link_interno', 'pliego_descarga', 'imagen_1', 'imagen_2', 'imagen_3', 'imagen_4', 'estudio_ambiental_descarga', 'entorno', 'compromiso', 'destacada', 'financiamiento']
            
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df = df.drop(columns=columnasAEliminar, axis=1)
            
            df.fillna({'nombre': 'Area ambiental'}, inplace=True)            
            df.fillna({'tipo_obra': 'Salud'}, inplace=True)            
            df.fillna({'descripcion': 'Obra en ejecucion'}, inplace=True)            
            df.fillna({'monto_contrato': '300.000.000'}, inplace=True)            
            df.fillna({'porcentaje_avance': '0'}, inplace=True)            
            df.fillna({'fecha_fin_inicial': '31/12/2024'}, inplace=True)            
            df.fillna({'expediente-numero': '46213850'}, inplace=True)            
            df.fillna({'mano_obra': '10'}, inplace=True)            
            df.fillna({'nro_contratacion': '1816/SIGAF/2014'}, inplace=True)            
            df.fillna({'cuit_contratista': '30505454436'}, inplace=True)            
            df.fillna({'beneficiarios': 'vecinos'}, inplace=True)            
            df.fillna({'contratacion_tipo': 'Licitación Pública'}, inplace=True)
            df.fillna({'licitacion_anio': '2024'}, inplace=True)            
            
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

        # try:
        #     datosEtapa = list(df['etapa'].unique())
        #     for etapa in datosEtapa:
        #         try:
        #             etapa_existente = Etapa.select().where(Etapa.nombre == etapa).first()
                    
        #             if etapa_existente:
        #                 print(f"Etapa ya existente: {etapa}")
        #                 continue

        #             nueva_etapa = Etapa.create(nombre=etapa)
        #             nueva_etapa.save()
        #             print(f"Etapa creada: {etapa}")
                
        #         except Exception as e:
        #             print(f"Error al procesar la etapa '{etapa}': {e}")

        # except Exception as e:
        #     print(f"Error general al cargar datos para Etapa: {e}")
       
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

        #         if not EmpresaObra.select().where(
        #             (EmpresaObra.idEmpresa == empresa) & (EmpresaObra.idObra == obra)
        #         ).exists():
        #             EmpresaObra.create(idEmpresa=empresa, idObra=obra)
        #             print(f"EmpresaObra creada: Empresa='{empresa.licitacionOfertaEmpresa}', Obra='{obra.nombre}'")
        #         else:
        #             print(f"EmpresaObra ya existe para Empresa='{empresa.licitacionOfertaEmpresa}', Obra='{obra.nombre}'")

        #     except Exception as e:
        #         print(f"Error al procesar EmpresaObra para Empresa='{row['licitacion_oferta_empresa']}', Obra='{row['nombre']}': {e}")

        #     except Exception as e:
        #         print(f"Error al cargar datos para EmpresaObra: {e}")

      
        #print("Datos cargados exitosamente.")
        
       

    @classmethod
    def nueva_obra(cls):
        try:
            nombre = input("Ingresar el nombre de la nueva obra: ")          
            try:
                fechaDeInicio = int(input("Ingresar fecha de inicio de obra (solo año, en formato AAAA): "))
            except ValueError:
                print("Error: La fecha de inicio debe ser un número entero.")
                return
            try:
                montoDeContrato = int(input("Ingresar monto de contrato: "))
            except ValueError:
                print("Error: El monto de contrato debe ser un número entero.")
                return
            try:
                nroDeExpediente = int(input("Ingresar nro de expediente: "))
            except ValueError:
                print("Error: El número de expediente debe ser un número entero.")
                return
            manoDeObra = input("Ingresar tipo de mano de obra: ")
            while True:
                tipoObra = input("Ingrese tipo de obra: ")
                try:
                    if TipoObra.objects.filter(nombre=tipoObra).exists():
                        print("El tipo de obra existe.")
                        break
                    else:
                        print("El tipo de obra no existe. Ingrese uno correcto.")
                except Exception as e:
                    print(f"Error al validar el tipo de obra: {e}")
                    return
            while True:
                tipoDeArea = input("Ingrese el tipo de área: ")
                try:
                    if AreaResponsable.objects.filter(nombre=tipoDeArea).exists():
                        print("El tipo de área existe.")
                        break
                    else:
                        print("El tipo de área no existe. Ingrese uno correcto.")
                except Exception as e:
                    print(f"Error al validar el tipo de área: {e}")
                    return
            while True:
                ubicacion = input("Ingrese la ubicación de la obra: ")
                try:
                    if Ubicacion.objects.filter(nombre=ubicacion).exists():
                        print("La ubicación es existente.")
                        break
                    else:
                        print("La ubicación no existe. Ingrese los datos correctamente.")
                except Exception as e:
                    print(f"Error al validar la ubicación: {e}")
                    return
            try:
                nueva_obra = Obra.create(
                    nombre=nombre, 
                    fechaDeInicio=fechaDeInicio,
                    montoDeContrato=montoDeContrato,
                    nroDeExpediente=nroDeExpediente,
                    manoDeObra=manoDeObra
                )
                nueva_obra.save()
                print("Obra creada exitosamente.")
            except Exception as e:
                print(f"Error al crear la nueva obra: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")


    @classmethod
    def obtener_indicadores():
        print("\nListado de todas las áreas responsables:")
        areas = AreaResponsable.select()
        for area in areas:
            print(f"- {area.nombre}")

        print("\nListado de todos los tipos de obra:")
        tipos_obra = TipoObra.select()
        for tipo in tipos_obra:
            print(f"- {tipo.nombre}")

        print("\nCantidad de obras por etapa:")
        etapas = Etapa.select()
        for etapa in etapas:
            cantidad = Obra.select().where(Obra.idEtapa == etapa).count()
            print(f"- {etapa.nombre}: {cantidad} obras")

        print("\nCantidad de obras y monto total de inversión por tipo de obra:")
        tipos_obra = TipoObra.select()
        for tipo in tipos_obra:
            obras_tipo = Obra.select().where(Obra.idTipoObra == tipo)
            cantidad = obras_tipo.count()
            montos = [obra.montoContrato for obra in obras_tipo]
            monto_total = np.sum(montos) if montos else 0
            print(f"- {tipo.nombre}: {cantidad} obras, Inversión total: ${monto_total}")
    

prueba = GestionarObra()

